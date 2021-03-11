import time
import json

from aiohttp import web

import simple_auth

# CRUNCHES
notes = []
users = [("First User", "Someones_password"),
         ("Second User", "Very_strong_pass")]
# CRUNCHES


async def api_create(request):
    t = time.localtime()
    note_id = 0 if not notes else notes[-1].get('id')
    post = await request.post()
    if 'text' not in post:
        return web.Response(text='Note can\'t be empty', status=400)
    text = post['text']
    if 'username' not in post:
        return web.Response(text='Username can\'t be empty', status=401)
    username = post['username']
    auth_token = request.cookies.get('auth_token', None)
    if not auth.check_user(username, auth_token):
        return web.Response(text='Unauthorized', status=401)
    notes.append({'id': note_id + 1,
                  'username': username,
                  'text': text,
                  'date': time.strftime('%d.%m.%Y %H:%M:%S', t),
                  'unix_time': time.mktime(t)})
    return web.Response(text='ok')


async def api_read(request):
    return web.Response(text=json.dumps(notes), content_type='application/json')


async def api_update(request):
    t = time.localtime()
    post = await request.post()
    if 'text' not in post or 'id' not in post:
        return web.Response(text='Note or ID can\'t be empty', status=400)
    text = post['text']
    note_id = int(post['id'])
    if 'username' not in post:
        return web.Response(text='Username can\'t be empty', status=401)
    username = post['username']
    auth_token = request.cookies.get('auth_token', None)
    if not auth.check_user(username, auth_token):
        return web.Response(text='Unauthorized', status=401)
    note_with_given_id = next((item for item in notes if item['id'] == note_id), None)
    if note_with_given_id is None:
        return web.Response(text='Invalid ID.', status=400)
    note_with_given_id['text'] = text
    note_with_given_id['date'] = time.strftime('%d.%m.%Y %H:%M:%S', t)
    note_with_given_id['unix_time'] = time.mktime(t)
    note_with_given_id['username'] = username
    return web.Response(text='ok')


async def api_delete(request):
    post = await request.post()
    if 'id' not in post:
        return web.Response(text='ID can\'t be empty', status=400)
    note_id = int(post['id'])
    if 'username' not in post:
        return web.Response(text='Username can\'t be empty', status=401)
    username = post['username']
    auth_token = request.cookies.get('auth_token', None)
    if not auth.check_user(username, auth_token):
        return web.Response(text='Unauthorized', status=401)
    note_with_given_id = next((item for item in notes if item['id'] == note_id), None)
    if note_with_given_id is None:
        return web.Response(text='Invalid ID.', status=400)
    notes.remove(note_with_given_id)
    return web.Response(text='ok')

app = web.Application()
app.add_routes([web.post('/api/create', api_create),
                web.route('*', '/api/read', api_read),
                web.post('/api/update', api_update),
                web.post('/api/delete', api_delete)])
auth = simple_auth.Authenticate(users)

if __name__ == '__main__':
    web.run_app(app)
