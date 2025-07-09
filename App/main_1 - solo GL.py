import sys
import os
import requests
import re
import json

def estrai_prefisso(titolo: str) -> str:
    """
    Restituisce la parte del titolo fino alla seconda lettera maiuscola.
    """
    match = re.finditer(r'[A-Z]', titolo)
    positions = [m.start() for m in match]
    if len(positions) < 2:
        return titolo.strip()
    return titolo[:positions[1]].strip()

def recupera_prefissi_dal_sito() -> list[str]:
    """
    Recupera i prefissi dei titoli prodotto tramite WooCommerce API.
    """
    prefissi = set()
    page = 1
    while True:
        url = "https://www.business.fantinipelletteria.com/wp-json/wc/v3/products"
        auth = ("ck_da6917f5cfcd7bacee57bd0d5a2dac4b745e08cb", "cs_c280b3de7b6cc03d90e1d689dcab752e98daa474")
        params = {"per_page": 100, "page": page}
        resp = requests.get(url, auth=auth, params=params)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        for prodotto in data:
            nome = prodotto.get("name", "")
            prefisso = estrai_prefisso(nome)
            if prefisso:
                prefissi.add(prefisso)
        page += 1
    return sorted(prefissi)

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget,
    QLineEdit, QComboBox, QMessageBox, QHBoxLayout, QCompleter, QCheckBox, QRadioButton,
    QScrollArea, QButtonGroup, QSpinBox, QListWidget, QListWidgetItem, QTableWidget,
    QTableWidgetItem, QDialog, QTextEdit, QAbstractItemView, QGroupBox
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# === CONFIG ===
API_URL = "https://www.genuineleather.it/wp-json"
CONSUMER_KEY = "ck_823c8de6c324868f391603313e0440303aa1b2fe"
CONSUMER_SECRET = "cs_250586cab32e97515528279360bd0bba12ac352d"
# Credenziali WordPress per il caricamento media
WP_USERNAME = "Elia"  # Prova con l'utente admin
WP_APP_PASSWORD = "7vpS QOKp Fr2L Z6yg Vbuo Uryd"  # Application Password
PREFISSI_PATH = os.path.join("C:\\Users\\fanti\\Desktop\\Caricamento_Prodotti\\Anagrafiche", "prefissi_nome_prodotto.csv")
PACKAGING_PATH = os.path.join("C:\\Users\\fanti\\Desktop\\Caricamento_Prodotti\\Anagrafiche", "packaging.csv")
PRODUCTS_DIR = os.path.join("C:\\Users\\fanti\\Desktop\\Caricamento_Prodotti", "1-Prodotti_da_caricare")
CATEGORY_NAMES = {}
TAG_NAMES = {}

def preload_category_and_tag_names():
    global CATEGORY_NAMES, TAG_NAMES
    try:
        # Carica tutte le categorie con paginazione
        CATEGORY_NAMES = {}
        page = 1
        while True:
            cat_url = f"{API_URL}/wc/v3/products/categories"
            params = {"per_page": 100, "page": page}
            r_cat = requests.get(cat_url, auth=(CONSUMER_KEY, CONSUMER_SECRET), params=params)
            r_cat.raise_for_status()
            categories = r_cat.json()
            
            if not categories:  # Nessuna categoria rimasta
                break
                
            for cat in categories:
                CATEGORY_NAMES[cat["id"]] = cat["name"]
            
            page += 1
        
        # Carica tutti i tag con paginazione
        TAG_NAMES = {}
        page = 1
        while True:
            tag_url = f"{API_URL}/wc/v3/products/tags"
            params = {"per_page": 100, "page": page}
            r_tag = requests.get(tag_url, auth=(CONSUMER_KEY, CONSUMER_SECRET), params=params)
            r_tag.raise_for_status()
            tags = r_tag.json()
            
            if not tags:  # Nessun tag rimasto
                break
                
            for tag in tags:
                TAG_NAMES[tag["id"]] = tag["name"]
            
            page += 1
            
    except Exception as e:
        print("Errore nel caricamento dei nomi categorie/tag:", e)

# === STEP 1 to STEP 7 === (unchanged)
# [Mantieni qui il codice esistente degli step da 1 a 7]

