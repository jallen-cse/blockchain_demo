#!/usr/bin/env python3

import os
import json
from typing import Optional
from multiprocessing.connection import Client, Connection

from block import Block
from common import IPC_ADDRESS, ReqType, ResType

clear_term = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def display_block(block: Block):
    clear_term()
    formatted = ''
    for serialized in [chunk.decode('ascii') + '}' for chunk in block.data.split(b'}')][:-1]:
        tx = json.loads(serialized)
        tx['body'] = json.loads(bytes.fromhex(tx['body']).decode('ascii'))
        formatted += '\n' + json.dumps(tx, indent=2)
    print('-----------------------------------')
    print(f'Height: {block.height}') 
    print(f'Time: {block.timestamp}')
    print(f'Hash: {block.hash.hex()}\n')
    print(f'Data (raw): {block.data}\n')
    print(f'Data (decoded): {formatted}')
    print('-----------------------------------')

if __name__ == '__main__':
    
    ipc_client: Optional[Connection] = None
    try:
        ipc_client = Client(IPC_ADDRESS)
    except ConnectionRefusedError:
        print(f"Failed to reach blockchain on {IPC_ADDRESS[0]}:{IPC_ADDRESS[1]}")
        exit(1)

    while True:
        try:
            possible = input("Specify a chain height to query: ")
            req: ReqType = int(possible, base=10)
            ipc_client.send(req)
            res: ResType = ipc_client.recv()
            if res: display_block(res)
            else: print(f"Chain height is less than {req}")
        except ValueError:
            print("Input a valid positive integer")
        except KeyboardInterrupt:
            print()
            exit(0)