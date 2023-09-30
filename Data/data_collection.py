import mediapipe as mp
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

name = input("Enter the name of the data : ")

hol=mp.solutions.holistic
hands=mp.solutions.hands
holis=hol.Holistic()
draw=mp.solutions.drawing_utils

X=[]
data_size=0
while True:
    list=[]
    _,frame=cap.read()

    frame = cv2.flip(frame,1)

    res=holis.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

    if res.face_landmarks:
        for i in res.face_landmarks.landmark:
            list.append(i.x-res.face_landmarks.landmark[1].x)
            list.append(i.y - res.face_landmarks.landmark[1].y)
        if res.left_hand_landmarks:
            for i in res.left_hand_landmarks.landmark:
                list.append(i.x - res.left_hand_landmarks.landmark[8].x)
                list.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                list.append(0.0)

        if res.right_hand_landmarks:
            for i in res.right_hand_landmarks.landmark:
                list.append(i.x - res.right_hand_landmarks.landmark[8].x)
                list.append(i.y - res.right_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                list.append(0.0)

        X.append(list)
        data_size=data_size+1
    draw.draw_landmarks(frame,res.face_landmarks,hol.FACE_CONNECTIONS)
    draw.draw_landmarks(frame, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
    draw.draw_landmarks(frame, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

    cv2.putText(frame, str(data_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

    cv2.imshow("window",frame)
    if cv2.waitKey(1)==27 or data_size>99:
        cv2.destroyAllWindow()
        cap.release()
        break
np.save(f"{name}.npy", np.array(X))
print(np.array(X).shape)