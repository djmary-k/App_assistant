import sys
from pathlib import Path
import sort

if __name__ =="__main__":
    
    folder_to_scan = sys.argv[1]
              
    sort.read_folder(Path(folder_to_scan), Path(folder_to_scan))

    sort.handle_empty_folders(Path(folder_to_scan)) 

    

