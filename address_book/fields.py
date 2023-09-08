import warnings
from datetime import datetime
from myexception import MyException


class Field:
    """
    Class representing a fild in a record of an address book.
    """
    # name of the object type
    name = "field"

    def __init__(self, value: str):
        self.value = value

    def set_value(self, new_value: str):
        self.value = new_value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def validate(self, value: str):
        return True

    def __repr__(self):
        return f"{self.name}: {self.value}"


class Name(Field):
    """
    Class representing the contact name stored in a record of an address book.
    """

    def __init__(self, value: str):
        super(Name, self).__init__(value)
        self.name = "name"


class Phone(Field):
    """
    Class representing a phone number within a record of an address book.
    """

    def __init__(self, value: str):
        #super(Phone, self).__init__(None)
        self.__value = None
        self.value = value
        self.name = "phone"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Sets a new value for the value of the object if it passes internal validation.
        :param new_value: new value to be set.
        """
        if self.validate(new_value):
            self.__value = new_value
        else:
            raise MyException(f"The value {new_value} is not a valid telephone number. Please, provide another value.")

    def validate(self, phone: str):
        """
        Conducts a simple check if the given phone number is well-formed. Raises WARNING if it is not.
        NB: not a full check, only spots some incorrect features.
        :param phone: the phone number to be checked.
        :return: True if the phone number passes the simple check.
        """
        if phone and phone.isdigit() or (len(phone) > 2 and phone[0] == "+" and phone[1:].isdigit()):
            length = len(phone) - 1 if phone[0] == "+" else len(phone)
            if length < 3 or length > 15:
                warnings.warn(f"WARNING: the phone number '{phone}' is potentially malformed.")
            return True
        return False



class Email(Field):
    """
    Class representing an email within a record of an address book.
    """

    def __init__(self, value: str):
        super(Email, self).__init__(None)
        self.set_value(value)
        self.name = "e-mail"

    def validate(self, email: str):
        """
        Conducts a simple check if the given e-mail is well-formed. Raises WARNING if it is not.
        NB: not a full check, only spots some incorrect features.
        :param email: the e-mail to be checked.
        :return: True if the e-mail passes the simple check.
        """
        parts = email.split("@")
        if len(parts) == 2 and len(parts[1].split(".")) == 2:
            return True
        warnings.warn(f"WARNING: the email '{email}' is malformed.")

    def set_value(self, new_value):
        """
        Sets a new value for the value of the object. Calls internal validation
        but sets the value irrespective of validation results.
        :param new_value: new value to be set.
        :return: None.
        """
        self.validate(new_value)
        self.value = new_value


class Birthday(Field):
    """
    Class representing birthday info within a record of an address book.
    """

    @staticmethod
    def get_padded_number_string(cur_str: str, required_length: int):
        if len(cur_str) == required_length:
            return cur_str
        else:
            new_str = str(int(cur_str))
            assert len(new_str) <= required_length
            if len(new_str) < required_length:
                new_str = "0" * (required_length - len(new_str)) + new_str
            return new_str

    @staticmethod
    def reformat_value(value: str) -> str:
        """
        Reformats the input string with the birthday info, to ensure that all values are stored in the same format: "dd/mm"
        :param value: string that has to be reformatted in form "day_info/month_info/further_info"
        :return: reformatted string.
        """
        try:
            parts = value.split("/")
            day, month = parts[:2]
            day = Birthday.get_padded_number_string(day, 2)
            month = Birthday.get_padded_number_string(month, 2)
        except:
            raise MyException(f"The birthday date '{value}' is not well-formed.")
        return f"{day}/{month}"

    def __init__(self, value: str):
        #super(Birthday, self).__init__(None)
        self.__value = None
        self.value = value
        self.name = "birthday"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Sets a new value for the value of the object if it passes internal validation.
        :param new_value: new value to be set.
        """
        if self.validate(new_value):
            self.__value = self.reformat_value(new_value)
        else:
            raise MyException(
                f"The value {new_value} is not a valid birthday value. Please, provide another value in the format "
                f"'day_info/month_info.")

    def validate(self, value: str):
        """
        Conducts a simple check if the given birthday date is well-formed and valid. Only verifies the day and the month,
        ignores any further input if it is present (e.g. year after one more "/")
        Expected format: "day_info/month_info" (e.g. "dd/mm", "ddd/m" etc.), optionally: "day_info/month_info/further_input".
        :param value: the birthday date as a string to be checked.
        :return: True if the birthday date passes the simple check.
        """
        date = value.split("/")
        if len(date) >= 2:
            max_days = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            day, month = date[:2]
            if day.isdigit() and month.isdigit() and 1 <= int(month) <= 12 and 1 <= int(day) <= max_days[int(month)]:
                return True
        else:
            return False


if __name__ == "__main__":
    # testing validate() methods
    print(Email("shf_4uh@d.re"))
    phone = Phone("+36785295720958")
    print(phone, phone.get_value(), phone.value)
    phone = Phone("+366")
    print(phone, phone.get_value(), phone.value)
    # print(Phone("+36785295720958666827529"))
    phone = Phone("+36785295720958")
    print('phone.value = "689573"')
    phone.value = "689573"
    print(phone, phone.get_value(), phone.value)
    print('phone.set_value("76544321")')
    phone.set_value("76544321")
    print(phone, phone.get_value(), phone.value)
    birthday = Birthday("000024/0001/54")
    print(birthday, birthday.get_value(), birthday.value)
    birthday.set_value("0008/9")
    print(birthday, birthday.get_value(), birthday.value)
