#!/usr/bin/env python3

import json
import ecdsa
import random
import hashlib
import threading

from tx import Tx
from mempool import Mempool
from blockchain import Blockchain

class SimClient:
    def __init__(self, key: ecdsa.SigningKey, mempool: Mempool):
        self.skey: ecdsa.SigningKey = key
        self.pkey: ecdsa.VerifyingKey = key.get_verifying_key()
        
        self.halter = threading.Event()
        self.worker = threading.Thread(
            target=self.sim_send_txs, args=(mempool,))
        self.worker.setDaemon(True)
        self.worker.start()

    def stop(self):
        self.halter.set()
        self.worker.join()

    def sim_send_txs(self, mempool: Mempool):
        tx_count = 0
        send_interval = max(random.random() * 5, 1)
        while not self.halter.wait(send_interval):
            body = json.dumps({
                'tx_count': tx_count,
                'immutable': 'value'
            }).encode('ascii')
            sig = self.skey.sign_deterministic(body, hashfunc=hashlib.sha256)
            tx = Tx(self.pkey.to_string(), body, sig)
            mempool.tx(tx.serialize())
            tx_count += 1
        print(f'{self.pkey.to_string().hex()[:16]} sent {tx_count} transactions')

if __name__ == '__main__':

    BLOCK_TIME = 1          # how much time (in seconds) between each block
    MAX_BLOCK_SIZE = 16384  # how much transaction data may fit in each block
    NUM_CLIENTS = 25        # number of simulated tx clients to initialize

    chain = Blockchain(BLOCK_TIME, MAX_BLOCK_SIZE)

    clients = [
        SimClient(
            ecdsa.SigningKey.generate(ecdsa.SECP256k1),
            chain.mempool
        ) for _ in range(NUM_CLIENTS)
    ]
    
    try: input()
    except KeyboardInterrupt: pass

    for client in clients:
        client.stop()
    chain.stop()