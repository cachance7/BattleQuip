import urllib2
import urlparse
import json
from util import *

class CommunicationError(Exception):
    def __init__(self, message):
        super(CommunicationException, self).__init__()
        self.message = message

class Connection(object):
    def __init__(self):
        pass

    def join(self, board, username):
        pass

    def fire(self, coord):
        pass

    def status(self):
        pass

class ConnectionZ(Connection):
    def __init__(self, host, port):
        """Prepares battleship connection for ongoing use.

        Args:
            host (str): the server game host
            port (str or int): the port on host for server

        """
        self.base_url = 'http://' + host + ':' + port

    def join(self, board, username='anon'):
        """Connects to a battleship server using the given name and board.

        Args:
            board (Board): initializes the server with a board
            name (str, optional): tells the server who you are.

        Raises:
            CommunicationException: if request fails in any way
        """
        response = self._post('/games/join', board=board.to_array(), user=username)
        if response:
            self.user = username
            self.game_id = response['game_id']

    def fire(self, coord):
        """Sends an attack to the server. Will fail if not user's turn (and also
        maybe if coord has been used before).

        Args:
            coord (Coord): a coordinate on the board to attack

        Returns:
            Attack object detailing result of player move

        Raises:
            CommunicationException: if request fails in any way
        """

        response = self._post('/games/fire',
                user=self.user, game_id=self.game_id, shot=str(coord))
        if response:
            return Attack(coord, **response)
        else:
            raise CommunicationException("Server did not respond with data.")

    def status(self):
        """Queries status of gameplay.

        Returns:
            Status object

        Raises:
            CommunicationException: if request fails in any way

        """
        response = self._get('/games/status',
                user=self.user, game_id=self.game_id)
        if response:
            return Status(**response)
        else:
            raise CommunicationException("Server did not respond with data.")

    def _get(self, path, **kwargs):
        """Sends a GET request -- url encoding any data provided.

        Args:
            path (str): the path to be appended to the base url
            **kwargs: will be url encoded

        Returns:
            response (dict): the response object after JSON parsing

        """
        return self._make_req(path, True, **kwargs)

    def _post(self, path, **kwargs):
        """Sends a POST request

        Args:
            path (str): the path to be appended to the base url
            **kwargs: will be JSON encoded

        Returns:
            response (dict): the response object after JSON parsing

        """
        return self._make_req(path, False, **kwargs)

    def _make_req(self, path, encode_request, **kwargs):
        """Does the 'heavy' lifting of communicating with the server and
        parsing the response.
        """
        if encode_request:
            data = urllib.urlencode(kwargs)
        else:
            data = json.dumps(kwargs)

        url = urlparse.urljoin(self.base_url, path)

        try:
            res = urllib2.urlopen(url, data).read()
        except ValueError:
            raise CommunicationException("Malformed url")
        except urllib2.URLError as urlerr:
            raise CommunicationException("Could not communicate with server")

        try:
            response = json.loads(res)
            return response
        except:
            raise CommunicationException("Failed to parse server response: "
                    + res)

