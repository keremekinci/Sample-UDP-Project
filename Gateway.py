import socket
import json
import threading
import time

# Mutex'leri tanımla
mutex_HumidityAlive = threading.Lock()
mutex_HumidityData = threading.Lock()
mutex_TemperatureData = threading.Lock()


# Veri zaman damgalarını ve verilerini saklamak için değişkenler
HumidityAlive_timeStamp = 0
HumidityData_timeStamp = 0
TemperatureData_timeStamp = 0

HumidityAlive_data = ""
HumidityData_data = ""
Temperature_data = ""


def udp_server(port):
    server_address = ('127.0.0.1', port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(server_address)
        while True:
            data, client_address = server_socket.recvfrom(1024)
            received_data = data.decode('utf-8')
            # Convert the JSON-formatted string back to a list
            received_list = json.loads(received_data)
            print(received_list)
            data_type = received_list[1]

            # Mutex kullanarak verilere eş zamanlı erişimi kontrol et
            if data_type == "HumidityAlive":
                global HumidityAlive_timeStamp
                HumidityAlive_timeStamp = received_list[0]

            elif data_type == "HumidityData":
                print(received_data)
                global HumidityData_timeStamp
                global HumidityData_data
                HumidityData_timeStamp = received_list[0]
                HumidityData_data = received_list[2]

            elif data_type == "Temperature":
                global TemperatureData_timeStamp
                global TemperatureData_data
                TemperatureData_timeStamp = received_list[0]
                TemperatureData_data = received_list[2]

def HumidityAlive():
    global HumidityAlive_timeStamp
    global HumidityAlive_data
    HumidityAlive_timeStamp_old = 0
    sayac = 7
    gateway_address = ('127.0.0.1', 8080)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            if HumidityAlive_timeStamp == HumidityAlive_timeStamp_old:
                sayac = sayac+1
            elif HumidityAlive_timeStamp != HumidityAlive_timeStamp_old:
                HumidityAlive_timeStamp_old = HumidityAlive_timeStamp
                sayac = 0
            if(sayac >= 7):
                messageData = []
                messageData.append(HumidityAlive_timeStamp)
                messageData.append("Info")
                messageData.append("Humidity")
                messageData.append("HUMIDITY SENSOR OFF")
                json_message = json.dumps(messageData)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)
                pass
            elif(sayac <7):
                # print("Humidty On")
                pass
            time.sleep(1)


def HumidityData():
    global HumidityData_timeStamp
    global HumidityData_data
    HumidityData_timeStamp_old=0
    gateway_address = ('127.0.0.1', 8080)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            if HumidityData_timeStamp != HumidityData_timeStamp_old:
                HumidityData_timeStamp_old = HumidityData_timeStamp
                messageData = []
                messageData.append(HumidityData_timeStamp)
                messageData.append("Data")
                messageData.append("Humidity")
                messageData.append(HumidityData_data)
                json_message = json.dumps(messageData)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)
                # print(json_message)



            time.sleep(1)


def TemperatureData():
    global TemperatureData_timeStamp
    global TemperatureData_data
    TemperatureData_timeStamp_old = 0
    sayac = 3
    gateway_address = ('127.0.0.1', 8080)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            if TemperatureData_timeStamp == TemperatureData_timeStamp_old:
                sayac = sayac + 1
            elif TemperatureData_timeStamp != TemperatureData_timeStamp_old:
                messageData = []
                messageData.append(TemperatureData_timeStamp)
                messageData.append("Data")
                messageData.append("Temperature")
                messageData.append(TemperatureData_data)
                json_message = json.dumps(messageData)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)
                TemperatureData_timeStamp_old = TemperatureData_timeStamp
                sayac = 0

            if (sayac >= 3):
                messageData = []
                messageData.append(TemperatureData_timeStamp)
                messageData.append("Info")
                messageData.append("Temperature")
                messageData.append("TEMP SENSOR OFF")
                json_message = json.dumps(messageData)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)

            time.sleep(1)


if __name__ == "__main__":
    HumidityAlive_Thread = threading.Thread(target=HumidityAlive)
    HumidityData_Thread = threading.Thread(target=HumidityData)
    TemperatureData_Thread = threading.Thread(target=TemperatureData)

    HumidityAlive_Thread.start()
    HumidityData_Thread.start()
    TemperatureData_Thread.start()

    udp_port = 8888
    udp_server(udp_port)



