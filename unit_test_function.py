import unittest
import dlib
from functions.face_compare import *

class TestOperations(unittest.TestCase):
    def test_validate_threshold(self):
        # Case 1
        threshold, valid = validate_threshold("0.6")
        assert threshold is not None and valid==True

        # Case 2
        threshold, valid = validate_threshold("-0.6")
        assert threshold is not None and valid==False

        # Case 3
        threshold, valid = validate_threshold("abc")
        assert threshold is None and valid==False

    def test_crop_face(self):
        # Case 1
        file_1 = open('test_file/img_1.png', 'rb')
        img_1 = cv2.imdecode(np.frombuffer(file_1.read(), np.uint8), cv2.COLOR_BGR2RGB)
        file_1.close()

        result = crop_face(img_1)

        assert isinstance(result, dlib.rectangle)

        # Case 2
        file_1 = open('test_file/square.png', 'rb')
        img_1 = cv2.imdecode(np.frombuffer(file_1.read(), np.uint8), cv2.COLOR_BGR2RGB)
        file_1.close()

        result = crop_face(img_1)

        assert result is None

    def test_face_compare_process(self):
        # Case 1
        file_1 = open('test_file/img_1.png', 'rb')
        file_2 = open('test_file/img_2.png', 'rb')
        threshold = 0.6
        dst,res,message = face_compare_process(file_1.read(),file_2.read(),threshold)

        file_1.close()
        file_2.close()

        assert isinstance(dst, float)
        assert isinstance(res, bool)

        # Case 2
        file_1 = open('test_file/img_1.png', 'rb')
        file_2 = open('test_file/square.png', 'rb')
        threshold = 0.6
        dst,res,message = face_compare_process(file_1.read(),file_2.read(),threshold)

        file_1.close()
        file_2.close()

        assert dst is None
        assert res is None

if __name__ == '__main__':
    unittest.main()