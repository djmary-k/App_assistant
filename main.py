from address_book.main import main as ab
from note_book.main import main as nb
from file_sorter.main import main as fs
from prettytable.colortable import ColorTable, Themes

def hello_handler():
    return 'How can I help you?'

def exit_handler():
    return 'Good bye!'

def menu():
    # x = PrettyTable()
    x = ColorTable(theme=Themes.OCEAN)
    x.header = False
    # x.field_names = ["Menu", 'menu']
    x.add_row(["1", 'Address Book'], divider=True)
    x.add_row(["2", 'Note Book'], divider=True)
    x.add_row(["3", 'File Sorter'], divider=True)
    x.add_row(["4", 'Commands Description'], divider=True)
    x.add_row(["5", 'EXIT'], divider=True)
    return x

def commands_descr():
    x = ColorTable(theme=Themes.OCEAN)
    x.field_names = ["1", 'ADDRESS BOOK']
    x.align['ADDRESS BOOK'] = 'l'
    x._max_width={"1": 20, 'ADDRESS BOOK': 50}
    x.add_row(["Command", 'Description'], divider=True)
    x.add_rows(
        [
            ["hello", 'greeting'],
            ["add", 'adding new contact to the address book'],
            ["edit", 'editing existing contact in the address book'],
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
            ["good bye, close, exit, mainmenu", 'exiting the programme and going back to the main menu'],
            ["help", 'getting help'],
        ]
    )
    x.add_row(['', ''], divider=True)
    x.add_row(["2", 'NOTE BOOK'], divider=True)
    x.add_row(["Command", 'Description'], divider=True)
    x.add_rows(
        [
            ["add", 'to creat a note'],
            ["edit", 'to edit a note'],
            ["show", 'to show a note'],
            ["show_all", 'to show all notes'],
            ["delete", 'to delete a note'],
            ["search", 'to find all notes with a tag'],
            ["add_tag", 'to add tag to a note'],
            ["del_tag", 'to delete a tag from a note'],
            ["help", 'to call commands description'],
            ["exit", 'return to the main menu'],
        ]
    )
    x.add_row(['', ''], divider=True)
    x.add_row(["3", f'FILE SORTER\nFiles will be sorted by types: Images, Video, Documents, Audio, Archives, Others'], divider=True)
    x.add_row(["4", 'COMMANDS DESCRIPTION'], divider=True)
    x.add_row(["5", 'EXIT'], divider=True)
    print(x)
    return 'Check menu options type "menu".'

COMMANDS = {
    menu: 'menu',
    exit_handler: ['5'],
    ab: '1',
    nb: '2',
    fs: '3',
    commands_descr: '4',
}

def command_parser(raw_str: str):
    elements = raw_str.split()
    for key, value in COMMANDS.items():
        if (raw_str.lower() in value) or (elements and elements[0].lower() in value):
            return key
    return 'Invalid command. Please, try again. To see valid options type "menu".'

def run():
    print("Hello! My name is Luna. I'm your family assistant. Choose one of the following options:")
    print(menu())
    while True:        
        user_input = input('>>> ')
        if not user_input:
            continue                
        func = command_parser(user_input)
        if isinstance(func, str):
            result = func
        else:
            result = func()
        if result:       
            print(result)
        if func in [ab, nb, fs]:
            print('Welcome back to main menu! Please, choose one of the following options:')
            print(menu())
        if result == 'Good bye!':
            break
        


if __name__ == "__main__":
    run()
