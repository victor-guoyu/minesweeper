import os
import binascii
from cornice.resource import resource, view


@resource(collection_path='/game', path='/game/{id}')
class GameResource:
    _games = []

    def __init__(self, request):
        self.request = request

    # create new game
    def collection_post(self):
        return {
            "id": _create_id(),
            "msg": "create new game with collection post",
        }

    @view(renderer='json')
    def get(self):
        game_id = self.request.matchdict['id']
        return {
            'id': game_id,
            'msg': 'get existing game',
        }

    @view(renderer='json')
    def post(self):
        game_id = self.request.matchdict['id']
        return {
            "id": game_id,
            'msg': 'post existing game',
        }


def _create_id():
    return binascii.b2a_hex(os.urandom(20))
