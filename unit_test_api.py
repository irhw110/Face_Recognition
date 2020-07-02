import unittest
import requests

class TestOperations(unittest.TestCase):
    def test_api(self):
        url = 'http://localhost:5000/api/v1/face_comparation/compare'

        # Case 1
        image_1 = open('test_file/img_1.png', 'rb')
        image_2 = open('test_file/img_2.png', 'rb')
        files_payload = {'img_1': image_1, 'img_2': image_2}
        
        resp = requests.post(url, files =files_payload)       
        assert resp.status_code == 200

        image_1.close()
        image_2.close()

        # Case 2
        image_1 = open('test_file/img_1.png', 'rb')
        image_2 = open('test_file/test.txt', 'rb')
        payload = { 'threshold':0.6 }
        files_payload = {'img_1': image_1, 'img_2': image_2}
        
        resp = requests.post(url, files =files_payload, data=payload)       
        assert resp.status_code == 422

        image_1.close()
        image_2.close()

        # Case 3
        image_1 = open('test_file/img_1.png', 'rb')
        image_2 = open('test_file/img_2.png', 'rb')
        payload = { 'threshold': 'abc' }
        files_payload = {'img_1': image_1, 'img_2': image_2}
        
        resp = requests.post(url, files =files_payload, data=payload)       
        assert resp.status_code == 422

        image_1.close()
        image_2.close()

        # Case 4
        image_1 = open('test_file/img_1.png', 'rb')
        image_2 = open('test_file/square.png', 'rb')
        payload = { 'threshold': 0.5 }
        files_payload = {'img_1': image_1, 'img_2': image_2}
        
        resp = requests.post(url, files =files_payload, data=payload)       
        assert resp.status_code == 500

        image_1.close()
        image_2.close()

if __name__ == '__main__':
    unittest.main()
    