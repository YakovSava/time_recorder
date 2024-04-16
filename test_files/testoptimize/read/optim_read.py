from time import time
from asyncio import run
from aiofiles import open as aiopen
from opt import read as cread

def timeit(func, *args, **kwargs):
	start = time()
	res = func(*args, **kwargs)
	end = time()

	print(end - start)
	return res

def pyread(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		return file.read()

async def aioread(filename):
	async with aiopen(filename, 'r', encoding='utf-8') as file:
		return await file.read()

def aiopyread(filename):
	return run(aioread(filename))

if __name__ == '__main__':
	res1 = timeit(cread, 'systemlog.log')
	print(f'Res1:\nName: cread\nCount: {len(res1.splitlines())}')
	del res1
	res2 = timeit(pyread, 'systemlog.log')
	print(f'Res2:\nName: pyread\nCount: {len(res2.splitlines())}')
	del res2
	res3 = timeit(aiopyread, 'systemlog.log')
	print(f'Res3:\nName: aiopyread\nCount: {len(res3.splitlines())}')
	del res3