### Завдання
# - зберігати контакти з іменами, адресами, номерами телефонів, email та 
# днями народження до книги контактів;
# - виводити список контактів, у яких день народження через задану кількість днів від поточної дати;
# - перевіряти правильність введеного номера телефону та email під час створення 
# або редагування запису та повідомляти користувача у разі некоректного введення;
# - здійснювати пошук контактів серед контактів книги;
# - редагувати та видаляти записи з книги контактів;
# - зберігати нотатки з текстовою інформацією;
# - проводити пошук за нотатками;
# - редагувати та видаляти нотатки;
# - додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;
# - здійснювати пошук та сортування нотаток за ключовими словами (тегами);
# - сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).

# Додаткове ускладнене завдання: Бот повинен аналізувати введений текст і намагатися вгадати, 
# що хоче від нього користувач і запропонувати найближчу команду для виконання


from collections import UserDict
from datetime import datetime
import pickle, csv


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        # print(value.__class__)
        if (type(value) == int) and (len(str(value)) == 12): #перевірка правильності введеного номера телефону
            self.__value = value



class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if type(value) == datetime: #перевірка правильності введеної дати народження
            self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None):
        self.name = name
        self.phone = []
        self.birthday = birthday
        if phone:
            self.phone.append(phone)

    def __str__(self):
        return f"{self.name.value} {[ph.value for ph in self.phone]} {self.birthday.value}"
        
    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phone:
            self.phone.append(phone_number)

    def delete_phone(self, phone):
        self.phone.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phone.index(old_phone)
        self.phone[index] = new_phone

    def days_to_birthday(self, birthday): #повертає кількість днів до наступного дня народження
        current_date = datetime.now().date()
        if birthday:
            birthday_date = birthday.replace(year=datetime.now().year).date() 
            delta = birthday_date - current_date
            if delta.days >= 0:
                return f'{delta.days} days to birthday'
            else:
                delta = birthday_date.replace(year=datetime.now().year+1) - current_date
                return f'{delta.days} days to birthday'
        else:
            return None


class AddressBook(UserDict):
    N = 2

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        # {‘Bill’: “Bill 0987777 22.09.2000”} - результат add_record
    
    def find_record(self, value): #пошук контакта за іменем(тобто по ключу)
        return self.data.get(value)    

    def search(self, value): #пошук контактів за декількома літерами або цифрами
        result = []
        for cont in self.data.values():
            for ph in cont.phone:
                if value in str(ph.value):
                    result.append(f'{cont}')
                        
            if value in cont.name.value:
                    result.append(f'{cont}')
        return result if result != [] else f"No results for: {value}"        

    def iterator(self, n) -> list[dict]: #посторінковий вивід на екран контактів
        contact_list = []  # список записів контактів
        if n:
            AddressBook.N = n
        for record in self.data.values():
            contact_list.append(record)
        return self.__next__(contact_list)
    
    def __iter__(self, contact_list: list[dict]):
        n_list = []
        counter = 0
        for contact in contact_list:
            n_list.append(contact)
            counter += 1
            if counter >= AddressBook.N:  # якщо вже створено список із заданої кількості записів
                yield n_list
                n_list.clear()
                counter = 0
        yield n_list

    def __next__(self, contact_list):
        generator = self.__iter__(contact_list)
        page = 1
        while True:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result = next(generator)
                    if result:
                        print(f"{'*' * 20} Page {page} {'*' * 20}")
                        page += 1
                    for var in result:
                        print(var)
                except StopIteration:
                    print(f"{'*' * 20} END {'*' * 20}")
                    break
            else:
                break
    
    def save_to_file(self, filename): #збереження адресної книги на диск
        self.filename = filename
        with open(self.filename, 'wb') as fh:
            pickle.dump(self, fh)

    def read_from_file(self, filename): #відновлення адресної книги з диска
        self.filename = filename
        with open(self.filename, 'rb') as fh:
            unpacked = pickle.load(fh)
        return unpacked



# ### Checking mentor
if __name__ == "__main__":
    # record contact 1
    name = Name('Bill')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(1990, 8, 3))
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
    rec.add_phone(380999876543)
    
    # record contac 2
    name2 = Name('Mary')
    phone2 = Phone(987654321012)
    birthday2 = Birthday(datetime(1993, 9, 25))
    rec2 = Record(name2, phone2, birthday2)
    ab.add_record(rec2)
    
    """Додамо контактів для перевірки ітератора"""
    name = Name('Bob')
    phone = Phone(343456789012)
    birthday = Birthday(datetime(1980, 1, 31))
    rec2 = Record(name, phone, birthday)

    name = Name('Tom')
    phone = Phone(433456789015)
    birthday = Birthday(datetime(1992, 12, 13))
    rec3 = Record(name, phone, birthday)

    name = Name('Bard')
    phone = Phone(153455789062)
    birthday = Birthday(datetime(2000, 4, 10))
    rec4 = Record(name, phone, birthday)

    ab.add_record(rec2)
    ab.add_record(rec3)
    ab.add_record(rec4)
    # ab.iterator(n=3)

    """Збереження у файл"""
    # print(ab)
    # ab.save_to_table('mod12_ab_mary.csv')
    # ab.save_to_file('mod12_ab_mary.bin')
    # ab_from_file = ab.read_from_file('mod12_ab_mary.bin')
    # print(ab_from_file)

    """Пошук вмісту книги контактів"""
    # print(ab)
    # print(ab.find_record('Mary'))
    print(ab.search('ar'))

    print('All Ok)')
