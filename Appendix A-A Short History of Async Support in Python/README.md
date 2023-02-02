# Appendix A - A Short History of Async Support in Python

Despite having been part of the Python standard library for a long time, the asyncore
module suffers from fundamental flaws following from an inflexible API that does not
stand up to the expectations of a modern asynchronous networking module.
Moreover, its approach is too simplistic to provide developers with all the tools they
need in order to fully exploit the potential of asynchronous networking.
The most popular solution right now used in production involves the use of third-
party libraries. These often provide satisfactory solutions, but there is a lack of compat‐
ibility between these libraries, which tends to make codebases very tightly coupled to
the library they use.

> - Laurens van Houtven, [PEP 3153 (May 2011): Asynchronous IO Support](https://oreil.ly/pNyro)

The goal of this appendix is to describe a little of the history behind async program‐
ming in Python, and the point I want to make—which still amazes me when I think
about it—is that the key innovation that we’ve been awaiting for 20 years was lan‐
guage syntax.
Many people will be surprised by this, but Asyncio is not the first attempt that has
been made to add support for asynchronous network programming to Python, as is
discussed next.


## In the Beginning, There Was asyncore

Compared to asyncore,] Twisted is better in pretty much every possible way. It’s more
portable, more featureful, simpler, more scalable, better maintained, better docu‐
mented, and it can make a delicious omelette. Asyncore is, for all intents and purposes,
obsolete.

> —Glyph ca. 2010 on [Stack Overflow](https://oreil.ly/4pEeJ)

asyncore should really be considered a historical artifact and never actually used.

> —Jean-Paul Calderone ca. 2013 on [Stack Overflow](https://oreil.ly/oWGEZ)

Support for so-called asynchronous features was added to Python a long time ago, in
the asyncore module. As you can tell from the preceding quotes, reception of asyn
core was lukewarm, and usage low. What is jaw-dropping, to this author at least, is
when this module was added: in Python 1.5.2! This is what it says at the top of Lib/
asyncore.py in the CPython source:

```python
# -*- Mode: Python -*-
# Id: asyncore.py,v 2.51 2000/09/07 22:29:26 rushing Exp
# Author: Sam Rushing <rushing@nightmare.com>
# =============================================================
# Copyright 1996 by Sam Rushing
```

Furthermore, the first paragraph of the Python [documentation for asyncore](https://oreil.ly/tPp8_) says the
following, which could easily appear in today’s documentation for asyncio:

> This module provides the basic infrastructure for writing asynchronous socket service
clients and servers.
There are only two ways to have a program on a single processor do “more than one
thing at a time.” Multithreaded programming is the simplest and most popular way to
do it, but there is another very different technique, that lets you have nearly all the
advantages of multithreading, without actually using multiple threads. It’s really only
practical if your program is largely I/O bound. If your program is processor bound,
then preemptive scheduled threads are probably what you really need. Network servers
are rarely processor bound, however.

​1996, huh? Clearly it was already possible to manage multiple socket events in a single
thread in Python back then (and, in fact, much earlier than this in other languages).
So what has changed in the past quarter-century that makes Asyncio special now?
The answer is language syntax. We’re going to be looking at this more closely in the
next section, but before closing out this window into the past, it’s worth noting a
small detail that appeared in the Python 3.6 docs for asyncore (ca. December 2016):

> Source code: Lib/asyncore.py
Deprecated since version 3.6: Please use asyncio instead.

## The Path to Native Coroutines

Recall that I’m using the term Asyncio to refer to both the Python language syntax
changes, and the new asyncio module in the standard library.1 Let’s dig into that dis‐
tinction a little more.
Today, support for asynchronous programming in Python has three distinct compo‐
nents, and it’s interesting to consider when they were added:

*Language syntax: generators*

> Keyword yield, added in Python 2.2 (2001) in [PEP 255](https://oreil.ly/35Czp) and enhanced in Python
2.5 (2005) in [PEP 342](https://oreil.ly/UDWl) with the send() and throw() methods on generator
objects, which allowed generators to be used as coroutines for the first time.
Keyword yield from, added in Python 3.3 (2009) in [PEP 380](https://oreil.ly/38jVG) to make it much
easier to work with nested yields of generators, particularly in the case where gen‐
erators are being used as makeshift (i.e., temporary) coroutines.

*Language syntax: coroutines*

> Keywords async and await, added in Python 3.5 (2015) in [PEP 492](https://oreil.ly/XJUmS), which gave
first-class support to coroutines as a language feature in their own right. This also
means that generators can again be used as generators, even inside coroutine
functions.

*Library module: asyncio*

> Added in Python 3.4 (2012) in [PEP 3156](https://oreil.ly/QKG4m), providing batteries-included support
for both framework designers and end-user developers to work with coroutines
and perform network I/O. Crucially, the design of the event loop in asyncio was
intended to provide a common base upon which other existing third-party
frameworks like Tornado and Twisted could standardize.

These three are quite distinct from each other, although you could be forgiven confu‐
sion since the history of the development of these features in Python has been diffi‐
cult to follow.
The impact of new syntax for async and await is significant, and it’s having an effect
on other programming languages too, like JavaScript, C#, Scala, Kotlin, and Dart.
It took a long time and a lot of thinking by the thousands of programmers involved in
the Python project to get us to this point.



