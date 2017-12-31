import cfg
from ratelimiter import RateLimiter
from chat import Chat

sock = Chat().socket

@RateLimiter(max_calls=20, period=30)
def chat(msg):
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
    chat(sock, ".ban {}".format(user))

def timeout(user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))

def pong():
    sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))