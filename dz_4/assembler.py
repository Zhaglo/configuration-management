import sys
import csv

def assemble(input_file, output_file, log_file):
    instructions = []
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Skip comments and empty lines
        # Remove comments from the line
        line = line.split('#')[0].strip()
        if not line:
            continue

        parts = line.split(None, 1)
        mnemonic = parts[0]
        operands_str = parts[1] if len(parts) > 1 else ''
        operands = [operand.strip() for operand in operands_str.split(',')]

        try:
            if mnemonic == 'PUSH_CONST':
                if len(operands) != 1:
                    raise ValueError("Expected 1 operand")
                A = 87  # Opcode for PUSH_CONST
                B = int(operands[0])
                # Check that B fits in 28 bits (signed)
                if B < -(1 << 27) or B > (1 << 27) - 1:
                    raise ValueError(f"Constant {B} out of range for 28-bit signed integer")
                # Convert B to unsigned 28-bit two's complement
                B_unsigned = B & ((1 << 28) - 1)
                instr = (B_unsigned << 7) | (A & 0x7F)
                instructions.append(('PUSH_CONST', A, B, instr))

            elif mnemonic == 'LOAD_MEM':
                if len(operands) != 1:
                    raise ValueError("Expected 1 operand")
                A = 81  # Opcode for LOAD_MEM
                B = int(operands[0])
                # Check that B fits in 14 bits (unsigned)
                if B < 0 or B > (1 << 14) - 1:
                    raise ValueError(f"Offset {B} out of range for 14-bit unsigned integer")
                instr = (B << 7) | (A & 0x7F)
                instructions.append(('LOAD_MEM', A, B, instr))

            elif mnemonic == 'STORE_MEM':
                if len(operands) != 1:
                    raise ValueError("Expected 1 operand")
                A = 25  # Opcode for STORE_MEM
                B = int(operands[0])
                # Check that B fits in 13 bits (unsigned)
                if B < 0 or B > (1 << 13) - 1:
                    raise ValueError(f"Address {B} out of range for 13-bit unsigned integer")
                instr = (B << 7) | (A & 0x7F)
                instructions.append(('STORE_MEM', A, B, instr))

            elif mnemonic == 'SGN_OP':
                if len(operands) != 2:
                    raise ValueError("Expected 2 operands")
                A = 9  # Opcode for SGN_OP
                B = int(operands[0])
                C = int(operands[1])
                # Check that B fits in 14 bits (unsigned) and C in 13 bits (unsigned)
                if B < 0 or B > (1 << 14) - 1:
                    raise ValueError(f"Offset {B} out of range for 14-bit unsigned integer")
                if C < 0 or C > (1 << 13) - 1:
                    raise ValueError(f"Address {C} out of range for 13-bit unsigned integer")
                instr = (C << 21) | (B << 7) | (A & 0x7F)
                instructions.append(('SGN_OP', A, B, C, instr))

            else:
                raise ValueError(f"Unknown instruction: {mnemonic}")
        except ValueError as ve:
            print(f"Error on line {line_num}: {ve}")
            sys.exit(1)

    # Write to binary file
    with open(output_file, 'wb') as f_bin, open(log_file, 'w', newline='') as f_log:
        log_writer = csv.writer(f_log)
        for instr in instructions:
            if instr[0] == 'PUSH_CONST':
                _, A, B_original, code = instr
                f_bin.write(code.to_bytes(5, byteorder='little', signed=False))
                log_writer.writerow([f'opcode={A}', f'B={B_original}'])
            elif instr[0] == 'LOAD_MEM':
                _, A, B, code = instr
                f_bin.write(code.to_bytes(5, byteorder='little', signed=False))
                log_writer.writerow([f'opcode={A}', f'B={B}'])
            elif instr[0] == 'STORE_MEM':
                _, A, B, code = instr
                f_bin.write(code.to_bytes(5, byteorder='little', signed=False))
                log_writer.writerow([f'opcode={A}', f'B={B}'])
            elif instr[0] == 'SGN_OP':
                _, A, B, C, code = instr
                f_bin.write(code.to_bytes(5, byteorder='little', signed=False))
                log_writer.writerow([f'opcode={A}', f'B={B}', f'C={C}'])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
