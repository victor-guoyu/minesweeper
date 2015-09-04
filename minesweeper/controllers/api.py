from cornice import Service

game = Service(name='game api', path='/game', description='game api service')


@game.get()
def create_game(request):
    return {'Hello': 'world'}


@game.post()
def hello_post(request):
    return{'msg': 'This is the hello world from post service'}