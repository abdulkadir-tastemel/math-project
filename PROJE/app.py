import sqlite3     
import random       
from datetime import datetime


def veritabani_kur():
    baglanti = sqlite3.connect("matematik_projesi.db")
    imlec = baglanti.cursor()

    imlec.execute("CREATE TABLE IF NOT EXISTS Kullanicilar (id INTEGER PRIMARY KEY, ad TEXT)")
    imlec.execute("CREATE TABLE IF NOT EXISTS Formuller (id INTEGER PRIMARY KEY, ad TEXT, formul TEXT)")
    baglanti.commit()
    return baglanti, imlec

baglanti, imlec = veritabani_kur()



def formul_ekle():
    print("\n--- Yeni Formül Ekle ---")
    ad = input("Formülün Adı (Örn: Pisagor, İvme): ") 
 
    formul = input("Formülü 'x' ve 'y' değişkenleriyle yazın (Örn: x**2 + y**2): ").strip().lower()
    
    imlec.execute("INSERT INTO Formuller (ad, formul) VALUES (?, ?)", (ad, formul))
    baglanti.commit()
    print("Başarılı! {} formülü sisteme kaydedildi.".format(ad)) 

def formul_kullan():
    print("\n--- Kayıtlı Formüller ---")
    imlec.execute("SELECT * FROM Formuller")
    formuller = imlec.fetchall() 
    
    if not formuller:
        print("Sistemde hiç formül yok. Önce formül ekleyin!")
        return
        
    for f in formuller: 
        print(f"{f[0]}- {f[1]} (Denklem: {f[2]})")
        
    try: 
        secim = int(input("Kullanmak istediğiniz formülün ID'sini girin: "))
        imlec.execute("SELECT formul FROM Formuller WHERE id = ?", (secim,))
        secilen_formul = imlec.fetchone()[0]
        
       
        x = float(input("x değerini girin: "))
        y = float(input("y değerini girin: "))
        
       
        sonuc = eval(secilen_formul) 
        print(f"\nHesaplama Sonucu: {sonuc}")
        
    except ValueError:
        print("Hata: Lütfen sadece sayı veya geçerli bir ID girin!")
    except ZeroDivisionError:
        print("Hata: Sıfıra bölme işlemi yapılamaz!")
    except Exception as e: 
        print(f"Beklenmeyen bir hata oluştu: {e}")

def antrenman_modu():
    print("\n--- Antrenman Modu ---")
    puan = 0
    soru_sayisi = 3
    
    for i in range(soru_sayisi):
        sayi1 = random.randint(1, 20)
        sayi2 = random.randint(1, 20)
        islem = random.choice(['+', '-', '*'])
        
        soru_metni = f"{sayi1} {islem} {sayi2}"
        dogru_cevap = eval(soru_metni)
        
        try:
            cevap = float(input(f"Soru {i+1}: {soru_metni} = ? : "))
            if cevap == dogru_cevap:
                print("Tebrikler, doğru!")
                puan += 10
            else:
                print(f"Yanlış! Doğru cevap {dogru_cevap} olacaktı.")
        except ValueError:
            print("Geçersiz giriş, puan alamadınız!")
            
    print(f"\nAntrenman bitti! Toplam Puanınız: {puan}")
    rapor_kaydet(puan)

def rapor_kaydet(puan):

    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("gunluk_rapor.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"Tarih: {zaman} | Antrenman Puanı: {puan}\n")
    print("Sonucunuz 'gunluk_rapor.txt' dosyasına kaydedildi.")


def ana_menu():
    while True:
        print("\n" + "="*30)
        print(" MATEMATİK ASİSTANI V1.0")
        print("="*30)
        print("1- Yeni Formül Ekle")
        print("2- Kayıtlı Formül Kullan")
        print("3- Antrenman Modu (Soru Çöz)")
        print("4- Çıkış")
        
        secim = input("Lütfen bir işlem seçin (1-4): ")
        
        if secim == '1':
            formul_ekle()
        elif secim == '2':
            formul_kullan()
        elif secim == '3':
            antrenman_modu()
        elif secim == '4':
            print("Programdan çıkılıyor. Görüşmek üzere!")
            baglanti.close() 
            break 
        else:
            print("Hatalı seçim yaptınız, lütfen tekrar deneyin.")

if __name__ == "__main__":
    ana_menu()