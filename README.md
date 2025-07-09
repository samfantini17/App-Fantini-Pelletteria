# Caricamento Prodotti WooCommerce

Applicazione desktop per il caricamento automatico di prodotti su siti WooCommerce con gestione multilingua tramite WPML.

## Caratteristiche

- **Interfaccia grafica intuitiva** con step-by-step wizard
- **Supporto multilingua** con WPML (italiano/inglese)
- **Caricamento automatico immagini** nella libreria media WordPress
- **Gestione prodotti B2B** su business.fantinipelletteria.com
- **Gestione prodotti retail** su genuineleather.it
- **Struttura cartelle organizzata** per prodotti da caricare/caricati
- **Gestione categorie, tag e attributi** automatica
- **Packaging personalizzabile** con immagini automatiche
- **Posizionamento prodotti** nel catalogo

## Struttura del Progetto

```
Caricamento_Prodotti/
├── 1-Prodotti_da_caricare/     # Prodotti da processare
├── 2-Prodotti_caricati/         # Prodotti completati
├── Anagrafiche/                  # File di configurazione
│   ├── packaging.csv
│   └── prefissi_nome_prodotto.csv
├── App/                          # Codice applicazione
│   └── main_1.py                # File principale
└── Colori/                       # Configurazione colori
    └── Colori.txt
```

## Requisiti

- Python 3.8+
- PyQt6
- requests
- WooCommerce API access
- WordPress Media Library access

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/tuousername/caricamento-prodotti-woocommerce.git
cd caricamento-prodotti-woocommerce
```

2. Installa le dipendenze:
```bash
pip install PyQt6 requests
```

3. Configura le credenziali API nel file `App/main_1.py`:
```python
# Credenziali WooCommerce
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"

# Credenziali WordPress Media
WP_USERNAME = "your_username"
WP_APP_PASSWORD = "your_app_password"

# Credenziali B2B
B2B_CONSUMER_KEY = "your_b2b_consumer_key"
B2B_CONSUMER_SECRET = "your_b2b_consumer_secret"
```

## Utilizzo

1. **Preparazione prodotti**: Organizza i prodotti nelle cartelle `1-Prodotti_da_caricare/` con la struttura:
   ```
   NomeProdotto+Prezzo+Dimensioni+Peso/
   ├── SKU1!/
   │   ├── 1.jpg
   │   ├── 2.jpg
   │   └── 3.jpg
   └── SKU2/
       ├── 1.jpg
       ├── 2.jpg
       └── 3.jpg
   ```

2. **Avvio applicazione**:
   ```bash
   python App/main_1.py
   ```

3. **Processo di caricamento**:
   - Step 1: Seleziona prefisso prodotto
   - Step 2: Scegli Brand o B2B
   - Step 3: Seleziona categorie (primaria e secondarie)
   - Step 4: Seleziona tag (solo per retail)
   - Step 5: Scegli packaging
   - Step 6: Imposta posizione nel catalogo (solo per retail)
   - Step 7: Assegna colori e tag alle immagini
   - Step 8: Rivedi e carica

4. **Completamento**: I prodotti vengono automaticamente spostati in `2-Prodotti_caricati/`

## Configurazione

### File Anagrafiche

- `prefissi_nome_prodotto.csv`: Lista dei prefissi dei nomi prodotto
- `packaging.csv`: Lista delle opzioni di packaging disponibili

### Credenziali API

L'applicazione supporta due siti:
- **GenuineLeather.it** (retail)
- **Business.FantiniPelletteria.com** (B2B)

Ogni sito richiede credenziali separate per WooCommerce API e WordPress Media Library.

## Funzionalità Avanzate

### Gestione Multilingua
- Caricamento automatico in italiano
- Traduzioni gestite manualmente tramite WPML backend
- Immagini condivise tra le traduzioni

### Gestione Immagini
- Caricamento automatico nella libreria media WordPress
- Nomi file univoci per evitare conflitti
- Immagini packaging automatiche
- Posizionamento corretto delle immagini

### Prodotti B2B vs Retail
- **B2B**: Prodotti semplici, solo colore, visibilità nascosta
- **Retail**: Prodotti variabili con attributi colore, tag, posizionamento

## Troubleshooting

### Errori di Autenticazione
- Verifica le credenziali API WooCommerce
- Controlla le credenziali WordPress Media Library
- Assicurati che le Application Passwords siano abilitate

### Errori di Caricamento Immagini
- Verifica che i file immagine esistano
- Controlla i permessi di scrittura
- Verifica la dimensione dei file

### Prodotti Non Visibili
- Controlla lo status "instock"
- Verifica la visibilità del catalogo
- Controlla le categorie assegnate

## Licenza

Questo progetto è rilasciato sotto licenza MIT.

## Contributi

Le pull request sono benvenute. Per modifiche importanti, apri prima una issue per discutere cosa vorresti cambiare.

## Supporto

Per problemi o domande, apri una issue su GitHub. 