# === STEP 1 ===
class StepOne(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Inserisci o scegli il prefisso del prodotto")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Scrivi o scegli da elenco...")
        self.input.setFixedWidth(300)
        self.input.setStyleSheet("padding: 10px; border-radius: 25px; border: 1px solid gray;")
        layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Menu a tendina per selezione prefisso ===
        self.dropdown = QComboBox()
        self.dropdown.setFixedWidth(300)
        layout.addWidget(self.dropdown, alignment=Qt.AlignmentFlag.AlignCenter)
        self.dropdown.currentIndexChanged.connect(self.prefisso_selezionato)

        # === Caricamento prefissi dal file locale ===
        prefissi = self.carica_prefissi_da_file()

        self.dropdown.addItem("Seleziona un nome prodotto...")  # Placeholder iniziale
        for p in prefissi:
            self.dropdown.addItem(p)

        completer = QCompleter(prefissi)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input.setCompleter(completer)

        # === Pulsante Avanti ===
        nav = QHBoxLayout()
        nav.addStretch()
        self.btn_next = QPushButton("Avanti")
        self.btn_next.setFixedWidth(120)
        self.btn_next.setStyleSheet("""
            QPushButton {
                background-color: black; color: white;
                font-size: 14px; padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        nav.addWidget(self.btn_next)
        nav.addStretch()
        layout.addLayout(nav)

        self.setLayout(layout)

    def carica_prefissi_da_file(self):
        # Carica il file di testo contenente i prefissi
        prefissi = []
        try:
            prefissi_path = r"C:\Users\fanti\Desktop\Caricamento_Prodotti\Anagrafiche\prefissi_nome_prodotto.csv"
            with open(prefissi_path, "r", encoding="utf-8") as file:
                prefissi = [line.strip() for line in file if line.strip()]
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nel caricamento dei prefissi dal file: {e}")
        return prefissi

    def prefisso_selezionato(self, index):
        if index > 0:  # Ignora il primo item "placeholder"
            self.input.setText(self.dropdown.currentText())



# === STEP 2 ===
class StepTwo(QWidget):
    def aggiorna_stile_b2b(self, selezionato):
        if selezionato:
            self.btn_b2b.setStyleSheet("""
                QPushButton {
                    background-color: #CCFF00; color: black;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #bbee00;
                }
            """)
        else:
            self.btn_b2b.setStyleSheet("""
                QPushButton {
                    background-color: #0099A8; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #007d8a;
                }
            """)
    
    def __init__(self):
        self.b2b_selected = False  # Nuovo flag per B2B
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Inserisci il Brand o B2B")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        self.combo = QComboBox()
        self.combo.setFixedWidth(300)
        self.combo.setStyleSheet("padding: 10px; border-radius: 25px;")
        self.combo.currentIndexChanged.connect(self.brand_selezionato)

        self.btn_b2b = QPushButton("B2B")
        self.btn_b2b.setFixedWidth(300)
        self.btn_b2b.setStyleSheet("""
            QPushButton {
                background-color: #0099A8; color: white;
                font-size: 14px; padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #007d8a;
            }
        """)
        self.btn_b2b.clicked.connect(self.seleziona_b2b)
        layout.addWidget(self.btn_b2b, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignCenter)

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        self.setLayout(layout)
        self.load_brands()


    def seleziona_b2b(self):
        self.b2b_selected = True
        self.combo.setCurrentIndex(-1)
        self.aggiorna_stile_b2b(True)
        
    def brand_selezionato(self, index):
        if index >= 0:
            self.b2b_selected = False
            self.aggiorna_stile_b2b(False)
            
    def load_brands(self):
        try:
            endpoint = f"{API_URL}/wp/v2/product_brand"
            response = requests.get(endpoint)  # Nessuna autenticazione
            response.raise_for_status()
            for brand in response.json():
                self.combo.addItem(brand['name'], brand['id'])
        except Exception as e:
            QMessageBox.critical(self, "Errore API", f"Errore nel recupero dei brand: {e}")


# === Step 3 ===
class StepThree(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_categories = {}
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Seleziona le categorie e indica la primaria")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.cat_layout = QVBoxLayout()
        container.setLayout(self.cat_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.radio_group = QButtonGroup(self)
        self.radio_group.setExclusive(True)

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        self.setLayout(layout)
        self.load_categories()

    def load_categories(self):
        try:
            page = 1
            while True:
                endpoint = f"{API_URL}/wc/v3/products/categories"
                params = {"per_page": 100, "page": page}
                response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET), params=params)
                response.raise_for_status()
                categories = response.json()
                
                if not categories:  # Nessuna categoria rimasta
                    break
                
                for cat in categories:
                    # Escludi la categoria 'brand' (per nome o slug)
                    if cat.get('name', '').strip().lower() == 'brand' or cat.get('slug', '').strip().lower() == 'brand':
                        continue
                    h_layout = QHBoxLayout()
                    checkbox = QCheckBox(cat['name'])
                    radiobutton = QRadioButton("Primaria")
                    self.radio_group.addButton(radiobutton)
                    h_layout.addWidget(checkbox)
                    h_layout.addWidget(radiobutton)
                    self.cat_layout.addLayout(h_layout)
                    self.selected_categories[checkbox] = (cat['id'], radiobutton)
                
                page += 1
                
        except Exception as e:
            QMessageBox.critical(self, "Errore API", f"Errore nel recupero delle categorie: {e}")

    def get_selected_categories(self):
        selected, primary = [], None
        for cb, (cat_id, radio) in self.selected_categories.items():
            if cb.isChecked():
                selected.append(cat_id)
                if radio.isChecked():
                    primary = cat_id
        return selected, primary


# === Step 4 ===
class StepFour(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_tags = {}
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Seleziona i tag per il prodotto")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.tag_layout = QVBoxLayout()
        container.setLayout(self.tag_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        self.setLayout(layout)
        self.load_tags()

    def load_tags(self):
        try:
            endpoint = f"{API_URL}/wc/v3/products/tags"
            response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET))
            response.raise_for_status()
            for tag in response.json():
                checkbox = QCheckBox(tag['name'])
                self.tag_layout.addWidget(checkbox)
                self.selected_tags[checkbox] = tag['id']
        except Exception as e:
            QMessageBox.critical(self, "Errore API", f"Errore nel recupero dei tag: {e}")

    def get_selected_tags(self):
        return [tag_id for cb, tag_id in self.selected_tags.items() if cb.isChecked()]


# === Step 5 ===
class StepFive(QWidget):
    def __init__(self):
        super().__init__()
        self.packaging_buttons = {}
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Scegli il packaging")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        if os.path.exists(PACKAGING_PATH):
            with open(PACKAGING_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    packaging = line.strip()
                    if packaging:
                        btn = QPushButton(packaging)
                        btn.setFixedWidth(300)
                        btn.setStyleSheet("""
                            QPushButton {
                                background-color: #0099A8; color: white;
                                font-size: 14px; padding: 10px;
                                border-radius: 15px;
                            }
                            QPushButton:hover {
                                background-color: #007d8a;
                            }
                        """)
                        btn.clicked.connect(lambda checked, b=btn: self.select_packaging(b))
                        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
                        self.packaging_buttons[btn] = packaging

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        self.setLayout(layout)

    def select_packaging(self, selected_button):
        # Reset tutti i pulsanti al colore originale
        for btn in self.packaging_buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0099A8; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #007d8a;
                }
            """)
        
        # Imposta il pulsante selezionato al colore verde
        selected_button.setStyleSheet("""
            QPushButton {
                background-color: #CCFF00; color: black;
                font-size: 14px; padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #bbee00;
            }
        """)

    def get_packaging(self):
        for btn, packaging in self.packaging_buttons.items():
            if btn.styleSheet().find("#CCFF00") != -1:
                return packaging
        return None


