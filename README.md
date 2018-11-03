(py)VKGammBot
==================
> [@vkgrammbot](https://t.me/user?vkgrammbot)

Read in english [here](https://github.com/Coestaris/pyvkgram/blob/master/README_en.md)

Возможности бота:
* Регистрация групп на прослушивание
* Настройка формата постов
* Поддержка изображений, документов, ссылок в постах (TODO: аудио, видео)

Telegram Бот для автоматического репоста постов с ВК в Телеграмм

Установка
-----------------
Установка зависимостей Python2.X
```bash
sudo apt-get install python-pip # Если требуется установить pip 
pip install vk BeautifulSoup4 python-telegram-bot tinydb
```

Для фонового запуска бота рекомендую использовать pm2
```bash
sudo apt-get install nodejs npm # Если требуется установить ноду
npm i pm2
```

Копирование исходников проекта и задача нужных параметров
```bash
git clone https://github.com/Coestaris/pyvkgram
cd pyvkgram
cp cfg_template.json cfg.json #Создание конфигурационного файла с файла-шаблона
vim cfg.json #Установка параметров (telegram token, vk tokens, delays)
cd scripts 
```

Для запуска используйте скрипт ```./pystart.py```. 
Для запуска в фоне ```./start```.

Лицензия
---------------
Оригинал [здесь](https://github.com/Coestaris/pyvkgram/blob/master/LICENSE.md). Ниже - интерпретация на русском языке

```
Copyright (c) 2018 Coestaris
 
Данная лицензия разрешает лицам, получившим копию данного программного
обеспечения и сопутствующей документации (в дальнейшем именуемыми 
«Программное Обеспечение»), безвозмездно использовать Программное Обеспечение 
без ограничений, включая неограниченное право на использование, копирование, 
изменение, слияние,публикацию, распространение, сублицензирование и/или продажу
копий Программного Обеспечения, а также лицам, которым предоставляется данное
Программное Обеспечение, при соблюдении следующих условий: Указанное выше
уведомление об авторском праве и данные условия должны быть включены во все
копии или значимые части данного Программного Обеспечения.
 
 
ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО 
ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ 
ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ,
НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ 
ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ 
ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА,ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА 
ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ. 
```

