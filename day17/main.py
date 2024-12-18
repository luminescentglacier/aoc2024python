# --- Day 17: Chronospatial Computer ---
import re
from enum import Enum
from pathlib import Path
from typing import Self

import z3

INPUT_FILE = Path(__file__).parent / "input.txt"


class Op(int, Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

    @property
    def is_combo(self) -> bool:
        return self in (Op.adv, Op.bst, Op.out, Op.bdv, Op.cdv)


class Computer:
    def __init__(self, a: int, b: int, c: int, program: list[int]) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.inst: Op = None
        self.operand: int = None
        self.program = program
        self.instruction_pointer = 0
        self.stdout = []
        self.call_order = []

    @classmethod
    def from_string(cls, s: str) -> Self:
        registers, program = s.split("\n\n")
        a, b, c = map(int, re.findall(r"\d+", registers))
        _, program = program.split(": ")
        program = list(map(int, program.split(",")))
        return cls(a, b, c, program)

    def adv(self):
        self.a = self.a // (2**self.operand)

    def bxl(self):
        self.b = self.b ^ self.operand

    def bst(self):
        self.b = self.operand % 8

    def jnz(self):
        if self.a == 0:
            return
        self.instruction_pointer = self.operand

    def bxc(self):
        self.b = self.b ^ self.c

    def out(self):
        self.stdout.append(self.operand % 8)

    def bdv(self):
        self.b = self.a // (2**self.operand)

    def cdv(self):
        self.c = self.a // (2**self.operand)

    def step(self):
        self.read_opcode()
        self.read_operand()
        operation = getattr(self, self.inst.name)
        operation()
        self.advance_pointer()

    def advance_pointer(self):
        if self.inst == Op.jnz and self.a != 0:
            return
        self.instruction_pointer += 2

    def read_opcode(self):
        try:
            self.inst = Op(self.program[self.instruction_pointer])
        except IndexError:
            raise RuntimeError("HALT") from None

    def read_operand(self):
        value = self.program[self.instruction_pointer + 1]

        if not self.inst.is_combo or 0 <= value <= 3:
            self.call_order.append((self.inst, value, self.a, self.b, self.c))
            self.operand = value
            return

        match value:
            case 4:
                self.call_order.append((self.inst, "a", self.a, self.b, self.c))
                self.operand = self.a
            case 5:
                self.call_order.append((self.inst, "b", self.a, self.b, self.c))
                self.operand = self.b
            case 6:
                self.call_order.append((self.inst, "c", self.a, self.b, self.c))
                self.operand = self.c
            case 7 | _:
                assert False

    def run(self):
        while True:
            try:
                self.step()
            except RuntimeError:
                return
            if self.inst == Op.out:
                yield self.stdout[-1]

    def __str__(self):
        return "\n".join(
            [
                f"A: {self.a} | B: {self.b} | C: {self.c}",
                f"{self.inst.name} {self.operand}",
                ",".join(map(str, self.program)),
                " " * (self.instruction_pointer * 2) + "^",
                f"Out: {self.result()}",
            ]
        )

    def result(self):
        return ",".join(map(str, self.stdout))


def part_1(s: str) -> str:
    computer = Computer.from_string(s)
    return ",".join(map(str, computer.run()))


def part_2(s: str) -> int:
    computer = Computer.from_string(s)

    def run_vm(a: int, debug: bool = False) -> list[int]:
        vm = Computer(a=a, b=computer.b, c=computer.c, program=computer.program)
        res = list(vm.run())
        if debug:
            for op, operand, a, b, c in vm.call_order:
                print(op.name, operand)
                if op == Op.out:
                    print()
        return res

    run_vm(computer.a, debug=True)
    # 2,4,1,3,7,5,0,3,1,4,4,7,5,5,3,0
    #       ^ 7     ^ 1            ^ 0
    #       |       |              - this one will loop until A != 0
    #       ^-------+ this two will never be a jump instruction unless A was 0 at start
    #                 because of the offset
    #
    # which means program contains exactly one loop and executes the same operation
    # over and over
    #
    # the loop:
    #     jnz 0
    #     bst a
    #     bxl 3
    #     cdv b
    #     adv 3
    #     bxl 4
    #     bxc 7
    #     out b
    #
    # bst a <- take 3 lowest bits from a, store in b
    #   b = a & 7
    # bxl 3 <- b ^ 011, store in b
    #   b = (a & 7) ^ 3
    # cdv b <- remove lowest b bits from a, store in c
    #   c = a >> ((a & 7) ^ 3)
    # adv 3 <- remove lowest 3 bits from a, store in a
    #   a_new = a >> 3 - red herring, does not matter until next loop
    # bxl 4 <- b ^ 100, store in b
    #   b = ((a & 7) ^ 3) ^ 4
    # bxc 7 <- b ^ c, store in b
    #   b = (((a & 7) ^ 3) ^ 4) ^ (a >> ((a & 7) ^ 3))
    # out b <- b & 7 print last 3 bits of b
    #   out = ((((a & 7) ^ 3) ^ 4) ^ (a >> ((a & 7) ^ 3))) & 7
    #
    # then repeat with a = a >> 3
    #
    # we need 15 outs, which means a will be shifted right for 3 bits 15 times
    # 45 <= A bit count <= 48
    # I give up on finding solution for this without solver though

    s = z3.Solver()
    a = z3.BitVec("a", 48)
    for i, out in enumerate(computer.program):
        new_a = z3.LShR(a, i * 3)
        s.add(
            out == ((((new_a & 7) ^ 3) ^ 4) ^ (z3.LShR(new_a, ((new_a & 7) ^ 3)))) & 7
        )
    results = []
    while s.check() == z3.sat:
        s.model()
        res = s.model()[a].as_long()
        assert run_vm(res) == computer.program
        results.append(res)
        s.add(z3.Or(a != s.model()[a]))
    return min(results)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
