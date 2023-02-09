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
