import sys
import csv

def interpret(binary_file, memory_dump_file, memory_start, memory_end):
    memory = {}
    stack = []
    with open(binary_file, 'rb') as f:
        code = f.read()

    pc = 0  # Program counter
    while pc < len(code):
        # Read 5 bytes instruction
        if pc + 5 > len(code):
            print(f"Error: Not enough bytes to read instruction at address {pc}")
            sys.exit(1)
        instr_bytes = code[pc:pc+5]
        instr = int.from_bytes(instr_bytes, byteorder='little', signed=False)
        opcode = instr & 0x7F  # Bits 0-6

        if opcode == 87:  # PUSH_CONST
            B = (instr >> 7) & ((1 << 28) - 1)  # Bits 7-34
            # Convert B from two's complement if necessary
            if B >= (1 << 27):
                B -= 1 << 28
            stack.append(B)
            pc += 5
        elif opcode == 81:  # LOAD_MEM
            B = (instr >> 7) & ((1 << 14) - 1)  # Bits 7-20
            if not stack:
                print("Error: Stack is empty during LOAD_MEM")
                sys.exit(1)
            addr = stack[-1] + B
            value = memory.get(addr, 0)
            stack.append(value)
            pc += 5
        elif opcode == 25:  # STORE_MEM
            B = (instr >> 7) & ((1 << 13) - 1)  # Bits 7-19
            if not stack:
                print("Error: Stack is empty during STORE_MEM")
                sys.exit(1)
            value = stack.pop()
            memory[B] = value
            pc += 5
        elif opcode == 9:  # SGN_OP
            B = (instr >> 7) & ((1 << 14) - 1)  # Bits 7-20
            C = (instr >> 21) & ((1 << 13) - 1)  # Bits 21-33
            if not stack:
                print("Error: Stack is empty during SGN_OP")
                sys.exit(1)
            addr = stack.pop() + B
            value = memory.get(addr, 0)
            if value > 0:
                result = 1
            elif value < 0:
                result = -1
            else:
                result = 0
            memory[C] = result
            pc += 5
        else:
            print(f"Unknown opcode: {opcode} at address {pc}")
            sys.exit(1)

    # Save the memory dump
    with open(memory_dump_file, 'w', newline='') as f_mem:
        mem_writer = csv.writer(f_mem)
        for addr in range(int(memory_start), int(memory_end)+1):
            mem_writer.writerow([addr, memory.get(addr, 0)])

if __name__ == "__main__":
        if len(sys.argv) != 5:
            print("Usage: python interpreter.py <binary_file> <memory_dump_file> <memory_start> <memory_end>")
            sys.exit(1)
        interpret(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
