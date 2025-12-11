from tinyriscv import RISCV

riscv = RISCV()
# riscv.regs[0] = 12 # this will cause the error
riscv.addi(1, 2, -1) # -> 0 + (-1)
riscv.addi(2, 3, 2)  # -> 0 + 2
riscv.add(3, 1, 2)   # -> -1 + 2
riscv.mul(4, 2, 3)   # -> 2 * 1
print(riscv.regmap())
#print(riscv.asm(output=True))
