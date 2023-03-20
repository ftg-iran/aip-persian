# فصل 4

# 20 کتابخانه Asyncio که از آن‌ها استفاده نمی‌کنید (اما اهمیتی ندارد)

<hr>

در این فصل مواردی را با استفاده از امکانات جدید پایتون برای برنامه‌نویسی همزمان بررسی می‌کنیم. ما از چندین کتابخانه‌ی third-party استفاده خواهیم کرد؛ همانطور که شما نیز در پروژه‌های خود از آن‌ها بهره خواهید برد.

عنوان این فصل مربوط به عنوان کتاب قبلی من با نام 20 Python Libraries You Aren't Using (But Should) (O'Reilly) است. بسیاری از آن کتابخانه‌ها برای اپلیکیشن‌های همزمان شما نیز مفید خواهند بود، اما این فصل بر روی کتابخانه‌هایی تمرکز دارد که به طور ویژه برای امکانات همزمان جدید پایتون طراحی شده‌اند.

نمایش دادن کدهای همزمان به صورت تکه‌های کوتاه دشوار است. همانطور که نمونه کدهای پیشین در این کتاب را مشاهده کرده‌اید، تلاش کرده‌ام که هر مثال را به صورت برنامه‌ای کامل و قابل اجرا ارائه دهم، زیرا مدیریت طول عمر برنامه نکته‌ای اساسی برای استفاده صحیح از برنامه‌نویسی همزمان است.

به همین دلیل، بسیاری از موردپژوهی‌ها در این فصل از جهت تعداد خطوط کد تا حدودی بزرگ‌تر از حد معمول برای چنین کتابی خواهند بود. هدف من از به‌کارگیری این رویکرد مفیدتر کردن موردپژوهی‌ها با ارائه یک "نمای کامل" از یک برنامه‌ی همزمان است تا شما دیگر ناچار به تطبیق قطعات جداگانه با یکدیگر نباشید.

<!-- ![image_00](images/00.png) -->

برخی از مثال‌های این فصل به جهت صرفه‌جویی در فضا شیوه‌نامه‌های نوشتاری را دنبال نمی‌کنند. من PEP8 را به انداز Pythinosta بعدی دوست دارم، اما کاربردی بودن کد نسبت به تمیزی آ»ن ارجحیت دارد!

## کتابخانه Streams (کتابخانه استاندارد)

پیش از آنکه کتابخانه‌های third-party را بررسی کنیم، بهتر است از کتابخانه استاندارد شروع کنیم. streams API رابط کاربری سطح بالایی است که برای برنامه‌نویسی سوکت همزمان ارائه شده است، و همانطور که موردپژوهی بعدی نشان خواهد داد، استفاده از آن بسیار آسان است. با این وجود، طراحی برنامه همچنان به دلیل ماهیت این مبحث پیچیده است.

موردپژوهی‌‌ای که در ادامه به آن می‌پردازیم اجرای یک واسط پیام (message broker) را با یک طراحی اولیه ساده و به دنبال آن یک طراحی سنجیده‌تر نشان می‌دهد. هیچ یک از این طراحی‌ها نباید جهت استفاده در 'محیط اماده‌ برای استقرار' مناسب در نظر گرفته شوند؛ هدف من این است که شما را به تفکر درباره جنبه‌های گوناگون برنامه‌نویسی شبکه همروند (cuncurrent network programming) که باید در زمان طراحی چنین برنامه‌ای در نظر گرفته شوند وادار کنم.

### موردپژوهی: صف پیام (Message Queue)

صف پیام یا همان message queue یک اپلیکیشن بکند است که از دیگر اپلیکیشن‌ها اتصالات را دریافت کرده و پیام‌هایی را میان سرویس‌های متصل رد و بدل می‌کند. از این سرویس‌ها معمولا با نام‌های انتشاردهندگان (publishers) و مشترکین (subscribers) یاد می‌شود. مشترکین معمولا جهت دریافت پیام‌ها به کانال‌های مشخصی گوش می‌دهند. معمولا می‌توان توزیع پیام در کانال‌های مختلف را به دو روش پیکربندی کرد: پیام‌ها می‌توانند به تمام مشترکین یک کانال ارسال شوند (pub-sub)، و یا هر بار یک پیام متفاوت می‌تواند به یک مشترک ارسال شود (point-to-point).

اخیرا، من بر روی پروژه‌ای کار کردم که در آن از ActiveMQ به عنوان واسط پیام برای ارتباط داخلی میکروسرویس‌ها استفاده شد. در سطح پایه، چنین واسطی (سرور) به شرح زیر عمل می‌کند:

- اتصالات پایدار سوکت را برای چندین کلاینت حفظ می‌کند
- پیام‌ها را از کلاینت با نام کانال مورد نظر دریافت می‌کند
- پیام‌های دریافتی را به تمام سرویس‌‌گیرندگان دیگری که از مشترکین کانال مورد نظر هستند ارسال می‌کند

به یاد می‌آورم که فکر می‌کردم ساخت چنین اپلیکیشنی می‌تواند تا چه حد مشکل باشد. به عنوان یک نکته اضافی، ActiveMQ می‌تواند هر دو مدل توزیع پیام را اجرا کند، و این دو مدل به طور کلی با توجه به نام کانال از یکدیگر متمایز می‌شوند:

- نام کانال‌ها با پیشوند topic/ (به طور مثال: topic/customer/registration/) با الگوی pub-sub مدیریت می‌شوند. در این مدل تمامی مشترکین کانال تمامی پیام‌ها را دریافت می‌کنند.
- نام کانال‌ها با پیشوند queue/ با استفاده از مدل point-to-point مدیریت می‌شوند. در این مدل پیام‌های یک کانال میان مشترکین کانال با الگوی round-robin توزیع می‌شوند. (هر یک از مشترکین یک پیام منحصر‌به‌فرد دریافت می‌کند)

در این موردپژوهی، ما با استفاده از این امکانات اولیه یک واسط پیام آزمایشی خواهیم ساخت. اولین مشکلی که باید به آن بپردازیم آن است که TCP یک پروتکل مبتنی بر پیام نیست. در این پروتکل ما تنها می‌توانیم جریانی از بایت‌ها را در شبکه دریافت کنیم. ما باید پروتکل خود را برای ساختار پیام‌ها ایجاد کنیم. ساده‌ترین پروتکل این است که هر پیام را با یک هدر اندازه شروع کرده و به دنبال آن پیامی با همان آن اندازه را قرار دهیم. کتابخانه‌ کاربردی در مثال 1-4 قابلیت خواندن و نوشتن را برای چنین پیام‌هایی فراهم مي‌کند.

**_مثال 1-4. پروتکل پیام: خواندن و نوشتن_**

```python
# msgproto.py
from asyncio import StreamReader, StreamWriter

async def read_msg(stream: StreamReader) -> bytes:
   size_bytes = await stream.readexactly(4)
   size = int.from_bytes(size_bytes, byteorder='big')
   data = await stream.readexactly(size)
   return data

async def send_msg(stream: StreamWriter, data: bytes):
 size_bytes = len(data).to_bytes(4, byteorder='big')
 stream.writelines([size_bytes, data])
 await stream.drain()
```

۱. چهار بایت اول را بگیرید. این همان پیشوندِ اندازه است.

۲. این 4 بایت باید به عدد (integer) تبدیل شوند

۳. حال ما اندازه پیام را می‌دانیم، پس به همان اندازه از استریم می‌خوانیم

۴. عملیات نوشتن برعکس عملیات خواندن است: ابتدا طول داده با رمزگذاری 4 بایتی، و سپس داده را ارسال می‌کنیم.

حال که یک پروتکل پیام پایه‌ای داریم، می‌توانیم روی برنامه واسط پیام در مثال 2-4 تمرکز کنیم.

**_مثال 2-4. یک سرور نمونه با 40 خط کد_**

```python
# mq_server.py
import asyncio from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from msgproto import read_msg, send_msg

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)

async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    print(f'Remote {peername} subscribed to {subscribe_chan}')

    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            print(f'Sending to {channel_name}: {data[:19]}...')
            conns = SUBSCRIBERS[channel_name]
            if conns and channel_name.startswith(b'/queue'):
                conns.rotate()
                conns = [conns[0]]
            await gather(*[send_msg(c, data) for c in conns])
    except asyncio.CancelledError:
        print(f'Remote {peername} closing connection.')
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        print(f'Remote {peername} disconnected')
    finally:
        print(f'Remote {peername} closed')
        SUBSCRIBERS[subscribe_chan].remove(writer)

async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()

try:
    asyncio.run(main(client, host='127.0.0.1', port=25000))
except KeyboardInterrupt:
    print('Bye!')

```

۱. وابستگی‌ها از ماژول msgproto.py وارد می‌شوند.

۲. مجموعه‌ای کلی از مشترکین فعال حال حاضر. هر زمان که یک کلاینت ارتباط برقرار می‌کند، ابتدا باید نام کانالی که در آن اشتراک دارد را ارسال کند. یک صف (deque) تمامی مشترکین برای یک کانال خاص را ذخیره می‌کند.

۳. تابع کوروتین ()client برای هر اتصال جدید یک coroutine بلندمدت ایجاد می‌کند. می‌توان آن را به عنوان یک بازخوانی سرور (server callback) TCP که در ()main شروع شد در نظر گرفت. در این خط نشان داده‌ام که چگونه می‌توان میزبان و پورت همتای راه دور را به دست آورد؛ به طور مثال برای ورود به سیستم.

۴. پروتکل ما برای سرویس‌گیرندگان به شرح زیر است:

- در اولین اتصال، کلاینت باید پیام را به همراه نام کانالی که قصد اشتراک در آن را دارد ارسال کند (در اینجا subscribe_chan)
- پس از آن، در طی زمان اتصال، هر کلاینت ابتدا با ارسال پیامی حاوی نام کانال مقصد، و به دنبال آن پیامی حاوی داده، پیامی را به کانال ارسال می‌کند. واسط ما چنین پیام‌هایی را به تمام مشترکان آن کانال ارسال خواهد کرد.

<p dir="rtl">۵. StreamWriter instance را به مجموعه‌ی کلی مشترکین اضافه کنید.</p>

۶. یک حلقه‌ی بی‌نهایت که در انتظار برای دریافت داده از این کلاینت است. اولین پیام از سوی کلاینت باید نام کانال مقصد باشد.

۷. در قدم بعدی دیتای اصلی که قرار است در کانال توزیع شود می‌آید.

۸. صفی که حاوی مشترکین کانال هدف است را دریافت کنید.

۹. برخی دستورالعمل‌های خاص در شرایطی که نام کانال با پیشوند queue/ آغاز می‌شود: در این صورت، داده‌ها را تنها برای یکی از مشترکین، و نه تمام آن‌ها، ارسال می‌کنیم. این راه حل می‌تواند برای به اشتراک‌گذاری کار بین یک گروه از workerها به جای روش معمول اعلان pub-sub، که در آن همه مشترکین کانال تمامی پیام‌ها را دریافت می‌کنند به کار گرفته شود.

۱۰. چرا از deque به جای list استفاده می‌کنیم: چرخش deque به ما برای ردیابی کلاینت بعدی در لیست توزیع queue\ کمک می‌کند. به نظر می‌رسد که این روش هزینه بالایی داشته باشد، البته تا زمانی که متوجه شوید هر چرخش در deque از مرتبه زمانی O(1) برخوردار است.

۱۱. فقط هر کلاینت که در صف اول است را هدف قرار دهید. در هر دور پس از چرخش صف اولین کلاینت تغییر می‌کند.

۱۲. یک لیست از coroutineها برای ارسال پیام به هر نویسنده ایجاد کنید. سپس آن‌ها را در ()gather باز کنید تا بتوانیم برای اتمام همه‌ ارسال‌‌ها منتظر بمانیم.
این خط یک نقص در برنامه ما است، اما ممکن است دلیل آن روشن نباشد: اگرچه ممکن است درست باشد که تمام ارسال‌ها به هر یک از مشترکین به صورت همزمان انجام خواهد شد، اما اگر یک مشترک بسیار کند داشته باشیم چه اتفاقی خواهد افتاد؟ در این صورت، ()gather زمانی به پایان می‌رسد که کندترین کلاینت داده خود را دریافت کرده باشد. تا زمانی که کوروتین‌های ()send_msg تمام نشده‌اند نمی‌توانیم داده بیش‌تری از کلاینت ارسال‌کننده دریافت کنیم. این مسئله سرعت توزیع تمام پیام‌ها را به اندازه سرعت کندترین مشترک کاهش می‌دهد.

۱۳. زمانی که از کوروتین ()client خارج می‌شویم،‌ مطمئن می‌شویم که خود را از مجموعه‌ی کلی مشترکین (SUBSCRIBERS) نیز حذف کنیم. متاسفانه مرتبه زمانی این عملیات O(n) است که می‌تواند برای n بسیار بزرگ کمی هزینه‌بر باشد. یک ساختار داده متفاوت می‌تواند این مشکل را برطرف کند. اما در حال حاضر خودمان را با دانستن این مورد که اتصالات برای زمان طولانی در نظر گرفته شده‌اند تسلی می‌دهیم، بنابراین تعداد کمی رویداد قطعی ارتباط‌ خواهیم داشت. همچنین مقدار بسیار بزرگ (مثلا 10000~ به عنوان تخمین مرتبه بزرگی) برای n بعید است. همینطور درک این کد نیز نسبتا راحت است.

پس این سرورِ ما است. اکنون به کلاینت‌ها نیاز داریم، و سپس می‌توانیم برخی از خروجی‌ها را نشان دهیم. برای اهداف نمایشی،‌ دو نوع کلاینت خواهم ساخت: یک فرستنده و یک شنونده. در سرور تفاوتی ایجاد نمی‌شود، تمامی کلاینت‌ها یکسان هستند و تفاوت میان عملکرد فرستنده و شنونده تنها برای اهداف آموزشی است. مثال 3-4 کد مربوط به برنامه شنونده را نشان می‌دهد.

**_مثال 3-4. شنونده: جعبه ابزاری برای گوش دادن به پیام‌ها در واسط پیام_**

```python
# mq_client_listen.py
import asyncio import argparse, uuid
from msgproto import read_msg, send_msg

async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f'Starting up {me}')
    reader, writer = await asyncio.open_connection(
        args.host, args.port)
    print(f'I am {writer.get_extra_info("sockname")}')
    channel = args.listen.encode()
    await send_msg(writer, channel)
    try:
        while data := await read_msg(reader):
            print(f'Received by {me}: {data[:20]}')
            print('Connection ended.')
    except asyncio.IncompleteReadError:
        print('Server closed.')
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=25000)
    parser.add_argument('--listen', default='/topic/foo')

    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        print('Bye!')
```

۱. ماژول کتابخانه استاندارد uuid روشی آسان جهت ایجاد هویت برای این شنونده است. اگر چندین instance را ایجاد کنید، هر یک از آن‌ها هویت مخصوص به خود را خواهد داشت، و شما می‌توانید بدین وسیله آن چه را که در لاگ‌ها اتفاق می‌افتد را ردیابی کنید.

۲. یک ارتباط به سرور برقرار کنید.

۳. کانالی که باید در آن مشترک شوید یک پارامتر ورودی است که در args.listen ثبت شده است. پیش از ارسال آن را به بایت کدگذاری کنید.

۴. طبق قوانین پروتکل ما (همانطور که در تحلیل کد واسط پیام به آن پرداختیم)، اولین کاری که باید پس از اتصال انجام دهیم ارسال نام کانال برای اشتراک است.

۵. این حلقه تنها برای دریافت داده بر روی سوکت منتظر می‌ماند.

۶. آرگومان‌های خط فرمان برای این برنامه، اشاره به یک میزبان، یک پورت، و یک نام کانال برای گوش دادن را آسان می‌کنند.

کد برای کلاینت دیگر (برنامه فرستنده) که در مثال 4-4 نشان داده شده است ساختاری مشابه ماژول شنونده دارد.

**_مثال 4-4. فرستنده: جعبه ابزاری برای ارسال داده به واسط پیام_**

```python
# mq_client_sender.py
import asyncio
import argparse, uuid
from itertools import count
from msgproto import send_msg

async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f'Starting up {me}')
    reader, writer = await asyncio.open_connection(
        host=args.host, port=args.port)
    print(f'I am {writer.get_extra_info("sockname")}')
    channel = b'/null'
    await send_msg(writer, channel)

    chan = args.channel.encode()
    try:
        for i in count():
            await asyncio.sleep(args.interval)
            data = b'X'*args.size or f'Msg {i} from {me}'.encode()
            try:
                await send_msg(writer, chan)
                await send_msg(writer, data)
            except OSError:
                print('Connection ended.')
                break
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=25000, type=int)
    parser.add_argument('--channel', default='/topic/foo')
    parser.add_argument('--interval', default=1, type=float)
    parser.add_argument('--size', default=0, type=int)

    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        print('Bye!')
```

