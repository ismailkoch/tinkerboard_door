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
        port.close()                                                                            # portu kapat
