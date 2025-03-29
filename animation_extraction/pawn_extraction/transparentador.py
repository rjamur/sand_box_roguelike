from PIL import Image
import os

def remove_background_color(input_path, output_path, tolerance=30):
    """
    Abre a imagem de input_path, obtém a cor do primeiro pixel (canto superior esquerdo)
    e transforma em transparente todos os pixels que forem similares a essa cor (dentro da tolerância).
    
    Parâmetros:
      input_path: Caminho para a imagem de entrada.
      output_path: Caminho para salvar a imagem com fundo transparente.
      tolerance: Valor máximo para a diferença entre os canais (R,G,B) do pixel e da cor de fundo.
    """
    # Abre a imagem e converte para o modo RGBA para garantir a presença do canal alpha
    img = Image.open(input_path).convert("RGBA")
    
    # Obtém a cor do primeiro pixel (assumindo ser o fundo verde)
    bg_color = img.getpixel((0, 0))
    print("Cor de fundo detectada:", bg_color)
    
    new_data = []
    # Processa cada pixel da imagem
    for pixel in img.getdata():
        r, g, b, a = pixel
        # Se a diferença entre o pixel atual e a cor de fundo for menor que a tolerância para cada canal
        if abs(r - bg_color[0]) < tolerance and abs(g - bg_color[1]) < tolerance and abs(b - bg_color[2]) < tolerance:
            # Define o pixel como transparente (alpha = 0)
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    
    # Atualiza a imagem com os novos dados e salva
    img.putdata(new_data)
    img.save(output_path)
    print("Imagem salva com fundo transparente em:", output_path)

if __name__ == "__main__":
    # Pasta de origem das imagens (ajuste conforme necessário)
    images_folder = "images"
    input_filename = "sprite_sheet.png"  # Nome da sua imagem de origem
    output_filename = "sprite_sheet_transparent.png"
    
    input_path = os.path.join(images_folder, input_filename)
    output_path = os.path.join(images_folder, output_filename)
    
    # Executa a função de remoção do fundo (ajuste a tolerância se necessário)
    remove_background_color(input_path, output_path, tolerance=30)
