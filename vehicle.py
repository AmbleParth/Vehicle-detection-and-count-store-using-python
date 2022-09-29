import cv2
from cv2 import dilate
import numpy as np
import sqlite3

conn = sqlite3.connect('count.db')

c = conn.cursor
'''conn.execute("""CREATE TABLE count (
        count integer
)""")'''
# conn.execute("INSERT INTO count VALUES(('?',count))")

print(conn.execute("SELECT * FROM count"))



conn.commit()

conn.close()
# Start Webcam or import video
vid = cv2.VideoCapture('1.mp4')

# Setting the position of counter line
count_line_position = 550

# Minimum height and width of rectangle
min_width_rect = 80
min_height_rect = 80

# Defining a function for creating a center point on all vehicles
def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Creating a list to append count of vehicles
detect = []
counter = 0

# Allowable error between pixels
offset = 6

# Initialize Subtractor algorithm
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

sum = 0
# To read and show the video
while True:
    ret, frame1 = vid.read()

    # Converting the video into grey scale
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Creates a point on a vehicle
    blur = cv2.GaussianBlur(grey, (3,3), 5)

    # Applying this point on each frame
    img_sub = algo.apply(blur)
    dil = cv2.dilate(img_sub, np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    # To create shapes for multiple vehicles
    dilat = cv2.morphologyEx(dil, cv2.MORPH_CLOSE, kernel)
    dilat = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)

    # To count number of vehicles
    counter_shape, h = cv2.findContours(dilat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
    # Creating the counter line
    cv2.line(frame1, (25, count_line_position), (1250, count_line_position), (255, 127, 0), 3)

    # Creating rectangles on multiple vehicles
    for (i, c) in enumerate(counter_shape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_rect) and (h >= min_height_rect)
        if not validate_counter:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Vehicle", (x, y-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

        # To display the count on screen
        for (x, y) in detect:
            if y < (count_line_position + offset) and y > (count_line_position - offset):
                counter = counter+1
                cv2.line(frame1, (25, count_line_position), (1250, count_line_position), (0, 127, 255), 3)
                detect.remove((x, y))
                print("Vehicle Counter : "+str(counter))
        sum = counter
    
    cv2.putText(frame1, "Vehicle Count : "+str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    


    #cv2.imshow('Detecter', dilat)
    cv2.imshow('Original Video', frame1)

    # To close the video press enter
    if cv2.waitKey(1) == 13:
        break

    
print("Total Count : ",str(sum))
with open("count.txt","a") as o:
    o.write('\n***************PROGRAM STARTS***************')
    o.write('\nTotal number of cars counted:')
    o.write(str(sum))
    o.write('\n****************PROGRAM ENDS****************\n\n')
    o.truncate()
    o.close()

cv2.destroyAllWindows()
vid.release()