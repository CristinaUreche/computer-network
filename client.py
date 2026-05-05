import socket
import json
import os

SERVER_HOST, SERVER_PORT = 'localhost', 5000
LOCAL_FILES_DIR = 'local_files'

class FTPClient:
    def __init__(self):
        self.socket = None
        self.authenticated = False
        if not os.path.exists(LOCAL_FILES_DIR): os.makedirs(LOCAL_FILES_DIR)
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER_HOST, SERVER_PORT))
        return True

    def send_command(self, data):
        self.socket.send(json.dumps(data).encode('utf-8'))
        return json.loads(self.socket.recv(4096).decode('utf-8'))

    def run(self):
        self.connect()
        while True:
            print("\n1. Login | 2. Create Local | 3. Upload | 4. Rename | 5. Read | 6. Download | 7. Edit | 9. List | 0. Exit")
            choice = input(">> ")
            if choice == '0': break
            
            if choice == '1':
                u, p = input("User: "), input("Pass: ")
                res = self.send_command({'command': 'login', 'username': u, 'password': p})
                if res['status'] == 'success': self.authenticated = True
                print(res['message'])
            
            elif not self.authenticated: print("Please login first!")
            
            elif choice == '4': # Rename
                old = input("Old name: ")
                new = input("New name: ")
                print(self.send_command({'command': 'rename_file', 'old_name': old, 'new_name': new})['message'])
                
            elif choice == '5': # Read
                fn = input("Filename to read: ")
                print(self.send_command({'command': 'read_file', 'filename': fn})['message'])
                
            elif choice == '6': # Download
                fn = input("Filename to download: ")
                res = self.send_command({'command': 'download', 'filename': fn})
                if res['status'] == 'success':
                    with open(os.path.join(LOCAL_FILES_DIR, fn), 'w') as f: f.write(res['content'])
                    print(f"File {fn} saved locally.")
                
            elif choice == '7': # Edit
                fn = input("Filename to edit: ")
                txt = input("New content: ")
                print(self.send_command({'command': 'edit_file', 'filename': fn, 'new_content': txt})['message'])
                
            elif choice == '9': # List
                res = self.send_command({'command': 'list_files'})
                print(f"Files: {res['files']}")

if __name__ == '__main__': FTPClient().run()