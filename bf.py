# Simple Brainfuck interpreter (8-bit cells)

import sys

code = sys.stdin.read()
tape = [0] * 30000
ptr = 0
pc = 0
stack = []

while pc < len(code):
    c = code[pc]

    if c == '>':
        ptr += 1
    elif c == '<':
        ptr -= 1
    elif c == '+':
        tape[ptr] = (tape[ptr] + 1) & 0xFF
    elif c == '-':
        tape[ptr] = (tape[ptr] - 1) & 0xFF
    elif c == '.':
        sys.stdout.buffer.write(bytes([tape[ptr]]))
    elif c == '[':
        if tape[ptr] == 0:
            depth = 1
            while depth:
                pc += 1
                if code[pc] == '[':
                    depth += 1
                elif code[pc] == ']':
                    depth -= 1
        else:
            stack.append(pc)
    elif c == ']':
        if tape[ptr] != 0:
            pc = stack[-1]
        else:
            stack.pop()

    pc += 1
