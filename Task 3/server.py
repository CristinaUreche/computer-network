import socket
import json
import os
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 5000
FILES_DIR = 'files'
DEFAULT_USER = 'student'
DEFAULT_PASSWORD = '1234'

def ensure_files_dir():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

def authenticate(username, password):
    return username == DEFAULT_USER and password == DEFAULT_PASSWORD

def handle_client(conn, addr):
    authenticated = False
    try:
        while True:
            request_data = conn.recv(4096).decode('utf-8')
            if not request_data: break
            request = json.loads(request_data)
            command = request.get('command')
            
            if command == 'login':
                if authenticate(request.get('username'), request.get('password')):
                    authenticated = True
                    response = {'status': 'success', 'message': 'Welcome!'}
                else:
                    response = {'status': 'error', 'message': 'Invalid credentials'}
            
            elif not authenticated:
                response = {'status': 'error', 'message': 'Not authenticated'}
            
            elif command == 'create_file':
                filepath = os.path.join(FILES_DIR, request.get('filename'))
                with open(filepath, 'w') as f: f.write(request.get('content', ''))
                response = {'status': 'success', 'message': 'File created'}

            elif command == 'upload':
                filepath = os.path.join(FILES_DIR, request.get('filename'))
                with open(filepath, 'w') as f: f.write(request.get('content'))
                response = {'status': 'success', 'message': 'File uploaded'}

            elif command == 'rename_file':
                old_path = os.path.join(FILES_DIR, request.get('old_name'))
                new_path = os.path.join(FILES_DIR, request.get('new_name'))
                os.rename(old_path, new_path)
                response = {'status': 'success', 'message': 'File renamed'}

            elif command == 'read_file':
                filepath = os.path.join(FILES_DIR, request.get('filename'))
                with open(filepath, 'r') as f: content = f.read()
                response = {'status': 'success', 'message': content}

            elif command == 'download':
                filepath = os.path.join(FILES_DIR, request.get('filename'))
                with open(filepath, 'r') as f: content = f.read()
                response = {'status': 'success', 'content': content}

            elif command == 'edit_file':
                filepath = os.path.join(FILES_DIR, request.get('filename'))
                with open(filepath, 'w') as f: f.write(request.get('new_content'))
                response = {'status': 'success', 'message': 'File updated'}

            elif command == 'list_files':
                response = {'status': 'success', 'files': os.listdir(FILES_DIR)}

            elif command == 'logout':
                authenticated = False
                response = {'status': 'success', 'message': 'Logged out'}
            
            conn.send(json.dumps(response).encode('utf-8'))
    except Exception as e:
        conn.send(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
    finally:
        conn.close()

def start_server():
    ensure_files_dir()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__': start_server()