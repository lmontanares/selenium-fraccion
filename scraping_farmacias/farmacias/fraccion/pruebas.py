from os import read


with open("datos_faltantes.txt", "r") as file:
    reader = [x for x in file.readlines()]


print(reader)
