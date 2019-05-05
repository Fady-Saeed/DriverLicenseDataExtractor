from flask import Flask, request, Response, jsonify
import base64
import numpy as np
import cv2
import gc

from main import get_bounding_box, cut_image
from get_license_no import get_no_and_text
from get_id import get_id

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
		# print(base64Image)
		letters, digits = get_no_and_text(image)
		gc.collect()
		# END 	-- Call the Image Processing algorithm
		if len(letters) > 0 and len(digits) > 0:
			payload = {
				'letters': letters,
				'digits': digits
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
		else:
			return getErrorResponse()
		# except:
		# 	return getErrorResponse()

@app.route('/driver', methods = ['GET','POST'])
def GetDriverLicenseDetails():
	if request.method == "GET":
		return 'GET Request is not supported, You should use POST Request to uplaod the \"image\" of the Driver\'s License'
	elif request.method == "POST":
		# try: 
		image = data_uri_to_cv2_img(request.form["image"])
		
		# START -- Call the Image Processing algorithm
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		retval, image = cv2.imencode('.jpg', image)
		base64Image = base64.b64encode(image).decode()
		base64Image = 'data:image/jpg;base64,{}'.format(base64Image)
		nationalID = get_id(base64Image)
		# END 	-- Call the Image Processing algorithm
		
		payload = {
			'nationalID': nationalID
		}
		data = {
			'type': 'success',
			'message': 'Data retrieved successfully',
			'payload': payload,
		}
		response = jsonify(data)
		response.status_code = 200

		return response
		# except:
		# 	return getErrorResponse()

def data_uri_to_cv2_img(uri):
	nparr = np.fromstring(base64.b64decode(uri), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

def getErrorResponse():
	data = {
		'type': 'error',
		'message': 'An error occurred while retrieving the data'
	}
	response = jsonify(data)
	response.status_code = 500
	return response

if __name__ == '__main__':
    app.run()
