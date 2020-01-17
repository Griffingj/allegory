from flask import Flask
from root import ROOT_DIR

static_folder = ROOT_DIR + "/static"
app = Flask(__name__, static_url_path="/static", static_folder=static_folder)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def root():
    return app.send_static_file('chess.html')
