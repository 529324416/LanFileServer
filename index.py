# Lan Files Share System
# Author: Prince Biscuit
# Date: 2024/04/17


from urllib.parse import quote, unquote
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from file_handle import *
import argparse

class LanFileServer(Flask):

    def __init__(self):
        '''Init function
        @param root: root path of the share system
        '''

        super().__init__(__name__)
    
    def init_file_system(self, root):
        '''Init file system
        @param root: root path of the share system
        '''

        self.fileSystem = FileSystem(root)
    

app = LanFileServer()


def render_current():
    '''Render the current page'''

    # about breadcrumb
    _breadcrumb = [(name, f'/folder/{quote(url)}') for name, url in app.fileSystem.breadcrumb]
    _breadcrumb.insert(0, ("Home", "/folder"))

    # about folders and files
    idx = 2
    folders, files = app.fileSystem.contents
    folders = [
        {
            "num": idx + i,
            "name": folder.name,
            "url": f"/folder/{quote(folder.path_local)}",
        } for i, folder in enumerate(folders)
    ]

    idx += len(folders)
    files = [
        {
            "num": idx + i,
            "name": file.name,
            "url": "/download/" + quote(file.path_full),
            "filesize": 0,
            "filetype": "Unknown"
        } for i, file in enumerate(files)
    ]
    
    return render_template("index.html", breadcrumb=_breadcrumb, folders=folders, files=files)


@app.route("/")
def index():
    '''Index page'''

    return root_folder()

@app.route("/folder")
def root_folder():
    '''Root folder page'''

    return enter_folder("")

@app.route("/folder/<path:path_param>")
def enter_folder(path_param):
    '''Folder page'''

    # change state of file system
    if len(path_param) > 0:
        path_param = unquote(path_param)
        print(path_param)
        if not app.fileSystem.set_current_folder(path_param):
            return "something error happened"
    else:
        app.fileSystem.set_root_folder()
    return render_current()


@app.route("/move/parent")
def leave_folder():
    '''Leave the folder'''

    app.fileSystem.leave_folder()
    return render_current()

@app.route('/download/<path:path_param>')
def download_file(path_param):
    '''Download a file
    @param path_param: path of the file'''

    path_param = unquote(path_param)
    if os.path.exists(path_param) and os.path.isfile(path_param):
        return send_from_directory(os.path.dirname(path_param), os.path.basename(path_param), as_attachment=True)
    return "File not found"

if __name__ == '__main__':

    # parse root folder, host and port from args
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="C:\\Users\\Biscuit\\Desktop")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8688)
    args = parser.parse_args()

    app.init_file_system(args.root)
    app.run(host=args.host, port=args.port)