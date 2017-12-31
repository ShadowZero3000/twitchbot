# bot.py
import api
import cfg
import socket
import time

from interactions import evaluate_message
from threading import Thread

# network functions go here
from chat import Chat

def loop():
    twitch = Chat()
    twitch.connect()
    time.sleep(3)
    while True:
        try:
            response = twitch.get_message()
            #DEBUG
            #print("Reponse:"+response)
            if response == "PING :tmi.twitch.tv\r\n":
                twitch.pong()
            elif response:
                evaluate_message(response)
        except socket.timeout:
            debug_event = True
            #print("Socket Timed Out!")

        except socket.error:
            print("Socket Error, Connection closed!")
            time.sleep(1)
            twitch.connect()
        except Exception as e:
            print("Unknown error")
            print(e)
        #TODO: Find a better sleep cycle. Rate limiting already in place
        time.sleep(1 / cfg.RATE)


apiThread = Thread(target=api.createServer)
apiThread.start()

#DEBUG
print("API Thread launched")


botThread = Thread(target=loop)
botThread.start()

#DEBUG
print("Bot Thread launched")