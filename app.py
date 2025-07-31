from flask import Flask, Response, make_response

app = Flask(__name__)

@app.after_request
def set_security_headers(response: Response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'none'; "
        "object-src 'none'; base-uri 'self'; frame-ancestors 'none';"
    )
    response.headers['Permissions-Policy'] = "geolocation=(), camera=()"
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Server'] = ''
    return response

@app.route("/")
def hello():
    return "ZAP DAST Pipeline is Working!"

@app.errorhandler(404)
def not_found(e):
    response = make_response("404 - Not Found", 404)
    response.mimetype = "text/html"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)

