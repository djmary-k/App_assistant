from address_book.main import main as ab #import AddressBook, Name, Phone, Birthday, Record
# from note_book.main import main as nb
# from clean_folder.main import main as cf
# from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes

def hello_handler(*args):
    return 'How can I help you?'

def exit_handler(*args):
    return 'Good bye!'

def menu(*args):
    # x = PrettyTable()
    x = ColorTable(theme=Themes.OCEAN)
    x.header = False
    # x.field_names = ["Menu", 'menu']
    x.add_row(["1", 'Address Book'], divider=True)
    x.add_row(["2", 'Note Book'], divider=True)
    x.add_row(["3", 'Clean Folder'], divider=True)
    x.add_row(["4", 'Commands Description'], divider=True)
    x.add_row(["5", 'EXIT'], divider=True)
    return x

def commands_descr(*args):
    x = ColorTable(theme=Themes.OCEAN)
    x.header = False
    x.add_row(["1", 'Address Book'], divider=True)
    x.add_rows(
        [
            ["add", 'adding new contact to the address book'],
            ["change", 'changing existing contact in the address book'],
            ["find", 'finding and showing a record in the address book: by name, phone number or e-mail'],
            ["delete", 'deleting a contact from the address book'],
            ["phone", 'showing all phone numbers saved for a given contact'],
            ["email", 'howing all e-mails saved for a given contact'],
            ["birthday", 'showing the birthday info stored for a given contact'],
            ["show all", 'showing all records in the address book'],
            ["username", 'showing the username in the address book'],
            ["new username", 'changing the username in the address book'],
            ["store", 'storing current address book into a file'],
            ["load", 'loading an address book from a file'],
            ["help", 'storing current address book into a file'],
        ],
    )
    x.add_row(['', ''], divider=True)
    x.add_row(["2", 'Note Book'], divider=True)
    x.add_rows(
        [
            ["add", 'adding new contact to the address book'],
            ["change", 'changing existing contact in the address book'],
            ["find", 'finding and showing a record in the address book: by name, phone number or e-mail'],
            ["delete", 'deleting a contact from the address book'],
        ]
    )
    x.add_row(['', ''], divider=True)
    x.add_row(["3", f'Clean Folder\nFiles will be sorted by types: IMAGES, VIDEO, DOCS, AUDIO, ARCHIVES, OTHERS'], divider=True)
    x.add_row(["4", 'Commands Description'], divider=True)
    x.add_row(["5", 'EXIT'], divider=True)
    print(x)
    return 'Go back to menu type "menu".'

COMMANDS = {
    menu: 'menu',
    hello_handler: ['hello', 'hello!', 'hi', 'hi!'],
    exit_handler: ['5', 'bye', 'good bye', 'close', 'exit', 'quit'],
    ab: '1',
    # nb: '2',
    # cf: '3',
    commands_descr: '4',
}

def command_parser(raw_str: str):
    elements = raw_str.split()
    for key, value in COMMANDS.items():
        if raw_str.lower() in value:
            return key(elements[1:])
        elif elements[0].lower() in value:
            return key(elements[1:])
    return 'Invalid command. Please, try again.'

def run():
    print("Hello! My name is Luna. I'm your family assistant. Choose one of these options:")
    print(menu())
    while True:        
        user_input = input('>>> ')
        if not user_input:
            continue                
        result = command_parser(user_input)        
        print(result)
        if result == 'Good bye!':
            break


if __name__ == "__main__":
    run()

