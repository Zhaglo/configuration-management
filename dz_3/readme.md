# Config to XML Converter
Этот проект предназначен для преобразования конфигурационных файлов в формате текстовых выражений в XML. Входной файл может содержать переменные, массивы и вычисления, которые обрабатываются и преобразуются в структурированный XML-формат.

### Функциональность
* Чтение и обработка конфигураций: Процессор конфигурации парсит строки, определяет переменные, массивы и выражения.
* Вычисление выражений: Для вычисления выражений, таких как max(arr), используется безопасная функция safe_max.
* Поддержка массивов: Преобразует массивы значений в соответствующие XML-структуры.
* Безопасность: Для выполнения вычислений используется безопасный механизм (без встроенных функций Python).
### Установка
1. Клонируйте репозиторий:

~~~bash
git clone https://github.com/Zhaglo/configuration-management/tree/master/dz_3
~~~
2. Установите зависимости:

~~~bash
pip install -r requirements.txt
~~~
### Использование
Для запуска программы, используйте команду:

~~~bash
python config_to_xml.py -i <input_file> -o <output_file>
~~~
где:

* <input_file> — путь к входному текстовому файлу с конфигурацией.
* <output_file> — путь для сохранения сгенерированного XML-файла.
### Пример входного файла (input.txt)
~~~plaintext
x is "apple"
y is "banana"
arr is #(x, y)
max is ![max(arr)]
~~~
### Пример выхода (output.xml)
~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <variable name="x">apple</variable>
    <variable name="y">banana</variable>
    <variable name="arr">
        <array>
            <item>apple</item>
            <item>banana</item>
        </array>
    </variable>
    <variable name="max">banana</variable>
</config>
~~~
### Структура кода
#### Основные компоненты:
* evaluate_expression — Функция для вычисления выражений, таких как max(arr), с использованием безопасной функции safe_max.
* ConfigParser — Класс для парсинга входных данных, обработки выражений, переменных и массивов, а также преобразования данных в формат XML.
* safe_max — Функция для безопасного нахождения максимального значения в массиве, игнорируя несоответствующие типы данных.
* to_xml — Метод для преобразования парсенных данных в XML-формат с отступами.
### Пример работы программы
#### Пример использования:

1. Входной файл (input.txt):

~~~plaintext
x is "apple"
y is "banana"
arr is #(x, y)
max is ![max(arr)]
~~~
2. Команда для конвертации в XML:

~~~bash
python config_to_xml.py -i input.txt -o output.xml
~~~
3. Результат в output.xml:

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <variable name="x">apple</variable>
    <variable name="y">banana</variable>
    <variable name="arr">
        <array>
            <item>apple</item>
            <item>banana</item>
        </array>
    </variable>
    <variable name="max">banana</variable>
</config>
~~~
### Обработка ошибок
* Если в процессе парсинга или вычислений возникнут ошибки (например, неправильный синтаксис или неопределенная переменная), программа выбросит исключение с детализированным сообщением.
### Требования
* Python 3.6 или выше
* Библиотеки: re, xml.etree.ElementTree, xml.dom.minidom, argparse