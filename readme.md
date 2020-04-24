#### Giriş
------------
Arabanın kapısı önüne engel geldiği zaman algılayıcılar ile bu durum algılanması ile algılayıcılardan edinilen veri ile birlikte araç kapasının engele çarpma durumunun engellenmesi için kapının durması gerektiği zamanın ve mesafenin kararı geliştirme kartı tarafından verilecektir.
#### Gerekli Donanım Bileşenleri
------------
- 1 adet Asus TinkerBoard geliştirme kartı
- 2 adet Sharp GP2Y0A41SK0F kızılötesi analog mesafe algılayıcı
- 2 adet MZ80 kızılötesi dijital mesafe algılayıcı
- 2 adet HCSR-04 ses ötesi algılayıcı
- 2 adet 30x30 cm strafor köpük
- 2 adet  3x3 cm yaprak menteşe
- 1 adet strafor köpük yapıştırıcı
- 15 adet kumper kablo
- 1 adet Breadboard
- 3 adet led
- 3 adet 220 ohm direnç 

#### Gerekli Yazılım Bileşenleri
------------
- Python 3
- Arduino Uno R3

#### Şematik Çizim
------------
![alt text][Fritzing]

[Fritzing]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/Fritzing.png
#### Yapım Aşamaları
------------
Kapı sistemi hazırlanması için önce kapının kendisi iki strafor köpüğün iki yaprak menteşe aracılığıyla strafor yapıştıcı kullanılarak yapıldı, ardından Arduino geliştirme kartına  kızılötesi analog algılayıcılar bağlandı, arduino seri port (usb) üzerinde TinkerBoard geliştime kartına bağlandı. TinkerBoard geliştirme kartına MZ80 kızılötesi algılayıcılar bağlandı. Algılayıcıların algıladığı mesafe bilgisini gösteren ledler TinkerBoard geliştirme kartına bağlandı (hazırlanan şemada ledlere direnç bağlı değildir).

##### Adım 1:
Köpükler belli ölçüde kesildi ve menteşe ile birleştirildi. Ardından bir köpük daha yapıştırılarak algılayıcılar için sabitleme kısmı hazırlanmış oldu.

##### Adım 2:
Asus tinkerboard üzerinden python kodu yazıldı,arduino üzerinden de arduino kodu yazıldı ve arduino üzerinde analog sensörlerin bağlantısı yapıldı. Tinkerboard üzerinde analog giriş çıkış portu yok bu yüzden arduino kullanılıyor. Arduino seri port üzerinde tinkerboard a bağlandı ve bağlantının sağlanması için serial kütüphane python üzerinde eklendi ve seri haberleşme ile analog sensörlerin bilgisi alındı. Ayrıca Tinkerboard a SSH üzerinden bağlantı sağlandı.

#### SSH ile TinkerBoard Geliştirme Kartının Bilgisayara Bağlanması

![alt text][ssh]

[ssh]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/ssh.png
'ssh name@IP' komutu terminal üzerinden yazılarak TinkerBoard kartına bağlantı sağlanır. 'name' kullanıcı adı ve 'IP' IP adresidir.

#### TinkerBoard GPIO Pinleri

![alt text][tinkerboardgpio]

[tinkerboardgpio]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/tinkerboard%20gpio.png

#### Arduino ile TinkerBoard Geliştirme Kartının Bağlantısı

Arduino ile TinkerBoard geliştirme kartı usb bağlantısı üzerinden bağlanacaktır. Arduino bağlandığı zaman TinkerBoard geliştirme kartında'/dev' dizininde bağlantı portu gözükecektir (bu projede '/dev/ttyAMC0' portu referans alınmıştır).

#### Python Kodu

