class RISCVException(Exception):
  """Base class for all RISCV sim exceptions"""

class RegisterZeroViolation(RISCVException):
  """x0 register must always be zero"""

class MisalignedAddress(RISCVException):
  """Misaligned memory access"""

class InvalidRegister(RISCVException):
  """Invalid register index (must be x0-x31)"""
