#!/usr/bin/env python3

import os
import socket
import subprocess
import threading

from flask import Flask, render_template, request

app = Flask(__name__)

conns = {}


class Conn(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        conns[self.port] = {
            'thread': self,
            'status': 'Attente de connexion...'
        }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(20)
        print(f'Waiting for connections on port {self.port}')

        try:
            client, addr = self.server_socket.accept()
            print(f'Connection from {addr} on port {self.port}')
            conns[self.port]['status'] = 'OK'
            client.close()
        except socket.timeout:
            conns[self.port]['status'] = 'KO: Server timout (20s)'
            print(f'Timeout 20s for port {self.port}')
            self.stop()

    def stop(self):
        print(f'Closing server on port {self.port}')
        self.server_socket.close()


def stop_thread(port):
    if port in conns:
        t = conns[port]['thread']
        t.stop()
        t.join()

def run_subprocess(file_path, port):
    try:
        subprocess.run([file_path])
    except Exception as e:
        conns[port]['status'] = f'KO: exe cassé : {e}'
        stop_thread(port)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    port = int(request.form['port'])
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    file_path = os.path.join('uploads', f'{port}.exe')
    uploaded_file.save(file_path)

    stop_thread(port)
    c = Conn(port)
    c.start()

    subprocess_thread = threading.Thread(target=run_subprocess, args=(file_path, port))
    subprocess_thread.start()

    return render_template('check.html', port=port)


@app.route('/status')
def status():
    port = int(request.args.get('port'))
    return conns[port]['status'] if port in conns else 'Unknown'


if __name__ == '__main__':
    app.run(debug=True)
