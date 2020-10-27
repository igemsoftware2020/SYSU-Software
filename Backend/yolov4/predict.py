from yolo import YOLO
from PIL import Image
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def predict(yolo, filename):
    image = Image.open(filename)
    ret = yolo.detect_image(image)
    image.close()
    return json.dumps(ret)

class PredictHandler(BaseHTTPRequestHandler):
    yolo = YOLO()

    def do_GET(self):
        if self.path.startswith('/predict/') == False:
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(bytes("404", "utf8"))
            return
        filename = self.path[9:]
        result = predict(PredictHandler.yolo, filename)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        self.wfile.write(bytes(result, "utf8"))
        return

server_address = ('127.0.0.1', 5002)
httpd = HTTPServer(server_address, PredictHandler)
httpd.serve_forever()

# predict('000252.jpg')
# predict('000252.jpg')