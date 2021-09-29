#include <iostream>
#include <vector>
#include <algorithm>
#include "useful.h"

typedef std::vector<char*> charvec;
typedef std::vector<char*>::iterator charit;


int main(){

  srand(time(NULL));


  charvec liste = {"Brot", "Butter", "Milch"};
  print<std::vector<char*> >(liste);
  //find
  charit found = find(liste.begin(), liste.end(), "Milch");
  std::cout <<  found-liste.begin() << "\n\n";

  std::cout << shuffle(liste[0], 4);



  return 0;
}
