import http.server
from threading import Thread


class HelloHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set the response headers

        if self.path == "/path/to/valid-page.html":
            # Create a valid OK response
            self.send_response(200)
            body = b"<html><head><title>this is a test page</title></head><body><p>well hello there</p></body></html>"
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            # Set the response status code to 404 (Not Found)
            self.send_response(404)

            # Write the response body
            self.wfile.write(b"404 Not Found")


def before_feature(context, feature):
    # Start the HTTP server in a separate thread
    context.server = http.server.HTTPServer(("localhost", 8000), HelloHandler)
    context.thread = Thread(target=context.server.serve_forever)
    context.thread.start()


def after_feature(context, feature):
    context.server.shutdown()
    context.server.server_close()
    context.thread.join()
