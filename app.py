from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader
import os

# Настройка Jinja
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=True
)


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Обработка статических файлов
            if self.path.startswith('/static/'):
                filepath = os.path.join(os.getcwd(), self.path[1:])
                if os.path.exists(filepath):
                    self.send_response(200)
                    if filepath.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    with open(filepath, 'rb') as f:
                        self.wfile.write(f.read())
                    return
                else:
                    self.send_error(404)
                    return

            # Обработка HTML-шаблонов
            template_map = {
                '/': 'index.html',
                '/catalog': 'catalog.html',
                '/category': 'category.html',
                '/contacts': 'contacts.html'
            }

            if self.path in template_map:
                template = env.get_template(template_map[self.path])
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(template.render().encode('utf-8'))
                return

            self.send_error(404)

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'✅ Сервер запущен: http://localhost:{port}')
    httpd.serve_forever()


if __name__ == "__main__":
    run()