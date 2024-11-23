# Maven Dependency Visualizer
### Описание
Maven Dependency Visualizer — это инструмент для визуализации зависимостей Maven пакетов в графическом виде. Он генерирует графы в формате PlantUML, которые затем можно преобразовать в изображения (например, в формате PNG или SVG) с помощью библиотеки PlantUML.

Этот проект предоставляет функционал для:

* Генерации кода PlantUML для отображения зависимостей.
* Сохранения графа в формате .puml и генерации соответствующих изображений.
### Требования
Перед использованием инструмента убедитесь, что у вас установлены следующие зависимости:

* Python 3.x
* Java (необходим для генерации изображений с помощью PlantUML)
* PlantUML (необходим для генерации изображений из .puml файлов)

Для работы с проектом рекомендуется создать виртуальное окружение:

~~~bash
python -m venv .venv
source .venv/bin/activate  # для Linux/macOS
.venv\Scripts\activate  # для Windows
~~~
Затем установите все необходимые зависимости:

~~~bash
pip install -r requirements.txt
~~~
### Использование
1. Создание визуализатора зависимостей:

Для создания визуализатора зависимостей необходимо указать имя пакета и путь для сохранения графа:

~~~python
visualizer = MavenDependencyVisualizer(package_name="org.example", output_path="output.png")
~~~
2. Добавление зависимостей:

Зависимости добавляются в словарь зависимостей вручную или через другие методы, и они должны быть доступны в объекте visualizer.dependencies.

3. Генерация кода PlantUML:

Для создания кода PlantUML для визуализации зависимостей используйте метод generate_plantuml_code:

~~~python
plantuml_code = visualizer.generate_plantuml_code()
~~~
4. Сохранение графа и генерация изображения:

Для сохранения графа и генерации изображения вызовите метод save_graph:

~~~python
visualizer.save_graph(plantuml_code)
~~~
Метод автоматически сохранит файл .puml и сгенерирует изображение в формате PNG или SVG в указанной директории.

### Тестирование
Для тестирования функционала в проекте используется модуль unittest. Тесты проверяют добавление зависимостей, корректность генерации PlantUML кода и работу метода сохранения графа.

Для запуска тестов используйте команду:

~~~bash
python -m unittest test_visualizer
~~~
### Пример
Пример использования визуализатора зависимостей:

~~~python
from dependency_visualizer import MavenDependencyVisualizer

# Создание экземпляра визуализатора
visualizer = MavenDependencyVisualizer(package_name="org.example", output_path="output.png")

# Добавление зависимостей вручную в словарь dependencies
visualizer.dependencies["org.example"].append(("example-dependency", "1.0"))
visualizer.dependencies["example-dependency"].append(("transitive-dependency", "1.1"))

# Генерация кода PlantUML
plantuml_code = visualizer.generate_plantuml_code()

# Сохранение графа
visualizer.save_graph(plantuml_code)
~~~