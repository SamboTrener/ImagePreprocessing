import cv2
import keyboard
from tkinter import *
from tkinter import ttk
import os


test_img_path = 'D:/assets/bell_raw'

final_img_path = 'D:/assets/bell_ready'

def mouse_crop(event, x, y, flags, param):

    global x_start, y_start, x_end, y_end, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            resized_img = cv2.resize(roi, (60, 80), cv2.INTER_LINEAR)

            img_grey = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

            median_img = cv2.medianBlur(img_grey, 5)


            gX = cv2.Sobel(median_img, cv2.CV_32F, 1, 0, 3)
            gY = cv2.Sobel(median_img, cv2.CV_32F, 0, 1, 3)
            gX = cv2.convertScaleAbs(gX)
            gY = cv2.convertScaleAbs(gY)

            sobelxy = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)

            labelName, imageName = getLabelAndImageNames()


            cv2.imwrite(final_img_path + '/' + labelName.get() + "." + imageName.get() + ".png", sobelxy)

def getLabelAndImageNames():
    root = Tk()
    root.title("window")
    root.geometry("250x150")

    labelName = StringVar()
    imageName = StringVar()

    text = ttk.Label()
    entry = ttk.Entry(textvariable=labelName)
    entry.pack(anchor=NW, padx=6, pady=6)

    entry = ttk.Entry(textvariable=imageName)
    entry.pack(anchor=NW, padx=6, pady=6)

    Button(root, text="Quit", command=root.destroy).pack()

    root.mainloop()

    return labelName, imageName


for rawImage in os.listdir(test_img_path):
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    image = cv2.imread(test_img_path + '/' + rawImage)
    image = cv2.resize(image, (int(image.shape[1] * 0.9), int(image.shape[0] * 0.9)), cv2.INTER_LINEAR)
    oriImage = image.copy()


    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    while True:
        i = image.copy()
        if not cropping:
            cv2.imshow("image", image)
        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv2.imshow("image", i)
        cv2.waitKey(1)
        if keyboard.is_pressed('q'):
            print('You Pressed A Key!')
            cv2.waitKey(500)
            break
    cv2.destroyAllWindows()
