
from typing import Optional, Union, Literal
from block import Block

ReqType = Union[int,Literal['close']]
ResType = Optional[Block]

IPC_ADDRESS = ('localhost', 6000)