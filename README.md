<img src="./docs/tinyriscv.png" alt="tinyriscv.png">

# TinyRISCV

trying to implement the tiny riscv core in python

### TODO
- [X] Encode instruction and push it into the so called `self.memory`
- [X] Implement hex, oct and bin output files
- [ ] Draw graph for visualization
- [ ] Generate the assembly full fledged assembly code
- [ ] Include all the I, R, J type instruction

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
riscv.addi(1, 1, 2)
riscv.addi(2, 2, 5)
riscv.add(3, 1, 2)
riscv.sll(4, 3, 2)
riscv.xor(5, 4, 3)
riscv.asm()
print(riscv.regmap())
```

### Output
```bash
00208093
00510113
002081B3
00219233
003242B3
x0 = 0x0
x1 = 0x2
x2 = 0x5
x3 = 0x7
x4 = 0xe0
x5 = 0xe7
x6 = 0x0
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
