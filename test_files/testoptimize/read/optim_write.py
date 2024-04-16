from time import time
from asyncio import run
from aiofiles import open as aiopen
from opt import write as cwrite
from optim_read import aiopyread

def timeit(func, *args, **kwargs):
	start = time()
	res = func(*args, **kwargs)
	end = time()

	print(end - start)
	return res

def pywrite(filename, data):
	with open(filename, 'w', encoding='utf-8') as file:
		return file.write(data)

async def aiowrite(filename, data):
	async with aiopen(filename, 'w', encoding='utf-8') as file:
		return await file.write(data)

def aiopywrite(filename, data):
	return run(aiowrite(filename, data))

if __name__ == '__main__':
	lines = aiopyread('systemlog.log')
	print(len(lines.splitlines()))

	res2 = timeit(pywrite, 'systemlog.log', lines)
	print(f'Res2:\nName: pywrite\nResult: {res2}\n\n')
	del res2
	res3 = timeit(aiopywrite, 'systemlog.log', lines)
	print(f'Res3:\nName: aiopywrite\nResult: {res3}\n\n')
	del res3
	res1 = timeit(cwrite, 'systemlog.log', lines)
	print(f'Res1:\nName: cwrite\nResult: {res1}\n\n')
	del res1