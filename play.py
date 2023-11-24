import cv2
import time
import os
import mediapipe as mp

def toss(frame):
    cv2.putText(frame,"TOSS",(300,300),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.putText(frame,"1-3 for even 4-5 for odd",(300,300),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


if __name__ == "__main__":
    w, h = 640*2, 480*2
    cap = cv2.VideoCapture(0)
    cap.set(3, w)
    cap.set(4, h)

    mpHands = mp.solutions.hands
    hands=mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    folderPath = 'finger'
    myList = os.listdir(folderPath)
    print(myList)

    finger_coordinates=[(8,6),(12,10),(16,14),(20,18)]
    thumb_coordinates=(4,2)

    overlayList = []
    for imgPath in myList:
        image = cv2.imread(f'{folderPath}/{imgPath}')
        overlayList.append(image)

        
    upcount=0
    stime = 0
    phase=0 # 0 toss 1 1st innings 2 2nd innnings
    check=1
    prev=0

    while True:
        isTrue, frame = cap.read()
        img_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(img_rgb)
        hand_landmarks=results.multi_hand_landmarks
        #print(hand_landmarks)

        if hand_landmarks:
            hand_points=[]
            for handLms in hand_landmarks:
                mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS)

            for idx,lm in enumerate(handLms.landmark):
                #print(idx,lm)            # prints the coordinates of the landmarks
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h) #converts into pixels
                hand_points.append((cx,cy))
        
            for point in hand_points:
                cv2.circle(frame,point,10,(0,0,255),cv2.FILLED)

            upcount=0
            for coordinate in finger_coordinates:
                if hand_points[coordinate[0]][1] < hand_points[coordinate[1]][1]:
                    upcount+=1
            if hand_points[thumb_coordinates[0]][0] > hand_points[thumb_coordinates[1]][0]:
                upcount+=1

            cv2.putText(frame,f'Fingers Up: {upcount}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        
        if prev==upcount:
            check+=1
        else:
            prev=upcount
            check=1
        
        if upcount==0:
            check=0

        if phase==0:
            toss(frame)
        
        if check//10==3:
            cv2.putText(frame,f'check registered',(100,400),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.putText(frame,f'{check//10}',(150,250),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        frame[0:200, 0:200] = overlayList[upcount]
        etime = time.perf_counter()
        fps = 1 / (etime - stime)
        stime = etime
        cv2.putText(frame, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
