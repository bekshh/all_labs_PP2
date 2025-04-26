import psycopg2
import csv
import re
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
        self._create_procedures()
    
    def _create_procedures(self):
        """Create necessary stored procedures in the database"""
        try:
            # ... (остальные процедуры остаются без изменений)
            
            # Обновленная процедура для массовой вставки
            self.cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_many_users(
                    INOUT invalid_data_ref TEXT,
                    users TEXT[][]
                )
                AS $$
                DECLARE
                    user_record TEXT[];
                    phone_pattern TEXT := '^\+?[0-9]{10,15}$';
                    invalid_cursor REFCURSOR;
                BEGIN
                    -- Создаем временную таблицу для невалидных записей
                    CREATE TEMP TABLE IF NOT EXISTS temp_invalid (
                        name TEXT,
                        phone TEXT,
                        reason TEXT
                    ) ON COMMIT DROP;
                    
                    TRUNCATE temp_invalid;
                    
                    -- Обрабатываем каждую запись
                    FOREACH user_record SLICE 1 IN ARRAY users
                    LOOP
                        -- Проверки валидности...
                        -- (остальной код проверок остается без изменений)
                    END LOOP;
                    
                    -- Открываем курсор с результатами
                    invalid_cursor := invalid_data_ref;
                    OPEN invalid_cursor FOR SELECT * FROM temp_invalid;
                END;
                $$ LANGUAGE plpgsql;
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Error creating procedures: {e}")
            self.conn.rollback()
    
    def create_table(self):
        """Create PhoneBook table"""
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
            self.conn.rollback()
    
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
            self.conn.rollback()
    
    def update_contact(self, name, phone):
        """Обновление данных контакта"""
        try:
            # Проверяем существует ли контакт
            self.cur.execute("SELECT COUNT(*) FROM phonebook WHERE first_name = %s OR phone = %s", 
                           (name, phone))
            if self.cur.fetchone()[0] == 0:
                print("Ошибка: контакт не найден!")
                return
            
            if name:
                self.cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", 
                               (phone, name))
            else:
                self.cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s", 
                               (name, phone))
            
            self.conn.commit()
            print("Контакт успешно обновлен!")
        except Exception as e:
            print(f"Ошибка при обновлении контакта: {e}")
            self.conn.rollback()
    
    def query_contacts(self):
        """Поиск контактов с фильтрами"""
        print("\nПоиск контактов")
        print("1 - По имени")
        print("2 - По фамилии")
        print("3 - По телефону")
        print("4 - По email")
        print("5 - Показать все контакты")
        choice = input("Ваш выбор (1-5): ")
        
        try:
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
        except Exception as e:
            print(f"Ошибка при поиске контактов: {e}")
    
    def delete_contact(self):
        """Удаление контакта"""
        print("\nУдаление контакта")
        print("1 - По имени")
        print("2 - По телефону")
        choice = input("Ваш выбор (1-2): ")
        
        try:
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
        except Exception as e:
            print(f"Ошибка при удалении контакта: {e}")
            self.conn.rollback()
    
    def search_by_pattern(self, pattern):
        """Поиск по шаблону в любом поле"""
        if not pattern:
            print("Search pattern cannot be empty")
            return []
        
        try:
            like_pattern = f"%{pattern}%"
            self.cur.execute("""
                SELECT * FROM phonebook 
                WHERE first_name ILIKE %s 
                   OR last_name ILIKE %s 
                   OR phone LIKE %s 
                   OR email ILIKE %s
            """, (like_pattern, like_pattern, like_pattern, like_pattern))
            
            rows = self.cur.fetchall()
            if not rows:
                print("No contacts found matching the pattern")
            else:
                print("\nMatching contacts:")
                for row in rows:
                    print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}, Email: {row[4]}")
            return rows
        except Exception as e:
            print(f"Error searching by pattern: {e}")
            return []
    
    def insert_or_update_user(self, name, phone):
        """Insert new user or update phone if user exists"""
        try:
            # Используем CALL для вызова процедуры
            self.cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
            self.conn.commit()
            print(f"User '{name}' processed successfully!")
            return True
        except Exception as e:
            print(f"Error in insert_or_update_user: {e}")
            self.conn.rollback()
            return False

    
    def insert_many_users(self, users):
        """
        Insert multiple users with validation
        users: list of tuples (name, phone)
        Returns invalid records
        """
        try:
            # Convert users list to 2D array format for PostgreSQL
            users_array = [[name, phone] for name, phone in users]
            
            # Begin transaction
            self.cur.execute("BEGIN;")
            
            # Call the procedure and get the cursor name
            cursor_name = "invalid_data_cursor"
            self.cur.execute(
                "CALL insert_many_users(%s, %s);", 
                (cursor_name, users_array)
            )
            
            # Fetch results from the cursor
            self.cur.execute(f"FETCH ALL FROM {cursor_name};")
            invalid_records = self.cur.fetchall()
            
            # Close the cursor
            self.cur.execute(f"CLOSE {cursor_name};")
            
            self.conn.commit()
            
            if invalid_records:
                print("\nInvalid records:")
                for record in invalid_records:
                    print(f"Name: {record[0]}, Phone: {record[1]}, Reason: {record[2]}")
            else:
                print("All records were inserted successfully!")
            
            return invalid_records
        except Exception as e:
            print(f"Error in insert_many_users: {e}")
            self.conn.rollback()
            return []
    
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
            print("7 - Поиск по шаблону")
            print("8 - Вставить/обновить пользователя")
            print("9 - Вставить несколько пользователей")
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
                name = input("Name: ")
                phone = input("Phone number: ")
                self.update_contact(name, phone)
            elif choice == '5':
                self.query_contacts()
            elif choice == '6':
                self.delete_contact()
            elif choice == '7':
                pattern = input("Enter search pattern: ")
                self.search_by_pattern(pattern)
            elif choice == '8':
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                self.insert_or_update_user(name, phone)
            elif choice == '9':
                print("Enter users in format 'name,phone' (one per line). Enter 'done' when finished.")
                users = []
                while True:
                    entry = input("> ")
                    if entry.lower() == 'done':
                        break
                    parts = entry.split(',')
                    if len(parts) == 2:
                        users.append((parts[0].strip(), parts[1].strip()))
                    else:
                        print("Invalid format. Use 'name,phone'")
                if users:
                    self.insert_many_users(users)
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