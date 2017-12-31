# twitchbot
My personal twitch bot

Designed to be run on the desktop in a Docker container (in Virtualbox, thus the 192.168.99.100 IP) with a bound volume to the text file for currently playing song.
This allows for you to collect requests for songs from the bot, and to record what song is currently playing from a Chrome plugin. (Plugin calls the API, which writes to the file, which OBS can read)
