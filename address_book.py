from collections import UserDict

class IncorrectPhone(Exception):
    pass

class IncorrectName(Exception):
    pass

class NameNotFound(Exception):
    pass

class PhoneNotFound(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.value = self.validate(name)

    def validate(self, name):
        if not name:
            raise IncorrectName("Name can't be empty")
        return name

class Phone(Field):
    def __init__(self, phone):
        self.value = self.validate(phone)

    def validate(self, phone):
        if not phone.isdigit():
            raise IncorrectPhone("Phone number must contain only digits")
        if len(phone) != 10:
            raise IncorrectPhone("Phone number must be 10 digits long")
        return phone

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = phone.validate(new_phone)
                return
        raise PhoneNotFound(f"Phone {old_phone} not found")

    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        raise PhoneNotFound(f"Phone {phone} not found")

    def remove_phone(self, phone_to_remove):
        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                return
        raise PhoneNotFound(f"Phone {phone} not found")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return
        raise NameNotFound(f"Record with name {name} not found")

    def find(self, name):
        if name in self.data:
            return self.data[name]
        raise NameNotFound(f"Record with name {name} not found")


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
john.remove_phone("5555555555")

# Видалення запису Jane
book.delete("Jane")

print("-" * 20)
# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

print("-" * 20)

try:
    # Пошук запису, якого немає у книзі
    book.find("Jane")
except NameNotFound as e:
    print(e)

try:
    # Редагування телефону, якого немає у записі
    john.edit_phone("1234567890", "1112223333")
except PhoneNotFound as e:
    print(e)

try:
    # Пошук телефону, якого немає у записі
    john.find_phone("1234567890")
except PhoneNotFound as e:
    print(e)

try:
    # Спроба створити запис з пустим ім'ям
    empty_name = Record("")
except IncorrectName as e:
    print(e)

try:
    # Спроба створити запис з неправильним номером телефону
    incorrect_phone = Record("Incorrect")
    incorrect_phone.add_phone("123")
except IncorrectPhone as e:
    print(e)
