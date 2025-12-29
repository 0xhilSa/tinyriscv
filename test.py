from tinyriscv import RISCV

riscv = RISCV()
riscv.addi(1, 1, 2)
riscv.addi(2, 2, 5)
riscv.add(3, 1, 2)
riscv.sll(4, 3, 2)
riscv.xor(5, 4, 3)
riscv.asm()
riscv.dump(view=True)
print(riscv.regmap())
