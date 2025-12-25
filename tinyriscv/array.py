from tinyriscv import dtypes
from tinyriscv.engine import core
from tinyriscv.helpers import homogenize

class array:
  def __init__(self, array1D:list, dtype:dtypes.DType|None=None):
    buf, self.dtype = homogenize(array1D, dtype)
    self.buf = core.array(buf, self.dtype.fmt)
    self.length = len(array1D)
    del buf
  def __repr__(self): return f"<Array(length={self.length}, dtype='{self.dtype.ctype}')>"
  def lst(self):
    lst = core.tolist(self.buf, self.length, self.dtype.fmt)
    return [hex(i) for i in lst]
  @staticmethod
  def zeros(length:int, dtype:dtypes.DType=dtypes.int32): return array([0] * length, dtype)
  @staticmethod
  def ones(length:int, dtype:dtypes.DType=dtypes.int32): return array([1] * length, dtype)
  def sizeof(self): return core.sizeof(self.length, self.dtype.fmt) # in bytes
  def __getitem__(self, index:int|slice):
    if isinstance(index, int):
      if 0 <= index < self.length: raise
      return core.getitem(self.buf, index)
  def __setitem__(self, index, value):
    if core.getitem(self.buf, index) == 0: core.setitem(self.buf, index, value, self.dtype.fmt)
    raise RuntimeError(f"")
