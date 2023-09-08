"""
This is the main script of the application.

Notes:
    Possible commands: call "help" to get the command list and info
    The format of phone numbers and e-mails is checked with a very
        simple strategy, warnings can appear if the input does not pass validation
    Phone validation: phone has to consist of digits, optionally preceded with one "+";
                      additionally, a warning appears if the number of digits < 3 or > 15
    Birthday: year of the birthday is ignored even if provided, only day_info/month_info is stored
    Birthday validation: it is checked if the combination day/month (provided in a correct format)
                        is generally possible, irrespective of the year

    Changes made (hw12):
        store/load functions optimized: only data and username get stored
        added automatic storing of the AB before exiting the programme
        added the possibility to find record(s) by a substring of the name/phone number: see 'find -np <substr>
        edited the way of displaying 'find' results: now with numbers

    As before:
        Command "store" stores the current address books in the folder "users"
            in the same directory (will be created if does not exist),
            in a file <username>.bin
        Recognition of the commands is case-insensitive,
            the arguments are treated with respect to their case
            (e.g. name "ann" != "Ann")
        Provided arguments which are irrelevant for the specified command
            will be ignored (the command will be executed)

    Previous changes (hw11):
        - added parameters "birthday", "r-birthday" to the "change" command
        - added possibility to enter birthday when a contact is created
        - added possibility to get birthday info displayed: command "birthday"
        - added birthday info to the display of a record
        - added possibility to find a record by the birthday date (find -b)
        - added parameter <n> for the number of contacts per page to commands "show all", "find"
        - implemented property-setter combination for the attribute "value" in classes Phone and Birthday


Possible improvements:
    extend 'find' command to search for a substring in e-mails and birthday
    suggest a list of currently stored user books to load
    for birthday: accept the birthday year as well and display the future age of the contact
    improve format checking of the phone numbers/e-mails
    extend 'add' command: to allow multiple phones and e-mails to be provided
"""

from addressbook import *
import os
import warnings

ADDRESSBOOK = AddressBook()
WARNING_COLOR = '\033[93m'  # '\033[92m' #'\033[93m'
RESET_COLOR = '\033[0m'

IDX_STRING = "idx="
WARNING_WRONG_N_PER_PAGE = f"Parameter for the number of records per page should be a positive integer. Parameter " \
                           f"which was given: "
INSTRUCTION_CHANGE = "\t<name> -n <new_name>\t-\tto change the contact name from its current value\n" \
                     "\t\t\t\t\t\t\t\t<name> to the value <new_name>\n" \
                     f"\t<name> [+p|+e] <phone|email> ({IDX_STRING}[first|last|<idx>])\t-\tto add a new\n" \
                     "\t\t\t\t\t\t\t\tphone number (+p <phone>) or e-mail (+e <email>)\n" \
                     "\t\t\t\t\t\t\t\tto the record with the name <name>,\n" \
                     f"\t\t\t\t\t\t\t\tOPTIONALLY: at the specified position ({IDX_STRING}) -\n" \
                     "\t\t\t\t\t\t\t\tat the beginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)\n" \
                     f"\t<name> [-p|-e] [<phone|email>|{IDX_STRING}[first|last|<idx>]]\t-\tto remove a phone\n" \
                     "\t\t\t\t\t\t\t\tnumber (-p) or an e-mail (-e)\n" \
                     "\t\t\t\t\t\t\t\tfrom the record with the name <name>,\n" \
                     "\t\t\t\t\t\t\t\tspecifying the target phone number/e-mail by its value\n" \
                     f"\t\t\t\t\t\t\t\t(<phone|email>) or position ({IDX_STRING}) in the record - at the\n" \
                     "\t\t\t\t\t\t\t\tbeginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)\n" \
                     f"\t<name> [edit-p|edit-e] [<phone|email>|{IDX_STRING}[first|last|<idx>]] <new_phone|email>\t-\n" \
                     "\t\t\t\t\t\t\t\tto edit a phone number (edit-p) or an e-mail (edit-e)\n" \
                     "\t\t\t\t\t\t\t\tin the record with the name <name> (replace an old value\n" \
                     "\t\t\t\t\t\t\t\twith the new value <new_phone|email>),\n" \
                     "\t\t\t\t\t\t\t\tspecifying the target phone number/e-mail by its value\n" \
                     f"\t\t\t\t\t\t\t\t(<phone|email>) or position ({IDX_STRING}) in the record - at the\n" \
                     "\t\t\t\t\t\t\t\tbeginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)\n" \
                     f"\t<name> birthday <new_birthday>\t-\tto add or edit the birthday date in the record\n" \
                     "\t\t\t\t\t\t\t\twith the name <name> (the old value will be replaced)\n" \
                     f"\t<name> r-birthday\t-\tto remove the birthday date from the record with the name <name>."

