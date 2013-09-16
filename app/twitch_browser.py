import json
import urllib
import urllib2

from flask import Flask, render_template

import twitch_stream

app = Flask(__name__)


@app.route('/')
def index():
    streams = getMultiGameStreams(['dota 2', 'starcraft 2', 'dark souls'])
    return render_template("index.html", streams=streams)


def getMultiGameStreams(game_names):
    streams = []
    for game_name in game_names:
        raw_content = fetchStreams(game_name)
        streams += parseStreams(raw_content)
    return sorted(streams, key=lambda stream: (stream.getViewerCount(), stream.getUserDisplayName()), reverse=True)


def fetchStreams(game_name):
    host = "https://api.twitch.tv"
    path = "/kraken/search/streams"
    params = urllib.urlencode({
        'q': game_name
    })
    url = "%s%s?%s" % (host, path, params)
    headers = {
        'Accept': 'application/vnd.twitchtv.v2+json',
        'Client-ID': 'Twitch Browser https://github.com/jachien/twitch-browser'
    }
    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    return resp.read()


def parseStreams(raw_content):
    streams = []
    streams_root = json.loads(raw_content)
    for stream in streams_root['streams']:
        streams.append(twitch_stream.TwitchStream(stream))
    return streams

if __name__ == '__main__':
    app.run('0.0.0.0')
