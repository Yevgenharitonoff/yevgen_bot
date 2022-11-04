import sqlite3


conn = sqlite3.connect('database.sqlite3')
cur = conn.cursor()

# таблица Типы расходов
cur.execute("""CREATE TABLE IF NOT EXISTS `expenditure_types`(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# таблица Типы расходов
cur.execute("""CREATE TABLE IF NOT EXISTS `income_types`(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# таблица Расходы
cur.execute("""CREATE TABLE IF NOT EXISTS `expenditures`(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    typeID INTEGER NOT NULL,
    value FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(typeID) REFERENCES expenditure_types(id) ON UPDATE CASCADE ON DELETE CASCADE
);
""")

# таблица Доходы
cur.execute("""CREATE TABLE IF NOT EXISTS `incomes`(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    typeID INTEGER NOT NULL,
    value FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(typeID) REFERENCES income_types(id) ON UPDATE CASCADE ON DELETE CASCADE
);
""")

# **************************************************************************************************
cur.execute("""INSERT INTO `expenditure_types` (name) VALUES 
('Одежда'),
('Дом'),
('Здоровье'),
('Автомобиль'),
('Домашние животные')
;
""")

# **************************************************************************************************
cur.execute("""INSERT INTO `income_types` (name) VALUES 
('Зарплата'),
('Подарки'),
('Другие')
;
""")

conn.commit() # раскомментируйте, чтобы добавить данные
cur.close()
conn.close()
