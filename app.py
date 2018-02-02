from tornado import websocket, web, ioloop
from tornroutes import route
import os

client_list = []
message = 'Someone else just visited, or refreshed their browser.'

def message_all(message):
    for client in client_list:
        client.write_message(message)

@route('/')
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")
        message_all(message)

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in client_list:
            client_list.append(self)

    def on_close(self):
        if self in client_list:
            client_list.remove(self)


app = web.Application(route.get_routes() + [(r'/ws', SocketHandler)])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    ioloop.IOLoop.instance().start()