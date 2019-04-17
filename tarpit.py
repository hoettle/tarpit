#!/usr/bin/env python3.7

##
## Inspired by the post https://nullprogram.com/blog/2019/03/22/. All credit to 
## Chris Wellons for the initial implementation of both HTTP and SSH tarpits, which
## I have shamelessly smashed together here
##


import asyncio
import random

async def ssh_handler(_reader, writer):
    try:
        while True:
            await asyncio.sleep(10)
            writer.write(b'%x\r\n' % random.randint(0, 2**32))
            await writer.drain()
    except ConnectionResetError:
        pass

async def ssh_tarpit():
    server = await asyncio.start_server(ssh_handler, '0.0.0.0', 2222)
    async with server:
        await server.serve_forever()


async def http_handler(_reader, writer):
    writer.write(b'HTTP/1.1 200 OK\r\n')
    try:
        while True:
            await asyncio.sleep(5)
            header = random.randint(0, 2**32)
            value = random.randint(0, 2**32)
            writer.write(b'X-%x: %x\r\n' % (header, value))
            await writer.drain()
    except ConnectionResetError:
        pass

async def http_tarpit():
    server = await asyncio.start_server(http_handler, '0.0.0.0', 8080)
    async with server:
        await server.serve_forever()


asyncio.run(ssh_tarpit())
asyncio.run(http_tarpit())

