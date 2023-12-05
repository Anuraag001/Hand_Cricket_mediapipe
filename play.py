import cv2
import time
import os
import mediapipe as mp
import random

score=[0,0]

def bat_bowl(frame,choice):
     cv2.putText(frame,"You won the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
     cv2.putText(frame,"Choose 1-3 for bat 4-5 for bowl",(300,300),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
     if check>40:
        return choice
     else:
         return -1

def compu_bb(frame):
    cv2.putText(frame,"You lost the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    cv2.putText(frame,"Computer choosing...",(300,300),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    return random.randint(0,1)
     
def choice(frame,choice):
     cv2.putText(frame,"Choose 1-3 for even 4-5 for odd",(300,300),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
     if check>40:
        return choice
     else:
         return -1
     
def toss(frame,my_val,compu_val,check,my_choice):
    cv2.putText(frame,"TOSS",(1100,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    cv2.putText(frame,f"Your choice={my_choice}",(900,100),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    if check>30:
        sum=compu_val+my_val
        cv2.putText(frame,f"{my_val}you+{compu_val}comp={sum}",(900,400),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
    
    if check>40:

        if my_choice=="even":
            if sum%2==0:
                cv2.putText(frame,"You won the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
                return 1
            else:
                cv2.putText(frame,"You lost the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
                return 0
        
        if my_choice=="odd":
            if sum%2!=0:
                cv2.putText(frame,"You won the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
                return 1
            else:
                cv2.putText(frame,"You lost the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
                return 0
    
def innings(frame,bat,comp_val,my_val,change=0,inning=1):
    text="st" if inning==1 else "nd"
    cv2.putText(frame,f"{inning}{text} innings",(900,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

    if bat==1:
        cv2.putText(frame,f"(bowl)You:{score[0]}",(900,400),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        cv2.putText(frame,f"(bat)CPU:{score[1]}",(900,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
            
    else:
        cv2.putText(frame,f"(bat)You:{score[0]}",(900,400),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        cv2.putText(frame,f"(bowl)CPU:{score[1]}",(900,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

    if change==1:
        score[bat]=score[bat]+(my_val if bat==0 else comp_val)


if __name__ == "__main__":
    #w, h = 640*2, 480*2
    w,h=1920,1080
    file=open("review.txt","w")
    file.write(f"{10*'*'}Hand Cricket Game{10*'*'}\n")
    file.write('Toss\n')
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
    check=0
    prev=0
    comp_val=0
    my_choice=""
    bat=-1
    # 0 is you 1 is cpu

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
        else:
            upcount=0
        
        if prev==upcount:
            check+=1
        if prev!=upcount:
            prev=upcount
            check=0
        
        if upcount==0:
            check=0

        
        if check//10==3:
            cv2.putText(frame,f'check registered',(450,700),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
            comp_val=random.randint(1,5)

        frame[0:200, 0:200] = overlayList[comp_val]

        if phase==0:
            final=choice(frame,upcount)
            if final in (1,2,3):
                my_choice="even"
                phase=1
                check=0
                file.write(f"Your choice={my_choice}\n")
            elif final in (4,5):
                my_choice="odd"
                phase=1
                check=0
                file.write(f"Your choice={my_choice}\n")
            final=-1
        
        if phase==1:
            final=toss(frame,upcount,comp_val,check,my_choice)
            if final==1:
                phase=2
                check=0
                file.write(f"Value is You={upcount} + cpu={comp_val} = {upcount+comp_val}\n\n")
                file.write("You won the toss\n")
                cv2.putText(frame,"You won the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    
            elif final==0:
                phase=3
                check=0
                file.write(f"Value is You={upcount} + cpu={comp_val} = {upcount+comp_val}\n")
                file.write("You lost the toss\n")
                cv2.putText(frame,"You lost the toss",(900,300),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)

            final=-1
        
        if phase==2:
            final=bat_bowl(frame,upcount)
            if final in (1,2,3):
                my_choice="bat"
                bat=0
                phase=4
                check=0
                file.write(f"Your choice={my_choice}\n\n")
                file.write(f"You{' '*10}CPU\n")
            elif final in (4,5):
                my_choice="bowl"
                bat=1
                phase=4
                check=0
                file.write(f"Your choice={my_choice}\n\n")
                file.write(f"You{' '*10}CPU\n")
            final=-1

        if phase==3:
            final=compu_bb(frame)
            if final==1:
                my_choice="bowl"
                bat=1
                phase=4
                check=0
                file.write(f"CPU choice=bat\n\n")
                file.write(f"You{' '*10}CPU\n")
            elif final==0:
                my_choice="bat"
                bat=0
                phase=4
                check=0
                file.write(f"CPU choice=bowl\n\n")
                file.write(f"You{' '*10}CPU\n")
            final=-1
        
        if phase==4:
            if check<30:
                innings(frame,bat,comp_val,upcount)

            if comp_val==upcount and check>30:
                check=0
                bat=(1 if bat==0 else 0)
                innings(frame,bat,comp_val,upcount)
                file.write(f"{upcount}{' '*10}{comp_val}\n\n\n\n")
                phase=5
            
            elif check>30:
                innings(frame,bat,comp_val,upcount,1)
                file.write(f"{upcount}{' '*10}{comp_val}\n")
                check=0
        
        if phase==5:
            if check<30:
                innings(frame,bat,comp_val,upcount,inning=2)

            if comp_val==upcount and check>30:
                check=0
                innings(frame,bat,comp_val,upcount,0,2)
                #bat=(0 if bat==1 else 1)
                #bowl=(1 if bat==0 else 0)
                file.write(f"{upcount}{' '*10}{comp_val}\n")
                phase=6
                
            elif check>30:
                innings(frame,bat,comp_val,upcount,1,2)
                file.write(f"{upcount}{' '*10}{comp_val}\n")
                bowl=(1 if bat==0 else 0)
                if(score[bat]>score[bowl]):
                    phase=6
                check=0
            
        if phase==6:
            if score[0]>score[1]:
                print("You win")
                file.write("You win\n")
            else:
                print("You lose")
                file.write("You lose\n")
            print(f"Your score={score[0]} CPU score={score[1]}")
            file.write(f"Your score={score[0]} CPU score={score[1]}\n")
            break


        cv2.putText(frame,f'{check//10}',(450,650),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        cv2.putText(frame,"Opponent",(5,225),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
        etime = time.perf_counter()
        fps = 1 / (etime - stime)
        stime = etime
        cv2.putText(frame, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
