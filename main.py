from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('chess.html')