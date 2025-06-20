from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run/scontornare')
def run_scontornare():
    subprocess.Popen(['python', 'Applicazione per Scontornare.py'], cwd=os.path.dirname(__file__))
    return 'Applicazione per Scontornare avviata'

@app.route('/run/shooting')
def run_shooting():
    subprocess.Popen(['python', 'Riepilogo Shooting.py'], cwd=os.path.dirname(__file__))
    return 'Riepilogo Shooting avviato'

if __name__ == '__main__':
    app.run(debug=True)
