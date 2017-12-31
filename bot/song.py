import urllib
import datetime

def request(user, song_name):
    message = "User: '%s' requested song: '%s'" % (user, song_name)
    print(message)
    f = open('requested_songs.txt', 'a')
    f.write("\r\n"+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))\
        +' '+message)
    f.close()

def get_song():
    f = open('current_song.txt', 'r')
    song = f.read()
    f.close()
    return urllib.parse.unquote(song)

def set_song(song_name):
    song_name = urllib.parse.unquote(song_name)
    if song_name == 'undefined':
        song_name = ''
    print("Setting current song to: %s" % (song_name))
    f = open('current_song.txt', 'w')
    f.write(song_name)
    f.close()
    return song_name