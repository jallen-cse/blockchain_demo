
import threading
from typing import List, Tuple
from datetime import datetime
from multiprocessing.connection import Listener

from common import IPC_ADDRESS, ReqType
from mempool import Mempool
from block import Block

class GenesisError(Exception):
    def __str__(self):
        return "genesis may only occur once"

class Blockchain:
    def __init__(self, block_time: float = 1.0, max_block_size: int = 16384):
        self.mempool = Mempool()
        self.blocks: List[Block] = []
        self.block_time = block_time
        self.block_size = max_block_size

        self.halter = threading.Event()
        self.writer = threading.Thread(target=self.write_loop)
        self.writer.start()

        self.server = threading.Thread(target=self.serve_queries)
        self.server.setDaemon(True)
        self.server.start()

    def stop(self):
        """Interrupt block commission and wait for writer loop"""
        self.halter.set()
        self.writer.join()

    def genesis(self):
        """Create a genesis block (first block in chain)"""
        if len(self.blocks) > 0:
            raise GenesisError
        genesis_block = Block(0, datetime.now(), b'genesis', b'')
        self.blocks.append(genesis_block)
        print(genesis_block)

    def write_loop(self):
        """Initialize the chain then, every `block_time` seconds, collect from
        the mempool and write the next block"""
        self.genesis()
        while not self.halter.wait(self.block_time):
            new_block = Block(
                len(self.blocks),
                datetime.now(),
                self.mempool.get_txs(self.block_size),
                self.blocks[-1].hash)
            self.blocks.append(new_block)
            print(new_block)
    
    def serve_queries(self):
        """Serve basic inter-proccess block queries"""
        listener = Listener(IPC_ADDRESS)
        while not self.halter.is_set():
            connection = listener.accept()
            while not connection.closed and not self.halter.wait(0.05):
                if connection.poll():
                    try:
                        req: ReqType = connection.recv()
                        if req == 'close':
                            connection.close()
                        else:
                            connection.send(
                                self.blocks[req] if 
                                req < len(self.blocks) 
                                else None)
                    except EOFError:
                        connection.close()
