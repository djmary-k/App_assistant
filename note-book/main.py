from collections import UserDict
from datetime import datetime
import pickle

FILENAME = 'notebook.pkl'


class Record:
    def __init__(self, note: str, tags=None):
        self.note = note
        self.tags = []
        if tags:
            self.tags.extend(list(set(tags.split(', '))))

    def add_tag(self, tag: str):
        if (tag in self.tags):
            print('Tag already exists')
        else:
            self.tags.append(tag)

    def delete_tag(self, tag: str):
        try:
            self.tags.remove(tag)
        except ValueError:
            print('Tag does not exist')


class Field:
    def __init__(self, value: str):
        self.value = value


class Note(Field):
    def is_valid(self, value: str):
        return len(value) > 2

    def __set__(self, _, value: str):
        if not self.is_valid(value):
            raise ValueError("Note is too short")
        self.value = value

    def __get__(self):
        return self.value


class NoteBook(UserDict):
    def add_note(self, record: Record):
        self.data[record.note.value] = record
        self.save_data()

    def search_notes(self, query):
        results = []
        for record in self.data.values():
            if (
                query.lower() in record.note.value.lower()
                or any(query in tag for tag in record.tags)
            ):
                results.append(record)
        return results

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


if __name__ == "__main__":
    note_book = NoteBook()
    # note = Note('hello first note')
    # record = Record(note, 'first, second, third')
    # note_book.add_note(record)
    res = note_book.search_notes('lalal')
    for result in res:
        print(result.note.value)
        print(result.tags)
