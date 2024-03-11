unsigned char buf[] = "toto";

int foo()
{
  return 42;
}

int bar()
{
  return 1337;
}

int main(int argc, char const *argv[])
{
  if (argc == 42)
  {
    foo();
    bar();
  }

  bar();

  return 0;
}
