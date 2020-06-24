import cv2
import dlib
import numpy as np # upgrade to 1.8.0
import time

from scipy.spatial import distance

'''
Get the largest detected face from a list of detected faces
    input : list of rectangles
    return: rectangle [(left,top),(right,bottom)]
'''
def largest_face(detected_faces):
    max = 0
    for i,face_rect in enumerate(detected_faces):
        if((face_rect.width()+face_rect.height()) > (detected_faces[max].width()+detected_faces[max].height())):
            max = i
    return detected_faces[max]

'''
Get list of detected faces from an image
    input : image (png,jpg,jfif,jpeg)
    return: list of rectangle
'''
def crop_face(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_detector = dlib.get_frontal_face_detector()
    detected_faces = face_detector(image, 1)
    return(largest_face(detected_faces))

def face_compare_process(img_file_1, img_file_2, threshold):
    start = time.time()
    # Load image 1 and image 2 file
    img_1 = cv2.imdecode(np.frombuffer(img_file_1, np.uint8), cv2.COLOR_BGR2RGB)
    img_2 = cv2.imdecode(np.frombuffer(img_file_2, np.uint8), cv2.COLOR_BGR2RGB)
    
    # Crop face from both image
    dets_1 = crop_face(img_1)
    dets_2 = crop_face(img_2)

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
    res = 0 if(dst<threshold) else 1
    duration = time.time() - start

    return dst,res,duration

start_load = time.time()
sp_5 = dlib.shape_predictor('model/shape_predictor_5_face_landmarks.dat')
sp_68 = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('model/dlib_face_recognition_resnet_model_v1.dat')
print("Load model took "+str(time.time() - start_load))
