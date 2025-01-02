# Shared Bitcoin Wallet

Un'applicazione per gestire un wallet Bitcoin condiviso tra amici, che tiene traccia delle quote di ciascun utente e del loro valore in tempo reale.

## Caratteristiche
- Gestione quote Bitcoin per utente
- Aggiornamento automatico del valore in USD
- Visualizzazione quote proporzionali
- Interfaccia API RESTful

## Setup

1. Creare un ambiente virtuale:
```bash
python -m venv venv
```

2. Attivare l'ambiente virtuale:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Installare le dipendenze:
```bash
pip install -r requirements.txt
```

4. Avviare l'applicazione:
```bash
python app.py
```

## API Endpoints

- GET /api/users - Lista tutti gli utenti e le loro quote
- GET /api/wallet-info - Informazioni generali sul wallet

## Utenti Iniziali
- Alessandro: 0.001 BTC
- Andrea: 0.001 BTC
- Admin: 0.0045 BTC 