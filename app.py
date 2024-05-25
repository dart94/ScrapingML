from flask import Flask, request, render_template
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


def buscar_producto(palabra_clave):
    return palabra_clave


def formatear_palabra(palabra):
    palabra = palabra.lower()
    palabra = palabra.replace(" ", "-")
    resultado = f"{palabra}#D[A:{palabra}]"
    return resultado


def obtener_tabla(url, driver):
    driver.get(url)
    tabla_presente = EC.presence_of_element_located(
        (By.CSS_SELECTOR, "li.ui-search-layout__item"))
    WebDriverWait(driver, 5).until(tabla_presente)

    Producto = []
    Precio = []

    contenido = driver.page_source
    soup = bs(contenido, "html.parser")

    contenedores_tarjetas = soup.find_all(
        "li", class_="ui-search-layout__item")
    for tarjeta in contenedores_tarjetas:
        nombre_producto_elemento = tarjeta.select_one(
            "div.ui-search-result__content-wrapper > div.ui-search-item__group.ui-search-item__group--title > a.ui-search-item__group__element.ui-search-link")
        nombre_producto = nombre_producto_elemento.text.strip(
        ) if nombre_producto_elemento else "No disponible"
        Producto.append(nombre_producto)

        precio_elemento = tarjeta.select_one(
            "div.ui-search-result__content-wrapper > div.ui-search-result__content-columns > div.ui-search-result__content-column.ui-search-result__content-column--left > div.ui-search-item__group.ui-search-item__group--price.ui-search-item__group--price-grid-container > div > div > div > span.andes-money-amount.ui-search-price__part.ui-search-price__part--medium.andes-money-amount--cents-superscript > span.andes-money-amount__fraction")
        precio = precio_elemento.text.strip() if precio_elemento else "No disponible"
        Precio.append(precio)

    df = pd.DataFrame({"Producto": Producto, "Precio": Precio})
    return df


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palabra = request.form['palabra']
        busqueda = formatear_palabra(palabra)
        url = "https://listado.mercadolibre.com.mx/" + busqueda

        chromedriver_path = r"C:\path\to\chromedriver.exe"
        options = Options()
        options.add_argument("--headless")
        service = Service(executable_path=chromedriver_path)

        driver = webdriver.Chrome(service=service, options=options)
        df = obtener_tabla(url, driver)
        driver.quit()

        return render_template('result.html', tables=[df.to_html(classes='data', header="true")])

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
