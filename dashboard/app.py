from flask import Flask, render_template, redirect, url_for, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'qualcosa-di-sicuro'  # Necessario per i messaggi flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run/photoroom')
def run_photoroom():
    subprocess.Popen(['python', 'Applicazione per Scontornare PhotoRoom.py'], cwd=os.path.dirname(__file__))
    flash('PhotoRoom avviato con successo')
    return redirect(url_for('index'))

@app.route('/run/scontornare')
def run_scontornare():
    subprocess.Popen(['python', 'Applicazione per Scontornare.py'], cwd=os.path.dirname(__file__))
    flash('Applicazione per Scontornare avviata')
    return redirect(url_for('index'))

@app.route('/run/shooting')
def run_shooting():
    subprocess.Popen(['python', 'Riepilogo Shooting.py'], cwd=os.path.dirname(__file__))
    flash('Riepilogo Shooting avviato')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
