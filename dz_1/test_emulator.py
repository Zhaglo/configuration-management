import unittest
import os
import shutil
import calendar
from datetime import datetime
from emulator import Emulator

class TestEmulatorCommands(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Копируем тестовый архив и создаем конфигурацию для тестов
        shutil.copy("virtual_fs.zip", "test_virtual_fs.zip")
        with open("config_test.csv", "w") as config:
            config.write("username,testuser\n")
            config.write("hostname,localhost\n")
            config.write("start,start.txt\n")
            config.write("zip_path,test_virtual_fs.zip\n")
            config.write("log_path,log_test.json\n")

    def setUp(self):
        # Создаем экземпляр эмулятора перед каждым тестом
        self.emulator = Emulator("config_test.csv")

    def tearDown(self):
        # Удаляем журнал после каждого теста
        if os.path.exists("log_test.json"):
            os.remove("log_test.json")
        # Закрываем файловую систему эмулятора
        self.emulator.close_filesystem()

    @classmethod
    def tearDownClass(cls):
        # Удаляем конфигурационный файл и архив после всех тестов
        if os.path.exists("config_test.csv"):
            os.remove("config_test.csv")
        if os.path.exists("test_virtual_fs.zip"):
            os.remove("test_virtual_fs.zip")

    def test_echo(self):
        # Проверка стандартного вывода команды echo
        result = self.emulator.echo(["echo", "Hello, World!"])
        expected = "Hello, World!"
        self.assertEqual(result, expected)

    def test_echo_no_newline(self):
        # Проверка вывода команды echo с опцией -n
        result = self.emulator.echo(["echo", "-n", "No newline"])
        expected = "No newline"
        self.assertEqual(result, expected)

    def test_echo_with_escape(self):
        # Проверка вывода команды echo с опцией -e для интерпретации escape-последовательностей
        result = self.emulator.echo(["echo", "-e", "Line1\\nLine2\\tTabbed"])
        expected = "Line1\nLine2\tTabbed"
        self.assertEqual(result, expected)

    # def test_echo_write_file(self):
    #     # Проверка записи в файл
    #     self.emulator.echo(["echo", "Line1", ">", "testfile.txt"])
    #     self.emulator.echo(["echo", "Line2", ">>", "testfile.txt"])
    #     with zipfile.ZipFile('test_virtual_fs.zip', 'r') as zip_ref:
    #         with zip_ref.open('testfile.txt') as file:
    #             content = file.read().decode('utf-8')
    #             expected = "Line1\nLine2\n"
    #             self.assertEqual(content, expected)

    def test_chmod_success(self):
        # Предположим, что файл testfile.txt существует в архиве
        self.emulator.echo(["echo", "This is a test file.", ">", "testfile.txt"])  # Создаем файл для теста
        result = self.emulator.chmod("u+x", "testfile.txt")
        expected = "Permissions for testfile.txt set to u+x"
        self.assertEqual(result, expected)

    def test_chmod_invalid_file(self):
        # Проверка обработки несуществующего файла
        result = self.emulator.chmod("u+x", "non_existent_file.txt")
        expected = "File non_existent_file.txt does not exist"
        self.assertEqual(result, expected)

    def test_chmod_invalid_permission(self):
        # Проверка обработки недопустимого формата разрешений
        self.emulator.echo(["echo", "This is a test file.", ">", "testfile.txt"])  # Создаем файл для теста
        result = self.emulator.chmod("invalid_permission", "testfile.txt")
        expected = "Invalid permission: use format u+x, g-w, o=r"
        self.assertEqual(result, expected)

    def test_cal_current_month(self):
        result = self.emulator.cal()
        expected = calendar.month(datetime.now().year, datetime.now().month)
        self.assertEqual(result.strip(), expected.strip())

    def test_cal_specific_year(self):
        result = self.emulator.cal("12")
        expected = calendar.calendar(12)
        self.assertEqual(result.strip(), expected.strip())

    def test_cal_invalid_month(self):
        result = self.emulator.cal("invalid_month")
        expected = "Invalid input: invalid literal for int() with base 10: 'invalid_month'"
        self.assertIn("Invalid input", result)

if __name__ == "__main__":
    unittest.main()
