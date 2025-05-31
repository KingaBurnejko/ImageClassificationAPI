# 🦋 Image Classification API – rozpoznawanie motyli

Projekt realizuje usługę klasyfikacji obrazów z wykorzystaniem sieci neuronowej ResNet50. Zaimplementowano aplikację webową w Flasku z prostym interfejsem HTML oraz pełnym API umożliwiającym trenowanie, testowanie i predykcję modeli.

---

## 📌 Wymagania funkcjonalne

- ✅ Trenowanie modelu na lokalnym zbiorze danych (`data/train/`, `data/valid/`)
- ✅ Testowanie dokładności i F1-score modelu
- ✅ Predykcja pojedynczego obrazu przez API lub interfejs HTML
- ✅ Obsługa statusu trenowania (`/training/status`)
- ✅ Zwracanie błędów trenowania (`/training/error`)
- ✅ Lista dostępnych modeli (`/models`)
- ✅ API w Flasku (z użyciem blueprintów)
- ✅ Sieć ResNet50 z `tensorflow.keras.applications`

---

## 🚀 Szybki start (lokalnie)

1. Utwórz środowisko:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

## 🚀 Uruchom aplikację

```bash
python run.py
```
Aplikacja będzie dostępna pod http://127.0.0.1:5000/

## 🐳 Uruchomienie w Dockerze

Zbuduj obraz i uruchom usługę:

```
docker compose up --build
```
Aplikacja będzie dostępna pod http://localhost:5000/

## 🧠 Trenowanie modelu
Endpoint:

```
POST /train

```

Opis:
- Rozpoczyna trenowanie modelu ResNet50 na danych z folderu data/train/
- Zapisywany jest status do pliku training_status.json
- Wytrenowany model zapisywany jest jako data/butterfly_model.h5

## 📊 Testowanie modelu
Endpoint:

```
POST /test
```
Opis:
- Uruchamia testowanie modelu na zbiorze data/valid/
- Zwraca wartości: loss, accuracy, f1_score

## 📸 Klasyfikacja obrazu
Endpoint:

```
POST /predict
```
Parametr: file — przesyłany obraz (format JPG/PNG)

Zwraca: Klasa i wartość prawdopodobieństwa (np. "class": "Papilio machaon", "confidence": 0.9123)


## 🧪 Dodatkowe endpointy

- GET /training/status – status trenowania (done, in_progress, error)
- GET /training/error – opis błędu w trenowaniu
- GET /models – lista dostępnych modeli .h5