# === Step 6 ===
class StepSix(QWidget):
    def __init__(self):
        super().__init__()
        self.primary_category_id = None
        self.primary_category_name = None
        self.current_table = None  # Per gestire la tabella dinamica
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Indica la posizione del prodotto nel catalogo")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        # Tabella compatta unica (verrà aggiornata dinamicamente)
        self.current_table = None
        # (La tabella verrà aggiunta dinamicamente subito dopo la descrizione)

        # SpinBox per la posizione
        position_layout = QHBoxLayout()
        position_layout.addStretch()
        position_label = QLabel("Posizione:")
        position_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        position_layout.addWidget(position_label)
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 10000)
        self.spinbox.setValue(1)
        self.spinbox.setFixedWidth(100)
        self.spinbox.setStyleSheet("padding: 10px; border-radius: 10px; font-size: 16px;")
        position_layout.addWidget(self.spinbox)
        position_layout.addStretch()
        layout.addLayout(position_layout)

        # Bottoni in basso come nello step 5
        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)
        self.setLayout(layout)

    def show_all_categories_positions(self):
        # Rimuovi la tabella precedente se presente
        if self.current_table is not None and self.layout() is not None:
            self.layout().removeWidget(self.current_table)
            self.current_table.deleteLater()
            self.current_table = None
        # Tabella compatta unica
        table = QTableWidget()
        table.setStyleSheet("QTableWidget {margin:0;padding:0;} QTableWidget::item {padding:2px;}")
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Categoria", "Nome Prodotto", "Range Posizioni", "Quantità"])
        table.setColumnWidth(0, 180)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 140)
        table.setColumnWidth(3, 80)
        table.setMaximumHeight(220)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        header = table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
        # Costruisco un dizionario per raggruppare e contare
        row_counter = {}
        for cat_id in self.selected_category_ids:
            cat_name = CATEGORY_NAMES.get(cat_id, str(cat_id))
            is_main = (cat_id == self.primary_category_id)
            cat_label = f"{cat_name} (Principale)" if is_main else cat_name
            try:
                endpoint = f"{API_URL}/wc/v3/products"
                params = {
                    "category": cat_id,
                    "per_page": 100,
                    "orderby": "menu_order",
                    "order": "asc"
                }
                response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET), params=params)
                response.raise_for_status()
                products = response.json()
                positions = []
                for product in products:
                    position = product.get('menu_order', 0)
                    if position > 0:
                        positions.append({
                            'id': product['id'],
                            'name': product['name'],
                            'position': position
                        })
                positions.sort(key=lambda x: x['position'])
                ranges = self.analyze_position_ranges(positions)
                for range_info in ranges:
                    start = range_info['start']
                    end = range_info['end']
                    range_text = f"Posizione {start}" if start == end else f"Range {start}-{end}"
                    for product in range_info['products']:
                        key = (cat_label, product['name'], range_text)
                        row_counter[key] = row_counter.get(key, 0) + 1
            except Exception as e:
                key = (cat_label, "Errore", f"Errore: {e}")
                row_counter[key] = 1
        # Popolo la tabella senza duplicati
        table.setRowCount(len(row_counter))
        for i, (key, qty) in enumerate(row_counter.items()):
            cat_label, prod_name, range_text = key
            table.setItem(i, 0, QTableWidgetItem(cat_label))
            table.setItem(i, 1, QTableWidgetItem(prod_name))
            table.setItem(i, 2, QTableWidgetItem(range_text))
            table.setItem(i, 3, QTableWidgetItem(str(qty)))
        # Aggiungo la tabella subito dopo la descrizione
        if self.layout() is not None:
            self.layout().insertWidget(1, table)
            self.current_table = table

    def set_primary_category(self, category_id, category_name):
        """Imposta la categoria primaria e carica le informazioni sulle posizioni"""
        self.primary_category_id = category_id
        self.primary_category_name = category_name
        self.category_info_label.setText(f"Categoria primaria: {category_name}")
        self.load_category_positions()

    def load_category_positions(self):
        """Carica i prodotti della categoria e analizza le posizioni occupate"""
        if not self.primary_category_id:
            return
            
        try:
            # Recupera tutti i prodotti della categoria
            endpoint = f"{API_URL}/wc/v3/products"
            params = {
                "category": self.primary_category_id,
                "per_page": 100,
                "orderby": "menu_order",
                "order": "asc"
            }
            response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET), params=params)
            response.raise_for_status()
            products = response.json()
            
            # Estrai le posizioni (menu_order)
            positions = []
            for product in products:
                position = product.get('menu_order', 0)
                if position > 0:  # Solo posizioni valide
                    positions.append({
                        'id': product['id'],
                        'name': product['name'],
                        'position': position
                    })
            
            # Ordina per posizione
            positions.sort(key=lambda x: x['position'])
            
            # Analizza i range di posizioni
            ranges = self.analyze_position_ranges(positions)
            
            # Mostra le informazioni
            self.display_position_ranges(ranges, positions)
            
        except Exception as e:
            self.clear_positions_table()
            self.suggestions_label.setText(f"Errore nel caricamento delle posizioni: {e}")

    def clear_positions_table(self):
        """Pulisce la tabella delle posizioni"""
        self.positions_table.setRowCount(0)

    def display_position_ranges(self, ranges, all_positions):
        """Mostra i range di posizioni nell'interfaccia"""
        if not ranges:
            self.clear_positions_table()
            self.suggestions_label.setText("Nessun prodotto trovato in questa categoria.")
            return
        
        # Popola la tabella
        self.positions_table.setRowCount(len(ranges))
        
        for i, range_info in enumerate(ranges):
            start = range_info['start']
            end = range_info['end']
            products = range_info['products']
            
            # Range posizioni
            if start == end:
                range_text = f"Posizione {start}"
            else:
                range_text = f"Range {start}-{end}"
            
            # Numero prodotti
            num_products = len(products)
            
            # Lista prodotti
            products_text = ""
            for product in products:
                products_text += f"• {product['name']} (pos. {product['position']})\n"
            products_text = products_text.strip()
            
            # Inserisci nella tabella
            self.positions_table.setItem(i, 0, QTableWidgetItem(range_text))
            self.positions_table.setItem(i, 1, QTableWidgetItem(str(num_products)))
            self.positions_table.setItem(i, 2, QTableWidgetItem(products_text))
        
        # Aggiungi suggerimenti per posizioni libere
        suggested_positions = self.suggest_free_positions(ranges)
        if suggested_positions:
            suggestions_text = "Posizioni consigliate: " + ", ".join(map(str, suggested_positions[:5]))
        else:
            suggestions_text = "Posizioni consigliate: 1"
        
        self.suggestions_label.setText(suggestions_text)

    def analyze_position_ranges(self, positions):
        """Analizza le posizioni e trova i range continui"""
        if not positions:
            return []
        
        ranges = []
        current_range_start = positions[0]['position']
        current_range_end = positions[0]['position']
        current_products = [positions[0]]
        
        for i in range(1, len(positions)):
            current_pos = positions[i]['position']
            expected_pos = current_range_end + 1
            
            if current_pos == expected_pos:
                # Continua il range corrente
                current_range_end = current_pos
                current_products.append(positions[i])
            else:
                # Chiudi il range corrente e inizia uno nuovo
                ranges.append({
                    'start': current_range_start,
                    'end': current_range_end,
                    'products': current_products.copy()
                })
                current_range_start = current_pos
                current_range_end = current_pos
                current_products = [positions[i]]
        
        # Aggiungi l'ultimo range
        ranges.append({
            'start': current_range_start,
            'end': current_range_end,
            'products': current_products
        })
        
        return ranges

    def suggest_free_positions(self, ranges):
        """Suggerisce posizioni libere basate sui range esistenti"""
        suggestions = []
        
        # Prima posizione se non c'è nulla
        if not ranges:
            return [1]
        
        # Dopo l'ultimo range
        last_end = ranges[-1]['end']
        suggestions.append(last_end + 1)
        
        # Tra i range se ci sono gap
        for i in range(len(ranges) - 1):
            gap_start = ranges[i]['end'] + 1
            gap_end = ranges[i + 1]['start'] - 1
            if gap_start <= gap_end:
                suggestions.append(gap_start)
        
        # Ordina le suggerimenti dal più piccolo al più grande
        suggestions.sort()
        return suggestions

    def get_visibility_position(self):
        return self.spinbox.value()

    def set_categories(self, category_ids):
        """Imposta tutte le categorie selezionate e mostra i range per ciascuna."""
        self.selected_category_ids = category_ids
        self.show_all_categories_positions()






# === STEP 7 ===
class ClickableImageLabel(QLabel):
    def __init__(self, img_path, dot, parent=None):
        super().__init__(parent)
        self.img_path = img_path
        self.dot = dot
        self.click_callback = None
    
    def set_click_callback(self, callback):
        self.click_callback = callback
    
    def mousePressEvent(self, event):
        if self.click_callback:
            self.click_callback(self.img_path, self.dot)
        super().mousePressEvent(event)

