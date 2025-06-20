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

# Cartelle principali
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
input_master = os.path.join(desktop, "Immagini B2B")
output_master = os.path.join(desktop, "Immagini B2B finali")
os.makedirs(output_master, exist_ok=True)

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
    risultati = []
    totale = 0
    inizio_totale = time.time()

    for root_dir, _, files in os.walk(input_master):
        for filename in files:
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            totale += 1
            input_path = os.path.join(root_dir, filename)
            relative_path = os.path.relpath(root_dir, input_master)
            output_dir = os.path.join(output_master, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            output_jpg_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg')

            inizio = time.time()
            titolo.set(f"🟦 Elaborazione immagine {totale}")
            stato.set(f"In corso: {filename}")
            root.update()

            try:
                with open(input_path, 'rb') as f:
                    input_data = f.read()

                output_data = remove(input_data, **ALPHA_MATTING_PARAMS)
                image_no_bg = Image.open(BytesIO(output_data)).convert('RGBA')
                cropped = crop_to_content(image_no_bg)
                cleaned = clean_edges(cropped)
                resized = resize_image(cleaned)

                background = Image.new('RGBA', (1200, 1200), (255, 255, 255, 255))
                offset = ((1200 - resized.width) // 2, (1200 - resized.height) // 2)
                background.paste(resized, offset, resized)

                final_image = background.convert('RGB')
                final_image.save(output_jpg_path, 'JPEG', quality=95)

                durata = time.time() - inizio
                stato.set(f"✅ Completata in {durata:.2f} sec: {filename}")
                risultati.append(f"{filename} – {durata:.2f} sec")
                root.update()
            except Exception as e:
                risultati.append(f"{filename} – Errore: {str(e)}")

    tempo_totale = time.time() - inizio_totale
    titolo.set("🎉 Elaborazione completata!")
    stato.set(f"{totale} immagini elaborate in {tempo_totale:.2f} secondi.")
    mostra_risultati(risultati, tempo_totale)

# Mostra riepilogo
def mostra_risultati(risultati, tempo_totale):
    testo_risultati.config(state='normal')
    testo_risultati.delete(1.0, END)
    testo_risultati.insert(END, f"🧾 Riepilogo elaborazione ({len(risultati)} immagini):\n")
    for riga in risultati:
        testo_risultati.insert(END, f"• {riga}\n")
    testo_risultati.insert(END, f"\n⏱ Tempo totale: {tempo_totale:.2f} secondi")
    testo_risultati.config(state='disabled')

# Thread GUI
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

Label(root, textvariable=titolo, font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#1e90ff").pack(pady=(20, 5))
Label(root, textvariable=stato, font=("Arial", 11), bg="#f4f4f4", fg="#333", wraplength=480).pack()

Button(root,
       text="Avvia Elaborazione",
       font=("Arial", 12, "bold"),
       bg="#1e90ff",
       fg="white",
       activebackground="#1c86ee",
       activeforeground="white",
       width=22,
       height=2,
       bd=0,
       relief="flat",
       command=avvia_elaborazione_thread).pack(pady=15)

testo_risultati = Text(root, height=12, width=60, font=("Courier New", 9), bg="white", fg="#333", state="disabled", wrap="none")
testo_risultati.pack(pady=10)

root.mainloop()