۱. همانند چیزی که در برنامه شنونده داشتیم، یک هویت مشخص کنید.‌

۲. یک اتصال برقرار کنید.

۳. طبق قوانین پروتکل ما، اولین کاری که باید پس از اتصال به سرور انجام دهیم ارسال نام کانال برای اشتراک است؛ با این وجود از آنجایی که ما یک فرستنده هستیم اشتراک در هیچ کانالی برایمان اهمیت ندارد. با این حال پروتکل به ارسال نام کانال نیاز دارد، بنابراین فقط یک null به عنوان نام کانال ارائه دهید (در واقعیت به هیچ چیز گوش نمی‌دهیم)

۴. نام کانال برای اشتراک را ارسال کنید.

۵. پارامتر خط فرمان args.channel کانالی که قصد ارسال پیام به آن داریم را ارائه می‌دهد. این مقدار باید پیش از ارسال به بایت تبدیل شود.

۶. استفاده از ()itertools.count مانند استفاده از یک حلقه‌ی while True است. استفاده از این مورد در پیام‌های دیباگ می‌تواند ردیابی مبدا و مقصد پیام‌ها را کمی آسان‌تر کند.

۷. تاخیری که میان پیام‌های ارسال‌شده وجود دارد یک پارامتر ورودی است که در args.interval ارائه می‌شود. خط بعدی پیام مورد نظر را تولید می‌کند. این پیام یا رشته‌ای از بایت‌ها با اندازه‌ای مشخص(args.size)، و یا یک پیام توصیفی است. این انعطاف‌پذیری تنها برای تست و آزمایش است.

۸. توجه داشته باشید که در اینجا دو پیام ارسال می‌شود: اولی نام کانال مقصد، و دومی پیام اصلی است.

۹. مانند شنونده، گزینه‌های زیادی در خط فرمان برای تغییر دادن فرستنده وجود دارند: channel نام کانال مقصد برای ارسال پیام، و interval تاخیر میان ارسال‌ها را مشخص می‌کند. پارامتر size نیز اندازه متن اصلی هر پیام را کنترل می‌کند.

حال ما یک واسط پیام، یک شنونده، و یک فرستنده داریم؛ وقت آن است که کمی از خروجی‌ها را مشاهده کنیم. برای تولید کدهای زیر ابتدا سرور را راه‌اندازی کرده و پس از آن دو شنونده و یک فرستنده را ایجاد کردم. سپس، پس از ارسال چند پیام سرور را با Ctrl-c متوقف کردم. خروجی سرور در **مثال 5-4** نشان داده شده است. خروجی فرستنده در **مثال 6-4**، و خروجی شنونده نیز در مثال‌های **7-4** و **8-4** نشان داده شده‌اند.

**_مثال 5-4. خروجی واسط پیام‌(سرور)_**

```bash
$ mq_server.py
Remote ('127.0.0.1', 55382) subscribed to b'/queue/blah'
Remote ('127.0.0.1', 55386) subscribed to b'/queue/blah'
Remote ('127.0.0.1', 55390) subscribed to b'/null'
Sending to b'/queue/blah': b'Msg 0 from 6b5a8e1d'...
Sending to b'/queue/blah': b'Msg 1 from 6b5a8e1d'...
Sending to b'/queue/blah': b'Msg 2 from 6b5a8e1d'...
Sending to b'/queue/blah': b'Msg 3 from 6b5a8e1d'...
Sending to b'/queue/blah': b'Msg 4 from 6b5a8e1d'...
Sending to b'/queue/blah': b'Msg 5 from 6b5a8e1d'...
^CBye!
Remote ('127.0.0.1', 55382) closing connection.
Remote ('127.0.0.1', 55382) closed
Remote ('127.0.0.1', 55390) closing connection.
Remote ('127.0.0.1', 55390) closed
Remote ('127.0.0.1', 55386) closing connection.
Remote ('127.0.0.1', 55386) closed
```

**_Example 4-6. Sender (client) output_**

**_مثال 6-4. خروجی فرستنده (کلاینت)_**

```bash
$ mq_client_sender.py --channel /queue/blah
Starting up 6b5a8e1d
I am ('127.0.0.1', 55390)
Connection ended.
```

**_Example 4-7. Listener 1 (client) output_**

**_مثال 7-4. خروجی شنونده1 ‌(کلاینت)_**

```bash
$ mq_client_listen.py --listen /queue/blah
Starting up 9ae04690
I am ('127.0.0.1', 55382)
Received by 9ae04690: b'Msg 1 from 6b5a8e1d'
Received by 9ae04690: b'Msg 3 from 6b5a8e1d'
Received by 9ae04690: b'Msg 5 from 6b5a8e1d'
Server closed.
```

**_Example 4-8. Listener 2 (client) output_**

**_مثال 8-4. خروجی شنونده2 (کلاینت)_**

```bash
$ mq_client_listen.py --listen /queue/blah
Starting up bd4e3baa
I am ('127.0.0.1', 55386)
Received by bd4e3baa: b'Msg 0 from 6b5a8e1d'
Received by bd4e3baa: b'Msg 2 from 6b5a8e1d'
Received by bd4e3baa: b'Msg 4 from 6b5a8e1d'
Server closed.
```

واسط پیام آزمایشی ما کار می‌کند. همچنین فهم کد نیز با توجه به پیچیده‌ بودن مشکل تا حدودی آسان است. اما متاسفانه، طراحی واسط به خودیِ خود مشکل‌ساز است.

مشکل این است که برای یک کلاینت خاص، جهت ارسال پیام‌ها به مشترکین از همان کوروتینی استفاده می‌کنیم که پیام‌های جدید در آن دریافت می‌شوند. این بدان معناست که اگر هر یک از مشترکین در دریافت پیامِ ارسالی کند عمل کند، ممکن است کامل شدن خط مربوط به ()await gather در **مثال 2-4** طول بکشد، و ما نمی‌توانیم در زمان انتظار پیام‌های بیش‌تری را دریافت و پردازش کنیم.

در عوض ما باید دریافت پیام‌ها را از ارسال پیام‌ها جدا کنیم. در موردپژوهی بعدی، کد خود را برای انجام همین کار تغییر خواهیم داد.

### موردپژوهی: بهبود صف پیام

در این موردپژوهی، طراحی واسط پیام آزمایشی خود را بهبود می‌دهیم. برنامه‌های فرستنده و شنونده بدون تغییر باقی می‌مانند. تغییر خاصی که برای طراحی واسط جدید در نظر داریم جداسازی ارسال و دریافت پیام‌ها است. انجام این کار همانطور که در بخش قبلی به آن پرداختیم می‌تواند مشکل مربوط به کند شدن دریافت پیام‌های جدید به خاطر مشترکین کند را برطرف کند. کد جدید که در مثال 6-4 نشان داده شده است تنها کمی طولانی‌تر است.

**_مثال 9-4. واسط پیام: طراحی بهبودیافته_**

```python
# mq_server_plus.py
import asyncio
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from msgproto import read_msg, send_msg

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHAN_QUEUES: Dict[bytes, Queue] = {}

async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    send_task = asyncio.create_task(
        send_client(writer, SEND_QUEUES[writer]))
    print(f'Remote {peername} subscribed to {subscribe_chan}')
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            if channel_name not in CHAN_QUEUES:
                CHAN_QUEUES[channel_name] = Queue(maxsize=10)
                asyncio.create_task(chan_sender(channel_name))
            await CHAN_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f'Remote {peername} connection cancelled.')
    except asyncio.IncompleteReadError:
        print(f'Remote {peername} disconnected')
    finally:
        print(f'Remote {peername} closed')
        await SEND_QUEUES[writer].put(None)
        await send_task
        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscribe_chan].remove(writer)

async def send_client(writer: StreamWriter, queue: Queue):
    while True:
        try:
            data = await queue.get()
        except asyncio.CancelledError:
            continue

        if not data:
            break

        try:
            await send_msg(writer, data)
        except asyncio.CancelledError:
            await send_msg(writer, data) writer.close()
            await writer.wait_closed()

async def chan_sender(name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[name]
            if not writers:
                await asyncio.sleep(1)
                continue
            if name.startswith(b'/queue'):
                writers.rotate()
                writers = [writers[0]]
            if not (msg := await CHAN_QUEUES[name].get()):
                break
            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f'Sending to {name}: {msg[:19]}...')
                    await SEND_QUEUES[writer].put(msg)

async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()

try:
    asyncio.run(main(client, host='127.0.0.1', port=25000))
except KeyboardInterrupt:
    print('Bye!')
```

۱. در پیاده‌سازی قبلی، تنها SUBSCRIBERS را داشتیم، اکنون SEND_QUEUES و CHAN_QUEUES به عنوان مجموعه‌های سراسری وجود دارند. این مسئله نتیجه‌ی جداسازی کامل ارسال و دریافت داده است. SEND_QUEUES یک ورودی صف برای هر اتصال کلاینت دارد: هر داده‌ای که قرار است به کلاینت مورد نظر ارسال شود باید در این صف قرار گیرد. (اگر کمی جلوتر را بررسی کنید، کوروتین ()send_client داده‌ها را از SEND_QUEUES خارج کرده و ارسال می‌کند.)

۲. تا این مرحله در تابع کوروتین ()client، کد مربوطه با کد سرور ساده‌ای که داشتیم یکسان است: نام کانال برای اشتراک دریافت می‌شود و instance مربوط به StreamWriter برای کلاینت جدید به مجموعه‌ی سراسری SUBSCRIBERS اضافه می‌شود.

۳. قابلیت جدیدی که وجود دارد: یک تسک بلندمدت ایجاد می‌کنیم که تمام ارسال‌‌های داده‌ها به این کلاینت را بر عهده خواهد داشت. این تسک به عنوان یک کوروتین کاملا جداگانه به صورت مستقل اجرا شده و پیام‌ها را از صف ارائه‌شده یا همان SEND_QUEUES[writer] جهت ارسال خارج می‌کند.

۴. اکنون در حلقه‌ای قرار داریم که جهت دریافت داده تعبیه شده است. به یاد داشته باشید که ما همیشه دو پیام دریافت می‌کنیم: یکی برای کانال هدف، و دیگری برای داده اصلی. یک صف جدید و اختصاصی برای هر کانال مقصد ایجاد کرده و آن را CHAN_QUEUES می‌نامیم: زمانی که هر یک از کلاینت‌ها می‌خواهد داده‌ای را به یک کانال ارسال کند،‌ ما آن داده را در صف مناسب قرار می‌دهیم و بلافاصله برای گوش دادن جهت دریافت داده‌های بیش‌تر بازمی‌گردیم. این رویکرد موجب جداسازی توزیع پیام‌ها از دریافت پیام‌ها از این کلاینت می‌شود.

۵. اگر از قبل صفی برای کانال هدف وجود ندارد صف جدیدی ایجاد کنید.

۶. یک تسک اختصاصی و بلندمدت برای آن کانال ایجاد کنید. کوروتین ()chan_sender مسئول برداشتن داده از صف کانال و توزیع آن به مشترکین خواهد بود.

۷. داده دریافتی جدید را به صف کانال مربوطه اضافه کنید. اگر صف پر شد، همینجا منتظر خواهیم ماند تا برای داده جدید فضای کافی ایجاد شود. انتظار در اینجا به معنای آن است که هیچ داده جدیدی از سوکت نخواهیم خواند. این بدان معناست که کلاینت نیز باید در سمت خود برای ارسال داده جدید به سوکت منتظر بماند. این مسئله لزوما چیز بدی نیست، زیرا فشار برگشتی را به کلاینت منتقل می‌کند. (با توجه به شرایط، می‌توانید پیام‌ها را در این نقطه حذف کنید.)

۸. زمانی که اتصال بسته می‌شود زمان پاکسازی فرا رسیده است. می‌توانیم تسک بلندمدتی که برای ارسال داده به این کلاینت ایجاد کرده‌بودیم (send_task) را با قرار دادن None در صفِ آن (SEND_QUEUES[writer]) متوقف کنیم. (()send_client را در کد بررسی کنید.) مهم است که به جای لغو کامل صف، مقداری را در آن قرار دهیم؛ زیرا ممکن است همچنان داده‌ای در صف وجود داشته باشد که بخواهیم پیش از پایان ()send_client ارسال شود.

۹. صبر کنید تا کار فرستنده به پایان برسد...

۱۰. ...سپس ورودی مجموعه‌ی SEND_QUEUES را حذف کنید(و در خط بعدی نیز همانند قبل سوکت را از مجموعه‌ی SUBSCRIBERS حذف می‌کنیم).

۱۱. تابع کوروتین ()send_client تقریبا یک مثال کامل از جمع‌آوری کار از صف است. به خروج کوروتین تنها در شرایطی که در صف None باشد توجه کنید. همچنین توجه داشته باشید که چگونه CancelledError را داخل حلقه سرکوب می‌کنیم: این کار را بدین دلیل انجام می‌دهیم که می‌خواهیم تسک تنها در زمانی به پایان رسد که از صف None دریافت شود. بدین ترتیب، تمام داده‌های در حال انتظار در صف پیش از خاموشی ارسال می‌شوند.

۱۲. تابع ()chan_sender منطق توزیع برای یک کانال است: این تابع داده را از یک instance صف کانال اختصاصی به تمام مشترکین آن کانال ارسال می‌کند. اما در صورتی که هنوز مشترکی برای این کانال وجود نداشته باشد چه اتفاقی می‌افتد؟ فقط کمی صبر می‌کنیم و سپس دوباره تلاش می‌کنیم. (البته توجه داشته باشید که صف این کانال (CHAN_QUEUES[name]) به پر شدن ادامه خواهد داد.)

۱۳. همانند پیاده‌سازی قبلی که برای واسط پیام داشتیم، برای کانال‌هایی که نام آن‌ها با queue/ آغاز می‌شود کار خاصی انجام می‌دهیم: deque را می‌چرخانیم و تنها به اولین ورودی ارسال می‌کنیم. این کار همانند یک سیستم load-balancing ابتدایی عمل می‌کند، زیرا هر یک از مشترکین پیام متفاوتی را از یک صف یکسان دریافت می‌کند. برای تمام کانال‌های دیگر، تمام مشترکین تمام پیام‌ها را دریافت می‌کنند.

۱۴. در اینجا برای داده‌ای که در صف است منتظر می‌مانیم و اگر None دریافت شد خارج می‌شویم. در حال حاضر، این کار در هیچ یک از نقاط برنامه انجام نمی‌شود (پس کوروتین‌های ()chan_sender تا ابد به فعالیت ادامه می‌دهند)، اما اگر منطقی برای پاکسازی تسک‌های مربوط به کانال‌ها داشته باشیم، مثلا پس از یک دوره عدم فعالیت، می‌توانیم این کار را انجام دهیم.

۱۵. داده دریافت شده است،‌ پس حالا زمان آن است که آن را به مشترکین ارسال کنیم. عملیات ارسال را در اینجا انجام نمی‌دهیم: در عوض داده را در صف ارسال هر یک از مشترکین قرار می‌دهیم. این جداسازی لازم است تا مطمئن شویم که مشترکینِ کند باعث کاهش سرعت دریافت داده توسط دیگران نمی‌شوند. علاوه بر این،‌ اگر یکی از مشترکین آنقدر کند باشد که صف ارسال وی پر شود، داده را به صف او اضافه نمی‌کنیم؛ مثلا آن را از دست رفته در نظر می‌گیریم.

این طراحی همان خروجی طراحی پیشین که پیاده‌سازی ساده‌تری داشت تولید می‌کند. اما حالا می‌توانیم مطمئن باشیم که یک شنونده‌ی کند در توزیع پیام به دیگر شنونده‌ها تداخلی نخواهد داشت.

این دو موردپژوهی، پیشرفت در تفکر پیرامون طراحی یک سیستم توزیع پیام را نشان می‌دهند. یکی از جنبه‌های کلیدی فهم این نکته بود که بهتر است ارسال و دریافت پیام بسته به مورد استفاده در کوروتین‌های جداگانه‌ای انجام شوند. در چنین مواردی استفاده از صف‌ها برای جابجایی داده میان کوروتین‌های متفاوت و همچنین فراهم کردن بافر جهت جداسازی آن‌ها بسیار مفید است.

