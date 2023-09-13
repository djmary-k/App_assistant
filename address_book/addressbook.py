from collections import UserDict
from address_book.record import *
from address_book.change import *
import warnings
import pickle
import os
from datetime import datetime, timedelta
from address_book.myexception import *


class ABIterator:
    """
    this class represents an iterator over the records in an address book.
    """

    def __init__(self, collection, n=None):
        """
        Initializes the iterator.
        :param collection: collection over with the iterator will iterate. Expected: dict with records.
        :param n: number of objects from the collection which have to be returned in one iteration.
                    If None, all objects will be returned at once.
        """
        self.collection = None
        self.set_collection(collection)
        self.n = None
        self.set_n(n)
        self.start_idx = 0

    def set_collection(self, new_collection):
        """
        Validates and sets a new collection to iterate over.
        :param new_collection: new collection
        """
        if not new_collection:
            self.collection = None
        else:
            try:
                self.collection = list(new_collection)
            except Exception:
                raise ValueError(f"The collection {new_collection} for iteration is not iterable.")

    def set_n(self, new_n: int):
        """
        Validates and sets a new value for the parameter "n": number of elements returned in one iteration.
        Throws an exception if the new value is not valid: must be a positive integer number.
        :param new_n: new value for the parameter "n".
        """
        if not new_n:
            self.n = None
            return
        try:
            new_n = int(new_n)
            if new_n <= 0:
                raise MyException()
            self.n = new_n
        except Exception:
            raise MyIteratorNException(f"Positive integer number is expected as a parameter for iteration, provided: '{new_n}")

    def __iter__(self):
        return self

    def __next__(self):
        if not self.collection:
            raise StopIteration
        elif self.start_idx >= len(self.collection):
            raise StopIteration
        elif not self.n:
            self.start_idx = len(self.collection)
            return AddressBook.display_records(self.collection)
        else:
            end_idx = min(self.start_idx + self.n, len(self.collection))
            res = self.collection[self.start_idx: end_idx]
            res = AddressBook.display_records(res, self.start_idx)
            self.start_idx = end_idx
            return res


