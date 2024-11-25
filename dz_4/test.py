import subprocess
import os
import csv

def run_test(test_name, asm_code, expected_memory, memory_range):
    asm_file = f"{test_name}.asm"
    bin_file = f"{test_name}.bin"
    log_file = f"{test_name}_log.csv"
    mem_dump_file = f"{test_name}_memory.csv"

    # Запись ассемблерного кода в файл
    with open(asm_file, 'w') as f:
        f.write(asm_code)

    # Запуск ассемблера
    assembler_cmd = ['python', 'assembler.py', asm_file, bin_file, log_file]
    result = subprocess.run(assembler_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при ассемблировании {test_name}:")
        print(result.stdout)
        print(result.stderr)
        return

    # Запуск интерпретатора
    interpreter_cmd = ['python', 'interpreter.py', bin_file, mem_dump_file, str(memory_range[0]), str(memory_range[1])]
    result = subprocess.run(interpreter_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при выполнении {test_name}:")
        print(result.stdout)
        print(result.stderr)
        return

    # Чтение результата из mem_dump_file
    memory = {}
    with open(mem_dump_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            addr, value = int(row[0]), int(row[1])
            memory[addr] = value

    # Проверка ожидаемых значений
    success = True
    for addr in range(memory_range[0], memory_range[1]+1):
        expected_value = expected_memory.get(addr, 0)
        actual_value = memory.get(addr, 0)
        if actual_value != expected_value:
            print(f"Тест {test_name} не пройден: адрес {addr}, ожидается {expected_value}, получено {actual_value}")
            success = False

    if success:
        print(f"Тест {test_name} пройден успешно")

    # Удаление временных файлов
    os.remove(asm_file)
    os.remove(bin_file)
    os.remove(log_file)
    os.remove(mem_dump_file)

# Ассемблерный код для теста vector_sgn
asm_code = """
# Initialize vector at address 200
PUSH_CONST 10
STORE_MEM 200
PUSH_CONST -5
STORE_MEM 201
PUSH_CONST 0
STORE_MEM 202
PUSH_CONST 15
STORE_MEM 203
PUSH_CONST -20
STORE_MEM 204

# sgn() operation on each element
# Element 0
PUSH_CONST 200
SGN_OP 0, 200

# Element 1
PUSH_CONST 200
SGN_OP 1, 201

# Element 2
PUSH_CONST 200
SGN_OP 2, 202

# Element 3
PUSH_CONST 200
SGN_OP 3, 203

# Element 4
PUSH_CONST 200
SGN_OP 4, 204
"""

# Ожидаемые значения в памяти после выполнения программы
expected_memory = {
    200: 1,
    201: -1,
    202: 0,
    203: 1,
    204: -1
}

# Диапазон адресов памяти для проверки
memory_range = (200, 204)

# Запуск теста
run_test("vector_sgn_test", asm_code, expected_memory, memory_range)
