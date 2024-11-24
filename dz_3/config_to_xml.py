import re
import xml.etree.ElementTree as ET
import argparse
from xml.dom import minidom

# Функция для вычисления выражений
def evaluate_expression(expr, variables):
    expr = expr.strip('![]')  # Убираем "!" и "[]"
    for var in variables:
        # Заменяем переменные в выражении их значениями
        expr = expr.replace(var, str(variables[var]))

    try:
        return eval(expr)
    except Exception as e:
        raise SyntaxError(f"Invalid expression: {expr}, error: {e}")

# Класс для обработки конфигурации
class ConfigParser:
    def __init__(self):
        self.variables = {}

    def parse(self, text):
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            print(f"Parsing line: {line}")  # Для отладки
            if line.startswith('#('):
                self.parse_array(line)
            elif 'is' in line:
                self.parse_assignment(line)
            else:
                raise SyntaxError(f"Invalid statement: {line}")

    def parse_assignment(self, line):
        print(f"Parsing assignment: {line}")  # Для отладки
        var_name, value = line.split(' is ')
        value = value.strip()

        if value.startswith('!['):  # Это выражение
            value = evaluate_expression(value, self.variables)
        elif value.startswith('"') and value.endswith('"'):  # Это строка
            value = value[1:-1]
        elif value.isdigit():  # Это число
            value = int(value)
        elif value.startswith('#('):  # Это массив
            value = self.parse_array(value)  # Массив обрабатываем через метод parse_array
        self.variables[var_name.strip()] = value

    def parse_array(self, line):
        # Убираем "#(" и ")"
        array_values = line[2:-1]
        # Разделяем по запятой и обрабатываем каждый элемент
        elements = [self.parse_value(val.strip()) for val in array_values.split(',')]
        return elements

    def parse_value(self, value):
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