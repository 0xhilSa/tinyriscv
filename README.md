# TinyRISCV

trying to implement the tiny riscv core in python

### TODO
- [ ] Decode instruction and push it into the so called `self.memory`
- [ ] Implement hex and bin output files based on the output assembly
- [ ] Draw graph for visualization
    - [ ] Node having register, address, and value(hex)
    - [ ] Edge indicating which op will be performed

### Install from the source
```bash
git clone https://github.com/0xhilSa/tinyriscv ~/tinyriscv
cd tinyriscv
./compile.sh
pip install -e .
```

### Example
```python
from tinyriscv import RISCV

riscv = RISCV()
riscv.addi(1, 2, 10)
riscv.addi(2, 3, 2)
riscv.sll(3, 1, 2)
riscv.srl(4, 3, 2)
riscv.slli(5, 4, 1)
riscv.srai(6, 5, 1)
riscv.xor(2, 3, 2)
riscv.dump(view=True)
print(riscv.regmap())
```

### Output
```bash
00a10093
00218113
002091b3
0021d233
00121293
4012d313
0021c133
x0 = 0x0
x1 = 0xa
x2 = 0x2a
x3 = 0x28
x4 = 0xa
x5 = 0x14
x6 = 0xa
x7 = 0x0
x8 = 0x0
x9 = 0x0
x10 = 0x0
x11 = 0x0
x12 = 0x0
x13 = 0x0
x14 = 0x0
x15 = 0x0
x16 = 0x0
x17 = 0x0
x18 = 0x0
x19 = 0x0
x20 = 0x0
x21 = 0x0
x22 = 0x0
x23 = 0x0
x24 = 0x0
x25 = 0x0
x26 = 0x0
x27 = 0x0
x28 = 0x0
x29 = 0x0
x30 = 0x0
x31 = 0x0
```
