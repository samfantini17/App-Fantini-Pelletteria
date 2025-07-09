import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict

class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generatore Report Foto Borse")
        self.root.geometry("500x300")
        self.root.configure(bg="white")

        self.selected_folder = ""

        self.title_label = tk.Label(
            root,
            text="Seleziona la cartella delle immagini",
            font=("Arial", 16),
            bg="white"
        )
        self.title_label.pack(pady=20)

        self.select_button = tk.Button(
            root,
            text="Sfoglia Cartella",
            command=self.select_folder,
            font=("Arial", 12),
            bg="#33CCCC",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground="#2ab3b3",
            activeforeground="white"
        )
        self.select_button.pack()

        self.status_label = tk.Label(
            root,
            text="",
            font=("Arial", 12),
            bg="white"
        )
        self.status_label.pack(pady=10)

        self.stats_text = tk.Text(
            root,
            height=8,
            width=60,
            font=("Courier", 10),
            bg="white"
        )
        self.stats_text.pack(pady=10)
        self.stats_text.config(state=tk.DISABLED)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Seleziona la cartella principale delle immagini")
        if folder:
            self.selected_folder = folder
            self.status_label.config(text="Cartella selezionata: " + folder)
            self.generate_report()

    def generate_report(self):
        root_dir = self.selected_folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(script_dir, "report_foto_borse.csv")

        image_extensions = (".jpg", ".jpeg", ".png", ".webp")
        dati_foto = []
        non_conformi_count = 0

        categorie = set()
        prodotti_per_categoria = defaultdict(set)
        colori_per_categoria = defaultdict(set)
        foto_per_categoria_prodotto = defaultdict(int)

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(image_extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)
                    path_parts = rel_path.split(os.sep)

                    livello_1 = path_parts[0] if len(path_parts) > 0 else ""
                    livello_2 = path_parts[1] if len(path_parts) > 1 else ""
                    livello_3 = path_parts[2] if len(path_parts) > 2 else ""
                    livello_4 = path_parts[3] if len(path_parts) > 3 else ""

                    nome_file = os.path.splitext(file)[0].strip()
                    conforme = nome_file in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

                    if not conforme:
                        non_conformi_count += 1

                    dati_foto.append([
                        livello_1, livello_2, livello_3, livello_4,
                        file, "Sì" if conforme else "No", file_path
                    ])

                    categorie.add(livello_1)
                    prodotti_per_categoria[livello_1].add(livello_2)
                    colori_per_categoria[livello_1].add(livello_3)
                    foto_per_categoria_prodotto[(livello_1, livello_2)] += 1

        if dati_foto:
            with open(output_csv, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Livello 1", "Livello 2", "Livello 3", "Livello 4",
                    "Nome file", "Conforme (1/2/3)", "Percorso completo"
                ])
                writer.writerows(dati_foto)

            # Statistiche compatte
            total_categorie = len(categorie)
            total_prodotti = sum(len(prodotti) for prodotti in prodotti_per_categoria.values())
            total_colori = sum(len(colori) for colori in colori_per_categoria.values())
            total_foto = len(dati_foto)

            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, f"Categorie (Livello 1): {total_categorie}\n")
            self.stats_text.insert(tk.END, f"Prodotti (Livello 2): {total_prodotti}\n")
            self.stats_text.insert(tk.END, f"Colori (Livello 3): {total_colori}\n")
            self.stats_text.insert(tk.END, f"Foto totali (Livello 4): {total_foto}\n")
            self.stats_text.insert(tk.END, f"Foto non conformi: {non_conformi_count}\n")
            self.stats_text.config(state=tk.DISABLED)

            messagebox.showinfo("Report generato", f"Report CSV generato con successo:\n{output_csv}")
        else:
            messagebox.showwarning("Nessuna immagine trovata", "Non sono state trovate immagini nella cartella selezionata.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()
