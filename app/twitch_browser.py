import logging

from twitch_browser import app
from twitch_browser.settings import config

def start_server():
    init_logging()
    app.logger.info('starting server')
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug,
        use_reloader=config.use_reloader,
        use_evalex=config.use_evalex,
        processes=config.processes)

def init_logging():
    app.logger.setLevel(logging.DEBUG)
    for handler in config.log_handlers:
        app.logger.addHandler(handler)


if __name__ == '__main__':
    #print json.dumps(json.loads(fetchStreams('starcraft 2')), indent=4)
    start_server()
