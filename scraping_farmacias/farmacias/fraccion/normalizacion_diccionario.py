from dataclasses import dataclass
from pathlib import Path
import os
import pandas as pd


@dataclass
class NormalizacionDiccionario:
    def __init__(self, Farmaco) -> None:
        self.Farmaco = Farmaco
        self.cargar_data_diccionario()
        self.datos_faltantes = {}
        self.tipo_unidades = Farmaco.cantidad_unidades

    def cargar_data_diccionario(self):
        """Carga datos de normalizacion de laboratorio desde diccionario"""
        dir_path = Path(__file__).parent.parent
        file_path = os.path.join(dir_path, "diccionario.xlsx")
        # DATOS LABORATORIOS
        df_laboratorios = pd.read_excel(file_path, sheet_name="EMPRESA")
        self.laboratorios = list(df_laboratorios["Empresa"])
        self.laboratorios_normalizados = list(df_laboratorios["Normalizado"])
        # DATOS PRINCIPIO ACTIVO
        df_principio_activo = pd.read_excel(file_path, sheet_name="PA")
        self.principios_activos = list(df_principio_activo["PA"])
        self.principios_activos_normalizados = list(df_principio_activo["NORMALIZADO"])
        # DATOS VIA ADMINISTRACION
        df_via_administracion = pd.read_excel(file_path, sheet_name="VIA")
        self.vias_administracion = list(df_via_administracion["Via administracion"])
        self.vias_administracion_normalizados = list(
            df_via_administracion["NORMALIZADO"]
        )

    def normalizacion_laboratorio(self):
        Farmaco = self.Farmaco
        laboratorios = self.laboratorios
        laboratorios_normalizados = self.laboratorios_normalizados
        if Farmaco.laboratorio in laboratorios:
            i = laboratorios.index(Farmaco.laboratorio)
            Farmaco.laboratorio = laboratorios_normalizados[i]
        else:
            self.datos_faltantes = {
                "tipo_dato": "Laboratorio",
                "dato": Farmaco.laboratorio,
                "url": Farmaco.url,
            }
        self.Farmaco = Farmaco

    def normalizacion_principio_activo(self):
        Farmaco = self.Farmaco
        principios_activos = self.principios_activos
        principios_activos_normalizados = self.principios_activos_normalizados
        if Farmaco.principio_activo in principios_activos:
            i = principios_activos.index(Farmaco.principio_activo)
            Farmaco.principio_activo = principios_activos_normalizados[i]
        else:
            self.datos_faltantes = {
                "tipo_dato": "Principio Activo",
                "dato": Farmaco.principio_activo,
                "url": Farmaco.url,
            }
        self.Farmaco = Farmaco

    def normalizacion_via_administracion(self):
        Farmaco = self.Farmaco
        vias_administracion = self.vias_administracion
        vias_administracion_normalizados = self.vias_administracion_normalizados
        if Farmaco.via_administracion in vias_administracion:
            i = vias_administracion.index(Farmaco.via_administracion)
            Farmaco.via_administracion = vias_administracion_normalizados[i]
        else:
            self.datos_faltantes = {
                "tipo_dato": "Via Administracion",
                "dato": Farmaco.via_administracion,
                "url": Farmaco.url,
            }

        self.Farmaco = Farmaco

    def save_datos_faltantes(self):

        with open("tipo_unidades.csv", "a") as file:
            if self.tipo_unidades:
                file.writelines(self.tipo_unidades + "\n")

    def normalizacion_diccionario(self):
        self.normalizacion_laboratorio()
        self.normalizacion_principio_activo()
        self.normalizacion_via_administracion()


if __name__ == "__main__":
    print("Executed when invoked directly")
else:
    print("Executed when imported")
