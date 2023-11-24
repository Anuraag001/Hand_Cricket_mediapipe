import cv2
import time
import os
import mediapipe as mp

w, h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

folderPath = 'finger'
myList = os.listdir(folderPath)
print(myList)


overlayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

stime = 0
while True:
    isTrue, frame = cap.read()
    

    frame[0:200, 0:200] = overlayList[5]
    etime = time.perf_counter()
    fps = 1 / (etime - stime)
    stime = etime
    cv2.putText(frame, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