هدف مهم‌تری که از این موردپژوهی‌ها داشتیم نشان دادن این نکته بود که استفاده از streams API در برنامه‌نویسی همزمان چگونه می‌تواند ساخت یک برنامه‌ی مبتنی بر سوکت را بسیار آسان کند.

## Twisted

پروژه‌ی **Twisted** بسیار قبل‌تر از کتابخانه استاندارد asyncio ارائه شد و اکنون حدود 14 سال است که پرچم برنامه‌نویسی async در پایتون را در دست دارد. این پروژه نه تنها ابزارهای پایه مانند event loop را ارائه می‌دهد، بلکه ابزارهای اولیه مانند deferredها که کمی به futures در asyncio شبیه هستند را نیز فراهم می‌کند. طراحی asyncio به میزان قابل توجهی از Twisted و تجربه بالای رهبران و نگهدارندگان آن الهام گرفته شده است.

توجه داشته باشید که **asyncio جایگزین Twisted نیست**. Twisted شامل پیاده‌سازی‌های بسیار باکیفیت از تعداد زیادی از پروتکل‌های اینترنتی از جمله HTTP، XMPP،‌ NNTP، IMAP، SSH، IRC، و FTP(هم سرور و هم کلاینت) است. این لیست همچنان ادامه دارد: DNS, SMTP, POP3. در دسترس بودن پیاده‌سازی این پروتکل‌های اینترنتی Twisted را جذاب‌ می‌کند.

در سطح کد، تفاوت اصلی میان asyncio و Twisted جدا از زمینه‌ی تاریخی، این است که پایتون تا مدت زیادی فاقد پشتیبانی زبانی برای کوروتین‌ها بود، و این بدان معنا بود که Twisted و پروژه‌های مانند آن باید راه‌هایی برای مواجهه با ناسازگاری همزمانی و سینتکس پایتون یافت می‌کردند.

تا مدت زیادی از تاریخِ Twisted، ابزاری که برای برنامه‌نویسی همزمان مورد استفاده قرار می‌گرفت callbackها بودند که پیچیدگی‌های غیرخطی به همراه داشتند. با این وجود، زمانی که استفاده از generatorها به عنوان کوروتین‌های موقت امکان‌پذیر شد، ناگهان امکان کدنویسی خطی در Twisted با استفاده از defer@ نیز فراهم شد. دکوراتور inlineCallback که در **مثال 10-4** نشان داده شده است.

**_مثال 10-4. Twisted با inline callbacks_**

```python
@defer.inlineCallbacks
def f():
    yield defer.returnValue(123)

@defer.inlineCallbacks
def my_coro_func():
    value = yield f()
    assert value == 123
```

۱. به طور معمول، در Twisted برای ایجاد برنامه‌های همزمان، نیاز به ساخت instanceهایی از Deferred و اضافه کردن callbackها به این نمونه‌ها است. چند سال پیش، دکوراتور `inlineCallbacks@` اضافه شد که generatorها را به عنوان کوروتین‌ها مورد استفاده قرار می‌دهد.

۲. در حالی که `inlineCallbacks@` برخلاف callbackها به شما اجازه‌ی نوشتن برنامه به صورت ظاهرا خطی را می‌داد، به ترفندهایی نیز نیاز پیدا می‌کردید، مثلا صدا زدن `()defer.returnValue`، که روشی برای برگشت مقادیر از کوروتین‌های `inlineCallbacks@` است.

۳. در اینجا می‌توانیم yield را مشاهده کنیم که این تابع را به یک generator تبدیل می‌کند. برای آنکه `inlineCallbacks@` کار کند، حداقل یک yield باید در تابعی که دکوراتور را برای آن استفاده می‌کنیم به کار گرفته شود.

از زمانی که کوروتین‌های اصلی در پایتون 3.5 اضافه شدند، تیم Twisted (و به خصوص Amber Brown) در حال کار برای اضافه کردن پشتیبانی اجرای Twisted در حلقه‌ی رویداد asyncio بوده‌اند.

این یک تلاش مداوم است، و هدف من در این بخش قانع کردن شما برای استفاده از Twisted و asyncio به طور ترکیبی در برنامه‌هایتان نیست. بلکه هدف من آگاه‌ کردن شما از کارهای مهمی است که در حال حاضر برای ایجاد قابلیت همکاری میان این دو انجام می‌شود.

برای کسانی که تجربه‌ی کار با Twisted را دارند، **مثال 11-4** می‌تواند ناراحت‌کننده باشد.

**_مثال 11-4. پشتیبانی از asyncio در Twisted_**

```python
# twisted_asyncio.py
from time import ctime
from twisted.internet import asyncioreactor
asyncioreactor.install()
from twisted.internet import reactor, defer, task

async def main():
    for i in range(5):
        print(f'{ctime()} Hello {i}')
        await task.deferLater(reactor, 1, lambda: None)

defer.ensureDeferred(main())
reactor.run()
```

۱. این روشی است که با استفاده از آن به Twisted می‌گویید که از حلقه‌ی رویداد `asyncio` به عنوان reactor اصلی خود استفاده کند. توجه داشته باشید که این خط باید پیش از import کردن reactor از `twisted.internet` در خط بعدی بیاید.

۲. هر کسی که با برنامه‌نویسی Twisted آشنا باشد این importها را خواهد شناخت. ما در اینجا فضایی برای پوشش عمیق این مبحث نداریم، اما به طور خلاصه، reactor یک ورژن از حلقه‌ی `asyncio` در `Twisted` است، و `defer` و `task` در واقع namespaceهایی برای ابزارهای مربوط به کوروتین‌های زمانبندی هستند.

۳. مشاهده‌ی `async def` در یک برنامه‌ی Twisted عجیب است. اما این همان چیزی است که پشتیبانیِ جدید `async/await` در اختیار ما قرار می‌دهد: قابلیت استفاده از کوروتین‌های اصلی به طور مستقیم در برنامه‌های Twisted.

۴. در دنیای قدیمی‌تر `inlineCallbacks@`، از اینجا از yield استفاده می‌کردید، اما حال می‌توانیم مانند چیزی که در کد `asyncio` داشتیم از await استفاده کنیم. بخش دیگر این خط، `()deferLater`، روشی جایگزین برای انجام همان کاری است که `asyncio.sleep(1)` انجام می‌دهد. ما منتظر آینده‌ای هستیم که در آن پس از گذشت 1 ثانیه، یک callback بدون هیچ محتوایی اجرا می‌شود.

۵. تابع `()ensureDeferred` نسخه‌ی Twisted برای زمانبندی کوروتین‌ها است. مشابه همان کاری که `()loop.create_task` یا `()asyncio.ensure_future` انجام مي‌دادند.

۶. اجرا کردن reactor مانند `()loop.run_forever` در asyncio است.

اجرا کردن این قطعه کد خروجی زیر را تولید می‌کند:

```bash
$ twisted_asyncio.py
Mon Oct 16 16:19:49 2019 Hello 0
Mon Oct 16 16:19:50 2019 Hello 1
Mon Oct 16 16:19:51 2019 Hello 2
Mon Oct 16 16:19:52 2019 Hello 3
Mon Oct 16 16:19:53 2019 Hello 4
```

مباحث زیادی برای یادگیری درباره Twisted وجود دارد. به طور خاص، مرور پیاده‌سازی‌های پروتکل‌های شبکه ارزش وقت شما را خواهند داشت. هنوز کارهای زیادی وجود دارند، اما آینده برای همکاری میان Twisted و asyncio بسیار روشن به نظر می‌رسد.

خوشبختانه asyncio به گونه‌ای طراحی شده است که می‌توانیم انتظار آینده‌ای را داشته باشیم که در آن امکان ترکیب کدهای بسیاری از فریمورک‌های async از جمله Twisted و Tornado در یک برنامه‌ی واحد، در حالی که همه کدها در یک حلقه‌ی رویداد اجرا می‌شوند وجود داشته باشد.

## صف Janus

صف Janus (که با `pip install janus` نصب می‌شود) راه حلی برای ارتباط میان رشته‌ها (threads) و کوروتین‌ها ارائه می‌دهد. در کتابخانه استاندارد پایتون، دو نوع صف وجود دارد:

`queue.Queue`

- یک صف مسدودکننده که معمولا برای ارتباط و بافر کردن میان رشته‌ها استفاده می‌شود.

`asyncio.Queue`

- یک صف سازگار با برنامه‌نویسی همزمان، که معمولا برای ارتباط و بافر کردن میان کوروتین‌ها استفاده می‌شود.

متاسفانه، هیچ یک از این دو برای ارتباط میان رشته‌ها و کوروتین‌ها مفید نیستند! اینجاست که Janus وارد می‌شود: Janus یک صف است که هر دو API را نمایش می‌دهد، یک API مسدودکننده و یک API همزمان. مثال 12-4 از داخل یک رشته داده تولید کرده و آن را در یک صف قرار می‌دهد، و سپس آن داده‌ها را از یک کوروتین مصرف می‌کند.

**_مثال 12-4. متصل کردن رشته‌ها و کوروتین‌ها با صف Janus_**

---

```python
# janus_demo.py
import asyncio
import random
import time
import janus

async def main():
    loop = asyncio.get_running_loop()
    queue = janus.Queue(loop=loop)
    future = loop.run_in_executor(None, data_source, queue)
    while (data := await queue.async_q.get()) is not None:
        print(f'Got {data} off queue')
        print('Done.')

def data_source(queue):
    for i in range(10):
        r = random.randint(0, 4)
        time.sleep(r)
        queue.sync_q.put(r)
    queue.sync_q.put(None)

asyncio.run(main())
```

۱. یک صف Janus بسازید. توجه داشته باشید که دقیقا مانند asyncio.Queue، صف Janus با یک حلقه رویداد خاص مرتبط خواهد بود. اگر پارامتر حلقه را ارائه نکنید، فراخوانی استاندارد `()get_event_loop` به صورت داخلی استفاده خواهد شد.

۲. تابع کوروتین `()main` ما منتظر داده در یک صف است. این خط دقیقا تا زمانی که داده وجود داشته باشد معلق می‌ماند، دقیقا مانند فراخوانی `()get` بر روی یک instance از `asyncio.Queue`. شئ صف دو چهره دارد: این `async_q` نام دارد و API صف سازگار با async را ارائه می‌دهد.

۳. یک پیام چاپ کنید.

۴. داخل تابع ()data_source، یک عدد تصادفی تولید می‌شود، که هم به عنوان مدت زمان خواب و هم به عنوان مقدار داده استفاده می‌شود. توجه داشته باشید که فراخوانی ()time.sleep برنامه را مسدود می‌کند، پس این تابع باید در یک رشته اجرا شود.

۵. داده را در صف Janus قرار دهید. این خط چهره‌های دیگر صف Janus را نشان می‌دهد: `sync_q`، که API استاندارد و مسدودکننده `Queue` را ارائه می‌دهد.

خروجی بدین شکل است:

```bash
$ <name>
Got 2 off queue
Got 4 off queue
Got 4 off queue
Got 2 off queue
Got 3 off queue
Got 4 off queue
Got 1 off queue
Got 1 off queue
Got 0 off queue
Got 4 off queue
Done.
```

اگر می‌توانید، بهتر است برای داشتن کارهای اجرایی کوتاه‌مدت هدف‌گذاری کنید، و در چنین شرایطی، به صف (برای ارتباط) نیازی نخواهد بود. با این حال، این کار همیشه ممکن نیست، و در چنین شرایطی، صف Janus می‌تواند مناسب‌ترین راه برای توزیع و پوشش داده میان رشته‌ها و کوروتین‌ها باشد.

## aiohttp

<p dir="rtl"> aiohttp تمام موارد مربوط به HTTP را به asyncio می‌آورد؛ از جمله پشتیبانی از سرویس‌گیرندگان و سرورهای HTTP، و همچنین پشتیبانی از WebSocket. بیاید مستقیما به نمونه‌های کد بپردازیم، و با نمونه‌ای بسیار ساده شروع کنیم: "Hello World."</p>

### موردپژوهی: Hello World

**مثال 13-4\*** یک وب سرور ساده و کوچک با استفاده از aiohttp را نشان می‌دهد.

**_مثال 13-4. مثالی ساده و کوچک از aiohttp_**

```python
from aiohttp import web

async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.router.add_get('/', hello)
web.run_app(app, port=8080)
```

۱. یک instance از `Application` ساخته می‌شود.

۲. یک route ساخته می‌شود، که کوروتین هدف `()hello` به عنوان handler به آن داده می‌شود.

۳. وب اپلیکیشن اجرا می‌شود.

مشاهده می‌شود که هیچ اشاره‌ای به حلقه‌ها، تسک‌ها، و یا futureها در این کد نشده است. توسعه‌دهندگان aiohttp تمام این موارد را از ما پنهان کرده‌ و یک API بسیار تمیز باقی گذاشته‌اند. این کار در بسیاری از فریمورک‌هایی که بر روی asyncio ساخته می‌شوند بسیار رایج است، که به طراحان فریمورک‌ها اجاره می‌دهد که تنها بخش‌هایی را که به آن‌ها نیاز دارند انتخاب کرده و آن‌ها را در API ترجیحی خود محصور کنند.

### موردپژوهی: استخراج اخبار

کتابخانه aiphttp می‌تواند هم به عنوان یک سرور و هم به عنوان یک کتابخانه کلاینت مورد استفاده قرار گیرد، دقیقا همانند کتابخانه‌ بسیار محبوب (و البته مسدودکننده) `requests`.

در این موردپژوهی،وبسایتی را طراحی خواهیم کرد که در پشت صحنه به web scraping مشغول است. این برنامه دو سایت خبری را scrape کرده و عناوین خبری را در یک صفحه نتایج ترکیب می‌کند. استراتژی ما بدین صورت است:

۱. یک مرورگر کلاینت درخواستی به http://localhost:8080/news. ارسال می‌کند

۲. وب سرور ما درخواست را دریافت می‌کند، و سپس بکند داده‌ی HTML را از چندین وبسایت خبری دریافت می‌کند.

۳. داده‌ی هر صفحه برای به دست آوردن تیترهای خبری scrape می‌شود.

۴. تیترهای خبری به شکل پاسخ HTML که به مرورگر کلاینت ارسال می‌کنیم قالب‌بندی و مرتب می‌شوند.

**شکل 1-4** خروجی را نشان می‌دهد.

![شکل 1-4. نتیجه نهایی استخراج اخبار: تیترهای خبری از CNN به یک رنگ، و تیترهای AI Jazeera به رنگی دیگر نمایش داده می‌شوند.](images/uaip_0401.png)
شکل 1-4. نتیجه نهایی استخراج اخبار: تیترهای خبری از CNN به یک رنگ، و تیترهای Al Jazeera به رنگی دیگر نمایش داده می‌شوند.

امروزه استخراج داده از وب (web scraping) بسیار دشوار شده است. به طور مثال اگر `requests.get('http://edition.cnn.com')` را امتحان کنید، مشاهده خواهید کرد که پاسخی که دریافت می‌کنید حاوی داده‌های قابل استفاده بسیار کمی است! برای به دست آوردن داده‌های مورد نیاز، توانایی اجرای جاوا اسکریپت به صورت محلی به طور فزاینده‌ای ضروری شده است، زیرا سایت‌های بسیاری برای بارگذاری داده‌های واقعی خود از جاوااسکریپت استفاده می‌کنند. فرایند اجرای جاوا اسکریپت برای تولید خروجی نهایی و کامل HTML را رندر (rendering) می‌نامند.

برای رندر کردن، از یک پروژه‌ جالب به نام Splash استفاده می‌کنیم، که خود را به عنوان "سرویس رندر جاوا اسکریپت" توصیف می‌کند. این پروژه می‌تواند در یک کانتینتر داکر اجرا شود و یک API برای رندر کردن سایت‌های دیگر ارائه می‌دهد. در داخل، از یک موتور WebKit(با قابلیت جاوا اسکریپت) برای بارگیری و رندر کامل وبسایت استفاده می‌شود. این همان چیزی است که ما برای به دست آوردن داده‌های وبسایت استفاده خواهیم کرد. سرور aiohttp ما، که در مثال 14-4 نشان داده شده است، API مربوط به Splash را فراخوانی می‌کند تا داده‌های صفحه را به دست آورد.

> برای ایجاد و اجرای کانتینر Splash، دستورات زیر را در shell اجرا کنید:
>
> ```bash
> $ docker pull scrapinghub/splash
> $ docker run --rm -p 8050:8050 scrapinghub/splash\
> ```
>
> سرور بکند ما Splash API را در http://localhost:8050 فراخوانی خواهد کرد.

