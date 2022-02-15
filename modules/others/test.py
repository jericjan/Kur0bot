import asyncio, time
from aiolimiter import AsyncLimiter
limiter = AsyncLimiter(4, 8)
async def task(id):
    await asyncio.sleep(id * 0.01)
    async with limiter:
        print(f'{id:>2d}: Drip! {time.time() - ref:>5.2f}')

tasks = [task(i) for i in range(10)]
ref = time.time()
result = asyncio.run(asyncio.wait(tasks))