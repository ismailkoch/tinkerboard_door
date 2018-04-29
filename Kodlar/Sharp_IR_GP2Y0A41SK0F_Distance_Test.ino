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