INSTRUCTION_FIND = "\t-n <name> (<n>)\t\t-\tto find the record with the contact name <name>\n" \
                   "\t-p <phone> (<n>)\t-\tto find the record(s) with the phone number <phone>\n" \
                   "\t-e <email> (<n>)\t-\tto find the record(s) with the e-mail <email>\n" \
                   "\t-b <birthday> (<n>)\t-\tto find the record(s) with the birthday <birthday> (format: day/month)\n" \
                   "\t-np <substr> (<n>)\t-\tto find the record(s) with the substring <substr> in the name or phone\n" \
                   "\t(The optional parameter <n> specifies the maximum number of records to be displayed at once.)"

HELP_STRING = "This programme supports the following commands\n" \
              "(elements in () are optional, [] specify options to select from):\n" \
              "1.\tGreeting:\n" \
              "\thello\n" \
              "2.\tAdding new contact to the address book:\n" \
              "\tadd <name> (<phone> <email> <birthday>)\n" \
              f"3.\tEditing existing contact in the address book:\n{INSTRUCTION_CHANGE}\n" \
              f"4.\tSearching for a record in the address book:\n{INSTRUCTION_FIND}\n" \
              "5.\tDeleting a contact from the address book:\n" \
              "\tdelete <name>\n" \
              "6.\tShowing all phone numbers saved for a given contact:\n" \
              "\tphone <name>\n" \
              "7.\tShowing all emails saved for a given contact:\n" \
              "\temail <name>\n" \
              "8.\tShowing birthday info saved for a given contact:\n" \
              "\tbirthday <name>\n" \
              "9.\tShowing all records in the address book:\n" \
              "\tshow all (<n>)\n" \
              "\t(The optional parameter <n> specifies the maximum number of records to be displayed at once.)\n"\
              "10.\tShowing the username in the address book (the name of the owner):\n" \
              "\tusername\n" \
              "11.\tChanging the username in the address book:\n" \
              "\tnew username <username>\n" \
              "12.\tStoring current address book into a file (under the current username):\n" \
              "\tstore\n" \
              "13.\tLoading an address book from a file:\n" \
              "\tload <username>\n" \
              "14.\tExiting the programme (executes storing as in 12. beforehand):\n" \
              "\tgood bye\n" \
              "\tclose\n" \
              "\texit\n" \
              "15.\tGetting help:\n" \
              "\thelp\n" \
              "\nAll commands are case insensitive."


def hello_handler(*args):
    """
    Handles greeting.
    """
    return "How can I help you?"


def exit_handler(*args):
    """
    Handles programme performance by exiting.
    """
    res = store_handler(args)
    return f"{res}\nGood bye!"


