
import struct
import hashlib
from datetime import datetime

class Block:
    def __init__(
        self,
        height: int,
        timestamp: datetime,
        data: bytes,
        prev_hash: bytes
    ):
        self.height = height
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.data = data
        self.hash = hashlib.sha256(
            height.to_bytes(8, 'big') +
            struct.pack("d", timestamp.timestamp()) +
            prev_hash + data).digest()
    
    def __repr__(self) -> str:
        return f"""        --------------------------------------
        [  height   : {self.height}
        [ timestamp : {self.timestamp}
        [ prev_hash : {self.prev_hash.hex()}
        [   data    : ({len(self.data)} bytes) {self.data[:16].hex()}...{self.data[-16:].hex()}
        [   hash    : {self.hash.hex()}
        --------------------------------------
                        |""" \
            if len(self.data) > 32 else f"""        --------------------------------------
        [  height   : {self.height}
        [ timestamp : {self.timestamp}
        [ prev_hash : {self.prev_hash.hex()}
        [   data    : ({len(self.data)} bytes) {self.data.hex()}
        [   hash    : {self.hash.hex()}
        --------------------------------------
                        |"""