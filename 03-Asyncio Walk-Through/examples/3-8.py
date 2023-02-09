>>> coro = f()
>>> coro.send(None)
>>> coro.throw(Exception, 'blah')
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
 File "<stdin>", line 2, in f
Exception: blah
blah
