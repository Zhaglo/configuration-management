import os
import unittest
from dependency_visualizer import MavenDependencyVisualizer

class TestMavenDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.visualizer = MavenDependencyVisualizer("org.example", "output.png")
        self.temp_files = []  # Список временных файлов для удаления

    def tearDown(self):
        """Очистка после каждого теста."""
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def add_temp_file(self, file_path):
        """Добавление файла в список временных файлов."""
        self.temp_files.append(file_path)

    def test_add_dependency(self):
        """Тест добавления зависимости."""
        self.visualizer.dependencies["org.example"].append(("example-dependency", "1.0"))
        self.assertIn(("example-dependency", "1.0"), self.visualizer.dependencies["org.example"])

    def test_generate_plantuml_code(self):
        """Тест генерации PlantUML-кода."""
        self.visualizer.dependencies["org.example"].append(("example-dependency", "1.0"))
        plantuml_code = self.visualizer.generate_plantuml_code()
        self.assertIn('node "example_dependency:1_0" as example_dependency_1_0', plantuml_code)

    def test_save_graph(self):
        """Тест сохранения графа с проверкой на некорректный формат."""
        plantuml_code = "@startuml\n@enduml"
        self.visualizer.output_path = "test_output.png"
        self.visualizer.save_graph(plantuml_code)

        # Добавление файлов в список для удаления
        self.add_temp_file("test_output.png")
        self.add_temp_file("test_output.puml")

        # Проверяем, что файлы созданы
        self.assertTrue(os.path.exists("test_output.png"))
        self.assertTrue(os.path.exists("test_output.puml"))

        # Проверка обработки некорректного формата
        try:
            self.visualizer.output_path = "output.txt"
            self.visualizer.save_graph(plantuml_code)
        except ValueError:
            # Добавляем некорректный файл в список для удаления, если он был создан
            self.add_temp_file("output.txt")

    def test_handle_transitive_dependencies(self):
        """Тест обработки транзитивных зависимостей."""
        self.visualizer.dependencies["org.example"].append(("example-dependency", "1.0"))
        self.visualizer.dependencies["example-dependency"].append(("transitive-dependency", "1.1"))
        plantuml_code = self.visualizer.generate_plantuml_code()
        self.assertIn('example_dependency --> transitive_dependency_1_1', plantuml_code)

    def test_empty_dependencies(self):
        """Тест обработки пустых зависимостей."""
        plantuml_code = self.visualizer.generate_plantuml_code()
        self.assertEqual(plantuml_code.strip(), '@startuml\nnode "org_example" as org_example\n@enduml')

if __name__ == "__main__":
    unittest.main()
