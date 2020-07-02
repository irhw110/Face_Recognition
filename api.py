import flask
import time
from healthcheck import HealthCheck
from flask_restx import Api, Resource, apidoc
from flask import Blueprint, url_for, render_template, make_response
from functions.face_compare import *

app = flask.Flask(__name__)
app.config['DEBUG'] = False

#health check
health = HealthCheck()

class MyCustomApi(Api):
    def _register_apidoc(self, app: flask) -> None:
        conf = app.extensions.setdefault('restx', {})
        custom_apidoc = apidoc.Apidoc('restx_doc', 'flask_restx.apidoc',
                                      template_folder='templates', static_folder='static',
                                      static_url_path='/api/v1/face_comparation')

        @custom_apidoc.add_app_template_global
        def swagger_static(filename: str) -> str:
            return url_for('restx_doc.static', filename=filename)

        if not conf.get('apidoc_registered', False):
            app.register_blueprint(custom_apidoc)
        conf['apidoc_registered'] = True

api = MyCustomApi(app=app, doc='/api/v1/face_comparation/docs',prefix='/api/v1/face_comparation',
          version='1.0.0',default ='Compare',title='Flask-REST Face Comparation API')

@api.route('/compare')
class api_url(Resource):
    @api.doc(params={   'img_1': {'description': 'First face image to compare',
                                 'in': 'formData', 'type': 'file', 'required': 'true'},
                        'img_2': {'description': 'Second face image to compare',
                                 'in': 'formData', 'type': 'file', 'required': 'true'},
                        'threshold': {'description': 'Threshold for classification',
                                 'in': 'formData', 'type': 'float', 'default': 0.55}
                        })
                        
    @api.doc(responses={
        200: 'Success',
        422: 'Unprocessable Entity',
        500: 'Internal Server Error'
    })

    
    def post(self):
        img_extension = ['bmp','png','jpg','JPG','jpeg','tfif','tiff','tif']

        if 'img_1' in flask.request.files:
            if(flask.request.files['img_1'].filename.split('.')[-1] in img_extension):
                file_1 = flask.request.files['img_1'].read()
            else:
                return make_response(flask.jsonify({'message': 'uploaded file must be image file type', 'status': 'failed'}), 422)
        else:
            return make_response(flask.jsonify({'message': 'img_1 is not provided.', 'status': 'failed'}), 422)
        
        if 'img_2' in flask.request.files:
            if(flask.request.files['img_2'].filename.split('.')[-1] in img_extension):
                file_2 = flask.request.files['img_2'].read()
            else:
                return make_response(flask.jsonify({'message': 'uploaded file must be image file type', 'status': 'failed'}), 422)
        else:
            return make_response(flask.jsonify({'message': 'img_2 is not provided.', 'status': 'failed'}), 422)

        if 'threshold' in flask.request.form:
            threshold, valid = validate_threshold(flask.request.form.get('threshold'))
            if not valid:
                return make_response(flask.jsonify({'message': 'threshold must be a number and greater than 0.', 'status': 'failed'}), 422)
        else:
            threshold = 0.55
        
        start = time.time()
        print('Image processing started')

        dst,res,message = face_compare_process(file_1,file_2,threshold)

        if not((res is None) and (dst is None)):
            return make_response(flask.jsonify({
                    'result': {
                        'distance': dst,
                        'match': res,
                        'duration': time.time() - start,
                    },
                    'message': message,
                    'status': 'success'
            }), 200)
        else:
            return make_response(flask.jsonify({
                    'message': message,
                    'status': 'error'
            }), 500)

# Add a flask route to expose information
app.add_url_rule('/api/v1/face_comparation/health', 'healthcheck', view_func=lambda: health.run())

if __name__ == '__main__':
    app.run(host='0.0.0.0')