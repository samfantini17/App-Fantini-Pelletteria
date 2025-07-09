# Istruzioni per Caricare su GitHub

## Passo 1: Crea un Repository su GitHub

1. Vai su [GitHub.com](https://github.com)
2. Clicca su "New repository" (pulsante verde)
3. Inserisci:
   - **Repository name**: `caricamento-prodotti-woocommerce`
   - **Description**: `Applicazione desktop per caricamento automatico prodotti su WooCommerce`
   - **Visibility**: Public o Private (a tua scelta)
   - **Non selezionare** "Add a README file" (l'abbiamo già creato)
4. Clicca "Create repository"

## Passo 2: Collega il Repository Locale a GitHub

Dopo aver creato il repository su GitHub, esegui questi comandi nel terminale:

```bash
# Aggiungi il remote origin (sostituisci USERNAME con il tuo username GitHub)
git remote add origin https://github.com/USERNAME/caricamento-prodotti-woocommerce.git

# Rinomina il branch principale in 'main' (standard GitHub)
git branch -M main

# Carica il codice su GitHub
git push -u origin main
```

## Passo 3: Verifica il Caricamento

1. Vai sul tuo repository GitHub
2. Verifica che tutti i file siano presenti:
   - `README.md`
   - `requirements.txt`
   - `LICENSE`
   - `App/main_1.py`
   - `config_example.py`
   - `STRUCTURE_EXAMPLE.md`
   - `Anagrafiche/` (cartella con file di esempio)
   - `Colori/` (cartella con file di esempio)

## Passo 4: Personalizza il Repository

### Aggiungi Descrizione
Nel repository GitHub, clicca su "About" e aggiungi:
- **Description**: `Applicazione desktop per caricamento automatico prodotti su WooCommerce con supporto multilingua`
- **Topics**: `woocommerce`, `python`, `pyqt6`, `wordpress`, `ecommerce`, `product-management`

### Aggiungi Badge (Opzionale)
Nel README.md, puoi aggiungere badge per:
- Python version
- License
- Build status

## Struttura Finale del Repository

```
caricamento-prodotti-woocommerce/
├── README.md                    # Documentazione principale
├── LICENSE                      # Licenza MIT
├── requirements.txt             # Dipendenze Python
├── .gitignore                  # File da ignorare
├── config_example.py           # Esempio configurazione
├── STRUCTURE_EXAMPLE.md        # Esempio struttura cartelle
├── GITHUB_SETUP.md            # Questo file
├── App/
│   └── main_1.py              # Applicazione principale
├── Anagrafiche/
│   ├── packaging.csv           # Esempio packaging
│   └── prefissi_nome_prodotto.csv  # Esempio prefissi
└── Colori/
    └── Colori.txt              # Esempio colori
```

## Note Importanti

### Sicurezza
- **NON caricare mai** le credenziali reali su GitHub
- Il file `config_example.py` è solo un esempio
- Le cartelle `1-Prodotti_da_caricare/` e `2-Prodotti_caricati/` sono ignorate dal .gitignore

### Aggiornamenti Futuri
Per aggiornare il repository dopo modifiche:

```bash
git add .
git commit -m "Descrizione delle modifiche"
git push origin main
```

### Collaborazione
Se vuoi permettere collaborazioni:
1. Vai su Settings > Collaborators
2. Aggiungi collaboratori per email
3. Oppure rendi il repository pubblico per contributi open source

## Supporto

Se hai problemi con il caricamento:
1. Verifica che Git sia installato: `git --version`
2. Verifica le credenziali GitHub: `git config --list`
3. Controlla i log: `git log --oneline` 