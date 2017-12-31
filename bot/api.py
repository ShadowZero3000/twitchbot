from flask import Flask, request
from flask_cors import CORS, cross_origin
import urllib
import song

def createServer():
    api = Flask(__name__)
    CORS(api)

    def interrupt():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @api.route('/', methods=['POST'])
    def result():
        print(request.json['foo']) # should display 'bar'
        return 'Received !' # response to your request.

    @api.route('/api/currentsong', methods=['GET','OPTIONS'])
    def get_song():
        return song.get_song()

    @api.route('/api/currentsong', methods=['POST','OPTIONS'])
    def set_song():
        song.set_song(request.json['song'])
        return 'Song written.' # response to your request.

    api.run(host='0.0.0.0')
