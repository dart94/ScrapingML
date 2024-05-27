from flask import Flask, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import traceback

app = Flask(__name__)


def formatear_palabra(palabra):
    palabra = palabra.lower()
    palabra = palabra.replace(" ", "-")
    resultado = f"{palabra}#D[A:{palabra}]"
    return resultado


def limpiar_texto(texto):
    return re.sub(r'\s+', ' ', texto.strip())


def obtener_tabla(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        contenido = response.text
        soup = bs(contenido, "html.parser")

        productos = []
        precios = []

        contenedores_tarjetas = soup.find_all(
            # Limita a 10 resultados
            "li", class_="ui-search-layout__item")[:10]
        for tarjeta in contenedores_tarjetas:
            nombre_producto_elemento = tarjeta.select_one(
                "div.ui-search-result__content-wrapper > div.ui-search-item__group.ui-search-item__group--title > a.ui-search-item__group__element.ui-search-link"
            )
            nombre_producto = limpiar_texto(
                nombre_producto_elemento.text) if nombre_producto_elemento else "No disponible"
            productos.append(nombre_producto)

            precio_elemento = tarjeta.select_one(
                "span.andes-money-amount__fraction")
            precio = limpiar_texto(
                precio_elemento.text) if precio_elemento else "No disponible"
            precios.append(precio)

        df = pd.DataFrame({"Producto": productos, "Precio": precios})
        return df
    except Exception as e:
        traceback.print_exc()
        return pd.DataFrame({"Producto": ["Error"], "Precio": ["Error"]})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palabra = request.form['palabra']
        busqueda = formatear_palabra(palabra)
        url = "https://listado.mercadolibre.com.mx/" + busqueda

        df = obtener_tabla(url)

        return render_template('result.html', tables=df.to_html(classes='table table-striped', header="true", index=False))

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
