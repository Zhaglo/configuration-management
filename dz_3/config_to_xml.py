import re
import xml.etree.ElementTree as ET
import argparse
from xml.dom import minidom

# Функция для вычисления выражений
def evaluate_expression(expr, variables):
    expr = expr.strip('![]')  # Убираем "!" и "[]"

    # Подставляем значения переменных в выражение
    def replace_variables(token):
        if token in variables:  # Если токен - это переменная
            value = variables[token]
            if isinstance(value, list):  # Преобразуем массивы в строку
                return repr(value)
            elif isinstance(value, str):  # Если это строка, добавляем кавычки
                return f'"{value}"'
            return str(value)  # Возвращаем строковое представление значения
        return token  # Если это не переменная, оставляем как есть

    # Учитываем строки с кавычками и символы
    tokens = re.split(r'("[^"]*"|\W)', expr)  # Учитываем строки в кавычках и разделители
    processed_tokens = [
        replace_variables(token) if not re.match(r'^".*"$', token) else token
        for token in tokens if token.strip()
    ]
    processed_expr = ''.join(processed_tokens)

    try:
        # Указываем безопасные функции, доступные в выражении
        safe_globals = {"__builtins__": None, "len": len, "max": max}
        result = eval(processed_expr, safe_globals, {})
        return result
    except Exception as e:
        raise SyntaxError(f"Invalid expression: {processed_expr}, error: {e}")

# Функция safe_max для безопасного нахождения максимального значения
def safe_max(iterable):
    # Проверяем, есть ли хотя бы один элемент
    if not iterable:
        return None

    # Сортируем элементы, преобразуя их в строки для безопасного сравнения
    try:
        return max(iterable, key=lambda x: str(x))
    except TypeError:
        # В случае ошибки, если элементы несопоставимы, вернем None
        return None


# Класс для обработки конфигурации
class ConfigParser:
    def __init__(self):
        self.variables = {}

    def parse(self, text):
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('#('):
                self.parse_array(line)
            elif 'is' in line:
                self.parse_assignment(line)
            else:
                raise SyntaxError(f"Invalid statement: {line}")

    def parse_assignment(self, line):
        var_name, value = line.split(' is ')
        value = value.strip()

        if value.startswith('!['):  # Это выражение, которое нужно вычислить
            value = evaluate_expression(value, self.variables)
        elif value.startswith('"') and value.endswith('"'):  # Это строка
            value = value[1:-1]  # Убираем кавычки
        elif value.isdigit():  # Это число
            value = int(value)
        elif value.startswith('#('):  # Это массив
            value = self.parse_array(value)  # Массив обрабатываем через метод parse_array
        else:
            # Если это переменная, то берем её значение
            value = self.variables.get(value, value)

        self.variables[var_name.strip()] = value

    def handle_string_concatenation(self, value):
        # Разделяем строку по символу "+" и обрабатываем каждую часть
        parts = value.split('+')
        processed_parts = []
        for part in parts:
            part = part.strip()
            if part.startswith('"') and part.endswith('"'):
                # Если это строка, удаляем кавычки и добавляем
                processed_parts.append(part[1:-1])
            elif part in self.variables:
                # Если это переменная, подставляем ее значение
                processed_parts.append(str(self.variables[part]))
            else:
                raise ValueError(f"Unknown part in concatenation: {part}")

        # Соединяем все части в одну строку
        return ''.join(processed_parts)

    def parse_array(self, line):
        # Убираем "#(" и ")"
        array_values = line[2:-1]
        # Если массив пустой, возвращаем пустой список
        if not array_values.strip():
            return []

        # Разделяем по запятой и обрабатываем каждый элемент
        elements = []
        for val in array_values.split(','):
            val = val.strip()
            if not val:  # Если элемент пустой, выбрасываем исключение
                raise SyntaxError(f"Invalid array syntax: empty element in {line}")
            elements.append(self.parse_value(val))
        return elements

    def parse_value(self, value):
        if not value:
            raise ValueError("Value cannot be empty.")
        # Если это выражение (начинается с ![), то вычисляем
        if value.startswith('!['):
            return evaluate_expression(value, self.variables)
        # Если это строка (начинается и заканчивается кавычками)
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        # Если это число, просто возвращаем его как int
        elif value.isdigit():
            return int(value)
        # Если это массив (начинается с #()), то обрабатываем как массив
        elif value.startswith('#('):
            return self.parse_array(value)
        # Если это переменная, ищем её значение в self.variables
        elif value in self.variables:
            return self.variables[value]
        else:
            raise ValueError(f"Invalid value: {value}")

    def to_xml(self):
        root = ET.Element('config')
        for var_name, value in self.variables.items():
            var_element = ET.Element('variable', name=var_name)

            if isinstance(value, list):  # Если это массив
                array_element = ET.SubElement(var_element, 'array')
                for item in value:
                    item_element = ET.SubElement(array_element, 'item')
                    item_element.text = str(item)
            else:
                var_element.text = str(value)

            root.append(var_element)

        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        return minidom.parseString(xml_str).toprettyxml(indent="    ")


# Основная часть программы
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert config to XML.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output XML file.')  # Добавлен аргумент для вывода
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        text = f.read()

    config_parser = ConfigParser()
    try:
        config_parser.parse(text)
        xml_output = config_parser.to_xml()

        # Записываем результат в файл с отступами
        with open(args.output, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_output)
        print(f"XML output has been written to {args.output}")
    except Exception as e:
        print(f"Error: {e}")