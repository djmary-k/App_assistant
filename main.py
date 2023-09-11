from pathlib import Path
import sort

if __name__ =="__main__":
    
    while True:
        folder_to_scan = input('Please, enter the path of folder should be cleaned: ')
        if not Path(folder_to_scan).is_dir():
            print('The entered path is not a folder. Try again.')
        else:
            break

    while True:
        destination_folder = input('Please, enter the path of destination folder: ')
        if not Path(destination_folder).is_dir():
            _ = input('The entered folder does not exist. Do you want create new folder? (y/n): ')
            if _ == 'y':
                Path(destination_folder).mkdir(mode=511, exist_ok=True, parents=True)
                break
        else:
            break
        
            
    sort.read_folder(Path(folder_to_scan), Path(destination_folder))

    sort.handle_empty_folders(Path(folder_to_scan)) 
    
    exit()
    

