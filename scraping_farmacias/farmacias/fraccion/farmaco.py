from dataclasses import dataclass


@dataclass
class Farmaco:
    nombre: str
    precio: str
    registro_sanitario: str
    principio_activo: str
    laboratorio: str
    via_administracion: str
    formato: str
    unidad_medida: str
    dosis: str
    sku: str
    url: str
    cantidad_unidades: str = None

    def normalizacion_principio_activo(self):

        p = self.principio_activo
        p = p.replace("|", "-")
        p = p.replace("Á", "A")
        p = p.replace("É", "E")
        p = p.replace("Í", "I")
        p = p.replace("Ó", "O")
        p = p.replace("Ú", "U")
        self.principio_activo = p

    def normalizacion_laboratorio(self):
        l = self.laboratorio
        l = l.replace("|", "-")
        l = l.replace("Á", "A")
        l = l.replace("É", "E")
        l = l.replace("Í", "I")
        l = l.replace("Ó", "O")
        l = l.replace("Ú", "U")
        self.laboratorio = l

    def normalizacion_dosis(self):
        d = self.dosis
        d = d.replace("|", "-")
        d = d.replace(",", ".")
        self.dosis = d

    def normalizacion_formato(self):
        f = self.formato
        f = f.replace("UNGÜENTO", "UNGUENTO")
        f = f.replace("SOLUCION ORAL", "SOLUCION")
        f = f.replace("COMPRIMIDO RECUBIERTO", "COMPRIMIDO")
        f = f.replace("COMPRIMIDO CON RECUBRIMIENTO ENTERICO", "COMPRIMIDO")
        f = f.replace("POLVO GRANULADO PARA SOLUCION ORAL", "POLVO")
        f = f.replace("SOLUCION PARA INHALACION", "SOLUCION")
        f = f.replace("AEROSOL PARA INHALACION", "AEROSOL")
        f = f.replace("COMPRIMIDO MASTICABLE", "COMPRIMIDO")
        f = f.replace("TABLETA EFERVESCENTE", "TABLETA")
        f = f.replace("SOLUCION OFTALMICA", "SOLUCION")
        f = f.replace("SUSPENSION ORAL", "SUSPENSION")
        f = f.replace("CAPSULA CON GRANULOS CON RECUBRIMIENTO ENTERICO", "CAPSULA")
        f = f.replace("OVULOS", "OVULO")
        f = f.replace("CAPSULA BLANDA", "CAPSULA")
        f = f.replace("COMPRIMIDO LIBERACION PROLONGADA", "COMPRIMIDO")
        f = f.replace("COMPRIMIDO RECUBIERTO LIBERACION PROLONGADA", "COMPRIMIDO")
        f = f.replace("CAPSULA CON MICROGRANULOS CON RECUBRIMIENTO ENTERI", "CAPSULA")
        f = f.replace("COMPRIMIDO DISPERSABLE", "COMPRIMIDO")
        f = f.replace("COMPRIMIDO BUCODISPERSABLE", "COMPRIMIDO")
        f = f.replace("COMPRIMIDO EFERVESCENTE", "COMPRIMIDO")
        f = f.replace("COMPRIMIDO SUBLINGUAL", "COMPRIMIDO")
        f = f.replace("POLVO PARA SOLUCION ORAL", "POLVO")
        f = f.replace("SOLUCION NASAL", "SOLUCION")
        f = f.replace("SOLUCION NEBULIZACION", "SOLUCION")
        f = f.replace("SOLUCION PARA ENEMA", "SOLUCION")
        f = f.replace("SOLUCION PARA ENEMA", "SOLUCION")
        self.formato = f

    def normalizacion_via_administracion(self):
        v = self.via_administracion
        v = v.replace("Á", "A")
        v = v.replace("É", "E")
        v = v.replace("Í", "I")
        v = v.replace("Ó", "O")
        v = v.replace("Ú", "U")
        v = v.replace("Ü", "U")
        v = v.replace("TOPICA", "TOPICO")
        v = v.replace(",", ".")
        self.via_administracion = v

    def normalizacion_nombre(self):
        n = self.nombre
        n = n.replace("Á", "A")
        n = n.replace("É", "E")
        n = n.replace("Í", "I")
        n = n.replace("Ó", "O")
        n = n.replace("Ú", "U")
        n = n.replace("Ü", "U")
        n = n.replace("TOPICA", "TOPICO")
        n = n.replace(",", ".")
        self.nombre = n

    def normalizacion_precio(self):
        p = self.precio
        temp_str = ""
        for x in p:
            if x.isnumeric():
                temp_str += x
        self.precio = temp_str
        p = self.precio

    def get_numero_unidades(self):
        nombre = self.nombre
        try:
            if " X " in nombre:
                i = nombre.index(" X ") + 3
                self.cantidad_unidades = nombre[i:]
        except Exception as e:
            print(e)

    def normalizar(self):
        self.normalizacion_nombre()
        self.normalizacion_via_administracion()
        self.normalizacion_precio()
        self.normalizacion_dosis()
        self.normalizacion_principio_activo()
        self.normalizacion_formato()
        self.normalizacion_precio()
        self.normalizacion_laboratorio()
        self.get_numero_unidades()


if __name__ == "__main__":
    print("Executed when invoked directly")
else:
    print("Executed when imported")
