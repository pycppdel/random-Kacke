#include <iostream>

int main(){
  int z = 8;
  int* p = &z;
  p += 99;
  std::cout << (*p);
  return 0;
}
