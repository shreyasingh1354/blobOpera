import cv2
import numpy as np
import mediapipe as mp
from time import sleep
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

cap = cv2.VideoCapture(0)

cap.set(3, 1920)  
cap.set(4, 1080)  

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)

driver.get(r"https://artsandculture.google.com/experiment/blob-opera/AAHWrq360NcGbw?hl=en")
pg.press('f11') 
sleep(5)
driver.find_element(by=By.CLASS_NAME, value="snByac").click()
sleep(5)
height = driver.execute_script("return document.body.scrollHeight")
pg.moveTo(x=976, y=797)
sleep(5)
pg.dragTo(x=976, y=223, duration=3)
pg.moveTo(x=1805, y=1033)
pg.click()
sleep(2)

def returngrid(x):
    if(x>=0 and x<=775):
        return 1
    elif(x>775 and x<=916):
        return 2
    elif(x>916 and x<=1158):
        return 3
    elif(x>1158 and x<=1920):
        return 4

while True:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
            hand_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])
            screen_width, screen_height = pg.size()
            cursor_x = int(hand_x * screen_width / frame.shape[1])
            cursor_y = int(hand_y * screen_height / frame.shape[0])
            
            
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            distance = np.sqrt((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2)
            grid = returngrid(cursor_x)
            if(grid==1):
                cursor_x=661
            elif(grid==2):
                cursor_x=881
            elif(grid==3):
                cursor_x=1083
            elif(grid==4):
                cursor_x=1275
            pg.dragTo(cursor_x, cursor_y,duration=1.5)
    
    cv2.imshow('Hand Motion', frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
driver.quit()
# GRID 1: 0 775
# GRID 2: 775 916
# GRID 3: 916 1158
# GRID 4: 1158 1920