**_مثال 14-4. کد مربوط به news scraper_**

```python
from asyncio import gather, create_task
from string import Template
from aiohttp import web, ClientSession
from bs4 import BeautifulSoup

async def news(request):
    sites = [
        ('http://edition.cnn.com', cnn_articles),
        ('http://www.aljazeera.com', aljazeera_articles),
    ]
    tasks = [create_task(news_fetch(*s)) for s in sites]
    await gather(*tasks)

    items = {
        text: (
            f'<div class="box {kind}">'
            f'<span>'
            f'<a href="{href}">{text}</a>'
            f'</span>'
            f'</div>'
        )
        for task in tasks for href, text, kind in task.result()
    }
    content = ''.join(items[x] for x in sorted(items))

    page = Template(open('index.html').read())
    return web.Response(
        body=page.safe_substitute(body=content),
        content_type='text/html',
    )

async def news_fetch(url, postprocess):
    proxy_url = (
        f'http://localhost:8050/render.html?'
        f'url={url}&timeout=60&wait=1'
    )
    async with ClientSession() as session:
        async with session.get(proxy_url) as resp:
            data = await resp.read()
            data = data.decode('utf-8')
    return postprocess(url, data)

def cnn_articles(url, page_data):
    soup = BeautifulSoup(page_data, 'lxml')
    def match(tag):
        return (
            tag.text and tag.has_attr('href')
            and tag['href'].startswith('/')
            and tag['href'].endswith('.html')
            and tag.find(class_='cd__headline-text')
        )
    headlines = soup.find_all(match)
    return [
        (url + hl['href'], hl.text, 'cnn')
        for hl in headlines
    ]

def aljazeera_articles(url, page_data):
    soup = BeautifulSoup(page_data, 'lxml')
    def match(tag):
        return (
            tag.text and tag.has_attr('href')
            and tag['href'].startswith('/news')
            and tag['href'].endswith('.html')
        )
    headlines = soup.find_all(match)
    return [
        (url + hl['href'], hl. text, 'aljazeera')
        for hl in headlines
    ]

app = web.Application()
app.router.add_get('/news', news)
web.run_app(app, port=8080)
```

۱. تابع `()news` یک handler برای آدرس news/ بر روی سرور ما است. این تابع یک صفحه HTML شامل تمام تیترهای خبری را بازمی‌گرداند.

۲. ما در اینجا تنها 2 وبسایت خبری را برای استخراج داده داریم: CNN و Al Jazeera. وبسایت‌های بیش‌تری را نیز می‌توانیم اضافه کنیم، اما در این صورت باید پس‌پردازش‌های دیگری را نیز اضافه کنیم، درست مانند تابع‌های `()cnn_articles` و `()aljazeera_articles` که برای استخراج تیترهای خبری نوشته شده‌اند.

۳. برای هر سایت خبری، یک تسک برای دریافت و پردازش داده‌های صفحه HTML برای صفحه اول آن ایجاد می‌کنیم. توجه داشته باشید که ما تاپل ((s\*)) را باز می‌کنیم، زیرا تابع کوروتین `()news_fetch` هم URL و هم تابع پس‌پردازش را به عنوان پارامترهای ورودی دریافت می‌کند. هر فراخوانی `()news_fetch` یک لیست تاپل از نتایج تیترهای خبری را در قالب `<article URL>` , `<article title>` باز می‌گرداند.

۴. تمام تسک‌ها باهم در یک Future جمع می‌شوند (`()gather` یک future که نشان‌دهنده‌ی وضعیت تمام تسک‌های جمع‌اوری شده است را بازمی‌گرداند)، و سپس بلافاصله برای کامل شدن future از await استفاده می‌کنیم. این خط تا زمانی که future کامل شود متوقف خواهد شد.

۵. از آنجایی که اکنون تمام تسک‌های `()news_fetch` کامل شده‌اند، تمام نتایج به دست آمده را در یک دیکشنری ذخیره می کنیم. توجه داشته باشید که چگونه nested comprehensions برای حلقه زدن بر روی تسک‌ها و همچنین لیست تاپل‌هایی که هر تسک بازمی‌گرداند استفاده می‌شود. علاوه بر این از f-stringها نیز برای جایگزینی مستقیم داده‌ها استفاده می‌کنیم، که حتی شامل نوع صفحه نیز می‌شود. نوع صفحه در CSS برای تغییر رنگ پس‌زمینه‌ی div استفاده می‌شود.

۶. در این دیکشنری، کلید همان تیتر خبری، و مقدار یک رشته‌ی HTML برای یک div است که در صفحه نتایج ما نشان داده می‌شود.

۷. وب سرور ما قرار است HTML بازگرداند. ما داده‌های HTML را از یک فایل لوکال با نام index.html بارگذاری می‌کنیم. این فایل در **مثال B-1** نشان داده شده است که در صورت تمایل می‌توانید از آن برای بازسازی این موردپژوهی استفاده کنید.

۸. تیترهای خبری جمع‌آوری شده را در قالب جایگزین کرده و صفحه را به مرورگر کلاینت بازمی‌گردانیم. این کار صفحه‌ای که در **شکل 1-4** نشان داده شده است را تولید می‌کند.

۹. در اینجا، در داخل تابع کوروتین `()news_fetch`، یک قالب کوچک برای استفاده از Splash API داریم (که برای من داخل یک کانتینر داکر لوکال بر روی پورت 8050 اجرا می‌شود). این نشان‌ می‌دهد که aiohttp چگونه می‌تواند به عنوان کلاینت HTTP مورد استفاده قرار گیرد.

۱۰. روش استاندارد ساخت یک instance از `()ClientSession`، و سپس استفاده از متد `()get` بر روی session instance برای اجرای فراخوانی REST است. در خط بعدی، داده‌های پاسخ دریافت می‌شوند. توجه داشته باشید که به خاطر آن که همیشه با async with و await با کوروتین‌ها کار می‌کنیم، این کوروتین هرگز مسدود نخواهد شد: ما قادر خواهیم بود که به هزاران درخواست از این نوع پاسخ دهیم، اگرچه این عملیات به خاطر فراخوانی وب به صورت درونی (`()new_fetch`) نسبتا کند باشد.

۱۱. پس از آنکه داده دریافت شد، تابع پس‌پردازش را فراخوانی می‌کنیم. برای CNN،‌ این تابع همان `()cnn_articles` و برای Al Jazeera همان `()aljazeera_articles` خواهد بود.

۱۲. ما برای بررسی فرایند پس‌پردازش فرصت کمی داریم. پس از دریافت داده‌های صفحه، از کتابخانه‌ی Beautiful Soup 4 جهت استخراج تیترهای خبری استفاده می‌کنیم.

۱۳. تابع `()match` تمام تگ‌های مشابه را بازمی‌گرداند (من به طور دستی منبع HTML این وبسایت‌های خبری را بررسی کرده‌ام تا بفهمم کدام ترکیب از فیلترها بهترین تگ‌ها را استخراج خواهد کرد)، و سپس لیستی از تاپل‌ها را به شکل `<article URL>`, `<article title>` بازمی‌گردانیم.

۱۴. این پس‌پردازش‌کننده مشابه پس‌پردازش‌کننده Al Jazeera است. شرط `()match` کمی متفاوت است، اما در مجموع مشابه پردازش‌کننده‌ی CNN است.

به طور کلی متوجه خواهید شد که aiohttp از API ساده‌تری برخوردار است و در حین توسعه برنامه‌هایتان، مزاحم شما نمی‌شود.

در بخش بعدی، به استفاده از ZeroMQ با asyncio نگاهی خواهیم داشت، که اثر عجیبی داشته و موجب لذت‌بخش‌تر شدن برنامه‌نویسی با سوکت می‌شود.

## ØMQ (ZeroMQ)

> برنامه‌نویسی علمی است که در قالب هنر ظاهر می‌شود، زیرا بسیاری از ما اساس کار نرم‌افزار را درک نمی‌کنیم، و این علم به ندرت آموزش داده می‌شود. اساس کار نرم‌افزار الگوریتم‌ها، ساختار داده‌ها، زبان‌ها، و انتزاعات نیستند. این‌ها تنها ابزارهایی هستند که ما آن‌ها را می‌سازیم، استفاده می‌کنیم، و در انتها دور می‌اندازیم. اساس کار واقعی نرم‌افزار اساس کار انسان‌ها است. در واقع، این مربوط به محدودیت‌های ما در مواجهه با پیچیدگی، و تمایلات ما برای همکاری جهت حل مشکلات بزرگ‌تر در قطعات کوچک است. این همان علم برنامه‌نویسی است: ایجاد قطعات کاربردی کوچک که برای دیگران ساده و قابل فهم باشند، تا افراد بتوانند با همکاری یکدیگر بزرگ‌ترین مشکلات را حل کنند.
> --**Pieter Hintjens, ZeroMQ: Messaging for Many Applications**

کتابخانه‌ی ØMQ (یا ZeroMq) یک کتابخانه‌ی محبوب غیروابسته به زبان برای برنامه‌های شبکه است که سوکت‌های "هوشمند" را ارائه می‌دهد. زمانی که در برنامه سوکت‌های ØMQ را ایجاد می‌کنید، شبیه سوکت‌های معمولی با نام‌‌های قابل تشخیص برای متدها مانند `()resv` و `()send` و... هستند. اما این سوکت‌ها به صورت داخلی برخی کارهای آزاردهنده‌تر و خسته‌کننده‌تر مورد نیاز برای کار با سوکت‌های معمولی را انجام می‌دهند.

یکی از قابلیت‌هایی که این کتابخانه ارائه می دهد مدیریت ارسال پیام است. بدین ترتیب لازم نیست پروتکل خود را اختراع کنید و بایت‌ها را روی رشته بشمارید تا بفهمید چه زمانی تمام بایت‌های یک پیام خاص رسیده‌اند. شما به سادگی هر آنچه را که به عنوان یک "پیام" در نظر دارید را ارسال می‌کنید و پیام شما کاملا سالم و دست‌نخورده در سمت دیگر دریافت می‌شود.

یکی دیگر از ویژگی‌های عالی این کتابخانه منطق اتصال مجدد به صورت خودکار است. اگر سرور از کار بیفتد و بعدا دوباره راه‌اندازی شود، کلاینت سوکت ØMQ به طور خودکار به سرور متصل خواهد شد. و حتی بهتر، پیام‌هایی که کد شما به سوکت ارسال می‌کند در زمان قطع ارتباط بافر می‌شوند، بدین ترتیب زمانی که سرور دوباره متصل می‌شود تمام این پیام‌ها ارسال خواهند شد. این‌ قابلیت‌ها تنها چند دلیل برای آن است که ØMQ به عنوان پیام‌رسانی بدون واسط شناخته می‌شود: این کتابخانه برخی از قابلیت‌های سیستم‌های واسط پیام را به طور مستقیم در شئ‌های سوکت ارائه می‌دهد.

سوکت‌های ØMQ به صورت داخلی به شکل ناهمزمان پیاده‌سازی شده‌اند (تا بتوانند بیش از هزاران اتصال همزمان را حتی در کدهای چندرشته‌ای حفظ کنند)، اما این قابلیت در پشت ØMQ API از ما پنهان است. با این وجود، پشتیبانی از Asyncio به PyZMQ Python bindings برای کتابخانه ØMQ اضافه شده است، و در این بخش، قرار است با چندین مثال نحوه‌ی استفاده از این سوکت‌های هوشمند در برنامه‌های پایتونی را بررسی کنیم.

### موردپژوهی: چندین سوکت

در اینجا سوالی وجود دارد: اگر ØMQ سوکت‌هایی را ارائه می‌دهد که ناهمزمان بوده و می‌توانند با رشته‌ها استفاده شوند، پس فایده‌ی استفاده از ØMQ با asyncio چیست؟ پاسخ به این سوال کد تمیزتر است.

برای نشان دادن این موضوع، بیاید به یک موردپژوهی مختصر نگاهی بیندازیم که در آن از چندین سوکت ØMQ در یک اپلیکیشن استفاده می‌شود. ابتدا، **مثال 15-4** نسخه‌ی مسدودکننده را نشان می‌دهد (این مثال از **zguide** گرفته شده است، راهنمای رسمی ØMQ)

**_مثال 15-4. رویکرد سنتی ØMQ_**

```python
# poller.py
import zmq

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt_string(zmq.SUBSCRIBE, '')

poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(subscriber, zmq.POLLIN)

while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if receiver in socks:
        message = receiver.recv_json()
        print(f'Via PULL: {message}')

    if subscriber in socks:
        message = subscriber.recv_json()
        print(f'Via SUB: {message}')
```

۱. سوکت‌های ØMQ انواع مختلفی دارند. این یک سوکت PULL است. می‌توانید به آن به چشم یک سوکت recieve-only نگاه کنید که توسط دیگر سوکت‌های send-only که PUSH نام دارند تغذیه می‌شوند.

۲. سوکت SUB از دیگر انواع سوکت recieve-only است، که توسط یک سوکت PUB که از نوع send-only است تغذیه می‌شود.

۳. اگر نیاز به جابجایی داده میان چندین سوکت در یک برنامه‌ی ØMQ چندرشته‌ای دارید، به یک poller نیاز خواهید داشت. زیرا این سوکت‌ها از نظر رشته‌ای ایمن نیستند، به همین دلیل هم نمی‌توانید بر روی سوکت‌های مختلف در رشته‌های مختلف ()recv را اجرا کنید.[^1]

۴. این بخش مشابه با سیستم فراخوانی ()select است. زمانی که داده‌های آماده‌ی دریافت در یکی از سوکت‌های ثبت شده وجود داشته باشد poller از حالت انسداد خارج می‌شود، و سپس این شما هستید که باید داده‌ها را بردارید و با آن‌ها کاری انجام دهید. بلوک بزرگ if روشی است که با استفاده از آن می‌توانید سوکت صحیح را تشخیص دهید.

استفاده از یک حلقه‌ی poller به همراه یک بلوک برای انتخاب صحیح سوکت باعث می‌شود که کد کمی گنگ به نظر رسد، اما این رویکرد تضمین می‌کند که یک سوکت یکسان در چندین رشته‌ی متفاوت مورد استفاده قرار نخواهد گرفت، و بدین ترتیب از مشکلات مربوط به thread-safety جلوگیری می‌کند.

**مثال 16-4** کد سرور را نشان می‌دهد.

**_مثال 16-4. کد سرور_**

```python
# poller_srv.py
import zmq, itertools, time

context = zmq.Context()
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://*:5557")

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

for i in itertools.count():
    time.sleep(1)
    pusher.send_json(i)
    publisher.send_json(i)
```

این کد برای بحث ما اهمیتی ندارد، اما به طور خلاصه: همانطور که پیش‌تر گفتم یک سوکت PUSH و یک سوکت PUB وجود دارند، و یک حلقه که داخل آن در هر ثانیه داده به هر دو سوکت ارسال می‌شود. این یک نمونه خروجی از poller.py است (نکته: هر دو برنامه باید در حال اجرا باشند):

```bash
$ poller.py
Via PULL: 0
Via SUB: 0
Via PULL: 1
Via SUB: 1
Via PULL: 2
Via SUB: 2
Via PULL: 3
Via SUB: 3
```

برنامه کار می‌کند؛ با این وجود، در اینجا صرفا اجرای برنامه برای ما اهمیتی ندارد، آنچه برای ما مهم است این است که آیا asyncio چیز بیش‌تری برای ساختار `poller.py` ارائه می‌دهد. نکته مهمی که باید متوجه آن باشیم آن است که کد asyncio ما قرار است در یک رشته اجرا شود، این بدان معناست که کار کردن سوکت‌های مختلف در کوروتین‌های مختلف خوب است-و در واقع این همان کاری است که انجام خواهیم داد.

البته، **کسی باید کار سخت را انجام می‌داد** تا پشتیبانی از کوروتین‌ها را به pyzmq (کتابخانه‌ی کلاینت پایتون برای ØMQ) اضافه کند تا این روش کار کند، بنابراین این کار رایگان نبود. اما ما می‌توانیم از آن بهره ببریم تا ساختار کد "سنتی" خود را بهبود دهیم، همانطور که در **مثال 17-4** نشان داده شده است.

**_مثال 17-4. جداسازی تمیز با asyncio_**

```python
# poller_aio.py
import asyncio
import zmq
from zmq.asyncio import Context

context = Context()

async def do_receiver():
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    while message := await receiver.recv_json():
        print(f'Via PULL: {message}')

async def do_subscriber():
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
    while message := await subscriber.recv_json():
        print(f'Via SUB: {message}')

async def main():
    await asyncio.gather(
        do_receiver(),
        do_subscriber(),
    )

asyncio.run(main())
```

