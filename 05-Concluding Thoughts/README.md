# Chapter 5 - Concluding Thoughts

When substantial new features appear in Python, they’re new for everybody. I have
nearly two decades’ experience with Python, but I still found Asyncio difficult to
learn—even taking into account that I had already worked with Twisted and Tornado
on previous projects, so event-based programming was not new to me. I found the
asyncio API to be much more complex than I had expected. Part of this was due to a
lack of high-level documentation.
Now, having spent the time to learn how to use Asyncio in Python, I feel a lot more
comfortable with it, and this progression will likely be similar for you too. There is a
coherent structure and purpose behind the design of the API, and hopefully this book
will make it much easier for you to learn than it was for me. With a basic understand‐
ing in place, I’m now finding it quite easy to write new Asyncio-based code without
having to constantly refer back to the docs: this is a very good sign, and certainly isn’t
the case with all the standard library modules.
There are still some rough edges, though. The asyncio standard library will continue
to have a large, fine-grained API, since it caters to both framework designers and
end-user developers. This means that we—as end-user developers—will have to learn
which parts of the API are applicable to us and which are not. In time, as the third-
party library ecosystem for asyncio grows and matures, we will likely find ourselves
working with those library APIs rather than the raw asyncio standard library API.
Existing libraries like aiohttp and Sanic are good examples of this. The asyncio API
itself will also continue to improve as more people gain experience with it.
I also made unexpected discoveries along the way: by happy coincidence, it turned
out that I needed to finally learn ZeroMQ at around the same time this book was
being written, and I’m finding that asyncio in combination with pyzmq makes net‐
work programming a joy. My recommendation for the best way to learn Asyncio is to
experiment, try things out and have fun.
