# Introducing Asyncio

> My story is a lot like yours, only more interesting ’cause it involves robots.

> Bender, Futurama episode “30% Iron Chef ”

The most common question I receive about Asyncio in Python 3 is this: “What is it, and what do I do with it?” The answer you’ll hear most frequently is likely something about being able to execute multiple concurrent HTTP requests in a single program. But there is more to it than that—much more. Asyncio requires changing how you think about structuring programs.

The following story provides a backdrop for gaining this understanding. The central focus of Asyncio is on how best to best perform multiple tasks at the same time—and not just any tasks, but specifically tasks that involve waiting periods. The key insight required with this style of programming is that while you wait for this task to com‐plete, work on other tasks can be performed.

### The Restaurant of ThreadBots

The year is 2051, and you find yourself in the restaurant business. Automation, largely by robot workers, powers most of the economy, but it turns out that humans still enjoy going out to eat once in a while. In your restaurant, all the employees are robots—humanoid, of course, but unmistakably robots. The most successful manu‐facturer of robots is Threading Inc., and robot workers from this company have come to be called “ThreadBots.”

Except for this small robotic detail, your restaurant looks and operates like one of those old-time establishments from, say, 2020. Your guests will be looking for that vintage experience. They want fresh food prepared from scratch. They want to sit at tables. They want to wait for their meals—but only a little. They want to pay at the end, and they sometimes even want to leave a tip, for old times’ sake.

Being new to the robotic restaurant business, you do what every other restaurateur does and hire a small fleet of robots: one to greet diners at the front desk (GreetBot), one to wait tables and take orders (WaitBot), one to do the cooking (ChefBot), and one to manage the bar (WineBot).

Hungry diners arrive at the front desk and are welcomed by GreetBot, your front-of-house ThreadBot. They are then directed to a table, and once they are seated, WaitBot takes their order. Then WaitBot brings that order to the kitchen on a slip of paper (because you want to preserve that old-time experience, remember?). ChefBot looks at the order on the slip and begins preparing the food. WaitBot will periodically check whether the food is ready, and when it is, will immediately take the dishes to the cus‐ tomers’ table. When the guests are ready to leave, they return to GreetBot, who calcu‐lates the bill, takes their payment, and graciously wishes them a pleasant evening.

Your restaurant is a hit, and you soon grow to have a large customer base. Your robot employees do exactly what they’re told, and they are perfectly good at the tasks you assign them. Everything is going really well, and you couldn’t be happier.

Over time, however, you do begin to notice some problems. Oh, it’s nothing truly serious; just a few things that seem to go wrong. Every other robotic restaurant owner seems to have similar niggling glitches. It is a little worrying that these problems seem to get worse the more successful you become.

Though rare, there are the occasional collisions that are very unsettling: sometimes, when a plate of food is ready in the kitchen, WaitBot will grab it before ChefBot has even let go of the plate. This usually ends up with the plate shattering and leaves a big mess. ChefBot cleans it up, of course, but still, you’d think that these top-notch robots would know how to be a bit more synchronized with each other. This happens at the bar too: sometimes WineBot will place a drink order on the bar, and WaitBot will grab it before WineBot has let go, resulting in broken glass and spilled Nederburg Cabernet Sauvignon.

Also, sometimes GreetBot will seat new diners at exactly the same moment that Wait‐Bot has decided to clean what it thought was an empty table. It’s pretty awkward for the diners. You’ve tried adding delay logic to WaitBot’s cleaning function, or delays to GreetBot’s seating function, but these don’t really help, and the collisions still occur. But at least these events are rare.

Well, they used to be. Your restaurant has become so popular that you’ve had to hire a few more ThreadBots. For very busy Friday and Saturday evenings, you’ve had to add a second GreetBot and two extra WaitBots.Unfortunately, the hiring contracts for ThreadBots mean that you have to hire them for the whole week, so this effectively means that for most of the quiet part of the week, you’re carrying three extra Thread‐Bots that you don’t really need.

