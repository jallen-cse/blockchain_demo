
from typing import List

class Mempool:
    def __init__(self):
        self.txs: List[bytes] = []

    def tx(self, serialized: bytes):
        self.txs.append(serialized)
    
    def get_txs(self, max_size: int = 16384) -> bytes: 
        buffer = bytes()
        take_count = 0
        for tx in self.txs:
            if len(buffer) + len(tx) <= max_size:
                buffer += tx
                take_count += 1
            else:
                break
        self.txs = self.txs[take_count:]
        return buffer