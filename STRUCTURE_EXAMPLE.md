# Struttura di Esempio per i Prodotti

## Struttura Cartelle

```
1-Prodotti_da_caricare/
├── Borsa+150+30x20x15+1,2/
│   ├── ABC123-1!/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── 3.jpg
│   ├── ABC123-2/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── 3.jpg
│   └── ABC123-3/
│       ├── 1.jpg
│       ├── 2.jpg
│       └── 3.jpg
└── Portafoglio+80+15x10x3+0,5/
    ├── DEF456-1!/
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   └── 3.jpg
    └── DEF456-2/
        ├── 1.jpg
        ├── 2.jpg
        └── 3.jpg
```

## Convenzioni di Nomenclatura

### Nome Cartella Prodotto
```
NomeProdotto+Prezzo+Dimensioni+Peso
```

- **NomeProdotto**: Nome del prodotto (es. "Borsa", "Portafoglio")
- **Prezzo**: Prezzo in euro (es. "150", "80")
- **Dimensioni**: Lunghezza x Larghezza x Altezza in cm (es. "30x20x15")
- **Peso**: Peso in kg (es. "1,2", "0,5")

### Nome Cartella SKU
```
SKU-1!     # Prodotto principale (con !)
SKU-2      # Variante/miniatura (senza !)
```

- **SKU**: Codice prodotto univoco
- **!**: Indica il prodotto principale (quello che verrà mostrato nel catalogo)
- **Numero**: Variante del prodotto

### Nome File Immagine
```
1.jpg      # Immagine principale
2.jpg      # Immagine secondaria
3.jpg      # Immagine terziaria
```

## Esempi Pratici

### Esempio 1: Borsa con 3 varianti
```
Borsa+150+30x20x15+1,2/
├── BORS001-1!/     # Borsa principale nera
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── BORS001-2/      # Borsa marrone
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
└── BORS001-3/      # Borsa beige
    ├── 1.jpg
    ├── 2.jpg
    └── 3.jpg
```

### Esempio 2: Portafoglio semplice
```
Portafoglio+80+15x10x3+0,5/
└── PORT001-1!/     # Portafoglio principale
    ├── 1.jpg
    ├── 2.jpg
    └── 3.jpg
```

## Note Importanti

1. **Solo un prodotto principale per cartella**: Una sola cartella SKU deve avere il "!" alla fine
2. **Immagini obbligatorie**: Ogni SKU deve avere almeno 1.jpg
3. **Formato immagini**: JPG, PNG, JPEG sono supportati
4. **Dimensioni**: Le dimensioni devono essere in formato "Lunghezza x Larghezza x Altezza"
5. **Separatori**: Usa "+" per separare i campi nel nome della cartella prodotto
6. **Codifica**: Usa UTF-8 per i nomi delle cartelle 