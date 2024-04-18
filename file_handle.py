import os


def split_path(path:str) -> list:
    '''Split the path into a list of dir names'''

    path = path.strip("\\").strip('/')
    if len(path) == 0:
        return list()
    
    start, idx = 0, 0
    output = list()
    for char in path:
        if char == '\\' or char == '/':
            output.append(path[start : idx])
            start = idx + 1
        idx += 1
    output.append(path[start : idx])
    return output


class File:
    '''This class is used to handle file operations'''

    def __init__(self, path_full):
        '''Init function
        @param fullpath: full path of the file
        '''

        self.name = os.path.basename(path_full)
        self.path_full = path_full

    def __repr__(self) -> str:
        '''Represent the file'''

        return f"File: <{self.path_full}>"

class Folder:

    def __init__(self, path_local, path_full):
        '''Init function
        @param fullpath: full path of the folder
        '''

        self.name = os.path.basename(path_full)
        self.path_local = path_local
        self.path_full = path_full
    
    def invoke(self) -> tuple:
        '''Invoke the folder to get files and folders in it'''

        objects = os.listdir(self.path_full)
        files, folders = [], []
        for obj in objects:
            filepath = os.path.join(self.path_full, obj)
            local = os.path.join(self.path_local, obj)
            if os.path.isfile(filepath):
                files.append(File(filepath))
            else:
                folders.append(Folder(local, filepath))
        return files, folders
    
    def contains_folder(self, folder_name):
        '''Check if the folder contains a folder'''

        if not self.__is_invoked:
            self.invoke()
        for folder in self.__folders:
            if folder.name == folder_name:
                return True
        return False
    
    def __repr__(self) -> str:
        '''Represent the folder'''

        return f"Folder: <{self.path_full}>"


class FileSystem:
    '''This class is used to handle file operations'''

    def __init__(self, root:str):
        '''Init function
        @param root: root path of the share system
        '''

        self.__root = root
        if not os.path.exists(root) or os.path.isfile(root):
            raise ValueError("Root path does not exist or is a file")
        
        self.__path = str()
        self.__path_queue = list()
        self.__folder = Folder(self.__path, root)

        self.__cache = dict()
        self.__cache.setdefault(self.__path, self.__folder)

    @property
    def breadcrumb(self) -> list:
        '''Get the breadcrumb of the current path'''

        output = list()
        for idx, name in enumerate(self.__path_queue):
            url = os.path.join(*self.__path_queue[:idx+1])
            url = url.replace('\\', '/')
            output.append((name, url))
        return output

    @property
    def contents(self) -> list:
        '''Get the contents of the current path'''

        files, folders = self.__folder.invoke()
        return folders, files
    
    def __read_now(self):
        '''Read the current path'''

        if self.__path in self.__cache:
            self.__folder = self.__cache[self.__path]
        else:
            self.__folder = Folder(self.__path, os.path.join(self.__root, self.__path))
            self.__cache.setdefault(self.__path, self.__folder)

    def enter_folder(self, name:str) -> bool:
        '''Enter a folder
        @param folder: folder name
        '''

        if not self.__folder.contains_folder(name):
            return False
        self.__path = os.path.join(self.__path, name)
        self.__path_queue.append(name)
        self.__read_now()
        return True
    
    def leave_folder(self) -> bool:
        '''Leave the folder'''

        if len(self.__path) == 0:
            return False
        
        self.__path = os.path.dirname(self.__path)
        self.__path_queue.pop()
        self.__read_now()
        return True
    
    def set_current_folder(self, path:str) -> bool:
        '''Set the current folder
        @path: relative path to root'''

        if not os.path.exists(os.path.join(self.__root, path)):
            return False
        
        self.__path = path
        self.__path_queue = split_path(path)
        self.__read_now()
        return True
    
    def set_root_folder(self):
        '''Set the root folder'''

        self.__path = str()
        self.__path_queue = list()
        self.__read_now()


if __name__ == '__main__':

    x = FileSystem("C:\\Users\\Biscuit\\Desktop")
    x.set_current_folder("草稿/.vscode")
    for value in x.contents:
        print(value)

    print(x.breadcrumb)
