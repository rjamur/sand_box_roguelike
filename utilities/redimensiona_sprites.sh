#!/bin/bash

# Caminho do diretório base
BASE_DIR="."

# Fator de escala (300% para triplicar)
SCALE="300%"

# Percorre todas as pastas e subpastas
find "$BASE_DIR" -type f -name "*.png" | while read file; do
    # Redimensiona a imagem utilizando o ImageMagick
    mogrify -resize $SCALE "$file"
    echo "Imagem redimensionada: $file"
done
