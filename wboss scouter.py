import cv2
import numpy as np
import pyautogui
import pytesseract
from discord_webhook import DiscordWebhook
from PIL import Image
import time
import re
import os
from dotenv import load_dotenv
load_dotenv()
webhookURL = os.getenv("URL")
tesseeract = os.getenv("tesseractPath")
pytesseract.pytesseract.tesseract_cmd = tesseeract
bosses = ["kazzak","azuregos","ysondere","emeriss","lethon","taerar",]
def checkIfBoss(text,i):
    if text.find(i)>=0:
        webhookmsg = "@everyone " + i + " spawned"
        webhook = DiscordWebhook(url=webhookURL, content=webhookmsg)
        response = webhook.execute()
        time.sleep(300)
        print(i)
def check_for_text():
    x, y, width, height = 0, 0, 220, 60
    im = pyautogui.screenshot(region=(x, y, width, height))
    im = im.convert('L')
    imnumpy = np.array(im)
    img_filtered = cv2.bilateralFilter(imnumpy, 9, 75, 75) 
    _, thresh = cv2.threshold(img_filtered, 127, 255, cv2.THRESH_BINARY)
    #Image.fromarray(thresh).show()
    text = pytesseract.image_to_string(Image.fromarray(thresh))
    if text.strip():
        regex = re.compile('[^a-zA-Z]')
        text = regex.sub('',text)
        text = text.lower()
        print(text)
        [checkIfBoss(text,i) for i in bosses] 
while(True):
    check_for_text()
    time.sleep(3)