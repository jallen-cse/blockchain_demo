
from base64 import b64encode
import json

class Tx:
    def __init__(
        self,
        sender: bytes,
        body: bytes,
        signature: bytes
    ):
        self.sender = sender.hex()
        self.body = body.hex()
        self.signature = signature.hex()
    
    def serialize(self) -> bytes:
        return json.dumps({
            'sender': self.sender,
            'body': self.body,
            'signature': self.signature
        }, separators=(',',':')).encode('ascii')