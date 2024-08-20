#include <iostream>
#include "DataStreamClient.h"
#include <unistd.h>  // Para sleep()

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string>
#include <string.h>


using namespace ViconDataStreamSDK::CPP;

int createTelloSocket(){

    int sockfd;
    char buffer[1024];
    struct sockaddr_in servaddr;

    // Creating socket file descriptor
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return -1;
    }

    memset(&servaddr, 0, sizeof(servaddr));

    // Filling server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(8889);
    servaddr.sin_addr.s_addr = INADDR_ANY;

    const char *hello = "Hello from client";
    sendto(sockfd, hello, strlen(hello), MSG_CONFIRM, (const struct sockaddr *)&servaddr, sizeof(servaddr));
    std::cout << "Hello message sent." << std::endl;

    socklen_t len;
    int n;

    n = recvfrom(sockfd, (char *)buffer, 1024, MSG_WAITALL, (struct sockaddr *)&servaddr, &len);
    buffer[n] = '\0';
    std::cout << "Server : " << buffer << std::endl;

    close(sockfd);


}


int main()
{
    // Cria o cliente
    Client myClient;

    // Conecta ao servidor Vicon
    std::cout << "Connecting to Vicon server..." << std::endl;
    while (!myClient.IsConnected().Connected)
    {
        myClient.Connect("152.92.155.50:801");  // Substitua pelo endereço IP e porta do seu servidor Vicon
        std::cout << ".";
        sleep(1);
    }
    std::cout << "\nConnected!" << std::endl;

    // Configura o modo de transmissão
    myClient.SetStreamMode(StreamMode::ClientPull);

    // Configura o mapeamento de eixos
    myClient.SetAxisMapping(Direction::Forward, Direction::Left, Direction::Up);

    // Ativa os dados de segmentos
    myClient.EnableSegmentData();

    // Verifica se a ativação foi bem-sucedida
    if (!myClient.IsSegmentDataEnabled().Enabled)
    {
        std::cerr << "Failed to enable segment data!" << std::endl;
        return 1;
    }

    // Nome do sujeito e segmento para rastrear
    std::string subjectName = "disco";  // Nome do objeto que você está rastreando
    std::string segmentName = subjectName; // Para simplicidade, assumimos que o segmento principal tem o mesmo nome que o sujeito

    while (true)
    {
        // Atualiza os dados
        myClient.GetFrame();

        // Obtém a tradução global do segmento
        Output_GetSegmentGlobalTranslation translation = myClient.GetSegmentGlobalTranslation(subjectName, segmentName);

        if (translation.Result == Result::Success)
        {
            std::cout << "Object: " << subjectName << std::endl;
            std::cout << "Translation: " << translation.Translation[0] << ", "
                      << translation.Translation[1] << ", "
                      << translation.Translation[2] << std::endl;
        }
        else
        {
            std::cerr << "Failed to get translation for " << subjectName << std::endl;
        }

        sleep(1);  // Ajuste o intervalo conforme necessário
    }

    // Desconecta do servidor Vicon
    myClient.Disconnect();
    std::cout << "Disconnected from Vicon server." << std::endl;

    return 0;
}
