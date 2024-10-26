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
import io
class VCL:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.currentpath = ""
        self.user = self.config['username']
        self.host = self.config['hostname']
        self.start_script = self.config['start']
        self.filesystem = zipfile.ZipFile(self.config['zip_path'], 'a')
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
                    result = self.echo(cmd)  # Передаем срез, чтобы избежать лишних аргументов
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
            if any(file.filename.startswith(newpath) for file in self.filesystemlist):
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
            if any(file.filename.startswith(new_path.lstrip("/")) for file in self.filesystemlist):
                self.currentpath = new_path
            else:
                result = f'Directory "{newpath}" does not exist.'
                print(result)
                return result
        while "//" in self.currentpath:
            self.currentpath = self.currentpath.replace('//', '/')
        return f"Changed directory to {self.currentpath}"
    def chmod(self, permissions, filename):
        # Нормализуем путь к текущей директории
        current_path_normalized = self.currentpath.lstrip('/')
        file_path = f"{current_path_normalized}/{filename}".replace("//", "/")
        print(f"Checking permissions for {file_path}")  # Debug print
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
        result = f"Permissions for {filename} set to {permissions} (simulated)"
        print(result)
        self.log_command(f"chmod {permissions} {filename}", result)
        return result
    def cal(self, month=None, year=None):
        try:
            if month is None and year is None:
                month = datetime.now().month
                year = datetime.now().year
                result = calendar.month(year, month)
                print(result)
            elif month is not None and year is None:
                if len(month) == 4 and month.isdigit():
                    year = int(month)
                    result = calendar.calendar(year)
                    print(result)
                else:
                    result = "Usage: cal [month] [year]"
                    print(result)
            elif month is not None and year is not None:
                month = int(month)
                year = int(year)
                result = calendar.month(year, month)
                print(result)
            else:
                result = "Usage: cal [month] [year]"
                print(result)
        except ValueError as e:
            result = f"Invalid input: {e}"
            print(result)
        return result
    def echo(self, cmd):
        interpret_escape_sequences = False
        add_newline = True
        args = []
        i = 1
        while i < len(cmd):
            if cmd[i] == '-n':
                add_newline = False
            elif cmd[i] == '-e':
                interpret_escape_sequences = True
            else:
                args = cmd[i:]
                break
            i += 1
        output = " ".join(args)
        if interpret_escape_sequences:
            output = output.replace("\\n", "\n").replace("\\t", "\t").replace("\\a", "\a").replace("\\\\", "\\")
        if add_newline:
            print(output)
        else:
            print(output, end='')
        return output
    def run_script(self):
        script_file = self.start_script
        try:
            with open(script_file, 'r') as file:
                for line in file:
                    self.execute_command(line.strip())
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
        self.filesystem.close()  # Метод для закрытия ZIP-файла, когда он больше не нужен
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)
    vcl = VCL(sys.argv[1])
    vcl.start()
    vcl.close_filesystem()