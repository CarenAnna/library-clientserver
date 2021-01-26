"""
----------------------------------------------------------------
Caren Groenhuijzen
01-07-2020
Eindopdracht gemaakt voor de leerlijn Python van NOVI Hogeschool
----------------------------------------------------------------
"""

import socket as s
import pickle as p

"""This client can connect to the server. 
It can receive strings and pickles. It can only send strings back to the server.
Four errors are caught, a message will let the client know what went wrong."""

HOST = s.gethostname()
PORT = 7007
socket = s.socket(s.AF_INET, s.SOCK_STREAM)

HEADERSIZE = 10
BUFFER = 1024

try:
    socket.connect((HOST, PORT))

    while True:
        full_msg = b""
        new_msg = True
        while True:
            msg = socket.recv(BUFFER)
            if new_msg:
                msg_len = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg) - HEADERSIZE*2 == msg_len:
                reply_string = "--> "
                if full_msg[HEADERSIZE:HEADERSIZE*2].decode("utf-8")[0] == 's':
                    full_msg = full_msg.decode("utf-8")
                    print(full_msg[HEADERSIZE * 2:])

                    if "enter" in full_msg.lower() and "username" in full_msg.lower():
                        reply_string = "Username: "

                    elif "enter" in full_msg.lower() and "password" in full_msg.lower():
                        reply_string = "Password: "

                elif full_msg[HEADERSIZE:HEADERSIZE*2].decode("utf-8")[0] == 'p':
                    received_object = p.loads(full_msg[HEADERSIZE*2:])
                    if type(received_object) == dict:
                        for key in received_object:
                            print(key)
                    else:
                        print(received_object)
                    socket.send(bytes(f"{len('Object received'):<{HEADERSIZE}}" + "Object received", "utf-8"))
                    break

                reply = input(reply_string)

                reply = f"{len(reply):<{HEADERSIZE}}" + reply
                socket.send(bytes(reply, "utf-8"))

                new_msg = True
                full_msg = b""

except ConnectionRefusedError:
    print("Server is not running. Try running the server first and then the client.")

except ConnectionResetError:
    print("Connection with server lost. \n"
          "Client will now be disconnected.")

except TimeoutError:
    print("Connection failed, server didn't respond. \n"
          "This could be caused by the server not having internet access.")

except ConnectionAbortedError:
    print("The server closed the connection.")
