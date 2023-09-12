from collections import UserDict
from operator import attrgetter
import pickle
import prettytable

FILENAME = './note_book/notebook.pkl'
COMMANDS = (
    'add', 'edit', 'show', 'show_all', 'delete', 'search',
    'add_tag', 'del_tag', 'help', 'exit'
      )
DESCRIPTION = (
    'add note by: add <name>\nthen enter a note',
    'edit note by: edit <name>',
    'show note by: show <name>',
    'show all notes',
    'delete note by: delete <name>',
    'search note by tag: search <keyword>',
    'add tag by: add_tag <name> <tags>',
    'delete tag by: del_tag <name>\nthen enter tag to delete',
    'show this description',
    'exit to main menu'
    )

class Field:
    pass


class Note(Field):
    def __init__(self):
        self.__value = None

    def is_valid(self, new_value: str):
        return len(new_value) > 2

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            print("Note is too short")
        else:
            self.__value = new_value


class Record:
    def __init__(self, name: str, note: Note, tags=None):
        self.name = name
        self.note = note
        self.tags = []
        if tags:
            self.tags.extend(list(set(tags.split(', '))))
            self.tags = sorted(self.tags)

    def add_tag(self, tag: str):
        if tag in self.tags:
            print('Tag already exists')
        else:
            self.tags.append(tag)
            self.tags = sorted(self.tags)

    def delete_tag(self, tag: str):
        try:
            self.tags.remove(tag)
        except ValueError:
            print('Tag does not exist')


class NoteBook(UserDict):
    def add_note(self, name: str, value: str, tags: str):
        note = Note()
        note.value = value
        record = Record(name, note, tags)
        self.data[record.name] = record
        self.save_data()
        

    def edit_note(self, name: str, new_note: str):
        try:
            self.data[name].note.value = new_note
        except KeyError:
            print('Note not found!')

    def show_note(self, name: str) -> str:
        try:
            note = prettytable.PrettyTable()
            note.align = 'l'
            note.field_names = [self.data[name].name]
            note.add_row([self.data[name].note.value])
            note.add_row(['Tags: ' + ', '.join(self.data[name].tags)])
            print(note)
        except KeyError:
            print('Note not found!')

    def delete_note(self, name: str):
        try:
            self.data.pop(name)
        except KeyError:
            print('Note not found!')

    def search_notes(self, query: str) -> str:
        results = set()
        if query:
            for record in self.data.values():
                if (any(query in tag for tag in record.tags)):
                    results.add(record)

            results = self.sort_notes(list(results))
            return ', '.join(note.name for note in results)
        return 'No value to search'

    def show_all_notes(self):
        result = prettytable.PrettyTable()
        result.align = 'l'
        result.header = False
        lines = []
        line = ''
        for note in self.data.values():
            if not line:
                line += note.name
                continue
            if len(line + note.name + ', ') > 30:
                lines.append(line)
                line = note.name
            else:
                line += ', ' + note.name
        if line:
            lines.append(line)
        result.add_row(['\n'.join(lines)])
        return result

    def sort_notes(self, notes:list[Note]):
        return sorted(notes, key=attrgetter('tags'))

    def save_data(self):
        with open(FILENAME, 'wb') as file:
            pickle.dump(self.data, file)

    def load_data(self):
        try:
            with open(FILENAME, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def __init__(self):
        super().__init__(self)
        self.load_data()

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.data):
            keys = list(self.data.keys())
            key = keys[self.idx]
            self.idx += 1
            return self.data[key]
        else:
            raise StopIteration
note_book = NoteBook()

def command_list():
    description = prettytable.PrettyTable()
    description.field_names = ['Command', 'Description']
    description.align = 'l'
    for command, descr in zip(COMMANDS, DESCRIPTION):
        description.add_row([command, descr])
    return description


def command_parser(raw_input: str):
    user_input = raw_input.split(' ')
    name = ''
    tag = ''
    command = user_input[0]
    if len(user_input) > 1:
        name = user_input[1]
    if len(user_input) > 2:
        tag = user_input[2]
    return (command, name, tag)

def command_handler(command: str, name: str, tag: str):
    if command == 'add':
        if name in note_book.keys():
            print('Note already exist')
        else:
            value = input(f'{name}:\n')
            tags = input('Put some tags: ').split(', ')
            note_book.add_note(name, value, tags)

    elif command == 'edit':
        value = input('Enter your note:\n')
        note_book.edit_note(name, value)

    elif command == 'show':
        note_book.show_note(name)

    elif command == 'show_all':
        print(note_book.show_all_notes())

    elif command == 'delete':
        note_book.delete_note(name)

    elif command == 'help':
        print(command_list())

    elif command == 'search':
        print(note_book.search_notes(name))

    elif command == 'add_tag':
        if tag:
            note_book.data[name].add_tag(tag)

    elif command == 'del_tag':
        print(', '.join(note_book.data[name].tags))
        tag = input('Choose tag to delete: ')
        note_book.data[name].delete_tag(tag)

    else:
        print('Unknown command')

def main():
    print(command_list())
    print('You are in Notebook. How can I help you?')
    while True:
        user_input = input('NoteBook: ')
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit', 'close', 'goodbye'):
            note_book.save_data()
            break
        try:
            user_input = command_parser(user_input)
            command_handler(user_input[0].lower(), user_input[1], user_input[2])
        except:
            note_book.save_data()
            print('Something went wrong!')

if __name__ == "__main__":
    main()
