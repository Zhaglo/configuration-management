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
