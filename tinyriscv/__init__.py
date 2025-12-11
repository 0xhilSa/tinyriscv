from tinyriscv import dtypes
from tinyriscv.array import array
from tinyriscv.regs import RegFile

class RISCV:
  def __init__(self, memory:int=1024): # memory size of 1MB
    self.memory = array.zeros(memory, dtypes.uint8)
    self.regs = RegFile()
    self.pc = 0
    self.halted = False
    self.__lines = []
  def ipc(self): self.pc += 4
  def add(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = self.regs[rs1] + self.regs[rs2] # type: ignore
    self.__lines.append(f"add x{rd}, x{rs1}, x{rs1}")
    self.ipc()
  def addi(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = self.regs[rs1] + imm # type: ignore
    self.__lines.append(f"add x{rd}, x{rs1}, {imm}")
    self.ipc()
  def sub(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = self.regs[rs1] - self.regs[rs2] # type: ignore
    self.__lines.append(f"sub x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def mul(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = self.regs[rs1] * self.regs[rs2] # type: ignore
    self.__lines.append(f"muli x{rd}, x{rs1}, x{rs1}")
    self.ipc()
  def muli(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = self.regs[rs1] * imm # type: ignore
    self.__lines.append(f"muli x{rd}, x{rs1}, {imm}")
    self.ipc()
  def xor(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = self.regs[rs1] ^ self.regs[rs2] # type: ignore
    self.__lines.append(f"xor x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def sign_extend(self, value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)
  def regmap(self):
    txt = ""
    for index, value in enumerate(self.regs):
      if index == len(self.regs)-1: txt += f"x{index} = {value}"
      else: txt += f"x{index} = {value}\n"
    return txt
  def asm(self, output:bool=False):
    txt = ""
    for line in self.__lines: txt += line+"\n"
    if output:
      with open("a.asm", "a") as file: file.write(txt)
    return txt
