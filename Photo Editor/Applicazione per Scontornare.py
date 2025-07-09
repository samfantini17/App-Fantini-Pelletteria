import os
import threading
import time
from tkinter import Tk, Label, Button, StringVar, Text, END, Frame, ttk, DoubleVar
from PIL import Image, ImageEnhance
from rembg import remove
from io import BytesIO

# PARAMETRI ALPHA MATTING OTTIMIZZATI
ALPHA_MATTING_PARAMS = {
    'alpha_matting': True,
    'alpha_matting_foreground_threshold': 240,
    'alpha_matting_background_threshold': 10,
    'alpha_matting_erode_size': 5,
    'alpha_matting_base_size': 800
}

# Cartelle
input_folder = '2_da_scontornare'
output_scontornate = '3_ridimensionate_scontornate'
output_finali = '4_finali'

os.makedirs(output_scontornate, exist_ok=True)
os.makedirs(output_finali, exist_ok=True)

# Funzioni di elaborazione
def crop_to_content(image):
    bbox = image.getbbox()
    return image.crop(bbox) if bbox else image

def resize_image(image, max_size=1000):
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def clean_edges(image):
    r, g, b, a = image.split()
    r = ImageEnhance.Brightness(r).enhance(1.05)
    g = ImageEnhance.Brightness(g).enhance(1.05)
    b = ImageEnhance.Brightness(b).enhance(1.05)
    return Image.merge("RGBA", (r, g, b, a))

# Elaborazione immagini
def elabora_immagini():
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    totale = len(files)
    risultati = []

    if totale == 0:
        stato.set("⚠️ Nessuna immagine da elaborare.")
        progress_var.set(0)
        return

    inizio_totale = time.time()
    for i, filename in enumerate(files, start=1):
        inizio = time.time()
        progress = (i / totale) * 100
        progress_var.set(progress)
        titolo.set(f"🔄 Elaborazione immagine {i} di {totale}")
        stato.set(f"In corso: {filename}")
        root.update()

        input_path = os.path.join(input_folder, filename)
        try:
            with open(input_path, 'rb') as f:
                input_data = f.read()

            output_data = remove(input_data, **ALPHA_MATTING_PARAMS)
            image_no_bg = Image.open(BytesIO(output_data)).convert('RGBA')
            cropped = crop_to_content(image_no_bg)
            cleaned = clean_edges(cropped)
            resized = resize_image(cleaned)

            output_png = os.path.join(output_scontornate, os.path.splitext(filename)[0] + '.png')
            resized.save(output_png, 'PNG')

            background = Image.new('RGBA', (1200, 1200), (255, 255, 255, 255))
            offset = ((1200 - resized.width) // 2, (1200 - resized.height) // 2)
            background.paste(resized, offset, resized)

            final_image = background.convert('RGB')
            output_jpg = os.path.join(output_finali, os.path.splitext(filename)[0] + '.jpg')
            final_image.save(output_jpg, 'JPEG', quality=95)

            fine = time.time()
            durata = fine - inizio
            stato.set(f"✅ Completata in {durata:.2f} secondi: {filename}")
            risultati.append(f"{filename} – {durata:.2f} secondi")
            root.update()
        except Exception as e:
            stato.set(f"❌ Errore su {filename}: {str(e)}")
            continue

    tempo_totale = time.time() - inizio_totale
    progress_var.set(100)
    titolo.set("🎉 Elaborazione completata!")
    stato.set(f"{totale} immagini elaborate in {tempo_totale:.2f} secondi.")
    mostra_risultati(risultati, tempo_totale)

# Mostra riepilogo finale
def mostra_risultati(risultati, tempo_totale):
    testo_risultati.config(state='normal')
    testo_risultati.delete(1.0, END)
    testo_risultati.insert(END, f"📋 Riepilogo elaborazione ({len(risultati)} immagini):\n")
    testo_risultati.insert(END, "=" * 50 + "\n")
    for riga in risultati:
        testo_risultati.insert(END, f"• {riga}\n")
    testo_risultati.insert(END, "=" * 50 + "\n")
    testo_risultati.insert(END, f"⏱ Tempo totale: {tempo_totale:.2f} secondi\n")
    testo_risultati.insert(END, f"📁 Immagini salvate in: {output_finali}")
    testo_risultati.config(state='disabled')

# Thread per non bloccare la GUI
def avvia_elaborazione_thread():
    avvia_btn.config(state='disabled')
    elabora_immagini()
    avvia_btn.config(state='normal')

# GUI
root = Tk()
root.title("Scontornamento Immagini - Rembg")
root.geometry("600x500")
root.configure(bg="#f8f9fa")
root.resizable(False, False)

# Stile moderno
style = ttk.Style()
style.theme_use('clam')
style.configure("Custom.Horizontal.TProgressbar", 
               troughcolor="#e9ecef", 
               background="#007bff", 
               bordercolor="#007bff")

# Container principale
main_frame = Frame(root, bg="#f8f9fa", padx=20, pady=20)
main_frame.pack(fill='both', expand=True)

# Header
header_frame = Frame(main_frame, bg="#f8f9fa")
header_frame.pack(fill='x', pady=(0, 20))

Label(header_frame, 
      text="✂️ Scontornamento Immagini", 
      font=("Segoe UI", 20, "bold"), 
      bg="#f8f9fa", 
      fg="#212529").pack()

Label(header_frame, 
      text="Rimuove automaticamente lo sfondo dalle immagini", 
      font=("Segoe UI", 11), 
      bg="#f8f9fa", 
      fg="#6c757d").pack(pady=(3, 0))

# Contenuto principale
content_frame = Frame(main_frame, bg="#f8f9fa")
content_frame.pack(fill='both', expand=True)

# Sezione stato
status_frame = Frame(content_frame, bg="white", relief="flat", bd=1)
status_frame.pack(fill='x', pady=(0, 20))

status_inner = Frame(status_frame, bg="white", padx=15, pady=15)
status_inner.pack(fill='x')

titolo = StringVar()
titolo.set("✨ Pronto per iniziare")
stato = StringVar()
stato.set("Inserisci le immagini nella cartella 'Da scontornare' e clicca Avvia")

Label(status_inner, 
      textvariable=titolo, 
      font=("Segoe UI", 14, "bold"), 
      bg="white", 
      fg="#007bff").pack(anchor='w')

Label(status_inner, 
      textvariable=stato, 
      font=("Segoe UI", 10), 
      bg="white", 
      fg="#495057",
      wraplength=500).pack(anchor='w', pady=(3, 0))

# Progress bar
progress_frame = Frame(content_frame, bg="#f8f9fa")
progress_frame.pack(fill='x', pady=(0, 20))

progress_var = DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, 
                              variable=progress_var, 
                              maximum=100, 
                              style="Custom.Horizontal.TProgressbar",
                              length=500)
