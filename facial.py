import cv2
import pandas as pd
from datetime import datetime

# Inicializa a captura de vídeo
video_capture = cv2.VideoCapture(0)

# Carrega o classificador de rosto pré-treinado do OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Lista para armazenar os horários de detecção
detecções = []

while True:
    # Captura frame por frame
    ret, frame = video_capture.read()
    if not ret:
        break

    # Converte o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostos no frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Para cada rosto detectado
    for (x, y, w, h) in faces:
        # Desenha um retângulo ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Registra o horário atual
        horário_detecção = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        detecções.append([horário_detecção])
        print(f"Face detectada em: {horário_detecção}")

    # Exibe o frame resultante
    cv2.imshow('Video', frame)

    # Pressione 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura e fecha as janelas
video_capture.release()
cv2.destroyAllWindows()

# Salva os horários de detecção em uma planilha Excel
df = pd.DataFrame(detecções, columns=['Horário de Detecção'])
df.to_excel('detecções.xlsx', index=False)
print("Horários de detecção salvos em 'detecções.xlsx'")
