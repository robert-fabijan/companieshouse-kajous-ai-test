# Użyj oficjalnego obrazu Pythona
FROM python:3.8

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . /app

# Zainstaluj wymagane zależności
RUN pip install -r requirements.txt

# Uruchom aplikację
CMD ["python", "./TwojaAplikacja.py"]