۱. این نمونه کد مانند مثال 15-4 عمل می‌کند، با این تفاوت که در اینجا ما از کوروتین‌ها برای بازسازی همه چیز استفاده می‌کنیم. حال می‌توانیم با هر سوکت به صورت مجزا کار کنیم. من دو تابع کوروتین ایجاد کرده‌ام، یکی برای هر سوکت؛ این یکی برای سوکت PULL است.

۲. من از پشتیبانی asyncio در pymzq استفاده می‌کنم، این بدان معناست که تمام فراخوانی‌های ()send و ()recv باید از کلیدواژه‌ی await استفاده کنند. Poller دیگر در هیچ کجا ظاهر نمی‌شود، زیرا در خود حلقه‌ی رویداد asyncio ادغام شده است.

۳. این بخش همان handler برای سوکت SUB است. ساختار این بخش بسیار مشابه با handler سوکت PULL است، اما این مسئله اهمیتی ندارد. اگر منطق پیچیده‌تری مورد نیاز بود، می‌توانستم آن را به راحتی به اینجا اضافه کنم، به شکلی که کاملا درون کد SUB-handler کپسوله شود.

۴. دوباره، سوکت‌های سازگار با asyncio برای ارسال و دریافت به کلمه کلیدی await نیاز دارند.

خروجی دقیقا مانند قبل است، پس دوباره آن را نشان نمی‌دهم.

به نظر من استفاده از کوروتین‌ها تاثیر مثبت خیره‌کننده‌ای بر طرح کد در این مثال‌ها دارد. در کدهای واقعی محیط توسعه با تعداد زیادی سوکت ØMQ، توابع handler کوروتین‌ها برای هرکدام می‌توانند در فایل‌های جداگانه نیز باشند و فرصت‌های بیش‌تری برای ساختار بهتر کد ارائه دهند. حتی برای برنامه‌هایی با تنها یک سوکتِ خواندن/نوشتن،‌ در صورت نیاز استفاده از کوروتین‌های مجزا برای خواندن و نوشتن بسیار راحت است.

کد بهبودیافته شباهت زیادی با کد چندرشته‌ای دارد، و در حقیقت، برای مثال خاصی که در اینجا نشان داده شده است، همان کد برای threading هم کار خواهد کرد: توابع مسدودکننده‌ی ()do_receiver و ()do_subscriber را در رشته‌های مجزا اجرا کنید. اما آیا واقعا می‌خواهید حتی با پتانسیل پیش آمدن race conditions دست و پنجه نرم کنید؟به خصوص زمانی که برنامه‌تان از نظر پیچیدگی زمانی و قابلیت‌ها به مرور زمان رشد کند.

در اینجا مطالب زیادی برای کاوش وجود دارند، و همانطور که پیش‌تر گفتم، کار با این سوکت‌های جادویی بسیار لذت‌بخش است. در موردپژوهی بعدی، به استفاده‌ای عملی‌تر از ØMQ نگاه خواهیم کرد.

### موردپژوهی: نظارت بر عملکرد برنامه

با روش‌های مدرن، کانتینری، و مبتنی بر میکروسرویس‌ها که امروزه در توسعه برنامه‌ها مورد استفاده قرار می‌گیرند، برخی از چیزهایی که در گذشته بی‌اهمیت بودند، مانند نظارت بر میزان مصرف CPU و حافظه، بسیار پیچیده‌تر شده‌اند. در چند سال اخیر چندین محصول تجاری برای مقابله با این مشکلات به بازار عرضه شده‌اند، اما هزینه استفاده از آن‌ها می‌تواند برای تیم‌های کوچک استارتاپی و علاقمندان بسیار زیاد باشد.

در این موردپژوهی، من از ØMQ و asyncio برای ساخت یک نمونه‌ی اولیه برای نظارت بر برنامه‌های توزیع شده استفاده خواهم کرد. طراحی ما 3 قسمت دارد:

لایه Application

- این لایه شامل تمام برنامه‌های ما می‌شود. به عنوان مثال می‌توان به یک میکروسرویس "کلاینت‌ها"، یک میکروسرویس "رزروها"، یک میکروسرویس "ایمیل" و... اشاره داشت. من به هر یک از برنامه‌هایمان یک سوکت "انتقال" ØMQ اضافه خواهم کرد. این سوکت معیارهای عملکرد را به یک سرور مرکزی ارسال خواهد کرد.

لایه Collection

- سرور مرکزی یک سوکت ØMQ را برای جمع‌آوری داده از تمام برنامه‌های در حال اجرا ارائه می‌دهد. علاوه بر این سرور یک صفحه وب نیز برای نشان دادن گراف‌های عملکرد در طول زمان ارائه خواهد داد و داده‌های ورودی را به صورت زنده نیز نمایش می‌دهد.

لایه Visualization

- این لایه همان صفحه وب است که نمایش داده می‌شود. ما داده‌های جمع‌آوری شده را در مجموعه‌ای از نمودارها نشان خواهیم داد، و این نمودارها به صورت لحظه‌ای به روز می‌شوند. برای ساده‌‌سازی نمونه های کد، من از کتابخانه‌ی جاوااسکریپتی Smothie Charts استفاده خواهم کرد؛ این کتابخانه تمام ویژگی‌های مورد نیاز سمت کلاینت را فراهم می‌کند.

برنامه‌ی بکند (لایه application) که معیارها را تولید می‌کند در مثال 18-4 نشان داده شده است.

**_مثال 18-4. لایه application: تولید معیارها_**

```python
import argparse
import asyncio
from random import randint, uniform
from datetime import datetime as dt
from datetime import timezone as tz
from contextlib import suppress
import zmq, zmq.asyncio, psutil

ctx = zmq.asyncio.Context()

async def stats_reporter(color: str):
    p = psutil.Process()
    sock = ctx.socket(zmq.PUB)
    sock.setsockopt(zmq.LINGER, 1)
    sock.connect('tcp://localhost:5555')
    with suppress(asyncio.CancelledError):
        while True:
            await sock.send_json(dict(
                color=color,
                timestamp=dt.now(tz=tz.utc).isoformat(),
                cpu=p.cpu_percent(),
                mem=p.memory_full_info().rss / 1024 / 1024
            ))
            await asyncio.sleep(1)
    sock.close()

async def main(args):
    asyncio.create_task(stats_reporter(args.color))
    leak = []
    with suppress(asyncio.CancelledError):
        while True:
            sum(range(randint(1_000, 10_000_000)))
            await asyncio.sleep(uniform(0, 1))
            leak += [0] * args.leak

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', type=str)
    parser.add_argument('--leak', type=int, default=0)
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print('Leaving...')
        ctx.term()
```

۱. این تابع کوروتین به عنوان یک کوروتین طولانی‌مدت اجرا می‌شود و طور مداوم داده‌ها را به سرور ارسال می‌کند.

۲. یک سوکت ØMQ بسازید. همانطور که می‌دانید، انواع مختلفی از سوکت‌ها وجود دارند؛ این سوکت از نوع PUB است، که اجازه می‌دهد پیام‌های یک‌طرفه به یک سوکت ØMQ دیگر ارسال شوند. این سوکت همانطور که در راهنمای ØMQ به آن اشاره شده است قدرت‌های فوق‌العاده‌ای دارد و به صورت خودکار تمام اتصالات مجدد و منطق بافر را برای ما مدیریت خواهد کرد.

۳. به سرور متصل شوید.

۴. توالی خاموشی ما در خطوط بعدیِ برنامه توسط KeyboardInterrupt هدایت می‌شود. زمانی که سیگنال دریافت می‌شود، تمام تسک‌ها لغو می‌شوند. در اینجا من از `()supress` که یک context manager از ماژول کتابخانه‌ی استاندارد `        contextlib` است برای کنترل خطای `CancelledError` استفاده می‌کنم.

۵. ارسال داده‌ها به سرور تا ابد تکرار می‌شود.

۶. از آنجایی که ØMQ می‌داند چگونه با پیام‌های کامل، و نه فقط تکه‌هایی از بایت‌استریم، کار کند، دری به سمت استفاده از wrapperهایی مفید برای `()socket.send` گشوده می‌شود: در اینجا، از یکی از آن توابع کمک‌کننده به نام `()send_json` کار می‌کنم، که به طور اتوماتیک آرگومان ورودی را به JSON تبدیل می‌کند. استفاده از این تابع به ما اجازه می‌دهد که مستقیما از `()dict` استفاده کنیم.

۷. یکی از روش های مطمئن برای انتقال اطلاعات مربوط به زمان، استفاده از فرمت ISO 8601 است. استفاده از این روش به ویژه برای انتقال داده‌های زمانی میان نرم‌افزارهایی که به زبان‌های متفاوت نوشته شده‌اند توصیه می‌شود، زیرا اغلب پیاده‌سازی‌ها قادر به کار با این استاندارد هستند.

۸. برای اینکه به این نقطه برسیم باید خطای `CancelledError` که ناشی از لغو شدن تسک است را دریافت کرده باشیم. برای آنکه برنامه خاموش شود، سوکت ØMQ باید بسته باشد.

۹. تابع `()main` برنامه میکروسرویس واقعی را نشان می دهد. با این sum که بر روی اعداد تصادفی اجرا می‌شود داده‌های غیرواقعی تولید می‌شوند، فقط برای آنکه به ما داده‌‌های غیرصفر داده شود تا بتوانیم آن‌ها را کمی بعد در لایه‌ی visualization مشاهده کنیم.

۱۰. من چندین instance از این برنامه خواهم ساخت تا بتوانیم (بعدا، در بخش نمودارها) آن‌ها را با یک پارامتر `color--` متمایز کنیم.

۱۱. بالاخره، ØMQ context را می‌توان خاتمه داد.

نکته‌ی اصلی مورد توجه تابع `()stats_reporter` است. این همان چیزی است داده های متریک را (که توسط کتابخانه‌ی مفید psutil جمع‌آوری شده‌اند) پخش می‌کند. باقی کد را می‌توان یک برنامه‌ی میکروسرویس معمولی فرض کرد.

برنامه‌ی سرور در مثال 19-4 تمام داده‌ها را دریافت کرده و آن‌ها به کلاینت وب ارسال می‌کند.

**_مثال 19-4. لایه collection: این سرور آمار پروسه را جمع‌آوری می‌کند_**

```python
# metric-server.py
import asyncio
from contextlib
import suppress
import zmq
import zmq.asyncio
import aiohttp
from aiohttp import web
from aiohttp_sse import sse_response
from weakref import WeakSet
import json

# zmq.asyncio.install()
ctx = zmq.asyncio.Context()
connections = WeakSet()

async def collector():
    sock = ctx.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    sock.bind('tcp://*:5555')
    with suppress(asyncio.CancelledError):
        while data := await sock.recv_json():
            print(data)
            for q in connections:
                await q.put(data)
    sock.close()

async def feed(request):
    queue = asyncio.Queue()
    connections.add(queue)
    with suppress(asyncio.CancelledError):
        async with sse_response(request) as resp:
            while data := await queue.get():
                print('sending data:', data)
                resp.send(json.dumps(data))
    return resp

async def index(request):
    return aiohttp.web.FileResponse('./charts.html')

async def start_collector(app):
    app['collector'] = app.loop.create_task(collector())

async def stop_collector(app):
    print('Stopping collector...')
    app['collector'].cancel()
    await app['collector']
    ctx.term()

if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/feed', feed)
    app.on_startup.append(start_collector)
    app.on_cleanup.append(stop_collector)
    web.run_app(app, host='127.0.0.1', port=8088)
```

۱. نیمی از این برنامه داده‌ها را از دیگر اپلیکیشن‌ها دریافت می‌کند، و نیمی دیگر از آن داده‌ها را توسط server-sent events (SSEs) به مرورگر کلاینت ارسال می‌کند. من برای پیگیری کلاینت‌هایی که در حال حاضر متصل هستند از `()WeakSet` استفاده می‌کنم. هر یک از کلاینت‌های متصل یک instance از `()Queue` را خواهند داشت، بدین ترتیب این شناسه از اتصالات در واقع مجموعه‌ای از صف‌ها است.

۲. همانطور که به خاطر دارید در لایه‌ی application از سوکت `zmq`.PUB استفاده کردم. در اینجا نیز در لایه‌ی collection، من از شریک آن سوکت، یعنی سوکت `zmq`.SUB استفاده کردم. این سوکت ØMQ تنها می‌تواند داده‌ها را دریافت کند و قابلیت ارسال ندارد.

۳. برای سوکت `zmq`.SUB،‌ ارائه یک نام برای اشتراک لازم است؛ اما برای اهداف ما، ما فقط هر چیزی که وارد می‌شود را دریافت می‌کنیم، از این رو نام اشتراک خالی است.

۴. من سوکت `zmq`.SUB را متصل می‌کنم. یک لحظه به آن فکر کنید. در تنظیمات pub-sub، معمولا باید pub را به سرور تبدیل کنید (`()bind`) و sub را نیز به کلاینت تبدیل کنید(()connect). در ØMQ این مورد متفاوت است: هر دو طرف می‌توانند سرور باشند. برای مورد استفاده ما این مسئله اهمیت دارد، زیرا هر یک از instanceهای لایه application به یک مجموعه نام دامنه سرور یکسان متصل می‌شوند، و نه بالعکس.

۵. پشتیبانی از asyncio در `pyzmq` به ما اجازه می‌دهد از await برای دریافت داده از برنامه‌های متصل استفاده کنیم. علاوه بر این داده‌های دریافتی به طور خودکار از JSON به `()dict` تبدیل می‌شوند.

۶. به خاطر داشته باشید که مجموعه اتصالات ما برای هر کلاینت متصل یک صف نگه می‌دارد. حال که داده‌ها دریافت شده‌اند، زمان آن رسیده است که آن‌ها را به تمام کلاینت‌ها ارسال کنیم: داده در هر صف جایگذاری می‌شود.

۷. تابع کوروتین `()feed` برای هر کلاینت متصل کوروتین‌هایی را ایجاد خواهد کرد. به طور داخلی، **رویدادهایی که از سمت سرور ارسال می‌شوند** برای ارسال داده‌ها به کلاینت‌های وب مورد استفاده قرار می‌گیرند.

۸. همانطور که پیش‌تر توضیح داده شد، هر کلاینت وب یک instance از صف برای خود خواهد داشت تا بدین ترتیب بتواند از کوروتین `()collector` داده دریافت کند. صف به مجموعه‌ی اتصالات اضافه می‌شود، اما چون مجموعه‌ی اتصالات یک مجموعه‌ی ضعیف است، زمانی که صف از محدوده خارج می‌شود، ورودی به طور خودکار از مجموعه اتصالات حذف می‌شود؛ به طور مثال زمانی که یک کلاینت وب ارتباط خود را از دست می‌دهد. Weakrefها برای ساده‌تر کردن این نوع وظایف بسیار عالی هستند.

۹. پکیج `aiohttp_see` یک context manager با نام `()sse_response` ارائه می‌دهد. بدین ترتیب ما محدوده‌ای داریم که می‌توانیم داخل آن داده‌ها را به کلاینت وب منتقل کنیم.

۱۰. به کلاینت وب متصل مانده و منتظر داده در صف مخصوص به این کلاینت می‌مانیم.

۱۱. هر چه داده (در داخل `()collector`) دریافت شود، بلافاصله به کلاینت وب متصل ارسال خواهد شد. توجه داشته باشید که در اینجا من دیکشنری داده‌ها را مجددا به JSON تبدیل می‌کنم. یک روش برای بهینه‌سازی این کد این است که از تبدیل داده‌ی JSON به دیکشنری در `()collector` دوری کرده و به جای آن از `()sock.recv_string` استفاده کنیم تا از رفت و برگشت برای تبدیل داده جلوگیری کنیم. البته که در یک سناریوی واقعی ممکن است بخواهید داده را در collector از JSON به دیکشنری تبدیل کرده و پیش از ارسال داده به مرورگر کلاینت کمی اعتبارسنجی روی آن انجام دهید. انتخاب‌های زیادی در این زمینه وجود دارند.

۱۲. در اندپوینت `()index` بارگذاری صفحه اصلی انجام می‌شود، و ما در اینجا یک فایل استاتیک با نام charts.html را ارائه می‌کنیم.

