import glob
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

imgs = glob.glob("./img_nihai/*.png")
#ismi ne olursa olsun tüm png dosyalarını al ve imgs'ye aktar

width = 125
height = 50
#resim boyutumuzu yeniden boyutlandırmak için

X = []
Y = []

for img in imgs:
    
    filename = os.path.basename(img)
    #Dosya adını alıyoruz 
    label = filename.split("_")[0]
    #alt çizdiye göre ayır ilk kısmı al
    im = np.array(Image.open(img).convert("L").resize((width, height)))
    #resmimizi yeniden boyutlandırıyoruz
    im = im / 255
    #resim 0 ile 255 arasında değerler alıyordu biz bunları normalize ediyoruz
    X.append(im)
    #x'e resimlerimiz ekleniyor y'ye etiketlerimiz
    Y.append(label)
    
#train test split metodu içerisine array kabul eden bir metod
X = np.array(X)
#x.shape[0]-> Kaç tane resim olduğunu gösteriyor
X = X.reshape(X.shape[0], width, height, 1) #channel değeri 1'dir rgb değil



#Grafiksel olarak gösterme down ne kadar kullanılmış 
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(Y)

sns.countplot(x=y_encoded)


def onehot_labels(values):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    #önce öğreniyor sonra dönüştürüyor
    onehot_encoder = OneHotEncoder(sparse = False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded),1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded

Y = onehot_labels(Y)
train_X, test_X, train_y, test_y = train_test_split(X, Y , test_size = 0.33, random_state = 2)    

# cnn model
model = Sequential()   
#Evrişim katmanı ekliyoruz
model.add(Conv2D(32, kernel_size = (3,3), activation = "relu", input_shape = (width, height, 1)))
#tekrardan bir girdi eklememize gerek yok ilk katmanın çıktısı diğer katmanın girdisi olacaktır
model.add(Conv2D(64, kernel_size = (3,3), activation = "relu"))
# Piksel ekleme
model.add(MaxPooling2D(pool_size = (2,2)))
#Seyreltme
model.add(Dropout(0.25))
#Düzleştirme
model.add(Flatten())
#Gizli katman -> 128 tane nöron yaptık
model.add(Dense(128, activation = "relu"))
#seyreltme
model.add(Dropout(0.4))
#Çıktı katmanı
model.add(Dense(3, activation = "softmax"))

#Eğer hazır bir modelimiz varsa onu yüklemek için böyle yapıyoruz
# if os.path.exists("./trex_weight.h5"):
#     model.load_weights("trex_weight.h5")
#     print("Weights yuklendi")    

#loss -> En son nihai olarak hatalarımızı hesaplamamıza yarayan fonk
#loss çok azsa bizim modelimiz iyi eğitilmiş olacak
#optimizer -> parametreleri optimize etmeye yarayan algoritma
#metrics-> modelimizin sonuçlarını yorumlamamız için gerekli olan yapı
model.compile(loss = "categorical_crossentropy", optimizer = "Adam", metrics = ["accuracy"])

#Eğitme işlemi resimlerimiz toplamda 35 kere (eğitiliyor iterasyon)
#batch_size Resimlerin kaç grup halinde iterasyona sokulacağını belirtiyor
#64lü gruplar şeklinde 3 grupta 169 resim ifade edilir son grup 41 resim
model.fit(train_X, train_y, epochs = 35, batch_size = 64)

score_train = model.evaluate(train_X, train_y)
print("Eğitim doğruluğu: %",score_train[1]*100)    
#score_train -> 1.indeksi kaybı 2. indeksi accuracy'yi başarımı verir  
#aynı şekilde score_test
score_test = model.evaluate(test_X, test_y)
print("Test doğruluğu: %",score_test[1]*100)      
    
 
open("model_new.json","w").write(model.to_json())
model.save_weights("trex_weight_new.h5")   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    