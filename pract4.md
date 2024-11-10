### ЗАДАНИЕ 1.

---

На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.

#### РЕШЕНИЕ: 
    
![Снимок экрана 2024-11-10 183055](https://github.com/user-attachments/assets/4cb804e3-a1bc-493a-b661-7ef8eb796f82)

### ЗАДАНИЕ 2. 

---

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.

#### РЕШЕНИЕ:

Создание локального репозитория:
~~~
mkdir rep
cd rep
git init
~~~
Установка имени и почты:
~~~
git config user.name "Igor Zhaglo"
git config user.email "zhaglo.i.d@edu.mirea.ru"
~~~
Создание prog.py и добавление в репозиторий:
~~~
echo "# Python code" > prog.py
git add prog.py
git commit -m "first commit"
~~~
Вывод терминала:
~~~
[master (root-commit) 47d7683] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py
~~~

### ЗАДАНИЕ 3.

---

Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

#### РЕШЕНИЕ:

Создание bare-репозитория:
~~~
git init --bare server.git
~~~
~~~
Initialized empty Git repository in C:/Users/Пользователь/test_f/server.git/
~~~
Добавление сервера и удаленного репозитория и пуш содержимого:
~~~
cd rep
git remote add server ../server.git
git remote -v
git remote -u server master
~~~
~~~
server  ../server.git (fetch)
server  ../server.git (push)
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 228 bytes | 228.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To ../server.git
 * [new branch]      master -> master
branch 'master' set up to track 'server/master'.
~~~
Клонирование сервера в отдельную папку, указание имени и почты:
~~~
cd ..
mkdir rep_coder2
git clone server.git rep_coder2
cd rep_coder2
git config user.name "Igor Zhaglo"
git config user.email "zhaglo.i.d@edu.mirea.ru"
~~~
~~~
Cloning into 'rep_coder2'...
done.
~~~
Добавление readme.md и пуш на сервер
~~~
echo "# Project info" > readme.md
git add readme.md
git commit -m "readme"
git push
~~~
~~~
[master 315dc94] readme
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md

Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 12 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 290 bytes | 290.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To C:/Users/Пользователь/test_f/server.git
   47d7683..315dc94  master -> master
~~~
Возвращаемся к coder1, получаем актуальные данные, добавляем данные об авторе, пушим изменения
~~~
cd ../rep
git pull server master
echo "## Coder1" >> readme.md
git add readme.md
git commit -m "coder1 info"
git push

remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 270 bytes | 33.00 KiB/s, done.
From ../server
 * branch            master     -> FETCH_HEAD
   47d7683..315dc94  master     -> server/master
Updating 47d7683..315dc94
Fast-forward
 readme.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md

[master d851de6] coder 1 info
 1 file changed, 1 insertion(+)

Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 304 bytes | 304.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To ../server.git
   315dc94..d851de6  master -> master
~~~
Coder1 добавляет информацию, пушит изменения
~~~
cd ../rep_coder2
git pull --rebase
echo "Coder2" >> readme.md
git add readme.md
git commit -m "coder2 info"
git push

remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 284 bytes | 25.00 KiB/s, done.
From C:/Users/Пользователь/test_f/server
   315dc94..d851de6  master     -> origin/master
Updating 315dc94..d851de6
Fast-forward
 readme.md | 1 +
 1 file changed, 1 insertion(+)

[master a86d882] coder2 info
 1 file changed, 1 insertion(+)

Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 308 bytes | 308.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To C:/Users/Пользователь/test_f/server.git
   d851de6..a86d882  master -> master
~~~

### ЗАДАНИЕ 4.

---

Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.

~~~python
import subprocess

def get_git_objects():
    # Получаем список всех объектов (хешей) в репозитории
    result = subprocess.run(["git", "rev-list", "--all", "--objects"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Ошибка при получении списка объектов:", result.stderr)
        return []
    # Парсим вывод и извлекаем хеши объектов
    return [line.split()[0] for line in result.stdout.splitlines() if line]

def show_object_content(obj_hash):
    # Выводим содержимое объекта с помощью git cat-file -p
    result = subprocess.run(["git", "cat-file", "-p", obj_hash], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при выводе содержимого объекта {obj_hash}:", result.stderr)
    else:
        print(f"\n--- Содержимое объекта {obj_hash} ---\n")
        print(result.stdout)

def main():
    # Получаем все объекты и выводим их содержимое
    objects = get_git_objects()
    for obj_hash in objects:
        show_object_content(obj_hash)

if __name__ == "__main__":
    main()
~~~
Пример вывода программы:
~~~
--- Содержимое объекта cbacfd40f47dec909035d3481a5eef9e539c6bb1 ---

tree e9145164cdf6968c0420d1565d490a258441c5c5
parent 44cf87a125a9353b5b9437095fd8387fab49a017
author Zhaglo <jagloik@gmail.com> 1731255312 +0300
committer Zhaglo <jagloik@gmail.com> 1731255312 +0300

pract4_3


--- Содержимое объекта 44cf87a125a9353b5b9437095fd8387fab49a017 ---

tree 5a5c9fe7980344bdffd4e0f1c0dd92e03ab6e0e7
parent 35f4551e3a0273ee39f0e892a38a2896e46bb137
parent 88ad306543151ad12dc8d3b203a29e14d4050f77
author Zhaglo <jagloik@gmail.com> 1731253650 +0300
committer Zhaglo <jagloik@gmail.com> 1731253650 +0300

Merge remote-tracking branch 'origin/master'


--- Содержимое объекта 35f4551e3a0273ee39f0e892a38a2896e46bb137 ---

tree 5a5c9fe7980344bdffd4e0f1c0dd92e03ab6e0e7
parent 070b3cb4c311870591459d72fa31cadacab304f6
author Zhaglo <jagloik@gmail.com> 1731253627 +0300
committer Zhaglo <jagloik@gmail.com> 1731253627 +0300

pract4_2


--- Содержимое объекта 88ad306543151ad12dc8d3b203a29e14d4050f77 ---

tree b3bf66a5b7b7d477d3a421cef8573ff719e6b08c
parent 5f642a66b500d8f2f2864cc80055c17227fc786e
parent 070b3cb4c311870591459d72fa31cadacab304f6
author Zhaglo <147069106+Zhaglo@users.noreply.github.com> 1730125614 +0300
committer GitHub <noreply@github.com> 1730125614 +0300
gpgsig -----BEGIN PGP SIGNATURE-----
 
 wsFcBAABCAAQBQJnH58uCRC1aQ7uu5UhlAAAXVQQAK5a0IsmoQXuGwCBxQzfsp67
 qRkssMggp0sOR/a+Xfp0KtzY6uPJeNJvgeHET7KI0Pl8Reg6bzu+frdO6ItUlTKe
 FDrOUd6BRey35Yz9M1wvThBBJGMWQKrJIdRc4pgfKv8+/kaQw5PSao63lB7ZeJoV
 yij2zyGoahTFPNUws0CeAdEiERN24VB+xQV6DZ6vq/H9ZHrlgyz9n0+ap1kaXQrf
 XOGMlVXaJXQtYC/Aph8WUU9e9JoWwm28ADG2WljpDoCAg5xvrNfKrCE3i9mJuZ/Z
 lv4m/Q99htVtdcnC+RDCF9F1ugTsvbD11lr/aV8+8G/AdAxJvbWbAKs0+TeKQNKC
 VxhMvphs7r3JTs6U9APSvwcqgwCpfEuyrwbnlXTcWxToSp0E0YCFt1zqiYU38X5B
 UfJ5AtJS/qJ002rDKjKBFHD9HgqgVyaPSz9/1+H2s2dDLtvaz63vJyxfCaevSVgO
 D4ve9z+RhnVjWLkYfjPbuaPVUXIlNt7eCtAoNgpvqcw3+gxlzZhFfvuA4j8asl84
 f9jHfafMC+hmraXiDF1M8/jP4NlKGzoDPyHziAak/G1RcyQr9y+U0ECoF+3QTRuo
 qtMzciHWGoi4Za22DLXoJ4Ys+0pXrlZ4GQrB6lR3uqK4P8GTqcQ6wajJFCbXmsTO
 luzqi2clUdiPyt4ZG/Xc
 =4goc
 -----END PGP SIGNATURE-----
 

Merge pull request #1 from Zhaglo/main
~~~