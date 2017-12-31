import cfg
from ratelimiter import RateLimiter
from socket import socket as create_socket
class Chat:
    class __Chat:
        def __init__(self):
            self.socket = create_socket()
            self.socket.settimeout(5.0)
            self.connected = False
        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not Chat.instance:
            Chat.instance = Chat.__Chat()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def connect(self):
        s = self.socket
        s.connect((cfg.HOST, cfg.PORT))
        if not self.connected:
            s.send(("CAP REQ :twitch.tv/membership\r\n").encode())
            s.send(("CAP REQ :twitch.tv/tags\r\n").encode())
            s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
            s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
            s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))
            self.connected = True

    def get_message(self):
        return self.socket.recv(1024).decode("utf-8")

    def pong():
        """
        Send a twitch pong statement
        """
        self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

sock = Chat().socket
@RateLimiter(max_calls=20, period=30)
def say(msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))
    print("Message sent: %s" % ("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg)))

def ban(user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    user -- the user to be banned
    """
    say(".ban {}".format(user))

def timeout(user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    say(".timeout {}".format(user, secs))
