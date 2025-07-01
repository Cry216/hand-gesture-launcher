import cv2
import numpy as np
import time
import os

action_time = 0
ostanovka= 2


cap = cv2.VideoCapture(0)
cap.set(4, 300)
cap.set(3, 666)

while True:
    success, img = cap.read()
    cv2.imshow('result', img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) 

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    total_fingers = 0

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(img, [max_contour], -1, (0, 255, 0), 2)
    
        hull = cv2.convexHull(max_contour, returnPoints=False)
        if hull is not None and len(hull) > 3:
            defects = cv2.convexityDefects(max_contour, hull)
            if defects is not None:
                fingers = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(max_contour[s][0])
                    end = tuple(max_contour[e][0])
                    far = tuple(max_contour[f][0])
                    

                    a = np.linalg.norm(np.array(end) - np.array(start))
                    b = np.linalg.norm(np.array(far) - np.array(start))
                    c = np.linalg.norm(np.array(end) - np.array(far))


                    angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))

                    if angle <= np.pi / 2 and d > 15000 and  a > 50:
                        fingers += 1
                        cv2.circle(img, far, 8, (255, 0, 0), -1)

                total_fingers = fingers + 1
                cv2.putText(img, f"Пальчики: {total_fingers}", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                
            current_time = time.time()
            if current_time - action_time > ostanovka:

                if total_fingers == 1 and time.time() - action_time > 1:
                   print("Один палец — открываю доту")
                   action_time = current_time


                elif total_fingers == 2 and time.time() - action_time > 2:
                     print(" Два пальца — открываю дискорд")
                     action_time = current_time


                elif total_fingers == 3 and time.time() - action_time > 2:
                      print(" Четыре пальца — закрываю вкладку дискорда")
                      action_time = current_time


                elif total_fingers == 4 and time.time() - action_time > 2:
                      print(" Четыре пальца — закрываю вкладку дискорда")
                      action_time = current_time

                elif total_fingers == 5 and time.time() - action_time > 2:
                     print(" Пять пальцев — открываю ютуб")
                     action_time = current_time

            print("вижу пальцы ", total_fingers)
            if total_fingers == 2 and current_time - action_time > 2:
                print("Запускаю Discord через:", f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Discord\\Update.exe")

    cv2.imshow("Kamera", img)
    cv2.imshow("Macka", thresh)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()