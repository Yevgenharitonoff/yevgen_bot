import sqlite3


class DataAccessor:
    def __init__(self, dbname):
        self.dbname = dbname
        self.periods = {
            "1": "created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')",
            "2": "created_at BETWEEN datetime('now', '-182 days') AND datetime('now', 'localtime')",
            "3": "created_at BETWEEN datetime('now', '-365 days') AND datetime('now', 'localtime')",
        }

    def get_incomes_expenditures(self, where="1"):
        expenditures, incomes = [], []

        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()

            self.cursor.execute("""SELECT id, SUM(value) FROM expenditures
                WHERE %s
                GROUP BY id, value
            """%self.periods.get(where))

            expenditures = self.cursor.fetchall()

            self.cursor.execute("""SELECT id, SUM(value) FROM incomes
                WHERE %s
                GROUP BY id, value
            """%self.periods.get(where))

            incomes = self.cursor.fetchall()

            return expenditures, incomes
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            # print("СОЕДИНЕНИЕ ЗАКРЫТО")
            self.cursor.close()
            self.connection.close()
            return expenditures, incomes

    def add_expend(self, type_id, value):
        table = "expenditures"
        columns = "typeID, value"
        values = str(type_id) + "," + str(value)

        return self.__insert_query(table, columns, values)

    def add_income(self, type_id, value):
        table = "incomes"
        columns = "typeID, value"
        values = str(type_id) + "," + str(value)

        return self.__insert_query(table, columns, values)

    def __select_query(self, columns, table, where=None):
        data = []
        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()

            if where:
                self.cursor.execute("""SELECT %s FROM %s WHERE %s"""%(columns, table, where))
            else:
                self.cursor.execute("""SELECT %s FROM %s"""%(columns, table))

            data = self.cursor.fetchall()

            return data
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, columns, table)
        finally:
            # print("СОЕДИНЕНИЕ ЗАКРЫТО")
            self.cursor.close()
            self.connection.close()
            return data

    def __insert_query(self, table, columns, values):
        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()

            self.cursor.execute("""INSERT INTO %s (%s) VALUES (%s)"""%(table, columns, values))
            self.connection.commit()

            return self.cursor.lastrowid
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, table, columns, values)
            return 0
        finally:
            # print("СОЕДИНЕНИЕ ЗАКРЫТО")
            self.cursor.close()
            self.connection.close()

    def __update_query(self, query):
        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()

            self.cursor.execute(query)
            self.connection.commit()

            return self.cursor.lastrowid
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, query)
            return 0
        finally:
            # print("СОЕДИНЕНИЕ ЗАКРЫТО")
            self.cursor.close()
            self.connection.close()

    def __delete_query(self, table_name, column, value):
        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()

            self.cursor.execute("DELETE FROM %s WHERE %s=%s"%(table_name, column, value))
            self.connection.commit()

            return self.cursor.lastrowid
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, table_name, column, value)
            return 0
        finally:
            # print("СОЕДИНЕНИЕ ЗАКРЫТО")
            self.cursor.close()
            self.connection.close()
