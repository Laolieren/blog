from werkzeug.routing import BaseConverter


class Regexconverter(BaseConverter):

    def __init__(self, url_map, regex):
        super(Regexconverter, self).__init__(url_map)
        self.regex = regex
