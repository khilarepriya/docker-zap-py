from flask import Flask, Response, make_response

app = Flask(__name__)

@app.after_request
def apply_security_headers(response: Response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Permissions-Policy'] = "geolocation=(), camera=()"
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Server'] = ''
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'none'; "
        "media-src 'none'; object-src 'none'; frame-ancestors 'none'; "
        "base-uri 'self'; form-action 'self';"
    )
    return response

@app.route("/")
def home():
    return make_response("ZAP DAST Pipeline is Working!")

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow:", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return Response("<?xml version='1.0'?><urlset></urlset>", mimetype="application/xml")

@app.errorhandler(404)
def not_found(e):
    return make_response("404 - Not Found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)
