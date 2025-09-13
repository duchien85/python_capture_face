from flask import Flask, render_template
from routes.face_routes import bp as face_bp

app = Flask(__name__)
app.register_blueprint(face_bp)

@app.route('/')
def index():
    return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)
# if __name__ == "__main__":
#     # Khi chạy Flask, cần cho phép bind ra tất cả interface (LAN, WiFi, v.v.) bằng host='0.0.0.0'.
#     app.run(host="0.0.0.0", port=5000, debug=True)

# if __name__ == "__main__":
#     # Chạy HTTPS, cho phép LAN
#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         ssl_context=("certs/cert.pem", "certs/key.pem"),
#         debug=True
#     )

if __name__ == "__main__":
    # Load cert đã tạo bằng mkcert
    cert_file = "./certs/127.0.0.1+1.pem"
    key_file = "./certs/127.0.0.1+1-key.pem"

    # host="0.0.0.0" để chạy cho cả LAN
    app.run(
        host="0.0.0.0",
        port=5000,
        ssl_context=(cert_file, key_file),
        debug=True
    )