from cornice import Service

hello = Service(name='Hello', path='/hello', description='this is the hello controller')

@hello.get()
def hello_get(request):
    return {'Hello': 'world'}

@hello.post()
def hello_post(request):
    return{'msg': 'This is the hello world from post service'}