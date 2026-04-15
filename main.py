import cv2
import datetime

# HEVSEL-GÖZCÜ Yapay Zeka Modülü
# Hazırlayan: Muhammed Ekrem Özer

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# Arka plan çıkarıcı (hareket tespiti için)
back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50)

print("--- HEVSEL-GÖZCÜ SİSTEMİ BAŞLATILDI ---")
print("Durum: Hazırlanma Aşamasında / Geliştirici: M. Ekrem Özer")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü işle ve maske oluştur
    fg_mask = back_sub.apply(frame)
    
    # Gürültü giderme
    _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 2000: # Hassasiyet ayarı
            continue
            
        # Tespit edilen nesneye kutu çiz
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        # Ekran Bilgileri
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"TEHDIT TESPIT: {timestamp}", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Askeri Arayüz Katmanı
    cv2.putText(frame, "HEVSEL-GOZCU V1.0 - ANALIZ MODU", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "DURUM: HAZIRLIK ASAMASINDA", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.imshow('HEVSEL-GOZCU Komuta Merkezi', frame)

    # 'q' tuşuna basınca çık
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
