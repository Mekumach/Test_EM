import json


class Book:
    """Класс для представления книги в библиотеке."""

    def __init__(self, title: str, author: str, year: int):
        self.id = id(self)  # Уникальный идентификатор
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"  # По умолчанию книга доступна

    def to_dict(self) -> dict:
        """Преобразование объекта книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создание объекта книги из словаря."""
        book = Book(data["title"], data["author"], data["year"])
        book.id = data["id"]
        book.status = data["status"]
        return book


class Library:
    """Класс для управления библиотекой."""

    def __init__(self, file_path: str = "library.json"):
        self.file_path = file_path
        self.books: list[Book] = []
        self.load_books()

    def load_books(self):
        """Загрузка данных из файла."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            self.books = []

    def save_books(self):
        """Сохранение данных в файл."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавление новой книги в библиотеку."""
        new_book = Book(title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' успешно добавлена с id {new_book.id}.")

    def delete_book(self, book_id: int):
        """Удаление книги по id."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с id {book_id} успешно удалена.")
                return
        print(f"Книга с id {book_id} не найдена.")

    def search_books(self, **criteria) -> list[Book]:
        """Поиск книг по заданным критериям."""
        result = self.books
        for key, value in criteria.items():
            if key == "id":  # Если поиск по ID
                result = [book for book in result if book.id == int(value)]
            else:  # Поиск по другим строковым критериям
                result = [book for book in result if str(getattr(book, key, "")).lower() == str(value).lower()]
        return result

    def display_books(self):
        """Отображение всех книг."""
        if not self.books:
            print("В библиотеке нет книг.")
        for book in self.books:
            print(
                f"ID: {book.id} | Название: {book.title} | Автор: {book.author} | "
                f"Год: {book.year} | Статус: {book.status}")

    def update_status(self, book_id: int, status: str):
        """Изменение статуса книги."""
        if status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Выберите 'в наличии' или 'выдана'.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                print(f"Статус книги с id {book_id} изменён на '{status}'.")
                return
        print(f"Книга с id {book_id} не найдена.")


def main():
    """Основной интерфейс командной строки."""
    library = Library()

    while True:
        print("\n--- Система управления библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
        elif choice == "2":
            while True:
                try:
                    book_id = int(input("Введите ID книги для удаления: "))
                    break
                except ValueError:
                    print("Некорректный ввод. ID должен быть числом. Попробуйте снова.")
            library.delete_book(book_id)
        elif choice == "3":
            print("Выберите критерий поиска:")
            print("1. ID")
            print("2. Название")
            print("3. Автор")
            print("4. Год")
            search_choice = input("Введите номер критерия: ")
            if search_choice == "1":
                while True:
                    try:
                        book_id = int(input("Введите ID книги: "))
                        break
                    except ValueError:
                        print("Некорректный ввод. ID должен быть числом. Попробуйте снова.")
                result = library.search_books(id=book_id)
            elif search_choice == "2":
                title = input("Введите название книги: ")
                result = library.search_books(title=title)
            elif search_choice == "3":
                author = input("Введите автора книги: ")
                result = library.search_books(author=author)
            elif search_choice == "4":
                year = int(input("Введите год издания: "))
                result = library.search_books(year=year)
            else:
                print("Некорректный выбор.")
                continue
            if result:
                for book in result:
                    print(
                        f"ID: {book.id} | Название: {book.title} | Автор: {book.author} | "
                        f"Год: {book.year} | Статус: {book.status}")
            else:
                print("Книги не найдены.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            while True:
                try:
                    book_id = int(input("Введите ID книги: "))
                    break
                except ValueError:
                    print("Некорректный ввод. ID должен быть числом. Попробуйте снова.")
            status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
