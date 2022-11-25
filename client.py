# client side
import socket
import pickle
import time
import config as conf

# https://note-tech.com/python_socket_programming_udp/#toc2

# IP for the destination which receive the message: server address
UDP_IP = conf.UDP_IP 
UDP_PORT = conf.UDP_PORT
WATER_PUMP_SERVER_ADDRESS = (UDP_IP, UDP_PORT)

# create a socket. IPv4 and UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message_to_watering_server(state, watering_duration, pause):
    message = {"state": state, "watering_duration":watering_duration, "pause": pause}
#     print('UDP target IP: ' + UDP_IP)
#     print('UDP target port: ' + str(UDP_PORT))
#     print ('message: ' + str(message))
#     print ('message type: ' + str(type(message)))
    message = pickle.dumps(message)
#     print ('pickled message: ' + str(message))
#     print ('pickled message type: ' + str(type(message)))
    sock.sendto(message, WATER_PUMP_SERVER_ADDRESS)
    
def close_socket():
    global sock
    print(str(sock))
    sock.close()
    print(str(sock))
