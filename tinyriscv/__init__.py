from tinyriscv import dtypes
from tinyriscv.array import array
from tinyriscv.regs import RegFile

class RISCV:
  def __init__(self, memory:int=1024): # memory size of 1MB
    self.memory = array.zeros(memory, dtypes.uint8)
    self.regs = RegFile()
    self.pc = 0
    self.halted = False # for sim
    self.__lines = []
    self.__inst = []
  @property
  def inst(self): return self.__inst
  def __ipc(self): self.pc += 4
  def add(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) + int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"add x{rd}, x{rs1}, x{rs1}")
    self.__ipc()
  def addi(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1]) + imm # type: ignore
    inst = self.__encode_i(imm, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"addi x{rd}, x{rs1}, {hex(imm)}")
    self.__ipc()
  def sub(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) - int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x20, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"sub x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def mul(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) * int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x01, rs2, rs1, 0x0, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"mul x{rd}, x{rs1}, x{rs1}")
    self.__ipc()
  def and_(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) & int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x7, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"and x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def andi(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1]) & imm # type: ignore
    inst = self.__encode_i(imm, rs1, 0x7, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"andi x{rd}, x{rs1}, {imm}")
    self.__ipc()
  def or_(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) | int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x6, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"or x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def ori(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1]) | imm # type: ignore
    inst = self.__encode_i(imm, rs1, 0x6, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"ori x{rd}, x{rs1}, {imm}")
    self.__ipc()
  def xor(self, rd:int, rs1:int, rs2:int):
    self.regs[rd] = int(self.regs[rs1]) ^ int(self.regs[rs2]) # type: ignore
    inst = self.__encode_r(0x00, rs2, rs1, 0x4, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"xor x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def xori(self, rd:int, rs1:int, imm:int):
    self.regs[rd] = int(self.regs[rs1] ^ imm) # type: ignore
    inst = self.__encode_i(imm, rs1, 0x4, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"xori x{rd}, x{rs1}, {hex(imm)}")
    self.__ipc()
  def sll(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val << sh) & 0xffffffff
    inst = self.__encode_r(0x00, rs2, rs1, 0x1, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"sll x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def srl(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_r(0x00, rs2, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"srl x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def sra(self, rd:int, rs1:int, rs2:int):
    sh = int(self.regs[rs2]) & 0x1f # type: ignore
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    if val & 0x80000000: val -= 0x100000000
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_r(0x20, rs2, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"sra x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def slli(self, rd:int, rs1:int, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val << sh) & 0xffffffff
    inst = self.__encode_i_shift(0x00, sh, rs1, 0x1, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"slli x{rd}, x{rs1}, {hex(sh)}")
    self.__ipc()
  def srli(self, rd:int, rs1, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_i_shift(0x00, sh, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"srli x{rd}, x{rs1}, {hex(sh)}")
    self.__ipc()
  def srai(self, rd:int, rs1:int, shamt:int):
    sh = shamt & 0x1f
    val = int(self.regs[rs1]) & 0xffffffff # type: ignore
    if val & 0x80000000: val -= 0x100000000
    self.regs[rd] = (val >> sh) & 0xffffffff
    inst = self.__encode_i_shift(0x20, sh, rs1, 0x5, rd).to_bytes(4, byteorder="big").hex()
    self.__store_inst(int(inst,16))
    self.__inst.append(inst)
    self.__lines.append(f"srai x{rd}, x{rs1}, {hex(sh)}")
    self.__ipc()
  def slt(self, rd:int, rs1:int, rs2:int):
    v1 = int(self.regs[rs1]) & 0xffffffff # type: ignore
    v2 = int(self.regs[rs2]) & 0xffffffff # type: ignore
    if v1 & 0x80000000: v1 -= 0x100000000
    if v2 & 0x80000000: v2 -= 0x100000000
    self.regs[rd] = 1 if v1 < v2 else 0
    inst = self.__encode_r(0x00, rs2, rs1, 0x2, rd)
    self.__store_inst(inst)
    self.__inst.append(f"{inst:08X}")
    self.__lines.append(f"slt x{rd}, x{rs1}, x{rs2}")
    self.__ipc()
  def slti(self, rd:int, rs1:int, imm:int):
    imm &= 0xfff
    if imm & 0x800: imm -= 0x1000
    self.regs[rd] = 1 if int(self.regs[rs1]) < imm else 0 # type: ignore
    inst = self.__encode_i(imm, rs1, 0x2, rd)
    self.__store_inst(inst)
    self.__inst.append(f"{inst:08X}")
    self.__lines.append(f"slti x{rd}, {hex(imm)}")
    self.__ipc()
  def sltiu(self, rd:int, rs1:int, imm:int):
    imm &= 0xfff
    self.regs[rd] = 1 if (int(self.regs[rs1]) & 0xffffffff) < imm else 0 # type: ignore
    inst = self.__encode_i(imm, rs1, 0x3, rd)
    self.__store_inst(inst)
    self.__inst.append(f"{inst:08X}")
    self.__lines.append(f"sltiu x{rd}, x{rs1}, {hex(imm)}")
    self.__ipc()
  def lui(self, rd:int, imm:int):
    imm &= 0xfffff
    self.regs[rd] = (imm << 12) # type: ignore
    inst = self.__encode_u(imm, rd, 0x37)
    self.__store_inst(inst)
    self.__inst.append(f"{inst:08X}")
    self.__lines.append(f"lui x{rd}, {hex(imm)}")
    self.__ipc()
  def auipc(self, rd:int, imm:int):
    imm &= 0xfffff
    self.regs[rd] = self.pc + (imm << 12) # type: ignore
    inst = self.__encode_u(imm, rd, 0x17)
    self.__store_inst(inst)
    self.__inst.append(f"{inst:08X}")
    self.__lines.append(f"auipc x{rd}, {hex(imm)}")
    self.__ipc()
  def regmap(self):
    txt = ""
    for index, value in enumerate(self.regs):
      if index == len(self.regs)-1: txt += f"x{index} = {hex(value)}"
      else: txt += f"x{index} = {hex(value)}\n"
    return txt
  def asm(self, filename:str="a.asm", show_addr:bool=True):
    lines = []
    pc = 0
    lines.append("  .section .text")
    lines.append("  .globl _start")
    lines.append("_start:")
    for asm_line, hexinst in zip(self.__lines, self.__inst):
      if show_addr: lines.append(f"  {asm_line:<25} # 0x{pc:08X} : {hexinst}")
      else: lines.append(f"  {asm_line}")
      pc += 4
    txt = "\n".join(lines) + "\n"
    with open(filename, "w") as f: f.write(txt)
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
           ((rs1 & 0x1f) << 15) | \
           ((funct3 & 0x07) << 12) | \
           ((rd & 0x1f) << 7)  | \
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
  def __encode_u(self, imm: int, rd: int, opcode: int):
    imm &= 0xfffff
    inst = ((imm & 0xfffff) << 12) | ((rd & 0x1f) << 7) | (opcode & 0x7f)
    return inst
  def __store_inst(self, inst:int):
    addr = self.pc
    self.memory[addr + 0] = (inst >> 0) & 0xff
    self.memory[addr + 1] = (inst >> 8) & 0xff
    self.memory[addr + 2] = (inst >> 16) & 0xff
    self.memory[addr + 3] = (inst >> 24) & 0xff
  def dump(self, filename:str="a", format="hex", view:bool=False):
    if format not in ["bin", "oct", "hex"]: raise ValueError(f"invalid file format '{format}', expected from 'bin', 'oct', or 'hex'")
    with open(f"{filename}.{format}", "w") as file:
      for inst in self.__inst:
        val = int(inst, 16)
        if format == "hex": file.write(f"{val:08X}\n")
        elif format == "oct": file.write(f"{val:011o}\n")
        else: file.write(f"{val:032b}\n")
    if view:
      txt = ""
      for i, inst in enumerate(self.__inst):
        val = int(inst, 16)
        if format == "hex": s = f"{val:08X}"
        elif format == "oct": s = f"{val:011o}"
        else: s = f"{val:032b}"
        txt += s if i == len(self.__inst) - 1 else s + "\n"
      print(txt)
