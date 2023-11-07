# The Truth About Threads
>Let’s be frank for a moment—you really don’t want to use Curio. All things equal,
>you should probably be programming with threads. Yes, threads. THOSE threads. Seriously. I’m not kidding.
>
>&nbsp;&nbsp;&nbsp;—Dave Beazley, [“Developing with Curio”](https://oreil.ly/oXJaC)

<p style='text-align: justify;'>If you’ve never heard of threads before, here’s a basic description: threads are a feature provided by an operating system (OS), made available to software developers so that they may indicate to the OS which parts of their program may be run in parallel. The OS decides how to share CPU resources with each of the parts, much as the OS decides to share CPU resources with all the other different programs (processes) running at the same time.</p>

<p style='text-align: justify'>Since you’re reading an Asyncio book, this must be the part where I tell you, “Threads are terrible, and you should never use them,” right? Unfortunately, the situation is not so simple. We need to weigh the benefits and risks of using threads, just like with any technology choice.</p>

<p style='text-align: justify'>This book is not supposed to be about threads at all. But there are two problems here: Asyncio is offered as an alternative to threading, so it’s hard to understand the value proposition without some comparison; and even when using Asyncio, you will still likely have to deal with threads and processes, so you need to know something about threading.</p>

>The context of this discussion is exclusively concurrency in network programming applications.
>Preemptive multithreading is also used in other domains, where the trade-offs are entirely different.
<hr>

## Benefits of Threading

These are the main benefits of threading:  
- *Ease of reading code*
    - <p style='text-align: justify'>Your code can run concurrently, but still be set out in a very simple, top-down linear sequence of commands to the point where—and this is key—you can pretend, within the body of your functions, that no concurrency is happening.</p>

- *Parallelism with shared memory*
    - <p style='text-align: justify'>Your code can exploit multiple CPUs while still having threads share memory. This is important in many workloads where it would be too costly to move large amounts of data between the separate memory spaces of different processes, for example.</p>

- *Know-how and existing code*
    - <p style='text-align: justify'>There is a large body of knowledge and best practices available for writing threaded applications. There is also a huge amount of existing “blocking” code that depends on multithreading for concurrent operation.</p> 

<p style='text-align: justify'>
Now, with <i>Python</i>, the point about parallelism is questionable because the Python interpreter uses a global lock, called the <i>global interpreter lock</i> (GIL), to protect the internal state of the interpreter itself. That is, it provides protection from the potential catastrophic effects of race conditions between multiple threads. A side effect of the lock is that it ends up pinning all threads in your program to a single CPU. As you might imagine, this negates any parallelism performance benefits (unless you use tools like Cython or Numba to maneuver around the limitation).
</p>
<p style='text-align: justify'>The first point regarding perceived simplicity, however, is significant: threading in Python <i>feels</i> exceptionally simple, and if you haven’t been burned before by impossibly hard race condition bugs, threading offers a very attractive concurrency model. Even if you have been burned in the past, threading remains a compelling option because you will likely have learned (the hard way) how to keep your code both simple and safe.
</p>
<p style='text-align: justify'>I don’t have space to get into safer threaded programming here, but generally speaking, the best practice for using threads is to use the <code>ThreadPoolExecutor</code> class from the <code>concurrent.futures</code> module, passing all required data in through the <code>submit()</code> method. Example 2-1 shows a basic example.
</p>

*Example 2-1. Best practice for threading*
```python
from concurrent.futures import ThreadPoolExecutor as Executor

def worker(data):
    # <process the data>

with Executor(max_workers=10) as exe:
    future = exe.submit(worker, data)
```

<p style='text-align: justify'>The <code>ThreadPoolExecutor</code> offers an extremely simple interface for running functions in a thread—and the best part is that, if needed, you can convert the pool of threads into a pool of subprocesses simply by using <code>ProcessPoolExecutor</code> instead. It has the same API as <code>ThreadPoolExecutor</code>, which means that your code will be little affected by the change. The executor API is also used in <code>asyncio</code> and is described in the next chapter (see Example 3-3).
</p>
<p style='text-align: justify'>In general, you’ll prefer your tasks to be somewhat short-lived, so that when your program needs to shut down, you can simply call <code>Executor.shutdown(wait=True)</code> and wait a second or two to allow the executor to complete.
</p>
<p style='text-align: justify'>Most importantly: if at all possible, you should try to prevent your threaded code (in the preceding example, the <code>worker()</code> function) from accessing or writing to any global variables!
</p>


>Raymond Hettinger presented several great guidelines for safer threaded code at [PyCon Russia 2016](https://oreil.ly/ZZVps) and [PyBay 2017](https://oreil.ly/JDplJ). I strongly urge you to add these videos to your watch list.

## Drawbacks of Threading

> [N]ontrivial multithreaded programs are incomprehensible to humans. It is true that the programming model can be improved through the use of design patterns, better granularity of atomicity (e.g., transactions), improved languages, and formal methods. However, these techniques merely chip away at the unnecessarily enormous nondeterminism of the threading model. The model remains intrinsically intractable.
>
>&nbsp;&nbsp;&nbsp;—Edward A. Lee [“The Problem with Threads”](http://bit.ly/2CFOv8a)

The drawbacks of threading have been mentioned in a few other places already, but for completeness let’s collect them here anyway:
- *Threading is difficult*
    - <p style='text-align: justify'>Threading bugs and race conditions in threaded programs are the hardest kinds of bugs to fix. With experience, it is possible to design new software that is less prone to these problems, but in nontrivial, naively designed software, they can benearly impossible to fix, even by experts. Really!</p>

- *Threads are resource-intensive*
    - <p style='text-align: justify'>Threads require extra operating system resources to create, such as preallocated, per-thread stack space that consumes process virtual memory up front. This is a big problem with 32-bit operating systems, because the address space per process is limited to 3 GB.[1]() Nowadays, with the widespread availability of 64-bit operating systems, virtual memory isn’t as precious as it used to be (addressable space for virtual memory is typically 48 bits; i.e., 256 TiB). On modern desktop operating systems, the physical memory required for stack space for each thread isn’t even allocated by the OS until it is required, including stack space per thread. For example, on a modern, 64-bit Fedora 29 Linux with 8 GB memory, creating 10,000 do-nothing threads with this short snippet:
    ```python
    # threadmem.py
    import os
    from time import sleep
    from threading import Thread
    threads = [
        Thread(target=lambda: sleep(60)) for i in range(10000)
    ]
    [t.start() for t in threads]
    print(f'PID = {os.getpid()}')
    [t.join() for t in threads]
    ```
    </p>

    leads to the following information in top:<br>
    ```
    MiB Mem : 7858.199 total, 1063.844 free, 4900.477 used
    MiB Swap: 7935.996 total, 4780.934 free, 3155.062 used
    
        PID   USER     PR   NI    VIRT    RES     SHR  COMMAND
      15166  caleb     20    0 80.291g 131.1m    4.8m  python3
    ```
    <p style='text-align: justify'>Preallocated virtual memory is a staggering ~80 GB (due to 8 MB stack space perthread!), but resident memory is only ~130 MB. On a 32-bit Linux system, I would be unable to create this many because of the 3 GB user-space address space limit, <i>regardless</i> of actual consumption of physical memory. To get around this problem on 32-bit systems, it is sometimes necessary to decrease the preconfigured stack size, which you can still do in Python today, with <code>threading.stack_size([size])</code>. Obviously, decreasing stack size has implications for runtime safety with respect to the degree to which function calls may be nested, including recursion. Single-threaded coroutines have none of these problems and are a far superior alternative for concurrent I/O. </p>

- *Threading can affect throughput*
    - <p style='text-align: justify'>At very high concurrency levels (say, >5,000 threads), there can also be an impact on throughput due to context-switching costs, assuming you can figure out how to configure your operating system to even allow you to create that many threads! It has become so tedious on recent macOS versions, for example, to test the preceding 10,000 do-nothing-threads example, that I gave up trying to raise the limits at all.</p>
- *Threading is inflexible*
    - <p style='text-align: justify'>The operating system will continually share CPU time with all threads regardless of whether a thread is ready to do work or not. For instance, a thread may be waiting for data on a socket, but the OS scheduler may still switch to and from that thread thousands of times before any actual work needs to be done. (In the async world, the <code>select()</code> system call is used to check whether a socket-awaiting coroutine needs a turn; if not, that coroutine isn’t even woken up, avoiding any switching costs completely.)</p>

<sub>
<hr>
1 The theoretical address space for a 32-bit process is 4 GB, but the operating system typically reserves some of that. Often, only 3 GB is left to the process as addressable virtual memory, but on some operating systems it can be as low as 2 GB. Please take the numbers mentioned in this section as generalizations and not absolutes. There are far too many platform-specific (and historically sensitive) details to get into here.
<hr>
</sub>

<p style='text-align: justify'>None of this information is new, and the problems with threading as a programming model are not platform-specific either. For example, this is what the <a href='http://bit.ly/2Fr3eXK'>Microsoft Visual C++</a> documentation says about threading:
</p>


>The central concurrency mechanism in the Windows API is the thread. You typically use the CreateThread function to create threads. Although threads are relatively easy to create and use, the operating system allocates a significant amount of time and other resources to manage them. Additionally, although each thread is guaranteed to receive the same execution time as any other thread at the same priority level, the associated overhead requires that you create sufficiently large tasks. For smaller or more finegrained tasks, the overhead that is associated with concurrency can outweigh the benefit of running the tasks in parallel.

<p style='text-align: justify'>But—I hear you protest—this is <i>Windows</i>, right? Surely a Unix system doesn’t have these problems? Here follows a similar recommendation from the Mac Developer Library’s <a href='https://oreil.ly/W3mBM'>Threading Programming Guide</a>:
</p>


>Threading has a real cost to your program (and the system) in terms of memory use and performance. Each thread requires the allocation of memory in both the kernel memory space and your program’s memory space. The core structures needed to manage your thread and coordinate its scheduling are stored in the kernel using wired memory. Your thread’s stack space and per-thread data is stored in your program’s memory space. Most of these structures are created and initialized when you first create the thread—a process that can be relatively expensive because of the required interactions with the kernel.


<p style='text-align: justify'>They go even further in the <a href='https://oreil.ly/fcGNL'>Concurrency Programming Guide</a> (emphasis mine):</p>


>In the past, introducing concurrency to an application required the creation of one or more additional threads. Unfortunately, writing threaded code is challenging. Threads are a low-level tool that must be managed manually. Given that the optimal number of threads for an application can change dynamically based on the current system load and the underlying hardware, implementing a correct threading solution becomes extremely difficult, if not impossible to achieve. In addition, the synchronization mechanisms typically used with threads add complexity and risk to software designs without any guarantees of improved performance.


These themes repeat throughout:
- Threading makes code hard to reason about.
- Threading is an inefficient model for large-scale concurrency (thousands of concurrent tasks).

Next, let’s look at a case study involving threads that highlights the first and most important point.

## Case Study: Robots and Cutlery

>Second, and more important, we did not (and still do not) believe in the standard multithreading model, which is preemptive concurrency with shared memory: we still think that no one can write correct programs in a language where “a = a + 1” is not deterministic.
>
>&nbsp;&nbsp;&nbsp;&nbsp;—Roberto Ierusalimschy et al., [“The Evolution of Lua”](http://bit.ly/2Fq9M8P)


<p style='text-align: justify'>At the start of this book, I told the story of a restaurant in which humanoid robots ThreadBots—did all the work. In that analogy, each worker was a thread. In the case study in Example 2-2, we’re going to look at why threading is considered unsafe.</p>

*Example 2-2. ThreadBot programming for table service*
```python
import threading
from queue import Queue

class ThreadBot(threading.Thread): # 1
    def __init__(self):
        super().__init__(target=self.manage_table) # 2
        self.cutlery = Cutlery(knives=0, forks=0) # 3
        self.tasks = Queue() # 4
    
    def manage_table(self):
        while True: # 5
            task = self.tasks.get()
            if task == 'prepare table':
                kitchen.give(to=self.cutlery, knives=4, forks=4) # 6
            elif task == 'clear table':
                self.cutlery.give(to=kitchen, knives=4, forks=4)
            elif task == 'shutdown':
                return
```

1. A `ThreadBot` is a subclass of a thread.

2. The target function of the thread is the `manage_table()` method, defined later in the file.

3. This bot is going to be waiting tables and will need to be responsible for some cutlery. Each bot keeps track of the cutlery that it took from the kitchen here. (The `Cutlery` class will be defined later.)

4. The bot will also be assigned tasks. They will be added to this task queue, and the bot will perform them during its main processing loop, next.

5. The primary routine of this bot is this infinite loop. If you need to shut down a bot, you have to give them the `shutdown` task.

6. There are only three tasks defined for this bot. This one, `prepare table`, is whatthe bot must do to get a new table ready for service. For our test, the only requirement is to get sets of cutlery from the kitchen and place them on the table. `clear table` is used when a table is to be cleared: the bot must return the used cutlery back to the kitchen. `shutdown` just shuts down the bot.

Example 2-3 shows the definition of the `Cutlery` object.
<br>
Example 2-3. Definition of the *Cutlery* object

```python
from attr import attrs, attrib

@attrs # 1
class Cutlery:
    knives = attrib(default=0) # 2
    forks = attrib(default=0)
    
    def give(self, to: 'Cutlery', knives=0, forks=0): # 3
        self.change(-knives, -forks)
        to.change(knives, forks)
    
    def change(self, knives, forks): # 4
        self.knives += knives
        self.forks += forks

kitchen = Cutlery(knives=100, forks=100) # 5
bots = [ThreadBot() for i in range(10)] # 6

import sys

for bot in bots:
    for i in range(int(sys.argv[1])): # 7
        bot.tasks.put('prepare table')
        bot.tasks.put('clear table')
    bot.tasks.put('shutdown') # 8

print('Kitchen inventory before service:', kitchen)
for bot in bots:
    bot.start()

for bot in bots:
    bot.join()
print('Kitchen inventory after service:', kitchen)
```


1. `attrs`, which is an open source Python library that has nothing to do with threads or `asyncio`, is a really wonderful library for making class creation easy. Here, the `@attrs` decorator will ensure that this `Cutlery` class will get all the usual boilerplate code (like `__init__()`) automatically set up.

2. The `attrib()` function provides an easy way to create attributes, including defaults, which you might normally have handled as keyword arguments in the `__init__()` method.

3. This method is used to transfer knives and forks from one `Cutlery` object to another. Typically, it will be used by bots to obtain cutlery from the kitchen for new tables, and to return the cutlery back to the kitchen after a table is cleared.

4. This is a very simple utility function for altering the inventory data in the object instance.

5. We’ve defined `kitchen` as the identifier for the kitchen inventory of cutlery. Typically, each of the bots will obtain cutlery from this location. It is also required that they return cutlery to this store when a table is cleared.

6. This script is executed when testing. For our test, we’ll be using 10 ThreadBots.

7. We get the number of tables as a command-line parameter, and then give each bot that number of tasks for preparing and clearing tables in the restaurant.

8. The `shutdown` task will make the bots stop (so that `bot.join()` a bit further down will return). The rest of the script prints diagnostic messages and starts up the bots.

- *Prepare* a “table for four,” which means obtaining four sets of knives and forks from the kitchen.
- *Clear* a table, which means returning the set of four knives and forks from a table back to the kitchen.

<p style='text-align: justify'>If you run a bunch of ThreadBots over a bunch of tables a specific number of times, you expect that after all the work is done, all of the knives and forks should be back in the kitchen and accounted for.</p>

<p style='text-align: justify'>Wisely, you decide to test that, with one hundred tables to be prepared and cleared by each ThreadBot and all of them operating at the same time, because you want to ensure that they can work together and nothing goes wrong. This is the output of that
<br>test:
</p>

```bash
$ python cutlery_test.py 100
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)
```

<p style='text-align: justify'>All the knives and forks end up back in the kitchen! So, you congratulate yourself on writing good code and deploy the bots. Unfortunately, in <i>practice</i>, every now and then you find that you <i>do not</i> end up with all cutlery accounted for when the restaurant closes. You notice the problem gets worse when you add more bots and/or the place gets busier. Frustrated, you run your tests again, changing nothing except the size of the test (10,000 tables!):</p>

```bash
$ python cutlery_test.py 10000
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=96, forks=108)
```
<p style='text-align: justify'>Oops. Now you see that there is indeed a problem. With 10,000 tables served, you end up with the wrong number of knives and forks left in the kitchen. For reproducibility, you check that the error is consistent:</p>

```bash
$ python cutlery_test.py 10000
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=112, forks=96)
```

<p style='text-align: justify'>There are still errors, but by different amounts compared to the previous run. That’s just ridiculous! Remember, these bots are exceptionally well constructed and they don’t make mistakes. What could be going wrong?</p>

Let’s summarize the situation:

- Your ThreadBot code is very simple and easy to read. The logic is fine.
- You have a working test (with 100 tables) that reproducibly passes.
- You have a longer test (with 10,000 tables) that reproducibly fails.
- The longer test fails in *different*, nonreproducible ways.

<p style='text-align: justify'>These are a few typical signs of a race condition bug. Experienced readers will already have seen the cause, so let’s investigate that now. It all comes down to this method inside our <code>Cutlery</code> class:</p>


```python
def change(self, knives, forks):
    self.knives += knives
    self.forks += forks
```

<p style='text-align: justify'>The inline summation, +=, is implemented internally (inside the C code for the Python interpreter itself) as a few separate steps:</p>

1. Read the current value, `self.knives`, into a temporary location.
2. Add the new value, `knives`, to the value in that temporary location.
3. Copy the new total from the temporary location back into the original location.

<p style='text-align: justify'>The problem with preemptive multitasking is that any thread busy with these steps can be interrupted at <i>any time</i>, and a different thread can be given the opportunity to work through the same steps.
<br>
In this case, suppose ThreadBot A does step 1, and then the OS scheduler pauses A and switches to ThreadBot B. B <i>also</i> reads the current value of <code>self.knives</code>; then execution goes back to A. A increments its total and writes it back—but then B continues from where it got paused (after step 1), and it increments and writes back its new total, thereby <i>erasing</i> the change made by A!
</p>


>While this may sound complex, this example of a race condition is just about the simplest possible case. We were able to check *all* the code, and we even have tests that can reproduce the problem on demand. In the real world, in large projects, try to imagine how much more difficult it can become!

This problem can be fixed by placing a *lock* around the modification of the shared
state (imagine we added a `threading.Lock` to the `Cutlery` class):

```python
def change(self, knives, forks):
    with self.lock:
        self.knives += knives
        self.forks += forks
```

<p style='text-align: justify'>But this requires you to know all the places where state will be shared between multiple threads. This approach is viable when you control all the source code, but it becomes very difficult when many third-party libraries are used—which is likely in Python thanks to the wonderful open source ecosystem.
</p>

<p style='text-align: justify'>Note that it was not possible to see the race condition by looking at the source code alone. This is because the source code provides no hints about where execution is going to switch between threads. That wouldn’t be useful anyway, because the OS can switch between threads just about anywhere.
</p>

<p style='text-align: justify'>Another, much better, solution—and the point of async programming—is to modify our code so that we use only one ThreadBot and configure it to move between <i>all</i> the tables as necessary. For our case study, this means that the knives and forks in the kitchen will get modified by only a single thread.</p>

<p style='text-align: justify'>And even better, in our async programs, we’ll be able to see exactly where context will switch between multiple concurrent coroutines, because the <code>await</code> keyword indicates such places explicitly. I’ve decided against showing an async version of this case study here, because Chapter 3 explains how to use <code>asyncio</code> in depth. But if your curiosity is
insatiable, there is an annotated example in Example B-1; it’ll probably only make sense after you read the next chapter!</p>