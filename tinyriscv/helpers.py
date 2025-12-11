from tinyriscv import dtypes

def homogenize(buf:list, dtype=None):
  if not buf: raise ValueError("Cannot homogenize an empty buffer")
  if isinstance(dtype, dtypes.DType):
    if dtype in dtypes.FP: return [float(x) for x in buf], dtype
    elif dtype in dtypes.INT or dtype in dtypes.UINT: return [int(x) for x in buf], dtype
    else: raise TypeError(f"Unsupported dtype: {dtype}")
  has_float = any(isinstance(x, float) for x in buf)
  has_int = all(isinstance(x, int) for x in buf)
  if has_int:
    target_dtype = dtypes.int32
    buf = [int(x) for x in buf]
  elif has_float:
    target_dtype = dtypes.float32
    buf = [float(x) for x in buf]
  else: raise TypeError(f"Unsupported element types in buf: {set(type(x) for x in buf)}")
  return buf, target_dtype

def sign_extend(value, bits):
  sign_bit = 1 << (bits - 1)
  return (value & (sign_bit - 1)) - (value & sign_bit)