۱۳. کتابخانه `aiohttp` امکاناتی برای ما فراهم می‌کند تا بتوانیم برای کوروتین‌های بلندمدت که ممکن است به آن‌ها نیاز داشته باشیم hook اضافه کنیم. با کوروتین `()collector`، ما دقیقا همین شرایط را داریم، برای همین من یک کوروتین راه‌اندازی با نام `()start_collector` و یک کوروتین shutdown ایجاد می‌کنم. این کوروتین‌ها در طی مراحل خاصی از راه‌اندازی و خاموشی `aiohttp` فراخوانی می‌شوند. توجه داشته باشید که من تسک collector را به خود برنامه اضافه می‌کنم، که یک پروتکل mapping را پیاده‌سازی می‌کند تا بتوانید از ان به عنوان یک دیکشنری استفاده کنید.

۱۴. کوروتین `()collector` را از شناسه `app` دریافت می‌کنم و `()cancel` را برای آن فراخوانی می‌کنم.

۱۵. در نهایت، می‌توانید ببینید که کوروتین‌های راه‌اندازی و خاموشی که طراحی کردیم به کجا متصل هستند: نمونه `app` قلاب‌هایی (hook) را ارائه می‌دهد که کوروتین‌های سفارشی ما ممکن است به آن‌ها متصل شوند.

تمام چیزی که باقی مانده است لایه‌ی visualization است که در **مثال 20-4** نشان داده شده است. من از **Smoothie Charts library** برای تولید نمودارهایی که قابلیت پیمایش دارند استفاده می‌کنم، و HTML کامل برای صفحه وب اصلی ما که همان charts.html است در **مثال 1-B** ارائه شده است. HTML, CSS, و جاوا اسکریپت زیادی برای ارائه در این بخش وجود دارد، اما من می‌خواهم چندین نکته درباره چگونگی کار با رویدادهای دریافتی از سوی سرور در جاواسکریپت در مرورگر کلاینت صحبت کنم.

**_مثال 20-4. لایه‌ی visualization، که نامی زیبا برای "مرورگر" است_**

```javascript
<snip>
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
<snip>
```

۱. یک instance جدید از `()EventSource` بر روی لینک feed/ ایجاد کنید. مرورگر بر روی سرور ما به feed/ متصل می‌شود، (mertic_server.py). توجه داشته باشید که در صورتی که اتصال از بین برود مرورگر به طور خودکار برای اتصال مجدد تلاش خواهد کرد. رویدادهای ارسال شده از سوی سرور معمولا نادیده گرفته می‌شوند، اما در بسیاری از موقعیت‌ها سادگی‌ آن‌ها باعث می‌شود که به WebSockets ترجیح داده شوند.

۲. رویداد `onmessage` هر زمان که سرور داده‌ای ارسال کند فعال می‌شود. در اینجا داده به عنوان JSON تجزیه می‌شود.

۳. شناسه‌ی `cpu` یک نگاشت از یک رنگ به یک instance از `()TimeSeries` است (برای اطلاعات بیش‌تر در این زمینه، مثال B-1 را بررسی کنید). در اینجا، ما آن time series را به دست آورده و داده‌ها را به آن اضافه می‌کنیم. همچنین timestamp را نیز به دست آورده و آن را برای به دست آوردن فرمت صحیح مورد نیاز برای نمودار فرمت می‌کنیم.

حال می‌توانیم برنامه را اجرا کنیم. برای آنکه تمام برنامه‌ها را اجرا کنیم به چند دستور خط فرمان نیاز داریم، اولین دستور برای شروع پروسه‌ی جمع‌آوری داده است:

```bash
$ metric-server.py
======== Running on http://127.0.0.1:8088 ========
(Press CTRL+C to quit)
```

قدم بعدی اجرای تمام instanceهای میکروسرویس‌ها است. این برنامه‌ها متریک‌های cpu و حافظه خود را به collector ارسال می‌کنند. هر یک از این داده‌ها با رنگ متفاوتی مشخص می‌شود، که در خط فرمان تعریف شده است. توجه داشته باشید که چگونه به دو مورد از میکروسرویس‌ها گفته می‌شود که مقداری از حافظه را نشت کنند.

```bash
$ backend-app.py --color red &
$ backend-app.py --color blue --leak 10000 &
$ backend-app.py --color green --leak 100000 &
```

شکل 2-4 نتیجه نهایی را بر روی مرورگر نشان می‌دهد. باور کنید که نمودارها واقعا متحرک هستند. متوجه خواهید شد که در دستورات خط فرمان قبلی، کمی نشت حافظه به خط آبی، و مقدار بیش‌تری به خط سبز اضافه کرده‌ام. حتی برای اینکه جلوی پیشروی خط سبز به بیش از 100MB را بگیرم باید آن را چند بار ری‌استارت می‌کردم.

![شکل 2-4. بهتر است هر چه سریع‌تر برای خط سبز SRE دریافت کنیم.](images/uaip_0402.png)

شکل 2-4. بهتر است هر جه سریع‌تر برای خط سبز SRE دریافت کنیم.

چیزی که درباره این پروژه بسیار جالب است این است: هر یک از نمونه‌های در حال اجرا در هر بخشی از این برنامه را می‌توان ری‌استارت کرد، و برای آن به هیچ برنامه‌ای جهت مدیریت اتصال مجدد نیاز نخواهد بود. سوکت‌های ØMQ، به همراه نمونه‌‌ی جاوا اسکریپتی ()EventScore در مرورگر، به شکل خارق‌العاده‌ای مجددا متصل شده و کار را از جایی که رها شده بود ادامه می‌دهند.

در بخش بعدی، توجه خود را صرف دیتابیس‌ها کرده و به این موضوع می‌پردازیم که asyncio چگونه می‌تواند برای طراحی سیستم‌های cache invalidation مورد استفاده قرار گیرد.

## asyncpg و Sanic

کتابخانه asyncpg دسترسی کلاینت به دیتابیس PostgreSQL را فراهم می‌کند. اما این کتابخانه با تاکید بر سرعت، خود را از دیگر کتابخانه‌های سازگار با asyncio برای کار با Postgres متمایز می‌کند. کتابخانه‌ی asyncpg توسط Yury Selivanov، یکی از اصلی‌ترین توسعه‌دهندگان asyncio Python، و نویسنده پروژه‌ی uvloop نوشته شده است. این کتابخانه هیچ وابستگی‌ third-party ندارد، البته اگر آن را از منبع نصب می‌کنید، Cpython لازم است.

کتابخانه asyncpg به دلیل آن که مستقیما با پروتکل باینری PostgreSQL کار می‌کند سرعت بالایی دارد. از دیگر مزایای این رویکرد پشتیبانی از دستورات آماده و cursorهای قابل پیمایش است.

ما به یک موردپژوهی که در آن از asyncpg برای cache invalidation استفاده شده است نگاهی خواهیم انداخت. اما پیش از آن بهتر است به درک پایه‌ای از API ارائه شده توسط asyncpg برسیم. برای تمام کدهای این بخش، به یک نمونه‌ی در حال اجرا از PostgreSQL نیاز خواهیم داشت. این کار با استفاده از داکر و با دستور زیر به راحتی قابل انجام است:

```bash
$ docker run -d --rm -p 55432:5432 postgres
```

Note that I’ve exposed port 55432 rather than the default, 5432, just in case you already have a running instance of the database on the default port. Example 4-21 briefly demonstrates how to use asyncpg to talk to PostgreSQL.

توجه داشته باشید که من به جای پورت پیش‌فرض، 5432، پورت 55432 را مورد استفاده قرار داده‌ام، فقط به خاطر اینکه ممکن است یک نمونه در حال اجرای دیگر از این دیتابیس بر روی پورت پیش‌فرض آن داشته باشید. مثال 21-4 به طور خلاصه نحوه استفاده از asyncpg برای ارتباط با PostgreSQL را نشان می‌دهد.

**_مثال 21-4. نمونه‌ای ساده از asyncpg_**

```python
# asyncpg-basic.py
import asyncio
import asyncpg
import datetime
from util import Database

async def main():
    async with Database('test', owner=True) as conn:
        await demo(conn)

async def demo(conn: asyncpg.Connection):
    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name text,
            dob date
        )'''
    )
    pk = await conn.fetchval(
        'INSERT INTO users(name, dob) VALUES($1, $2) '
        'RETURNING id', 'Bob', datetime.date(1984, 3, 1)
    )

    async def get_row():
        return await conn.fetchrow(
            'SELECT * FROM users WHERE name = $1',
            'Bob'
            )
    print('After INSERT:', await get_row())

    await conn.execute(
        'UPDATE users SET dob = $1 WHERE id=1',
        datetime.date(1985, 3, 1)
        )
    print('After UPDATE:', await get_row())

    await conn.execute(
        'DELETE FROM users WHERE id=1'
        )
    print('After DELETE:', await get_row())

if __name__ == '__main__':
    asyncio.run(main())
```

۱. من برخی از کدهای تکراری را در یک module به نام کوچک util پنهان کرده‌ام تا همه چیز ساده‌تر شده و پیام اصلی نیز حفظ شود.

۲. کلاس `Database` یک context manager به ما می‌دهد که یک دیتابیس جدید برای ما خواهد ساخت (در این کد نام آن test است) و زمانی که context manager خارج شود دیتابیس را از بین خواهد برد. به نظر می‌رسد که این کار هنگام ازمایش ایده‌های مختلف در کد بسیار مفید است. به دلیل عدم انتقال وضعیت بین آزمایش‌ها، می‌توانید هربار از یک دیتابیس تمیز شروع کنید. توجه داشته باشید که این یک context manager از نوع async with است؛ در ادامه بیش‌تر درباره آن صحبت خواهیم کرد، اما فعلا، محل تمرکز این کد چیزی است که در کوروتین `()demo` اتفاق می‌افتد.

<p dir="rtl">۳.  <code>Datebase</code> یک instance از Connection به ما ارائه کرده است، که بلافاصله برای ساخت یک جدول جدید در دیتابیس با نام users استفاده می‌شود.</p>

۴. من برای اضافه کردن رکورد جدید در دیتابیس از `()fetchval` استفاده می‌کنم. البته می‌توانستم از `()execute` برای انجام این کار استفاده کنم، اما مزیت استفاده از `()fetchval` این است که می‌توانم id رکورد جدیدی که به جدول اضافه شده است را دریافت کرده و آن را در شناسه‌ی pk ذخیره کنم.

۵. در ادامه‌، قصد دارم داده‌ی موجود در جدول users را تغییر دهم، بنابراین در اینجا یک تابع کوروتین جدید می‌سازم که رکوردی را از دیتابیس را دریافت می‌کند. این تابع چندین بار فراخوانی خواهد شد.

۶. زمان دریافت داده‌ها، استفاده از توابع مبتنی بر `fetch` بسیار مفیدتر است، زیرا این توابع اشیاء از نوع `Record` را باز می‌گردانند. کتابخانه‌ی asyncpg به طور خودکار انواع داده‌ها را به مناسب‌ترین نوع برای پایتون تبدیل می‌کند.

۷. بلافاصله از تابع کمکی `()get_row` برای نمایش رکورد جدیدی که به جدول اضافه شده است استفاده می‌کنم.

۸. از دستور `UPDATE` در SQL برای تغییر داده‌ها استفاده می‌کنم. یک تغییر کوچک: مقدار year در تاریخ تولد به اندازه 1 سال تغییر می‌کند. همانند قبل، این کار با استفاده از تابع `()execute` انجام می‌شود.

**_خروجی حاصل از اجرای این قطعه کد به شکل زیر است:‌_**

```bash
$ asyncpg-basic.py
After INSERT: <Record id=1 name='Bob' dob=datetime.date(1984, 3, 1)>
After UPDATE: <Record id=1 name='Bob' dob=datetime.date(1985, 3, 1)>
After DELETE: None
```

توجه داشته باشید که چگونه مقدار date که در شئ Record بازیابی شده است به یک شئ تاریخ در پایتون تبدیل شده است: asyncpg نوع داده‌ها را به طور خودکار از نوع SQL به معادل آن‌ها در پایتون تبدیل کرده است. یک جدول بزرگ از تبدیل انواع داده‌ها در داکیومنت asyncpg تمام نگاشت‌هایی که برای نوع داده‌ها در این کتابخانه وجود دارند را توضیح می‌دهد.

کد قبلی بسیار ساده است، شاید حتی بتوان آن را یک کد خام دانست (اگر به راحتی‌ِ کار با object-relational-mappers (ORMs) مانند SQLAlchemy یا ORM داخلی فریمورک وب Django عادت داشته باشید). در انتهای این فصل، من به چندین کتابخانه شخص ثالث اشاره خواهم داشت که دسترسی به ORM یا ویژگی‌های مشابه ORM را برای asyncpg فراهم می‌کنند.

**مثال 22-4** شئ Database در ماژول utils را نشان می‌دهد؛ ممکن است ساخت چیزی مشابه برای آزمایش‌های خودتان برایتان مفید باشد.

**_مثال 22-4. ابزاری مفید برای آزمایش‌های asyncpg شما_**

```python
# util.py
import argparse, asyncio, asyncpg
from asyncpg.pool import Pool

DSN = 'postgresql://{user}@{host}:{port}'
DSN_DB = DSN + '/{name}'
CREATE_DB = 'CREATE DATABASE {name}'
DROP_DB = 'DROP DATABASE {name}'

class Database:
    def __init__(self, name, owner=False, **kwargs):
        self.params = dict(
            user='postgres',
            host='localhost',
            port=55432,
            name=name)
        self.params.update(kwargs)
        self.pool: Pool = None
        self.owner = owner
        self.listeners = []

    async def connect(self) -> Pool:
        if self.owner:
            await self.server_command(
                CREATE_DB.format(**self.params))

        self.pool = await asyncpg.create_pool(
            DSN_DB.format(**self.params))
        return self.pool

    async def disconnect(self):
        """Destroy the database"""
        if self.pool:
            releases = [
                self.pool.release(conn)
                for conn in self.listeners
            ]
            await asyncio.gather(*releases)
            await self.pool.close()

        if self.owner:
            await self.server_command(
                DROP_DB.format(**self.params))

    async def __aenter__(self) -> Pool:
        return await self.connect()

    async def __aexit__(self, *exc):
        await self.disconnect()

    async def server_command(self, cmd):
        conn = await asyncpg.connect(
            DSN.format(**self.params))
        await conn.execute(cmd)
        await conn.close()

    async def add_listener(self, channel, callback):
        conn: asyncpg.Connection = await self.pool.acquire()
        await conn.add_listener(channel, callback)
        self.listeners.append(conn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', choices=['create', 'drop'])
    parser.add_argument('--name', type=str)
    args = parser.parse_args()
    d = Database(args.name, owner=True)

    if args.cmd == 'create':
        asyncio.run(d.connect())
    elif args.cmd == 'drop':
        asyncio.run(d.disconnect())
    else:
        parser.print_help()
```

۱. کلاس Database فقط یک context manager برای ایجاد یا از بین بردن دیتابیس‌ها در یک instance از PostgreSQL است. نام دیتابیس به constructor داده می‌شود.

۲. (توجه: دنباله‌ی فراخوانی‌ها در این کد عمدا با این لیست متفاوت است.) این یک context manager همزمان است. به جای تابع‌های معمول `()__enter__` و `()__exit__`،‌ من از معادل‌های آن‌ها `()__aenter__` و `()__aexit__` استفاده می‌کنم.

۳. در اینجا،‌ در بخش ورودی،‌ من دیتابیس جدید را ساخته و یک connection به این دیتابیس را بازمی‌گردانم. `()server_command` یکی دیگر از توابع کمکی است که چند خط پایین‌تر تعریف شده است. من از این تابع برای اجرای دستور مربوط به ساخت دیتابیس جدید استفاده می‌کنم.

۴. سپس به دیتابیس جدید یک اتصال برقرار می‌کنم. توجه داشته باشید که من تعدادی از جزئیات درباره اتصال را به صورت ثابت در کد وارد کرده‌ام: این کار عمدی است، چون می‌خواستم نمونه کدها را کوچک نگه دارم. شما می‌توانید با ساخت فیلدهایی برای نام کاربری، نام سرور، و پورت این کار را به صورت کلی انجام دهید.

۵. در بخش هیجان‌انگیز context manager، من اتصال را می‌بندم و...

۶. ...دیتابیس را از بین می‌برم.

۷. برای کامل‌تر کردن،‌ این تابع کمکی ما برای اجرای دستورات مربوط به سرور PostgreSQL است. برای این منظور، یک اتصال ایجاد می‌کند، دستور مربوطه را اجرا کرده، و از اتصال خارج می‌شود.

۸. این تابع یک اتصال سوکت بلند مدت به دیتابیس ایجاد می‌کند که به رویداد‌ها گوش مي‌دهد. این مکانیزم در موردپژوهی آتی مورد استفاده قرار می‌گیرد.

