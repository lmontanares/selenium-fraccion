from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import os


class NormalizacionMaestro:
    def __init__(self) -> None:
        # self.Farmaco = Farmaco
        self.cargar_data_maestro()

        # self.tipo_unidades = Farmaco.cantidad_unidades

    def cargar_data_maestro(self):
        dir_path = Path(__file__).parent.parent
        file_path = os.path.join(dir_path, "MAESTRO.xlsx")
        # DATOS LABORATORIOS
        df_laboratorios = pd.read_excel(file_path, sheet_name="LABORATORIO")
        self.laboratorios = list(df_laboratorios["LABORATORIO"])
        # DATOS PRINCIPIO ACTIVO
        df_principio_activo = pd.read_excel(file_path, sheet_name="PRINCIPIO ACTIVO")
        self.principios_activos = list(df_principio_activo["PRINCIPIO ACTIVO"])

        # DATOS VIA ADMINISTRACION
        df_via_administracion = pd.read_excel(
            file_path, sheet_name="VIA ADMINISTRACION"
        )
        self.vias_administracion = list(df_via_administracion["VIA ADMINISTRACION"])

    def normalizacion_laboratorio(self):
        pass

    def normalizacion_principio_activo(self):
        pass

    def normalizacion_via_administracion(self):
        pass


t = NormalizacionMaestro()
print(t.maestro)
