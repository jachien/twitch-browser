class TwitchStream(object):
    def __init__(self, stream_map):
        self.stream_map = stream_map

    def _getChannel(self):
        return self.stream_map['channel']

    def getStreamId(self):
        return self.stream_map['_id']

    def getUserDisplayName(self):
        return self._getChannel()['display_name']

    def getGameName(self):
        return self.stream_map['game']

    def getStatus(self):
        return self._getChannel()['status']

    def getUrl(self):
        return self._getChannel()['url']

    def getViewerCount(self):
        return self.stream_map['viewers']

    def getPreviewUrl(self):
        return self.stream_map['preview']
