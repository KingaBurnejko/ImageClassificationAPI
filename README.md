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

Zbuduj obraz i uruchom usługę:
```
docker compose up --build
```
Aplikacja będzie dostępna pod http://localhost:5000/

**! Uwaga**: Wymagany jest wcześniej skonfigurowany plik `.env`.
Przed uruchomieniem skopiuj plik `.env.example` jako `.env` i uzupełnij:
```
cp .env.example .env
```

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
- GET `/training/status` - status trenowania (done, in_progress, error);
- GET `/training/error` - opis błędu w trenowaniu