```Python
#-*-coding:utf-8-*-
import ASUS.GPIO as GPIO        # Asus tinkerboard GPIO kütüphanesi eklendi
import time                     # time kütüphanesi eklendi
import serial                   # serial kütüphanesi eklendi

GPIO.setwarnings(False)         # GPIO ile ilgili hatalar göz ardı edildi
GPIO.setmode(GPIO.ASUS)         # GPIO modu GPIO.ASUS a göre seçildi (ona göre pin numaraları belirlenecek)
        
mz80_1=252                      # 1. MZ80 (Dijital kızılötesi) sensörü için giriş portu belirlendi
mz80_2=253                      # 2. MZ80 (Dijital kızılötesi) sensörü için giriş portu belirlendi

IR_analog_warn = 257            # Kızılötesi analog sensörlerin uyarı çıkışı
Ultrason_warn = 256             # Ultrasonik sensörlerin uyarı çıkışı
IR_digital_warn = 254           # Kızılötesi dijital sensörlerin uyarı çıkışı

GPIO.setup(mz80_1, GPIO.IN)     # 1. MZ80 sensörünün çıkışı GPIO'da giriş olarak tanımlandı
GPIO.setup(mz80_2, GPIO.IN)     # 2. MZ80 sensörünün çıkışı GPIO'da giriş olarak tanımlandı

GPIO.setup(IR_analog_warn, GPIO.OUT)    # Kızılötesi analog sensörlerin uyarı çıkışı GPIO'da tanımlandı
GPIO.setup(IR_digital_warn, GPIO.OUT)   # Kızılötesi dijital sensörlerin uyarı çıkışı GPIO'da tanımlandı
GPIO.setup(Ultrason_warn, GPIO.OUT)     # Ultrasonik sensörlerin uyarı çıkışı GPIO'da tanımlandı

GPIO.output(Ultrason_warn, GPIO.LOW)    # Ultrasonik sensörlerin uyarı çıkışı LOW olarak tanımlandı
GPIO.output(IR_digital_warn, GPIO.LOW)  # Kızılötesi dijital sensörlerin uyarı çıkışı LOW olarak tanımlandı
GPIO.output(IR_analog_warn, GPIO.LOW)   # Kızılötesi analog sensörlerin uyarı çıkışı LOW olarak tanımlandı

try:                                                                                    
        port = serial.Serial("/dev/ttyACM0",baudrate=9600,timeout = 2)                  # Try except ile klavyede KeyboardInterrupt işlevi olana kadar kod çalışmaya devam eder
        port.flushInput()                                                               # Seri port tanımlandı bununla birlikte timeout ve baudrate değerleri atandı
        print "...starting..."                                                          # Başlatılıyor
        time.sleep(2)                                                                   # 2 saniye bekle
        
        while True:                                                                     # Program sonsuz döngüye girer
                                                                                        # MZ80 sensörünün yaptığı ölçüm limit değerinin altında ise çıkış LOW olur       
                if GPIO.input(mz80_1) and GPIO.input(mz80_2):                           # Her iki MZ80 sensörü çıkış veriyorsa problem yok ve Kızılötesi dijital sensörlerin uyarı çıkışı LOW olarak atanır               
                        print "...no problem..."
                        GPIO.output(IR_digital_warn, GPIO.LOW)  
                else:                                                                   # Aksi halde Kızılötesi dijital sensörlerin uyarı çıkışı HIGH olarak atanır
                        print "be careful"
                        GPIO.output(IR_digital_warn, GPIO.HIGH)
                        
                satir = port.readline()                                                 # satir değişkeni ile seri porttan gelen bilgi okunur
                satir = satir[:-2]                                                      # satir değişkenindeki \r\n ifadeleri temizlenir
                distance_IRsensor1, distance_IRsensor2, distance_ultrason = satir.split("-")    # satir değişkeni 3 farklı değişken bilgisi bulundurur (3-4-5) ve bu bilgiler değişkenlere atanır
                distance_IRsensor1 = float(distance_IRsensor1)                                  # Değişkenlere atanan bilgiler string olduğu için veri tipleri float olark değiştiriliyor
                distance_IRsensor2 = float(distance_IRsensor2)                                  # Değişkenlere atanan bilgiler string olduğu için veri tipleri float olark değiştiriliyor
                distance_ultrason = float(distance_ultrason)                                    # Değişkenlere atanan bilgiler string olduğu için veri tipleri float olark değiştiriliyor

                if distance_ultrason > 2 and distance_ultrason < 300:                           # Ultrasonik sensörün mesafesi 2-300 cm arasında ise Ultrasonik sensörlerin uyarı çıkışı LOW olarak atanır
                        print "...no problem..."                                                
                        GPIO.output(Ultrason_warn, GPIO.LOW)                                    
                elif distance_ultrason > 300:                                                   # Ultrasonik sensörün mesafesi 300 cm den büyük ise sensörleri kontrol et uyarısı verir ve Ultrasonik sensörlerin uyarı çıkışı HIGH olarak atanır
                        print "check your ultrasonic sensors"                                   
                        GPIO.output(Ultrason_warn, GPIO.HIGH)                                   
                else:                                                                           # Aksi halde Ultrasonik sensörlerin uyarı çıkışı HIGH olarak atanır
                        print "be careful"
                        GPIO.output(Ultrason_warn, GPIO.HIGH)
       
                if (distance_IRsensor1 > 5 and distance_IRsensor2 > 5) and (distance_IRsensor1 < 30 and distance_IRsensor2 < 30):       # Kızılötesi analog sensörlerin mesafesi 2-30 cm arasında ise Kızılötesi analog sensörlerin uyarı çıkışı LOW olarak atanır  
                        print "...no problem..."
                        GPIO.output(IR_analog_warn, GPIO.LOW)
                elif distance_IRsensor1 > 30 or distance_IRsensor > 30:                         # Kızılötesi analog sensörlerin mesafesi 30 cm'den büyük olursa sensörleri kontrol et uyarısı verir ve Kızılötesi analog sensörlerin uyarı çıkışı HIGH olarak atanır
                        print "check your analog IR sensors"
                        GPIO.output(IR_analog_warn, GPIO.HIGH)
                else:                                                                           # Aksi halde Kızılötesi analog sensörlerin uyarı çıkışı HIGH olarak atanır
                        print "be careful"
                        GPIO.output(IR_analog_warn, GPIO.HIGH)

except KeyboardInterrupt:                                                                       # KeyboardInterrupt durumu olursa
        GPIO.cleanup()                                                                          # GPIO portlarını temizle
        port.close()          
```

