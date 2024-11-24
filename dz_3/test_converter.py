import unittest
import tempfile
import os
from config_to_xml import ConfigParser


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        # Инициализация парсера перед каждым тестом
        self.parser = ConfigParser()

    def test_simple_variables(self):
        """Тест на корректное парсинг простых переменных."""
        input_data = """
        name is "John Doe"
        age is 30
        """
        self.parser.parse(input_data)
        self.assertEqual(self.parser.variables['name'], "John Doe")
        self.assertEqual(self.parser.variables['age'], 30)

    def test_arrays(self):
        """Тест на корректное парсинг массивов."""
        input_data = """
        fruits is #("apple", "banana", "cherry")
        numbers is #(1, 2, 3)
        """
        self.parser.parse(input_data)
        self.assertEqual(self.parser.variables['fruits'], ["apple", "banana", "cherry"])
        self.assertEqual(self.parser.variables['numbers'], [1, 2, 3])

    def test_expressions(self):
        """Тест на вычисление выражений."""
        input_data = """
        a is 5
        b is 10
        result is ![a + b]
        """
        self.parser.parse(input_data)
        self.assertEqual(self.parser.variables['result'], 15)

    def test_string_concatenation(self):
        """Тест на конкатенацию строк."""
        input_data = """
        part1 is "Hello"
        part2 is "World"
        message is ![part1 + " " + part2]
        """
        self.parser.parse(input_data)
        self.assertEqual(self.parser.variables['message'], "Hello World")

    def test_invalid_syntax(self):
        """Тест на некорректный синтаксис."""
        input_data = """
        invalid is #(1, "string", )
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(input_data)

    def test_to_xml(self):
        """Тест на преобразование конфигурации в XML."""
        input_data = """
        name is "Test User"
        roles is #("admin", "user")
        """
        self.parser.parse(input_data)
        xml_output = self.parser.to_xml()
        expected_output = """<?xml version="1.0" ?>
<config>
    <variable name="name">Test User</variable>
    <variable name="roles">
        <array>
            <item>admin</item>
            <item>user</item>
        </array>
    </variable>
</config>
"""
        self.assertEqual(xml_output.strip(), expected_output.strip())

    def test_domain_configurations(self):
        """Примеры из разных предметных областей."""

        # Пример 1: Конфигурация для управления пользователями
        input_data1 = """
        admin is "root"
        users is #("user1", "user2", "user3")
        max_users is ![len(users)]
        """
        self.parser.parse(input_data1)
        self.assertEqual(self.parser.variables['admin'], "root")
        self.assertEqual(self.parser.variables['users'], ["user1", "user2", "user3"])
        self.assertEqual(self.parser.variables['max_users'], 3)

        # Пример 2: Конфигурация для электронной коммерции
        input_data2 = """
        product is "Laptop"
        price is 1000
        discount is 10
        final_price is ![price - (price * discount / 100)]
        """
        self.parser.parse(input_data2)
        self.assertEqual(self.parser.variables['product'], "Laptop")
        self.assertEqual(self.parser.variables['price'], 1000)
        self.assertEqual(self.parser.variables['discount'], 10)
        self.assertAlmostEqual(self.parser.variables['final_price'], 900)

    def test_error_handling(self):
        """Тесты на обработку ошибок."""
        # Использование несуществующей переменной
        input_data = """
        result is ![unknown_var + 1]
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(input_data)

        # Некорректный массив
        input_data = """
        array is #(1, "string", )
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(input_data)
