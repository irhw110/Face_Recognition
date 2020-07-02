import cv2
import dlib
import numpy as np # upgrade to 1.8.0
from scipy.spatial import distance

'''
Get largest detected faces from an image
    input : image (png,jpg,jfif,jpeg)
    return: rectangle
'''
def crop_face(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_detector = dlib.get_frontal_face_detector()
    detected_faces = face_detector(image, 1)
    if(len(detected_faces)==0):
        return None
    else:
        max = 0
        for i,face_rect in enumerate(detected_faces):
            if((face_rect.width()+face_rect.height()) > (detected_faces[max].width()+detected_faces[max].height())):
                max = i
        return detected_faces[max]

'''
Check if a input threshold can be converted to float and is greater than 0
    input : string
    return: threshold: float, valid: boolean
'''
def validate_threshold(threshold_string):
    valid = False
    try :  
        threshold = float(threshold_string) 
        if(threshold > 0):
            valid = True
    except : 
        threshold = None

    return threshold, valid
    

'''
Compare the face from 2 different picture
    input  : 
    - img_1     : first image to compare
    - img_2     : second image to compare
    - threshold : threshold for classification
    return : 
    - dst       : distance of image compare result using euclidean
    - res       : result of image comparation, True if same person, False if different person
    - message   : information about process result
'''
def face_compare_process(img_file_1, img_file_2, threshold):
    try:
        # Load image 1 and image 2 file
        img_1 = cv2.imdecode(np.frombuffer(img_file_1, np.uint8), cv2.COLOR_BGR2RGB)
        img_2 = cv2.imdecode(np.frombuffer(img_file_2, np.uint8), cv2.COLOR_BGR2RGB)
        
        # Crop face from both image
        dets_1 = crop_face(img_1)
        dets_2 = crop_face(img_2)

        if(dets_1 is None or dets_2 is None):
            raise Exception("Face not found")

        shape = sp_68(img_1, dets_1)
        face_descriptor_1 = facerec.compute_face_descriptor(img_1, shape)
        if(len(face_descriptor_1)==0):
            shape = sp_5(img_1, dets)
            face_descriptor_1 = facerec.compute_face_descriptor(img_1, shape)

        shape = sp_68(img_2, dets_2)
        face_descriptor_2 = facerec.compute_face_descriptor(img_2, shape)
        if(len(face_descriptor_2)==0):
            shape = sp_5(img_2, dets)
            face_descriptor_2 = facerec.compute_face_descriptor(img_2, shape)
            
        # Measure the distance
        dst = distance.euclidean(face_descriptor_1, face_descriptor_2)
        res = dst < threshold

        return dst,res,"Operation successful"

    except Exception as e:
        return None,None,e.args

sp_5 = dlib.shape_predictor('model/shape_predictor_5_face_landmarks.dat')
sp_68 = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('model/dlib_face_recognition_resnet_model_v1.dat')
print("Load Models")