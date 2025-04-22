import os

def remove_files(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            if file in {'Cmap.npy', 'P,noy'}:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'File deleted: {file_path}')
                except Exception as e:
                    print(f'Error deleting: {file_path}: {e}')
                    
work_dir = os.getcwd()
remove_files(work_dir)
