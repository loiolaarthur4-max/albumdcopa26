from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_csv('album.csv')
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/update', methods=['POST'])
def update():
    # Lógica para salvar a figurinha como "tenho" no CSV
    return "Atualizado!"

if __name__ == '__main__':
    app.run(debug=True)
