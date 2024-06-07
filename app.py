from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def buscar_productos(palabra):
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={palabra}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        productos = [{
            'nombre': item['title'],
            'precio': item['price'],
            'enlace': item['permalink']
        } for item in data['results']]
        return productos
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palabra = request.form.get('palabra')
        if palabra:
            return redirect(url_for('result', palabra=palabra))
        else:
            error = "Por favor ingresa una palabra clave para buscar."
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/result/<palabra>', methods=['GET'])
def result(palabra):
    try:
        productos = buscar_productos(palabra)
        if productos is not None:
            return render_template('result.html', productos=productos)
        else:
            error = "Error al buscar productos. Por favor intenta nuevamente."
            return render_template('index.html', error=error)
    except Exception as e:
        error = f"Se produjo un error: {e}"
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
