from collections import UserDict
from operator import attrgetter
import pickle
import prettytable

FILENAME = './note_book/notebook.pkl'
COMMANDS = (
    'add <name>', 'edit <name>', 'show <name>',
    'show_all', 'delete <name>', 'search <keyword>',
    'search_by <tag>', 'add_tag <name>', 'del_tag <name>', 'help', 'exit'
      )

DESCRIPTION = (
    'to creat a note with the name <name> \
and add it to the Note Book. You will be prompted \
to enter the note text under the name.',
    'to edit a note with the name <name>.',
    'to show a note with the name <name>.',
    'to show list of all notes.',
    'to delete a note with the name <name>.',
    'to find notes with a keyword <keyword>.',
    'to find all notes by tag <tag>.',
    'to add tag to a note with the name <name>. \
You can enter multiple tags separated by ", "',
    'to delete a tag from a note with the name <name>. \
You will be promted to select a tag to delete.',
    'to call commands description.',
    'return to the main menu.'
    )


class Note:
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
            raise ValueError('Note is too short')
        else:
            self.__value = new_value


class Record:
    def __init__(self, name: str, note: Note, tags=None):
        if name:
            self.name = name
        else:
            raise ValueError('Name is too short')
        self.note = note
        self.tags = []
        if tags:
            self.tags.extend(list(set(tags.split(', '))))
            self.tags = sorted(self.tags)

    def add_tag(self, tags: str):
        tags = list(set(tags.split(', ')))
        for tag in tags:
            if tag in self.tags:
                print(f'Tag "{tag}" already exists')
            else:
                self.tags.append(tag)
                self.tags = sorted(self.tags)

    def delete_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError('Tag not found')


class NoteBook(UserDict):
    def add_note(self, name: str, value: str, tags: str):
        try:
            note = Note()
            note.value = value
            record = Record(name, note, tags)
            self.data[record.name] = record
            self.save_data()
        except ValueError as err:
            print(', '.join(err.args))
        

    def edit_note(self, name: str, new_note: str):
        try:
            self.data[name].note.value = new_note
        except KeyError:
            print('Note not found!')
        except ValueError:
            print('Note is too short')

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
            print(f'Note with the name "{name}" succesufully deleted.')
        except KeyError:
            print('Note not found!')

    def search_note(self, query):
        results = set()
        if query:
            for record in self.data.values():
                if query in record.note.value:
                    results.add(record)

            results = self.sort_notes(list(results))
            return ', '.join(note.name for note in results)
        return 'No value to search'

    def search_by_tag(self, query: str) -> str:
        matches = set()
        result = prettytable.PrettyTable()
        result.field_names = ['Name', 'Tags']
        result._max_width = {'Name': 30, 'Tags': 20}
        if query:
            for record in self.data.values():
                if any(query == tag for tag in record.tags):
                    matches.add(record)

            matches = self.sort_notes(list(matches))
            for record in matches:
                result.add_row([record.name, ', '.join(record.tags)])
            return result
        return 'No value to search'

    def show_all_notes(self):
        result = prettytable.PrettyTable()
        result.align = 'l'
        result.header = False
        result.max_table_width = 30
        result.add_row([', '.join(self.data.keys())])
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
    description._max_width = {'Command': 20, 'Description': 50}
    return description


def command_parser(raw_input: str):
    user_input = raw_input.split(' ')
    name = ''
    command = user_input[0]
    if len(user_input) > 1:
        name = ' '.join(user_input[1:])
    return (command, name)

def command_handler(command: str, name: str):
    if command == 'add':
        if name in note_book.keys():
            print('Note already exist')
        else:
            value = input('Enter your note:\n')
            tags = input('Put some tags: ')
            note_book.add_note(name, value, tags)
            if name in note_book.keys():
                print(f'Note with the name "{name}" succesufully added.')

    elif command == 'edit':
        value = input('Enter your note:\n')
        note_book.edit_note(name, value)
        if note_book[name].note.value == value:
            print(f'Note with the name "{name}" has been edited.')

    elif command == 'show':
        note_book.show_note(name)

    elif command == 'show_all':
        print(note_book.show_all_notes())

    elif command == 'delete':
        note_book.delete_note(name)

    elif command == 'help':
        print(command_list())

    elif command == 'search':
        result = note_book.search_note(name)
        if result:
            print(result)
        else:
            print(f'Note that contains {name} not found!')

    elif command == 'search_by':
        result = note_book.search_by_tag(name)
        if result:
            print(result)
        else:
            print(f'Notes with the {name} tag not found!')

    elif command == 'add_tag':
        if not name in note_book.keys():
            print(f'Note with the name "{name}" does not exist.')
        else:
            tags = input('Enter tags to add:\n')
            if tags:
                note_book.data[name].add_tag(tags)
                print(f'Tag(s) "{tags}" succesufully added to the note with the name "{name}".')
            else:
                print('Tag is too short')

    elif command == 'del_tag':
        if not name in note_book.keys():
            print(f'Note with the name "{name}" does not exist.')
        else:
            print(', '.join(note_book.data[name].tags))
            tag = input('Choose tag to delete: ')
            try:
                note_book.data[name].delete_tag(tag)
                print(f'Tag "{tag}" succesufully deleted from the note with the name "{name}".')
            except ValueError as err:
                print(', '.join(err.args))

    else:
        print('Unknown command')

def main():
    print(command_list())
    print('You are in Note Book. How can I help you?')
    while True:
        user_input = input('NoteBook: ')
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit', 'close', 'goodbye'):
            break
        user_input = command_parser(user_input)
        command_handler(user_input[0].lower(), user_input[1])
        note_book.save_data()

if __name__ == "__main__":
    main()
