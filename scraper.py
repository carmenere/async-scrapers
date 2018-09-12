import asyncio
import aiohttp
import requests
import targets
import concurrent.futures

sites = []

async def fetch1(url):
#async def fetch1(url, executor):
    s = requests.Session()
    print('start load {}'.format(url))
    #return s.get(url)
    #return await loop.run_in_executor(executor, s.get, url)
    return await loop.run_in_executor(None, s.get, url)
    #sites.append(yield from loop.run_in_executor(None, s.get, url))


import time

async def fetch2(url):
    response = await aiohttp.request('GET', url)
    return await response.text()

def fn(future):
    print('Task {} complited.'.format(future.id))
    sites.append(future.result())

def async_main():
    #executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_event_loop()
    futures_list = []
    for uri in targets.targets[0:11]:
        #future = asyncio.ensure_future(fetch1(uri, executor))
        future = asyncio.ensure_future(fetch1(uri))
        futures_list.append(future)
        future.id = [id(future), uri]
        future.add_done_callback(fn)
    print(futures_list)
    #loop.run_until_complete(asyncio.gather(tuple(futures_list[0:10])))
    loop.run_until_complete(asyncio.wait(futures_list[0:10]))
    #time.sleep(10)
    #loop.stop()
    #loop.close()


def main(targets):
    for uri in targets:
        print (uri)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    async_main()
    for site in sites:
        print(site)

