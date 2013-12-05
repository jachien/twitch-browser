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
    streams, api_time = getCombinedStreams(games)
    return render_template("index.html", streams=streams, api_time=api_time, num_games=len(games))


def getGames():
    games_cookie = request.cookies.get('games')
    if games_cookie is None:
        return ['Dota 2', 'StarCraft II: Heart of the Swarm', 'Dark Souls']
    elif games_cookie == "":
        return []
    encoded_games = games_cookie.split(':')
    return [urllib.unquote(encoded_game).decode('utf8') for encoded_game in encoded_games]


def getCombinedStreams(game_names):
    streams = []
    total_api_time = 0;
    for game_name in game_names:
        raw_content, api_time = fetchStreams(game_name)
        streams += parseStreams(raw_content)
        total_api_time += api_time
    return sorted(streams, key=lambda stream: stream.getViewerCount(), reverse=True), total_api_time


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
    return content, tot_time


def parseStreams(raw_content):
    streams = []
    streams_root = json.loads(raw_content)
    for stream in streams_root['streams']:
        streams.append(twitch_stream.TwitchStream(stream))
    return streams


@app.route('/manage-games')
def manageGames():
    return render_template("manage_games.html")


@app.errorhandler(500)
def handleError(exc):
    app.logger.exception(exc)
    return render_template("error.html")
