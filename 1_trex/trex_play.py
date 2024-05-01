from keras.models import model_from_json
import numpy as np
from PIL import Image
import keyboard
import time
from mss import mss


sct = mss()
width = 125
height = 50
# model yükle
model = model_from_json(open("model.json","r").read())
mon = {"top":401, "left":759, "width":250, "height":100}

model.load_weights("trex_weight.h5")

# down = 0, right = 1, up = 2
labels = ["Down", "Right", "Up"]

framerate_time = time.time()
counter = 0
i = 0
delay = 0.4
#Bir komut verdikten sonra diğer komutu verebilmek için 0.4 saniye beklemesini istiyoruz
key_down_pressed = False

is_exit = False #fonksiyondan çıkmayı sağlıyacak

def exit():
    global is_exit
    is_exit = True
    
#escape tuşuna basınca fonksiyondan çıkacak
keyboard.add_hotkey("esc", exit)

while True:
    
    if is_exit: break
    
    img = sct.grab(mon)
    #ekranı kayıt altına al mon pixelleri doğrultusunda img'e eşitle
    im = Image.frombytes("RGB", img.size, img.rgb)
    im2 = np.array(im.convert("L").resize((width, height)))
    im2 = im2 / 255
    
    X =np.array([im2])
    X = X.reshape(X.shape[0], width, height, 1)
    r = model.predict(X) 
    #Modelimizi kullanarak bir predict işlemi gerçekleştir
    
    #toplamı 1 olan 3 tane sayıdan oluşacak
    result = np.argmax(r)
    
    
    if result == 0: # down = 0
        
        keyboard.press(keyboard.KEY_DOWN)
        key_down_pressed = True
    elif result == 2:    # up = 2
        
        
    #Bir önceki frame'de aşağıya bastıysak bırakmamız gerekiyor
        if key_down_pressed:
            keyboard.release(keyboard.KEY_DOWN)
        time.sleep(delay)
        keyboard.press(keyboard.KEY_UP)
        
        
        #oyun 1500. frame'e kadar oyun normal bir hızda akıyor sonra değişiyor
        if i < 1500:
            time.sleep(0.3)
            #havada 30ms vakit geçiriyor
        elif 1500 < i and i < 5000:
            time.sleep(0.2)
        else:
            time.sleep(0.17)
            
            #yukarıya zıpladım belli bir süre bekledim sonra
            #initial pozisyonuma geri dönmeliyim
        keyboard.press(keyboard.KEY_DOWN)
        keyboard.release(keyboard.KEY_DOWN)
    
    counter += 1
    
    if (time.time() - framerate_time) > 1:
        
        counter = 0
        framerate_time = time.time()
        if i <= 1500:
            delay -= 0.003
        else:
            delay -= 0.005
        if delay < 0:
            
            delay = 0
        print("---------------------")
        print("Down: {} \nRight:{} \nUp: {} \n".format(r[0][0],r[0][1],r[0][2]))
        i += 1
        
        



























