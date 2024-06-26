from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup as bs
import re
import traceback
from markupsafe import escape

app = Flask(__name__)


def formatear_palabra(palabra):
    palabra = palabra.lower()
    palabra = palabra.replace(" ", "-")
    resultado = f"{palabra}#D[A:{palabra}]"
    return resultado


def limpiar_texto(texto):
    return re.sub(r'\s+', ' ', texto.strip())


def obtener_productos(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = bs(response.content, "html.parser")

        productos = []
        contenedores_tarjetas = soup.find_all(
            "li", class_="ui-search-layout__item")[:20]

        for tarjeta in contenedores_tarjetas:
            nombre_producto_elemento = tarjeta.select_one(
                "div.ui-search-result__content-wrapper > div.ui-search-item__group.ui-search-item__group--title > a.ui-search-item__group__element.ui-search-link"
            )
            nombre_producto = limpiar_texto(
                nombre_producto_elemento.text) if nombre_producto_elemento else "No disponible"

            precio_elemento = tarjeta.select_one(
                "span.andes-money-amount__fraction")
            precio = limpiar_texto(
                precio_elemento.text).replace(',', '') if precio_elemento else "0"

            enlace_producto = nombre_producto_elemento['href'] if nombre_producto_elemento else "#"

            productos.append({
                "nombre": nombre_producto,
                "precio": float(precio),
                "enlace": enlace_producto
            })

        return productos
    except Exception as e:
        traceback.print_exc()
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palabra = escape(request.form['palabra'])
        return redirect(url_for('result', palabra=palabra))

    return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    palabra = escape(request.args.get('palabra', ''))
    orden = request.args.get('orden', 'relevancia')
    busqueda = formatear_palabra(palabra)
    url = "https://listado.mercadolibre.com.mx/" + busqueda

    productos = obtener_productos(url)

    if not productos:
        error_message = "Hubo un problema al obtener los datos. Por favor, intenta nuevamente."
        return render_template('index.html', error=error_message)

    if orden == 'precio_asc':
        productos = sorted(productos, key=lambda x: x['precio'])
    elif orden == 'precio_desc':
        productos = sorted(productos, key=lambda x: x['precio'], reverse=True)

    return render_template('result.html', productos=productos, palabra=palabra, orden=orden)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