#### Arduino Kodu

```C
#define sensor1 A0 /* Sharp IR GP2Y0A41SK0F (4-30cm, analog1)*/
#define sensor2 A1 /* Sharp IR GP2Y0A41SK0F (4-30cm, analog2)*/
int trigPin1 = 2; /* Sensorun trig pini Arduinonun 2 numaralı ayağına bağlandı */
int echoPin1 = 3 ;  /* Sensorun echo pini Arduinonun 3 numaralı ayağına bağlandı */
int trigPin2 = 4; /* Sensorun trig pini Arduinonun 4 numaralı ayağına bağlandı */
int echoPin2 = 5 ;  /* Sensorun echo pini Arduinonun 5 numaralı ayağına bağlandı */
long uzaklik, uzaklik1, uzaklik2; /* değişkenler tanımlandı*/
long sure, sure1, sure2; /* değişkenler tanımlandı*/

void setup() {
  pinMode(trigPin1, OUTPUT); /* trig pini çıkış olarak ayarlandı */
  pinMode(trigPin2, OUTPUT); /* trig pini çıkış olarak ayarlandı */
  pinMode(echoPin1,INPUT); /* echo pini giriş olarak ayarlandı */
  pinMode(echoPin2,INPUT); /* echo pini giriş olarak ayarlandı */
  Serial.begin(9600); /* seri portu başlat */
  delay(500);         /* 500 ms gecikme */
}

void loop() {
  SonarSensor(trigPin1, echoPin1); /*SonarSensor fonksiyonu kullanılarak 1. sonar sensörün bilgisi alındı*/
  uzaklik1 = uzaklik;
  sure1 = sure;
  SonarSensor(trigPin2, echoPin2); /*SonarSensor fonksiyonu kullanılarak 2. sonar sensörün bilgisi alındı*/
  uzaklik2 = uzaklik;
  sure2 = sure;

  if (uzaklik1 > uzaklik2) {  /* Mesafesi en kısa olan uzaklık seçilecek çünkü sonar sensörlerden birisi engele yakın olduğu zaman sistemin çıkış vermesi gerekiyor*/
      uzaklik = uzaklik2; }
  else if (uzaklik2 > uzaklik1) {
      uzaklik = uzaklik1; }
  
  float volts1 = analogRead(sensor1)*0.0048828125;  /* sensör değeri * (5/1024) */
  int distance1 = 13*pow(volts1, -1); /* datasheet grafiğinden belirlendi */
  float volts2 = analogRead(sensor2); /*0.0048828125;  //sensör değeri * (5/1024) */
  int distance2 = 13*pow(volts2, -1); /* datasheet grafiğinden belirlendi */

  Serial.print(distance1);
  Serial.print("-");
  Serial.print(distance2);
  Serial.print("-");
  Serial.println(uzaklik1); /*Seri porta çıkışımızı yazdırıyoruz, serialprint() ile Serial.println() arasındaki fark Serial.println() seri porta çıkışı verdikten sonra yazı bir alt satıra geçer.*/
  delay(250); /*seri portu yavaşlatmak için (daha uzun aralıklarda çıkış vermesi için)*/  
}
void SonarSensor(int trigPinSensor,int echoPinSensor) /*echo ve trig pinlerinde yapılan giriş çıkışlara göre mesafe ölçümü yapılıyor. */
{  
digitalWrite(trigPinSensor, LOW);/* trigpin LOW */
delayMicroseconds(2); /* 2 mikrosaniye bekle */
digitalWrite(trigPinSensor, HIGH); /* trigpin HIGH */
delayMicroseconds(10); /* 10 mikrosaniye bekle */
digitalWrite(trigPinSensor, LOW); /* trigpin LOW */

sure = pulseIn(echoPinSensor, HIGH); /* pulseIn fonksiyonu, yapılandırılan pinin HIGH veya LOW seviyesinde kaldığı süreyi döndürür */
uzaklik = (sure/2) / 29.1; /* uzaklık değişkeni elde ediliyor */
}
```

#### Nasıl Kullanılır

![alt text][execute]

[execute]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/execute.png

#### Projeye Ait Görseller

![alt text][1]

[1]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/1.jpg
>Kızılötesi algılayıcılar (Kapının alt kısmı)

![alt text][2]

[2]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/2.jpg
>Arduino ve BreadBoard bağlantısı (Kapının arka kısmı)

![alt text][3]

[3]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/3.jpg
>Ses ötesi algılayıcıları (Kapının ön kısmı)






