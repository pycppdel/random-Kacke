#include <termios.h>
#include <iostream>
#include <unistd.h>

int main(){

  struct termios tty;

  tcgetattr(fileno(stdin), &tty);
  tty.c_cflag &= (~PARENB | ~CSTOPB | ~CSIZE | ~CRTSCTS | CREAD | CLOCAL);
  tty.c_cflag |= (CS5 | CS6 | CS7 | CS8);
  return 0;
}
