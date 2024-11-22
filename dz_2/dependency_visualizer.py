import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
import requests
import os
import subprocess


def download_pom(url):
    """Скачиваем файл pom.xml по указанному URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка загрузки файла pom.xml с URL: {url}")
    return response.text


def parse_pom(pom_content):
    """Парсим содержимое pom.xml и извлекаем зависимости вместе со свойствами."""
    root = ET.fromstring(pom_content)
    ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}  # Пространство имен Maven

    properties = {}
    for prop in root.findall('.//mvn:properties/*', ns):
        properties[prop.tag.split('}')[1]] = prop.text

    dependencies = root.findall('.//mvn:dependency', ns)
    parsed_deps = []

    for dependency in dependencies:
        group_id = dependency.find('mvn:groupId', ns).text
        artifact_id = dependency.find('mvn:artifactId', ns).text
        version_elem = dependency.find('mvn:version', ns)
        version = version_elem.text if version_elem is not None else "unknown"

        if version.startswith('${') and version.endswith('}'):
            version_key = version[2:-1]
            version = properties.get(version_key, "unknown")

        parsed_deps.append((group_id, artifact_id, version))

    return parsed_deps


class MavenDependencyVisualizer:
    def __init__(self, package_name, output_path, repo_url=None):
        self.package_name = package_name
        self.output_path = output_path
        self.repo_url = repo_url or "https://repo1.maven.org/maven2"
        self.dependencies = defaultdict(list)
        self.processed_artifacts = set()

    def get_package_pom_url(self, package_name):
        group_id, artifact_id, version = package_name.split(":")
        url = f"{self.repo_url}/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
        return url

    def process_dependencies(self):
        url = self.get_package_pom_url(self.package_name)
        pom_content = download_pom(url)

        dependencies = parse_pom(pom_content)
        for group_id, artifact_id, version in dependencies:
            dep_key = f"{group_id}:{artifact_id}:{version}"

            if version != "unknown" and dep_key not in self.processed_artifacts:
                self.dependencies[group_id].append((artifact_id, version))
                self.processed_artifacts.add(dep_key)

                transitive_url = (f"{self.repo_url}/{group_id.replace('.', '/')}/"
                                  f"{artifact_id}/{version}/{artifact_id}-{version}.pom")
                try:
                    transitive_pom = download_pom(transitive_url)
                    transitive_deps = parse_pom(transitive_pom)
                    for t_group_id, t_artifact_id, t_version in transitive_deps:
                        if t_version != "unknown":
                            t_dep_key = f"{t_group_id}:{t_artifact_id}:{t_version}"
                            if t_dep_key not in self.processed_artifacts:
                                self.dependencies[group_id].append((t_artifact_id, t_version))
                                self.processed_artifacts.add(t_dep_key)
                except Exception as e:
                    print(f"Не удалось загрузить транзитивные зависимости для {dep_key}: {e}")

    def generate_plantuml_code(self):
        plantuml_lines = ["@startuml"]

        main_package_name = self.package_name.replace(":", "_").replace(".", "_").replace("-", "_")
        plantuml_lines.append(f'node "{main_package_name}" as {main_package_name}')

        for group, deps in self.dependencies.items():
            root_node = group.replace('.', '_').replace('-', '_')
            plantuml_lines.append(f'node "{root_node}" as {root_node}')
            plantuml_lines.append(f'{main_package_name} --> {root_node}')

            for artifact, version in deps:
                artifact = artifact.strip().replace(" ", "_").replace(".", "_").replace("-", "_").replace("\n", "")
                version = version.strip().replace(" ", "").replace(".", "_").replace("-", "_").replace("\n", "")
                child = f"{artifact}_{version}".replace(":", "_")
                plantuml_lines.append(f'node "{artifact}:{version}" as {child}')
                plantuml_lines.append(f'{root_node} --> {child}')

        plantuml_lines.append("@enduml")
        return "\n".join(plantuml_lines)

    def save_graph(self, plantuml_code):
        """Сохраняем граф в формате .puml и генерируем изображение."""
        puml_path = self.output_path.replace('.png', '.puml').replace('.svg', '.puml')
        with open(puml_path, 'w') as f:
            f.write(plantuml_code)
        print(f"Файл .puml сохранен: {puml_path}")

        # Генерация изображения через консоль
        output_extension = os.path.splitext(self.output_path)[1].lower()
        if output_extension not in {".png", ".svg"}:
            raise ValueError("Выходной файл должен иметь расширение .png или .svg.")

        cmd = [
            "java", "-jar", "plantuml.jar",  # Укажите путь к plantuml.jar
            "-t" + output_extension[1:],  # Определяем формат (png или svg)
            "-o", os.path.dirname(self.output_path),  # Указываем папку для результата
            puml_path  # Указываем файл .puml
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Граф успешно сгенерирован: {self.output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка генерации графа: {e}")

    def run(self):
        print(f"Парсинг пакета {self.package_name}...")
        self.process_dependencies()

        print("Генерация PlantUML-графа...")
        plantuml_code = self.generate_plantuml_code()

        print("Сохранение графа и генерация изображения...")
        self.save_graph(plantuml_code)
        print("Готово!")


def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Maven-пакета.")
    parser.add_argument('--package-name', required=True, help="Имя пакета в формате groupId:artifactId:version.")
    parser.add_argument('--output-path', required=True, help="Путь к файлу для записи результата (в формате SVG или PNG).")
    parser.add_argument('--repo-url', help="URL-адрес Maven-репозитория для загрузки транзитивных зависимостей.",
                        default="https://repo1.maven.org/maven2")

    args = parser.parse_args()

    visualizer = MavenDependencyVisualizer(args.package_name, args.output_path, args.repo_url)
    visualizer.run()


if __name__ == "__main__":
    main()