class StepSeven(QWidget):
    def __init__(self, current_product=None):
        super().__init__()
        self.selected_data = {}
        self.colors = {}
        self.tags = {}  # Tag disponibili dal sito
        self.current_product = current_product

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Scritta descrittiva
        desc_label = QLabel("Seleziona i tag ed il colore per ogni immagine")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        # Layout orizzontale per le immagini
        self.images_layout = QHBoxLayout()
        self.images_layout.setSpacing(20)
        self.images_layout.setContentsMargins(0, 10, 0, 10)
        layout.addLayout(self.images_layout)

        self.btn_edit = QPushButton("Scegli il tag ed il colore")
        self.btn_edit.setFixedWidth(300)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #0099A8; color: white;
                font-size: 14px; padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #007d8a;
            }
        """)
        self.btn_edit.clicked.connect(self.edit_tags_and_color)
        layout.addWidget(self.btn_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Tabella per mostrare i tag e colori selezionati
        self.table_selections = QTableWidget()
        self.table_selections.setColumnCount(3)
        self.table_selections.setHorizontalHeaderLabels(["Nome Prodotto", "Colore", "Tag"])
        header = self.table_selections.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
            # Imposta larghezze specifiche per le colonne
            self.table_selections.setColumnWidth(0, 250)  # Nome Prodotto più largo
            self.table_selections.setColumnWidth(1, 120)  # Colore medio
            # La colonna Tag si estende automaticamente
        layout.addWidget(QLabel("Selezioni effettuate:"))
        layout.addWidget(self.table_selections)

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_next = QPushButton("Avanti")
        for btn in (self.btn_back, self.btn_next):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        self.setLayout(layout)
        self.load_colors()
        self.load_tags()
        self.load_images()

    def set_current_product(self, product_name):
        """Imposta il prodotto corrente e ricarica le immagini"""
        self.current_product = product_name
        self.load_images()

    def load_colors(self):
        try:
            endpoint = f"{API_URL}/wc/v3/products/attributes/1/terms"
            response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET))
            response.raise_for_status()
            for color in response.json():
                self.colors[color['name']] = color['id']
        except Exception as e:
            QMessageBox.critical(self, "Errore API", f"Errore nel recupero dei colori: {e}")

    def load_tags(self):
        try:
            endpoint = f"{API_URL}/wc/v3/products/tags"
            response = requests.get(endpoint, auth=(CONSUMER_KEY, CONSUMER_SECRET))
            response.raise_for_status()
            for tag in response.json():
                self.tags[tag['name']] = tag['id']
        except Exception as e:
            QMessageBox.critical(self, "Errore API", f"Errore nel recupero dei tag: {e}")

    def load_images(self):
        # Pulisci il layout delle immagini
        while self.images_layout.count():
            child = self.images_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()
        
        if not self.current_product:
            return
            
        prodotto_path = os.path.join(PRODUCTS_DIR, self.current_product)
        if os.path.isdir(prodotto_path):
            for sku in os.listdir(prodotto_path):
                sku_path = os.path.join(prodotto_path, sku)
                if os.path.isdir(sku_path):
                    for file in os.listdir(sku_path):
                        if file.startswith("1") and file.lower().endswith((".jpg", ".png", ".jpeg")):
                            img_path = os.path.join(sku_path, file)
                            self.create_image_widget(img_path, f"{self.current_product}/{sku}")

    def create_image_widget(self, img_path, label_text):
        """Crea un widget per ogni immagine con pallino di selezione"""
        # Container per immagine e pallino
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(5, 5, 5, 5)
        
        # Pallino di selezione
        selection_dot = QLabel()
        selection_dot.setFixedSize(20, 20)
        selection_dot.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 10px;
            }
        """)
        selection_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(selection_dot, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Immagine cliccabile
        image_label = ClickableImageLabel(img_path, selection_dot)
        pixmap = QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedSize(150, 150)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #cccccc; border-radius: 5px;")
        image_label.set_click_callback(self.select_image)
        
        container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Label del nome
        name_label = QLabel(label_text)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 10px; color: #666666; margin-top: 5px;")
        container_layout.addWidget(name_label)
        
        container.setLayout(container_layout)
        self.images_layout.addWidget(container)

    def select_image(self, img_path, dot):
        """Seleziona un'immagine e aggiorna il pallino"""
        # Reset tutti i pallini
        for i in range(self.images_layout.count()):
            child = self.images_layout.itemAt(i)
            if child:
                container = child.widget()
                if container:
                    layout = container.layout()
                    if layout:
                        dot_item = layout.itemAt(0)
                        if dot_item:
                            dot_widget = dot_item.widget()
                            if dot_widget:
                                dot_widget.setStyleSheet("""
                                    QLabel {
                                        background-color: white;
                                        border: 2px solid #cccccc;
                                        border-radius: 10px;
                                    }
                                """)
        
        # Riempie il pallino selezionato
        dot.setStyleSheet("""
            QLabel {
                background-color: #0099A8;
                border: 2px solid #0099A8;
                border-radius: 10px;
            }
        """)
        
        # Salva l'immagine selezionata
        self.selected_image_path = img_path

    def edit_tags_and_color(self):
        if not hasattr(self, 'selected_image_path') or not self.selected_image_path:
            QMessageBox.warning(self, "Attenzione", "Seleziona un'immagine prima di procedere.")
            return

        img_path = self.selected_image_path

        dialog = QDialog(self)
        dialog.setWindowTitle("Modifica Tag e Colore")
        dialog.setFixedSize(400, 500)
        layout = QVBoxLayout()

        # Selezione colore
        color_label = QLabel("Seleziona il colore:")
        color_combo = QComboBox()
        for color in self.colors:
            color_combo.addItem(color)
        layout.addWidget(color_label)
        layout.addWidget(color_combo)

        # Selezione tag
        tags_label = QLabel("Seleziona i tag:")
        tags_list = QListWidget()
        tags_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        for tag in self.tags:
            item = QListWidgetItem(tag)
            tags_list.addItem(item)
        layout.addWidget(tags_label)
        layout.addWidget(tags_list)

        # Pulsanti
        buttons = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Annulla")
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        dialog.setLayout(layout)

        # Connessioni
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_color = color_combo.currentText()
            selected_tags = [item.text() for item in tags_list.selectedItems()]
            
            self.selected_data[img_path] = {
                "tags": selected_tags,
                "color": selected_color
            }
            
            self.update_selections_table()

    def update_selections_table(self):
        self.table_selections.setRowCount(len(self.selected_data))
        for i, (img_path, data) in enumerate(self.selected_data.items()):
            # Estrai nome prodotto e SKU dal path
            sku = os.path.basename(os.path.dirname(img_path))
            prodotto = os.path.basename(os.path.dirname(os.path.dirname(img_path)))
            nome_prodotto = f"{prodotto}/{sku}"
            
            color = data.get("color", "")
            tags = ", ".join(data.get("tags", []))
            
            self.table_selections.setItem(i, 0, QTableWidgetItem(nome_prodotto))
            self.table_selections.setItem(i, 1, QTableWidgetItem(color))
            self.table_selections.setItem(i, 2, QTableWidgetItem(tags))

    def get_selected_data(self):
        return self.selected_data



# === Step 8 ===
class StepEight(QWidget):
    def __init__(self, data_collector, step7_data, current_product=None):
        super().__init__()
        self.data_collector = data_collector
        self.step7_data = step7_data
        self.current_product = current_product

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        self.table_global = QTableWidget()
        self.table_global.setColumnCount(2)
        self.table_global.setHorizontalHeaderLabels(["Campo", "Valore"])
        self.table_global.setColumnWidth(0, 200)  # Colonna Campo più larga
        self.table_global.setColumnWidth(1, 400)  # Colonna Valore molto più larga
        header_global = self.table_global.horizontalHeader()
        if header_global:
            header_global.setStretchLastSection(True)
        self.table_global.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                gridline-color: #cccccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                border: 1px solid #cccccc;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        layout.addWidget(QLabel("Dati Globali"))
        layout.addWidget(self.table_global)

        self.table_images = QTableWidget()
        self.table_images.setColumnCount(3)
        self.table_images.setHorizontalHeaderLabels(["SKU", "Colore", "Tag Specifici"])
        self.table_images.setColumnWidth(0, 150)  # Colonna SKU
        self.table_images.setColumnWidth(1, 120)  # Colonna Colore
        self.table_images.setColumnWidth(2, 350)  # Colonna Tag più larga
        header_images = self.table_images.horizontalHeader()
        if header_images:
            header_images.setStretchLastSection(True)
        self.table_images.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                gridline-color: #cccccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                border: 1px solid #cccccc;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        layout.addWidget(QLabel("Dati per Immagine"))
        layout.addWidget(self.table_images)

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Indietro")
        self.btn_finish = QPushButton("Fine")
        self.btn_upload = QPushButton("Carica Prodotti")
        for btn in (self.btn_back, self.btn_finish, self.btn_upload):
            btn.setFixedWidth(120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
        self.btn_upload.setStyleSheet("""
            QPushButton {
                background-color: #CCFF00; color: black;
                font-size: 14px; padding: 10px;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbee00;
            }
        """)
        nav.addWidget(self.btn_back)
        nav.addStretch()
        nav.addWidget(self.btn_upload)
        nav.addWidget(self.btn_finish)
        layout.addLayout(nav)

        self.setLayout(layout)

    def set_current_product(self, product_name):
        """Imposta il prodotto corrente"""
        self.current_product = product_name

    def extract_global_data_from_folder(self):
        try:
            if not self.current_product:
                return {}
                
            nome_cartella = self.current_product
            parts = nome_cartella.split("+")
            nome_interno = parts[0] if len(parts) > 0 else ""
            prezzo = parts[1] if len(parts) > 1 else ""
            dimensioni = parts[2] if len(parts) > 2 else ""
            peso = parts[3] if len(parts) > 3 else ""

            # Parsing corretto: Lunghezza x Larghezza x Altezza
            lunghezza, larghezza, altezza = ("", "", "")
            if "x" in dimensioni:
                dim_parts = dimensioni.split("x")
                if len(dim_parts) == 3:
                    lunghezza, larghezza, altezza = dim_parts
            lunghezza = lunghezza.strip() or "0"
            larghezza = larghezza.strip() or "0"
            altezza = altezza.strip() or "0"

            return {
                "Nome interno": nome_interno,
                "Prezzo": prezzo,
                "Lunghezza": lunghezza,
                "Larghezza": larghezza,
                "Altezza": altezza,
                "Peso": peso
            }
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nella lettura cartella prodotto: {e}")
            return {}

    def load_summary(self):
        data = self.data_collector()
        extra_data = self.extract_global_data_from_folder()

        # Tabella globale
        combined = {
            **extra_data,
            "Nome prodotto": data.get("Nome prodotto", ""),
            "Brand": data.get("Brand", ""),
            "Categorie selezionate": data.get("Categorie selezionate", ""),
            "Categoria primaria": data.get("Categoria primaria", ""),
            "Tag selezionati": data.get("Tag selezionati", ""),
            "Packaging": data.get("Packaging", ""),
            "Posizione visibilità": data.get("Posizione visibilità", "")
        }

        self.table_global.setRowCount(len(combined))
        for i, (key, value) in enumerate(combined.items()):
            self.table_global.setItem(i, 0, QTableWidgetItem(key))
            self.table_global.setItem(i, 1, QTableWidgetItem(str(value)))

        # Tabella immagini
        selected_data = self.step7_data()
        self.table_images.setRowCount(len(selected_data))
        for i, (path, info) in enumerate(selected_data.items()):
            sku = os.path.basename(os.path.dirname(path))
            color = info.get("color", "")
            tags = ", ".join(info.get("tags", []))
            self.table_images.setItem(i, 0, QTableWidgetItem(sku))
            self.table_images.setItem(i, 1, QTableWidgetItem(color))
            self.table_images.setItem(i, 2, QTableWidgetItem(tags))

# === PRODUCT UPLOADER ===
class ProductUploader:
    def __init__(self, api_url, consumer_key, consumer_secret):
        self.api_url = api_url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
    def upload_product(self, product_data, image_data, global_data):
        """Carica un prodotto su WooCommerce"""
        try:
            # Recupera l'ID del brand selezionato
            brand_id = global_data.get("Brand_ID")
            # Separa i prodotti principali (con !) dalle miniature (senza !)
            main_skus = []
            thumbnail_skus = []
            
            for sku in image_data.keys():
                if sku.endswith("!"):
                    main_skus.append(sku)
                else:
                    thumbnail_skus.append(sku)
            
            # Crea il prodotto principale solo per gli SKU con !
            for main_sku in main_skus:
                main_img_data = {main_sku: image_data[main_sku]}
                
                # Debug: mostra i dati globali estratti
                print("DEBUG DATI GLOBALI:", global_data)
                
                # Prepara i dati del prodotto principale
                product_payload = {
                    "name": f"{global_data['Nome prodotto']} - {image_data[main_sku]['color']}",
                    "slug": f"{global_data['Nome prodotto'].lower().replace(' ', '-')}-{image_data[main_sku]['color'].lower().replace(' ', '-')}",
                    "type": "simple",  # Prodotto semplice per il principale
                    "description": self.create_product_description(global_data, image_data[main_sku]['color']),
                    "short_description": "",
                    "categories": self.get_category_ids(global_data["Categorie selezionate"]),
                    "tags": self.get_tag_ids(global_data["Tag selezionati"]),
                    "brands": [brand_id] if brand_id else [],
                    "regular_price": global_data["Prezzo"],
                    "sku": main_sku,
                    "manage_stock": False,
                    "stock_status": "instock",
                    "menu_order": global_data["Posizione visibilità"],
                    "dimensions": {
                        "length": str(global_data["Lunghezza"]),
                        "width": str(global_data["Larghezza"]),
                        "height": str(global_data["Altezza"])
                    },
                    "meta_data": [
                        {"key": "_brand", "value": global_data["Brand"]},
                        {"key": "_length", "value": global_data["Lunghezza"]},
                        {"key": "_width", "value": global_data["Larghezza"]},
                        {"key": "_height", "value": global_data["Altezza"]},
                        {"key": "_weight", "value": global_data["Peso"]},
                        {"key": "_packaging", "value": global_data["Packaging"]},
                        {"key": "_color", "value": image_data[main_sku]["color"]},
                        {"key": "_thumbnail_skus", "value": ",".join(thumbnail_skus)}
                    ]
                }
                
                # In upload_product, subito prima della POST:
                print(f"DEBUG DIMENSIONI PRINCIPALE: {product_payload['dimensions']}")
                print("PAYLOAD CHE INVIO:", json.dumps(product_payload, indent=2, ensure_ascii=False))
                
                # Crea il prodotto principale
                response = requests.post(
                    f"{self.api_url}/wc/v3/products",
                    auth=(self.consumer_key, self.consumer_secret),
                    json=product_payload
                )
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print("ERRORE RISPOSTA API:", response.text)
                    raise
                product = response.json()
                product_id = product["id"]
                
                # Carica le immagini per il prodotto principale
                self.upload_product_images(product_id, main_img_data, global_data)
                
                # Crea le miniature per gli SKU senza !
                thumbnail_ids = self.create_thumbnail_products(product_id, thumbnail_skus, image_data, global_data, brand_id)
                
                # Aggiorna le miniature correlate per tutti i prodotti
                self.update_related_thumbnails(product_id, thumbnail_ids, image_data, global_data)
                
                return product_id
            
            # Se non ci sono prodotti principali, crea un prodotto normale
            if not main_skus:
                return self.create_normal_product(image_data, global_data, brand_id)
                
        except Exception as e:
            raise Exception(f"Errore nel caricamento del prodotto: {e}")
    
    def create_normal_product(self, image_data, global_data, brand_id=None):
        """Crea un prodotto normale quando non ci sono SKU con !"""
        product_payload = {
            "name": global_data["Nome prodotto"],
            "type": "variable",
            "description": self.create_product_description(global_data, ""),  # Colore vuoto per prodotto variabile
            "short_description": "",
            "categories": self.get_category_ids(global_data["Categorie selezionate"]),
            "tags": self.get_tag_ids(global_data["Tag selezionati"]),
            "brands": [brand_id] if brand_id else [],
            "attributes": [
                {
                    "id": 1,
                    "name": "Colore",
                    "position": 0,
                    "visible": True,
                    "variation": True,
                    "options": list(set([img["color"] for img in image_data.values()]))
                }
            ],
            "menu_order": global_data["Posizione visibilità"],
            "dimensions": {
                "length": str(global_data["Larghezza"]),
                "width": str(global_data["Larghezza"]),
                "height": str(global_data["Altezza"])
            },
            "meta_data": [
                {"key": "_brand", "value": global_data["Brand"]},
                {"key": "_width", "value": global_data["Larghezza"]},
                {"key": "_width", "value": global_data["Larghezza"]},
                {"key": "_height", "value": global_data["Altezza"]},
                {"key": "_weight", "value": global_data["Peso"]},
                {"key": "_packaging", "value": global_data["Packaging"]}
            ]
        }
        
        # In create_normal_product, subito prima della POST:
        print(f"DEBUG DIMENSIONI VARIABILE: {product_payload['dimensions']}")
        
        response = requests.post(
            f"{self.api_url}/wc/v3/products",
            auth=(self.consumer_key, self.consumer_secret),
            json=product_payload
        )
        response.raise_for_status()
        product = response.json()
        product_id = product["id"]
        
        # Crea le varianti
        self.create_product_variations(product_id, image_data, global_data)
        
        return product_id
    
    def create_thumbnail_products(self, main_product_id, thumbnail_skus, image_data, global_data, brand_id=None):
        """Crea prodotti miniature per gli SKU senza !"""
        thumbnail_ids = {}
        for sku in thumbnail_skus:
            try:
                # Crea un prodotto semplice per la miniatura
                thumbnail_payload = {
                    "name": f"{global_data['Nome prodotto']} - {image_data[sku]['color']}",
                    "slug": f"{global_data['Nome prodotto'].lower().replace(' ', '-')}-{image_data[sku]['color'].lower().replace(' ', '-')}",
                    "type": "simple",
                    "description": self.create_product_description(global_data, image_data[sku]['color']),
                    "short_description": "",
                    "categories": self.get_category_ids(global_data["Categorie selezionate"]),
                    "tags": self.get_tag_ids(global_data["Tag selezionati"]),
                    "brands": [brand_id] if brand_id else [],
                    "regular_price": global_data["Prezzo"],
                    "sku": sku,
                    "manage_stock": False,
                    "stock_status": "instock",
                    "catalog_visibility": "hidden",
                    "dimensions": {
                        "length": str(global_data["Larghezza"]),
                        "width": str(global_data["Larghezza"]),
                        "height": str(global_data["Altezza"])
                    },
                    "meta_data": [
                        {"key": "_brand", "value": global_data["Brand"]},
                        {"key": "_width", "value": global_data["Larghezza"]},
                        {"key": "_width", "value": global_data["Larghezza"]},
                        {"key": "_height", "value": global_data["Altezza"]},
                        {"key": "_weight", "value": global_data["Peso"]},
                        {"key": "_packaging", "value": global_data["Packaging"]},
                        {"key": "_color", "value": image_data[sku]["color"]},
                        {"key": "_is_thumbnail", "value": "yes"},
                        {"key": "_main_product_id", "value": main_product_id}
                    ]
                }
                
                # In create_thumbnail_products, subito prima della POST:
                print(f"DEBUG DIMENSIONI MINIATURA: {thumbnail_payload['dimensions']}")
                
                response = requests.post(
                    f"{self.api_url}/wc/v3/products",
                    auth=(self.consumer_key, self.consumer_secret),
                    json=thumbnail_payload
                )
                response.raise_for_status()
                thumbnail_product = response.json()
                thumbnail_id = thumbnail_product["id"]
                thumbnail_ids[sku] = thumbnail_id
                
                # Carica tutte le immagini disponibili per la miniatura
                thumbnail_img_data = {sku: {k: v for k, v in image_data[sku].items() if k.startswith("image_")}}
                self.upload_product_images(thumbnail_id, thumbnail_img_data, global_data)
                
            except Exception as e:
                print(f"Errore nella creazione della miniatura {sku}: {e}")
        
        return thumbnail_ids
    
    def update_related_thumbnails(self, main_product_id, thumbnail_ids, image_data, global_data):
        """Aggiorna le miniature correlate per tutti i prodotti del gruppo, secondo la logica richiesta."""
        try:
            # Lista ID delle miniature (prodotti alternativi)
            alternative_ids = list(thumbnail_ids.values())
            all_ids = [main_product_id] + alternative_ids
            
            for current_id in all_ids:
                if current_id == main_product_id:
                    # Il principale: miniature = tutti gli alternativi
                    related = alternative_ids
                else:
                    # Alternativo: miniature = principale + altri alternativi (escluso se stesso)
                    related = [main_product_id] + [aid for aid in alternative_ids if aid != current_id]
                if related:
                    response = requests.put(
                        f"{self.api_url}/wc/v3/products/{current_id}",
                        auth=(self.consumer_key, self.consumer_secret),
                        json={"related_ids": related}
                    )
                    response.raise_for_status()
                    print(f"Miniature correlate aggiornate per prodotto {current_id}: {related}")
        except Exception as e:
            print(f"Errore nell'aggiornamento delle miniature correlate: {e}")
    
    def upload_product_images(self, product_id, image_data, global_data):
        """Carica le immagini per un prodotto"""
        try:
            for sku, img_data in image_data.items():
                image_ids = []
                # Carica le immagini principali (1.jpg, 2.jpg, 3.jpg)
                for i in range(1, 4):
                    img_path = img_data.get(f"image_{i}")
                    if img_path and os.path.exists(img_path):
                        image_id = self.upload_image_to_media_library(img_path, sku, i)
                        if image_id:
                            image_ids.append((i-1, image_id))  # (position, id)
                # Aggiungi l'immagine del packaging come ultima
                packaging_image_id = self.find_packaging_image_in_media(global_data["Packaging"])
                if packaging_image_id:
                    image_ids.append((3, packaging_image_id))
                # Ordina per posizione e costruisci la lista images
                image_ids.sort(key=lambda x: x[0])
                images_payload = [{"id": img_id, "position": pos} for pos, img_id in image_ids]
                # Aggiorna il prodotto con le immagini
                if images_payload:
                    response = requests.put(
                        f"{self.api_url}/wc/v3/products/{product_id}",
                        auth=(self.consumer_key, self.consumer_secret),
                        json={"images": images_payload}
                    )
                    response.raise_for_status()
                    print(f"Immagini caricate per il prodotto {product_id}: {images_payload}")
                else:
                    print(f"Attenzione: Nessuna immagine caricata per il prodotto {product_id}")
        except Exception as e:
            print(f"Errore nel caricamento delle immagini per il prodotto {product_id}: {e}")
            print("Il prodotto è stato creato ma senza immagini. Puoi aggiungerle manualmente.")

    def upload_variation_images(self, variation_id, img_data, global_data):
        """Carica le immagini per una variante specifica"""
        try:
            image_ids = []
            for i in range(1, 4):
                img_path = img_data.get(f"image_{i}")
                if img_path and os.path.exists(img_path):
                    image_id = self.upload_image_to_media_library(img_path, img_data.get('sku', ''), i)
                    if image_id:
                        image_ids.append((i-1, image_id))
            packaging_image = self.get_packaging_image(global_data["Packaging"])
            if packaging_image:
                packaging_id = self.upload_image_to_media_library(packaging_image, img_data.get('sku', ''), 0)
                if packaging_id:
                    image_ids.append((3, packaging_id))
            image_ids.sort(key=lambda x: x[0])
            images_payload = [{"id": img_id, "position": pos} for pos, img_id in image_ids]
            if images_payload:
                response = requests.put(
                    f"{self.api_url}/wc/v3/products/variations/{variation_id}",
                    auth=(self.consumer_key, self.consumer_secret),
                    json={"images": images_payload}
                )
                response.raise_for_status()
        except Exception as e:
            print(f"Errore nel caricamento delle immagini per la variante {variation_id}: {e}")
    
    def create_product_description(self, global_data, color=None):
        """
        Crea la descrizione del prodotto come elenco puntato, tutto a sinistra.
        """
        brand = global_data.get("Brand", "")
        lunghezza = global_data.get("Lunghezza", "")
        larghezza = global_data.get("Larghezza", "")
        altezza = global_data.get("Altezza", "")
        peso = global_data.get("Peso", "")
        colore = color or ""

        elenco = f'''
        <ul style="list-style-type: disc; padding-left: 24px; text-align: left;">
            <li><strong>Brand:</strong> {brand}</li>
            <li><strong>Colore:</strong> {colore}</li>
            <li><strong>Dimensioni:</strong> {lunghezza} × {larghezza} × {altezza} cm</li>
            <li><strong>Peso:</strong> {peso} kg</li>
        </ul>
        '''
        return elenco
    
    def get_category_ids(self, categories_str):
        """Converte i nomi delle categorie in ID"""
        if not categories_str:
            return []
        
        category_names = [cat.strip() for cat in categories_str.split(",")]
        category_ids = []
        
        for name in category_names:
            for cat_id, cat_name in CATEGORY_NAMES.items():
                if cat_name.lower() == name.lower():
                    category_ids.append({"id": cat_id})
                    break
        
        return category_ids
    
    def get_tag_ids(self, tags_str):
        """Converte i nomi dei tag in ID"""
        if not tags_str:
            return []
        
        tag_names = [tag.strip() for tag in tags_str.split(",")]
        tag_ids = []
        
        for name in tag_names:
            for tag_id, tag_name in TAG_NAMES.items():
                if tag_name.lower() == name.lower():
                    tag_ids.append({"id": tag_id})
                    break
        
        return tag_ids
    
    def create_product_variations(self, product_id, image_data, global_data):
        """Crea le varianti del prodotto per ogni colore"""
        for sku, img_data in image_data.items():
            try:
                # Prepara i dati della variante
                variation_payload = {
                    "regular_price": global_data["Prezzo"],
                    "attributes": [
                        {
                            "id": 1,
                            "name": "Colore",
                            "option": img_data["color"]
                        }
                    ],
                    "sku": sku,
                    "manage_stock": False,
                    "stock_status": "instock"
                }
                
                # Crea la variante
                response = requests.post(
                    f"{self.api_url}/wc/v3/products/{product_id}/variations",
                    auth=(self.consumer_key, self.consumer_secret),
                    json=variation_payload
                )
                response.raise_for_status()
                variation = response.json()
                variation_id = variation["id"]
                
                # Carica le immagini per questa variante
                self.upload_variation_images(variation_id, img_data, global_data)
                
            except Exception as e:
                print(f"Errore nella creazione della variante {sku}: {e}")
    
    def upload_image_to_media_library(self, image_path, sku='', index=0):
        """Carica un'immagine nella libreria media di WordPress con nome unico"""
        try:
            # Verifica che il file esista
            if not os.path.exists(image_path):
                print(f"File non trovato: {image_path}")
                return None
            
            # Verifica le dimensioni del file
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                print(f"File vuoto: {image_path}")
                return None
            
            print(f"Caricamento immagine: {image_path} ({file_size} bytes)")
            
            with open(image_path, 'rb') as f:
                # Nome unico: SKU_indice_nomefile.jpg
                base_name = os.path.basename(image_path)
                unique_name = f"{sku}_{index}_{base_name}"
                files = {'file': (unique_name, f, 'image/jpeg')}
                
                # Usa autenticazione WordPress per l'endpoint media
                response = requests.post(
                    f"{self.api_url}/wp/v2/media",
                    auth=(WP_USERNAME, WP_APP_PASSWORD),
                    files=files
                )
                
                print(f"Risposta API: {response.status_code} - {response.text[:200]}")
                
                if response.status_code == 401:
                    print("Errore di autenticazione WordPress. Verificare username e password.")
                    return None
                
                response.raise_for_status()
                media_data = response.json()
                print(f"Immagine caricata con successo. ID: {media_data.get('id')}")
                return media_data["id"]
                
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine {image_path}: {e}")
            print(f"Tipo di errore: {type(e).__name__}")
            return None
    
    def get_packaging_image(self, packaging):
        """Restituisce il percorso dell'immagine del packaging appropriata"""
        if packaging.lower() == "medio":
            return "fantini-pelletteria-panno-protettivo-packaging1.jpg"
        elif packaging.lower() == "piccolo":
            return "fantini-pelletteria-packaging2.jpg"
        return None
    
    def test_authentication(self):
        """Testa l'autenticazione API"""
        try:
            # Test con endpoint prodotti (WooCommerce)
            response = requests.get(
                f"{self.api_url}/wc/v3/products",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": 1}
            )
            
            if response.status_code == 401:
                return False, "Errore di autenticazione WooCommerce per endpoint prodotti"
            
            # Test con endpoint media (WordPress)
            response = requests.get(
                f"{self.api_url}/wp/v2/media",
                auth=(WP_USERNAME, WP_APP_PASSWORD),
                params={"per_page": 1}
            )
            
            if response.status_code == 401:
                return False, "Errore di autenticazione WordPress per endpoint media"
            
            return True, "Autenticazione riuscita per entrambi gli endpoint"
            
        except Exception as e:
            return False, f"Errore nel test di autenticazione: {e}"
    
    def find_packaging_image_in_media(self, packaging):
        """Cerca l'immagine del packaging nella libreria media di WordPress"""
        try:
            packaging_filename = self.get_packaging_image(packaging)
            if not packaging_filename:
                return None
            
            # Cerca l'immagine nella libreria media usando autenticazione WordPress
            response = requests.get(
                f"{self.api_url}/wp/v2/media",
                auth=(WP_USERNAME, WP_APP_PASSWORD),
                params={"search": packaging_filename}
            )
            response.raise_for_status()
            media_items = response.json()
            
            for item in media_items:
                if packaging_filename.lower() in item.get("source_url", "").lower():
                    return item["id"]
            
            return None
            
        except Exception as e:
            print(f"Errore nella ricerca dell'immagine packaging: {e}")
            return None

# === MAIN ===
class ClickableLabel(QLabel):
    def __init__(self, text, step_index, parent=None):
        super().__init__(text, parent)
        self.step_index = step_index
        self.click_callback = None
    
    def set_click_callback(self, callback):
        self.click_callback = callback
    
    def mousePressEvent(self, event):
        if self.click_callback:
            self.click_callback(self.step_index)
        super().mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caricamento Prodotti")
        self.resize(1000, 800)
        self.current_step = 0
        self.total_steps = 8
        self.current_product_index = 0
        self.products_list = self.get_products_list()
        self.total_products = len(self.products_list)
        
        layout = QVBoxLayout()
        
        # Indicatore di progresso con pallini
        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(20, 10, 20, 10)
        self.step_indicators = []
        self.create_step_indicators()
        layout.addLayout(self.progress_layout)
        
        # Indicatore prodotto corrente
        self.product_info_layout = QHBoxLayout()
        self.product_info_layout.setContentsMargins(20, 5, 20, 5)
        self.product_label = QLabel(f"Prodotto {self.current_product_index + 1}/{self.total_products}")
        self.product_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.product_label.setStyleSheet("color: white;")
        self.product_info_layout.addWidget(self.product_label)
        self.product_info_layout.addStretch()
        layout.addLayout(self.product_info_layout)
        
        self.stack = QStackedWidget()

        self.step1 = StepOne()
        self.step2 = StepTwo()
        self.step3 = StepThree()
        self.step4 = StepFour()
        self.step5 = StepFive()
        self.step6 = StepSix()
        self.step7 = StepSeven(self.products_list[0] if self.products_list else None)
        self.step8 = StepEight(self.collect_data, self.step7.get_selected_data, self.products_list[0] if self.products_list else None)

        self.stack.addWidget(self.step1)
        self.stack.addWidget(self.step2)
        self.stack.addWidget(self.step3)
        self.stack.addWidget(self.step4)
        self.stack.addWidget(self.step5)
        self.stack.addWidget(self.step6)
        self.stack.addWidget(self.step7)
        self.stack.addWidget(self.step8)

        layout.addWidget(self.stack)
        self.setLayout(layout)

        # Connessioni per i pulsanti con aggiornamento dell'indicatore
        self.step1.btn_next.clicked.connect(lambda: self.go_to_step(1))
        self.step2.btn_back.clicked.connect(lambda: self.go_to_step(0))
        self.step2.btn_next.clicked.connect(lambda: self.go_to_step(2))
        self.step3.btn_back.clicked.connect(lambda: self.go_to_step(1))
        self.step3.btn_next.clicked.connect(self.check_category_selection)
        self.step4.btn_back.clicked.connect(lambda: self.go_to_step(2))
        self.step4.btn_next.clicked.connect(lambda: self.go_to_step(4))
        self.step5.btn_back.clicked.connect(lambda: self.go_to_step(3))
        self.step5.btn_next.clicked.connect(lambda: self.go_to_step(5))
        self.step6.btn_back.clicked.connect(lambda: self.go_to_step(4))
        self.step6.btn_next.clicked.connect(lambda: self.go_to_step(6))
        self.step7.btn_back.clicked.connect(lambda: self.go_to_step(5))
        self.step7.btn_next.clicked.connect(self.show_summary)
        self.step8.btn_back.clicked.connect(lambda: self.go_to_step(6))
        self.step8.btn_finish.clicked.connect(self.next_product_or_finish)
        self.step8.btn_upload.clicked.connect(self.upload_products)

    def create_step_indicators(self):
        for i in range(self.total_steps):
            indicator = ClickableLabel(str(i + 1), i)
            indicator.setFixedSize(30, 30)
            indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
            indicator.setStyleSheet("""
                QLabel {
                    background-color: #666666;
                    color: white;
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QLabel:hover {
                    background-color: #555555;
                    cursor: pointer;
                }
            """)
            # Rendi il pallino cliccabile
            indicator.set_click_callback(lambda step=i: self.go_to_step(step))
            self.step_indicators.append(indicator)
            self.progress_layout.addWidget(indicator)
            if i < self.total_steps - 1:
                # Aggiungi spazio tra i pallini
                spacer = QLabel()
                spacer.setFixedWidth(20)
                self.progress_layout.addWidget(spacer)
        
        # Centra i pallini
        self.progress_layout.addStretch()
        self.progress_layout.insertStretch(0)
        
        # Inizializza il primo step come attivo
        self.update_step_indicators(0)

    def update_step_indicators(self, current_step):
        self.current_step = current_step
        for i, indicator in enumerate(self.step_indicators):
            if i <= current_step:
                # Step corrente e completati: colore #0099A8
                indicator.setStyleSheet("""
                    QLabel {
                        background-color: #0099A8;
                        color: white;
                        border-radius: 15px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QLabel:hover {
                        background-color: #007d8a;
                        cursor: pointer;
                    }
                """)
            else:
                # Step futuri: colore grigio scuro
                indicator.setStyleSheet("""
                    QLabel {
                        background-color: #666666;
                        color: white;
                        border-radius: 15px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QLabel:hover {
                        background-color: #555555;
                        cursor: pointer;
                    }
                """)

    def go_to_step(self, step_index):
        # Se stiamo andando allo Step 6, passa la categoria primaria
        if step_index == 5:  # Step 6 (indice 5)
            categories, primary = self.step3.get_selected_categories()
            if primary:
                primary_name = CATEGORY_NAMES.get(primary, str(primary))
                self.step6.set_categories(categories)
        
        self.stack.setCurrentIndex(step_index)
        self.update_step_indicators(step_index)

    def check_category_selection(self):
        selected, primary = self.step3.get_selected_categories()
        if not selected or primary is None:
            QMessageBox.warning(self, "Attenzione", "Devi selezionare almeno una categoria e impostarne una come primaria.")
        else:
            self.go_to_step(3)

    def show_summary(self):
        self.step8.load_summary()
        self.go_to_step(7)

    def collect_data(self):
        name = self.step1.input.text()
        brand = "B2B" if self.step2.b2b_selected else self.step2.combo.currentText()
        brand_id = self.step2.combo.currentData() if not self.step2.b2b_selected else None
        categories, primary = self.step3.get_selected_categories()
        tags = self.step4.get_selected_tags()
        packaging = self.step5.get_packaging()
        order_pos = self.step6.get_visibility_position()

        cat_names = [CATEGORY_NAMES.get(cid, str(cid)) for cid in categories]
        primary_name = CATEGORY_NAMES.get(primary, str(primary))
        tag_names = [TAG_NAMES.get(tid, str(tid)) for tid in tags]

        return {
            "Nome prodotto": name,
            "Brand": brand,
            "Brand_ID": brand_id,
            "Categorie selezionate": ", ".join(cat_names),
            "Categoria primaria": primary_name,
            "Tag selezionati": ", ".join(tag_names),
            "Packaging": packaging or "Nessuno",
            "Posizione visibilità": order_pos
        }

    def get_products_list(self):
        """Ottiene la lista delle cartelle prodotto dalla directory"""
        products = []
        try:
            for item in os.listdir(PRODUCTS_DIR):
                item_path = os.path.join(PRODUCTS_DIR, item)
                if os.path.isdir(item_path):
                    products.append(item)
        except Exception as e:
            print(f"Errore nel caricamento dei prodotti: {e}")
        return sorted(products)

    def update_product_info(self):
        """Aggiorna l'indicatore del prodotto corrente"""
        if self.current_product_index < self.total_products:
            self.product_label.setText(f"Prodotto {self.current_product_index + 1}/{self.total_products}")
        else:
            self.product_label.setText("Tutti i prodotti completati!")

    def next_product_or_finish(self):
        """Passa al prodotto successivo o termina se tutti i prodotti sono completati"""
        self.current_product_index += 1
        if self.current_product_index < self.total_products:
            # Reset per il prossimo prodotto
            self.reset_for_next_product()
            self.go_to_step(0)  # Torna al primo step
        else:
            # Tutti i prodotti completati
            QMessageBox.information(self, "Completato", "Tutti i prodotti sono stati processati!")
            self.close()

    def reset_for_next_product(self):
        # Reset Step 1
        self.step1.input.clear()
        self.step1.dropdown.setCurrentIndex(0)
        
        # Reset Step 2
        self.step2.b2b_selected = False
        self.step2.combo.setCurrentIndex(-1)
        self.step2.aggiorna_stile_b2b(False)
        
        # Reset Step 3
        for checkbox, (cat_id, radio) in self.step3.selected_categories.items():
            checkbox.setChecked(False)
            radio.setChecked(False)
        
        # Reset Step 4
        for checkbox in self.step4.selected_tags:
            checkbox.setChecked(False)
        
        # Reset Step 5
        for btn in self.step5.packaging_buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0099A8; color: white;
                    font-size: 14px; padding: 10px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #007d8a;
                }
            """)
        
        # Reset Step 6
        self.step6.spinbox.setValue(1)
        self.step6.primary_category_id = None
        self.step6.primary_category_name = None
        # Rimosso: self.step6.category_info_label.setText("")
        # Rimosso: self.step6.clear_positions_table()
        # Rimosso: self.step6.suggestions_label.setText("")
        
        # Reset Step 7
        self.step7.selected_data.clear()
        while self.step7.images_layout.count():
            child = self.step7.images_layout.takeAt(0)
            widget = child.widget()
            if widget:
                widget.deleteLater()
        self.step7.table_selections.setRowCount(0)
        
        # Aggiorna l'indicatore del prodotto
        self.update_product_info()

    def upload_products(self):
        """Carica i prodotti su WooCommerce"""
        try:
            # Raccogli i dati globali
            global_data = self.collect_data()
            
            # Aggiungi i dati estratti dalla cartella
            folder_data = self.step8.extract_global_data_from_folder()
            global_data.update(folder_data)
            
            # Raccogli i dati delle immagini
            image_data = self.step7.get_selected_data()
            
            if not image_data:
                QMessageBox.warning(self, "Attenzione", "Nessuna immagine selezionata. Seleziona almeno un'immagine prima di procedere.")
                return
            
            # Prepara i dati delle immagini con i percorsi completi
            processed_image_data = {}
            current_product = self.products_list[self.current_product_index]
            prodotto_path = os.path.join(PRODUCTS_DIR, current_product)
            
            for img_path, img_info in image_data.items():
                # Estrai SKU dal path dell'immagine
                sku = os.path.basename(os.path.dirname(img_path))
                
                # Trova tutte le immagini per questo SKU
                sku_path = os.path.join(prodotto_path, sku)
                if os.path.isdir(sku_path):
                    # Cerca le immagini 1.jpg, 2.jpg, 3.jpg, ecc.
                    for i in range(1, 10):
                        img_file = f"{i}.jpg"
                        img_full_path = os.path.join(sku_path, img_file)
                        if os.path.exists(img_full_path):
                            img_info[f"image_{i}"] = img_full_path
                
                processed_image_data[sku] = img_info
            
            # Conferma il caricamento
            reply = QMessageBox.question(
                self, 
                "Conferma Caricamento", 
                f"Stai per caricare il prodotto '{global_data['Nome prodotto']}' con {len(processed_image_data)} varianti.\n\nProcedere?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Crea l'uploader e testa l'autenticazione
                uploader = ProductUploader(API_URL, CONSUMER_KEY, CONSUMER_SECRET)
                
                # Testa l'autenticazione prima di procedere
                auth_success, auth_message = uploader.test_authentication()
                if not auth_success:
                    QMessageBox.critical(
                        self, 
                        "Errore di Autenticazione", 
                        f"Impossibile connettersi al sito:\n{auth_message}\n\nVerificare le credenziali API."
                    )
                    return
                
                # Carica il prodotto
                product_id = uploader.upload_product(None, processed_image_data, global_data)
                
                # Verifica se ci sono stati problemi con le immagini
                if product_id:
                    QMessageBox.information(
                        self, 
                        "Caricamento Completato", 
                        f"Prodotto caricato con successo!\nID Prodotto: {product_id}\n\nIl prodotto è ora disponibile sul sito con tutte le immagini caricate automaticamente."
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Caricamento Parziale",
                        "Il prodotto è stato creato ma ci sono stati problemi con il caricamento delle immagini.\n\nPuoi aggiungere le immagini manualmente dalla libreria media di WordPress."
                    )
                
                # Passa al prodotto successivo
                self.next_product_or_finish()
                
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante il caricamento del prodotto:\n{str(e)}")

if __name__ == '__main__':
    preload_category_and_tag_names()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
