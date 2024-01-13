import socket
import random
import time
import json

def humidity_sensor():
    gateway_address = ('127.0.0.1', 8888)
    second=0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            humidity_value = random.randint(40, 90)
            timestamp = time.time()
            formatted_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
            if humidity_value > 80:
                messageData = []
                messageData.append(formatted_time)
                messageData.append("HumidityData")
                messageData.append(humidity_value)
                json_message = json.dumps(messageData)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)
                print(json_message)
            if second % 3 == 0:
                messageAlive = []
                messageAlive.append(formatted_time)
                messageAlive.append("HumidityAlive")
                messageAlive.append("ALIVE")
                json_message = json.dumps(messageAlive)
                client_socket.sendto(json_message.encode('utf-8'), gateway_address)
                print(json_message)

            # print("Running...")
            time.sleep(1)
            second = second + 1

if __name__ == "__main__":
    humidity_sensor()