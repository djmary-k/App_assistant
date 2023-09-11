from collections import UserDict
from operator import attrgetter
import pickle
import prettytable

FILENAME = './note_book/notebook.pkl'
COMMANDS = ('add', 'edit', 'show', 'delete', 'search', 'add_tag', 'del_tag')
DESCRIPTION = (
    'add note by: add "name"\nthen enter a note',
    'edit note by: edit "name"',
    'show note by: show "name"',
    'delete note by: delete "name"',
    'search note by: search "keyword"',
    'add tag by: add_tag "name" "tags"',
    'delete tag by: del_tag "name"\nthen enter tag to delete'
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
            raise ValueError("Note is too short")
        self.__value = new_value


class Record:
    def __init__(self, name: str, note: Note, tags=None):
        self.name = name
        self.note = note
        self.tags = []
        if tags:
            self.tags.extend(list(set(tags.split(', '))))

    def add_tag(self, tag: str):
        if tag in self.tags:
            print('Tag already exists')
        else:
            self.tags.append(tag)

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
            self.data[name] = new_note
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
                if (
                    query.lower() in record.note.value.lower()
                    or any(query in tag for tag in record.tags)
                    or query in record.name
                ):
                    results.add(record.name)
            return ', '.join(results)
        return 'No value to search'

    def sort_notes(self):
        return sorted(self.data.values(), key=attrgetter('tags'))

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

def command_list():
    description = prettytable.PrettyTable()
    description.field_names = ['Command', 'Description']
    description.align = 'l'
    for command, descr in zip(COMMANDS, DESCRIPTION):
        description.add_row([command, descr])
    return description


def command_parser(raw_input: str):
    user_input = raw_input.split(' ')
    name = None
    tag = None
    command = user_input[0]
    if len(user_input) > 1:
        name = user_input[1]
    if len(user_input) > 2:
        tag = user_input[2]
    return (command, name, tag)

def command_handler(command: str, name: str, tag: str):
    if command == 'add':
        value = input(f'{name}:\n')
        tags = input('Put some tags: ')
        note_book.add_note(name, value, tags)

    elif command == 'edit':
        value = input(f'{name}\n')
        note_book.edit_note(name, value)

    elif command == 'show':
        note_book.show_note(name)

    elif command == 'delete':
        note_book.delete_note(name)

    elif command == 'help':
        print(command_list())

    elif command == 'search':
        print(note_book.search_notes(name))

    elif command == 'add_tag':
        note_book.data[name].add_tag(tag)

    elif command == 'del_tag':
        print(', '.join(note_book.data[name].tags))
        tag = input('Choose tag to delete: ')
        note_book.data[name].delete_tag(tag)

    else:
        print('Unknown command')

def main():
    command_list()
    print('You are in Notebook. How can I help you?')
    while True:
        user_input = input('NoteBook: ')
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit', 'close', 'goodbye'):
            note_book.save_data()
            print('Good bye!')
            break
        user_input = command_parser(user_input)
        command_handler(user_input[0].lower(), user_input[1], user_input[2])


if __name__ == "__main__":
    note_book = NoteBook()
    main()
