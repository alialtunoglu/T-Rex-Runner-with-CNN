import keyboard
import uuid
import time
from PIL import Image
from mss import mss

"""
http://www.trex-game.skipser.com/
"""

mon = {"top":403, "left":770, "width":250, "height":100}
sct = mss() 
#mss kütüphanesi bizim mon'daki kordinatlar doğrultusunda ekrandan
#roi kısmını (ilgilenilen kısmı) kesip frame haline dönüştüren kütüphanedir

i = 0

#Ekran kaydı yapıcak
def record_screen(record_id, key):
    global i
    #Buradaki key klavyemizdeki bastığımız tuş
    #i ise kaç kez bastığımız
    i += 1
    print("{}: {}".format(key, i))
    img = sct.grab(mon)
    #ekranı al mon pixelleri doğrultusunda img'e eşitle
    im = Image.frombytes("RGB", img.size, img.rgb)
    #RGB formatında okuyacağız
    im.save("./img/{}_{}_{}.png".format(key, record_id, i))
    
is_exit = False #fonksiyondan çıkmayı sağlıyacak

def exit():
    global is_exit
    is_exit = True
    
#escape tuşuna basınca fonksiyondan çıkacak
keyboard.add_hotkey("esc", exit)

record_id = uuid.uuid4()

while True:
    
    if is_exit: break

    try:
        if keyboard.is_pressed(keyboard.KEY_UP):
            record_screen(record_id, "up")
            time.sleep(0.1)
        elif keyboard.is_pressed(keyboard.KEY_DOWN):
            record_screen(record_id, "down")
            time.sleep(0.1)
        elif keyboard.is_pressed("right"):
            record_screen(record_id, "right")
            time.sleep(0.1)
    except RuntimeError: continue
            























