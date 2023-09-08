from fields import *
from collections import deque
from myexception import *
from datetime import datetime
import warnings


class Record:
    """
    Class representing a single record in an address book.
    """

    def __init__(self, name: str, phone=None, email=None, birthday=None):
        self.name = Name(name)
        self.phones = deque()
        self.emails = deque()
        self.birthday = None
        if phone:
            self.add_phone_number(phone)
        if email:
            self.add_email(email)
        if birthday:
            self.edit_birthday(birthday)

    def set_name(self, new_name: str):
        self.name.set_value(new_name)

    def get_name(self):
        return self.name.get_value()

    def get_all_values(self, el_list: deque):
        """
        Returns list of values stored in a collection of Field objects.
        :param el_list: collection of Field objects.
        :return: list of values stored in the elements within el_list.
        """
        return [el.get_value() for el in el_list]

    def get_phones(self):
        '''
        Returns the stored phones as a list f strings.
        :return: phones as a list of strings.
        '''
        return self.get_all_values(self.phones)

    def get_emails(self):
        return self.get_all_values(self.emails)

    def get_birthday(self):
        if self.birthday:
            return self.birthday.get_value()
        else:
            return ""

    def edit_name(self, new_name):
        self.name.set_value(new_name)

    def edit_birthday(self, new_birthday):
        if not self.birthday:
            self.birthday = Birthday(new_birthday)
        else:
            warnings.warn(f"WARNING: you are overwriting existing birthday info. Old info: '{self.birthday.get_value()}', new info: '{new_birthday}'.")
            self.birthday.set_value(new_birthday)

    def remove_birthday(self):
        self.birthday = None

    def is_in_list(self, el: Field, el_list: deque):
        el_value = el.get_value()
        list_values = self.get_all_values(el_list)
        return el_value in list_values

    def add_field_element(self, el_list: deque, el: Field, idx=None, add_to_beginning=False):
        """
         Adds element 'el' to the list 'el_list'.
         Raises an exception if the element is already in the list or the adding is not possible.
         :param el_list: list to which the new element has to be added, e.g. self.phones or self.emails
         :param el: new element which has to be added to el_list
         :param idx: index of the position to insert the new element.
                     Must be None, integer or another type convertible to integer.
                     If provided, 'add_to_beginning' will be ignored.
         :param add_to_beginning: specifies if the new element has to be added to
                                 the beginning of the list (True) or to its end (False).
                                 If 'idx' is provided, add_to_beginning will be ignored
         :return: None
         """

        if self.is_in_list(el, el_list):
            raise MyException(f"{el.get_name().title()} '{el.get_value()}' is already present.")
        elif idx:
            try:
                idx = int(idx)
                idx -= 1
            except:
                raise MyException(f"Provided index must be an integer, given: {idx}.")
            if idx < 0 or idx >= len(el_list):
                raise MyException(f"Provided index '{idx+1}' is out of range.")
            try:
                el_list.insert(idx, el)
            except:
                raise MyException(f"Provided index '{idx+1}' is out of range.")
        elif add_to_beginning:
            el_list.appendleft(el)
        else:
            el_list.append(el)

    def add_phone_number(self, new_value: str, idx=None, add_to_beginning=False):
        phone = Phone(new_value)
        self.add_field_element(el_list=self.phones,
                               el=phone, idx=idx, add_to_beginning=add_to_beginning)

    def add_email(self, new_value: str, idx=None, add_to_beginning=False):
        email = Email(new_value)
        self.add_field_element(el_list=self.emails,
                               el=email, idx=idx, add_to_beginning=add_to_beginning)

    def remove_field_element(self, el_list: deque, el=None, idx=None, first=False, last=False):
        """
        Removes an element from the list 'el_list'.
        Raises an exception if the list is empty the element is not in the list or the specified index is out of range.
        :param el_list: list from which the specified element has to be removed, e.g. self.phones or self.emails
        :param el: specific element which has to be removed.
                    If provided, this element will be sought for and removed if found. Other parameters will be ignored.
                    If None, further parameters will be considered.
        :param idx: position in the 'el_list' from which an element has to be removed.
                     Must be None, integer or another type convertible to integer.
                     If 'el' is provided, this parameter will be ignored.
        :param first: if True, first element in the list will be removed.
                     If 'el' or 'idx' is provided, this parameter will be ignored.
        :param last: if True, last element in the list will be removed.
                     If 'el', 'idx' or 'first' is provided, this parameter will be ignored.
        :return: None.
        """
        if el:
            el_value = el.get_value()
            cur_values2ids = {element.get_value(): position for position, element in enumerate(el_list)}
            if el_value in cur_values2ids:
                idx = cur_values2ids[el_value]
                del el_list[idx]
            else:
                raise MyException(f"{el.get_name()} '{el.get_value()}' cannot be deleted: it is not in the list.")
        elif idx:
            try:
                idx = int(idx)
                idx -= 1
            except:
                raise MyException(f"Provided index must be an integer, given: {idx}.")
            try:
                del el_list[idx]
            except IndexError:
                raise MyException(f"Provided index '{idx}' is out of range.")
        elif first:
            try:
                el_list.popleft()
            except IndexError:
                raise MyException(f"First {el.get_name()} can't be removed: the list is empty.")
        elif last:
            try:
                el_list.pop()
            except IndexError:
                raise MyException(f"Last {el.get_name()} can't be removed: the list is empty.")
        else:
            raise MyException(f"Please specify the {el.get_name()} which has to be removed.")

    def remove_phone_number(self, cur_value="", idx=None, first=False, last=False):
        if cur_value:
            phone = Phone(cur_value)
        else:
            phone = None
        self.remove_field_element(el_list=self.phones, el=phone, idx=idx, first=first, last=last)

    def remove_email(self, cur_value="", idx=None, first=False, last=False):
        if cur_value:
            email = Email(cur_value)
        else:
            email = None
        self.remove_field_element(el_list=self.emails, el=email, idx=idx, first=first, last=last)

    def edit_field_element(self, el_list: deque, new_el: Field, old_el=None, idx=None, first=False, last=False):
        """
        Edits an element in the list 'el_list'.
        Raises an exception if the list is empty, the element is not in the list or the specified index is out of range.
        :param el_list: list in which the specified element has to be edited, e.g. self.phones or self.emails
        :param new_el: new value for the element which has to be edited.
        :param old_el: specific element which has to be edited.
                    If provided, this element will be sought for and edited if found. Other parameters will be ignored.
                    If None, further parameters will be considered.
        :param idx: position in the 'el_list' at which an element has to be edited.
                     Must be None, integer or another type convertible to integer.
                     If 'old_el' is provided, this parameter will be ignored.
        :param first: if True, first element in the list will be edited.
                     If 'old_el' or 'idx' is provided, this parameter will be ignored.
        :param last: if True, last element in the list will be edited.
                     If 'old_el', 'idx' or 'first' is provided, this parameter will be ignored.
        :return: None.
        """
        if self.is_in_list(new_el, el_list):
            raise MyException(f"{new_el.get_name().title()} '{new_el.get_value()}' is already present.")
        if old_el:
            el_value = old_el.get_value()
            cur_values2ids = {element.get_value(): position for position, element in enumerate(el_list)}
            if el_value in cur_values2ids:
                idx = cur_values2ids[el_value]
                el_list[idx] = new_el
            else:
                raise MyException(f"{old_el.get_name()} '{old_el.get_value()}' cannot be edited: it is not in the list.")
        elif idx:
            try:
                idx = int(idx)
                idx -= 1
            except:
                raise MyException(f"Provided index must be an integer, given: {idx}.")
            try:
                el_list[idx] = new_el
            except IndexError:
                raise MyException(f"Provided index '{idx}' is out of range.")
        elif first:
            try:
                el_list[0] = new_el
            except IndexError:
                raise MyException(f"First {old_el.get_name()} can't be edited: the list is empty.")
        elif last:
            try:
                el_list[-1] = new_el
            except IndexError:
                raise MyException(f"Last {old_el.get_name()} can't be edited: the list is empty.")
        else:
            raise MyException(f"Please specify the {old_el.get_name()} which has to be edited.")

    def edit_phone_number(self, new_value: str, cur_value="", idx=None, first=False, last=False):
        new_el = Phone(new_value)
        if cur_value:
            old_el = Phone(cur_value)
        else:
            old_el = None
        self.edit_field_element(el_list=self.phones, new_el=new_el, old_el=old_el, idx=idx, first=first, last=last)

    def edit_email(self, new_value: str, cur_value="", idx=None, first=False, last=False):
        new_el = Email(new_value)
        if cur_value:
            old_el = Email(cur_value)
        else:
            old_el = None
        self.edit_field_element(el_list=self.emails, new_el=new_el, old_el=old_el, idx=idx, first=first, last=last)

    def days_to_birthday(self):
        if not self.birthday:
            return "unknown (no information about birthday)"
        cur_date = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
        cur_year = cur_date.year
        birthday_day, birthday_month = self.birthday.get_value().split("/")
        birthday_day = int(birthday_day)
        birthday_month = int(birthday_month)
        if birthday_month > cur_date.month or (birthday_month == cur_date.month and birthday_day >= cur_date.day):
            birthday_year = cur_year
        else:
            birthday_year = cur_year + 1
        try:
            birthday_date = datetime(day=birthday_day, month=birthday_month, year=birthday_year)
        except ValueError:
            if birthday_day == 29 and birthday_month == 2:
                birthday_date = datetime(day=1, month=3, year=birthday_year)
            else:
                raise MyException(f"Unknown problem with the birthday date ('{self.get_birthday()}') of the contact '{self.get_name()}, days till birthday cannot be calculated.")

        delta_time = birthday_date - cur_date
        return delta_time.days

    def display_birthday_info(self):
        if self.birthday is None:
            return ""
        else:
            days_till_birthday = self.days_to_birthday()
            days = "days" if days_till_birthday != 1 else "day"
            return f"{self.birthday.get_value()} ({days_till_birthday} {days} till birthday)"

    def to_string(self):

        if len(self.phones) == 1:
            phones = [self.phones[0].get_value()]
        else:
            phones = [f"{position + 1}. {phone.get_value()}" for position, phone in enumerate(self.phones)]
        if len(self.emails) == 1:
            emails = [self.emails[0].get_value()]
        else:
            emails = [f"{position + 1}. {email.get_value()}" for position, email in enumerate(self.emails)]
        line = "----------------------------------------------------------------"
        phones = "\n\t\t\t".join(phones)
        emails = "\n\t\t\t".join(emails)
        birthday = self.display_birthday_info()
        res = f"CONTACT INFO\nNAME:\t\t{self.get_name()}\n{line}\nBIRTHDAY:\t{birthday}\n{line}\nPHONE(S):\t{phones}\n{line}\nEMAIL(S):\t{emails}"
        return res


