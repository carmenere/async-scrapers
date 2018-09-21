import aiohttp
import asyncio
from targets import targets
import datetime
import uvloop
import aiodns
from aiohttp import client_exceptions

import os, errno

sites_dir = 'sites-by-python-scrapper'

try:
    os.makedirs(sites_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

async def fetch(session, domain, start):
    uri = 'http://{}/'.format(domain)
    print('--> uri {} started...'.format(uri))
    r=None
    try:
        async with session.get(uri, allow_redirects=True) as response:
            if response.status != 200:
                response.raise_for_status()
            try:
                r = await response.text()
            except Exception as e:
                print('[ERROR] {} for {}.'.format(e.__class__.__name__, uri))
            stop = datetime.datetime.now()
            print('<-- uri {} completed in {}s.'.format(uri, stop-start))
            try:
                fd = open('{}/{}'.format(sites_dir, domain), 'w')
                fd.write(str(r))#, encoding='UTF-8')
                fd.close()
            except Exception as e:
                print('[FILE WRITING ERROR] {}.'.format(e.__class__.__name__))
            return r
    except client_exceptions.ClientConnectionError as e:
        print('[ERROR] {} for {}.'.format(e.__class__.__name__, uri))
        print('DETAILS: \n', e)
    except Exception as e:
        print('[ERROR] {} for {}.'.format(e.__class__.__name__, uri))


async def fetch_all(session, uris, loop):
    #resolver = aiodns.DNSResolver(loop=loop)
    try:
        #results = await asyncio.wait([fetch(session, uri) for uri in uris])
        results = await asyncio.gather(*[fetch(session, uri, start) for uri in uris])
    except Exception as e:
        print('[ERROR] {}.'.format(e.__class__.__name__))
    return results


async def main(N=500):    
    uris = targets[0:N]
    loop = asyncio.get_event_loop()
    
    timeout = aiohttp.ClientTimeout(total=300, connect=None,
                      sock_connect=60, sock_read=None)
    conn = aiohttp.TCPConnector(verify_ssl=False, limit=250)
    #resolver = aiohttp.AsyncResolver(nameservers=["127.0.0.11"])
    try:
        #async with aiohttp.ClientSession(timeout=timeout, resolver=resolver, connector=conn, loop=loop) as session:
        async with aiohttp.ClientSession(timeout=timeout, connector=conn, loop=loop) as session:
        #async with aiohttp.ClientSession(timeout=timeout, loop=loop) as session:
            try:
                htmls = await fetch_all(session, uris, loop)
            except Exception as e:
                print('[ERROR] {}.'.format(e.__class__.__name__))
            #print(htmls)
    except Exception as e:
        print('[ERROR] {}.'.format(e.__class__.__name__))



if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    #asyncio.run_until_complete(main(1000))
    start = datetime.datetime.now()
    asyncio.run(main(1000))
