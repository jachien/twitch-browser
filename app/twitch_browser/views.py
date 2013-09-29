import json
import time
import urllib
import urllib2

from flask import render_template

from twitch_browser import app
from twitch_browser import twitch_stream


@app.route('/')
def index():
    games = ['Dota 2', 'StarCraft II: Heart of the Swarm', 'Dark Souls']
    streams = getGameStreams(games)
    return render_template("index.html", streams=streams)

@app.errorhandler(500)
def handleError(exc):
    app.logger.exception(exc)
    return render_template("error.html")

def getGameStreams(game_names):
    query = buildQuery(game_names)
    raw_content = fetchStreams(query)
    return parseStreams(raw_content)


def buildQuery(game_names):
    q = ''
    first = True
    for game_name in game_names:
        if first:
            first = False
        else:
            q += ' OR '
        q += '"%s"' % game_name
    return q


def fetchStreams(query):
    start = time.time()
    host = "https://api.twitch.tv"
    path = "/kraken/search/streams"
    params = urllib.urlencode({
        'q': query,
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
    app.logger.info('took %f secs to retrieve %s @ %s' % (tot_time, query, url))
    return content


def parseStreams(raw_content):
    streams = []
    streams_root = json.loads(raw_content)
    for stream in streams_root['streams']:
        streams.append(twitch_stream.TwitchStream(stream))
    return streams