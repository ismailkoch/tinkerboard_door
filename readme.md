#### Giriş
------------
Arabanın kapısı önüne engel geldiği zaman algılayıcılar ile bu durum algılanması ile algılayıcılardan edinilen veri ile birlikte araç kapasının engele çarpma durumunun engellenmesi için kapının durması gerektiği zamanın ve mesafenin kararı geliştirme kartı tarafından verilecektir.
#### Gerekli Donanım Bileşenleri
------------
- 1 Adet Asus TinkerBoard Geliştirme Kartı
- 2 adet Sharp GP2Y0A41SK0F kızılötesi analog mesafe algılayıcı
- 2 adet MZ80 kızılötesi dijital mesafe algılayıcı
- 2 adet HCSR-04 ses ötesi algılayıcı
- 2 adet 30x30 cm strafor köpük
- 2 adet  3x3 cm yaprak menteşe
- 1 adet strafor köpük yapıştırıcı

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

#### TinkerBoard GPIO Pinleri

![alt text][tinkerboardgpio]

[tinkerboardgpio]: https://github.com/ismailkoch492/tinkerboard_door/blob/master/Proje%20Görselleri/tinkerboard%20gpio.png

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






