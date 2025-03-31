#!/usr/bin/python
import os
import sys
import argparse
from PIL import Image


def remove_background_color(input_path, output_path, tolerance=30, msg_indent="   |            "):
    """
    Abre a imagem em input_path, obtém a cor do primeiro pixel (canto superior esquerdo)
    e torna transparente todos os pixels com cor similar (dentro da tolerância).
    A imagem processada é salva em output_path.
    
    Parâmetros:
      input_path: Caminho da imagem de entrada.
      output_path: Caminho para salvar a imagem processada.
      tolerance: Valor máximo para a diferença entre os canais (R, G, B).
      msg_indent: Indentação (com marcador) para as mensagens exibidas.
    """
    img = Image.open(input_path).convert("RGBA")
    bg_color = img.getpixel((0, 0))
    print(f"{msg_indent}[Processando] {os.path.basename(input_path)} – cor de fundo: {bg_color}")

    new_data = []
    for pixel in img.getdata():
        r, g, b, a = pixel
        if (abs(r - bg_color[0]) < tolerance and
            abs(g - bg_color[1]) < tolerance and
            abs(b - bg_color[2]) < tolerance):
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    img.save(output_path)
    print(f"{msg_indent}[Salvo] {os.path.basename(output_path)}")


def process_folder(input_folder, output_folder, tolerance=30):
    """
    Percorre recursivamente a pasta input_folder e suas subpastas, 
    processa todos os arquivos PNG e salva a saída mantendo a estrutura original dentro de output_folder.
    
    Exibe a estrutura em árvore. Para cada arquivo, após imprimir sua linha (com "├──"),
    as mensagens de processamento são exibidas em linhas imediatamente abaixo, 
    com uma indentação extra iniciada por "   |            ".
    """
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)

    for dirpath, dirnames, filenames in os.walk(input_folder):
        # Ordena para exibição consistente
        dirnames.sort()
        filenames.sort()

        # Calcula o caminho relativo em relação à pasta de entrada
        relative = os.path.relpath(dirpath, input_folder)
        level = 0 if relative == "." else relative.count(os.sep)
        indent = "    " * level

        # Nome da pasta: se for raiz, usamos o nome da pasta de entrada
        folder_name = os.path.basename(input_folder) if relative == "." else os.path.basename(dirpath)
        print(f"{indent}{folder_name}/")

        # Cria o correspondente diretório na pasta de saída
        output_dir = os.path.join(output_folder, relative) if relative != "." else output_folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Para cada arquivo PNG, imprime a linha e processa o arquivo
        for filename in filenames:
            if filename.lower().endswith(".png"):
                file_indent = indent + "├── "
                print(f"{file_indent}{filename}")
                # Nova indentação para as mensagens, com vertical "|"
                child_indent = indent + "|        "
                input_path = os.path.join(dirpath, filename)
                output_path = os.path.join(output_dir, filename)
                remove_background_color(input_path, output_path, tolerance, msg_indent=child_indent)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Remove o fundo de todas as imagens PNG em uma pasta e subpastas, "
            "criando uma pasta de saída paralela com o sufixo '_transparente'."
        )
    )
    parser.add_argument(
        "folder", help="Caminho para a pasta que contém as imagens a serem processadas."
    )
    parser.add_argument(
        "--tolerance", type=int, default=30,
        help="Valor da tolerância para remoção do fundo (padrão: 30)."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Erro: '{args.folder}' não é um diretório válido.")
        sys.exit(1)

    # Cria a pasta de saída ao lado da original, com sufixo "_transparente"
    input_folder = os.path.abspath(args.folder)
    parent_folder = os.path.dirname(input_folder)
    folder_name = os.path.basename(input_folder)
    output_folder = os.path.join(parent_folder, folder_name + "_transparente")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta de saída criada: {output_folder}")
    else:
        print(f"Pasta de saída já existe: {output_folder}")

    process_folder(input_folder, output_folder, args.tolerance)


if __name__ == "__main__":
    main()
