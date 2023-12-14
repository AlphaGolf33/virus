#include <winsock2.h>
#include <stdio.h>

#pragma comment(lib, "ws2_32.lib")

int main()
{
  WSADATA wsaData;
  SOCKET clientSocket;
  struct sockaddr_in serverAddr;
  int iResult;

  // Initialiser Winsock
  iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
  if (iResult != 0)
  {
    printf("Erreur lors de l'initialisation de Winsock : %d\n", iResult);
    return 1;
  }

  // Créer la socket
  clientSocket = socket(AF_INET, SOCK_STREAM, 0);
  if (clientSocket == INVALID_SOCKET)
  {
    printf("Erreur lors de la création de la socket : %ld\n", WSAGetLastError());
    WSACleanup();
    return 1;
  }

  // Configuration de l'adresse du serveur
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
  serverAddr.sin_port = htons(1234);

  // Connecter à la socket du serveur
  iResult = connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
  if (iResult == SOCKET_ERROR)
  {
    printf("Erreur lors de la connexion au serveur : %d\n", WSAGetLastError());
    closesocket(clientSocket);
    WSACleanup();
    return 1;
  }

  // Envoyer "coucou"
  const char *message = "coucou";
  iResult = send(clientSocket, message, strlen(message), 0);
  if (iResult == SOCKET_ERROR)
  {
    printf("Erreur lors de l'envoi du message : %d\n", WSAGetLastError());
  }
  else
  {
    printf("Message envoyé avec succès : %s\n", message);
  }

  // Fermer la socket
  closesocket(clientSocket);

  // Terminer Winsock
  WSACleanup();

  return 0;
}
