from flask import Flask, make_response

app = Flask(__name__)

def secure_response(content, status=200, mimetype="text/html"):
    response = make_response(content, status)
    response.mimetype = mimetype

    # Mandatory site isolation headers
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

    # Other security headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Permissions-Policy'] = "geolocation=(), camera=()"
    response.headers['Server'] = ''
    return response

@app.route("/")
def home():
    return secure_response("ZAP DAST Pipeline is Working!")

@app.route("/robots.txt")
def robots():
    return secure_response("User-agent: *\nDisallow:", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return secure_response("<?xml version='1.0'?><urlset></urlset>", mimetype="application/xml")

@app.errorhandler(404)
def page_not_found(e):
    return secure_response("404 - Not Found", status=404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)