> در نکته 8 برای کد قبلی، برای هر کانالی که قصد گوش دادن به آن را دارم یک اتصال مخصوص ایجاد کردم. این کار هزینه‌بر است، زیرا بدان معناست که یک PostgreSQL worker برای هر کانالی که به آن گوش داده می‌شود کاملا مشغول خواهد بود. یک طراحی بسیار بهتر استفاده از یک اتصال برای چندین کانال است. وقتی روی این مثال کار کردید، سعی کنید کد را به گونه‌ای تغییر دهید که از یک اتصال برای گوش دادن به چندین کانال استفاده کند.

حال که درکی از مباحث پایه‌ای asyncpg پیدا کرده‌اید، می‌توانیم با یک موردپژوهی جالب آن را بیش‌تر بررسی کنیم: استفاده از پشتیبانی داخلی PostgreSQL برای ارسال اعلان‌های رویدادها جهت انجام cache invalidation!

### موردپژوهی: Cache Invalidation

> در علوم کامپیوتر دو چیز مشکل وجود دارد: باطل کردن کَش (cache invalidation)، نامگذاری، و خطاهای off-by-one.  
> --Phil Karlton

در وب‌سرویس‌ها و برنامه‌های کاربردی وب رایج است که لایه‌ی persistence، یعنی همان دیتابیس پشتیبان (DB)، زودتر از هر بخش دیگری در ساختار موجب محدودیت عملکرد شود. لایه application معمولا با اجرای نمونه‌های بیش‌تر می‌تواند به صورت افقی وسعت پیدا کند، در حالی که انجام این کار با پایگاه داده پیچیده‌تر است.

به همین دلیل هم بررسی گزینه‌های طراحی که می‌توانند تعامل بیش از اندازه با دیتابیس را کاهش دهند رایج است. متداول‌ترین راه حل استفاده از سیستم کَش برای "به خاطر سپردن" نتایج پیشین دیتابیس است تا هنگام درخواست بعدی، از تکراری شدن تماس با دیتابیس برای دریافت همان اطلاعات جلوگیری شود.

با این وجود، چه اتفاقی خواهد افتاد اگر یک نمونه از برنامه‌هایتان داده جدیدی را در دیتابیس وارد کند، در حالی که نمونه‌ای دیگر همچنان داده‌های قدیمی را از کَش داخلی خود بازمی‌گرداند؟ این مسئله یکی از مشکلات کلاسیک باطل کردن کَش است، و حل کردن آن به روشی مناسب می‌تواند بسیار دشوار باشد.

استراتژی حمله ما به شرح زیر است:

۱. هر نمونه از برنامه یک کَش داخلی از کوئری‌های دیتابیس دارد.

۲. زمانی که داده جدیدی در دیتابیس نوشته می‌شود، دیتابیس به تمام نمونه‌های برنامه که متصل هستند هشدار می‌دهد.

۳. سپس هر نمونه برنامه کَش داخلی خود را متناسب با اطلاعات جدید به روز می‌کند.

این موردپژوهی نشان می‌دهد که PostgreSQL، چگونه با پشتیبانی داخلی از به روزرسانی‌های رویداد از طریق دستورات `LISTEN` و `NOTIFY`، می‌تواند به سادگی به ما اعلام کند که داده‌های آن تغییر کرده‌اند.

کتابخانه‌ی asyncpg در حال حاضر API مربوط به دستورات `LISTEN/NOTIFY` را پشتیبانی می‌کند. از ویژگی PostgreSQL به برنامه‌های شما اجازه می‌دهد که در رویدادهای یک کانال نامگذاری شده مشترک شده و رویدادها را در کانال‌های نامگذاری شده ارسال کند. از PostgreSQL می‌توانید به عنوان یک ورژن سبک‌تر از **RabbitMQ** و **ActiveMQ** استفاده کنید.

این موردپژوهی دارای بخش‌هایی است که بیان آن‌ها به شکل خطیِ معمول دشوار است. به جای این کار، با مشاهده نتیجه نهایی شروع کرده و به سمت پیاده‌سازی‌ اصلی پیش‌ می‌رویم.

برنامه ما یک API مبتنی بر JSON برای مدیریت غذاهای مورد علاقه کلاینت‌ها در رستوران روباتیک ارائه می‌دهد. دیتابیس پشتیبان تنها یک جدول با نام patrons با دو فیلد name و fav_dish خواهد داشت. API ما امکان استفاده از 4 عملیات معمول را خواهد داشت: create, read, update, و delete. (یا همان CRUD)

در ادامه یک تعامل ساده با این API را با استفاده از دستور curl مشاهده می‌کنید که نحوه ایجاد یک داده جدیدی در دیتابیس را نشان می‌دهد. (من هنوز نحوه راه‌اندازی سرور روی localhost:8000 را نشان نداده‌ام؛ در ادامه به آن خواهیم پرداخت)

```bash
$ curl -d '{"name": "Carol", "fav_dish": "SPAM Bruschetta"}' \
    -H "Content-Type: application/json" \
    -X POST \
    http://localhost:8000/patron
{"msg":"ok","id":37}
```

پارامتر `d-` برای داده است [^2]، ‍‍`H-` برای هدرهای HTTP، پارامتر X- برای متد ریکوئست HTTP (که به جای آن می‌توانید از `GET`، `DELETE`، `PUT` و چند مورد دیگر استفاده کنید) و URL برای سرور API است. به زودی به کد مربوط به آن نیز خواهیم رسید.

در خروجی، می‌توانیم مشاهده کنیم که ایجاد داده به خوبی پیش رفته است، و id به عنوان کلید اصلی رکورد جدیدی که در دیتابیس ساخته شده است بازمی‌گردد.

در قطعه‌ کدهای بعدی در shell، سه عملیات دیگر را بررسی خواهیم کرد: read, update, و delete. با استفاده از دستور زیر می‌توانیم رکوردی که در دیتابیس ایجاد کردیم را مشاهده کنیم:

```bash
$ curl -X GET http://localhost:8000/patron/37
{"id":37,"name":"Carol","fav_dish":"SPAM Bruschetta"}
```

خواندن داده از دیتابیس به سادگی انجام می‌شود. توجه داشته باشید که id مربوط به رکورد مورد نظر باید در URL قرار داده شود.

در ادامه، رکورد ایجاد شده را آپدیت کرده و نتیجه را بررسی می‌کنیم:

```bash
$ curl -d '{"name": "Eric", "fav_dish": "SPAM Bruschetta"}' \
    -H "Content-Type: application/json" \
    -X PUT \
    http://localhost:8000/patron/37
$ curl -X GET http://localhost:8000/patron/37
{"msg":"ok"}
{"id":37,"name":"Eric","fav_dish":"SPAM Bruschetta"}
```

آپدیت کردن یک رکورد مشابه با ساخت آن است، با دو تفاوت کلیدی:

- ریکوئست HTTP که با `X-` مشخص می‌شود `PUT` است، نه POST.
- برای مشخص کردن رکوردی که قصد آپدیت آن را دارید، باید فیلد id را در URL مشخص کنید.

در نهایت، می‌توانیم رکورد مورد نظر را حذف کرده و با دستورات زیر حذف آن را تایید کنیم:

```bash
$ curl -X DELETE http://localhost:8000/patron/37
$ curl -X GET http://localhost:8000/patron/37
{"msg":"ok"}
null
```

همانطور که مشاهده می‌کنید، زمانی که می‌خواهید رکوردی که وجود ندارد را با GET دریافت کنید، null برگردانده می‌شود.

تا اینجا همه چیز معمولی به نظر می‌رسد، اما هدف ما تنها ایجاد یک API برای CRUD نیست، بلکه می‌خواهیم که باطل کردن اعتبار کَش نیز بپردازیم. پس بهتر است توجه خود را به کَش معطوف کنیم. حال که درک مناسبی از API برنامه خود پیدا کرده‌ایم، می‌توانیم به لاگ‌های برنامه نگاهی بیندازیم تا داده‌های زمانبندی هر درخواست را ببینیم: با این کار می‌توانیم متوجه شویم که کدام درخواست‌ها کَش شده‌اند، و کدام یک از آن‌ها به دیتابیس درخواست می‌دهند.

زمانی که سرور برای اولین بار راه‌اندازی می‌شود، کَش خالی است: زیرا حافظه داخلی است. ما سرور خود را راه‌اندازی کرده و در یک shell جداگانه دو ریکوئست GET را پشت سر هم اجرا می‌کنیم:

```bash
$ curl -X GET http://localhost:8000/patron/29
$ curl -X GET http://localhost:8000/patron/29
{"id":29,"name":"John Cleese","fav_dish":"Gravy on Toast"}
{"id":29,"name":"John Cleese","fav_dish":"Gravy on Toast"}
```

انتظار داریم اولین باری که رکورد خود را بازیابی می‌کنیم، چیزی در کَش وجود نداشته باشد، و دومین بار داده در کَش موجود باشد. ما می‌توانیم شواهدی از این موضوع را در لاگ سرور API مشاهده کنیم (اولین وب سرور Sanic که در localhost:8000 اجرا می شود):

```bash
$ sanic_demo.py
2019-09-29 16:20:33 - (sanic)[DEBUG]:
```

![sonic](images/sonic.png)

```bash
2019-09-29 16:20:33 (sanic): Goin' Fast @ http://0.0.0.0:8000
2019-09-29 16:20:33 (sanic): Starting worker [10366]
2019-09-29 16:25:27 (perf): id=37 Cache miss
2019-09-29 16:25:27 (perf): get Elapsed: 4.26 ms
2019-09-29 16:25:27 (perf): get Elapsed: 0.04 ms
```

۱. همه چیز تا این خط پیام‌های لاگ پیش‌فرص برای راه‌اندازی sanic است.

۲. همانطور که توضیح داده شد، اولین نتایج برای GET در کَش موجود نیستند، زیرا سرور به تازگی راه‌اندازی شده است.

۳. این برای اولین curl -X GET است. من کمی قابلیت زمان‌بندی به اندپوینت‌های API اضافه کرده‌ام. در اینجا می‌توانیم مشاهده کنیم که اجرای تابع مربوط به ریکوئست GET تقریبا 4 میلی‌ثانیه طول می‌کشد.

۴. دومین ریکوئست GET داده‌ها را از کَش بازمی‌گرداند، داده‌های مربوط به زمانبندی آن نیز بسیار سریع‌تر است (100 برابر سریع‌تر!)

تا اینجا هیچ چیز غیرعادی وجود نداشت. بسیاری از برنامه‌های وب به همین شکل از کَش استفاده می‌کنند.

حال بیاید یک نمونه برنامه دیگر در پورت 8001 راه‌اندازی کنیم (اولین نمونه روی پورت 8000 بود):

```bash
$ sanic_demo.py --port 8001
<snip>
2017-10-02 08:09:56 - (sanic): Goin' Fast @ http://0.0.0.0:8001
2017-10-02 08:09:56 - (sanic): Starting worker [385]
```

البته که هر دو نمونه برنامه به یک دیتابیس متصل هستند. حال، با اجرای هر دو نمونه سرور API، داده‌های مربوط به کاربر John را تغییر می‌دهیم، که به وضوح فاقد Spam کافی در رژیم غذایی خود است. در اینجا عملیات UPDATE را در اولین نمونه برنامه در پورت 8000 اجرا می‌کنیم:

```bash
$ curl -d '{"name": "John Cleese", "fav_dish": "SPAM on toast"}' \
    -H "Content-Type: application/json" \
    -X PUT \
    http://localhost:8000/patron/29
{"msg":"ok"}
```

بلافاصله پس از این رویداد مربوط به آپدیت بر روی یکی از نمونه‌‌ها، هر دور سرور API، در پورت‌های 8000 و 8001، رویداد را در لاگ‌های مربوطه نشان می‌دهند.

```bash
2019-10-02 08:35:49 - (perf)[INFO]: Got DB event:
{
    "table": "patron",
    "id": 29,
    "type": "UPDATE",
    "data": {
        "old": {
            "id": 29,
            "name": "John Cleese",
            "fav_dish": "Gravy on Toast"
        },
        "new": {
            "id": 29,
            "name": "John Cleese",
            "fav_dish": "SPAM on toast"
        },
        "diff": {
            "fav_dish": "SPAM on toast"
        }
    }
}
```

دیتابیس رویداد مربوط به آپدیت را در هر دو instance از برنامه گزارش داده است. ما هنوز هیچ ریکوئستی به نمونه برنامه روی پورت 8001 ارسال نکرده‌ایم. آیا این بدان معناست که داده‌های جدید قبلا در کَش آن ذخیره شده‌اند؟

برای بررسی، می‌توانیم یک ریکوئست GET روی سرور دوم، به پورت 8001 ارسال کنیم:

```bash
$ curl -X GET http://localhost:8001/patron/29
{"id":29,"name":"John Cleese","fav_dish":"SPAM on toast"}
```

اطلاعات زمانبندی در لاگ خروجی نشان می‌دهند که داده‌ها را مستقیما از کَش دریافت کرده‌ایم، با این که این اولین ریکوئست ما است:

```bash
2019-10-02 08:46:45 - (perf)[INFO]: get Elapsed: 0.04 ms
```

نتیجه این است که زمانی که دیتابیس تغییر می‌کند،‌تمام instanceهایی که به آن وصل هستند به طور خودکار مطلع شده و کَش خود را آپدیت می‌کنند.

پس از توضیح این موضوع، حال می‌توانیم به پیاده‌سازی asyncpg که برای انجام cache invalidation لازم است نگاهی داشته باشیم. طراحی پایه برای کد سرور که در مثال 23-4 نشان داده شده است به شرح زیر است:

۱. با استفاده از وب فریمورک جدید Sanic که با asyncio سازگار است یک API ساده داریم.

۲. داده‌ها در یک instance از دیتابیس PostgreSQL ذخیره خواهند شد، اما API توسط چندین نمونه از سرورهای برنامه وب API ارائه می‌شود.

۳. سرورهای برنامه داده‌ها را از دیتابیس کَش می‌کنند.

۴. سرورهای برنامه توسط asyncpg در جداول مخصوصی بر روی در رویدادها مشترک می‌شوند، و زمانی که داده‌ها در جدول دیتابیس تغییر می‌کنند اطلاعیه‌های آپدیت دریافت می‌کنند. بدین ترتیب سرور‌های برنامه می‌توانند به صورت مستقل کَش داخل حافظه خود را آپدیت کنند.

**_مثال 23-4. سرور API با Sanic_**

```python
# sanic_demo.py
import argparse
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json
from util import Database
from perf import aelapsed, aprofiler
import model

app = Sanic()

@aelapsed
async def new_patron(request):
    data = request.json
    id = await model.add_patron(app.pool, data)
    return json(dict(msg='ok', id=id))

class PatronAPI(HTTPMethodView, metaclass=aprofiler):
    async def get(self, request, id):
        data = await model.get_patron(app.pool, id)
        return json(data)

    async def put(self, request, id):
        data = request.json
        ok = await model.update_patron(app.pool, id, data)
        return json(dict(msg='ok' if ok else 'bad'))

    async def delete(self, request, id):
        ok = await model.delete_patron(app.pool, id)
        return json(dict(msg='ok' if ok else 'bad'))

@app.listener('before_server_start')
async def db_connect(app, loop):
    app.db = Database('restaurant', owner=False)
    app.pool = await app.db.connect()
    await model.create_table_if_missing(app.pool)
    await app.db.add_listener('chan_patron', model.db_event)

@app.listener('after_server_stop')
async def db_disconnect(app, loop):
await app.db.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    app.add_route(
        new_patron, '/patron', methods=['POST'])
    app.add_route(
        PatronAPI.as_view(), '/patron/<id:int>')
    app.run(host="0.0.0.0", port=args.port)
```

۱. ابزار کمکی Database، همانطور که پیش‌تر توضیح داده شد. این ابزار کمکی شامل متدهای لازم برای اتصال به پایگاه داده است.

۲. دو ابزار دیگر که برای لاگ گرفتن از زمان سپری شده در هر اندپوینت API با یکدیگر ترکیب کرده‌ام از این ابزار در بحث قبلی استفاده کردم تا بتوانیم زمان پاسخگویی به ریکوئست GET را موقع دریافت اطلاعات از کَش اندازه‌گیری کنیم. پیاده‌سازی‌های `()aelapsed` و `()profiler` در این موردپژوهی اهمیتی ندارند، اما می‌توانید آن‌ها را در **مثال ‌B-1** مشاهده کنید.

