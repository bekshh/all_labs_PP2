import psycopg2
import csv
from psycopg2 import sql

class PhoneBook:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="phonebook",
            user="bekshh",  
            password="wldr007"  
        )
        self.cur = self.conn.cursor()
    
    def create_table(self):
        """Создание таблицы PhoneBook"""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                phone VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        print("Таблица phonebook создана успешно!")
    
    def insert_from_csv(self, filename):
        """Вставка данных из CSV файла"""
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # пропускаем заголовок
                for row in reader:
                    self.cur.execute(
                        "INSERT INTO phonebook (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                        row
                    )
            self.conn.commit()
            print(f"Данные из {filename} успешно загружены!")
        except Exception as e:
            print(f"Ошибка при загрузке из CSV: {e}")
    
    def insert_from_console(self):
        """Ввод данных с консоли"""
        print("\nВведите данные контакта:")
        first_name = input("Имя: ")
        last_name = input("Фамилия (необязательно): ")
        phone = input("Телефон: ")
        email = input("Email (необязательно): ")
        
        try:
            self.cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, phone, email)
            )
            self.conn.commit()
            print("Контакт успешно добавлен!")
        except Exception as e:
            print(f"Ошибка при добавлении контакта: {e}")
    
    def update_contact(self):
        """Обновление данных контакта"""
        print("\nОбновление контакта")
        phone = input("Введите телефон контакта для обновления: ")
        
        print("Что вы хотите изменить?")
        print("1 - Имя")
        print("2 - Фамилию")
        print("3 - Телефон")
        print("4 - Email")
        choice = input("Ваш выбор (1-4): ")
        
        field = None
        new_value = None
        
        if choice == '1':
            field = 'first_name'
            new_value = input("Новое имя: ")
        elif choice == '2':
            field = 'last_name'
            new_value = input("Новая фамилия: ")
        elif choice == '3':
            field = 'phone'
            new_value = input("Новый телефон: ")
        elif choice == '4':
            field = 'email'
            new_value = input("Новый email: ")
        else:
            print("Неверный выбор!")
            return
        
        try:
            query = sql.SQL("UPDATE phonebook SET {} = %s WHERE phone = %s").format(
                sql.Identifier(field)
            )
            self.cur.execute(query, (new_value, phone))
            self.conn.commit()
            print("Контакт успешно обновлен!")
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")
    
    def query_contacts(self):
        """Поиск контактов с фильтрами"""
        print("\nПоиск контактов")
        print("1 - По имени")
        print("2 - По фамилии")
        print("3 - По телефону")
        print("4 - По email")
        print("5 - Показать все контакты")
        choice = input("Ваш выбор (1-5): ")
        
        if choice == '1':
            name = input("Введите имя: ")
            self.cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
        elif choice == '2':
            last_name = input("Введите фамилию: ")
            self.cur.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s", (f"%{last_name}%",))
        elif choice == '3':
            phone = input("Введите телефон: ")
            self.cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f"%{phone}%",))
        elif choice == '4':
            email = input("Введите email: ")
            self.cur.execute("SELECT * FROM phonebook WHERE email ILIKE %s", (f"%{email}%",))
        elif choice == '5':
            self.cur.execute("SELECT * FROM phonebook")
        else:
            print("Неверный выбор!")
            return
        
        rows = self.cur.fetchall()
        if not rows:
            print("Контакты не найдены")
        else:
            print("\nНайденные контакты:")
            for row in rows:
                print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}, Email: {row[4]}")
    
    def delete_contact(self):
        """Удаление контакта"""
        print("\nУдаление контакта")
        print("1 - По имени")
        print("2 - По телефону")
        choice = input("Ваш выбор (1-2): ")
        
        if choice == '1':
            name = input("Введите имя для удаления: ")
            self.cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        elif choice == '2':
            phone = input("Введите телефон для удаления: ")
            self.cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Неверный выбор!")
            return
        
        self.conn.commit()
        print(f"Удалено {self.cur.rowcount} контактов")
    
    def show_menu(self):
        """Главное меню"""
        while True:
            print("\n--- PhoneBook Menu ---")
            print("1 - Создать таблицу")
            print("2 - Загрузить из CSV")
            print("3 - Добавить вручную")
            print("4 - Обновить контакт")
            print("5 - Поиск контактов")
            print("6 - Удалить контакт")
            print("0 - Выход")
            
            choice = input("Ваш выбор: ")
            
            if choice == '1':
                self.create_table()
            elif choice == '2':
                filename = input("Введите имя CSV файла: ")
                self.insert_from_csv(filename)
            elif choice == '3':
                self.insert_from_console()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.query_contacts()
            elif choice == '6':
                self.delete_contact()
            elif choice == '0':
                print("Выход...")
                break
            else:
                print("Неверный выбор!")
        
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    pb = PhoneBook()
    pb.show_menu()