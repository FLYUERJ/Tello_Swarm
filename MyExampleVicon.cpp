#include "DataStreamClient.h"

#include <iostream>
#include <fstream>
#include <cassert>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string.h>

namespace aula
{
    class jonas{
        public:


        int idade;


};

} // namespace aula




int funcao2(){
    return 1;
}

int main(){

    std::string HostName = "152.92.155.4:801";

    //std::cout << "ALOOO";

    aula::jonas jonas1;
    
    ViconDataStreamSDK::CPP::Client ViconClient;

    bool conectado = ViconClient.Connect( HostName ).Result == ViconDataStreamSDK::CPP::Result::Success;

    
    std::cout << conectado << std::endl;

    

    return 0;
}