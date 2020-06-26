import flask
from functions.face_compare import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
'''
@app.route('/api/v1/face_compare', methods=['POST'])
def face_compare():
    if 'img_1' in flask.request.files:
        file_1 = flask.request.files['img_1'].read()
    else:
        return "Error: img_1 is not provided."
    
    if 'img_2' in flask.request.files:
        file_2 = flask.request.files['img_2'].read()
    else:
        return "Error: img_2 is not provided."

    if 'threshold' in flask.request.form:
        threshold = float(flask.request.form.get('threshold'))
    else:
        threshold = 0.55

    dst,res,duration = face_compare_process(file_1,file_2,threshold)

    return flask.jsonify(
            result   = res,
            distance = dst,
            duration = duration,
        )

app.run(host='0.0.0.0')