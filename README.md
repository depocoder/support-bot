# support-bot
 
Этот проект позволяет создать своего бота для быстрого ответа пользователям(VK, Telegram) при помощи [dialogflow](https://dialogflow.cloud.google.com/).

![пример телеграм](https://i.imgur.com/5wGUKZl.png)

## Подготовка dialogflow
Шаг 1. Создать проект   
[Как создать проект в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup)     
Там же вы должны получить идентификатор проекта. Нам выдали такой:   
`moonlit-dynamo-211973`   
    
Шаг 2. Создать агента   
[Создать "агента"](https://cloud.google.com/dialogflow/docs/quick/build-agent)
1. Идентификатор проекта из прошлого шага   
2. Русский язык, иначе бот не будет понимать ваши фразы
     
Шаг 3. Натренируйте бота на ваши фразы в вкладке Intent    
     
Шаг 4. Создайте JSON ключ     
[Создание JSON-ключа](https://cloud.google.com/docs/authentication/getting-started)

## Подготовка к запуску Mac OS

Уставновить Python 3+

```
sudo apt-get install python3
```

Установить, создать и активировать виртуальное окружение

```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```

Установить библиотеки командой

```
pip3 install -r requirements.txt
```

## Запуск кода

Вы можете добавить свои Intent через скрипт ml_study.py. Скрипт принимает JSON(файл должен быть в папке с ml_study.py и называться questions.json, в репозитории уже есть пример) с такой архитектурой     
```json

    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту прийдёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    },
```
     
Запуск ml_study.py
```
python3 ml_study.py
```
    
Запуск ботов 

```
python3 tg_bot.py
python3 vk_bot.py
```
Создайте файл ".env" в него надо прописать ваши token'ы.   
В переменную `TG_TOKEN` его можно получить в отце всех ботов @botfather в телеграме.    
В переменную `GOOGLE_APPLICATION_CREDENTIALS` путь к файлу с ключами.    
В переменную `PROJECT_ID` его мы получали в 1 шаге.    
В переменную `LANGUAGE_CODE` код языка на котором будет говорить бот.    
В переменную `VK_TOKEN` токен группы вк.    
    
**Пример**  
```
TG_TOKEN=1477653591:AAFWsLwFZow3r38niRfX-0v0RlMh9-x0Yo8
GOOGLE_APPLICATION_CREDENTIALS=My First Project-d13c49bcd421150.json
PROJECT_ID=compact-nirvana-292417614
LANGUAGE_CODE=ru
VK_TOKEN=a6e29a6d107cf50e457940fa9d997e0737c273180e8e9420e8a76eb80d0772b1ac5db2c012abe7a37a734
```


# Аргументы ml_study

1. `skip_intent` - не загружать intent.
2. `skip_train` - не обучать dialogflow.    
    
**Запуск ml_study с аргументами**

```
python3 ml_study.py --skip_train
```
