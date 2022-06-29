import cv2 as cv
from math import floor
from button import Button

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

