#!/usr/bin/env python3

##
## Inspired by the post https://nullprogram.com/blog/2019/03/22/. All credit to 
## Chris Wellons for the initial implementation of both HTTP and SSH tarpits, which
## I have shamelessly smashed together here
##

import argparse
import asyncio
import random

verbosity = 0

async def ssh_handler(_reader, writer):
    if (verbosity >= 1):
        addr = writer.get_extra_info('peername')
        print(f'SSH connected: {addr!r}')

    try:
        while True:
            await asyncio.sleep(10)
            writer.write(b'%x\r\n' % random.randint(0, 2**32))
            await writer.drain()
    except ConnectionResetError:
        if (verbosity >= 1):
            print(f'SSH disconnected: {addr!r}')

async def ssh_tarpit(port):
    if(verbosity >= 1):
      print(f'SSH tarpit enabled on port {port}')

    server = await asyncio.start_server(ssh_handler, '0.0.0.0', port)
    async with server:
        await server.serve_forever()

async def http_handler(_reader, writer):
    if (verbosity >= 1):
        addr = writer.get_extra_info('peername')
        print(f'HTTP connected: {addr!r}')

    writer.write(b'HTTP/1.1 200 OK\r\n')
    try:
        while True:
            await asyncio.sleep(10)
            header = random.randint(0, 2**32)
            value = random.randint(0, 2**32)
            writer.write(b'X-%x: %x\r\n' % (header, value))
            await writer.drain()
    except ConnectionResetError:
        if (verbosity >= 1):
            print(f'HTTP disconnected: {addr!r}')

async def http_tarpit(port):
    if(verbosity >= 1):
      print(f'HTTP tarpit enabled on port {port}')

    server = await asyncio.start_server(http_handler, '0.0.0.0', port)
    async with server:
        await server.serve_forever()

async def smtp_handler(_reader, writer):
    if (verbosity >= 1):
        addr = writer.get_extra_info('peername')
        print(f'SMTP connected: {addr!r}')

    try:
        while True:
            await asyncio.sleep(10)
            writer.write(b'220-%x\r\n' % random.randint(0, 2**32))
            await writer.drain()
    except ConnectionResetError:
        if (verbosity >= 1):
            print(f'SMTP disconnected: {addr!r}')

async def smtp_tarpit(port):
    if(verbosity >= 1):
      print(f'SMTP tarpit enabled on port {port}')

    server = await asyncio.start_server(smtp_handler, '0.0.0.0', port, limit=1024)
    async with server:
        await server.serve_forever()

def parse_args():
    parser = argparse.ArgumentParser(description='Tarpit for various services', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--verbose', '-v',  action='count', default=verbosity)

    parser.add_argument('mode',             action='store', nargs='*', default='all', choices=['ssh','http','smtp', 'all'], help='enable the specified tarpit(s)')

    parser.add_argument('--ssh-port',       action='store', type=int, default=2222, help='serve the SSH tarpit on the specified port', metavar='port')

    parser.add_argument('--http-port',      action='store', type=int, default=8080, help='serve the HTTP tarpit on the specified port', metavar='port')

    parser.add_argument('--smtp-port',      action='store', type=int, default=2525, help='serve the SMTP tarpit on the specified port', metavar='port')

    args = parser.parse_args()

    return parser.parse_args()



def main():
    tasks = list()
    args = parse_args()

    global verbosity
    verbosity = args.verbose

    if('ssh' in args.mode or 'all' in args.mode):
       tasks.append(ssh_tarpit(args.ssh_port))

    if('http' in args.mode or 'all' in args.mode):
        tasks.append(http_tarpit(args.http_port))

    if('smtp' in args.mode or 'all' in args.mode):
        tasks.append(smtp_tarpit(args.smtp_port))

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print('Terminated')





if __name__ == '__main__':
    main()

