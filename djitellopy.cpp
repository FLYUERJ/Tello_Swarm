#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string>


class Tello{
protected:

    std::string ip_addr = "192.168.10.1";
    int port = 8889;

    int tello_socket;

public:


    Tello(){
        
    }



};


int main(){

    Tello objeto1 = Tello();


}