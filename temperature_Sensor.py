import socket
import random
import time
import json

def temperature_sensor():
    gateway_address = ('127.0.0.1', 8888)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            temperature_value = random.uniform(20.0, 30.0)
            timestamp = time.time()
            formatted_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
            message =[]
            message.append(formatted_time)
            message.append("Temperature")
            message.append(temperature_value)
            json_message = json.dumps(message)
            client_socket.sendto(json_message.encode('utf-8'), gateway_address)
            print(json_message)
            # print("Running...")
            time.sleep(1)


if __name__ == "__main__":
    temperature_sensor()