# Инициализация вектора по адресу 200
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

# Элемент 0
PUSH_CONST 200      # Адрес базового элемента
SGN_OP 0, 200       # Смещение 0, результат в 200

# Элемент 1
PUSH_CONST 200
SGN_OP 1, 201       # Смещение 1, результат в 201

# Элемент 2
PUSH_CONST 200
SGN_OP 2, 202       # Смещение 2, результат в 202

# Элемент 3
PUSH_CONST 200
SGN_OP 3, 203       # Смещение 3, результат в 203

# Элемент 4
PUSH_CONST 200
SGN_OP 4, 204       # Смещение 4, результат в 204
