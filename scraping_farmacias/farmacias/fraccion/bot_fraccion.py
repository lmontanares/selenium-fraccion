from typing import List
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import time
from farmaco import Farmaco
import pandas as pd
import os
from pathlib import Path
from normalizacion_diccionario import NormalizacionDiccionario
from selenium.webdriver import FirefoxOptions


class FFraccion:
    def __init__(self):
        """Inicializacion parametros BOT, driver apunta a direccion de Selenium GRID,
        si se decide usar otro driver se debe modificar en este metodo"""
        options_firefox = FirefoxOptions()
        options_firefox.set_preference("javascript.enabled", True)
        options_firefox.set_capability("pageLoadStrategy", "eager")
        options_firefox.headless = True
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4444",
            options=options_firefox,
        )
        self.driver.set_script_timeout(10)
        self.urls_medicamentos = []
        self.data_medicamentos = []
        self.datos_faltantes = []

    def shutdown(self):
        """Cierra instancia de Driver"""
        self.driver.quit()

    def create_folders(self):
        """crea carpetas en el directorio actual del script
        -data
          |__-farmacos
          |__-precios
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        Path(os.path.join(current_dir, "/data")).mkdir(parents=True, exist_ok=True)
        self.farmaco_dir = Path(os.path.join(current_dir, "/data/farmacos"))
        self.farmaco_dir.mkdir(parents=True, exist_ok=True)
        self.precios_dir = Path(os.path.join(current_dir, "/data/precios"))
        self.precios_dir.mkdir(parents=True, exist_ok=True)

    def get_categorias(self):
        """obtiene y guarda una lista con las categorias de la farmacia (24 categorias)"""
        driver = self.driver
        driver.get("https://www.fraccion.cl/medicamentos")
        data = driver.find_elements_by_xpath(
            "//div[@class='sub-category-item']/div[@class='picture']/a[@href]"
        )
        self.urls_categorias = [x.get_attribute("href") for x in data]
        self.urls_categorias.append("https://www.fraccion.cl/medicamentos")
        print(f"Cantidad Categorias: {len(self.urls_categorias)}")

    def browse_categorias(self):
        """recorre la lista de categorias y llama a metodo get_urls()"""
        driver = self.driver
        urls_categorias = self.urls_categorias  # [:2]
        for x in urls_categorias:
            driver.get(x)
            self.get_urls()

    def get_urls(self):
        """obtiene y guarda los url de cada medicamento en la pagina actual"""
        driver = self.driver
        time.sleep(3)
        urls_medicamentos = driver.find_elements_by_xpath(
            "//div[@class='ribbon-wrapper']//div[@class='picture']/a"
        )
        for x in urls_medicamentos:  # [:2]
            self.urls_medicamentos.append(x.get_attribute("href"))
        self.get_next_page()

    def get_next_page(self):
        """busca en la pagina actual el boton "next-page" si existe le hace click y continua la extraccion con get_urls()"""
        driver = self.driver
        try:
            next_button = driver.find_element_by_xpath("//li[@class='next-page']")
            if next_button:
                next_button.click()
                self.get_urls()
        except NoSuchElementException as e:
            print(e)

    def get_med_data(self):
        """
        1.- recorre lista de medicamentos
        2.- extrae los datos de cada farmaco
        3.- crea un class object Farmaco
        4.- guarda class object en arreglo self.data_medicamentos
        """
        driver = self.driver
        urls = list(set(self.urls_medicamentos))
        print(f"se encontraron urls {len(self.urls_medicamentos)} y {len(urls)} unicos")
        for x in urls:
            try:
                driver.get(x)
                time.sleep(3)
                nombre = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[1]/div[1]/h1'
                ).text.upper()
                precio = driver.find_element_by_class_name("product-price").text
                principio_activo = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]'
                ).text.upper()
                dosis = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[6]/td[2]'
                ).text.upper()
                unidad_medida = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[7]/td[2]'
                ).text.upper()
                formato = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[8]/td[2]'
                ).text.upper()
                via_administracion = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[9]/td[2]'
                ).text.upper()
                registro_sanitario = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[10]/td[2]'
                ).text.upper()
                laboratorio = driver.find_element_by_xpath(
                    '//*[@id="product-details-form"]/div/div[2]/div[1]/div[2]/table/tbody/tr[14]/td[2]'
                ).text.upper()
                sku = driver.find_element_by_xpath(
                    '//div[@class="sku"]/span[@class="value"]'
                ).text

                f = Farmaco(
                    nombre=nombre,
                    precio=precio,
                    principio_activo=principio_activo,
                    dosis=dosis,
                    unidad_medida=unidad_medida,
                    formato=formato,
                    via_administracion=via_administracion,
                    registro_sanitario=registro_sanitario,
                    laboratorio=laboratorio,
                    sku=sku,
                    cantidad_unidades=None,
                    url=x,
                )
                self.data_medicamentos.append(f)

            except NoSuchElementException as e:
                print(e)
        print(
            f" Cantidad de Datos de medicamentos agregados {len(self.data_medicamentos)}"
        )

    def normalizar_data(self):
        """recorre lista de medicamentos y normaliza los datos"""
        data = self.data_medicamentos
        try:
            for x in data:
                x.normalizar()
                d = NormalizacionDiccionario(x)
                d.normalizacion_diccionario()
                if d.datos_faltantes:
                    self.datos_faltantes.append(d.datos_faltantes)
                    print(self.datos_faltantes)
        except Exception as e:
            print(e)
        data = self.data_medicamentos

    def save_data(self):
        """guarda los datos de los medicamentos en un dataframe y lo guarda en formato csv"""
        d = pd.DataFrame(self.data_medicamentos)
        dir = self.farmaco_dir
        d.to_csv(
            os.path.join(dir, "test_csv.csv"),
            index=False,
            sep="@",
            encoding="utf-8-sig",
        )
        d_1 = pd.DataFrame(self.datos_faltantes)
        d_1.to_csv(
            os.path.join(dir, "datos_faltantes.csv"),
            index=False,
            sep="@",
            encoding="utf-8-sig",
        )


def main():
    """ejecucion principal del programa"""
    e = None
    max_attempts = 1
    for i in range(0, max_attempts):
        try:
            bot = FFraccion()
            bot.create_folders()
            bot.get_categorias()
            bot.browse_categorias()
            bot.get_med_data()
            bot.shutdown()
            bot.normalizar_data()
            bot.save_data()
        except Exception as e:
            print(e)

    if e is not None:
        raise e


#%%
if __name__ == "__main__":
    main()
else:
    print("Executed when imported")
