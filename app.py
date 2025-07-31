from flask import Flask, make_response

app = Flask(__name__)

# ✅ Utility function to apply security headers
def secure_response(content, status=200, mimetype="text/html"):
    response = make_response(content, status)
    response.mimetype = mimetype

    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'none'; "
        "object-src 'none'; base-uri 'self'; frame-ancestors 'none'; "
        "form-action 'self';"
    )
    response.headers['Permissions-Policy'] = "geolocation=(), camera=()"
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Server'] = ''
    return response

@app.route("/")
def hello():
    return secure_response("ZAP DAST Pipeline is Working!")

@app.route("/robots.txt")
def robots():
    return secure_response("User-agent: *\nDisallow:", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return secure_response("<?xml version='1.0'?><urlset></urlset>", mimetype="application/xml")

@app.errorhandler(404)
def not_found(e):
    return secure_response("404 - Not Found", status=404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)

