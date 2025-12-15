#!/usr/bin/env python3
import sys

def run_brainfuck(code: str):
    tape = [0] * 30000
    ptr = 0
    pc = 0
    stack = []

    while pc < len(code):
        cmd = code[pc]

        if cmd == '>':
            ptr += 1
            if ptr >= len(tape):
                ptr = 0

        elif cmd == '<':
            ptr -= 1
            if ptr < 0:
                ptr = len(tape) - 1

        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) & 0xFF

        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) & 0xFF

        elif cmd == '.':
            sys.stdout.write(chr(tape[ptr]))
            sys.stdout.flush()

        elif cmd == ',':
            data = sys.stdin.read(1)
            tape[ptr] = ord(data) if data else 0

        elif cmd == '[':
            if tape[ptr] == 0:
                depth = 1
                while depth:
                    pc += 1
                    if pc >= len(code):
                        raise SyntaxError("Unmatched '['")
                    if code[pc] == '[':
                        depth += 1
                    elif code[pc] == ']':
                        depth -= 1
            else:
                stack.append(pc)

        elif cmd == ']':
            if tape[ptr] != 0:
                pc = stack[-1]
            else:
                stack.pop()

        pc += 1


def main():
    code = sys.stdin.read()
    run_brainfuck(code)


if __name__ == "__main__":
    main()
