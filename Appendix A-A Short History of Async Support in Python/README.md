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

> - Laurens van Houtven, PEP 3153 (May 2011): Asynchronous IO Support

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

> —Glyph ca. 2010 on Stack Overflow

asyncore should really be considered a historical artifact and never actually used.

> —Jean-Paul Calderone ca. 2013 on Stack Overflow

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

Furthermore, the first paragraph of the Python documentation for asyncore says the
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





