import json
import pandas as pd

class PruebaSubsistema:
    def __init__(self,estado_inicio,mechanismo,alcance):
        self.ESTADO_INICIO = estado_inicio
        self.CONDICIONES = len(estado_inicio)*'1'
        self.mechanismo = mechanismo
        self.alcance = alcance

    def __str__(self):
        return f"Mecanismo: {self.mechanismo}, Alcance: {self.alcance}"
        


class FormatExcel:
    def __init__(self, url,sistema_candidato):
        self.url = url  # Ruta del archivo Excel
        self.lista_valores_sin_formato = []
        self.lista_valores_con_formato = []
        self.sistema_candidato = sistema_candidato
        self.ConstruirLista()
        self.FormatoLista()


    def ConstruirLista(self):
        HojaSeleccionada = 0
        # Cargar el archivo Excel
        df = pd.read_excel(self.url,sheet_name=HojaSeleccionada, engine="openpyxl", header=None)
        # Seleccionar la columna B y extraer los valores desde B5 hasta B103, saltando de 2 en 2
        excel = pd.ExcelFile(self.url)  
 
        self.lista_valores_sin_formato = df.iloc[4:103:2,0].dropna().tolist()

    def FormatoLista(self):
        for i in self.lista_valores_sin_formato:
            part1 = i.split("|")[0].split('_')[0].strip()
            part2 = i.split("|")[1].split('_')[0].strip()
            self.lista_valores_con_formato.append([self.__FormatoEntero__(part1), self.__FormatoEntero__(part2)])
    
    def __FormatoEntero__(self, valor):
        valor_entero = ''
        for i in self.sistema_candidato:
            if i in valor:
                valor_entero += '1'
            else: 
                valor_entero += '0'
        return valor_entero
    
    
    def CargarValores(self, lista, fila):
        # Cargar el archivo Excel
        print('Lista de Limpieza: ',lista[0],lista[1],lista[2])
         
        df = pd.read_excel(self.url, engine="openpyxl", header=None)
        # Insertar los valores en la columna B desde la fila inicio hasta la fila fin
        print(lista[0],lista[1],lista[2])
        df.at[fila, 3] = lista[0]
        df.at[fila, 4] = lista[1]
        df.at[fila, 5] = lista[2]

        # Guardar el archivo Excel
        df.to_excel(self.url, index=False, header=False, engine="openpyxl")
        


class ControladorSubsistema:
    def __init__(self, URL, sistema_candidato,estado_inicio):
        self.formateo= FormatExcel(URL, sistema_candidato)
        self.listaObjetos = []
        self.CrearListaObjetos(estado_inicio)
        self.ObjectToJson()

    def CrearListaObjetos(self,estado_inicio):
        for i in self.formateo.lista_valores_con_formato:
            self.listaObjetos.append(PruebaSubsistema(estado_inicio,i[1], i[0]))


    def ObjectToJson(self, filename="ahiTiene.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([obj.__dict__ for obj in self.listaObjetos], file, indent=4) 

    def __str__(self):
        for i in self.listaObjetos:
            print(i.__str__())


class Prueba:
    def __init__(self, mecanismo, alcance, letras):
        self.mecanismo = mecanismo
        self.alcance = alcance
        self.lista = []
        self.letras = letras
        self.conversion_lista()


    def conversion_lista(self):
        for i in range(len(self.mecanismo)):
            mecanismo = self.__conversion_binario_a_letra__(self.mecanismo[i]) + '_{t}'
            alcance = self.__conversion_binario_a_letra__(self.alcance[i]) + '_{t+1}'
            self.lista.append(f'{alcance}|{mecanismo}')

    def __conversion_binario_a_letra__(self, binario):
        return ''.join([self.letras[i] for i, bit in enumerate(binario) if bit == '1'])
    
    def guardar_pruebas_excel(self, url):
        print(self.lista)
        try:
            df = pd.read_excel(url, engine="openpyxl", header=None)
        except FileNotFoundError:
            df = pd.DataFrame()

        fila_inicial = 2  # fila 3 en Excel (0-indexed)
        filas_necesarias = fila_inicial + (len(self.lista) - 1) * 2 + 1

        # Asegurar que el DataFrame tenga suficientes filas
        if len(df) < filas_necesarias:
            df = df.reindex(range(filas_necesarias))

        for i, valor in enumerate(self.lista):
            fila_actual = fila_inicial + i * 2
            df.at[fila_actual, 0] = valor  # Columna A

        df.to_excel(url, index=False, header=False, engine="openpyxl")
        print(f"Archivo guardado en: {url}")




# Uso de la clase
#URL = "/home/liceth/Documentos/Analisis y Diseno de Algoritmos/Pruebas de campo/pruebas15B.xlsx"  # Cambia esto ypor la ruta de tu archivo
#my_excel = ControladorSubsistema(URL, 'ABCDEFGHIJ','1000000000')
mecanismo = [
    "1111111111111111111111111", "1111111111111111111111111",
    "0111111111011111111101111", "0111111111011111111101111",
    "1010101010101010101010101", "0101010101010101010101010",
    "1101101101110110110111011", "1111111111111111111111111",
    "1111111111111111111111111", "0111111111011111111101111",
    "0111111111011111111101111", "1010101010101010101010101",
    "0101010101010101010101010", "1101101101110110110111011",
    "1111111111111111111111111", "1111111111111111111111111",
    "0111111111011111111101111", "0111111111011111111101111",
    "1010101010101010101010101", "0101010101010101010101010",
    "1101101101110110110111011", "1111111111111111111111111",
    "1111111111111111111111111", "0111111111011111111101111",
    "0111111111011111111101111", "1010101010101010101010101",
    "0101010101010101010101010", "1101101101110110110111011",
    "1111111111111111111111111", "1111111111111111111111111",
    "0111111111011111111101111", "0111111111011111111101111",
    "1010101010101010101010101", "0101010101010101010101010",
    "1101101101110110110111011", "1111111111111111111111111",
    "1111111111111111111111111", "0111111111011111111101111",
    "0111111111011111111101111", "1010101010101010101010101",
    "0101010101010101010101010", "1101101101110110110111011",
    "1111111111111111111111111", "1111111111111111111111111",
    "0111111111011111111101111", "0111111111011111111101111",
    "1010101010101010101010101", "0101010101010101010101010",
    "1101101101110110110111011", "0111111111011111111101111"
]

alcance = [
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "1111111111111111111111111", "1111111111111111111111111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "0111111111011111111101111", "0111111111011111111101111",
    "1010101010101010101010101", "1010101010101010101010101",
    "1010101010101010101010101", "1010101010101010101010101",
    "1010101010101010101010101", "1010101010101010101010101",
    "1010101010101010101010101", "0101010101010101010101010",
    "0101010101010101010101010", "0101010101010101010101010",
    "0101010101010101010101010", "0101010101010101010101010",
    "0101010101010101010101010", "0101010101010101010101010",
    "1101101101110110110111011", "1101101101110110110111011",
    "1101101101110110110111011", "1101101101110110110111011",
    "1101101101110110110111011", "1101101101110110110111011",
    "1101101101110110110111011", "0111111001011111100101111"
]

#pruebas25 = Prueba(mecanismo, alcance, 'ABCDEFGHIJKLMNOPQRSTUVWXY')
#pruebas25.guardar_pruebas_excel('/home/liceth/Documentos/Analisis y Diseno de Algoritmos/Pruebas de campo/pruebas25.xlsx')


