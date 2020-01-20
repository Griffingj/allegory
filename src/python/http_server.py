import asyncio
from threading import Lock
import json
from uuid import uuid4
from copy import deepcopy

from flask import Flask, request, jsonify

from root import ROOT_DIR
from src.python.chess.chess_interop import format_move
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_agency import ChessAgent

serve_folder = ROOT_DIR + "/serve"
app = Flask(__name__, static_url_path="/static", static_folder=serve_folder)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

analysis_lock = Lock()
loop = asyncio.get_event_loop()
shared = {
    "agent": None
}


@app.route("/")
def root():
    return app.send_static_file("chess.html")


@app.route("/api/analysis", methods=["POST"])
def create_analysis():
    request_id = str(uuid4())

    if analysis_lock.acquire(timeout=100):
        body = request.get_json()
        print(f"Request {request_id[:6]} for POST /api/analysis")
        print(json.dumps(body))
        out = {
            "result": None
        }
        chess_state = fen_to_state(body["fen"])
        shared["agent"] = ChessAgent(int(body["depth"]))

        def anaylsis():
            out["result"] = shared["agent"].start_game(chess_state)
        try:
            future = loop.run_in_executor(None, anaylsis)
            loop.run_until_complete(future)
        except Exception as e:
            print("Failed create_analysis: ")
            raise e
        finally:
            analysis_lock.release()

        (balance, best_path) = out["result"]
        next_move = next(best_path)
        next_state = deepcopy(shared["agent"].game)
        next_state.apply(next_move)
        next_fen = next_state.to_fen()
        resp = {
            "balance": balance,
            "move": format_move(next_move),
            "fen": next_fen,
            "done": next_state.is_done
        }
        print(f"Reponse {request_id[:6]} for POST /api/analysis")
        print(json.dumps(resp))
        return jsonify(resp)


@app.route("/api/analysis", methods=["DELETE"])
def stop_analysis():
    request_id = str(uuid4())
    print(f"Request {request_id[:6]} for DELETE /api/analysis")
    if shared["agent"] is not None:
        shared["agent"].stop()
    print(f"Request {request_id[:6]} for DELETE /api/analysis")
    return "Ok"


if __name__ == "__main__":
    app.run(debug=True)
