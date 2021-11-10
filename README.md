# Боты Telegram и VK для проведения опросов

Бэкэнд для ботов telegram и VK для проведения опросов.

## Как запустить локально на linux

* Скачайте код
* Перейдите в каталог проекта
* Установите зависимости `pip3 install -r requirements.txt`
* Создайте файл .env с переменными окружения (указаны ниже) и положите в каталог с проектом
* Экспортируйте переменные окружения `source .env`
* Создайте бота в telegram и начните с ним беседу
* Запустите бота `python3 tg_quiz_bot.py` или `python3 vk_quiz_bot.py`
* Откройте в браузере
* Зарегистрируйтесь на redis.com и получите бесплатную базу (либо разверните redis у себя)

## Настройки окружения. Пример:

```
export TELEGRAM_TOKEN='токен_полученный_при_регистрации_бота'
export VK_TOKEN="Токен VK"
export REDIS_HOST="хост redis"
export REDIS_PORT="порт"
export REDIS_PASS="пароль"%
```

## Пример
Пообщаться с ботом vk можно в группе [vk](https://vk.com/club208722794)


## Цели проекта

Код написан в учебных целях.
