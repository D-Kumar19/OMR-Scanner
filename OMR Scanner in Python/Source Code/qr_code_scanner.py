import cv2 as cv


# this function will read a qr code and print what is inside
def read_qr_code(img):
    detector = cv.QRCodeDetector()
    value, points, straight_qrcode = detector.detectAndDecode(img)

    # if points is not None:
    #     print(value)

    return value