The other resource problem, in addition to the extra cost, is that it’s more work for you to deal with these extra ThreadBots. It was fine to keep tabs on just four bots, but now you’re up to seven. Keeping track of seven ThreadBots is a lot more work, and because your restaurant keeps getting more and more famous, you become worried about taking on even more ThreadBots. It’s going to become a full-time job just to keep track of what each ThreadBot is doing. And another thing: these extra Thread‐Bots are using up a lot more space inside your restaurant. It’s becoming a tight squeeze for your customers, what with all these robots zipping around. You’re wor‐ried that if you need to add even more bots, this space problem is going to get even worse. You want to use the space in your restaurant for customers, not ThreadBots.

The collisions have also become worse since you added more ThreadBots. Now,
sometimes two WaitBots take the exact same order from the same table at the same time. It’s as if they both noticed that the table was ready to order and moved in to take it, without noticing that the other WaitBot was doing the exact same thing. As you can imagine, this results in duplicated food orders, which causes extra load on the kitchen and increases the chance of collisions when picking up the ready plates. You’re concerned that if you add more WaitBots, this problem might get worse.

Time passes.

Then, during one very, very busy Friday night service, you have a singular moment of clarity: time slows, lucidity overwhelms you, and you see a snapshot of your restau‐rant frozen in time. My ThreadBots are doing nothing! Not really nothing, to be fair, but they’re just…waiting.

Each of your three WaitBots at different tables is waiting for one of the diners at their table to give their order. The WineBot has already prepared 17 drinks, which are now waiting to be collected (it took only a few seconds), and is waiting for a new drink order. One of the GreetBots has greeted a new party of guests and told them they need to wait a minute to be seated, and is waiting for the guests to respond. The other GreetBot, now processing a credit card payment for another guest that is leaving, is
waiting for confirmation on the payment gateway device. Even the ChefBot, who is currently cooking 35 meals, is not actually doing anything at this moment, but is sim‐ply waiting for one of the meals to complete cooking so that it can be plated up and handed over to a WaitBot.

You realize that even though your restaurant is now full of ThreadBots, and you’re even considering getting more (with all the problems that entails), the ones that you currently have are not being fully utilized.

The moment passes, but not the realization. On Sunday, you add a data collection module to your ThreadBots. For each ThreadBot, you’re measuring how much time is spent waiting and how much is spent actively doing work. Over the course of the following week, the data is collected. Then on Sunday evening, you analyze the results. It turns out that even when your restaurant is at full capacity, the most hard‐working ThreadBot is idle about 98% of the time. The ThreadBots are so enormously efficient that they can perform any task in fractions of a second.

As an entrepreneur, this inefficiency really bugs you. You know that every other robotic restaurant owner is running their business the same as you, with many of the same problems. But, you think, slamming your fist on your desk, “There must be a better way!”

So the very next day, which is a quiet Monday, you try something bold: you program a single ThreadBot to do all the tasks. Every time it begins to wait, even for a second, the ThreadBot switches to the next task to be done in the restaurant, whatever it may be, instead of waiting. It sounds incredible-only one ThreadBot doing the work of all the others-but you’re confident that your calculations are correct. And besides, Monday is a quiet day; even if something goes wrong, the impact will be small. For this new project, you call the bot “LoopBot” because it will loop over all the jobs in the restaurant.

The programming was more difficult than usual. It isn’t just that you had to program one ThreadBot with all the different tasks; you also had to program some of the logic of when to switch between tasks. But by this stage, you’ve had a lot of experience with programming these ThreadBots, so you manage to get it done.

You watch your LoopBot like a hawk. It moves between stations in fractions of a second, checking whether there is work to be done. Not long after opening, the first guest arrives at the front desk. The LoopBot shows up almost immediately, and asks whether the guest would like a table near the window or near the bar. But then, as the LoopBot begins to wait, its programming tells it to switch to the next task, and it whizzes off. This seems like a dreadful error, but then you see that as the guest begins to say “Window please,” the LoopBot is back. It receives the answer and directs the guest to table 42. And off it goes again, checking for drink orders, food orders, table cleanup, and arriving guests, over and over again.

Late Monday evening, you congratulate yourself on a remarkable success. You check the data collection module on the LoopBot, and it confirms that even with a single ThreadBot doing the work of seven, the idle time was still around 97%. This result gives you the confidence to continue the experiment all through the rest of the week.

