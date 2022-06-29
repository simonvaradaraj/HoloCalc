import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from math import floor

# The calculator has to have 18 separate buttons, which may have variability in size
class Button:

    # setting the colors of the buttons in the paraameters didnt work well
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.color = (205, 205, 205)

    # draws a rectangle at the position with a small border and an attempt at centered text
    def draw(self, img):
        # solid gray rectangle
        cv.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), self.color, cv.FILLED)
        # gray border
        cv.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        # Text
        cv.putText(img, self.value, (self.pos[0] + int(self.width/2.3), self.pos[1] + int(self.height /1.9)), cv.FONT_HERSHEY_PLAIN, 1.5, (50, 50, 50), 2)
    
    # checks to see if the button has been clicked
    def checkClick(self, x, y, dist):
        # if the hover is above the bounds of the box
        if (self.pos[0] < x and x < self.pos[0] + self.height) and (
            self.pos[1] < y and y < self.pos[1] + self.height):

            # if the distance between the thumb and the index finger is below the threshold
            if(dist <= 39): 
                # print("CLICKED") - Used for debugging
                self.color = (125, 255, 125)
                return self.value
            else: 
                self.color = (255, 255, 255)
                return ""
            

        else:
            self.color = (205, 205, 205)

# 
class Calculator:

    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height

        self.buttonlist = []
        self.buttonValues = [
            ['1', '2', '3', '*'],
            ['4', '5', '6', '-'],
            ['7', '8', '9', '+'],
            ['0', '/', '.', '='],
            ['EX', 'Delete', 'AC']
        ]

        self.cols = len(self.buttonValues[0])
        self.rows = len(self.buttonValues) + 1

        self.equation = ""
        self.delay = 0

        for x in range(19):
            xpos = (x%self.cols + 1) * int(self.width / self.cols) + self.pos[0]
            ypos = (floor(x/self.cols) + 1) * int(self.height / self.rows) + self.pos[1]

            if x == 17:
                self.backspace = Button((xpos, ypos), (int(self.width / self.cols) * 2), int(self.height / self.rows), "Delete")
            if x == 18:
                xpos += int(self.width / self.cols)
                self.buttonlist.append(Button((xpos, ypos), int(self.width / self.cols), int(self.height / self.rows), self.buttonValues[floor(x/self.cols)][x%self.cols]))
            else:
                self.buttonlist.append(Button((xpos, ypos), int(self.width / self.cols), int(self.height / self.rows), self.buttonValues[floor(x/self.cols)][x%self.cols]))
        

    def buttonClick(self, x, y, length):
        for button in self.buttonlist:
            retVal = button.checkClick(x, y, length)
            if retVal and self.delay == 0:
                self.delay += 1
                if retVal == '=': 
                    self.equation = str(eval(self.equation))
                    return
                if retVal == 'AC': 
                    self.equation = ""
                    return
                if retVal == 'Delete': 
                    self.equation = self.equation[:-1]
                    return
                if retVal == 'EX':
                    self.equation = 'q'
                    return
                    
                self.equation += retVal
    
    def incDelay(self):
        # print(self.delay)
        if self.delay != 0: self.delay += 1
        if self.delay > 10: self.delay = 0

    def draw(self, img):
        for button in self.buttonlist: button.draw(img)
        self.backspace.draw(img)
        # self.quitbutton.draw(img)
        # drawing answerbar
        cv.rectangle(img, (self.pos[0] + int(self.width / self.cols), self.pos[1] - 10), (self.pos[0] + int(self.width * (self.cols + 1)/self.cols), self.pos[1] + int(self.height / self.rows)), (225, 225, 225), cv.FILLED)

        cv.rectangle(img, (self.pos[0] + int(self.width / self.cols), self.pos[1] - 10), (self.pos[0] + int(self.width *  (self.cols + 1)/self.cols), self.pos[1] + int(self.height / self.rows)), (50, 50, 50), 3)

        cv.putText(img, self.equation, (self.pos[0] + int(self.width / self.cols) + 20, self.pos[1] + int(self.height / 10) + 15), cv.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)



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