import flask
import time
from functions.face_compare import *

app = flask.Flask(__name__)

'''
Compare the face from 2 different picture
    input  : 
    - img_1     : first image to compare
    - img_2     : second image to compare
    - threshold : threshold for classification
    return : 
    - distance  : distance of image compare result using euclidean
    - duration  : execution time duration
    - result    : result of image comparation, 0 if same person, 1 if different person
    - message   : information about process result
'''
@app.route('/api/v1/face_compare', methods=['POST'])
def face_compare():
    if 'img_1' in flask.request.files:
        file_1 = flask.request.files['img_1'].read()
    else:
        return flask.jsonify(message="Error: img_1 is not provided."),500
    
    if 'img_2' in flask.request.files:
        file_2 = flask.request.files['img_2'].read()
    else:
        return flask.jsonify(message="Error: img_2 is not provided."),500

    if 'threshold' in flask.request.form:
        threshold = float(flask.request.form.get('threshold'))
    else:
        threshold = 0.55
    
    start = time.time()
    print("Image processing started")

    dst,res,message = face_compare_process(file_1,file_2,threshold)

    if not((res is None) and (dst is None)):
        return flask.jsonify(
                result   = res,
                distance = dst,
                duration = time.time() - start,
                message  = message
            ), 200
    else:
        return flask.jsonify(
                duration = time.time() - start,
                message  = message
            ), 500

app.run(host='0.0.0.0')