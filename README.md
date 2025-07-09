# Applicazioni Fantini Pelletteria

Repository contenente le applicazioni desktop per la gestione dei prodotti Fantini Pelletteria.

## 📁 Struttura del Progetto

```
App-Fantini-Pelletteria/
├── 📱 WooCommerce Uploader/          # App per caricamento prodotti
│   ├── App/
│   │   └── main_1.py                # Applicazione principale PyQt6
│   ├── Anagrafiche/                  # File di configurazione
│   ├── Colori/                       # Configurazione colori
│   └── README_WooCommerce.md         # Documentazione specifica
├── 🖼️ Photo Editor/                  # App per scontornamento foto
│   ├── dashboard/                    # Server Flask
│   │   ├── app.py                   # Server principale
│   │   ├── templates/               # Template HTML
│   │   └── static/                  # File statici
│   ├── Applicazione per Scontornare PhotoRoom.py
│   ├── Applicazione per Scontornare.py
│   └── Riepilogo Shooting.py
└── 📋 Documentazione/
    ├── README.md                     # Questo file
    ├── LICENSE                       # Licenza MIT
    └── requirements.txt              # Dipendenze Python
```

## 🚀 Applicazioni Disponibili

### 1. WooCommerce Uploader
**Tecnologie**: PyQt6, WooCommerce API, WordPress Media Library

Applicazione desktop per il caricamento automatico di prodotti su siti WooCommerce con gestione multilingua tramite WPML.

#### Caratteristiche:
- **Interfaccia grafica intuitiva** con step-by-step wizard
- **Supporto multilingua** con WPML (italiano/inglese)
- **Caricamento automatico immagini** nella libreria media WordPress
- **Gestione prodotti B2B** su business.fantinipelletteria.com
- **Gestione prodotti retail** su genuineleather.it
- **Struttura cartelle organizzata** per prodotti da caricare/caricati

#### Installazione:
```bash
cd "WooCommerce Uploader"
pip install -r requirements.txt
python App/main_1.py
```

#### Documentazione completa: [README_WooCommerce.md](WooCommerce%20Uploader/README_WooCommerce.md)

### 2. Photo Editor
**Tecnologie**: Flask, PhotoRoom API, Python

Applicazione web per la gestione e scontornamento automatico di foto utilizzando PhotoRoom.

#### Caratteristiche:
- **Dashboard Web**: Interfaccia web per gestire le applicazioni
- **PhotoRoom**: Scontornamento automatico delle foto
- **Ridimensionamento**: Ridimensionamento automatico delle immagini
- **Riepilogo Shooting**: Generazione di report delle sessioni

#### Installazione:
```bash
cd "Photo Editor/dashboard"
pip install flask requests pillow
python app.py
```

#### Utilizzo:
1. Accedi al dashboard web all'indirizzo `http://localhost:5000`
2. Utilizza i pulsanti per avviare le diverse applicazioni
3. Le foto vengono processate automaticamente attraverso le cartelle

## 📋 Requisiti Generali

- Python 3.8+
- PyQt6 (per WooCommerce Uploader)
- Flask (per Photo Editor)
- requests
- pillow

## 🔧 Installazione Completa

```bash
# Clona il repository
git clone https://github.com/samfantini17/App-Fantini-Pelletteria.git
cd App-Fantini-Pelletteria

# Installa le dipendenze
pip install -r requirements.txt

# Per WooCommerce Uploader
cd "WooCommerce Uploader"
python App/main_1.py

# Per Photo Editor
cd "Photo Editor/dashboard"
python app.py
```

## 🛠️ Configurazione

### WooCommerce Uploader
1. Copia `config_example.py` come `config.py`
2. Inserisci le tue credenziali API WooCommerce
3. Configura i percorsi delle cartelle

### Photo Editor
1. Configura le credenziali PhotoRoom API
2. Organizza le foto nelle cartelle appropriate
3. Avvia il server Flask

## 📁 Struttura Dettagliata

### WooCommerce Uploader
```
WooCommerce Uploader/
├── 1-Prodotti_da_caricare/     # Prodotti da processare
├── 2-Prodotti_caricati/         # Prodotti completati
├── Anagrafiche/                  # File di configurazione
│   ├── packaging.csv
│   └── prefissi_nome_prodotto.csv
├── App/
│   └── main_1.py                # Applicazione principale
└── Colori/
    └── Colori.txt               # Configurazione colori
```

### Photo Editor
```
Photo Editor/
├── dashboard/
│   ├── 1_grezze/               # Foto originali
│   ├── 2_da_scontornare/       # Foto da processare
│   ├── 3_ridimensionate_scontornate/  # Foto processate
│   ├── 4_finali/               # Foto finali
│   ├── app.py                   # Server Flask
│   ├── templates/
│   │   └── index.html
│   └── static/
├── Applicazione per Scontornare PhotoRoom.py
├── Applicazione per Scontornare.py
└── Riepilogo Shooting.py
```

## 🔒 Sicurezza

- **NON caricare mai** le credenziali reali su GitHub
- I file `config_example.py` sono solo esempi
- Le cartelle con dati sensibili sono ignorate dal .gitignore

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

## 🤝 Contributi

Le pull request sono benvenute. Per modifiche importanti, apri prima una issue per discutere cosa vorresti cambiare.

## 📞 Supporto

Per problemi o domande, apri una issue su GitHub. 