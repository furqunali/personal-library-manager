import json

class PersonalLibrary:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.load_library()

    def load_library(self):
        try:
            with open(self.filename, "r") as file:
                self.library = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.library = []

    def save_library(self):
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title):
        self.library.append(title)
        self.save_library()
        print(f"Book '{title}' added!")

    def view_books(self):
        if not self.library:
            print("No books in library.")
        else:
            for i, book in enumerate(self.library, start=1):
                print(f"{i}. {book}")


def main():
    lib = PersonalLibrary()
    while True:
        print("\nLibrary Manager")
        print("1. Add Book")
        print("2. View Books")
        print("3. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            lib.add_book(title)
        elif choice == "2":
            lib.view_books()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
