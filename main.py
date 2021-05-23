from telebot import TeleBot
import datetime
from currency_converter import CurrencyConverter
import time
import locale

locale.setlocale(locale.LC_ALL, 'turkish')

# Son 200 gün ortalaması
def uzunortalama():
    Kur_deger = open("C:\\Users\\alp13\\Desktop\\Bitirme-2\\Kur_Deger.txt", "r+")
    Toplam200 = 0.0
    for x in range(200):
        TekTek = Kur_deger.readline()
        Toplam200 += float(TekTek.strip())
    ortalama200 = Toplam200 / 200
    Kur_deger.close()
    return (round(ortalama200, 4))

# Son 50 gün ortalaması
def kısaortalama():
    Kur_deger = open("C:\\Users\\alp13\\Desktop\\Bitirme-2\\Kur_Deger.txt", "r+")
    Toplam50 = 0.0
    for x in range(50):
        TekTek2 = Kur_deger.readline()
        Toplam50 += float(TekTek2.strip())
    ortalama50 = Toplam50 / 50
    Kur_deger.close()
    return (round(ortalama50, 4))

# siteye bağlanma ve veri çekme
def Kur_Degeri():
    c = CurrencyConverter()
    return (round(c.convert(1, 'USD', 'TRY'), 3))

# Cross değerlerini hesaplıyor
def Crossislem():
    kısa = kısaortalama()
    uzun = uzunortalama()
    if kısa > uzun:
        return ("Golden cross !")
    elif uzun > kısa:
        return ("Death cross !")
    elif uzun == kısa:
        return ("Eşitlik söz konusu")
    else:
        return ("!!! Cross işlem kısmında hata mevcuttur !!!")

app = TeleBot(__name__)

# Stop komutu
@app.route('/stop ?(.*)')  # komut düzenleme
def example_command(message, cmd):
    chat_dest = message['chat']['id']
    msg = ("Durduruldu")
    app.send_message(chat_dest, msg)

# Start komutu
@app.route('/start ?(.*)')  # komut düzenleme
def example_command(message, cmd):
    chat_dest = message['chat']['id']
    tarihbilgisi = datetime.datetime.now()
    msg = ("Baslatıldı")
    app.send_message(chat_dest, msg)
    msg = ("Usd-Try:\t{} \nKesişim durumu:\t{}".format(Kur_Degeri(), Crossislem()))
    app.send_message(chat_dest, msg)
    while True:
        if (tarihbilgisi.hour % 2 == 0) and (tarihbilgisi.minute < 1):  # Saat çift ve dakika 0 ise
            msg = ("Usd-Try:\t{} \nKesişim durumu:\t{}".format(Kur_Degeri(), Crossislem()))
            app.send_message(chat_dest, msg)
            BeklemeSuresi = 90
            time.sleep(BeklemeSuresi)

# Help komutu
@app.route('/help ?(.*)')  # komut düzenleme
def example_command(message, cmd):
    chat_dest = message['chat']['id']
    msg = ("/start komutu ile başlamaktadır.")
    app.send_message(chat_dest, msg)

# bot ile bağlantı
if __name__ == '__main__':
    app.config['api_key'] = '1681582450:AAGY-CJBsYguKn5fuljfxBr6z7bSO63crdk'
    app.poll(debug=True)