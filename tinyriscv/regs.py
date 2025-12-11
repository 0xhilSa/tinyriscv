class RegFile:
  def __init__(self):
    self.x = [0] * 32
  def __getitem__(self, index:int|slice):
    if isinstance(index, int):
      if not 0 <= index < len(self.x): raise ValueError(f"invalid register call: {index}")
      return self.x[index]
    elif isinstance(index, slice): return self.x[index.start:index.stop:index.step]
  def __setitem__(self, index, value):
    if index == 0: raise ValueError(f"can't set the value of register x0(zero)")
    if not 1 <= index < len(self.x): raise ValueError(f"invalid register call: {index}")
    self.x[index] = value & 0xffffffff
  def __iter__(self): return iter(self.x)
  def __len__(self): return len(self.x)
