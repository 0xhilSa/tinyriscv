from __future__ import annotations
from typing import Literal, Type, Union, Final
from dataclasses import dataclass

Fmts = Literal["b", "B", "h", "H", "i", "I", "f"]

@dataclass(frozen=True, eq=True)
class DType:
  fmt:Fmts
  ctype:str
  nbyte:int
  signed:bool
  @classmethod
  def new(cls, fmt:Fmts, ctype:str, nbyte:int, signed:bool): return DType(fmt, ctype, nbyte, signed)
  def __repr__(self): return f"<DType(ctype='{self.ctype}', fmt='{self.fmt}', nbyte={self.nbyte}, signed={self.signed})>"
  @property
  def nbit(self): return self.nbyte * 8
  @staticmethod
  def to_pytype(dtype:DType):
    if dtype.fmt in (INT + UINT): return int
    elif dtype.fmt in FP: return float
    else: raise TypeError
  @staticmethod
  def from_pytype(dtype:Type[Union[int, float, complex, bool]]):
    if dtype == int: return DType.new("i", "long", 4, True)
    elif dtype == float: return DType.new("f", "float", 8, True)
    else: TypeError(f"Invalid Type: {dtype.__name__}")

int8:Final = DType.new("b", "char", 1, True)
uint8:Final = DType.new("B", "unsigned char", 1, False)
int16:Final = DType.new("h", "short", 2, True)
uint16:Final = DType.new("H", "unsigned short", 2, False)
int32:Final = DType.new("i", "int", 4, True)
uint32:Final = DType.new("I", "unsigned int", 4, False)
float32:Final = DType.new("f", "float", 4, True)

INT = [int8, int16, int32]
UINT = [uint8, uint16, uint32]
FP = [float32]

maps = {int:int32, float:float32}
