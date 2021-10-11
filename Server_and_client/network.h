#ifndef __NETW__
#define __NETW__


/*
File for a Server and a Client for linux and windows
*/


class Server{

public:

  struct Flags{

    int SOCKET_FAILED: 1;
    int BIND_FAILED: 1;
    int LISTEN_FAILED: 1;

  }__attribute__((packed));

private:

  int socket;

  int* connected_sockets;


};

class Client{

};
#endif
