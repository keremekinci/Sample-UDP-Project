import socket
import json
import threading
import time
from urllib.parse import urlparse

HTTP_200_OK = "HTTP/1.0 200 OK\n\n"
HTTP_403_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
HTTP_400_BAD_REQUEST = "HTTP/1.0 403 Bad Request\n\n"
HTTP_404_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"

HumidityData_list = []
HumidityDataInfo_list = []
TemperatureData_list = []
TemperatureDataInfo_list = []

Client = None
Url = None

humidity_mutex = threading.Lock()
temperature_mutex = threading.Lock()


def udp_server():
    server_address = ('127.0.0.1', 8080)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(server_address)
        while True:#UDP
            data, client_address = server_socket.recvfrom(1024)
            received_data = data.decode('utf-8')
            print(received_data)
            received_list = json.loads(received_data)
            if received_list[2] == "Temperature":
                with temperature_mutex:
                    global TemperatureData_list
                    global TemperatureDataInfo_list
                    if (received_list[1] == "Data"):
                        TemperatureData_list = received_list
                    elif (received_list[1] == "Info"):
                        TemperatureDataInfo_list = received_list

            elif received_list[2] == "Humidity":
                with humidity_mutex:
                    global HumidityData_list
                    global HumidityDataInfo_list
                    if(received_list[1]=="Data"):
                        HumidityData_list = received_list
                    elif(received_list[1]=="Info"):
                        HumidityDataInfo_list = received_list


def SocketClient():
    global HumidityData_list
    global TemperatureData_list
    global Client
    global Url
    host = "127.0.0.1"
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    while True:
        try:
            client, address = server.accept()
            message = client.recv(1024).decode('utf8')
            parsed_url = urlparse(message)
            first_line = parsed_url.path.split('\n')[0]
            url = first_line.split(' ')[1]
            response = None
            if url == "/humidity":
                response = HumidityData_list
                # client.send(f"{HTTP_200_OK}{response}\n".encode('utf-8'))
                # client.send(f"{HTTP_200_OK}<html><body><h1>{response}</h1></body></html>\n".encode('utf-8'))
                Client = client
                Url = url
            elif url == "/temperature":
                response = TemperatureData_list
                Client = client
                Url = url

            else:
                Client = None
                response = "Invalid URL"
                client.send(f"{HTTP_200_OK}{response}\n".encode('utf-8'))

        except Exception as e:
            print(f'Beklenmeyen bir hata oluştu: {e}')



def HumidityData():
    global HumidityData_list
    global HumidityDataInfo_list
    global Client
    global Url
    while True:
        try:
            if(Client != None):
                if Url == "/humidity":
                    if HumidityDataInfo_list != None:
                        response = HumidityDataInfo_list
                        Client.send(f"{HTTP_200_OK}<html><body><h1>No Data: {response}</h1><script>window.location.reload();</script></body></html>\n".encode('utf-8'))
                        HumidityDataInfo_list = None
                        time.sleep(1)

                    elif len(HumidityData_list) != 0 :
                        response = HumidityData_list

                        Client.send(f"{HTTP_200_OK}<html><body><h1>Data: {response}</h1><script>window.location.reload();</script></body></html>\n".encode('utf-8'))
                        time.sleep(1)

                    else:
                        Client.send(f"{HTTP_200_OK}<html><body><h1>Gateway Kapali</h1><script>window.location.reload();</script></body></html>\n".encode('utf-8'))
                        time.sleep(1)
        except ConnectionAbortedError as e:
            print(f'Bağlantı hatası: {e}')



def TemperatureData():
    global TemperatureData_list
    global TemperatureDataInfo_list
    while True:
        try:
            if (Client != None):
                if Url == "/temperature":
                    if TemperatureDataInfo_list != None:
                        response = TemperatureDataInfo_list
                        Client.send( f"{HTTP_200_OK}<html><body><h1>No Data: {response}</h1><script>window.location.reload();</script></body></html>\n".encode('utf-8'))
                        TemperatureDataInfo_list = None
                        time.sleep(1)
                    elif len(TemperatureData_list) != 0:
                        response = TemperatureData_list
                        Client.send(f"{HTTP_200_OK}<html><body><h1>Data: {response}</h1><script>window.location.reload();</script></body></html>\n".encode( 'utf-8'))
                        time.sleep(1)
                    else:
                        Client.send(f"{HTTP_200_OK}<html><body><h1>Gateway Kapalı</h1><script>window.location.reload();</script></body></html>\n".encode('utf-8'))
                        time.sleep(1)

        except ConnectionAbortedError as e:
            print(f'Bağlantı hatası: {e}')


if __name__ == "__main__":
    HumidityData_Thread = threading.Thread(target=HumidityData)
    TemperatureData_Thread = threading.Thread(target=TemperatureData)
    UDP_Thread = threading.Thread(target=udp_server)
    SocketClient_Thread = threading.Thread(target=SocketClient)

    HumidityData_Thread.start()
    TemperatureData_Thread.start()
    UDP_Thread.start()
    SocketClient_Thread.start()
