
import logging
import logging.handlers

from config import Config

log_file = '/var/log/twitch-browser/twitch-browser.log'
log_format = '%(asctime)s %(levelname)-8s [%(module)s] %(msg)s'
file_handler = logging.handlers.TimedRotatingFileHandler(
    log_file,
    when='midnight',
    interval=1,
    backupCount=28)
file_handler.setFormatter(logging.Formatter(log_format))

config = Config(
    host='0.0.0.0',
    port=5000,
    debug=True,
    use_reloader=False,
    use_evalex=False,
    processes=16,
    log_handlers=[
        file_handler,
    ],
)

try:
    from twitch_browser.settings import local
    config.update(local.config)
except ImportError:
    pass