def add_handler(args):  # takes *arguments: 0-unlimited
    """
    Adds new contact to the address book.
    :param args: expected argument in the contact name.
    :return: confirmation that the new record with the specified contact name was added.
    """
    if len(args) < 1:
        raise MyException("Give me a name for the new contact, please.")
    name = args[0]  # change to 1) args[0].title() if you want to always capitalize the 1st letter or to 2) args[0].lower().title()
    record = Record(name)

    phone = "NO PHONE NUMBER"
    email = "NO E-MAIL"
    birthday = "NO BIRTHDAY DATE"
    if len(args) > 1:
        phone = args[1]
        record.add_phone_number(phone)
    if len(args) > 2:
        email = args[2]
        record.add_email(email)
    if len(args) > 3:
        birthday = args[3]
        record.edit_birthday(birthday)
    ADDRESSBOOK.add_record(record)
    return f"New contact '{name}' with the phone number '{phone}', e-mail '{email}' and the birthday date '{birthday}' successfully added."


def change_handler(args):
    """
    Changes existing contact in the address book.
    :param args: expects arguments which specify the change to be performed.
    :return: confirmation of the performed change.
    """
    if len(args) < 2 or (len(args) == 2 and args[1].lower() not in ["r-birthday"]) or\
            (args[1].lower() not in ["-n", "+p", "+e", "-p", "-e", "edit-e", "edit-p", "birthday", "r-birthday"]) or \
            (args[1].lower() in ["edit-e", "edit-p"] and len(args) < 4):
        raise MyException(f"Please, specify the change parameters as follows:\n{INSTRUCTION_CHANGE}")
    param = args[1].lower()
    if param == "birthday":
        change = Change(changetype=ChangeType.EDIT_BIRTHDAY, name=args[0], new_birthday=args[2])
    elif param == "r-birthday":
        change = Change(changetype=ChangeType.REMOVE_BIRTHDAY, name=args[0])
    elif param == "-n":
        change = Change(changetype=ChangeType.EDIT_NAME, name=args[0], new_name=args[2])
    elif param in ["+p", "+e"]:
        idx = None
        add_to_beginning = False
        if len(args) > 3:
            if args[3][len(IDX_STRING):].lower() == "first":
                add_to_beginning = True
            elif not args[3][len(IDX_STRING):].lower() == "last":
                idx = args[3][len(IDX_STRING):]
        changetype = ChangeType.ADD_PHONE if param == "+p" else ChangeType.ADD_EMAIL
        change = Change(changetype=changetype, name=args[0],
                        new_value=args[2], idx=idx,
                        add_to_beginning=add_to_beginning)  # new_value: str, idx = None, add_to_beginning = False
    else:
        cur_value = ""
        idx = None
        first = False
        last = False
        if not args[2].lower().startswith(IDX_STRING):
            cur_value = args[2]
        elif args[2][len(IDX_STRING):].lower() == "first":
            first = True
        elif args[2][len(IDX_STRING):].lower() == "last":
            last = True
        else:
            idx = args[2][len(IDX_STRING):]
        if param in ["-p", "-e"]:
            changetype = ChangeType.REMOVE_PHONE if param == "-p" else ChangeType.REMOVE_EMAIL
            change = Change(changetype=changetype, name=args[0],
                            cur_value=cur_value, idx=idx, first=first,
                            last=last)  # cur_value = "", idx = None, first = False, last = False
        else:
            new_value = args[3]
            changetype = ChangeType.EDIT_PHONE if param[-1] == "p" else ChangeType.EDIT_EMAIL
            change = Change(changetype=changetype, name=args[0],
                            new_value=new_value,
                            cur_value=cur_value, idx=idx, first=first,
                            last=last)  # self, new_value: str, cur_value="", idx=None, first=False, last=False
    record = ADDRESSBOOK.edit_record(change)
    return f"The record was successfully edited. Updated record:\n{record.to_string()}"

