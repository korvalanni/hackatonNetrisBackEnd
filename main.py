import json
import logging


from config import CATEGORIES, RELEVANT_FROM_CONST
from modules.predict import classify

from flask import Flask, request, jsonify

app = Flask(__name__)

map = {}


@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'chunk_id' not in request.form or 'chunk' not in request.files or 'client_id' not in request.form or 'video_id' not in request.form or 'complete' not in request.form:
        return jsonify({"message": "Bad Request"}), 400

    chunk_id = request.form.get('chunk_id')
    video = request.files['chunk']
    client_id = request.form.get('client_id')
    video_id = request.form.get('video_id')
    complete = bool(request.form.get('complete'))

    print(chunk_id, video, client_id, video_id, complete)


    return jsonify({"message": "Successfully uploaded"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
