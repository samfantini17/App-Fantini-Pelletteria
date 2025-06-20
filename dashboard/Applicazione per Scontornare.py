import os
import threading
import time
from tkinter import Tk, Label, Button, StringVar, Text, END
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
    image.thumbnail((max_size, max_size), Image.LANCZOS)
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
        return

    inizio_totale = time.time()
    for i, filename in enumerate(files, start=1):
        inizio = time.time()
        titolo.set(f"🟦 Elaborazione immagine {i} di {totale}")
        stato.set(f"In corso: {filename}")
        root.update()

        input_path = os.path.join(input_folder, filename)
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

    tempo_totale = time.time() - inizio_totale
    titolo.set("🎉 Elaborazione completata!")
    stato.set(f"{totale} immagini elaborate in {tempo_totale:.2f} secondi.")
    mostra_risultati(risultati, tempo_totale)

# Mostra riepilogo finale
def mostra_risultati(risultati, tempo_totale):
    testo_risultati.config(state='normal')
    testo_risultati.delete(1.0, END)
    testo_risultati.insert(END, f"🧾 Riepilogo elaborazione ({len(risultati)} immagini):\n")
    for riga in risultati:
        testo_risultati.insert(END, f"• {riga}\n")
    testo_risultati.insert(END, f"\n⏱ Tempo totale: {tempo_totale:.2f} secondi")
    testo_risultati.config(state='disabled')

# Thread per non bloccare la GUI
def avvia_elaborazione_thread():
    threading.Thread(target=elabora_immagini).start()

# GUI
root = Tk()
root.title("Scontornamento Immagini")
root.geometry("500x500")
root.configure(bg="#f4f4f4")

titolo = StringVar()
titolo.set("✨ Pronto per iniziare")
stato = StringVar()
stato.set("")

# Etichetta grande (conteggio)
Label(root, textvariable=titolo, font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#1e90ff").pack(pady=(20, 5))

# Stato (nome file e tempo)
Label(root, textvariable=stato, font=("Arial", 11), bg="#f4f4f4", fg="#333", wraplength=480).pack()

# Bottone (aggiornato con stile azzurro)
Button(root,
       text="Avvia Elaborazione",
       font=("Arial", 12, "bold"),
       bg="#33CCCC",
       fg="white",
       activebackground="#2ab3b3",
       activeforeground="white",
       width=22,
       height=2,
       bd=0,
       relief="flat",
       command=avvia_elaborazione_thread).pack(pady=15)


# Box per riepilogo
testo_risultati = Text(root, height=12, width=60, font=("Courier New", 9), bg="white", fg="#333", state="disabled", wrap="none")
testo_risultati.pack(pady=10)

root.mainloop()
