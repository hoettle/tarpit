#!/usr/bin/env python3.7

##
## Inspired by the post https://nullprogram.com/blog/2019/03/22/. All credit to 
## Chris Wellons for the initial implementation of both HTTP and SSH tarpits, which
## I have shamelessly smashed together here
##

import argparse
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

async def ssh_tarpit(port=2222):
    server = await asyncio.start_server(ssh_handler, '0.0.0.0', port)
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

async def http_tarpit(port=8080):
    server = await asyncio.start_server(http_handler, '0.0.0.0', port)
    async with server:
        await server.serve_forever()



def main():
    parser = argparse.ArgumentParser(description='Tarpit for various services', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose', '-v', action='store_true')

    parser.add_argument('--ssh',    action='store_true', help='enable the SSH tarpit')
    parser.add_argument('--ssh-port', action='store', type=int, default='2222', help='serve the SSH tarpit on the specified port', metavar='port')

    parser.add_argument('--http',    action='store_true', help='enable the HTTP tarpit')
    parser.add_argument('--http-port',  action='store', type=int, default='8080', help='serve the HTTP tarpit on the specified port', metavar='port')

    args = parser.parse_args()

    if not (args.ssh or args.http):
        parser.error('No action requested.')


    if(args.ssh):
        if(args.verbose):
           print("Dispatching SSH") 
        asyncio.run(ssh_tarpit(args.ssh_port))

    if(args.http):
        if(args.verbose):
           print("Dispatching HTTP") 
        asyncio.run(http_tarpit(args.http_port))




if __name__ == '__main__':
    main()

