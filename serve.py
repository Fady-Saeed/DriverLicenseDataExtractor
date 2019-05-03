from flask import Flask, request, Response, jsonify
import base64
import numpy as np
import cv2
import gc

from main import get_bounding_box, cut_image
from get_license_no import get_no_and_text

app = Flask(__name__)

@app.route('/car', methods = ['GET','POST'])
def GetCarLicenseDetails():
	if request.method == "GET":
		return 'GET Request is not supported, You should use POST Request to uplaod the \"image\" of the Car\'s License'
	elif request.method == "POST":
		# try: 
		image = data_uri_to_cv2_img(request.form["image"])
		
		# START -- Call the Image Processing algorithm
		gc.collect()
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		image = get_bounding_box( cut_image(cv2.imread('images/match_bottom_left.jpg', 0) , cv2.imread('images/match.jpg', 0) , image ) )
		gc.collect()
		image = cv2.pyrUp(image)
		gc.collect()
		retval, image = cv2.imencode('.jpg', image)
		base64Image = base64.b64encode(image).decode()
		base64Image = 'data:image/jpg;base64,{}'.format(base64Image)
		# print(base64Image)
		text, num = get_no_and_text(base64Image)
		gc.collect()
		# END 	-- Call the Image Processing algorithm
		
		payload = {
			'firstLetter': text[0],
			'secondLetter': text[1],
			'thirdLetter': text[2],
			'digits': num[2] + "" + num[1] + "" + num[0]
		}
		data = {
			'type': 'success',
			'message': 'Data retrieved successfully',
			'payload': payload,
		}
		response = jsonify(data)
		response.status_code = 200
		
		gc.collect()

		return response
		# except:
		# 	data = {
		# 		'type': 'error',
		# 		'message': 'An error occurred while retrieving the data'
		# 	}
		# 	response = jsonify(data)
		# 	response.status_code = 200
		
		# 	gc.collect()

		# 	return response


def data_uri_to_cv2_img(uri):
	nparr = np.fromstring(base64.b64decode(uri), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

if __name__ == '__main__':
    app.run()
