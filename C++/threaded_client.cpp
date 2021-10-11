#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string>
#include <sstream>
#include <cstring>

#include <iostream>

int main(){

  int s;

  struct sockaddr_in data;
  std::stringstream transmitter;

  s = socket(AF_INET, SOCK_STREAM, 0);

  //making data

  data.sin_addr.s_addr = inet_addr("192.168.178.35");
  data.sin_port = htons(50000);
  data.sin_family = AF_INET;

  int z = connect(s, (struct sockaddr*)&data, sizeof(data));
  std::cout << z;

  char msg[20];

  while (true){

    std::cout << "Type your message: ";
    std::cin.getline(msg, 20);
    send(s, msg, sizeof(msg), 0);
    if (!(strncmp(msg, "quit", 20))){
      break;
    }
    recv(s, msg, sizeof(msg), 0);
    std::cout << msg << "\n";
  }

  std::cout << "ended connection";



  close(s);

  return 0;
}
