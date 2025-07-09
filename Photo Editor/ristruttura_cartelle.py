import os
import shutil

# Percorsi iniziali e finali
source_root = r"C:\Users\fanti\Desktop\Foto\MASTER Foto Prodotti"
destination_root = r"C:\Users\fanti\Desktop\Foto\Master Foto Prodotti NEW"

def process_master_folder(source_root, destination_root):
    # Crea la cartella di destinazione se non esiste
    if not os.path.exists(destination_root):
        os.makedirs(destination_root)

    # Scorre tutte le categorie merceologiche
    for category in os.listdir(source_root):
        category_path = os.path.join(source_root, category)
        if not os.path.isdir(category_path):
            continue

        # Crea la cartella della categoria nella nuova struttura
        new_category_path = os.path.join(destination_root, category)
        os.makedirs(new_category_path, exist_ok=True)

        # Scorre i prodotti
        for product_folder in os.listdir(category_path):
            product_path = os.path.join(category_path, product_folder)
            if not os.path.isdir(product_path):
                continue

            try:
                # NomeInterno-Prezzo-Dimensioni-Packaging
                nome_interno, prezzo, dimensioni, packaging = product_folder.split("-")
            except ValueError:
                print(f"⚠️ Nome non conforme: {product_folder}")
                continue

            # Nuovo nome: NomeInterno+Prezzo+Dimensioni+0 (peso fisso a 0)
            new_product_folder_name = f"{nome_interno}+{prezzo}+{dimensioni}+0"
            new_product_path = os.path.join(new_category_path, new_product_folder_name)
            os.makedirs(new_product_path, exist_ok=True)

            # Scorre le varianti colore
            for variant_folder in os.listdir(product_path):
                variant_path = os.path.join(product_path, variant_folder)
                if not os.path.isdir(variant_path):
                    continue

                try:
                    # ColoreIt-ColoreEn-SKU
                    _, _, sku = variant_folder.split("-")
                except ValueError:
                    print(f"⚠️ Variante non conforme: {variant_folder}")
                    continue

                # Crea cartella SKU
                sku_folder_path = os.path.join(new_product_path, sku)
                os.makedirs(sku_folder_path, exist_ok=True)

                # Copia le immagini
                for image in os.listdir(variant_path):
                    image_path = os.path.join(variant_path, image)
                    if os.path.isfile(image_path):
                        shutil.copy(image_path, sku_folder_path)

# Esecuzione
process_master_folder(source_root, destination_root)
print("✅ Completato: la nuova struttura è stata creata in:")
print(destination_root)
