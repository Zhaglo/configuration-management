ЗАДАНИЕ 1. Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

  РЕШЕНИЕ:
  ~~~jsonnet
  local groupPrefix = 'ИКБО-';
  local year = '-23';
  local groupNum = std.range(1, 10);
  
  local studentData = [
    {name: "Жагло И. Д.", age: 20, groupIndex: 2},
    {name: "Коротков А. А.", age: 69, groupIndex: 3},
    {name: "Запрягаев М. А.", age: 19, groupIndex: 1},
    {name: "Красоткин А. А.", age: 18, groupIndex: 4}
  ];
  
  {
    groups: [groupPrefix + std.toString(i) + year for i in groupNum],
  
    students: [
      {
        age: student.age,
        group: groupPrefix + std.toString(student.groupIndex) + year,
        name: student.name
      } for student in studentData
    ],
  
    subject: "Конфигурационное управление"
  }
  ~~~


  ![image](https://github.com/user-attachments/assets/67fee7bd-4c5b-4ee1-acec-75bf8f3e5631)


ЗАДАНИЕ 2. Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

  РЕШЕНИЕ:
  ~~~dhall
  let Group = Text
  let Student = { age : Natural, group : Group, name : Text }
  
  let createGroup : Natural -> Text =
        λ(n : Natural) → "ИКБО-" ++ Natural/show n ++ "-23"
  
  let groups : List Text =
        [ createGroup 1
        , createGroup 2
        , createGroup 3
        , createGroup 4
        , createGroup 5
        , createGroup 6
        , createGroup 7
        , createGroup 8
        , createGroup 9
        , createGroup 10
        ]
  
  let createStudent : Natural -> Group -> Text -> Student =
        λ(age : Natural) →
        λ(group : Group) →
        λ(name : Text) →
          { age = age, group = group, name = name }
  
  let students : List Student =
    [ createStudent 20 (createGroup 2) "Жагло И. Д."
    , createStudent 21 (createGroup 3) "Коротков А. А."
    , createStudent 22 (createGroup 1) "Запрягаев М. А."
    , createStudent 20 (createGroup 4) "Красоткин А. А."
    ]
  
  in  { groups = groups, students = students, subject = "Конфигурационное управление" }
  ~~~


  ![image](https://github.com/user-attachments/assets/e9736cc7-a114-475e-8f96-79da6e2cf9d9)


Для решения дальнейших задач потребуется программа на Питоне, представленная ниже. Разбираться в самом языке Питон при этом необязательно.

~~~
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = a
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
~~~   

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF:

ЗАДАНИЕ 3. Язык нулей и единиц.
~~~
10
100
11
101101
000
~~~
  РЕШЕНИЕ:
  ~~~
  BNF = '''
  E = 0 | 1 | 0 E | 1 E
  '''
  ~~~
  ВЫВОД ПРОГРАММЫ:
  ![image](https://github.com/user-attachments/assets/c6e7c985-f774-4dde-9de3-6a8e9477c56d)


ЗАДАНИЕ 4. Язык правильно расставленных скобок двух видов.
~~~
(({((()))}))
{}
{()}
()
{}
~~~
  РЕШЕНИЕ:
  ~~~
  BNF = '''
  E =  | ( E ) | { E } | E E
  '''
  ~~~
  ВЫВОД ПРОГРАММЫ:
  ![image](https://github.com/user-attachments/assets/5a9bb6fa-1b92-419d-96dc-fd71322ffca3)


ЗАДАНИЕ 5. Язык выражений алгебры логики.
~~~
((~(y & x)) | (y) & ~x | ~x) & x
y & ~(y)
(~(y) & y & ~y)
~x
~((x) & y | (y) | (x)) & x | x | (y & ~y)
~~~
  РЕШЕНИЕ:
  ~~~python

  import random
  
  def parse_bnf(text):
      '''
      Преобразовать текстовую запись БНФ в словарь.
      '''
      grammar = {}
      rules = [line.split('=') for line in text.strip().split('\n')]
      for name, body in rules:
          grammar[name.strip()] = [alt.split() for alt in body.split('/')]
      return grammar
  
  
  def generate_phrase(grammar, start):
      '''
      Сгенерировать случайную фразу.
      '''
      if start in grammar:
          seq = random.choice(grammar[start])
          return ''.join([generate_phrase(grammar, name) for name in seq])
      return str(start)
  
  BNF = '''
  E = x / y / ( E ) / ~ E / E & E / E | E
  '''
  
  for i in range(10):
      print(generate_phrase(parse_bnf(BNF), 'E'))
  ~~~

  ВЫВОД ПРОГРАММЫ:
  
  ![image](https://github.com/user-attachments/assets/05c8acb9-e8d1-468d-bb5f-cd5a85c025b7)

