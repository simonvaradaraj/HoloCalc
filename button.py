import cv2 as cv

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

