# TestingTZ
Варианты запуска:
1) Без Docker:
  1. Открыть файл app.py
  2. Изменить название базы данных PostgreSQL на свое, если нет, то
     - Установить PostgreSQL
     - cd "C:\Program Files\PostgreSQL\<версия SQL>\bin"
     - psql -U postgres -d postgres (возможна ошибка при выполнении команды, если она возникает, то .\psql)
     - ввод пароля (свой пароль)
     - также изменить пароль в файле app.py
  3. Сохранить изменения
  4. Win+X -> Power Shell (Администратор)
  5. Прописать pip install python3
  6. cd "<Путь до файла app.py>"
  7. python app.py
2) С использованием Docker:
  1. Через консоль:
     - Скачать образ
     - Win+X -> Power Shell (Администратор)
     - docker run <название образа>
  2. Через приложение
     - Найти контейнер 
     - Запустить его
