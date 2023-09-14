# Your Family Assistant
Team project developed by **Crazy Pythies**

*Your Family Assistant is a console bot that gives you and your family the opportunity to save contacts in the Address Book, creat and save notes in the Note Book and sort your files by File Sorter.*
## Installation
### ADDRESS BOOK
The application ***Address Book*** allows to create digital *address books* for diverse users. Each user can add new contacts to his/her *address book*, edit them, delete, get them displayed, search for specific contacts by information stored in them. The following information can be stored in an *address book* for each contact:

1. Name (obligatory): name of the contact (can be only one).
2. Birthday (optional): the birthday date of the contact (can be only one).
3. Phone number(s) (optional): one or multiple phone numbers belonging to the contact.
4. E-mail(s) (optional): one or multiple e-mails belonging to the contact.
5. Address (optional): the address of the contact (can be only one).

Name and birthday are represented by one token only. In case of phone numbers, e-mails, each phone number/e-mail is one token. The address can consist of multiple tokens.

The following functionality is supported by the application.
- Getting greetings.
- Adding new contact to the *address book*.
- Editing existing contact in the *address book*.
- Finding and showing a record in the *address book*: by name, phone number, e-mail, birthday, address or their substrings.
- Deleting a contact from the *address book*.
- Showing all saved phone numbers for a given contact.
- Showing all saved e-mails for a given contact.
- Showing saved birthday information for a given contact (including the number of days remaining till the contact’s birthday).
- Showing all records in the *address book*.
- Showing the name of the *address book’s* owner (user name).
- Changing the user name of the *address book*.
- Creating a new empty *address book*: with a default user name or the user name provided by the user.
- Storing current *address book* into a file (under the current user name).
- Loading an *address book* from a file (by the corresponding user name).
- Exiting the programme and going back to the main menu.
- Getting help.

For detailed instructions on the corresponding commands and required arguments, see the manual.

### NOTE BOOK
The application ***Note Book*** allows to create digital notes. User can add new notes, edit them, delete, get them displayed, search for specific notes by information stored in them. 

The following functionality is supported by the application.
- Adding new note to the *note book*.
- Editing existing note in the *note book*.
- Showing a note in the *note book*.
- Showing list of notes in the *note book*.
- Deleting a note from the *note book*.
- Adding tag to a note.
- Delete a tag from a note.
- Searching for specific notes by information stored in them and by tags.
- Exiting ***Note Book*** and returning to the main menu.

### FILE SORTER
The application ***File Sorter*** allows to sort files by types: Images, Video, Documents, Audio, Archives, Others.
If the file is unknown, it will move into the folder "Others".

The following functionality is supported by the application.
- Supporting file types: JPEG, JPG, PNG, SVG, AVI, MP4, MOV, MKV, DOC, DOCX, TXT, PDF, XLSX, PPTX, MP3, OGG, WAV, AMR, M4A, ZIP, GZ, TAR. Uknowing types moving to folder "Others".
- Transliterating Cyrillic alphabet to Latin and replacing all symbols to "_" except Latin letters and numbers.
- Unpacking archives and moving to the folder 'Archives'.
- Deleting empty folders in the target folder.
