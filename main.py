import json
import logging
import sys
import heapq
from typing import List, Tuple
import cv2
from openvino.runtime import Core

from config import CATEGORIES, RELEVANT_FROM_CONST
from flask_cors import CORS

from flask import Flask, request, jsonify

from utils.openvino_utils import detect
from utils.draw_utils import draw_results_with_motion
from utils.model_utils import dict_classes
from utils.motion_finder import MotionFinder

print(' ')
app = Flask(__name__)
CORS(app, origins='*', resources={
    r'*': {'origins': '*'}}, allow_headers=["Content-Type"])
app.config['CORS_HEADERS'] = 'Content-Type'

# Куча для каждого видосика
video_chunks = {}
videos = dict()

motion_finder = MotionFinder()
ie = Core()
model = ie.read_model(model="weights/yolov8n_1280_ufo_best_int8_openvino_model/yolov8n_1280_ufo_best.xml")
compiled_model = ie.compile_model(model=model, device_name="CPU")
output_layer = compiled_model.output(0)


@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'chunk_id' not in request.form or 'chunk' not in request.files or 'client_id' not in request.form or 'video_id' not in request.form or 'complete' not in request.form:
        return jsonify({"message": "Bad Request"}), 400

    chunk_id = int(request.form.get('chunk_id'))  # Должен быть int для порядка
    chunk = request.files['chunk'].read()
    client_id = request.form.get('client_id')
    video_id = request.form.get('video_id')
    complete = bool(request.form.get('complete'))

    # print(chunk_id, video, client_id, video_id, complete, file=sys.stderr)

    if video_id not in video_chunks:
        video_chunks[video_id] = []

    # Чанк в кучу
    heapq.heappush(video_chunks[video_id], (-chunk_id, chunk, client_id, complete))

    return jsonify({"message": "Successfully uploaded"}), 200


@app.route('/get-video', methods=['GET'])
def get_video():
    print(get_video_chunks("697112b8-fb2e-4260-a2e1-7d9473c89606"), file=sys.stderr)

    return jsonify({"data": "A net data"}), 200


def get_video_chunks(video_id: str) -> List[Tuple]:
    if video_id not in video_chunks:
        return []

    chunks_data = []
    while video_chunks[video_id]:
        _, chunk, client, is_last_chunk = heapq.heappop((video_chunks[video_id]))
        chunks_data.append((chunk, client, is_last_chunk))

    # Фетч чанков закончен
    del video_chunks[video_id]
    videos[id] = chunks_data
    return chunks_data



def get_video_from_heap():
    for video in videos:
        yield videos[video]


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