progress_bar.pack()

# Bottone con bordi arrotondati
button_frame = Frame(content_frame, bg="#f8f9fa")
button_frame.pack(pady=(0, 20))

# Frame per simulare bordi arrotondati
rounded_frame = Frame(button_frame, bg="#007bff", padx=3, pady=3)
rounded_frame.pack()

avvia_btn = Button(rounded_frame,
                   text="🚀 Avvia Elaborazione",
                   font=("Segoe UI", 12, "bold"),
                   bg="#007bff",
                   fg="white",
                   activebackground="#0056b3",
                   activeforeground="white",
                   width=20,
                   height=2,
                   bd=0,
                   relief="flat",
                   cursor="hand2",
                   command=avvia_elaborazione_thread)
avvia_btn.pack()

# Risultati
results_frame = Frame(content_frame, bg="white", relief="flat", bd=1)
results_frame.pack(fill='both', expand=True)

results_header = Frame(results_frame, bg="#f8f9fa", padx=15, pady=10)
results_header.pack(fill='x')

Label(results_header, 
      text="📊 Risultati Elaborazione", 
      font=("Segoe UI", 12, "bold"), 
      bg="#f8f9fa", 
      fg="#495057").pack(anchor='w')

testo_risultati = Text(results_frame, 
                       height=10, 
                       width=60, 
                       font=("Consolas", 9), 
                       bg="white", 
                       fg="#212529", 
                       state="disabled", 
                       wrap="word",
                       padx=15,
                       pady=10,
                       relief="flat",
                       bd=0)
testo_risultati.pack(fill='both', expand=True, padx=15, pady=(0, 15))

root.mainloop()
