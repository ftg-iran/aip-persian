<p align="center">Chapter 3<h1 align="center">Asyncio Walk-Through</h1></p>

> Asyncio provides another tool for concurrent programming in Python, that is more lightweight than threads or multiprocessing. In a very simple sense it does this by having an event loop execute a collection of tasks, with a key difference being that each task chooses when to yield control back to the event loop.
> —Philip Jones, [“Understanding Asyncio”](https://medium.com/@pgjones/understanding-asyncio-a6592a517def)

The asyncio API in Python is complex because it aims to solve different problems for
different groups of people. Unfortunately, very little guidance is available to help you
figure out which parts of asyncio are important for the group you’re in.

My goal is to help you figure that out. There are two main target audiences for the async features in Python:

End-user developers
> These want to make applications using asyncio. I am going to assume that you’re in this group.

Framework developers
> These want to make frameworks and libraries that end-user developers can use in their applications.

Much of the confusion around asyncio in the community today is due to lack of
understanding of this difference. For instance, the official Python documentation for
asyncio is more appropriate for framework developers than end users. This means
that end-user developers reading those docs quickly become shell-shocked by the
apparent complexity. You’re somewhat forced to take it all in before being able to do
anything with it.

---

It is my hope that this book can help you distinguish between the features of Asyncio
that are important for end-user developers and those important for framework
developers.

<img style="float: left;width:120px;height:120px" src="./images/2.png">

If you’re interested in the lower-level details around how concurrency frameworks like Asyncio are built internally, I highly recommend a wonderful talk by Dave Beazley, [“Python Concurrency
from the Ground Up: LIVE!”](https://youtu.be/MCs5OvhV9S4), in which he demonstrates putting
together a simpler version of an async framework like Asyncio.

My goal is to give you only the most basic understanding of the building blocks of
Asyncio—enough that you should be able to write simple programs with it, and cer‐
tainly enough that you will be able to dive into more complete references[^1].

First up, we have a “quickstart” section that introduces the most important building
blocks for Asyncio applications.

### Quickstart

You only need to know about seven functions to use Asyncio [for everyday use].

> —Yury Selivanov, author of PEP 492, which added the async and await keywords to Python.

It’s pretty scary diving into the [official documentation](https://docs.python.org/3/library/asyncio.html) for Asyncio. There are many
sections with new, enigmatic words and concepts that will be unfamiliar to even expe‐
rienced Python programmers, as Asyncio is a very new thing in Python. I’m going to
break all that down and explain how to approach the asyncio module documentation
later, but for now you need to know that the actual surface area you have to worry
about with the asyncio library is much smaller than it seems.

Yury Selivanov, the author of [PEP 492](https://peps.python.org/pep-0492/) and all-round major contributor to async
Python, explained in his PyCon 2016 talk [“async/await in Python 3.5 and Why It Is
Awesome,”](https://youtu.be/m28fiN9y_r8) that many of the APIs in the asyncio module are really intended for
framework designers, not end-user developers. In that talk, he emphasized the main
features that end users should care about. These are a small subset of the whole
asyncio API and can be summarized as follows:

* Starting the asyncio event loop
* Calling async/await functions
* Creating a task to be run on the loop
* Waiting for multiple tasks to complete
* Closing the loop after all concurrent tasks have completed

In this section, we’re going to look at those core features and see how to hit the
ground looping with event-based programming in Python.

The “Hello World” of Asyncio in Python looks like Example 3-1.

Example 3-1. The “Hello World” of Asyncio

```python
# quickstart.py
import asyncio, time
async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
asyncio.run(main()) #1
```

1. asyncio provides a run() function to execute an async def function and all
other coroutines called from there, like sleep() in the main() function.

Here’s the output from running Example 3-1:

```shell
$ python quickstart.py
Sun Aug 18 02:14:34 2019 Hello!
Sun Aug 18 02:14:35 2019 Goodbye!
```

In practice, most of your Asyncio-based code will use the run() function shown here,
but it’s important to understand a little more about what that function is doing for
you. This understanding is important because it will influence how you design larger
applications.

Example 3-2 is what I’ll call a “Hello-ish World” example. It isn’t exactly the same as
what run() does, but it’s close enough to introduce the ideas that we’ll build on
throughout the rest of the book. You’ll need a basic knowledge of coroutines (dis‐
cussed in depth later in this chapter), but try to follow along anyway and focus on the
high-level concepts for now.

Example 3-2. The “Hello-ish World” of Asyncio

```python
# quickstart.py
import asyncio
import time
async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")

loop = asyncio.get_event_loop() #1
task = loop.create_task(main()) #2
loop.run_until_complete(task) #3
pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True) #4
loop.run_until_complete(group) #3
loop.close() #5
```

1. `loop = asyncio.get_event_loop()`

- You need a loop instance before you can run any coroutines, and this is how you get one. In fact, anywhere you call it, `get_event_loop()` will give you the same loop instance each time, as long as you’re using only a single thread [^2]. If you’re inside an async def function, you should call `asyncio.get_running_loop()` instead, which always gives you what you expect. This is covered in much more detail later in the book.

2. `task = loop.create_task(coro)`

- In this case, the specific call is `loop.create_task(main())`. Your coroutine function will not be executed until you do this. We say that create_task() schedules your coroutine to be run on the loop[^3]. The returned task object can be used to monitor the status of the task (for example, whether it is still running or has completed), and can also be used to obtain a result value from your completed coroutine. You can cancel the task with `task.cancel()`.

3. `loop.run_until_complete(coro)`

- This call will block the current thread, which will usually be the main thread. Note that `run_until_complete()` will keep the loop running only until the given coro completes—but all other tasks scheduled on the loop will also run while the loop is running. Internally, `asyncio.run()` calls `run_until_complete()` for you and therefore blocks the main thread in the same way.

4. `group = asyncio.gather(task1, task2, task3)`

- When the “main” part of the program unblocks, either due to a [process signal](https://man7.org/linux/man-pages/man7/signal.7.html) being received or the loop being stopped by some code calling loop.stop(), the code after `run_until_complete()` will run. The standard idiom as shown here is to gather the still-pending tasks, cancel them, and then use `loop.run_until_complete()` again until those tasks are done. gather() is the method for doing the gathering. Note that asyncio.run() will do all of the cancelling, gathering, and waiting for pending tasks to finish up.

5. `loop.close()`

- `loop.close()` is usually the final action: it must be called on a stopped loop, and it will clear all queues and shut down the executor. A stopped loop can be restarted, but a closed loop is gone for good. Internally, `asyncio.run()` will close the loop before returning. This is fine because `run()` creates a new event loop every time you call it.

Example 3-1 shows that if you use asyncio.run(), none of these steps are necessary:
they are all done for you. However, it is important to understand these steps because
more complex situations will come up in practice, and you’ll need the extra knowl‐
edge to deal with them. Several of these are covered in detail later in the book.

<img style="float: left;width:120px;height:120px" src="./images/1.png">

The preceding example is still too simplistic to be useful in a practi‐
cal setting. More information around correct shutdown handling is
required. The goal of the example is merely to introduce the most
important functions and methods in asyncio. More practical infor‐
mation for shutdown handling is presented in “Starting Up and
Shutting Down (Gracefully!)” on page 57.
TODO: internal link
asyncio in Python exposes a great deal of the underlying machinery around the
event loop—and requires you to be aware of aspects like lifecycle management. This
is different from Node.js, for example, which also contains an event loop but keeps it
somewhat hidden away. However, once you’ve worked with asyncio for bit, you’ll
begin to notice that the pattern for starting up and shutting down the event loop
doesn’t stray terribly far from the code presented here. We’ll examine some of the
nuances of managing the loop life cycle in more detail later in the book.

I left something out in the preceding example. The last item of basic functionality
you’ll need to know about is how to run blocking functions. The thing about
cooperative multitasking is that you need all I/O-bound functions to…well, cooper‐
ate, and that means allowing a context switch back to the loop using the keyword
await. Most of the Python code available in the wild today does not do this, and
instead relies on you to run such functions in threads. Until there is more widespread support for async def functions, you’re going to find that using such blocking libraries is unavoidable.

For this, asyncio provides an API that is very similar to the API in the `concur
rent.futures` package. This package provides a ThreadPoolExecutor and a Proces
sPoolExecutor. The default is thread-based, but either thread-based or pool-based
executors can be used. I omitted executor considerations from the previous example
because they would have obscured the description of how the fundamental parts fit
together. Now that those have been covered, we can look at the executor directly.

There are a couple of quirks to be aware of. Let’s have a look at the code sample in Example 3-3.

Example 3-3. The basic executor interface

```python
# quickstart_exe.py
import time
import asyncio
async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')

def blocking(): #1
    time.sleep(0.5) #2
    print(f"{time.ctime()} Hello from a thread!")
loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_in_executor(None, blocking) #3
loop.run_until_complete(task)
pending = asyncio.all_tasks(loop=loop) #4
for task in pending:
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
```

1. `blocking()` calls the traditional time.sleep() internally, which would have
blocked the main thread and prevented your event loop from running. This
means that you must not make this function a coroutine—indeed, you cannot
even call this function from anywhere in the main thread, which is where the
asyncio loop is running. We solve this problem by running this function in an
executor.

TODO: “Waiting for the Executor During Shutdown” on page 68

2. Unrelated to this section, but something to keep in mind for later in the book:
note that the blocking sleep time (0.5 seconds) is shorter than the nonblocking
sleep time (1 second) in the `main()` coroutine. This makes the code sample neat
and tidy. In “Waiting for the Executor During Shutdown” on page 68 we’ll
explore what happens if executor functions outlive their async counterparts during the shutdown sequence.

3. `await loop.run_in_executor(None, func)`

- This is the last of our list of essential, must-know features of asyncio. Sometimes
you need to run things in a separate thread or even a separate process: this
method is used for exactly that. Here we pass our blocking function to be run in
the default executor.[^4] Note that `run_in_executor()` does not block the main
thread: it only schedules the executor task to run (it returns a Future, which
means you can await it if the method is called within another coroutine func‐
tion). The executor task will begin executing only after `run_until_complete()` is
called, which allows the event loop to start processing events.

4. Further to the note in callout 2: the set of tasks in pending does not include an entry for the call to `blocking()` made in `run_in_executor()`. This will be true of any call that returns a Future rather than a Task. The documentation is quite good at specifying return types, so you’ll see the return type there; just remember that `all_tasks()` really does return only Tasks, not Futures.

Here’s the output of running this script:

```shell
$ python quickstart_exe.py
Sun Aug 18 01:20:42 2019 Hello!
Sun Aug 18 01:20:43 2019 Hello from a thread!
Sun Aug 18 01:20:43 2019 Goodbye!
```

Now that you’ve seen the most essential parts of asyncio for end-user developer
needs, it’s time to expand our scope and arrange the asyncio API into a kind of hierarchy. This will make it easier to digest and understand how to take what you need from the documentation, and no more.

### The Tower of Asyncio

As you saw in the preceding section, there are only a handful of commands that you
need to know to be able to use asyncio as an end-user developer. Unfortunately, the
documentation for asyncio presents a huge number of APIs, and it does so in a very
“flat” format that makes it hard to tell which things are intended for common use and which are facilities being provided to framework designers.

When framework designers look at the same documentation, they look for hook
points to which they can connect up their new frameworks or third-party libraries. In this section, we’ll look at asyncio through the eyes of a framework designer to get a sense of how they might approach building a new async-compatible library. Hopefully, this will help to further delineate the features that you need to care about in your own work.

From this perspective, it is much more useful to think about the asyncio module as
being arranged in a hierarchy (rather than a flat list), in which each level is built on top of the specification of the previous level. It isn’t quite as neat as that, unfortunately, and I’ve taken liberties with the arrangement in Table 3-1, but hopefully this will give you an alternative view of the asyncio API.

<img style="float: left;width:120px;height:120px" src="./images/1.png">

Table 3-1, and the names and numbering of the “tiers” given here,
is entirely my own invention, intended to add a little structure to
help explain the asyncio API. The expert reader might arrange
things in a different order, and that’s OK!

Table 3-1. Features of asyncio arranged in a hierarchy; for end-user developers, the most important tiers are highlighted in bold.

TODO: Table

At the most fundamental level, Tier 1, we have the coroutines that you’ve already seen earlier in this book. This is the lowest level at which one can begin to think about designing a third-party framework, and surprisingly, this turns out to be somewhat popular with not one, but two, async frameworks currently available in the wild: [Curio](https://github.com/dabeaz/curio) and [Trio](https://github.com/python-trio/trio). Both of these rely only on native coroutines in Python, and nothing whatsoever from the asyncio library module.

The next level is the event loop. Coroutines are not useful by themselves: they won’t do anything without a loop on which to run them (therefore, necessarily, Curio and Trio implement their own event loops). asyncio provides both a loop specification, `AbstractEventLoop`, and an __implementation__, BaseEventLoop.

The clear separation between specification and implementation makes it possible for third-party developers to make alternative implementations of the event loop, and this has already happened with the uvloop project, which provides a much faster loop implementation than the one in the asyncio standard library module. Importantly, [uvloop](https://github.com/MagicStack/uvloop) simply “plugs into” the hierarchy and replaces only the loop part of the stack. The ability to make these kinds of choices is exactly why the asyncio API has been designed like this, with clear separation between the moving parts.

Tiers 3 and 4 bring us futures and tasks, which are very closely related; they’re separated only because Task is a subclass of Future, but they could easily be considered to be in the same tier. A Future instance represents some sort of ongoing action that will return a result via notification on the event loop, while a Task represents a coroutine running on the event loop. The short version is: a future is “loop-aware,” while a task is both “loop-aware” and “coroutine-aware.” As an end-user developer, you will be working with tasks much more than futures, but for a framework designer, the proportion might be the other way around, depending on the details.

Tier 5 represents the facilities for launching, and awaiting on work that must be run in a separate thread, or even in a separate process.

Tier 6 represents additional async-aware tools such as asyncio.Queue. I could have
placed this tier after the network tiers, but I think it’s neater to get all of the
coroutine-aware APIs out of the way first, before we look at the I/O layers. The Queue provided by asyncio has a very similar API to the thread-safe Queue in the queue module, except that the asyncio version requires the await keyword on get() and put(). You cannot use queue.Queue directly inside coroutines because its get() will block the main thread.

Finally, we have the network I/O tiers, 7 through 9. As an end-user developer, the
most convenient API to work with is the streams API at Tier 9. I have positioned the streams API at the highest level of abstraction in the tower. The protocols API, immediately below that (Tier 8), is a more fine-grained API; you can use the protocols tier in all instances where you might use the streams tier, but using streams will be simpler. The final network I/O tier is the transport tier (Tier 7). It is unlikely you will ever have to work with this tier directly, unless you’re creating a framework for others to use and you need to customize how the transports are set up.

In “Quickstart” on page 22, we looked at the absolute bare minimum that one would
need to know to get started with the asyncio library. Now that we’ve had a look at
how the entire asyncio library API is put together, I’d like to revisit that short list of features and reemphasize which parts you are likely to need to learn.

These are the tiers that are most important to focus on when learning how to use the asyncio library module for writing network applications:

Tier 1

- Understanding how to write async def functions and use await to call and exe‐
cute other coroutines is essential.

Tier 2

- Understanding how to start up, shut down, and interact with the event loop is
essential.

Tier 5

- Executors are necessary to use blocking code in your async application, and the
reality is that most third-party libraries are not yet asyncio-compatible. A good
example of this is the SQLAlchemy database ORM library, for which no featurecomparable alternative is available right now for asyncio.

Tier 6

- If you need to feed data to one or more long-running coroutines, the best way to
do that is with asyncio.Queue. This is exactly the same strategy as using
queue.Queue for distributing data between threads. The Asyncio version of
Queue uses the same API as the standard library queue module, but uses corou‐
tines instead of the blocking methods like get().

Tier 9

- The streams API gives you the simplest way to handle socket communication
over a network, and it is here that you should begin prototyping ideas for
network applications. You may find that more fine-grained control is needed, and
then you could switch to the protocols API, but in most projects it’s usually best
to keep things simple until you know exactly what problem you’re trying to solve.

Of course, if you’re using an asyncio-compatible third-party library that handles all the socket communication for you, like aiohttp, you won’t need to directly work with the asyncio network tiers at all. In this case, you must rely heavily on the documentation provided with the library.

The asyncio library tries to provide sufficient features for both end-user developers and framework designers. Unfortunately, this means that the asyncio API can appear somewhat sprawling. I hope that this section has provided enough of a road map to help you pick out the parts you need.

In the next sections, we’re going to look at the component parts of the preceding list in more detail.

<img style="float: left;width:120px;height:120px" src="./images/2.png">

The [pysheeet](https://www.pythonsheets.com/notes/python-asyncio.html) site provides an in-depth summary (or “cheat sheet”)
of large chunks of the asyncio API; each concept is presented with
a short code snippet. The presentation is dense, so I wouldn’t rec‐
ommend it for beginners, but if you have experience with Python
and you’re the kind of person who “gets it” only when new pro‐
gramming info is presented in code, this is sure to be a useful
resource.

### Coroutines

Let’s begin at the very beginning: what is a coroutine?

My goal in this section is to help you understand the specific meaning behind terms like coroutine object and asynchronous function. The examples that follow will show low-level interactions not normally required in most programs; however, the examples will help give you a clearer understanding of the fundamental parts of Asyncio, and will make later sections much easier to grasp.

The following examples can all be reproduced in a Python 3.8 interpreter in interactive mode, and I urge you to work through them on your own by typing them yourself, observing the output, and perhaps experimenting with different ways of interacting with async and await.

<img style="float: left;width:120px;height:170px" src="./images/1.png">

asyncio was first added to Python 3.4, but the new syntax for coro‐
utines using async def and await was only added in Python 3.5.
How did people do anything with asyncio in 3.4? They used gener‐
ators in very special ways to act as if they were coroutines. In some
older codebases, you’ll see generator functions decorated with
`@asyncio.coroutine` and containing yield from statements.
Coroutines created with the newer async def are now referred to
as native coroutines because they are built into the language as
coroutines and nothing else. This book ignores the older generatorbased coroutines entirely.

### The New async def Keywords

Let us begin with the simplest possible thing, shown in Example 3-4.

Example 3-4. Async functions are functions, not coroutines

```shell
>>> async def f(): #1
...     return 123
...
>>> type(f) #2
<class 'function'>
>>> import inspect #3
>>> inspect.iscoroutinefunction(f) #4
True
```

1. This is the simplest possible declaration of a coroutine: it looks like a regular
function, except that it begins with the keywords async def.

2. Surprise! The precise type of f is not “coroutine”; it’s just an ordinary function. While it is common to refer to async def functions as coroutines, strictly speaking they are considered by Python to be coroutine functions. This behavior is identical to the way generator functions work in Python:

```python
>>> def g():
...     yield 123
...
>>> type(g)
<class 'function'>
>>> gen = g()
>>> type(gen)
<class 'generator'>
```

- Even though g is sometimes incorrectly referred to as a “generator,” it remains a
function, and it is only when this function is evaluated that the generator is
returned. Coroutine functions work in exactly the same way: you need to call the
async def function to obtain the coroutine object

3. The inspect module in the standard library can provide much better introspec‐
tive capabilities than the type() built-in function.

4. There is an iscoroutinefunction() function that lets you distinguish between
an ordinary function and a coroutine function.

Returning to our async def f(), Example 3-5 reveals what happens when we call it.

Example 3-5. An async def function returns a coroutine object

```python
>>> coro = f()
>>> type(coro)
<class 'coroutine'>
>>> inspect.iscoroutine(coro)
True
```

This brings us back to our original question: what exactly is a coroutine? A coroutine is an object that encapsulates the ability to resume an underlying function that has been suspended before completion. If that sounds familiar, it’s because coroutines are very similar to generators. Indeed, before the introduction of native coroutines with the async def and await keywords in Python 3.5, it was already possible to use the asyncio library in Python 3.4 by using normal generators with special decorators[^5]. It isn’t surprising that the new async def functions (and the coroutines they return) behave in a similar way to generators.

We can play with coroutine objects a bit more to see how Python makes use of them. Most importantly, we want to see how Python is able to “switch” execution between coroutines. Let’s first look at how the return value can be obtained.

When a coroutine returns, what really happens is that a StopIteration exception is raised. Example 3-6, which continues in the same session as the previous examples, makes that clear.

Example 3-6. Coroutine internals: using send() and StopIteration

```python
>>> async def f():
...     return 123
>>> coro = f()
>>> try:
...     coro.send(None) #1
... except StopIteration as e:
...     print('The answer was:', e.value) #2
...
The answer was: 123
```

1. A coroutine is initiated by “sending” it a None. Internally, this is what the event
loop is going to be doing to your precious coroutines; you will never have to do
this manually. All the coroutines you make will be executed either with
loop.create_task(coro) or await coro. It’s the loop that does the .send(None)
behind the scenes.

2. When the coroutine returns, a special kind of exception is raised, called StopIter
ation. Note that we can access the return value of the coroutine via the value
attribute of the exception itself. Again, you don’t need to know that it works like
this: from your point of view, async def functions will simply return a value with
the return statement, just like normal functions.

These two points, the send() and the StopIteration, define the start and end of the
executing coroutine, respectively. So far this just seems like a really convoluted way to
run a function, but that’s OK: the event loop will be responsible for driving coroutines
with these low-level internals. From your point of view, you will simply schedule
coroutines for execution on the loop, and they will get executed top-down, almost
like normal functions.

The next step is to see how the execution of the coroutine can be suspended.

### The New await Keyword

This new keyword [await](https://peps.python.org/pep-0492/#await-expression) always takes a parameter and will accept only a thing called
an awaitable, which is defined as one of these (exclusively!):

* A coroutine (i.e., the result of a called async def function)[^6].
* Any object implementing the __await__() special method. That special method
must return an iterator.

The second kind of awaitable is out of scope for this book (you’ll never need it in dayto-day asyncio programming), but the first use case is pretty straightforward, as
Example 3-7 shows.

Example 3-7. Using await on a coroutine

```python
async def f():
    await asyncio.sleep(1.0)
    return 123
async def main():
    result = await f() #1
    return result
```

1. Calling f() produces a coroutine; this means we are allowed to await it. The
value of the result variable will be 123 when f() completes.

Before we close out this section and move on to the event loop, it is useful to look at
how coroutines may be fed exceptions. This is most commonly used for cancellation:
when you call task.cancel(), the event loop will internally use coro.throw() to
raise asyncio.CancelledError inside your coroutine (Example 3-8).

Example 3-8. Using `coro.throw()` to inject exceptions into a coroutine

``` python
>>> coro = f() #1
>>> coro.send(None)
>>> coro.throw(Exception, 'blah') #2
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
 File "<stdin>", line 2, in f
Exception: blah
blah
```

1. As before, a new coroutine is created from the coroutine function f().

2. Instead of doing another send(), we call throw() and provide an exception class
and a value. This raises an exception inside our coroutine, at the await point.

The throw() method is used (internally in asyncio) for task cancellation, which we
can also demonstrate quite easily. We’re even going to go ahead in Example 3-9 and
handle the cancellation inside a new coroutine.

Example 3-9. Coroutine cancellation with CancelledError

``` python
>>> import asyncio
>>> async def f():
...     try:
...         while True: await asyncio.sleep(0)
...     except asyncio.CancelledError: #1
...         print('I was cancelled!') #2
...     else:
...         return 111
>>> coro = f()
>>> coro.send(None)
>>> coro.send(None)
>>> coro.throw(asyncio.CancelledError) #3
I was cancelled! #4
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
StopIteration #5
```

1. Our coroutine function now handles an exception. In fact, it handles the specific exception type used throughout the asyncio library for task cancellation:
asyncio.CancelledError. Note that the exception is being injected into the coroutine from outside; i.e., by the event loop, which we’re still simulating with
manual send() and throw() commands. In real code, which you’ll see later,
CancelledError is raised inside the task-wrapped coroutine when tasks are
cancelled.

2. A simple message to say that the task got cancelled. Note that by handling the
exception, we ensure it will no longer propagate and our coroutine will `return`.

3. Here we throw() the CancelledError exception.

4. As expected, we see our cancellation message being printed.

5. Our coroutine exits normally. (Recall that the `StopIteration` exception is the
normal way that coroutines exit.)

Just to drive home the point about how task cancellation is nothing more than regu‐
lar exception raising (and handling), let’s look at Example 3-10, where we absorb cancellation and move on to a different coroutine.

Example 3-10. For educational purposes only—don’t do this!

``` python
>>> async def f():
...     try:
...         while True: await asyncio.sleep(0)
...     except asyncio.CancelledError:
...         print('Nope!')
...         while True: await asyncio.sleep(0) #1
...     else:
...         return 111
>>> coro = f()
>>> coro.send(None)
>>> coro.throw(asyncio.CancelledError) #2
Nope!
>>> coro.send(None) #3
```

1. Instead of printing a message, what happens if after cancellation, we just go right
back to awaiting another awaitable?

2. Unsurprisingly, our outer coroutine continues to live, and it immediately sus‐
pends again inside the new coroutine.

3. Everything proceeds normally, and our coroutine continues to suspend and
resume as expected.

Of course, it should go without saying that you should never actually do this! If your coroutine receives a cancellation signal, that is a clear directive to do only whatever cleanup is necessary and exit. Don’t just ignore it.

By this point, it’s getting pretty tiring pretending to be an event loop by manually doing all the .send(None) calls, so in Example 3-11 we’ll bring in the loop provided by asyncio and clean up the preceding example accordingly.

Example 3-11. Using the event loop to execute coroutines.

``` python
>>> async def f():
...     await asyncio.sleep(0)
...     return 111
>>> loop = asyncio.get_event_loop() #1
>>> coro = f()
>>> loop.run_until_complete(coro) #2
111
```

1. Obtain a loop.

2. Run the coroutine to completion. Internally, this is doing all those .send(None)
method calls for us, and it detects completion of our coroutine with the
StopIteration exception, which also contains our return value.

### Event Loop

The preceding section showed how the send() and throw() methods can interact
with a coroutine, but that was just to help you understand how coroutines themselves are structured. The event loop in asyncio handles all of the switching between coroutines, as well as catching those StopIteration exceptions—and much more, such as  listening to sockets and file descriptors for events.

You can get by without ever needing to work with the event loop directly: your asyncio code can be written entirely using `await` calls, initiated by an `asyncio.run(coro)` call. However, at times some degree of interaction with the event loop itself might be necessary, and here we’ll discuss how to obtain it.

There are two ways:

*__Recommended__*

> `asyncio.get_running_loop()`, callable from inside the context of a coroutine

*__Discouraged__*

> `asyncio.get_event_loop()`, callable from anywhere

You’re going to see the discouraged function in much existing code, because the newer function, get_running_loop(), was introduced much later, in Python 3.8. Thus, it will be useful in practice to have a basic idea of how the older method works, so we’ll look at both. Let’s start with Example 3-12.

Example 3-12. Always getting the same event loop

``` python
>>> loop = asyncio.get_event_loop()
>>> loop2 = asyncio.get_event_loop()
>>> loop is loop2 #1
True
```

1. Both identifiers, loop and loop2, refer to the same instance.

This means that if you’re inside a coroutine function and you need access to the loop instance, it’s fine to call `get_event_loop()` or get_running_loop() to obtain it. You do not need to pass an explicit loop parameter through all your functions.

The situation is different if you’re a framework designer: it would be better to design your functions to accept a loop parameter, just in case your users are doing something unusual with [event loop policies](https://docs.python.org/3/library/asyncio-policy.html#asyncio-policies). Policies are out of scope for this book, and we’ll say no more about them.

So if `get_event_loop()` and `get_running_loop()` work the same, why do they both exist? The `get_event_loop()` method works only within the same thread. In fact, `get_event_loop()` will fail if called inside a new thread unless you specifically create a new loop with `new_event_loop()`, and set that new instance to be the loop for that thread by calling `set_event_loop()`. Most of us will only ever need (and want!) a single loop instance running in a single thread. This is nearly the entire point of async programming in the first place.

In contrast, `get_running_loop()` (the recommended method) will always do what you expect: because it can be called only within the context of a coroutine, a task, or a function called from one of those, it always provides the current running event loop, which is almost always what you want.

The introduction of `get_running_loop()` has also simplified the spawning of background tasks. Consider Example 3-13, a coroutine function inside which additional tasks are created and not awaited.

Example 3-13. Creating tasks

``` python
async def f():
    # Create some tasks!
    loop = asyncio.get_event_loop()
for i in range():
    loop.create_task(<some other coro>)
```

In this example, the intention is to launch completely new tasks inside the coroutine. By not awaiting them, we ensure they will run independently of the execution context inside coroutine function f(). In fact, f() will exit before the tasks that it launched have completed.

Before Python 3.7, it was necessary to first obtain the loop instance to schedule a task, but with the introduction of get_running_loop() came other asyncio functions that use it, like asyncio.create_task(). From Python 3.7 on, the code to spawn an async task now looks like Example 3-14.

Example 3-14. Creating tasks the modern way

``` python
import asyncio
async def f():
    # Create some tasks!
    for i in range():
        asyncio.create_task(<some other coro>)
```

It is also possible to use another low-level function called `asyncio.ensure_future()` to spawn tasks in the same way as create_task(), and you will likely still see calls to `ensure_future()` in older asyncio code. I considered avoiding the distraction of discussing `ensure_future()`, but it is a perfect case study of an asyncio API that was intended only for framework designers, but made the original adoption of asyncio much more difficult to understand for application developers. The difference between `asyncio.create_task()` and `asyncio.ensure_future()` is subtle and confusing for many newcomers. We explore these differences in the next section.

### Tasks and Futures

Earlier we covered coroutines, and how they need to be run on a loop to be useful. Now I want to talk briefly about the Task and Future APIs. The one you will work with the most is Task, as most of your work will involve running coroutines with the `create_task()` function, exactly as set out in “Quickstart” on page 22. The Future class is actually a superclass of Task, and it provides all of the functionality for interaction with the loop.

TODO: “Quickstart” on page 22

A simple way to think of it is like this: a Future represents a future completion state of some activity and is managed by the loop. A Task is exactly the same, but the specific “activity” is a coroutine— probably one of yours that you created with an async def function plus `create_task()`.

The Future class represents a state of something that is interacting with a loop. That description is too fuzzy to be useful, so you can instead think of a Future instance as a toggle for completion status. When a Future instance is created, the toggle is set to “not yet completed,” but at some later time it will be “completed.” In fact, a Future instance has a method called done() that allows you to check the status, as shown in Example 3-15.

Example 3-15. Checking completion status with done()

``` python
>>> from asyncio import Future
>>> f = Future()
>>> f.done()
False
```

A Future instance may also do the following:

* Have a “result” value set (use .set_result(value) to set it and .result() to obtain it)

* Be cancelled with .cancel() (and check for cancellation with .cancelled())

* Have additional callback functions added that will be run when the future completes

Even though Tasks are more common, you can’t avoid Futures entirely: for instance, running a function on an executor will return a Future instance, not a Task. Let’s take a quick look at Example 3-16 to get a feel for what it is like to work with a Future instance directly.

Example 3-16. Interaction with a Future instance

``` python
>>> import asyncio
>>>
>>> async def main(f: asyncio.Future): #1
...     await asyncio.sleep(1)
...     f.set_result('I have finished.') #2
...
>>> loop = asyncio.get_event_loop()
>>> fut = asyncio.Future() #3
>>> print(fut.done()) #4
False
>>> loop.create_task(main(fut)) #5 
<Task pending name='Task-1' coro=<main() running at <console>:1>>
>>> loop.run_until_complete(fut) #6
'I have finished.'
>>> print(fut.done())
True
>>> print(fut.result()) #7
I have finished.
```

1. Create a simple main function. We can run this, wait for a bit, and then set a result on this Future, f.

2. Set the result.

3. Manually create a Future instance. Note that this instance is (by default) tied to our loop, but it is not and will not be attached to any coroutine (that’s what Tasks are for).

4. Before doing anything, verify that the future is not done yet.

5. Schedule the `main()` coroutine, passing the future. Remember, all the `main()` coroutine does is sleep and then toggle the Future instance. (Note that the `main()` coroutine will not start running yet: coroutines run only when the loop is running.)

6. Here we use `run_until_complete()` on a Future instance, rather than a Task instance[^7]. This is different from what you’ve seen before. Now that the loop is running, the `main()` coroutine will begin executing.

7. Eventually, the future completes when its result is set. After completion, the result can be accessed.

Of course, it is unlikely that you will work with Future directly in the way shown here; the code sample is for education purposes only. Most of your contact with `asyncio` will be through Task instances.

You might wonder what happens if you call set_result() on a Task instance. It was possible to do this before Python 3.8, but it is no longer allowed. Task instances are wrappers for coroutine objects, and their result values can be set only internally as the result of the underlying coroutine function, as shown in Example 3-17.

Example 3-17. Calling set_result() on a Task
TODO: 
``` python
>>> import asyncio
>>> from contextlib import suppress
>>>
>>> async def main(f: asyncio.Future):
...     await asyncio.sleep(1)
...     try:
...         f.set_result('I have finished.') #2
...     except RuntimeError as e:
...         print(f'No longer allowed: {e}')
...         f.cancel() #3
...
>>> loop = asyncio.get_event_loop()
>>> fut = asyncio.Task(asyncio.sleep(1_000_000)) #1
>>> print(fut.done())
False
>>> loop.create_task(main(fut))
<Task pending name='Task-2' coro=<main() running at <console>:1>>
>>> with suppress(asyncio.CancelledError):
... loop.run_until_complete(fut)
...
No longer allowed: Task does not support set_result operation
>>> print(fut.done())
True
>>> print(fut.cancelled()) #3
True
```

1. The only difference is that we create a Task instance instead of a Future. Of course, the Task API requires us to provide a coroutine; we just use sleep() because it’s convenient.

2. A Task instance is being passed in. It satisfies the type signature of the function (because Task is a subclass of Future), but since Python 3.8, we’re no longer allowed to call set_result() on a Task: an attempt will raise RuntimeError. The idea is that a Task represents a running coroutine, so the result should always come only from that.

3. We can, however, still cancel() a task, which will raise CancelledError inside the underlying coroutine.

### Create a Task? Ensure a Future? Make Up Your Mind!

TODO: internal link

In “Quickstart” on page 22, I said that the way to run coroutines was to use `asyncio.create_task()`. Before that function was introduced, it was necessary to obtain a loop instance and use loop.create_task() to do the same thing. This can, in fact, also be achieved with a different module-level function: `asyncio.ensure_future()`. Some developers recommended create_task(), while
others recommended ensure_future().

During my research for this book, I became convinced that the API method `asyncio.ensure_future()` is responsible for much of the widespread misunderstanding about the asyncio library. Much of the API is really quite clear, but there are a few bad stumbling blocks to learning, and this is one of them. When you come across `ensure_future()`, your brain works very hard to integrate it into your mental model of how asyncio should be used—and likely fails!

The problem with ensure_future() is highlighted by this now-infamous explanation
in the [Python 3.6 asyncio documentation](https://python.readthedocs.io/en/stable/library/asyncio-task.html):

`asyncio.ensure_future(coro_or_future, *, _loop=None)`

> Schedule the execution of a coroutine object: wrap it in a future. Return a Task object. If the argument is a Future, it is returned directly.

What!? When I first read this, it was very confusing. Here is a (hopefully) clearer
description of `ensure_future()`:

* If you pass in a coroutine, it will produce a Task instance (and your coroutine will be scheduled to run on the event loop). This is identical to calling `asyncio.create_task()` (or `loop.create_task()`) and returning the new Task instance.

* If you pass in a Future instance (or a Task instance, because Task is a subclass of Future), you get that very same thing returned, unchanged. Yes, really!

This function is a great example of the difference between the asyncio API that is aimed at end-user developers (the high-level API) and the asyncio API aimed at framework designers (the low-level API). Let’s have a closer look at how it works, in Example 3-18.

Example 3-18. A closer look at what ensure_future() is doing

``` python
import asyncio

async def f(): #1
 pass

coro = f() #2
loop = asyncio.get_event_loop() #3

task = loop.create_task(coro) #4
assert isinstance(task, asyncio.Task) #5

new_task = asyncio.ensure_future(coro) #6
assert isinstance(new_task, asyncio.Task)

mystery_meat = asyncio.ensure_future(task) #7
assert mystery_meat is task #8
```

1. A simple do-nothing coroutine function. We just need something that can make a coroutine

2. We make the coroutine object by calling the function directly. Your code will rarely do this, but I want to be explicit here (a few lines down) that we’re passing a coroutine object into each of create_task() and ensure_future().

3. Obtain the loop.

4. First off, we use loop.create_task() to schedule our coroutine on the loop, and we get a new Task instance back.

5. We verify the type. So far, nothing interesting.

6. We show that asyncio.ensure_future() can be used to perform the same act as create_task(): we passed in a coroutine and we got back a Task instance (and the coroutine has been scheduled to run on the loop)! If you’re passing in a coroutine, there is no difference between loop.create_task() and asyncio.ensure_future().

7. But what happens if we pass a Task instance to ensure_future()? Note that we’re passing in a Task instance that was already created by loop.create_task() in step 4.

8. We get back exactly the same Task instance as we passed in: it passes through unchanged.

What’s the point of passing Future instances straight through? And why do two different things with the same function? The answer is that `ensure_future()` is
intended to be used by framework authors to provide APIs to end-user developers that can handle both kinds of parameters. Don’t believe me? Here it is from the ex-BDFL himself:

> The point of ensure_future() is if you have something that could either be a coroutine or a Future (the latter includes a Task because that’s a subclass of Future), and you want to be able to call a method on it that is only defined on Future (probably about the only useful example being cancel()). When it is already a Future (or Task), this does nothing; when it is a coroutine, it wraps it in a Task.

> If you know that you have a coroutine and you want it to be scheduled, the correct API to use is create_task(). The only time when you should be calling ensure_future() is when you are providing an API (like most of asyncio’s own APIs) that accepts either a coroutine or a Future and you need to do something to it that requires you to have a Future.

—Guido van Rossum, [commenting](https://github.com/python/asyncio/issues/477#issuecomment-268709555) on [issue #477](https://github.com/python/asyncio/issues/477)

In sum, asyncio.ensure_future() is a helper function intended for framework designers. This is easiest to explain by analogy to a much more common kind of function, so let’s do that. If you have a few years’ programming experience behind you, you may have seen functions similar to the listify() function in Example 3-19.

Example 3-19. A utility function for coercing input into a list

``` python
def listify(x: Any) -> List:
    """ Try hard to convert x into a list """
    if isinstance(x, (str, bytes)):
        return [x]
    try:
        return [_ for _ in x]
    except TypeError
        return [x]
```

This function tries to convert the argument into a list, no matter what comes in. These kinds of functions are often used in APIs and frameworks to coerce inputs into a known type, which simplifies subsequent code—in this case, you know that the parameter (output from `listify()`) will always be a list.

If I rename the `listify()` function to `ensure_list()`, then you should begin to see the parallel with `asyncio.ensure_future()`: it tries to always coerce the argument into a Future (or subclass) type. This is a utility function to make life easier for framework developers, not end-user developers like you and I.

Indeed, the asyncio standard library module itself uses `ensure_future()` for exactly this reason. When next you look over the API, everywhere you see a function parameter described as “awaitable objects,” it is likely that internally `ensure_future()` is being used to coerce the parameter. For example, the `asyncio.gather()` function has the following signature:

``` python
asyncio.gather(*aws, loop=None, ...)
```

The aws parameter means “awaitable objects,” which includes coroutines, tasks, and futures. Internally, gather() is using ensure_future() for type coercion: tasks and futures are left untouched, while tasks are created for coroutines.

The key point here is that as an end-user application developer, you should never need to use asyncio.ensure_future(). It’s more a tool for framework designers. If you need to schedule a coroutine on the event loop, just do that directly with `asyncio.create_task()`.

In the next few sections, we’ll go back to language-level features, starting with asynchronous context managers.

### Async Context Managers: async with

Support for coroutines in context managers turns out to be exceptionally convenient.
This makes sense, because many situations require network resources—say,
connections—to be opened and closed within a well-defined scope.

The key to understanding async with is to realize that the operation of a context
manager is driven by method calls, and then consider: what if those methods were
coroutine functions? Indeed, this is exactly how it works, as shown in Example 3-20.

Example 3-20. Async context manager

``` python
class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    async def __aenter__(self): #1
        self.conn = await get_conn(self.host, self.port)
        return conn
    async def __aexit__(self, exc_type, exc, tb): #2
        await self.conn.close()
async with Connection('localhost', 9001) as conn:
    <do stuff with conn>
```

1. Instead of the `__enter__()` special method for synchronous context managers,
the new `__aenter__()` special method is used. This special method must be an
async def method.

2. Likewise, instead of `__exit__()`, use `__aexit__()`. The parameters are identical
to those for `__exit__()` and are populated if an exception was raised in the body
of the context manager.

<img style="float: left;width:120px;height:120px" src="./images/1.png">

Just because you’re using asyncio in your program, that doesn’t
mean that all your context managers must be async ones like these.
They’re useful only if you need to await something inside the enter
and exit methods. If there is no blocking I/O code, just use regular
context managers.

Now—between you and me—I don’t much like using this explicit style of context manager when the wonderful @contextmanager decorator exists in the contextlib module of the standard library. As you might guess, an asynchronous version, `@asynccontextmanager`, also exists and makes it much easier to create simple async context managers.

### The contextlib Way

This approach is analogous to the `@contextmanager` decorator in the contextlib standard library. To recap, Example 3-21 takes a look at the blocking way first.

Example 3-21. The blocking way

``` python
from contextlib import contextmanager

@contextmanager #1
def web_page(url):
    data = download_webpage(url) #2
    yield data
    update_stats(url) #3

with web_page('google.com') as data: #4
    process(data) #5
```

1. The @contextmanager decorator transforms a generator function into a context
manager

2. This function call (which I made up for this example) looks suspiciously like the sort of thing that will want to use a network interface, which is many orders of magnitude slower than “normal” CPU-bound code. This context manager must be used in a dedicated thread; otherwise, the whole program will be paused while waiting for data.

3. Imagine that we update some statistics every time we process data from a URL, such as the number of times the URL has been downloaded. From a concurrency perspective, we would need to know whether this function involves I/O inter‐ nally, such as writing to a database over a network. If so, update_stats() is also a blocking call.

4. Our context manager is being used. Note specifically how the network call (to download_webpage()) is hidden inside the construction of the context manager.

5. This function call, process(), might also be blocking. We’d have to look at what the function does, because the distinction between what is blocking or nonblocking is not clear-cut. It might be:

* Innocuous and nonblocking (fast and CPU-bound)
* Mildly blocking (fast and I/O-bound, perhaps something like fast disk access instead of network I/O)
* Blocking (slow and I/O-bound)
* Diabolical (slow and CPU-bound)

For the sake of simplicity in this example, let’s presume that the call to process()
is a fast, CPU-bound operation and therefore nonblocking.

was introduced in Python 3.7

Example 3-22. The nonblocking way.

``` python
from contextlib import asynccontextmanager

@asynccontextmanager #1
async def web_page(url): #2
    data = await download_webpage(url) #3
    yield data #4
    await update_stats(url) #5

async with web_page('google.com') as data: #6
    process(data)
```

1. The new `@asynccontextmanager` decorator is used in exactly the same way.

2. It does, however, require that the decorated generator function be declared with
async def.

3. As before, we fetch the data from the URL before making it available to the body
of the context manager. I have added the await keyword, which tells us that this
coroutine will allow the event loop to run other tasks while we wait for the net‐
work call to complete.

- Note that we cannot simply tack on the await keyword to anything. This change
presupposes that we were also able to modify the download_webpage() function
itself, and convert it into a coroutine that is compatible with the await keyword.
For the times when it is not possible to modify the function, a different approach
is needed; we’ll discuss that in the next example.

4. As before, the data is made available to the body of the context manager. I’m try‐
ing to keep the code simple, so I’ve omitted the usual try/finally handler that
you should normally write to deal with exceptions raised in the body of caller.

- Note that the presence of yield is what changes a function into a generator func‐
tion; the additional presence of the async def keywords in point 1 makes this an
asynchronous generator function. When called, it will return an asynchronous gen‐
erator. The inspect module has two functions that can test for these:
`isasyncgenfunction()` and `isasyncgen()`, respectively.

5. Here, assume that we’ve also converted the code inside the update_stats() func‐
tion to allow it to produce coroutines. We can then use the await keyword,
which allows a context switch to the event loop while we wait for the I/O-bound
work to complete.

6. Another change was required in the usage of the context manager itself: we
needed to use async with instead of a plain with.

Hopefully, this example shows that the new @asynccontextmanager is perfectly anal‐
ogous to the @contextmanager decorator.

In callouts 3 and 5, I said it was necessary to modify some functions to return corou‐
tines; these were download_webpage() and update_stats(). This is usually
not that easy to do, since async support needs to be added down at the socket level.
The focus of the preceding examples was simply to show off the new
@asynccontextmanager decorator, not to show how to convert blocking functions
into nonblocking ones. The more common situation is when you want to use a block‐
ing function in your program, but it’s not possible to modify the code in that
function.

This situation will usually happen with third-party libraries, and a great example is
the requests library, which uses blocking calls throughout[^8].
If you can’t change the
code being called, there is another way. This is a convenient place to show you how
an executor can be used to do exactly that, as illustrated in Example 3-23.

Example 3-23. The nonblocking-with-a-little-help-from-my-friends way

``` python
@asynccontextmanager
async def web_page(url): #1
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
       None, download_webpage, url) #2
    yield data
    
    await loop.run_in_executor(None, update_stats, url) #3
async with web_page('google.com') as data:
    process(data)
```

1. For this example, assume that we are unable to modify the code for our two
blocking calls, download_webpage() and update_stats(); i.e., we can’t alter
them to be coroutine functions. That’s bad, because the most grave sin of eventbased programming is breaking the rule that you must never, under any circum‐
stances, prevent the event loop from processing events.
To get around the problem, we will use an executor to run the blocking calls in a
separate thread. The executor is made available to us as an attribute of the event
loop itself.

2. We call the executor. The signature is AbstractEventLoop.run_in_execu
tor(executor, func, *args). If you want to use the default executor (which is a
ThreadPoolExecutor), you must pass None as the value for the executor
argument[^9].

3. As with the call to `download_webpage()`, we also run the other blocking call to
update_stats() in an executor. Note that you must use the await keyword in
front. If you forget, the execution of the asynchronous generator (i.e., your async
context manager) will not wait for the call to complete before proceeding.

It’s likely that async context managers are going to be heavily used in many asynciobased codebases, so it’s pretty important to have a good understanding of them. You
can read more about the new @asynccontextmanager decorator in the [Python 3.7
documentation](https://docs.python.org/3.7/library/contextlib.html#contextlib.asynccontextmanager).

### Async Iterators: async for

Next up is the async version of the for loop. It is easiest to understand how this works
if you first recognize that ordinary iteration—just like so many other language fea‐
tures—is implemented through the use of special methods, recognizable by the double
underscores in their names.
For reference, Example 3-24 shows how a standard (nonasync) iterator is defined
through the use of the __iter__() and __next__() methods.

Example 3-24. A traditional, nonasync iterator

``` python
>>> class A:
...     def __iter__(self): #1
...         self.x = 0 #2
...         return self #3
...     def __next__(self): #4
...         if self.x > 2:
...             raise StopIteration #5
...         else:
...             self.x += 1
...             return self.x #6
>>> for i in A():
...     print(i)
1
2
3
```

1. An iterator must implement the __iter__() special method.

2. Initialize some state to the “starting” state.

3. The __iter__() special method must return an iterable; i.e., an object that implements the __next__() special method. In this case, it’s the same instance, because A itself also implements the __next__() special method.

4. The __next__() method is defined. This will be called for every step in the iteration sequence until…

5. …StopIteration is raised.

6. The returned values for each iteration are generated.

Now you ask: what happens if you declare the `__next__()` special method as an async def coroutine function? That will allow it to await some kind of I/O-bound operation—and this is pretty much exactly how async for works, except for some small details around naming. The specification (in PEP 492) shows that to use async for on an async iterator, several things are required in the async iterator itself:

1. You must implement `def __aiter__()`. (Note: not with async def!)
2. `__aiter__()` must return an object that implements async `def __anext__()`.
3. `__anext__()` must return a value for each iteration and raise `StopAsync Iteration` when finished.

---

Let’s take a quick look at how that might work. Imagine that we have a bunch of keys in a [Redis](https://redis.io/) database, and we want to iterate over their data, but we fetch the data only on demand. An asynchronous iterator for that might look like Example 3-25.

Example 3-25. Async iterator for fetching data from Redis

```python
import asyncio
from aioredis import create_redis

async def main(): #1
    redis = await create_redis(('localhost', 6379)) #2
    keys = ['Americas', 'Africa', 'Europe', 'Asia'] #3

    async for value in OneAtATime(redis, keys): #4
        await do_something_with(value) #5

class OneAtATime: #6
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys
    def __aiter__(self): #7
        self.ikeys = iter(self.keys)
        return self
    async def __anext__(self): #8
        try:
            k = next(self.ikeys) #9
        except StopIteration: #10
            raise StopAsyncIteration
        value = await redis.get(k) #11
        return value

asyncio.run(main())
```

1. The main() function: we run it using asyncio.run() toward the bottom of the code sample.

2. We use the high-level interface in aioredis to get a connection.

3. Imagine that each of the values associated with these keys is quite large and stored in the Redis instance.

4. We’re using async for: the point is that iteration is able to suspend itself while waiting for the next datum to arrive.

5. For completeness, imagine that we also perform some I/O-bound activity on the fetched value—perhaps a simple data transformation—and then it gets sent on to another destination.

---

6. The initializer of this class is quite ordinary: we store the Redis connection instance and the list of keys to iterate over.

7. Just as in the previous code example with __iter__(), we use __aiter__() to set things up for iteration. We create a normal iterator over the keys, self.ikeys, and return self because OneAtATime also implements the __anext__() coroutine method.

8. Note that the __anext__() method is declared with async def, while the __aiter__() method is declared only with def.

9. For each key, we fetch the value from Redis: self.ikeys is a regular iterator over the keys, so we use next() to move over them.

10. When self.ikeys is exhausted, we handle the StopIteration and simply turn it into a StopAsyncIteration! This is how you signal stop from inside an async iterator.

11. Finally—the entire point of this example—we can get the data from Redis associated with this key. We can await the data, which means that other code can run on the event loop while we wait on network I/O.

Hopefully, this example is clear: async for provides the ability to retain the convenience of a simple for loop, even when iterating over data where the iteration itself is performing I/O. The benefit is that you can process enormous amounts of data with a single loop, because you have to deal with each chunk only in tiny batches.

### Simpler Code with Async Generators

Async generators are async def functions that have yield keywords inside them. Async generators result in simpler code.

However, the idea of them might be confusing if you have some experience with using generators as if they were coroutines, such as with the Twisted framework, or the Tornado framework, or even with yield from in Python 3.4’s asyncio. Therefore, before we continue, it will be best if you can convince yourself that

* Coroutines and generators are completely different concepts.
* Async generators behave much like ordinary generators.
* For iteration, you use async for for async generators, instead of the ordinary for used for ordinary generators.

---

The example used in the previous section to demonstrate an async iterator for inter‐
action with Redis turns out to be much simpler if we set it up as an async generator,
shown in Example 3-26.

Example 3-26. Easier with an async generator

``` python
import asyncio
from aioredis import create_redis

async def main(): #1
    redis = await create_redis(('localhost', 6379))
    keys = ['Americas', 'Africa', 'Europe', 'Asia']

    async for value in one_at_a_time(redis, keys): #2
        await do_something_with(value)

async def one_at_a_time(redis, keys): #3
    for k in keys: 
        value = await redis.get(k) #4
        yield value #5

asyncio.run(main())
```

1. The main() function is identical to the version in Example 3-25.
2. Well, almost identical: I changed the name from CamelCase to `snake_case`.
3. Our function is now declared with async def, making it a coroutine function, and
since this function also contains the yield keyword, we refer to it as an asynchro‐
nous generator function.
4. We don’t have to do the convoluted things necessary in the previous example
with self.ikeys: here, we just loop over the keys directly and obtain the value…
5. …and then yield it to the caller, just like a normal generator.

It might seem complex if this is new to you, but I urge you to play around with this
yourself on a few toy examples. It starts to feel natural pretty quickly. Async genera‐
tors are likely to become popular in asyncio-based codebases because they bring all
the same benefits as normal generators: making code shorter and simpler.

---

### Async Comprehensions

Now that we’ve seen how Python supports asynchronous iteration, the next natural
question to ask is whether it also works for list comprehensions—and the answer is
yes. This support was introduced in [PEP 530](https://peps.python.org/pep-0530/), and I recommend you take a look at the
PEP yourself; it is short and readable. Example 3-27 shows how typical async com‐
prehensions are laid out.

Example 3-27. Async list, dict, and set comprehensions

``` python
>>> import asyncio
>>>
>>> async def doubler(n):
...     for i in range(n):
...         yield i, i * 2 #1
...         await asyncio.sleep(0.1) #2
...
>>> async def main():
...     result = [x async for x in doubler(3)] #3
...     print(result)
...     result = {x: y async for x, y in doubler(3)} #4
...     print(result)
...     result = {x async for x in doubler(3)} #5
...     print(result)
...
>>> asyncio.run(main())
[(0, 0), (1, 2), (2, 4)]
{0: 0, 1: 2, 2: 4}
{(2, 4), (1, 2), (0, 0)}
```

1. doubler() is a very simple async generator: given an upper value, it’ll iterate over
a simple range, yielding a tuple of the value and its double.

2. Sleep a little, just to emphasize that this is really an async function.

3. An async list comprehension: note how async for is used instead of the usual
for. This difference is the same as that shown in the examples in “Async Iterators:
TODO: internal link
async for” on page 50.

4. An async dict comprehension; all the usual tricks work, such as unpacking the
tuple into x and y so that they can feed the dict comprehension syntax.

5. The async set comprehension works exactly as you would expect.

---

You can also use await inside comprehensions, as outlined in PEP 530. This shouldn’t
be a surprise; await coro is a normal expression and can be used in most places you
would expect.

It’s the async for that makes a comprehension an async comprehension, not the pres‐
ence of await. All that’s needed for await to be legal (inside a comprehension) is for it
to be used inside the body of a coroutine function—i.e., a function declared with
async def. Using await and async for inside the same list comprehension is really
combining two separate concepts, but we’ll do this anyway in Example 3-28 to make
sure you’re comfortable with async language syntax.

Example 3-28. Putting it all together

``` python
>>> import asyncio
>>>
>>> async def f(x): #1
...     await asyncio.sleep(0.1)
...     return x + 100
...
>>> async def factory(n): #2
...     for x in range(n):
...         await asyncio.sleep(0.1)
...         yield f, x #3
...
>>> async def main():
...     results = [await f(x) async for f, x in factory(3)] #4
...     print('results = ', results)
...
>>> asyncio.run(main())
results = [100, 101, 102]
```

1. A simple coroutine function: sleep for a bit; then return the parameter plus 100.

2. This is an async generator, which we will call inside an async list comprehension a
bit farther down, using async for to drive the iteration.

3. The async generator will yield a tuple of f and the iteration var x. The f return
value is a coroutine function, not yet a coroutine.

4. Finally, the async comprehension. This example has been contrived to demon‐
strate a comprehension that includes both async for and await. Let’s break
down what’s happening inside the comprehension. First, the factory(3) call
returns an async generator, which must be driven by iteration. Because it’s an
async generator, you can’t just use for; you must use async for.

---

The values produced by the async generator are a tuple of a coroutine function f
and an int. Calling the coroutine function f() produces a coroutine, which must
be evaluated with await.

Note that inside the comprehension, the use of await has nothing at all to do
with the use of async for: they are doing completely different things and acting
on different objects entirely.

### Starting Up and Shutting Down (Gracefully!)

Most async-based programs are going to be long-running, network-based applica‐
tions. This domain holds a surprising amount of complexity in dealing with how to
start up and shut down correctly.

Of the two, startup is simpler. The standard way of starting up an asyncio application
is to have a main() coroutine function and call it with asyncio.run(), as shown in
TODO: internal link
Example 3-2 at the beginning of this chapter.
Generally, startup will be fairly straightforward; for the server case described earlier,
you can read more about it [in the docs](https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams). We’ll also briefly look at a demonstration of
server startup in an upcoming code example.

Shutdown is much more intricate. For shutdown, I previously covered the dance that
happens inside asyncio.run(). When the async def main() function exits, the fol‐
lowing actions are taken:

1. Collect all the still-pending task objects (if any).
2. Cancel these tasks (this raises CancelledError inside each running coroutine,
which you may choose to handle in a try/except within the body of the corou‐
tine function).
3. Gather all these tasks into a group task.
4. Use run_until_complete() on the group task to wait for them to finish—i.e., let
the CancelledError exception be raised and dealt with.

asyncio.run() performs these actions for you, but in spite of this assistance, a rite of
passage in building your first few nontrivial asyncio apps is going to be trying to get
rid of error messages like “Task was destroyed but it is pending!” during shutdown.
This happens because your application was not expecting one or more of the preced‐
ing steps. Example 3-29 is an example of a script that raises this annoying error.

Example 3-29. Destroyer of pending tasks

``` python
# taskwarning.py
import asyncio
Starting Up and Shutting Down (Gracefully!) | 57
async def f(delay):
    await asyncio.sleep(delay)

loop = asyncio.get_event_loop()
t1 = loop.create_task(f(1))
t2 = loop.create_task(f(2))
loop.run_until_complete(t1)
loop.close()
```

1. Task 1 will run for 1 second.
2. Task 2 will run for 2 seconds.
3. Run only until task 1 is complete.

Running it produces the following output:

``` shell
$ python taskwarning.py
Task was destroyed but it is pending!
task: <Task pending coro=<f() done, defined at [...snip...]>
```

This error is telling you that some tasks had not yet been completed when the loop
was closed. We want to avoid this, and that is why the idiomatic shutdown procedure
is to collect all unfinished tasks, cancel them, and then let them all finish before clos‐
ing the loop. asyncio.run() does all of these steps for you, but it is important to
understand the process in detail so that you will be able to handle more complex
situations.

Let’s look at a more detailed code sample that illustrates all these phases.
Example 3-30 is a mini case study with a Telnet-based echo server.

Example 3-30. Asyncio application life cycle (based on the TCP echo server in the
Python documentation)

``` python
# telnetdemo.py
import asyncio
from asyncio import StreamReader, StreamWriter

async def echo(reader: StreamReader, writer: StreamWriter): #1
    print('New connection.')
    try:
        while data := await reader.readline(): #2
            writer.write(data.upper()) #3
            await writer.drain()
        print('Leaving Connection.')
    except asyncio.CancelledError: #4
        print('Connection dropped!')
async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port) #5
    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')
```

1. This echo() coroutine function will be used (by the server) to create a coroutine
for each connection made. The function is using the streams API for networking
with asyncio.
2. To keep the connection alive, we’ll have an infinite loop to wait for messages.
3. Return the data back to the sender, but in ALL CAPS.
4. If this task is cancelled, we’ll print a message.
5. This code for starting a TCP server is taken directly from the Python 3.8
documentation.

After starting the echo server, you can telnet to and interact with it:

``` shell
$ telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
hi!
HI!
stop shouting
STOP SHOUTING
^]
telnet> q/
Connection closed.
```

The server output for that session looks like this (the server keeps running until we
hit Ctrl-C):

``` python
$ python telnetdemo.py
New connection.
Leaving Connection.
^CBye!
```

In the Telnet session just shown, the client (i.e., Telnet) closed the connection before
the server was stopped, but let’s see what happens if we shut down our server while a
connection is active. We’ll see the following output from the server process:

``` shell
$ python telnetdemo.py
New connection.
^CConnection dropped!
Bye!
```

---

Here you can see that the exception handler for CancelledError was triggered. Now
let’s imagine that this is a real-world production application, and we want to send all
events about dropped connections to a monitoring service. The code sample might be
modified to look like Example 3-31.

Example 3-31. Creating a task inside a cancellation handler

``` python
# telnetdemo.py
import asyncio
from asyncio import StreamReader, StreamWriter

async def send_event(msg: str): #1
    await asyncio.sleep(1)

async def echo(reader: StreamReader, writer: StreamWriter):
     print('New connection.')
    try:
        while (data := await reader.readline()):
            writer.write(data.upper())
            await writer.drain()
        print('Leaving Connection.')
    except asyncio.CancelledError:
        msg = 'Connection dropped!'
        print(msg)
        asyncio.create_task(send_event(msg)) #2

async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')
```

1. Pretend that this coroutine actually contacts an external server to submit event
notifications.

2. Because the event notifier involves network access, it is common for such calls to
be made in a separate async task; that’s why we’re using the create_task() func‐
tion here.

This code has a bug, however. It becomes obvious if we rerun the example, and make
sure to stop the server (with Ctrl-C) while a connection is active:

``` shell
$ python telnetdemo.py
New connection.
^CConnection dropped!
Bye!
Task was destroyed but it is pending!
task: <Task pending name='Task-6' coro=<send_event() done, ...>
```

To understand why this is happening, we must go back to the sequence of cleanup
events that asyncio.run() does during the shutdown phase; in particular, the impor‐
tant part is that when we press Ctrl-C, all the currently active tasks are collected and
cancelled. At this point, only those tasks are then awaited, and asyncio.run() returns
immediately after that. The bug in our modified code is that we created a new task
inside the cancellation handler of our existing “echo” task. This new task was created
only after asyncio.run() had collected and cancelled all the tasks in the process.

This is why it is important to be aware of how asyncio.run() works.

<img style="float: left;width:120px;height:120px" src="./images/2.png">
As a general rule of thumb, try to avoid creating new tasks inside
CancelledError exception handlers. If you must, be sure to also
await the new task or future inside the scope of the same function.

And finally: if you’re using a library or framework, make sure to follow its documen‐
tation on how you should perform startup and shutdown. Third-party frameworks
usually provide their own functions for startup and shutdown, and they’ll provide
event hooks for customization. You can see an example of these hooks with the Sanic
framework in “Case Study: Cache Invalidation” on page 115.

TODO:  internal link

### What Is the return_exceptions=True for in gather()?

You may have noticed the keyword argument return_exceptions=True in the call to
gather() in Examples 3-3 and 3-1 during the shutdown sequence, but I very sneakily
said nothing about it at the time. asyncio.run() also uses gather() and
return_exceptions=True internally, and the time has come for further discussion.

Unfortunately, the default is gather(..., return_exceptions=False). This default
is problematic for most situations, including the shutdown process, and this is why
asyncio.run() sets the parameter to True. It’s a little complicated to explain directly;
instead, let’s step through a sequence of observations that’ll make it much easier to
understand:

1. run_until_complete() operates on a future; during shutdown, it’s the future
returned by gather().
2. If that future raises an exception, the exception will also be raised out of
run_until_complete(), which means that the loop will stop.
3. If run_until_complete() is being used on a group future, any exception raised
inside any of the subtasks will also be raised in the “group” future if it isn’t handled
in the subtask. Note this includes CancelledError.
4. If only some tasks handle CancelledError and others don’t, the ones that don’t
will cause the loop to stop. This means that the loop will be stopped before all the
tasks are done.
5. For shutdown, we really don’t want this behavior. We want
run_until_complete() to finish only when all the tasks in the group have fin‐
ished, regardless of whether some of the tasks raise exceptions.
6. Hence we have gather(*, return_exceptions=True): that setting makes the
“group” future treat exceptions from the subtasks as returned values, so that they
don’t bubble out and interfere with run_until_complete().

And there you have it: the relationship between return_exceptions=True and
run_until_complete(). An undesirable consequence of capturing exceptions in this
way is that some errors may escape your attention because they’re now (effectively)
being handled inside the group task. If this is a concern, you can obtain the output
list from run_until_complete() and scan it for any subclasses of Exception, and
then write log messages appropriate for your situation. Example 3-32 demonstrates
this approach.

Example 3-32. All the tasks will complete

``` python
# alltaskscomplete.py
import asyncio

async def f(delay):
    await asyncio.sleep(1 / delay) #1
    return delay

loop = asyncio.get_event_loop()
for i in range(10):
    loop.create_task(f(i))
pending = asyncio.all_tasks()
group = asyncio.gather(*pending, return_exceptions=True)
results = loop.run_until_complete(group)
print(f'Results: {results}')
loop.close()
```

1. It would be awful if someone were to pass in a zero…

Here’s the output:

``` shell
$ python alltaskscomplete.py
Results: [6, 9, 3, 7, ...
 ZeroDivisionError('division by zero',), 4, ...
 8, 1, 5, 2]
```

Without return_exceptions=True, the ZeroDivisionError would be raised from
run_until_complete(), stopping the loop and thus preventing the other tasks from
finishing.

In the next section, we look at handling signals (beyond KeyboardInterrupt), but
before we get there, it’s worth keeping in mind that graceful shutdown is one of the
more difficult aspects of network programming, and this remains true for asyncio.
The information in this section is merely a start. I encourage you to have specific tests
for clean shutdown in your own automated test suites. Different applications often
require different strategies.

<img style="float: left;width:120px;height:120px" src="./images/2.png">

I’ve published a tiny package on the Python package index (PyPI)
called [aiorun](https://pypi.org/project/aiorun/), primarily for my own experiments and education in
dealing with asyncio shutdown, that incorporates many ideas from
this section. It may also be useful for you to tinker with the code
and experiment with your own ideas around asyncio shutdown
scenarios.

### Signals

Previous examples showed how the event loop is stopped with a KeyboardInterrupt;
i.e., pressing Ctrl-C. Internally within asyncio.run(), the raised KeyboardInterrupt
effectively unblocks a loop.run_until_complete() call and allows the subsequent
shutdown sequence to happen.

KeyboardInterrupt corresponds to the SIGINT signal. In network services, the more
common signal for process termination is actually SIGTERM, and this is also the
default signal when you use the kill command in a Unix shell.

<img style="float: left;width:120px;height:120px" src="./images/1.png">

The kill command on Unix systems is deceptively named: all it
does it send signals to a process. Without arguments, kill <PID>
will send a TERM signal: your process can receive the signal and do a
graceful shutdown, or simply ignore it! That’s a bad idea, though,
because if your process doesn’t stop eventually, the next thing the
would-be killer usually does is kill -s KILL <PID>, which sends
the KILL signal. This will shut you down, and there’s nothing your
program can do about it. Receiving the TERM (or INT) signal is your
opportunity to shut down in a controlled way.

---

asyncio has built-in support for handling process signals, but there’s a surprising
degree of complexity around signal handling in general (not specific to asyncio). We
cannot cover everything here, but we can have a look at some of the more basic con‐
siderations that need to be made. Example 3-33 will produce the following output:

``` shell
$ python shell_signal01.py
<Your app is running>
<Your app is running>
<Your app is running>
<Your app is running>
^CGot signal: SIGINT, shutting down.
```

I pressed Ctrl-C to stop the program, as shown on the last line. Example 3-33 inten‐
tionally avoids using the convenient asyncio.run() function because I want to warn
you about specific traps in handling the two most common signals, SIGTERM and
SIGINT, during your shutdown sequence. After we discuss these, I will show a final
example of signal handling using the more convenient asyncio.run() function.

Example 3-33. Refresher for using KeyboardInterrupt as a SIGINT handler

``` python
# shell_signal01.py
import asyncio

async def main(): #1
    while True:
        print('<Your app is running>')
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(main()) #2
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt: #3
        print('Got signal: SIGINT, shutting down.')
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
```

1. This is the main part of our application. To keep things simple, we’re just going to
sleep in an infinite loop.
2. This startup and shutdown sequence will be familiar to you from the previous
section. We schedule main(), call run_forever(), and wait for something to stop
the loop.
3. In this case, only Ctrl-C will stop the loop. Then we handle KeyboardInterrupt
and do all the necessary cleanup bits, as covered in the previous sections.

So far, that’s pretty straightforward. Now I’m going to complicate things. Suppose
that:

* One of your colleagues asks that you please handle SIGTERM in addition to SIGINT
as a shutdown signal.
* In your real application, you need to do cleanup inside your main() coroutine;
you will need to handle CancelledError, and the cleanup code inside the excep‐
tion handler will take several seconds to finish (imagine that you have to commu‐
nicate with network peers and close a bunch of socket connections).
* Your app must not do weird things if you’re sent signals multiple times (such as
rerunning any shutdown steps); after you receive the first shutdown signal, you
want to simply ignore any new signals until exit.

asyncio provides enough granularity in the API to handle all these situations.
Example 3-34 modifies the previous simple code example to include these new
features.

Example 3-34. Handle both SIGINT and SIGTERM, but stop the loop only once

``` python
# shell_signal02.py
import asyncio
from signal import SIGINT, SIGTERM #1

async def main():
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError: #2
        for i in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)

def handler(sig): #3
    loop.stop() #4
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM) #5
    loop.add_signal_handler(SIGINT, lambda: None) #6

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for sig in (SIGTERM, SIGINT): #7
        loop.add_signal_handler(sig, handler, sig)
        loop.create_task(main())
        loop.run_forever() #8
        tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
 group = asyncio.gather(*tasks, return_exceptions=True)
 loop.run_until_complete(group)
 loop.close()
```

1. Import the signal values from the standard library signal module.

2. This time, our main() coroutine is going to do some cleanup internally. When
the cancellation signal is received (initiated by cancelling each of the tasks), there
will be a period of 3 seconds where main() will continue running during the
run_until_complete() phase of the shutdown process. It’ll print, “Your app is
shutting down…”.

3. This is a callback handler for when we receive a signal. It is configured on the
loop via the call to add_signal_handler() a bit farther down.

4. The primary purpose of the handler is to stop the loop: this will unblock the
loop.run_forever() call and allow pending task collection and cancellation, and
the run_complete() for shutdown.

5. Since we are now in shutdown mode, we don’t want another SIGINT or SIGTERM
to trigger this handler again: that would call loop.stop() during the
run_until_complete() phase, which would interfere with our shutdown pro‐
cess. Therefore, we remove the signal handler for SIGTERM from the loop.

6. This is a “gotcha”: we can’t simply remove the handler for SIGINT, because if we
did that, KeyboardInterrupt would again become the handler for SIGINT, the
same as it was before we added our own handlers. Instead, we set an empty
lambda function as the handler. This means that KeyboardInterrupt stays away,
and SIGINT (and Ctrl-C) has no effect[^10].

7. Here the signal handlers are attached to the loop. Note that, as discussed previ‐
ously, setting a handler on SIGINT means a KeyboardInterrupt will no longer be
raised on SIGINT. The raising of a KeyboardInterrupt is the “default” handler for SIGINT and is preconfigured in Python until you do something to change the
handler, as we’re doing here.

8. As usual, execution blocks on run_forever() until something stops the loop. In
this case, the loop will be stopped inside handler() if either SIGINT or SIGTERM is
sent to our process. The remainder of the code is the same as before.

Here’s the output:

``` python
$ python shell_signal02.py
<Your app is running>
<Your app is running>
<Your app is running>
<Your app is running>
<Your app is running>
^CGot signal: Signals.SIGINT, shutting down.
<Your app is shutting down...>
^C<Your app is shutting down...> #1
^C<Your app is shutting down...>
```

1. I hit Ctrl-C a bunch of times during the shutdown phase, but as expected, noth‐
ing happened until the main() coroutine eventually completed.

In these examples, I’ve controlled the life cycle of the event loop the hard way, but this
was necessary to explain the components of the shutdown procedure. In practice, we
would much prefer to use the more convenient asyncio.run() function.
Example 3-35 retains the features of the preceding signal-handling design, but also
takes advantage of the convenience of asyncio.run().

Example 3-35. Signal handling when using asyncio.run()

``` python
# shell_signal02b.py
import asyncio
from signal import SIGINT, SIGTERM

async def main():
    loop = asyncio.get_running_loop()
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig) #1
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)

def handler(sig):
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop=loop): #2
        task.cancel()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)

if __name__ == '__main__':
 asyncio.run(main())
```

1. Because asyncio.run() takes control of the event loop startup, our first opportu‐
nity to change signal handling behavior will be in the main() function.

2. Inside the signal handler, we can’t stop the loop as in previous examples, because
we’ll get warnings about how the loop was stopped before the task created for
main() was completed. Instead, we can initiate task cancellation here, which will
ultimately result in the main() task exiting; when that happens, the cleanup han‐
dling inside asyncio.run() will take over.

### Waiting for the Executor During Shutdown
TODO: internal 
“Quickstart” on page 22 introduced the basic executor interface with Example 3-3,
where I pointed out that the blocking time.sleep() call was conveniently shorter
than the asyncio.sleep() call—luckily for us, because it means the executor task
completes sooner than the main() coroutine, and as a result the program shuts down
correctly.

This section examines what happens during shutdown when executor jobs take
longer to finish than all the pending Task instances. The short answer is: without
intervention, you’re going to get errors like those produced by the code in

Example 3-36.

Example 3-36. The executor takes too long to finish

``` python
# quickstart.py
import time
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, blocking)
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')

def blocking():
    time.sleep(1.5) #1
    print(f"{time.ctime()} Hello from a thread!")
 
asyncio.run(main())
```

1. This code sample is exactly the same as the one in Example 3-3, except that the
sleep time in the blocking function is now longer than in the async one.
Running this code produces the following output:

``` shell
$ python quickstart.py
Fri Jan 24 16:25:08 2020 Hello!
Fri Jan 24 16:25:09 2020 Goodbye!
exception calling callback for <Future at [...snip...]>
Traceback (most recent call last):

<big nasty traceback>

RuntimeError: Event loop is closed
Fri Jan 24 16:25:09 2020 Hello from a thread!
```

What’s happening here is that behind the scenes, run_in_executor() does not create
a Task instance: it returns a Future. That means it isn’t included in the set of “active
tasks” that get cancelled inside asyncio.run(), and therefore run_until_complete()
(called inside asyncio.run()) does not wait for the executor task to finish. The
RuntimeError is being raised from the internal loop.close() call made inside asyn
cio.run().

At the time of writing, loop.close() in Python 3.8 does not wait for all executor jobs
to finish, and this is why the Future returned from run_in_executor() complains:
by the time it resolves, the loop has already been closed. There are discussions about
how to improve this in the core Python dev team, but until a solution has been settled
on, you’re going to need a strategy for handling these errors.

<img style="float: left;width:120px;height:120px" src="./images/2.png">

In Python 3.9, the asyncio.run() function [has been improved](https://bugs.python.org/issue34037) to
correctly wait for executor shutdown, but at the time of writing,
this has not yet been backported to Python 3.8.

Several ideas for fixing this spring to mind, all with different trade-offs, and we’re
going to look at a few of them. My real goal for this exercise is to help you think about
the event loop life cycle from different points of view, considering the lifetime man‐
agement of all the coroutines, threads, and subprocesses that might be interoperating
in a nontrivial program.

The first idea—and the easiest to implement, as shown in Example 3-37— is to always
await an executor task from inside a coroutine.

Example 3-37. Option A: wrap the executor call inside a coroutine

``` python
# quickstart.py
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor

async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking) #1
    try:
        print(f'{time.ctime()} Hello!')
        await asyncio.sleep(1.0)
        print(f'{time.ctime()} Goodbye!')
    finally:
        await future #2

def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')
```

1. The idea aims at fixing the shortcoming that run_in_executor() returns only a
Future instance and not a task. We can’t capture the job in all_tasks() (used
within asyncio.run()), but we can use await on the future. The first part of the
plan is to create a future inside the main() function.

2. We can use the try/finally structure to ensure that we wait for the future to be
finished before the main() function returns.

The code works, but it places a heavy limitation on lifetime management of the exec‐
utor function: it implies that you must use a try/finally within every single scope
where an executor job is created. We would prefer to spawn executor jobs in the same
way that we create async tasks, and still have the shutdown handling inside asyn
cio.run() perform a graceful exit.

The next idea, shown in Example 3-38, is a little more cunning. Since our problem is
that an executor creates a future instead of a task, and the shutdown handling inside
asyncio.run() deals with tasks, our next plan is to wrap the future (produced by the
executor) inside a new task object.

Example 3-38. Option B: add the executor future to the gathered tasks

``` python
# quickstart.py
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor

async def make_coro(future): #2
    try:
        return await future
    except asyncio.CancelledError:
        return await future
async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    asyncio.create_task(make_coro(future)) #1
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    
def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')
```

1. We take the future returned from the run_in_executor() call and pass it into a
new utility function, make_coro(). The important point here is that we’re using
create_task(), which means that this task will appear in the list of all_tasks()
within the shutdown handling of asyncio.run(), and will receive a cancellation
during the shutdown process.

2. This utility function make_coro() simply waits for the future to complete—but
crucially, it continues to wait for the future even inside the exception handler for
CancelledError.

This solution is better behaved during shutdown, and I encourage you to run the
example and hit Ctrl-C immediately after “Hello!” is printed. The shutdown process
will still wait for make_coro() to exit, which means that it also waits for our executor
job to exit. However, this code is very clumsy because you have to wrap every execu‐
tor Future instance inside a make_coro() call. 

If we’re willing to give up the convenience of the asyncio.run() function (until
Python 3.9 is available), we can do better with custom loop handling, shown in
Example 3-39.

Example 3-39. Option C: just like camping, bring your own loop and your own executor

``` python
# quickstart.py
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    loop.stop()

def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.get_event_loop()
executor = Executor() #1
loop.set_default_executor(executor) #2
loop.create_task(main())
future = loop.run_in_executor(None, blocking) #3

try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Cancelled')

tasks = asyncio.all_tasks(loop=loop)
for t in tasks:
    t.cancel()
group = asyncio.gather(*tasks, return_exceptions=True)
loop.run_until_complete(group)
executor.shutdown(wait=True) #4
loop.close()
```

1. This time, we create our own executor instance.
2. We have to set our custom executor as the default one for the loop. This means
that anywhere the code calls run_in_executor(), it’ll be using our custom
instance.
3. As before, we run the blocking function.
4. Finally, we can explicitly wait for all the executor jobs to finish before closing the
loop. This will avoid the “Event loop is closed” messages that we saw before. We
can do this because we have access to the executor object; the default executor is not exposed in the asyncio API, which is why we cannot call shutdown() on it
and were forced to create our own executor instance.

Finally, we have a strategy with general applicability: you can call run_in_executor()
anywhere, and your program will still shut down cleanly, even if executor jobs are still
running after all the async tasks have completed.

I strongly urge you to experiment with the code examples shown here and try differ‐
ent strategies to create tasks and executor jobs, staggering them in time and trying to
shut down cleanly. I expect that a future version of Python will allow the
asyncio.run() function to wait (internally) for executor jobs to finish, but I hope
that the discussion in this section is still useful for you to develop your thinking
around clean shutdown handling.
