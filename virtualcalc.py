import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from calculator import Calculator

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

xoffset = 700
yoffset = 100


detector = HandDetector(detectionCon = .8, maxHands = 1)
calc = Calculator((xoffset, yoffset), 360, 540)

while True:

    if calc.equation == 'q':
        break

    success, frame = cap.read()
    # flipping the image to that the hands are on the right side
    frame = cv.flip(frame, 1)

    # detecting the hand
    hands, img = detector.findHands(frame, flipType = False)

    calc.draw(frame)

    # check for hands
    if hands:
        lmList = hands[0]['lmList']
        # draws the distance between the thumb and the index finger
        length, _, img = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[4][0], lmList[4][1]), frame)
        x, y = int((lmList[8][0] + lmList[4][0]) / 2), int((lmList[8][1] + lmList[4][1]) / 2)
        calc.buttonClick(x, y, length)
        calc.incDelay()

    cv.imshow("Image", frame)

    if cv.waitKey(1) & 0xff == ord('q'):
        break