import json
import logging
import logging.handlers
import os
import time
import urllib
import urllib2

from flask import Flask, render_template

import twitch_stream

app = Flask(__name__)

def start_server():
    init_logging()
    app.logger.info('starting server')
    app.run('0.0.0.0', debug=True, use_reloader=False, use_evalex=False, threaded=True)

def init_logging():
    app.logger.setLevel(logging.DEBUG)
    log_path = os.path.join('c:/', 'cygwin', 'var', 'log', 'twitch-browser', 'twitch-browser.log')
    handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when='midnight',
        interval=1,
        backupCount=28)
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s [%(module)s] %(msg)s'))
    app.logger.addHandler(handler)

@app.route('/')
def index():
    games = ['dota 2', 'starcraft 2', 'dark souls']
    start = time.time()
    streams = getMultiGameStreams(games)
    tot_time = time.time() - start
    app.logger.info('retrieved streams for %d games in %f secs' % (len(games), tot_time))
    return render_template("index.html", streams=streams)

@app.errorhandler(500)
def handleError(exc):
    app.logger.exception(exc)
    return render_template("error.html")

def getMultiGameStreams(game_names):
    streams = []
    for game_name in game_names:
        raw_content = fetchStreams(game_name)
        streams += parseStreams(raw_content)
    return sorted(streams, key=lambda stream: (stream.getViewerCount(), stream.getUserDisplayName()), reverse=True)


def fetchStreams(game_name):
    start = time.time()
    host = "https://api.twitch.tv"
    path = "/kraken/search/streams"
    params = urllib.urlencode({
        'q': game_name,
        'limit': 20,
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
    app.logger.info('took %f secs to retrieve %s @ %s' % (tot_time, game_name, url))
    return content


def parseStreams(raw_content):
    streams = []
    streams_root = json.loads(raw_content)
    for stream in streams_root['streams']:
        streams.append(twitch_stream.TwitchStream(stream))
    return streams

if __name__ == '__main__':
    #print json.dumps(json.loads(fetchStreams('starcraft 2')), indent=4)
    start_server()
