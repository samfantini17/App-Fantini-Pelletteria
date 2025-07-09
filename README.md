# App Scontornamento Foto

Applicazione Flask per la gestione e scontornamento automatico di foto utilizzando PhotoRoom.

## Struttura del Progetto

```
dashboard/
├── 1_grezze/           # Foto originali
├── 2_da_scontornare/   # Foto da processare
├── 3_ridimensionate_scontornate/  # Foto processate
├── 4_finali/           # Foto finali
├── app.py              # Server Flask
├── Applicazione per Scontornare PhotoRoom.py
├── Applicazione per Scontornare.py
├── Riepilogo Shooting.py
└── templates/
    └── index.html
```

## Funzionalità

- **Dashboard Web**: Interfaccia web per gestire le applicazioni
- **PhotoRoom**: Scontornamento automatico delle foto
- **Ridimensionamento**: Ridimensionamento automatico delle immagini
- **Riepilogo Shooting**: Generazione di report delle sessioni

## Installazione

1. Clona il repository
2. Installa le dipendenze Python necessarie
3. Avvia l'applicazione Flask

```bash
python dashboard/app.py
```

## Utilizzo

1. Accedi al dashboard web all'indirizzo `http://localhost:5000`
2. Utilizza i pulsanti per avviare le diverse applicazioni
3. Le foto vengono processate automaticamente attraverso le cartelle

## Tecnologie

- Python
- Flask
- PhotoRoom API
- HTML/CSS