def find_handler(args):
    """
    Finds a record/records in the address book: by name, phone number, e-mail or birthday date.
    :param args: parameters to find the record(s).
    :return: the string representing the record(s).
    """
    if len(args) < 2 or args[0].lower() not in ["-np", "-n", "-p", "-e", "-b"]:
        raise MyException(f"Please, specify the search parameter, e.g.:\n{INSTRUCTION_FIND}")
    match args[0].lower():
        case "-np":
            param = "substring"
            res = ADDRESSBOOK.get_record_by_string(args[1])
        case "-n":
            param = "name"
            res = ADDRESSBOOK.get_record_by_name(args[1])
        case "-p":
            param = "phone number"
            res = ADDRESSBOOK.get_record_by_phone(args[1])
        case "-e":
            param = "e-mail"
            res = ADDRESSBOOK.get_record_by_email(args[1])
        case "-b":
            param = "birthday date"
            res = ADDRESSBOOK.get_record_by_birthday(args[1])
    if not res:
        return f"No record with the {param} '{args[1]}' found."
    elif type(res) == Record:
        return res.to_string()
    elif len(args) > 2:
        try:
            iterator = ABIterator(res, args[2])
            return iterator
        except MyIteratorNException:
            warnings.warn(WARNING_WRONG_N_PER_PAGE + f"'{args[2]}' (ignored).")
    return AddressBook.display_records(res) #"\n\n".join(record.to_string() for record in res)


def delete_handler(args):
    """
    Delets a contact from the address book.
    :param args: name of the contact for which the record should be deleted.
    :return: confirmation of the deletion.
    """
    if len(args) < 1:
        raise MyException("Please, give me the name of the contact to be deleted.")
    name = args[0]
    ADDRESSBOOK.delete_record(name)
    return f"The record for the name '{name} was successfully deleted."


def phone_handler(args):
    """
    Finds all phone numbers saved for a given contact.
    :param args: name of the contact whose phone number(s) has to be displayed.
    :return: phone number(s) of the specified contact (numerated if > 1).
    """
    if not args:
        raise MyException("Please, enter the contact name.")
    name = args[0]
    record = ADDRESSBOOK.get_record_by_name(name)
    phones = record.get_phones()
    if len(phones) < 1:
        return f"No phones stored for {name}."
    if len(phones) == 1:
        return phones[0]
    return "\n".join(f"{position + 1}. {phone}" for position, phone in enumerate(phones))


def email_handler(args):
    """
    Finds all e-mails saved for a given contact.
    :param args: name of the contact whose e-mail(s) has to be displayed.
    :return: e-mail(s) of the specified contact (numerated if > 1).
    """
    if not args:
        raise MyException("Please, enter the contact name.")
    name = args[0]
    record = ADDRESSBOOK.get_record_by_name(name)
    emails = record.get_emails()
    if len(emails) < 1:
        return f"No e-mails stored for {name}."
    if len(emails) == 1:
        return emails[0]
    return "\n".join(f"{position + 1}. {email}" for position, email in enumerate(emails))


def birthday_handler(args):
    """
    Displays the birthday info (birthday date and the number of days remaining till the birthday)
    saved for a given contact.
    :param args: name of the contact whose birthday info has to be displayed.
    :return: birthday info for the specified contact.
    """
    if not args:
        raise MyException("Please, enter the contact name.")
    name = args[0]
    record = ADDRESSBOOK.get_record_by_name(name)
    res = record.display_birthday_info()
    if not res:
        res = f"No birthday information stored for {name}."
    return res

def show_all_handler(args):
    """
    Handles showing all records in the address book.
    :param args: no parameters expected.
    :return: string representing all the contacts in the address book.
    """
    if len(args) > 0:
        try:
            iterator = ADDRESSBOOK.iterator(args[0])
            return iterator
        except MyIteratorNException:
            warnings.warn(WARNING_WRONG_N_PER_PAGE + f"'{args[0]}' (ignored).")
    res = ADDRESSBOOK.to_string()
    if not res:
        res = "Address book is empty."
    return res


def get_username_handler(args):
    """
    Gets current username in the address book (name of the address book owner).
    :param args: no parameters expected.
    :return: current username.
    """
    return ADDRESSBOOK.get_username()


