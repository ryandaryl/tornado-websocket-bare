from tornado import websocket, web, ioloop
import os

client_list = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")
        for c in client_list:
            c.write_message("I'm here.")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in client_list:
            client_list.append(self)

    def on_close(self):
        if self in client_list:
            client_list.remove(self)


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    ioloop.IOLoop.instance().start()