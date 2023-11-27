#!/usr/bin/env python3

import os
import socket
import threading

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    port = request.form['port']
    file_path = os.path.join('uploads', f'{port}.exe')
    uploaded_file.save(file_path)
    return render_template('check.html', port=port)


@app.route('/status')
def status():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
