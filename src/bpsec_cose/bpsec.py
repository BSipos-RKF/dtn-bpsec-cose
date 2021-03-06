''' BPSec Abstract Security Block (ASB) structure and logic.
'''
from dataclasses import dataclass, field
import enum
import re
from typing import List, Optional, Any
from .bp import EndpointId


@enum.unique
class BlockType(enum.IntEnum):
    ''' BPSec block type codepoints.
    '''
    BIB = 11
    BCB = 12


@dataclass
class KeyValPair():
    key: int
    val: Any


@dataclass
class SecurityBlockData():
    ''' The abstract security block type-specific-data.
    '''

    @enum.unique
    class Flags(enum.IntFlag):
        ''' Flags derived from presence of optional data.
        '''
        NONE = 0x00
        HAS_PARAMS = 0x01

    targets: List[int]
    context_id: int
    security_source: EndpointId
    parameters: Optional[List[KeyValPair]] = None
    results: List[List[KeyValPair]] = field(default_factory=list)

    def encode_item(self):
        flags = SecurityBlockData.Flags.NONE
        if self.parameters:
            flags |= SecurityBlockData.Flags.HAS_PARAMS

        item = [
            self.targets,
            self.context_id,
            flags,
        ]
        item.append(self.security_source)
        if self.parameters:
            item.append(self.parameters)
        item.append(self.results)
        return item
