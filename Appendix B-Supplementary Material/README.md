# Appendix B - Supplementary Material

This appendix contains some additional code related to the case studies presented in
the book. You might find this material helpful to round out your understanding of
the examples.

## Cutlery Example Using Asyncio

[“Case Study: Robots and Cutlery” on page 14](#robotcut) analyzed a race condition bug caused
by multiple threads modifying the cutlery records in the global “kitchen” object
instance. For completeness, here is how we might create an async version of the
solution.
There is a specific point I want to highlight about the observability of concurrency in
the asyncio approach, shown in [Example B-1](#corobot).

*Example B-1. Cutlery management using asyncio*

```python
import asyncio
class CoroBot():
def __init__(self):
self.cutlery = Cutlery(knives=0, forks=0)
self.tasks = asyncio.Queue()
async def manage_table(self):
while True:
task = await self.tasks.get()
if task == 'prepare table':
kitchen.give(to=self.cutlery, knives=4, forks=4)
elif task == 'clear table':
self.cutlery.give(to=kitchen, knives=4, forks=4)
elif task == 'shutdown':
return
from attr import attrs, attrib
@attrs
class Cutlery:
knives = attrib(default=0)
forks = attrib(default=0)
def give(self, to: 'Cutlery', knives=0, forks=0):
self.change(-knives, -forks)
to.change(knives, forks)
def change(self, knives, forks):
self.knives += knives
self.forks += forks
kitchen = Cutlery(knives=100, forks=100)
bots = [CoroBot() for i in range(10)]
import sys
for b in bots:
for i in range(int(sys.argv[1])):
b.tasks.put_nowait('prepare table')
b.tasks.put_nowait('clear table')
b.tasks.put_nowait('shutdown')
print('Kitchen inventory before service:', kitchen)
loop = asyncio.get_event_loop()
tasks = []
for b in bots:
t = loop.create_task(b.manage_table())
tasks.append(t)
task_group = asyncio.gather(*tasks)
loop.run_until_complete(task_group)
print('Kitchen inventory after service:', kitchen)
```

1. Instead of a ThreadBot, we now have a CoroBot. This code sample uses only one
thread, and that thread will be managing all 10 separate CoroBot object
instances—one for each table in the restaurant.

2. Instead of queue.Queue, we’re using the asyncio-enabled queue.

3. This is the main point: the only places at which execution can switch between
different CoroBot instances is where the await keyword appears. It is not possible
to have a context switch during the rest of this function, and this is why there is
no race condition during the modification of the kitchen cutlery inventory.

The presence of await keywords makes context switches observable. This makes it
significantly easier to reason about any potential race conditions in concurrent appli‐
cations. This version of the code always passes the test, no matter how many tasks are
assigned:

```cmd
$ python cutlery_test_corobot.py 100000
Kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)
```

This really isn’t impressive at all: it’s an entirely predictable outcome based on the fact
that there are clearly no race conditions in the code. And that is exactly the point.

## Supplementary Material for News Website Scraper

This index.html file shown in Example B-2 is required to run the code in “Case Study:
Scraping the News” on page 93.

*Example B-2. The index.html file required for the web scraping case study*

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The News</title>
<style>
.wrapper {
display: grid;
grid-template-columns: 300px 300px 300px;
grid-gap: 10px;
width: 920px;
margin: 0 auto;
}
.box {
border-radius: 40px;
padding: 20px;
border: 1px solid slategray;
}
.cnn {
background-color: #cef;
}
.aljazeera {
background-color: #fea;
}
h1 {
text-align: center;
font-size: 60pt;
}
a {
color: black;
text-decoration: none;
}
span {
text-align: center;
font-size: 15pt;
color: black;
}
</style>
</head>
<body>
<h1>The News</h1>
<div class="wrapper">
$body
</div>
</body>
</html>
```

It’s a very basic template with rudimentary styling.

## Supplementary Material for the ZeroMQ Case Study

In “Case Study: Application Performance Monitoring” on page 102, I mentioned that
you’ll need the HTML file being served to show the metrics charts. That file,
charts.html, is presented in Example B-3. You should obtain a URL for
smoothie.min.js from [Smoothie Charts](http://smoothiecharts.org/) or one of the CDNs, and use that URL as the
src attribute instead.

*Example B-3. charts.html*

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Server Performance</title>
<script src="smoothie.min.js"></script>
<script type="text/javascript">
function createTimeline() {
var cpu = {};
var mem = {};
var chart_props = {
responsive: true,
enableDpiScaling: false,
millisPerPixel:100,
grid: {
millisPerLine: 4000,
fillStyle: '#ffffff',
strokeStyle: 'rgba(0,0,0,0.08)',
verticalSections: 10
},
labels:{fillStyle:'#000000',fontSize:18},
timestampFormatter:SmoothieChart.timeFormatter,
maxValue: 100,
minValue: 0
};
var cpu_chart = new SmoothieChart(chart_props);
var mem_chart = new SmoothieChart(chart_props);
function add_timeseries(obj, chart, color) {
obj[color] = new TimeSeries();
chart.addTimeSeries(obj[color], {
strokeStyle: color,
lineWidth: 4
})
}
var evtSource = new EventSource("/feed");
evtSource.onmessage = function(e) {
var obj = JSON.parse(e.data);
if (!(obj.color in cpu)) {
add_timeseries(cpu, cpu_chart, obj.color);
}
if (!(obj.color in mem)) {
add_timeseries(mem, mem_chart, obj.color);
}
cpu[obj.color].append(
Date.parse(obj.timestamp), obj.cpu);
mem[obj.color].append(
Date.parse(obj.timestamp), obj.mem);
};
cpu_chart.streamTo(
document.getElementById("cpu_chart"), 1000
);
mem_chart.streamTo(
document.getElementById("mem_chart"), 1000
);
}
</script>
<style>
h1 {
text-align: center;
font-family: sans-serif;
}
</style>
</head>
<body onload="createTimeline()">
<h1>CPU (%)</h1>
<canvas id="cpu_chart" style="width:100%; height:300px">
</canvas>
<hr>
<h1>Memory usage (MB)</h1>
<canvas id="mem_chart" style="width:100%; height:300px">
</canvas>
```

1. cpu and mem are each a mapping of a color to a TimeSeries() instance.

2. One chart instance is created for CPU, and one for memory usage.

3. We create a TimeSeries() instance inside the onmessage event of the
EventSource() instance. This means that any new data coming in (e.g., on a dif‐
ferent color name) will automatically get a new time series created for it. The
add_timeseries() function creates the TimeSeries() instance and adds to the
given chart instance.

4. Create a new EventSource() instance on the /feed URL. The browser will con‐
nect to this endpoint on our server, (metric_server.py). Note that the browser will
automatically try to reconnect if the connection is lost. Server-sent events are
often overlooked, but in many situations their simplicity makes them preferable
to WebSockets.

5. The onmessage event will fire every time the server sends data. Here the data is
parsed as JSON.

6. Recall that the cpu identifier is a mapping of a color to a TimeSeries() instance.
Here, we obtain that time series and append data to it. We also obtain the time‐
stamp and parse it to get the correct format required by the chart.

## Database Trigger Handling for the asyncpg Case Study

In “Case Study: Cache Invalidation” on page 115, one of the required Python source
files was omitted in the interest of saving space. That file is presented in Example B-4.

*Example B-4. triggers.py*

```python
# triggers.py
from asyncpg.connection import Connection
async def create_notify_trigger(
conn: Connection,
trigger_name: str = 'table_update_notify',
channel: str = 'table_change') -> None:
await conn.execute(
'CREATE EXTENSION IF NOT EXISTS hstore')
await conn.execute(
SQL_CREATE_TRIGGER.format(
trigger_name=trigger_name,
channel=channel))
async def add_table_triggers(
conn: Connection,
table: str,
trigger_name: str = 'table_update_notify',
schema: str = 'public') -> None:
templates = (SQL_TABLE_INSERT, SQL_TABLE_UPDATE,
SQL_TABLE_DELETE)
for template in templates:
await conn.execute(
template.format(
table=table,
trigger_name=trigger_name,
schema=schema))
SQL_CREATE_TRIGGER = """\
CREATE OR REPLACE FUNCTION {trigger_name}()
RETURNS trigger AS $$
DECLARE
id integer; -- or uuid
data json;
BEGIN
data = json 'null';
IF TG_OP = 'INSERT' THEN
id = NEW.id;
data = row_to_json(NEW);
ELSIF TG_OP = 'UPDATE' THEN
id = NEW.id;
data = json_build_object(
'old', row_to_json(OLD),
'new', row_to_json(NEW),
'diff', hstore_to_json(hstore(NEW) - hstore(OLD))
);
ELSE
id = OLD.id;
data = row_to_json(OLD);
END IF;
PERFORM
pg_notify(
'{channel}',
json_build_object(
'table', TG_TABLE_NAME,
'id', id,
'type', TG_OP,
'data', data
)::text
);
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
SQL_TABLE_UPDATE = """\
DROP TRIGGER IF EXISTS
{table}_notify_update ON {schema}.{table};
CREATE TRIGGER {table}_notify_update
AFTER UPDATE ON {schema}.{table}
FOR EACH ROW
EXECUTE PROCEDURE {trigger_name}();
"""
SQL_TABLE_INSERT = """\
DROP TRIGGER IF EXISTS
{table}_notify_insert ON {schema}.{table};
CREATE TRIGGER {table}_notify_insert
AFTER INSERT ON {schema}.{table}
FOR EACH ROW
EXECUTE PROCEDURE {trigger_name}();
"""
SQL_TABLE_DELETE = """\
DROP TRIGGER IF EXISTS
{table}_notify_delete ON {schema}.{table};
CREATE TRIGGER {table}_notify_delete
AFTER DELETE ON {schema}.{table}
FOR EACH ROW
EXECUTE PROCEDURE {trigger_name}();
"""
```

1. These functions require asyncpg, although this import is used only to allow
Connection to be used in type annotations.

2. The create_notify_trigger() coroutine function will create the trigger func‐
tion itself in the database. The trigger function will contain the name of the chan‐
nel that updates will be sent to. The code for the function itself is in the
SQL_CREATE_TRIGGER identifier, and it is set up as a format string.

3. Recall from the case study example that update notifications included a “diff ”
section in which the difference between old and new data was shown. We use the
hstore feature of PostgreSQL to calculate that diff. It provides something close to
the semantics of sets. The hstore extension is not enabled by default, so we
enable it here.

4. The desired trigger name and channel are substituted into the template and then
executed.

5. The second function, add_table_triggers(), connects the trigger function to
table events like insert, update, and delete.

6. There are three format strings for each of the three methods.

7. The desired variables are substituted into the templates and then executed.

8. This SQL code took me a lot longer than expected to get exactly right! This
PostgreSQL procedure is called for insert, update, and delete events; the way to
know which is to check the TG_OP variable. If the operation is INSERT, then NEW
will be defined (and OLD will not be defined). For DELETE, OLD will be defined but
not NEW. For UPDATE, both are defined, which allows us to calculate the diff. We
also make use of PostgreSQL’s built-in support for JSON with the row_to_json()
and hstore_to_json() functions: these mean that our callback handler will
receive valid JSON.

Finally, the call to the pg_notify() function is what actually sends the event. All
subscribers on {channel} will receive the notification.

9. This is standard trigger code: it sets up a trigger to call a specific procedure {trig
ger_name}() when a specific event occurs, like an INSERT or an UPDATE.

There are sure to be many useful applications that can be built around notifications
received from PostgreSQL.

## Supplementary Material for the Sanic Example: aelapsed

The Sanic case study (see asyncpg case study) included utility decorators for printing
out elapsed time taken by a function. These are shown in Example B-5.

*Example B-5. perf.py*

```python
# perf.py
import logging
from time import perf_counter
from inspect import iscoroutinefunction
logger = logging.getLogger('perf')
def aelapsed(corofn, caption=''):
async def wrapper(*args, **kwargs):
t0 = perf_counter()
result = await corofn(*args, **kwargs)
delta = (perf_counter() - t0) * 1e3
logger.info(
f'{caption} Elapsed: {delta:.2f} ms')
return result
return wrapper
def aprofiler(cls, bases, members):
for k, v in members.items():
if iscoroutinefunction(v):
members[k] = aelapsed(v, k)
return type.__new__(type, cls, bases, members)
```

1. The aelapsed() decorator will record the time taken to execute the wrapped
coroutine.

2. The aprofiler() metaclass will make sure that every member of the class that is
a coroutine function will get wrapped in the aelapsed() decorator.

