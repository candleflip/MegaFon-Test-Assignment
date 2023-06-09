# Тестовое задание для МегаФон

1.	Изучить [статью](https://docs2.alationdata.com/en/latest/welcome/BestPractices/UseTrustFlagstoProceedwithConfidence.html?highlight=Trust%20Flags) из гайда Alation DC.
2.	Используя [статью](https://developer.alation.com/dev/docs/alation-apis-by-roles) найти 
спецификацию API которое считывает «светофор» и прислать ссылку.
3.	Используя файлик `./docs/response.txt` в качестве ответа на вызов API 
из п.2 написать скрипт который к этому API обращается и выводит все объекты типа 
«отчет BI» с «зеленым светофором» в виде csv файла, формата «url отчета;фио пользователя, 
который установил флаг». Значение `AlationInstanceURL` должно быть в качестве входного
параметра.
4.	Объяснить суть скрипта `./docs/code.txt`.
5.	Объяснить суть кода `./docs/role_glossary.txt`.

<br>

# Ответы

### Вопрос 2

Хочу отметить, что Alation API написано крайне информативным и понятным для использования
языком. Я не видел реализацию API под капотом, но те принципы REST, которые 
можно выявить из документации, соблюдены вплоть до формирования URL-запросов. Это
говорит о том, что с данным API можно приятно и эффективно работать.

Из текста задания я сделал вывод, что необходимо найти эндпоинт, позволяющий получить всю
информацию об определенном флаге проверки доверия ("светофоре").

В [этой](https://developer.alation.com/dev/docs/alation-apis-by-roles) статье, а также в
непосредственном описании реализации взаимодействия с определенным эндпоинтом "светофора"
[здесь](https://developer.alation.com/dev/reference/flags-api#get-details-of-a-particular-trust-check-flag),
есть ответ:
```
AlationInstanceURL/integration/flag/<flag_id>
```

где:
- `AlationInstanceURL` - URL-адрес экземпляра Alation, с которым
происходит взаимодействие (например, `https://alation.yourcompany.com`;
- `<flag_id>` - ID светофора, который необходимо считать.

Пример ответа на запрос к эндпоинту `AlationInstanceURL/integration/flag/8` (из документации):
```json
{
    "id": 8,
    "flag_type": "DEPRECATION",
    "ts_created": "2017-08-02T03:42:40.462533Z",
    "flag_reason": "Deprecate this data source",
    "subject": {
        "id": "1",
        "url": "/data/1",
        "otype": "data"
    },
    "user": {
        "id": 1,
        "url": "/user/1/",
        "display_name":"User Display Name"
    }
}
```

Из этого ответа можно получить всю необходимую информацию о светофоре, включая текущий
тип флага (`"DEPRECATION"`, `"ENDORSEMENT"` или `"WARNING"`).

#### Дополнительно

Если же необходимо получить информацию обо всех флагах и полный отчет (на что может намекать текст следующего задания),
то эндпоинт будет выглядеть следующим образом:

```
AlationInstanceURL/integration/flag/<flag_id>
```

где:
- `AlationInstanceURL` - URL-адрес экземпляра Alation, с которым
происходит взаимодействие (например, `https://alation.yourcompany.com`;

<br>

### Вопрос 3

Скрипт с ответом находится по пути `./main.py`. Во время разработки использовалась версия
`Python3.10.2`.

<br>

### Вопрос 4

Файл с исходным текстом находится по пути: `./docs/code.txt`. Я привел его в более читаемый формат и
сохранил в файле `./docs/code.sql`. Так с ним проще взаимодействовать, например, используя IDE.

Данный скрипт решает задачу поиска столбцов, назначенных в качестве первичного
ключа, в таблицах, соответствующих нескольким условиям. Также выводятся названия соответствующих таблиц и 
"наименование" владельца.

В скрипте происходит соединение трех таблиц для получения полной информации о первичном ключе и
связанных с ним столбцах. Это необходимо для применения условий поиска: выбираются только те таблицы, 

- которые являются обычными таблицами либо материализованными 
представлениями;
- владельцами которых являются `"PUB_DS"`, `"MBR"`, `"MFR_STG"`,
`"MBR_DEV"` или `"REP_B2B"`;
- и, по всей видимости, которые не являются устаревшими (не заканчиваются на `"_OLD"`) или
временными (не имеют в названии `"TMP_"`).

Результат сортируется в первую очередь по владельцам в алфавитном порядке, и после этого - по
названиям таблиц в алфавитном порядке.


<br>

### Вопрос 5

Файл с исходным текстом находится по пути: `./docs/role_grossary.txt`. Ответ сопровождается
соответствующими номерами строк из этого файла, написанными в скобках.

Этот скрипт используется для изменения политик доступа к статьям, предварительно 
отфильтрованным по значению `custom_template_id` (31). При условии нахождения
статьи с ID = `149` (37), для нее устанавливается пул разрешений, определенных
на строке 15, для определенных групп пользователей, определенных на строке 13.

Скрипт логирует начало модуля, прописывая (предполагаю) его название в логи (33)
и ID всех найденных и отфильтрованных статей. При нахождении статьи с ID = `149`
скрипт логирует ее название и результат запроса на изменение прав.

В файле `./docs/role_glossary_comments.py` этот код описан более подробно - я добавил
комментариев.

#### Дополнительно

У меня есть несколько вопросов и предложений, связанных с этим блоком кода. Вот 
некоторые из них:

Я не видел реализации класса Alation, но если такая возможность имеется,
я бы поместил использование `base_url` в методы класса, так как сейчас это лишняя строка 
(11) в скрипте. То же самое я предлагаю сделать с сессией, которая здесь создается
на строке 12, но с этим стоит быть осторожнее, так как в классе есть метод `get_groups()`
и возможно нет смысла переопределять весь класс в качестве контекстного менеджера.

Опять же, реализация класса Alation и вся бизнес-логика, для которой он
написан, даст больше информации.

Я сначала хотел переписать скрипт, проведя небольшую реорганизацию, разбив его на 
логические блоки и вынеся их в отдельные функции для более легкого масштабирования
впоследствии. Однако без четкого описания бизнес-задачи я решил этого не делать и 
с удовольствием опишу свои мысли при личной встрече. 

В первую очередь меня беспокоит то, что main() при вызове не принимает 
необходимый аргумент `settings` и имеет неиспользуемые позиционные и именованные
аргументы. На данный момент они лишние, а аргумент `settings` можно не использовать 
вовсе, так как по всей видимости он является константой. Если я прав, его можно внести,
например, в переменную окружения и оставить главную функцию без необходимости 
работать с аргументами.

Также:
- разработчик должен быть уверен, что группы, необходимые для
создания политик, будут получены в методе `get_groups()` и код не упадет с ошибкой;
- для повторения наименования группы в словаре (13), полагаю, должна быть причина;
- есть смысл использовать унифицированный тип форматирования строк (на 41 строке
тип отличается).
