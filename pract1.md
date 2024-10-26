ЗАДАЧА 1. Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd.
  РЕШЕНИЕ:
  cut -d: -f1 /etc/passwd | sort
  
  ![image](https://github.com/user-attachments/assets/3142e02b-3e12-4937-bca1-e1bd04e341aa)

ЗАДАЧА 2. Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов.
  РЕШЕНИЕ:
  cat /etc/protocols |sort -nrk2 | head -n 5 | awk '{print $2, $1}'
  
  ![image](https://github.com/user-attachments/assets/5c4fa12e-fe3a-44af-b922-80ca49da2be9)

ЗАДАЧА 3. Написать программу banner средствами bash для вывода текстов.
  РЕШЕНИЕ:
  string='MIREA'
  size=${#string}
  echo -n "+"
  for ((i=-2;i<size;i++))
  do
  echo -n "-"
  done
  echo "+"
  echo "| $string |"
  echo -n "+"
  for ((i=-2;i<size;i++))
  do
  echo -n "-"
  done
  echo "+"
  +-------+
  | MIREA |
  +-------+
  
  ![Снимок экрана от 2024-09-02 17-43-27](https://github.com/user-attachments/assets/3dee2459-5baf-4ee4-8e10-70b5c5a37d62)

ЗАДАЧА 4. Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).
  РЕШЕНИЕ: grep -o '\b[a-zA-Z_][a-zA-Z0-9_]*\b' Main.java | sort | uniq
  
  ![image](https://github.com/user-attachments/assets/1fe27d0c-6ad5-4da9-9eb9-c2890a93d449)

ЗАДАЧА 5. Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).
  РЕШЕНИЕ: sudo cp "$1" /home/igor/bin/
          chmod +x reg.sh
          ./reg.sh file.sh
          
  ![image](https://github.com/user-attachments/assets/efea722b-9181-4583-a8a6-d1327968cdca)
  ![image](https://github.com/user-attachments/assets/16fc7e30-00a5-4a56-94fd-538831cd2769)

ЗАДАЧА 6. Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.
  РЕШЕНИЕ: 

  for file in "$@"; do
  if [[ "$file" =~ \.(c|js|py)$ ]]; then
    first_line=$(head -n 1 "$file")
    if [[ "$file" =~ \.c$ && "$first_line" =~ ^// ]] || \
       [[ "$file" =~ \.js$ && "$first_line" =~ ^// ]] || \
       [[ "$file" =~ \.py$ && "$first_line" =~ ^# ]]; then
      echo "$file has a comment in the first line."
    else
      echo "$file does not have a comment in the first line."
    fi
  fi
  done

  ./go.sh ~/PycharmProjects/test/main.py
  
  ![image](https://github.com/user-attachments/assets/32348ac8-3d2e-4ffb-ad90-ee32da898346)
  ![image](https://github.com/user-attachments/assets/fe8468f8-1267-4b70-b0dd-237beed126de)

ЗАДАЧА 7. Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).
  РЕШЕНИЕ: find /home/igor/Загрузки/ -type f -exec md5sum {} + | sort | uniq -w32 -dD
  
  ![image](https://github.com/user-attachments/assets/507fb24b-76c5-4c0c-b0d4-22ad03daab27)

ЗАДАЧА 8. Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.
  РЕШЕНИЕ: find . -name "*.sh" -print0 | tar -czvf archive.tar.gz --null -T -
  
  ![image](https://github.com/user-attachments/assets/503126c4-05d8-4782-9941-6650b3fedea8)
  ![Снимок экрана от 2024-09-08 22-34-10](https://github.com/user-attachments/assets/b7b3a624-493a-4416-98a2-c0c0f0b7c626)


ЗАДАЧА 9. Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.
  РЕШЕНИЕ: sed 's/    /\t/g' "text1.txt" > "text2.txt"
  
  ![image](https://github.com/user-attachments/assets/6acff5a2-6906-4c72-bd85-519fc6f6ddd2)
  ![image](https://github.com/user-attachments/assets/c4658cf1-66fa-43ef-bdaf-fdc62b613284)

ЗАДАЧА 10. Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.
  РЕШЕНИЕ: find . -type f -empty -name "*.txt"
  
  ![image](https://github.com/user-attachments/assets/d0348a7c-e38e-4b3e-8476-d8907a3039cc)