۳. نمونه اصلی از برنامه‌ی Sanic را می‌سازیم.

۴. این تابع کوروتین برای ایجاد ورودی‌های کلاینت‌ها جدید است. در فراخوانی تابع `()add_route` که در بخش‌های پایانی کد مشاهده می‌شود، ‍`()new_patron` تنها برای متد POST با `patron/` مرتبط است. دکوراتور @aelapsed بخشی از Sanic API نیست: اختراع خودم است، صرفا برای لاگ گرفتن زمانبندی‌ها برای هر فراخوانی.

۵. با استفاده از `json.` روی شئ `request`

<p dir='rtl'>۶. Sanic با استفاده از ویژگی <code>json.</code> در شئ <code>request</code> داده‌های JSON دریافتی را deserialize می‌کند.</p>

۷. ماژول `model`، که در برنامه import کرده‌ام، مدلی برای جدول `patron` در دیتابیس است. در نمونه کد بعدی به جزئیات آن خواهم پرداخت؛ فعلا فقط توجه داشته باشید که تمام کوئری‌های دیتابیس و SQL در این ماژول قرار دارند. در اینجا من connection pool برای دیتابیس را استفاده می‌کنم. این الگو برای تمام تعاملات با مدل دیتابیس در این تابع و در کلاس `PatronAPI` که در ادامه به آن می‌رسیم استفاده می شود.

۸. یک کلید اصلی جدید، id، ساخته خواهد شد، و در قالب JSON برگردانده می‌شود.

۹. در حالی که ساخته شدن در تابع `()new_patron` مدیریت می‌شود، تمام تعاملات دیگر در این class-based view که Sanic ارائه داده است مدیریت می‌شوند. تمام متدها در این کلاس با یک URL مرتبط هستند، `patron/<id:int>/`، که می‌توانید آن را در تابع `()add_route` مشاهده کنید. توجه داشته باشید که پارامتر id در URL به هر یک از متدها ارسال می‌شود، و این پارامتر برای هر سه اندپوینت اجباری است.
می‌توانید به راحتی آرگومان `metaclass` را نادیده بگیرید: تمام کاری که این آرگومان انجام می‌دهد استفاده از دکوراتور `aelapsed@` برای متدها جهت پرینت کردن زمانبندی‌ها در لاگ است. دوباره اشاره می‌کنم که این بخشی از Sanic API نیست؛ این خلاقیت من برای لاگ گرفتن از داده‌های زمانبندی است.

۱۰. همانند قبل، تعامل با مدل داخل ماژول مدل انجام می‌شود.

۱۱. اگر مدل برای انجام عملیات آپدیت، شکست را گزارش دهد، داده‌های response را تغییر می‌دهم . من این مورد را برای خوانندگانی قرار داده‌ام که هنوز با عملگرد سه‌تایی در پایتون آشنا نشده‌اند.

۱۲. دکوراتورهای `app.listener@` در واقع hook هایی هستند که توسط Sanic ارائه شده‌اند تا بتوانید در طول راه‌اندازی و خاموش کردن، اقدامات اضافی مورد نظر خود را اضافه کنید. این مورد، `before_server_start`، پیش از آن که سرور API راه‌اندازی شود فراخوانی می‌شود. اینجا مکان مناسبی برای راه‌اندازی اتصال دیتابیس به نظر می‌رسد.

۱۳. از `Database` برای ایجاد اتصال به نمونه‌ی PostgreSQL استفاده کنید. دیتابیسی که به آن متصل می‌‌شویم restaurant است.

۱۴. یک connection pool به دیتابیس دریافت کنید.

۱۵. از مدل (برای جدول patron) استفاده کنید تا در صورتی که جدول وجود نداشته باشد آن را ایجاد کند.

۱۶. از مدل برای ساخت یک dedicated_listener برای رویدادهای دیتابیس استفاده کنید تا به کانال `chan_patron` گوش کند. تابع callback برای این رویدادها `()model.db_event` است که در مثال بعدی به آن خواهم پرداخت. تابع callback هر زمان که دیتابیس کانال را آپدیت می‌کند فراخوانی می‌شود.

<p dir='rtl'>۱۷. <code>after_server_stop</code> یک hook است که برای تسک‌هایی که در زمان خاموشی اجرا می‌شوند تعبیه شده‌ است. در اینجا ما اتصال خود را با دیتابیس قطع می‌کنیم. </p>

۱۸. این فراخوانی `()add_route` ریکوئست‌های POST را برای `patron/` به تابع کوروتین `()new_patron` ارسال می‌کند.

۱۹. این فراخوانی `()add_route` تمام ریکوئست‌ها را برای `patron/<id:int>/` به `PatronAPI‍` که یک class-based view است ارسال می‌کند.

کد قبلی شامل تمام پردازش‌های HTTP برای سرور ما است، و همچنین تسک‌های راه‌اندازی و خاموشی مانند راه‌اندازی یک connection pool متصل به دیتابیس، و مهم‌تر از همه، راه‌اندازی یک db-event listener روی کانال chan_patron بر روی سرور دیتابیس.

مثال 24-4 نشان‌دهنده‌ی مدل برای جدول patron در دیتابیس است.

**_مثال 24-4. مدل DB برای جدول "patron"_**

```python
# model.py
import logging
from json import loads, dumps
from triggers import (
    create_notify_trigger, add_table_triggers)
from boltons.cacheutils import LRU

logger = logging.getLogger('perf')
CREATE_TABLE = (
    'CREATE TABLE IF NOT EXISTS patron('
    'id serial PRIMARY KEY, name text, '
    'fav_dish text)'
    )
INSERT = (
    'INSERT INTO patron(name, fav_dish) '
    'VALUES ($1, $2) RETURNING id'
    )
SELECT = 'SELECT * FROM patron WHERE id = $1'
UPDATE = 'UPDATE patron SET name=$1, fav_dish=$2 WHERE id=$3'
DELETE = 'DELETE FROM patron WHERE id=$1'
EXISTS = "SELECT to_regclass('patron')"
CACHE = LRU(max_size=65536)

async def add_patron(conn, data: dict) -> int:
    return await conn.fetchval(
        INSERT, data['name'], data['fav_dish'])

async def update_patron(conn, id: int, data: dict) -> bool:
    result = await conn.execute(
        UPDATE, data['name'], data['fav_dish'], id)
    return result == 'UPDATE 1'

async def delete_patron(conn, id: int):
    result = await conn.execute(DELETE, id)
    return result == 'DELETE 1'

async def get_patron(conn, id: int) -> dict:
    if id not in CACHE:
        logger.info(f'id={id} Cache miss')
        record = await conn.fetchrow(SELECT, id)
        CACHE[id] = record and dict(record.items())
    return CACHE[id]

def db_event(conn, pid, channel, payload):
    event = loads(payload)
    logger.info('Got DB event:\n' + dumps(event, indent=4))
    id = event['id']
    if event['type'] == 'INSERT':
        CACHE[id] = event['data']
    elif event['type'] == 'UPDATE':
        CACHE[id] = event['data']['new']
    elif event['type'] == 'DELETE':
        CACHE[id] = None

async def create_table_if_missing(conn):
    if not await conn.fetchval(EXISTS):
        await conn.fetchval(CREATE_TABLE)
        await create_notify_trigger(
            conn, channel='chan_patron')
        await add_table_triggers(
            conn, table='patron')
```

۱. برای دریافت اعلان در زمان‌هایی که داده‌ها تغییر می‌کنند، باید محرک‌هایی را به دیتابیس اضافه کنیم. من این کمک‌کننده‌های مفید را برای ساخت تابع trigger (با ‍`create_notify_trigger`) و همچنین برای اضافه کردن trigger به یک جدول خاص (با `add_table_triggers`) ایجاد کرده‌ام. کوئری‌های SQL مورد نیاز برای انجام این کار تا حدودی از محدوده این کتاب خارج است، اما همچنان برای درک چگونه کار کردن این موردپژوهی لازم است. من کد مورد استفاده برای این محرک‌ها را در پیوست B قرار داده‌ام.

۲. پکیج boltons مجموعه‌ای از ابزارهای مفید را ارائه می‌دهد که کوچک‌ترین آن‌ها کَش LRU است، گزینه‌ای همه‌کاره‌تر نسبت به دکوراتور `lru_cache@` در ماژول کتابخانه استاندارد `functools` [^3].

۳. این تکه متن شامل تمام SQL لازم برای عملیات استاندارد CRUD است. توجه داشته باشید که من برای پارامترها از سینتکس اصلی PostgreSQL استفاده می‌کنم: 1$, 2$, و غیره. در اینجا چیز جدیدی وجود ندارد و بیش‌تر در مورد آن بحث نخواهد شد.

۴. برای این نمونه برنامه کَش را ایجاد کنید.

۵. من این تابع را از ماژول Sanic داخل اندپوینت `()new_patrons` برای اضافه کردن کلاینت‌ها جدید فراخوانی کردم. داخل تابع، از متد `()fetchval` برای اضافه کردن داده‌ی جدید استفاده می‌کنم. چرا `()fetchval` و نه `()execute`؟ زیرا `()fetchval` کلید اصلی رکورد جدید را بازمی‌‌گرداند! [^4]

۶. یکی از رکوردهای موجود را آپدیت کنید. زمانی که این عملیات موفق‌ شود، UPDATE 1 از طرف PostgreSQL بازگردانده می‌شود. من از آن برای تایید موفق بودن عملیات آپدیت استفاده می‌کنم.

۷. عملیات حذف بسیار مشابه با عملیات آپدیت است.

۸. این عملیات خواندن است. این تنها بخشی از رابط CRUD ما است که به کَش اهمیت می دهد. یک لحظه به آن فکر کنید: زمان درج، اپدیت، و یا حذف داده‌ها کَش را آپدیت نمی‌کنیم. به این دلیل که برای آپدیت کَش در صورت تغییر داده‌ها به اعلان‌های async از سمت دیتابیس (از طریق محرک‌ها) متکی هستیم.

۹. البته، ما همچنان می‌خواهیم پس از اولین GET از کَش استفاده کنیم.

۱۰. تابع `()db_event` یک callback است که زمانی که رویدادهایی در کانال اعلان‌های دیتابیس یا همان `chan_patrons` وجود دارند توسط asyncpg فراخوانی می‌شود. conn اتصالی است که رویداد بر روی آن ارسال شده است، pid همان process ID برای نمونه PostgreSQL است که رویداد را ارسال کرده است، channel نام `channel` است (که در این مورد `chan_patron` نام دارد)، و payload داده‌ای است که روی کانال ارسال می‌شود.

۱۱. فایل JSON را به dict تبدیل کنید.

۱۲. پر کردن کَش به طور کلی ساده است، اما توجه داشته باشید که رویداد آپدیت شامل داده‌های جدید و داده‌های قدیمی است، به همین دلیل باید مطمئن شویم که تنها داده‌های جدید را کَش می‌کنیم.

۱۳. این یک تابع کاربردی کوچک است که من برای ایجاد کردن مجدد جدول در صورتی که وجود نداشته باشد ساخته‌ام. اگر نیاز به انجام مکرر این کار دارید این تابع بسیار مفید است-مثلا هنگام نوشتن نمونه‌های کد برای این کتاب!

همچنین اینجا همان جایی است که محرک‌های اعلان‌های دیتابیس ساخته شده و به جدول patron اضافه می‌شوند. برای مشاهده‌ی فهرست مشروح این توابع به مثال B-1 مراجعه کنید.

این مثال ما را به پایان این موردپژوهی می‌رساند. مشاهده کردیم که استفاده از Sanic می‌تواند تا چه حد ساخت سرور API را آسان کند، و دیدیم که چگونه می‌توان از asyncpg برای اجرای کوئری‌ها توسط connection pool استفاده کرد، و همچنین چگونه می‌توان از قابلیت اعلان‌های async در PostgreSQL برای دریافت callbackها بر روی یک اتصال مخصوص و بلندمدت دیتابیس استفاده کرد.

بسیاری از مردم ترجیه می‌دهند برای کار با دیتابیس‌ها از object-relational mappers استفاده کنند، و در این زمینه SQLAlchemy پیشتاز است. پشتیبانی رو به رشدی برای استفاده از SQLAlchemy با asyncpg در کتابخانه‌های third-part مانند asyncpgsa و GINO وجود دارد. یکی از دیگر از ORMهای محبوب، Peewee، از طریق پکیج aiopeewee از asyncio پشتیبانی می‌کند.

## کتابخانه‌ها و منابع دیگر

کتابخانه‌های بسیار دیگری برای asyncio وجود دارند که در این کتاب به آن‌ها پرداخته نشد. برای کسب اطلاعات بیش‌تر می‌توانید پروژه aio-libs را بررسی کنید که نزدیک به 40 کتابخانه را مدیریت می‌کند، و همچنین پروژه Awesome asyncio که بسیاری از پروژه‌های دیگر سازگار با ماژول asyncio را نشان می‌دهد.

یکی از کتابخانه‌هایی که باید به آن اشاره ویژه‌ای داشته باشیم aiofiles است. همانطور که ممکن است از بحث‌های قبلی به خاطر داشته باشید،‌ گفتم که برای دستیابی به همزمانی بالا در Asyncio، بسیار مهم است که حلقه هرگز مسدود نشود. در این زمینه، تمرکز ما بر عملیات مسدودکننده عمدتا بر روی ورودی و خروجی‌های مبتنی بر شبکه بوده است، اما اینطور که به نظر می‌رسد دسترسی به دیسک نیز یک عملیات مسدودکننده است که در سطوح بالای همزمانی بر عملکرد شما تاثیرگذار خواهد بود. راه حل این مورد aiofiles است که روش مناسبی برای دسترسی به دیسک در رشته‌ها ارائه می‌دهد. این روش به این دلیل کار می‌کند که پایتون هنگام عملیات مربوط به فایل‌ها GIL را ازاد می‌کند تا رشته اصلی شما (که حلقه asyncio را اجرا می‌کند) تحت تاثیر قرار نگیرد.

مهم‌ترین دامنه برای Asyncio برنامه‌نویسی شبکه است. به همین دلیل، بد نیست که کمی درباره برنامه‌نویسی سوکت بیاموزید، و حتی پس از گذشت این همه سال، “Socket Programming HOWTO” از Gordon McMillan، که همراه داکیومنت استاندارد پایتون ارائه می‌شود، یکی از بهترین معرفی‌هایی است که می‌توانید پیدا کنید.

من Asyncio را از منابع مختلفی یاد گرفتم، که بسیاری از آن‌ها در بخش‌های قبلی معرفی شده‌اند. هر کس به روش متفاوتی یاد می‌گیرد، پس بهتر است مواد آموزشی مختلف را بررسی کنید. در اینجا به چند مورد دیگر اشاره شده است که به نظر من مفیدند:

- سخنرانی “Get to Grips with Asyncio in Python 3” از Robert Smallshire که در NDC لندن در ژانویه 2017 ارائه شد. تا کنون این بهترین ویدئوی یوتیوب درباره Asyncio است که به آن برخوردم. این سخنرانی ممکن است برای افراد مبتدی کمی پیشرفته باشد، اما واقعا توضیح شفافی از چگونگی طراحی Asyncio ارائه می‌دهد.

- اسلایدهای “Building Apps with Asyncio” از Nikolay Novik که در سال 2016 در PyCon UA ارائه شد. اطلاعات ارائه شده سنگین هستند، اما تجربیات عملی بسیاری در این اسلایدها گنجانده شده است.

- استفاده‌ی بسیار از Python REPL، آزمایش کردن موارد گوناگون، و دیدن نتایجی که حاصل می‌شوند.

شما را تشویق می‌کنم که به یادگیری ادامه دهید، و اگر در درک مفهومی مشکل دارید، به دنبال منابع جدید باشید تا توضیحی را پیدا کنید که برایتان مفید باشد.

[^1]: در واقع، می‌توانید این کار را انجام دهید. به شرطی که سوکت‌هایی که در رشته‌های مختلف مورد استفاده قرار می‌گیرند به طور کامل در رشته‌های خود ساخته شده، مورد استفاده قرار گرفته، و نابود شوند. انجام این کار ممکن، اما مشکل است، و بسیاری ازا فراد برای انجام صحیح آن تلاش می‌کنند. به همین دلیل هم بیش‌تر توصیه می‌شود از یک رشته و مکانیزم polling استفاده شود.
[^2]: دستور تهیه این غذا، و دیگر غذاها با Spam را می‌توانید در وبسایت UKTV بیابید.
[^3]: با pip install boltons آن را نصب کنید.
[^4]: البته به بخش RETURNING id از SQL نیز نیاز دارید!