As the busy Friday service approaches, you reflect on the great success of your experiment. For service during a normal working week, you can easily manage the workload with a single LoopBot. And you’ve noticed another thing: you don’t see any more collisions. This makes sense; since there is only one LoopBot, it cannot get confused with itself. No more duplicate orders going to the kitchen, and no more confusion about when to grab a plate or drink.

Friday evening service begins, and as you had hoped, the single ThreadBot keeps up with all the customers and tasks, and service is proceeding even better than before.You imagine that you can take on even more customers now, and you don’t have to worry about having to bring on more ThreadBots. You think of all the money you’re going to save.

Then, unfortunately, something goes wrong: one of the meals, an intricate soufflé, has flopped. This has never happened before in your restaurant. You begin to study the LoopBot more closely. It turns out that at one of your tables, there is a very chatty guest. This guest has come to your restaurant alone and keeps trying to make conversation with the LoopBot, even sometimes holding your LoopBot by the hand. When this happens, your LoopBot is unable to dash off and attend to the ever-growing list of tasks elsewhere in your restaurant. This is why the kitchen produced its first flopped soufflé: your LoopBot was unable to make it back to the kitchen to remove the dish from the oven because it was held up by a guest.

Friday service finishes, and you head home to reflect on what you have learned. It’s true that the LoopBot was able to do all the work that was required in the busy Friday service; but on the other hand, your kitchen produced its very first spoiled meal, something that has never happened before. Chatty guests used to keep WaitBots busy all the time, but that never affected the kitchen service at all.

All things considered, you decide it is still better to continue using a single LoopBot. Those worrying collisions no longer occur, and there is much more space in your restaurant—space that you can use for more customers. But you realize something profound about the LoopBot: it can be effective only if every task is short, or at least can be performed in a short period of time. If any activity keeps the LoopBot busy for too long, other tasks will begin to suffer neglect.

It is difficult to know in advance which tasks may take too much time. What if a guest orders a cocktail that requires intricate preparation, taking much more time than usual? What if a guest wants to complain about a meal at the front desk, refuses to pay, and grabs the LoopBot by the arm, preventing it from task switching? You decide that instead of figuring out all of these issues up front, it is better to continue with the LoopBot, record as much information as possible, and deal with any problems later as
they arise.

More time passes.

Gradually, other restaurant owners notice your operation, and eventually they figure out that they too can get by, and even thrive, with only a single ThreadBot. Word spreads. Soon every single restaurant operates in this way, and it becomes difficult to remember that robotic restaurants ever operated with multiple ThreadBots at all.

### Epilogue

In our story, each robot worker in the restaurant is a single thread. The key observation in the story is that the nature of the work in the restaurant involves a great deal of waiting, just as ```requests.get()``` is waiting for a response from a server.

In a restaurant, the worker time spent waiting isn’t huge when slow humans are doing manual work, but when super-efficient and quick robots are doing the work, nearly all their time is spent waiting. In computer programming, the same is true when network programming is involved. CPUs do work and wait on network I/O. CPUs in modern computers are extremely fast—hundreds of thousands of times faster than network traffic. Thus, CPUs running networking programs spend a great deal of time waiting.

The insight in the story is that programs can be written to explicitly direct the CPU to move between work tasks as necessary. Although there is an improvement in economy (using fewer CPUs for the same work), the real advantage, compared to a threading (multi-CPU) approach, is the elimination of race conditions.

It’s not all roses, however: as we found in the story, there are benefits and drawbacks to most technology solutions. The introduction of the LoopBot solved a certain class of problems but also introduced new problems—not the least of which is that the restaurant owner had to learn a slightly different way of programming.

### What Problem Is Asyncio Trying to Solve?

For I/O-bound workloads, there are exactly (only!) two reasons to use async-based concurrency over thread-based concurrency:

- Asyncio offers a safer alternative to preemptive multitasking (i.e., using threads), thereby avoiding the bugs, race conditions, and other nondeterministic dangers that frequently occur in nontrivial threaded applications.

