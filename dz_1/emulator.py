import sys
import zipfile
import os
import shlex
import csv
from datetime import datetime
import calendar
import json
import stat
import tempfile
import time

class Emulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.currentpath = ""
        self.user = self.config['username']
        self.host = self.config['hostname']
        self.start_script = self.config['start']
        self.filesystem = zipfile.ZipFile(self.config['zip_path'].strip())
        self.filesystemlist = self.filesystem.filelist
        self.logfile = self.config['log_path']
        # Очищаем log.json в начале нового сеанса
        with open(self.logfile, 'w') as logfile:
            logfile.write('')  # Очищаем файл перед новым сеансом
        self.run_script()  # Вызов скрипта сразу после инициализации

    def load_config(self, config_path):
        config = {}
        with open(config_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Убедимся, что у нас есть пара (ключ, значение)
                    config[row[0]] = row[1]
        return config

    def log_command(self, command, result):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.user,
            "command": command,
            "result": result if result is not None else "No output"
        }
        # Загружаем существующие логи или создаем новый массив логов
        logs = []
        if os.path.exists(self.logfile):
            with open(self.logfile, 'r') as logfile:
                try:
                    logs = json.load(logfile)
                except json.JSONDecodeError:
                    logs = []
        # Добавляем новый лог
        logs.append(log_entry)
        # Перезаписываем файл с обновленным массивом
        with open(self.logfile, 'w') as logfile:
            json.dump(logs, logfile, indent=4, ensure_ascii=False)

    def start(self):
        while True:
            try:
                cmd = input(f'{self.user}@{self.host}:{self.currentpath}$ ').split(" ")
                result = None
                if cmd[0].lower() == "ls":
                    result = self.ls(cmd[1] if len(cmd) > 1 else "")
                elif cmd[0].lower() == "cd":
                    result = self.cd(cmd[1] if len(cmd) > 1 else "")
                elif cmd[0].lower() == "chmod":
                    if len(cmd) >= 3:
                        result = self.chmod(cmd[1], cmd[2])
                    else:
                        result = "Usage: chmod <mode> <filename>"
                        print(result)
                elif cmd[0].lower() == "echo":
                    with zipfile.ZipFile(self.config['zip_path'], 'a') as zf:
                        result = self.echo(cmd, zf)  # Передаем срез, чтобы избежать лишних аргументов
                elif cmd[0].lower() == "cal":
                    if len(cmd) == 1:
                        result = self.cal()
                    elif len(cmd) == 2:
                        result = self.cal(cmd[1])  # Передаем только месяц
                    elif len(cmd) == 3:
                        result = self.cal(cmd[1], cmd[2])  # Передаем месяц и год
                    else:
                        result = "Usage: cal [month] [year]"
                        print(result)
                elif cmd[0].lower() == "exit":
                    break
                else:
                    result = 'Unknown command.'
                    print(result)
                self.log_command(' '.join(cmd), result)
            except Exception as e:
                print(f'Some error: {e}')
            finally:
                self.close_filesystem()

    def ls(self, newpath: str):
        path = self.currentpath
        if "/root" in newpath:
            path = newpath.replace('/root/', '')
        elif newpath in ("~", "/"):
            path = ""
        else:
            path = self.currentpath + "/" + newpath if not newpath.startswith("/") else newpath
        if path != "":
            path = path.lstrip("/")
        # Проверка существования директории
        flag = any(path in file.filename for file in self.filesystemlist)
        if not flag:
            result = f'Directory "{newpath}" does not exist.'
            print(result)
            return result
        displayed_files = set()  # Множество для отслеживания уникальных имен
        output = []
        for file in self.filesystemlist:
            if path in file.filename:
                files = file.filename[len(path):].split("/")
                files = list(filter(None, files))
                if len(files) > 1 or not files:
                    continue
                if files[0] not in displayed_files:
                    output.append(files[0])
                    displayed_files.add(files[0])
        print("\n".join(output))
        return "\n".join(output)

    def cd(self, newpath: str):
        if "/root" in newpath:
            newpath = newpath.replace('/root/', '')
            if any(file.filename == newpath + "/" or file.filename.startswith(newpath + "/") for file in
                   self.filesystemlist):
                self.currentpath = "/" + newpath
            else:
                result = f'Directory "{newpath}" does not exist.'
                print(result)
                return result
        elif newpath == "..":
            self.currentpath = '/'.join(self.currentpath.split('/')[:-1]) or "/"
        elif newpath in ("~", "/"):
            self.currentpath = ""
        elif newpath:
            new_path = self.currentpath + "/" + newpath if not newpath.startswith("/") else newpath
            new_path = new_path.strip("/")
            # Проверяем, что новая директория существует в точности
            if any(file.filename == new_path + "/" or file.filename.startswith(new_path + "/") for file in
                   self.filesystemlist):
                self.currentpath = "/" + new_path
            else:
                result = f'Directory "{newpath}" does not exist.'
                print(result)
                return result
        while "//" in self.currentpath:
            self.currentpath = self.currentpath.replace('//', '/')
        return self.currentpath

    def chmod(self, permissions, filename):
        # Нормализуем путь к текущей директории
        current_path_normalized = self.currentpath.lstrip('/')
        file_path = f"{current_path_normalized}/{filename}".replace("//", "/")
        # Проверка существования файла в ZIP-архиве
        file_exists = any(file.filename == file_path for file in self.filesystemlist)
        if not file_exists:
            result = f"File {filename} does not exist"
            print(result)
            self.log_command(f"chmod {permissions} {filename}", result)
            return result
        # Проверка и обработка формата `permissions`
        mode_bits = {'r': stat.S_IRUSR, 'w': stat.S_IWUSR, 'x': stat.S_IXUSR}
        user_bits = {'u': stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
                     'g': stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP,
                     'o': stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH}
        new_permissions = 0
        if not permissions.isdigit():
            for part in permissions.split(','):
                if len(part) >= 3 and part[0] in user_bits and part[1] in "+-=" and part[2] in mode_bits:
                    target, action, mode = part[0], part[1], part[2]
                    bit = mode_bits[mode]
                    if action == '+':
                        new_permissions |= bit
                    elif action == '-':
                        new_permissions &= ~bit
                    elif action == '=':
                        new_permissions = bit
                else:
                    result = "Invalid permission: use format u+x, g-w, o=r"
                    print(result)
                    self.log_command(f"chmod {permissions} {filename}", result)
                    return result
        else:
            new_permissions = int(permissions, 8)
        # Логирование изменений только один раз
        result = f"Permissions for {filename} set to {permissions}"
        print(result)
        self.log_command(f"chmod {permissions} {filename}", result)
        return result

    def cal(self, month=None, year=None):
        try:
            if month is None and year is None:
                # No arguments: show current month and year
                month = datetime.now().month
                year = datetime.now().year
                result = calendar.month(year, month)
                print(result)
            elif month is not None and year is None:
                # Check if the input is a 4-digit number (indicating a year)
                if month.isdigit() and len(month) == 4:
                    year = int(month)
                    result = calendar.calendar(year)  # Output the full calendar for the year
                    print(result)
                else:
                    # Treat input as a year if a valid integer within a reasonable range
                    year = int(month)
                    if 1 <= year <= 9999:  # Assuming any integer input is a year
                        result = calendar.calendar(year)
                        print(result)
                    else:
                        result = "Invalid input: Please enter a valid month or year"
                        print(result)
            elif month is not None and year is not None:
                month = int(month)
                year = int(year)
                result = calendar.month(year, month)  # Output the specific month of the specified year
                print(result)
            else:
                result = "Usage: cal [month] [year]"
                print(result)
        except ValueError as e:
            result = f"Invalid input: {e}"
            print(result)
        return result

    def echo(self, cmd, zf=None):
        interpret_escape_sequences = False
        add_newline = True
        output = ""
        file_mode = None
        file_path = None
        result = ""

        i = 1
        while i < len(cmd):
            if cmd[i] == '-n':
                add_newline = False
            elif cmd[i] == '-e':
                interpret_escape_sequences = True
            elif cmd[i] == '>':
                file_mode = 'w'  # Write mode
                if i + 1 < len(cmd):
                    file_path = cmd[i + 1]
                break
            elif cmd[i] == '>>':
                file_mode = 'a'  # Append mode
                if i + 1 < len(cmd):
                    file_path = cmd[i + 1]
                break
            else:
                output += cmd[i] + " "
            i += 1

        if interpret_escape_sequences:
            output = output.replace("\\n", "\n").replace("\\t", "\t").replace("\\a", "\a").replace("\\\\", "\\")

        if file_path:
            file_path = self.currentpath.lstrip("/") + "/" + file_path if not file_path.startswith(
                "/") else file_path.lstrip("/")
            temp_zip_path = tempfile.mktemp()

            try:
                existing_content = ""
                if file_mode == 'a':
                    try:
                        with zipfile.ZipFile(self.config['zip_path'], 'r') as zip_ref:
                            with zip_ref.open(file_path) as file:
                                existing_content = file.read().decode('utf-8')
                    except KeyError:
                        pass

                output = existing_content + output

                # Закрытие текущего архива перед записью
                if self.filesystem:
                    self.filesystem.close()

                with zipfile.ZipFile(self.config['zip_path'], 'r') as old_zip:
                    with zipfile.ZipFile(temp_zip_path, 'w') as new_zip:
                        for item in old_zip.infolist():
                            if item.filename != file_path:
                                new_zip.writestr(item, old_zip.read(item.filename))

                        new_zip.writestr(file_path, output.encode('utf-8'))

                time.sleep(0.1)  # Минимальная задержка, чтобы ОС освободила файловый дескриптор

                # Заменяем старый ZIP новым
                os.replace(temp_zip_path, self.config['zip_path'])

                # Переоткрываем обновленный ZIP-файл
                self.filesystem = zipfile.ZipFile(self.config['zip_path'], 'r')
                self.filesystemlist = self.filesystem.filelist

                result = f"Text written to {file_path}"
                print(result)
            except PermissionError:
                print(
                    "Some error: Unable to write to file due to permission issues. Try closing any open instances of the ZIP archive.")
            except Exception as e:
                print(f"Some error: {e}")
            finally:
                # Удаляем временный файл, если он существует
                if os.path.exists(temp_zip_path):
                    os.remove(temp_zip_path)
        else:
            print(output, end='' if not add_newline else '\n')
            result = output.strip()

        self.log_command(" ".join(cmd), result)
        return result

    def run_script(self):
        script_file = self.start_script
        try:
            with open(script_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    self.execute_command(line)
                    self.log_command(line, f"Executed: {line}")
        except FileNotFoundError:
            print(f"Script file '{script_file}' not found.")

    def execute_command(self, command: str):
        cmd = shlex.split(command)
        result = None
        if cmd[0].lower() == "ls":
            result = self.ls(cmd[1] if len(cmd) > 1 else "")
        elif cmd[0].lower() == "cd":
            result = self.cd(cmd[1] if len(cmd) > 1 else "")
        elif cmd[0].lower() == "chmod":
            print("chmod command not implemented.")
        elif cmd[0].lower() == "echo":
            result = self.echo(cmd)
        elif cmd[0].lower() == "cal":
            print("cal command not implemented.")
        elif cmd[0].lower() == "exit":
            sys.exit(0)
        else:
            print('Unknown command.')
        self.log_command(command, result)

    def close_filesystem(self):
        if self.filesystem:
            self.filesystem.close()  # Метод для закрытия ZIP-файла, когда он больше не нужен

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)
    vcl = Emulator(sys.argv[1])
    vcl.start()
    vcl.close_filesystem()