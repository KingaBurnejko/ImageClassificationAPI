# 🦋 Image Classification API – rozpoznawanie motyli

Projekt realizuje usługę klasyfikacji obrazów z wykorzystaniem sieci neuronowej ResNet50. Zaimplementowano aplikację webową w Flasku z prostym interfejsem HTML oraz pełnym API umożliwiającym trenowanie, testowanie i predykcję modeli.
Wykorzystano zbiór danych: [Butterfly & Moths Image Classification 100 species](https://www.kaggle.com/datasets/gpiosenka/butterfly-images40-species/data), który docelowo można dodać do folderu `data` w głównym pliku projektu.

---
### Uruchomienie lokalnie
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Uruchomienie aplikacji
```
python run.py
```

Aplikacja będzie dostępna pod http://127.0.0.1:5000/

### Uruchomienie - Docker

**! Uwaga** 
1. Wymagany jest wcześniej skonfigurowany plik `.env`.
Przed uruchomieniem skopiuj plik `.env.example` jako `.env` i uzupełnij:
```
cp .env.example .env
```
2. Przygotuj dane w strukturze:
```
data/
├── train/
├── valid/
└── test/
```
3. Pobierz plik `docker-compose.yml`
```
version: "3.8"

services:
  web:
    build:
      context: .
      args:
        GIT_TOKEN: ${GIT_TOKEN}
        REPO_URL: ${REPO_URL}
        BRANCH: ${BRANCH}
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - MODEL_PATH=${MODEL_PATH}
      - DATA_DIR=${DATA_DIR}
      - IMG_HEIGHT=${IMG_HEIGHT}
      - IMG_WIDTH=${IMG_WIDTH}
      - BATCH_SIZE=${BATCH_SIZE}
      - EPOCHS=${EPOCHS}
      - LABELS_PATH=${LABELS_PATH}
      - STATUS_PATH=${STATUS_PATH}
    volumes:
      - ./data:/app/data
    env_file:
      - .env
    restart: unless-stopped
```

4. Pobierz plik `Dockerfile`
```
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

ARG GIT_TOKEN
ARG REPO_URL
ARG BRANCH=main

RUN git clone -b ${BRANCH} https://${GIT_TOKEN}@${REPO_URL} /app && \
    rm -rf /app/.git

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "7200", "run:app"]

```

5. Zbuduj obraz i uruchom usługę:
```
docker compose up --build
```
Aplikacja będzie dostępna pod http://localhost:5000/



## Funkcjonalności aplikacji

### Trenowanie modelu
Endpoint:
```
POST /train
```
- Rozpoczyna trenowanie modelu ResNet50 na danych z folderu `data/train/`
- Zapisywany jest status do pliku `training_status.json`
- Wytrenowany model zapisywany jest jako `data/butterfly_model.h5`

### Testowanie modelu
Endpoint:
```
POST /test
```
- Uruchamia testowanie modelu na zbiorze `data/valid/`
- Zwracane wartości: loss i accuracy, np.
```
{
  "accuracy": 0.92,
  "loss": 0.15
}
```

### Klasyfikacja obrazu
Endpoint:
```
POST /predict
```
- Parametr: file - przesyłany obraz (format JPG/PNG)
- Zwracane: Klasa i wartość prawdopodobieństwa, np. 
```
{
  "class": "ADONIS",
  "confidence": 0.912
}
```

#### Dodatkowe endpointy
- GET `/training/status` - status trenowania (done, in_progress, error)
- GET `/training/error` - opis błędu w trenowaniu