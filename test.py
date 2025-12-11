from tinyriscv import RISCV

riscv = RISCV()
# riscv.regs[0] = 12 # this will cause the error
riscv.addi(1, 2, -12)
riscv.addi(2, 3, 3)
riscv.sub(3, 2, 1)
riscv.asm()
print(riscv.sign_extend(riscv.regs[3], 32))
print(riscv.regs[3])
print(riscv.regmap())

#print(riscv.asm(output=True))
