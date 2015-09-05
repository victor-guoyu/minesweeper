import json
import random
import string
from cornice.resource import resource, view
from webob import Response, exc
from minesweeper.models.game import Game

# store all the on going game
games = []


class _404(exc.HTTPError):

    def __init__(self, msg='Resource Not found'):
        body = {'status': 401, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 404
        self.content_type = 'application/json'


@resource(collection_path='/game', path='/game/{id}')
class GameResource:

    def __init__(self, request):
        self.request = request

    # create new game
    def collection_post(self):
        game_id = _create_id()
        game = Game(game_id)
        games.append(game)

        return {
            'id': game_id,
            'game_status': game.is_game_over(),
            'board': game.get_user_board()
        }

    # get existing game
    @view(renderer='json')
    def get(self):
        game_id = self.request.matchdict['id']
        game = _get_game_by_id(game_id)

        if game is None:
            raise _404()

        return {
            'id': game_id,
            'game_status': game.is_game_over(),
            'msg': 'get existing game',
            'board': game.get_user_board()
        }

    # update existing game
    @view(renderer='json')
    def post(self):
        game_id = self.request.matchdict['id']
        game = _get_game_by_id(game_id)

        if game is None:
            raise _404()

        data = self.request.json_body
        if data is not None:
            method = data['method']
            x = data['x']
            y = data['y']
            if method == 'open':
                game.open_cell(x, y)
            elif method == 'mark':
                game.mark_cell(x, y)
            else:
                pass

        return {
            'id': game_id,
            'game_status': game.is_game_over(),
            'board': game.get_user_board()
        }


def _create_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


def _get_game_by_id(game_id):
    for game in games:
        if game.game_id == game_id:
            return game
