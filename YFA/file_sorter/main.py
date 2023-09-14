from pathlib import Path
from . import sort


def main():
    print("You've entered File Sorter. To come back to the main menu type: *exit.")
    while True:
        folder_to_scan = input('Please, enter the path of a folder to sort: ')
        if folder_to_scan == '*exit':
            return
        if not folder_to_scan.strip():
            print('You have not entered the path. Try again.')
        elif not Path(folder_to_scan).is_dir():
            print('The entered path is not a folder. Try again.')
        else:
            break

    while True:
        destination_folder = input('Please, enter the path of destination folder: ')
        if destination_folder == '*exit':
            return
        if not destination_folder.strip():
            print('You have not entered the path. Try again.')
        elif not Path(destination_folder).is_dir():
            _ = input('The entered folder does not exist. Do you want to create new folder? (y/n): ')
            if _ == 'y':
                try:
                    Path(destination_folder).mkdir(mode=511, exist_ok=True, parents=True)
                    break  
                except OSError:
                    print('Not possible to creat a folder with the given path. Try again.')
        else:
            break
        
            
    sort.read_folder(Path(folder_to_scan), Path(destination_folder))

    sort.handle_empty_folders(Path(folder_to_scan)) 
    print(f'The folder "{Path(folder_to_scan)}" has been sorted. You are getting forwarded to the main menu...')

    
if __name__ == "__main__":
    main()