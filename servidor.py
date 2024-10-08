from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pymongo import MongoClient
import json

# Conectar a MongoDB
client = MongoClient("mongodb+srv://grearte:xS8fu8gVPAz9qGWm@cluster0.dffoict.mongodb.net/?retryWrites=true&w=majority")
db = client['Turismo']
collection_lugares = db['lugar']

# Servidor HTTP
class ComentarioHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/comentario':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            comentario = data.get('comentario', [''])[0]

            # Insertar el comentario en la colección 'lugar'
            if comentario:
                collection_lugares.update_one(
                    {'nombre': 'Estacion'},  # Actualiza este criterio según cómo se almacenen los lugares
                    {'$push': {'comentarios': comentario}}
                )
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Muchas Gracias por su comentario, le agradecemos que contribuya a la mejora de la ciudad.")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Comentario no válido.")

def run(server_class=HTTPServer, handler_class=ComentarioHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor corriendo en el puerto {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
