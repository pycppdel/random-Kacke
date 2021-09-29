#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <unistd.h>

#include <iostream>

int main(int argc, char** argv){

  int sock = socket(AF_INET, SOCK_STREAM, 0);

  struct sockaddr_in serv_addr;
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(10000);
  serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

  std::cout << connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));htons(
  std::cout.flush();

  close(sock);



  return 0;
}
