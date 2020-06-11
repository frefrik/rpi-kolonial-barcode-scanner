import imutils
import time
import json
from threading import Thread
from imutils.video import VideoStream
from pyzbar.pyzbar import ZBarSymbol
from pyzbar import pyzbar
from cv2 import cv2
from kolonial import Kolonial

USERNAME = 'your@email'
PASSWORD = 'yourPassword'
USER_AGENT = 'yourUserAgent'
TOKEN = 'yourToken'

api = Kolonial(USERNAME, PASSWORD, USER_AGENT, TOKEN)

def set_reset():
	# Prevent multiple rapid scans of the product
	while True:
		if len(detected):
			time.sleep(2)
			detected.clear()
		
timer = Thread(target=set_reset)
timer.daemon = True
detected = set()
DEBUG = False # Prints detected barcodes if True

print('Starting video stream...')
vs = VideoStream(usePiCamera=True).start()
time.sleep(2)
print('Video stream started')

timer.start()

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=480)
	barcodes = pyzbar.decode(frame, symbols=[ZBarSymbol.EAN13])

	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 0, 255), 2)

		if DEBUG:
			print('Barcode detected: {}'.format(barcodeData))

		if barcodeData not in detected:
			# Search Kolonial for barcode
			search = api.search(barcodeData)
			print('\n----------------------------------------')

			if len(search['products']) != 0:
				product_id = search['products'][0]['id']
				product_name = search['products'][0]['full_name']
				print('Found product: ' + product_name)
				
				# Cart item
				item = {"items": [{'product_id' : product_id, 'quantity' : '1'}]}

				# Add item to cart
				post_cart = api.modify_cart(json.dumps(item))
				print('DING! Product added to cart :D')
				print('----------------------------------------\n')
			else:
				print('Product not found @ Kolonial.no')
				print('----------------------------------------\n')
			
			detected.add(barcodeData)

    # Show the video frame
	cv2.imshow('Barcode Scanner', frame)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()
