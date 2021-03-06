                                                                                                                                                                                                        _CIRCUITS__

#include <iostream>
#include <bitset>
#include "useful.h"

class LFSR{

private:

  std::bitset<8> bits = {0};

public:

  LFSR(int number);
  void print();
  int random_number(int bitlength);
};

LFSR::LFSR(int number){

  for(int i=0;i<8;i++){
    bool zahl = number & 1;
    bits[i] = zahl;
    number = number >> 1;
  }

}

void LFSR::print(){
  for(int i = 0; i<8;i++){
    std::cout<<bits[7-i];
  }
  std::cout << "\n";
}

int LFSR::random_number(int bitlength){
  int *numbers;
  numbers = new int[bitlength];

  for(int i=0;i<bitlength;i++){
    numbers[i] = bits[0] & 1;
    int value = bits[0] ^ bits[1];
    for(int x=0;x<7;x++){
      bits[x] = bits[x+1];
    }
    bits[7] = value;
  }

  int back = 0;

  for(int i=0;i<bitlength;i++){
    back += numbers[i] * hoch(2, i);
  }

  delete [] numbers;
  return back;
}

#endif
