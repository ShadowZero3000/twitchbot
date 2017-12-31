import song
from chat import say
import re
CHAT_MSG=re.compile(r"^.*:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

def evaluate_message(msg):
    try:
        username = re.search(r"display-name=(\w+)", msg).group(1)
    except:
        username = "System"
    # Examine the message, and determine if a '!' prefixed command is in place
    trigger_words = re.match(r"(!\w+)(.*)", CHAT_MSG.sub("", msg))
    if trigger_words is not None:
        keyword = trigger_words.group(1)
        params = trigger_words.group(2).strip()
        for interaction in valid_interactions():
            if keyword in interaction['keywords']:
                interaction['method'](username, params)

def request_song(user, song_name):
    """
    User requests a song
    Keyword arguments:
    user -- the user's display name
    song_name -- the song to request
    """
    print("User '"+user+"' requested song: %s" % song_name)
    say("I'll ask Sparrow to play that for you, %s. We'll see what he says." % (user))
    song.request(user, song_name)

def current_song(user, message):
    """
    User requests the currently playing song be displayed
    Keyword arguments:
    user -- the user's display name
    message -- irrelevant what else they say
    """
    print("User '"+user+"' asked for current song")
    current_song=song.get_song()
    say("Current song: %s" % (current_song))

def get_commands(user, message):
    """
    User requests information about what they can ask for
    Keyword arguments:
    user -- the user's display name
    message -- irrelevant what else they say
    """
    say("Here's what I can do for you: ")
    for command in (x for x in valid_interactions() if x['display']):
        say(command['description']+': ['+", ".join(command['keywords'])+']')

def secret(user, message):
    """
    User requests a secret thing be done
    Keyword arguments:
    user -- the user's display name
    message -- irrelevant what else they say
    """
    say("This command isn't in the books.....for shame!")

def valid_interactions():
    # The wiring for interactions from users to their functions
    # name -- Internal name, not used
    # keywords -- '!' prefixed commands users can use to interact
    # method -- the method to run when this command is called. (Will get 'user' and 'message')
    # description -- The short display in help for this command
    # display -- Whether to show this command in the '!help' list
    return [
        {
            "name": "Song request",
            "keywords": ["!songrequest","!requestsong"],
            "method": request_song,
            "description": "Request a song",
            "display": True
        },{
            "name": "Get current song",
            "keywords": ["!currentsong","!whatsplaying","!song"],
            "method": current_song,
            "description": "Find out what's currently playing",
            "display": True
        },{
            "name": "Help",
            "keywords": ["!commands","!help"],
            "method": get_commands,
            "description": "Show a list of commands",
            "display": True
        },{
            "name": "Secret command",
            "keywords": ["!secret","!zero"],
            "method": secret,
            "description": "Secret, no description",
            "display": False
        }
    ]