"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
ST = 0b10000100
PRN = 0b01000111

MUL = 0b10100010
ADD = 0b10100000

POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8
        self.reg[7] = 0xF4
        self.ram = [0]*256
        self.PC = 0

        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[ST] = self.st
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[ADD] = self.add
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret

    def hlt(self):
        exit()

    def ldi(self):
        self.reg[self.ram_read(self.PC+1)] = self.ram_read(self.PC+2)
        self.PC += 2    

    def st(self):
        self.ram_write(
            self.reg[self.ram_read(self.PC+1)],
            self.reg[self.ram_read(self.PC+2)]
        )
        self.PC += 2

    def prn(self):
        print(self.reg[self.ram_read(self.PC+1)])
        self.PC += 1

    def mul(self):
        self.reg[self.ram_read(self.PC+1)] *= self.reg[self.ram_read(self.PC+2)]
        self.PC += 2

    def add(self):
        self.reg[self.ram_read(self.PC+1)] += self.reg[self.ram_read(self.PC+2)]
        self.PC += 2

    def pop(self):
        self.reg[self.ram_read(self.PC+1)] = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.PC += 1

    def push(self):
        self.reg[7] -= 1
        self.ram_write(
            self.reg[self.ram_read(self.PC+1)],
            self.reg[7]
        )
        self.PC += 1

    def call(self):
        # push address of next instruction to stack
        self.reg[7] -= 1
        self.ram_write(
            self.PC+2,
            self.reg[7]
        )
        # jump to the address at the given register
        self.PC = self.reg[self.ram_read(self.PC+1)]

    def ret(self):
        self.PC = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:

            ir = self.ram_read(self.PC)

            self.branchtable[ir]()

            if ir not in {CALL, RET}:
                self.PC += 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