class AddressBook(UserDict):
    """
    Class representing the address book.
    """
    @staticmethod
    def display_records(data, prev_id=0):
        res = "\n\n".join(f"{prev_id + pos + 1}. {record.to_string()}" for pos, record in enumerate(data))
        return res

    def __init__(self, username="defaultuser"):
        """
        Initiates the AddressBook object.
        :param username: name of the owner of the address book.
        """
        super(AddressBook, self).__init__(self)
        self.username = username    # owner of the address book
        self.n = None               # number of records to be returned per one iteration

    def get_username(self):
        return self.username

    def set_username(self, new_name):
        self.username = new_name

    def set_number_records_per_iteration(self, new_n: int):
        """
        Validates and sets a new value for the parameter "n": number of records to be returned in one iteration.
        Throws an exception if the new value is not valid: must be a positive integer number.
        :param new_n: new value for the parameter "n".
        """
        if not new_n:
            self.n = None
        try:
            new_n = int(new_n)
            if new_n <= 0:
                raise MyException()
            self.n = new_n
        except:
            raise MyException(f"Positive integer number is expected as a parameter for iteration, provided: '{new_n}")

    def add_record(self, record: Record):
        """
        Adds a new record to the address book.
        :param record: new record to be added to the address book.
        :return: None.
        """
        if record.get_name() in self.data:
            warnings.warn(f"WARNING: the record for the contact '{record.get_name()}' gets overwritten.")
        self.data[record.get_name()] = record

    def delete_record(self, name: str):
        """
        Deletes a record from the address book.
        :param name: contact name stored in the record which has to be deleted.
        :return: None.
        """
        try:
            del self.data[name]
        except KeyError:
            raise MyException(f"The record for the contact '{name}' cannot be deleted: this name is not in the "
                              f"address book.")

    def edit_record_name(self, old_name: str, new_name: str):
        """
        Changes the contact name within a record. Updates the way the record is stored in the address book.
        :param old_name: old name stored in a record that has to be changed.
        :param new_name: new name to replace the old one.
        :return: None.
        """
        try:
            record = self.data.pop(old_name)
            record.edit_name(new_name)
            self.add_record(record)
            return record
        except KeyError:
            raise MyException(f"Cannot change the name of a record: the name '{old_name}' is not in the address book.")

    def edit_record(self, change: Change):
        """
        Conducts changes specified by the Change object.
        :param change: object containing information about the change which has to be performed.
        :return: None.
        """
        name = change.get_name()
        changetype = change.get_changetype()
        kwargs = change.get_kwargs()
        record = self.get_record_by_name(name)
        match changetype:
            case ChangeType.EDIT_NAME:
                record = self.edit_record_name(old_name=name, new_name=kwargs["new_name"])
            case ChangeType.EDIT_PHONE:
                record.edit_phone_number(**kwargs)
            case ChangeType.EDIT_EMAIL:
                record.edit_email(**kwargs)
            case ChangeType.ADD_PHONE:
                record.add_phone_number(**kwargs)
            case ChangeType.ADD_EMAIL:
                record.add_email(**kwargs)
            case ChangeType.REMOVE_PHONE:
                record.remove_phone_number(**kwargs)
            case ChangeType.REMOVE_EMAIL:
                record.remove_email(**kwargs)
            case ChangeType.EDIT_BIRTHDAY:
                record.edit_birthday(**kwargs)
            case ChangeType.REMOVE_BIRTHDAY:
                record.remove_birthday()
            case ChangeType.EDIT_ADDRESS:
                record.edit_address(**kwargs)
            case ChangeType.REMOVE_ADDRESS:
                record.remove_address()
            case _:
                raise MyException("Change type is unknown.")
        return record

    def get_record_by_name(self, name: str):
        """
        Finds a record by the contact name in it.
        :param name: the name to look for in records.
        :return: a record with the specified name.
        """
        if not self.data:
            raise MyException(f"The address book is empty.")
        if name in self.data:
            return self.data[name]
        else:
            raise MyException(f"No record with the name '{name}' in the address book.")

    def get_record_by_phone(self, phone: str):
        """
        Finds all records where specified phone number is found.
        :param phone: phone number to look for in records.
        :return: list of records which contain the specified phone number.
        """
        res = []
        if not self.data:
            raise MyException(f"The address book is empty.")
        for record in self.data.values():
            if phone in record.get_phones():
                res.append(record)
        if not res:
            raise MyException(f"No record with the phone number '{phone}' in the address book.")
        return res

    def get_record_by_email(self, email: str):
        """
        Finds all records where specified e-mail is found.
        :param email: e-mail to look for in records.
        :return: list of records which contain the specified e-mail.
        """
        res = []
        if not self.data:
            raise MyException(f"The address book is empty.")
        for record in self.data.values():
            if email in record.get_emails():
                res.append(record)
        if not res:
            raise MyException(f"No record with the e-mail '{email}' in the address book.")
        return res

    def get_record_by_birthday(self, birthday: str):
        """
        Finds all records where specified birthday date is found.
        :param birthday: birthday date to look for in records.
        :return: list of records which contain the specified birthday date.
        """
        res = []
        if not self.data:
            raise MyException(f"The address book is empty.")
        birthday = Birthday.reformat_value(birthday)
        for record in self.data.values():
            if birthday == record.get_birthday():
                res.append(record)
        if not res:
            raise MyException(f"No record with the birthday date '{birthday}' in the address book.")
        return res

    def get_record_by_days_till_birthday(self, n_days: str):
        try:
            n_days = int(n_days)
            cur_day = datetime.now()
            birthday = cur_day + timedelta(days=n_days)
            birthday = f"{birthday.day}/{birthday.month}"
            return self.get_record_by_birthday(birthday)
        except ValueError:
            raise MyException(f"The given parameter '{n_days}' for the number of days is not a valid integer number.")

    def get_record_by_string(self, substring: str, fields="np"):
        """
        Finds all records where specified string is found in the contact
        fields (e.g. name or the phone number).
        :param substring: string to look for in records.
        :param fields: fields to check:
                        n - for 'name',
                        p - for 'phone number',
                        e - for 'emails'
                        b - for 'birthday'
                        a - for 'address'
        :return: list of records which contain the specified (sub)string.
        """
        res = []
        if not self.data:
            raise MyException(f"The address book is empty.")
        for record in self.data.values():
            if 'n' in fields and substring in record.get_name():
                res.append(record)
            elif "b" in fields and substring in record.get_birthday():
                res.append(record)
            elif "a" in fields and substring in record.get_address():
                res.append(record)
            elif 'p' in fields:
                for phone in record.get_phones():
                    if substring in phone:
                        res.append(record)
                        break
            if not res and 'e' in fields:
                for email in record.get_emails():
                    if substring in email:
                        res.append(record)
                        break
        if not res:
            raise MyException(f"No record with the substring '{substring}' within the fields '{fields}' in the address book.")
        return res

    def get_record_by_address(self, address: str):
        """
        Finds a record by the address in it.
        :param address: the address to look for in records.
        :return: a record with the specified address.
        """
        res = []
        if not self.data:
            raise MyException(f"The address book is empty.")
        for record in self.data.values():
            if address == record.get_address():
                res.append(record)
        if not res:
            raise MyException(f"No record with the address '{address}' in the address book.")
        return res

    def store_to_file(self, path="", filename=""):
        if not filename:
            filename = self.username
        filename = os.path.join(path, filename + ".bin")
        with open(filename, "wb") as f:
            pickle.dump((self.data, self.username), f, pickle.HIGHEST_PROTOCOL)

    def load_from_file(self, filename):
        try:
            with open(filename, "rb") as f:
                self.data, self.username = pickle.load(f)
        except FileNotFoundError:
            raise MyException(f"Address book cannot be loaded from the file '{filename}: the file does not exist.")

    def iterator(self, n=None):
        return ABIterator(self.data.values(), n)

    def to_string(self):
        return AddressBook.display_records(self.data.values())


if __name__ == "__main__":
    ab = AddressBook()
    ab.add_record(Record("tu", "684721", "ns@i.f", "08/09"))
    ab.add_record(Record("tu1", "684721787", "n@ks.jk", "07/10"))
    ab.add_record(Record("tu2", "6847", "nd@sn.v", "12/11"))
    ab.add_record(Record("tu4", "6847842197", "mck@ds.jc", "11/01"))
    #ab.set_number_records_per_iteration("m3")
    test = ab.iterator()
    #print(test)
    #test = ABIterator("1234", 6)
    cnt = 0
    for el in test:
        cnt += 1
        print("____________________NEW EL --------------------------")
        print(el, "\n")
        #if cnt == 10:
        #    break

'''
For tests:
add tu 684721 ns@i.f 08/09
add tu1 684721787 n@ks.jk 07/10
add tu2 6847 nd@sn.v 12/11 
add tu4 6847842197 mck@ds.jc 11/01 
add tu5 6847842197 mck@ds.jc 08/09 
new username tu
store

'''

