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
            ["add", 'to add new contact to the address book'],
            ["edit", 'to edit existing contact in the address book'],
            ["find", 'to find and show a record in the address book by: name, phone number or e-mail'],
            ["delete", 'to delete a contact from the address book'],
            ["phone", 'to show all saved phone numbers for a given contact'],
            ["email", 'to show all saved e-mails for a given contact'],
            ["birthday", 'to show saved birthday info for a given contact'],
            ["show all", 'to show all records in the address book'],
            ["username", 'to show the name of the current address book owner'],
            ["new username", 'to change the owner name of the current address book'],
            ["store", 'to store current address book into a file'],
            ["load", 'to load an address book from a file'],
            ["new profile", 'to create a new empty address book'],
            ["good bye, close, exit, mainmenu", 'to exit the Address Book and go back to the main menu'],
            ["help", 'to get help'],
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
            ["show_all", 'to show list of all notes'],
            ["delete", 'to delete a note'],
            ["search", 'to find notes with a keyword'],
            ["search", 'to find all notes by tag'],
            ["add_tag", 'to add tag to a note'],
            ["del_tag", 'to delete a tag from a note'],
            ["help", 'to call commands description'],
            ["exit", 'to return to the main menu'],
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
    exit_handler: ['5', 'exit'],
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
