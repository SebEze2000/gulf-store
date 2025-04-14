import pdfplumber
import json
import re

with pdfplumber.open("data/productos.pdf") as pdf:
    texto = ""
    for page in pdf.pages:
        texto += page.extract_text() + "\n"
        
# Rubros válidos
rubros_permitidos = {"BENV", "ALMA", "COFR", "SNAC", "PACO"}

# Regex para extraer campos
patron = re.compile(r"""
    ^(?P<codigo>[A-Z0-9]+)\s+               # Código al inicio de la línea
    (?P<nombre>.*?)\s+                      # Nombre del producto (lazy hasta rubro)
    (?P<rubro>BENV|ALMA|COFR|SNAC|PACO)\s+  # Rubros permitidos
    (?P<familia>[A-Z]+)\s+
    (?P<cantidad>-?\d+,\d+)\s+
    (?P<precio>\d{1,3}(?:\.\d{3})*,\d+)
""", re.VERBOSE | re.MULTILINE)




productos = []
for match in patron.finditer(texto):
    datos = match.groupdict()

    if datos["rubro"] in rubros_permitidos:
        nombre_limpio = datos["nombre"].strip()

        # Si el código está dentro del nombre, lo quitamos
        if datos["codigo"] in nombre_limpio:
            nombre_limpio = nombre_limpio.replace(datos["codigo"], "").strip()

        productos.append({
            "name": nombre_limpio,
            "price": int(float(datos["precio"].replace(".", "").replace(",", "."))),
            "rubro": datos["rubro"],
            "familia": datos["familia"]
        })

# Guardar como JSON
with open("productos.json", "w", encoding="utf-8") as f:
    json.dump({"productos": productos}, f, indent=2, ensure_ascii=False)

print(f"✅ JSON actualizado con {len(productos)} productos.")
