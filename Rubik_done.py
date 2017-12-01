import cv2
import numpy as np


def createColorsRange():
    colors=dict()
    reader=open("colors","r")
    lines=reader.readlines()

    for line in lines:
        color=line.split(",")
        string_color=color[0]
        low=np.array([int(color[1]),int(color[3]),int(color[5])],np.uint8)
        high=np.array([int(color[2]),int(color[4]),int(color[6])],np.uint8)

        colors[string_color]=[low,high]
    return colors

def clean_mask(mask):

    # Opening to remove salt and pepper noise

    kernel = np.ones((1, 1), np.uint8)
    mask_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    ret, th1 = cv2.threshold(mask_opening, 127, 255, cv2.THRESH_BINARY)
    return th1

def detect(frame,frame_hsv,color):
    b, g, r = convertHSV2BGR(color[1])
    mask = cv2.inRange(frame_hsv, color[0], color[1])
    mask = clean_mask(mask)
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    for count in contours:
        x, y, w, h = cv2.boundingRect(count)
        if (w * h > 3000):
            cv2.rectangle(frame, (x+100, y+100), (x + w+100, y + h+100), (int(b), int(g), int(r)), 2)

def convertHSV2BGR(color):
    ret_color = np.uint8([[color]])
    bgr_color = cv2.cvtColor(ret_color, cv2.COLOR_HSV2BGR)
    return bgr_color[0][0][0],bgr_color[0][0][1],bgr_color[0][0][2]

def main():

    # Video capture
    cap = cv2.VideoCapture(0)
    colors=createColorsRange()

    while(True):
        ret, frame = cap.read()
        cv2.rectangle(frame, (400, 400), (100, 100), (0, 255, 0), 0)
        crop_frame = frame[100:400, 100:400]
        # Transform the image to HSV color space
        frame_hsv = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2HSV)

        for color in colors.values():
            detect(frame, frame_hsv, color)


        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



