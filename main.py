import sqlite3
import json
import os

# Встановлення з'єднання з базою даних (якщо база даних не існує, вона буде створена)
conn = sqlite3.connect('books.db')

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor()

# Створення таблиці "books" з потрібними полями
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        publication_year INTEGER
    )
''')

# Збереження змін до бази даних
conn.commit()

# Закриття з'єднання з базою даних
conn.close()



def print_all_books():
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Вибірка всіх книг з бази даних
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()

    # Виведення результатів
    for book in all_books:
        print(book)

    # Закриття з'єднання з базою даних
    conn.close()

    print()

def add_book(title, author, publication_year):
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Перевірка, чи існує книга з такою ж назвою в базі даних
    cursor.execute('SELECT * FROM books WHERE title = ?', (title,))
    existing_book = cursor.fetchone()

    if existing_book:
        print('Книга з такою назвою вже існує в базі даних.\n')
    else:
        # Додавання нової книги в таблицю
        cursor.execute('INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)', (title, author, publication_year))
        print('Книга успішно додана до бази даних.\n')

    # Збереження змін до бази даних
    conn.commit()

    # Закриття з'єднання з базою даних
    conn.close()

def delete_book_by_id(book_id):
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Вибірка книги з бази даних за заданим ID
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        # Виведення знайденої книги
        print('\nЗнайдена книга:')
        print(book)

        # Перепитування користувача
        confirm = input('Ви впевнені, що хочете видалити цю книгу? (y/n): ')

        if confirm.lower() == 'y':
            # Видалення книги з бази даних
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            print('Книга успішно видалена з бази даних.\n')
        else:
            print('Видалення книги скасоване.\n')
    else:
        print('Книга з таким ID не знайдена в базі даних.\n')

    # Збереження змін до бази даних
    conn.commit()

    # Закриття з'єднання з базою даних
    conn.close()

def search_books_by_term(search_term):
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Пошук книги за ID, назвою, автором або роком видання
    cursor.execute('SELECT * FROM books WHERE id = ? OR title LIKE ? OR author LIKE ? OR publication_year = ?',
                   (search_term, f'%{search_term}%', f'%{search_term}%', search_term))
    books = cursor.fetchall()

    if books:
        print(f'Знайдено {len(books)} книг(и):')

        for book in books:
            print(book)
    else:
        print('Книги за вказаним пошуковим запитом не знайдено.')

    print()

    # Закриття з'єднання з базою даних
    conn.close()

def edit_book_by_id(book_id):
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Вибірка книги з бази даних за заданим ID
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        # Виведення знайденої книги
        print('\nЗнайдена книга:')
        print(book)

        # Запит на введення нових даних
        title = input('Введіть нову назву книги: ')
        author = input('Введіть нового автора книги: ')
        publication_year = input('Введіть новий рік видання книги: ')

        # Оновлення даних книги в базі даних
        cursor.execute('UPDATE books SET title = ?, author = ?, publication_year = ? WHERE id = ?', (title, author, publication_year, book_id))
        print('Книга успішно оновлена.\n')
    else:
        print('Книга з таким ID не знайдена в базі даних.\n')

    # Збереження змін до бази даних
    conn.commit()

    # Закриття з'єднання з базою даних
    conn.close()

def clear_database():
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Перевірка підтвердження користувача
    confirmation = input('Ви впевнені, що хочете видалити всі дані з бази даних? (y/n): ')

    if confirmation.lower() == 'y':
        # Видалення всіх даних з бази даних
        cursor.execute('DELETE FROM books')
        print('База даних була успішно очищена.\n')
    else:
        print('Очищення бази даних скасоване.\n')

    # Збереження змін до бази даних
    conn.commit()

    # Закриття з'єднання з базою даних
    conn.close()

def export_database():
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Вибірка всіх даних з бази даних
    cursor.execute('SELECT * FROM books')
    data = cursor.fetchall()

    # Конвертування даних у список словників
    books = []
    for row in data:
        book = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'publication_year': row[3]
        }
        books.append(book)

    # Генерація унікальної назви файлу
    counter = 1
    while True:
        filename = f'booksDB{counter}.json'
        if not os.path.exists(filename):
            break
        counter += 1

    # Запис даних у файл JSON
    with open(filename, 'w') as file:
        json.dump(books, file)

    print(f'База даних була успішно експортована до файлу {filename}.')
    print(f'Шлях до новоствореного файлу: {os.path.abspath(filename)}\n')

    # Закриття з'єднання з базою даних
    conn.close()

def import_database():
    # Запит шляху до файлу
    file_path = input('Введіть шлях до файлу: ')

    try:
        # Відкриття файлу та зчитування даних
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Встановлення з'єднання з базою даних
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()

        # Отримання максимального ID з бази даних
        cursor.execute('SELECT MAX(id) FROM books')
        max_id = cursor.fetchone()[0]

        # Перевірка, якщо база даних порожня
        if max_id is None:
            max_id = 0

        # Додавання книг з файлу до бази даних
        if isinstance(data, list):
            for book in data:
                if isinstance(book, dict):
                    max_id += 1
                    title = book.get('title')
                    author = book.get('author')
                    publication_year = book.get('publication_year')
                    cursor.execute('INSERT INTO books VALUES (?, ?, ?, ?)', (max_id, title, author, publication_year))
                else:
                    print(f'Помилка: неправильний формат даних книги.\n')
        elif isinstance(data, dict):
            max_id += 1
            title = data.get('title')
            author = data.get('author')
            publication_year = data.get('publication_year')
            cursor.execute('INSERT INTO books VALUES (?, ?, ?, ?)', (max_id, title, author, publication_year))
        else:
            print(f'Помилка: неправильний формат даних.\n')

        print(f'Книги з файлу {file_path} були успішно додані до бази даних.\n')

        # Збереження змін до бази даних
        conn.commit()

        # Закриття з'єднання з базою даних
        conn.close()

    except FileNotFoundError:
        print(f'Файл {file_path} не знайдено.\n')

    except json.JSONDecodeError:
        print(f'Помилка при зчитуванні даних з файлу {file_path}. Файл має неправильний формат.\n')



def main_menu():
    while True:
        print('Меню:')
        print('1. Переглянути всі книги')
        print('2. Додати нову книгу')
        print('3. Видалити книгу за ID')
        print('4. Пошук книг за ID, назвою, автором або роком')
        print('5. Редагувати книги за ID')
        print('6. Очистити базу даних')
        print('7. Експортувати базу даних в JSON')
        print('8. Імпортувати книги з JSON')
        print('0. Вийти з програми')

        choice = input('Виберіть опцію: ')

        if choice == '1':
            print_all_books()

        elif choice == '2':
            title = input('Введіть назву книги: ')
            author = input('Введіть автора книги: ')
            publication_year = input('Введіть рік видання книги: ')
            add_book(title, author, publication_year)

        elif choice == '3':
            book_id = input('Введіть ID книги, яку потрібно видалити: ')
            delete_book_by_id(book_id)

        elif choice == '4':
            search_term = input('Введіть пошуковий термін: ')
            search_books_by_term(search_term)

        elif choice == '5':
            book_id = input('Введіть ID книги, яку потрібно оновити: ')
            edit_book_by_id(book_id)

        elif choice == '6':
            clear_database()

        elif choice == '7':
            export_database()

        elif choice == '8':
            import_database()

        elif choice == '0':
            break

        else:
            print('Невірний вибір. Спробуйте ще раз.\n')

main_menu()