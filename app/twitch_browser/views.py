import json
import time
import urllib
import urllib2

from flask import render_template, request

from twitch_browser import app
from twitch_browser import twitch_stream


@app.route('/')
def index():
    games = getGames()
    streams = getCombinedStreams(games)
    return render_template("index.html", streams=streams)


def getGames():
    games_cookie = request.cookies.get('games')
    if games_cookie is None:
        return ['Dota 2', 'StarCraft II: Heart of the Swarm', 'Dark Souls']
    encoded_games = games_cookie.split(':')
    return [urllib.unquote(encoded_game).decode('utf8') for encoded_game in encoded_games]


def getCombinedStreams(game_names):
    streams = []
    for game_name in game_names:
        raw_content = fetchStreams(game_name)
        streams += parseStreams(raw_content)
    return sorted(streams, key=lambda stream: stream.getViewerCount(), reverse=True)


def fetchStreams(game):
    start = time.time()
    host = "https://api.twitch.tv"
    path = "/kraken/streams"
    params = urllib.urlencode({
        'game': game,
        'limit': 50,
        })
    url = "%s%s?%s" % (host, path, params)
    headers = {
        'Accept': 'application/vnd.twitchtv.v2+json',
        'Client-ID': 'Twitch Browser https://github.com/jachien/twitch-browser'
    }
    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    content = resp.read()
    tot_time = time.time() - start
    app.logger.info('took %f secs to retrieve %s @ %s' % (tot_time, game, url))
    return content


def parseStreams(raw_content):
    streams = []
    streams_root = json.loads(raw_content)
    for stream in streams_root['streams']:
        streams.append(twitch_stream.TwitchStream(stream))
    return streams


@app.errorhandler(500)
def handleError(exc):
    app.logger.exception(exc)
    return render_template("error.html")