def set_username_handler(args):
    """
    Changes the username in the address book (name of the address book owner).
    :param args: new username
    :return: confirmation that the username was changed.
    """
    if len(args) < 1:
        raise MyException("Please, specify the new user name.")
    name = args[0]
    ADDRESSBOOK.set_username(name)
    return f"The username successfully changed to '{name}'."


def store_handler(args):
    """
    Stores current address book into a binary file in the folder "users".
    By default, the current username will be used as the filename.
    :param args: not needed.
    :return: confirmation of the storage.
    """
    folder = "users"
    if folder not in os.listdir():
        os.makedirs(folder)
    ADDRESSBOOK.store_to_file(path=folder)
    return f"The address book for the user '{ADDRESSBOOK.get_username()}' was successfully stored."


def load_handler(args):
    """
    Loads an address book from a file. The must be in the folder "users" in the current directory.
    :param args: username whose address book has to be loaded.
    :return: confirmation of the loading.
    """
    if len(args) < 1:
        raise MyException("Please, specify the username.")
    name = args[0]
    filename = name + ".bin"
    folder = "users"
    if folder not in os.listdir() or filename not in os.listdir(folder):
        raise MyException(f"No address book stored for the user '{name}'")
    ADDRESSBOOK.load_from_file(os.path.join(folder, filename))
    return f"Address book for the user '{name}' successfully loaded."


def help_handler(args):
    return HELP_STRING


COMMANDS = {
    hello_handler: ["hello"],  # greeting
    add_handler: ["add"],  # adding new contact to the address book
    change_handler: ["change"],  # changing existing contact in the address book
    find_handler: ["find"],  # finding and showing a record in the address book: by name, phone number or e-mail
    delete_handler: ["delete"],  # deleting a contact from the address book
    phone_handler: ["phone"],  # showing all phone numbers saved for a given contact
    email_handler: ["email"],  # showing all e-mails saved for a given contact
    birthday_handler: ["birthday"], # ! showing the birthday info stored for a given contact
    show_all_handler: ["show all"],  # showing all records in the address book
    get_username_handler: ["username"],  # showing the username in the address book
    set_username_handler: ["new username"],  # changing the username in the address book
    store_handler: ["store"],  # storing current address book into a file
    load_handler: ["load"],  # loading an address book from a file
    exit_handler: ["good bye", "close", "exit"],  # exiting the programme
    help_handler: ["help"]  # getting help
}


def command_parcer(raw_str: str) -> (callable, list):
    case_insensitive = raw_str.lower()
    for handler, commands in COMMANDS.items():
        for command in commands:
            if case_insensitive == command or case_insensitive.startswith(command + " "):
                args = raw_str[len(command):].split()
                return handler, args
    return None, None


def input_error(fnc):
    def inner(*args):
        try:
            fnc(*args)
        except MyException as e:
            print(str(e).replace('"', ""))
            inner()

    return inner


@input_error
def main():
    while True:
        u_input = input(">>> ")
        with warnings.catch_warnings(record=True) as warning_list:
            func, data = command_parcer(u_input)
            while not func:
                print("The command is not defined. Please, use a valid command")
                u_input = input(">>> ")
                func, data = command_parcer(u_input)
            result = func(data)
        for w in warning_list:
            print(f"\t{WARNING_COLOR}{w.message}{RESET_COLOR}")
        if isinstance(result, ABIterator):
            for el in result:
                print(el)
                u_input = input("Show more? ([y/n]): ")
                while not (u_input.startswith("y") or u_input.startswith("n")):
                    u_input = input("Please, enter one of the options: 'y' to show more results, 'n' to finish this "
                                    "command.\n")
                if u_input.startswith("n"):
                    break
            if u_input.startswith("y"):
                print("No more results found.")
        else:
            print(result)
        if func == exit_handler:
            break


if __name__ == "__main__":
    main()
