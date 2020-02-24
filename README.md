# python-news-scraper

Небольшой веб-скрейпер для сайта lenta.ru.

Написан при помощи **python3, requests, BeautifulSoup**!


## Как запустить:

### Установка необходимых пакетов

```pip3 install requests```

```pip install beautifulsoup4```

### Запуск скрипта
```python3 main.py --file=out.txt --date=2020.02.20 --rubric=news```

* ```file``` - необходимый аргумент, файл вывода информации
* ```date``` - дата, в которую были выложены новости. Обязательно в формате YYYY.MM.DD
* ```rubric``` - необходимая рубрика. На выбор: news - новости, articles - статьи. 

