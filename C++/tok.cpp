#include <iostream>
#include <cstring>


char* clone(char* n, int size);

int main(){

  char u[] = "Hallo";
  strncpy(u, clone(u, sizeof(u)/sizeof(char)), sizeof(u)/sizeof(char));
  std::cout << u;
}

char* clone(char* n, int size){

  strncpy(n, "Hlo", size);
  return n;
}
