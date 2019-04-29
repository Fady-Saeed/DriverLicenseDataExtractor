import os
from flask import Flask, request, Response, jsonify
import io
import base64
from PIL import Image
import time

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def GetLicenseDetails():
	if request.method == "GET":
		return 'GET Request is not supported, You should use POST Request to uplaod the \"image\" of the Driver\'s License'
	elif request.method == "POST":
		try: 
			image = stringToImage(request.form["image"])
			
			# START -- Call the Image Processing algorithm
			time.sleep(3)
			# END 	-- Call the Image Processing algorithm
			
			payload = {
				'firstLetter': 'ن',
				'secondLetter': 'ط',
				'thirdLetter': 'ب',
				'digits': 648
			}
			data = {
				'type': 'success',
				'message': 'Data retrieved successfully',
				'payload': payload,
			}
			response = jsonify(data)
			response.status_code = 200

			return response
		except:
			data = {
				'type': 'error',
				'message': 'An error occurred while retrieving the data'
			}
			response = jsonify(data)
			response.status_code = 200
			return response


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

if __name__ == '__main__':
    app.run()