- Asyncio offers a simple way to support many thousands of simultaneous socket
connections, including being able to handle many long-lived connections for
newer technologies like WebSockets, or MQTT for Internet of Things (IoT)
applications.

That’s it.

Threading—as a programming model—is best suited to certain kinds of computational tasks that are best executed with multiple CPUs and shared memory for efficient communication between the threads. In such tasks, the use of multicoreprocessing with shared memory is a necessary evil because the problem domain requires it.

Network programming is not one of those domains. The key insight is that network programming involves a great deal of “waiting for things to happen,” and because of this, we don’t need the operating system to efficiently distribute our tasks over multiple CPUs. Furthermore, we don’t need the risks that preemptive multitasking brings,such as race conditions when working with shared memory.

However, there is a great deal of misinformation about other supposed benefits of event-based programming models. Here are a few of the things that just ain’t so:

##### Asyncio will make my code blazing fast

- Unfortunately, no. In fact, most benchmarks seem to show that threading solutions are slightly faster than their comparable Asyncio solutions. If the extent of concurrency itself is considered a performance metric, Asyncio does make it a bit easier to create very large numbers of concurrent socket connections, though. Operating systems often have limits on how many threads can be created, and this number is significantly lower than the number of socket connections that can be made. The OS limits can be changed, but it is certainly easier to do with Asyncio. And while we expect that having many thousands of threads should incur extra context-switching costs that coroutines avoid, it turns out to be difficult to benchmark this in practice.1 No, speed is not the benefit of Asyncio in Python; if that’s what you’re after, try Cython instead!

##### Asyncio makes threading redundant

- Definitely not! The true value of threading lies in being able to write multi-CPU programs, in which different computational tasks can share memory. The numerical library numpy, for instance, already makes use of this by speeding up certain matrix calculations through the use of multiple CPUs, even though all the memory is shared. For sheer performance, there is no competitor to this programming model for CPU-bound computation.

#### Asyncio removes the problems with the GIL

- Again, no. It is true that Asyncio is not aected by the GIL,2 but this is only because the GIL affects multithreaded programs. The “problems” with the GIL that people refer to occur because it prevents true multicore parallelism when using threads. Since Asyncio is single-threaded (almost by definition), it is unaffected by the GIL, but it cannot benefit from multiple CPU cores either.3It is also worth pointing out that in multithreaded code, the Python GIL can cause additional performance problems beyond what has already been mentioned in other points: Dave Beazley presented a talk on this called <p style="color:red">“Understanding the Python GIL”<p> at PyCon 2010, and much of what is discussed in that talk remains true today.

#### Asyncio prevents all race conditions

- False. The possibility of race conditions is always present with any concurrent programming, regardless of whether threading or event-based programming is used. It is true that Asyncio can virtually eliminate a certain class of race conditions common in multithreaded programs, such as intra-process shared memory access. However, it doesn’t eliminate the possibility of other kinds of race conditions, such as the interprocess races with shared resources common in distributed microservices architectures. You must still pay attention to how shared resources are being used. The main advantage of Asyncio over threaded code is that the points at which control of execution is transferred between coroutines are visible (because of the presence of await keywords), and thus it is much easier to reason about how shared resources are being accessed.

#### Asyncio makes concurrent programming easy

Ahem, where do I even begin?

The last myth is the most dangerous one. Dealing with concurrency is always complex, regardless of whether you’re using threading or Asyncio. When experts say “Asyncio makes concurrency easier,” what they really mean is that Asyncio makes it a little easier to avoid certain kinds of truly nightmarish race condition bugs—the kind that keep you up at night and that you tell other programmers about in hushed tones over campfires, wolves howling in the distance.

Even with Asyncio, there is still a great deal of complexity to deal with. How will your application support health checks? How will you communicate with a database that may allow only a few connections—much fewer than your five thousand socket connections to clients? How will your program terminate connections gracefully when you receive a signal to shut down? How will you handle (blocking!) disk access and logging? These are just a few of the many complex design decisions that you will have to answer.

Application design will still be difficult, but the hope is that you will have an easier time reasoning about your application logic when you have only one thread to deal with.
