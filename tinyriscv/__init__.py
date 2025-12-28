from tinyriscv import dtypes
from tinyriscv.array import array
from tinyriscv.regs import RegFile

class RISCV:
  def __init__(self, memory:int=1024): # memory size of 1MB
    self.memory = array.zeros(memory, dtypes.uint32)
    self.regs = RegFile()
    self.pc = 0
    self.halted = False # for sim
    self.__lines = []
    self.__inst = []
  def ipc(self): self.pc += 4
  def add(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) + int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"add x{rd}, x{rs1}, x{rs1}")
    self.ipc()
  def addi(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1]) + imm # type: ignore
    inst = self.__encode_i(imm, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"add x{rd}, x{rs1}, {imm}")
    self.ipc()
  def sub(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) - int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x20, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"sub x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def mul(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) * int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x01, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"mul x{rd}, x{rs1}, x{rs1}")
    self.ipc()
  def xor(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) ^ int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x4, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"xor x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def xori(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1] ^ imm) # type: ignore
    inst = self.__encode_i(imm, rs1, 0x4, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"xori x{rd}, x{rs1}, {imm}")
    self.ipc()
  def sll(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val << sh) & 0xffffffff
    inst = self.__encode_r(0x00, rs2, rs1, 0x1, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"sll x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def srl(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_r(0x00, rs2, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"srl x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def sra(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    if val & 0x80000000: val -= 0x10000000
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_r(0x20, rs2, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"sra x{rd}, x{rs1}, x{rs2}")
    self.ipc()
  def slli(self, rd:int, rs1:int, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val << sh) & 0xffffffff
    inst = self.__encode_i_shift(0x00, sh, rs1, 0x1, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"slli x{rd}, x{rs1}, {sh}")
    self.ipc()
  def srli(self, rd:int, rs1, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_i_shift(0x00, sh, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"srli x{rd}, x{rs1}, {sh}")
    self.ipc()
  def srai(self, rd:int, rs1:int, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    if val & 0x80000000: val -= 0x10000000
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_i_shift(0x20, sh, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__inst.append(inst)
    self.__lines.append(f"srai x{rd}, x{rs1}, {sh}")
    self.ipc()
  def regmap(self):
    txt = ""
    for index, value in enumerate(self.regs):
      if index == len(self.regs)-1: txt += f"x{index} = {hex(value)}"
      else: txt += f"x{index} = {hex(value)}\n"
    return txt
  def asm(self, output:bool=False):
    txt = ""
    for line in self.__lines: txt += line+"\n"
    if output:
      with open("a.asm", "a") as file: file.write(txt)
    return txt
  def clean(self):
    for index in range(1,len(self.regs)): self.regs[index] = 0
    self.pc = 0
  def __encode_r(self, funct7, rs2, rs1, funct3, rd, opcode=0x33):
    inst = ((funct7 & 0x7f) << 25) | \
           ((rs2 & 0x1f) << 20) | \
           ((rs1 & 0x1f) << 15) | \
           ((funct3 & 0x07) << 12) | \
           ((rd & 0x1f) << 7)  | \
           (opcode & 0x7f)
    return inst
  def __encode_i(self, imm:int, rs1:int, funct3:int, rd:int, opcode:int=0x13):
    imm &= 0xfff
    inst = ((imm & 0xfff) << 20) | \
           ((rs1 & 0x1f)  << 15) | \
           ((funct3 & 0x07) << 12) | \
           ((rd & 0x1f)  << 7)  | \
           (opcode & 0x7f)
    return inst
  def __encode_i_shift(self, funct7, shamt, rs1, funct3, rd, opcode=0x13):
    imm = ((funct7 & 0x7f) << 5) | (shamt & 0x1f)
    inst = ((imm & 0xfff) << 20) | \
        ((rs1 & 0x1f) << 15) | \
        ((funct3 & 0x07) << 12) | \
        ((rd & 0x1f) << 7) | \
        (opcode & 0x7f)
    return inst
  def dump(self, filename:str="a", format="hex", view:bool=False):
    if format not in ["bin", "oct", "hex"]: raise ValueError(f"invalid file format '{format}', expected from 'bin', 'oct', or 'hex'")
    with open(f"{filename}.{format}", "w") as file:
      if format == "hex":
        for inst in self.__inst: file.write(f"{inst}\n")
      elif format == "oct":
        for inst in self.__inst: file.write(f"{oct(int(inst,16))}\n"[2:])
      else:
        for inst in self.__inst: file.write(f"{bin(int(inst,16))}\n"[2:])
    if view:
      txt = ""
      if format == "hex":
        for index, inst in enumerate(self.__inst):
          if index == len(self.__inst)-1: txt += inst
          else: txt += f"{inst}\n"
      elif format == "bin":
        for index, inst in enumerate(self.__inst):
          if index == len(self.__inst)-1: txt +=f"{bin(int(inst,16))}"[2:]
          else: txt += f"{bin(int(inst,16))}"[2:]+"\n"
      elif format == "oct":
        for index, inst in enumerate(self.__inst):
          if index == len(self.__inst)-1: txt += f"{oct(int(inst,16))}"[2:]
          else: txt += f"{oct(int(inst,16))}"[2:]+"\n"
      print(txt)