if __name__ == "__main__":
    '''
    rec = Record("user1")
    rec.add_phone_number("1374658")
    #rec.add_phone_number("1374658")
    #rec.add_phone_number("1374658")
    rec.add_phone_number("678569872", add_to_beginning=True)
    rec.add_phone_number("87987498709", idx=2)
    rec.add_email("jhfsew@kjfjg")
    #rec.add_email("jhfsew@kjfjg")
    #rec.add_email("jhfsew@kjfjg")
    rec.add_email("njhfshfks@jfdjfir.fkjifu")
    rec.add_email("njhfiw@njrhjei.hj")
    rec.add_email("DFrf@njhreu")
    print(rec.to_string())
    print()
    print("removing elements...")
    #rec.remove_phone_number("678569872")
    rec.remove_phone_number(idx=1) #(self, phone="", idx=None, first=False, last=False)
    rec.remove_email(idx=1)
    #rec.remove_email("njhfiw@njrhjei.hj")
    print(rec.to_string())
    print()
    print("doing editing...")
    #rec.edit_email(old_el="njhfiw@njrhjei.hj", new_el="DFrf@njhreu")
    rec.edit_email(old_el="njhfiw@njrhjei.hj", new_el="new_email@hi")
    #rec.edit_phone_number(old_el="1374658", new_el="new_phone")
    rec.edit_phone_number(old_el="1374658", new_el="new_phone") # (self, new_el: str, old_el="", idx=None, first=False, last=False
    print(rec.to_string())
    '''
    rec = Record("test")
    rec.edit_birthday("18/08")
    print(rec.days_to_birthday())
    print(rec.to_string())
