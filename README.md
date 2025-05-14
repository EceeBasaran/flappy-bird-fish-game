# Flappy Bird-Fish Adventure
Bu proje, klasik Flappy Bird oyunundan esinlenerek Python ve Pygame ile geliştirilmiş bir 2D oyunudur. Oyunda skor arttıkça karakter ve arkaplan değişir. Örneğin oyuncu 50 puana ulaştığında kuş yerine balık karakterine dönüşür ve borular yerine kılıç balıkları yataydan rastgele olarak karaktere doğru gelir. Her 50 puanda bir arkaplan, karakter ve engeller değişir.

# Oyundan Görseller
![Oyun Başlama Ekranı](images/RESİM1.jpg)
![1.Tema Ölme Resmi](images/RESİM2.jpg)
![2.Tema Oyun Ekranı](images/RESİM3.jpg)
![2.Tema Ölme Ekranı](images/RESİM4.jpg)

# Özellikler
-Pygame tabanlı 2D oyun mekaniği
-Puan arttıkça karakter değişimi
-Balık modunda borular kaldırılır, kılıç balıkları engel olarak gelir.
-Özel ses ve sprite animasyonları
-Kolay kontrol
-Oyun sonu ekranı
-Restart tuşu

# Oynanış
-Boşluk (Space): Zıplama
-Sol tık: Zıplama

# Notlar
-assets/ klasörü oyun için gerekli resim, ses ve animasyonları içerir.
-main.py oyun döngüsünü çalıştırır.

# Kurulum ve Çalıştırma 
### Gereksinimler
-Python 3.x
-Pygame kütüphanesi

### Kurulum
```bash
git clone https://github.com/EceeBasaran/flappy-bird-fish-game
cd flappy-adventure
pip install pygame
python main.py
