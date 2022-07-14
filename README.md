# Product-Base-API
## Настройка
Для работы в локальном режиме необходимо:
1. Установить Python
2. Скачать все библиотеки из файла requirements.txt (из папки с requirements.txt в командную строку вбить `pip install -r requirements.txt`)
3. После выполнения пунктов ниже запусти файл main.py
_____
Необходимо в Firebase создать Firestore Database. 
В папку с файлом main.py, необходимо добавить выданный Firebase json файл (как его получить показанно в этом ролике https://www.youtube.com/watch?v=mNMv3WNgp0c&ab_channel=DataStream
с 0:15-1:00), а также в файл name.txt написать имя этого файла (с расширение) (Пример: `cool-1337-firebase-adminsdk-abcde-qwerrttyyu.json`)
### Примечание
Тут показан пример работы в локальном режиме, по этому все url'ы будут начинаться с http://127.0.0.1:5000
# Запросы
## Post-запросы
### Добавление продукта
URL
```
http://127.0.0.1:5000/products
```
#### Body
```
{
  "name": "BUS",
  "category": {
    "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",  //ID ОПЦИОНАЛЬНО
    "name": "cars"
  },
  "price": 105550.0,
  "content": "car",
  "imgs": [
      "bus.jpg",
      "bus2.jpg"
  ],
  "productLink": "coolcarsbus.com"
}
```
____
**Примечания:**
* "category" обязательно должно быть 'словарём', а "imgs" 'списком'
* В "category" обязательно писать только "name", если "id" не будет или значение "id" не будет в таблице с категориями, то API само сгенерирует его в формате UUID 
(в случае если категории с таким название нет в таблице с категориями, то API автоматически создаст эту категорию).
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
____
#### Значение ошибок
Не переданы данные в Body:
```
{'error': 'Empty request'}
```
Нет всех нужных 'полей':
```
{'error': 'Bad request'}
```
### Добавление категорий
URL
```
http://127.0.0.1:5000/categories
```
#### Body
```
{
  "name": "cars"
}
```
____
**Примечания:**
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
____
#### Значение ошибок
Не переданы данные в Body:
```
{'error': 'Empty request'}
```
Нет всех нужных 'полей':
```
{'error': 'Bad request'}
```
## Get-запросы
### Просмотр всех товаров (без деталей) (сортировка товаров идёт от самого нового к самому старому (по дате добавления))
URL
```
http://127.0.0.1:5000/products
```
#### Пример полученных данных:
```
[
    {
        "id": "18f199d3-f857-4416-abea-3ed404592796",
        "img": "bus.jpg",
        "name": "BUS"
    },
    {
        "id": "27393cae-8c91-4dbd-bbc5-679660f83b0f",
        "img": "bus.jpg",
        "name": "ICE BUS"
    }
]
```
### Просмотр всех товаров c деталей (сортировка товаров идёт от самого нового к самому старому (по дате добавления))
```
http://127.0.0.1:5000/products/details
```
#### Пример полученных данных:
```
[
    {
        "category": {
            "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
            "name": "cars"
        },
        "content": "car",
        "createdAt": "2022-07-14 13:28:48.195102",
        "id": "18f199d3-f857-4416-abea-3ed404592796",
        "imgs": [
            "bus.jpg",
            "car.jpg"
        ],
        "name": "BUS",
        "price": 1050.0,
        "productLink": "coolcarsbus.com"
    },
    {
        "category": {
            "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
            "name": "cars"
        },
        "content": "car",
        "createdAt": "2022-07-14 11:44:58.166337",
        "id": "27393cae-8c91-4dbd-bbc5-679660f83b0f",
        "imgs": [
            "bus.jpg",
            "car.jpg"
        ],
        "name": "ICE BUS",
        "price": 105550.0,
        "productLink": "coolcarsbus.com"
    }
]
```
### Просмотр товара по id (без деталей)
```
http://127.0.0.1:5000/products/<string:product_id>
```
* Вместо `<string:product_id>` должен быть id товара
#### Пример полученных данных:
```
{
    "id": "18f199d3-f857-4416-abea-3ed404592796",
    "img": "bus.jpg",
    "name": "BUS"
}
```
#### Значение ошибок
Неверный `<string:product_id>`:
```
{'error': 'Not found'}
```
### Просмотр товара по id с деталями
```
http://127.0.0.1:5000/products/<string:product_id>/details
```
* Вместо `<string:product_id>` должен быть id товара
#### Пример полученных данных: 
```
{
    "category": {
        "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
        "name": "cars"
    },
    "content": "car",
    "createdAt": "2022-07-14 13:28:48.195102",
    "id": "18f199d3-f857-4416-abea-3ed404592796",
    "imgs": [
        "bus.jpg",
        "car.jpg"
    ],
    "name": "BUS",
    "price": 1050.0,
    "productLink": "coolcarsbus.com"
}
```
#### Значение ошибок
Неверный `<string:product_id>`:
```
{'error': 'Not found'}
```
### Просмотр всех категорий
URL
```
http://127.0.0.1:5000/categories
```
#### Пример полученных данных:
```
[
    {
        "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
        "name": "cars"
    }
]
```
### Просмотр категории по id
```
http://127.0.0.1:5000/categories/<string:category_id>
```
* Вместо `<string:category_id>` должен быть id категории
#### Пример полученных данных:
```
{
    "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
    "name": "cars"
}
```
#### Значение ошибок
Неверный `<string:category_id>`:
```
{'error': 'Not found'}
```
## Put-запросы
### Редактирование продукта
URL
```
http://127.0.0.1:5000/products/<string:product_id>
```
* Вместо `<string:product_id>` должен быть id товара
#### Body
```
{
  "name": "BUS1",
  "category": {
    "id": "b3b3cc0c-9f8d-4f5d-9a27-9d608521eeef",
    "name": "cars"
  },
  "price": 105550.0,
  "content": "car",
  "imgs": [
      "bus.jpg",
      "bus2.jpg"
  ],
  "productLink": "coolcarsbus.com"
}
```
**Примечания:**
* "category" обязательно должно быть 'словарём', а "imgs" 'списком'
* **В "category" обязательно писать как "name", так и "id"**
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
#### Значение ошибок
Неверный `<string:product_id>`:
```
{'error': 'Not found'}
```
Нет всех нужных 'полей':
```
{'error': 'Bad request'}
```

### Редактирование категории
URL
```
http://127.0.0.1:5000/categories/<string:category_id>
```
* Вместо `<string:category_id>` должен быть id категории
#### Body
```
{
  "name": "car1"
}
```
**Примечания:**
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
#### Значение ошибок
Неверный `<string:category_id>`:
```
{'error': 'Not found'}
```
Нет всех нужных 'полей':
```
{'error': 'Bad request'}
```
## Delete-запросы
### Удаление товара по id
```
http://127.0.0.1:5000/products/delete/<string:product_id>
```
* Вместо `<string:product_id>` должен быть id товара
#### Примечания:
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
____
#### Значение ошибок
Неверный `<string:product_id>`:
```
{'error': 'Not found'}
```
### Удаление категории по id
```
http://127.0.0.1:5000/categories/delete/<string:category_id>
```
* Вместо `<string:category_id>` должен быть id категории
#### Примечания:
* В случае правильного запроса в ответ выдастся `{'success': 'OK'}`
____
#### Значение ошибок
Неверный `<string:category_id>`:
```
{'error': 'Not found'}
```
