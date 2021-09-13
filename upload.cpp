#include <iostream>
#include <bits/stdc++.h>
#include <thread>
#include <chrono>

using namespace std::this_thread;
using namespace std::chrono;

void delay();

int main(){

  char** commands;

  commands = new char*[4];
  for(int i = 0; i < 4; i++){
    commands[i] = new char[100];
  }


  strncpy(commands[0], "git pull", 100);
  strncpy(commands[1], "git add .", 100);
  strncpy(commands[2], "git commit -m autosave", 100);
  strncpy(commands[3], "git push", 100);

  for(int i = 0; i < 4; i++){
    system(commands[i]);
    delay();
  }




  for(int i = 0; i < 4; i++){
    delete [] commands[i];
  }
  delete [] commands;
  return 0;
}

void delay(){

  sleep_until(system_clock::now()+seconds(2));
}
