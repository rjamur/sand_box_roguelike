from PIL import Image
import math

def is_green(pixel, target=(0, 255, 0), tolerance=50):
    """
    Verifica se um pixel é próximo do verde definido em 'target'.
    
    Parâmetros:
      pixel: Uma tupla (r, g, b, a) do pixel.
      target: A cor verde alvo (padrão (0, 255, 0)).
      tolerance: A distância máxima permitida (em valor absoluto) para considerar que o pixel é verde.
    """
    r, g, b, a = pixel
    dr = r - target[0]
    dg = g - target[1]
    db = b - target[2]
    distance = math.sqrt(dr**2 + dg**2 + db**2)
    return distance < tolerance

def remove_green_background(input_path, output_path, target_green=(0, 255, 0), tolerance=50):
    """
    Abre a imagem, substitui os pixels cujo tom é próximo do verde (target_green)
    por pixels totalmente transparentes, e salva o resultado.
    
    Parâmetros:
      input_path: Caminho para a imagem de entrada.
      output_path: Caminho para salvar a imagem com fundo transparente.
      target_green: A cor verde que desejamos remover (padrão (0, 255, 0)).
      tolerance: Tolerância para considerar variações do verde.
    """
    # Abre a imagem e garante que ela esteja no modo RGBA
    img = Image.open(input_path).convert("RGBA")
    pixels = img.getdata()
    new_pixels = []
    
    # Percorre cada pixel; se for verde (dentro da tolerância), torna-o transparente
    for pixel in pixels:
        if is_green(pixel, target_green, tolerance):
            new_pixels.append((pixel[0], pixel[1], pixel[2], 0))
        else:
            new_pixels.append(pixel)
            
    img.putdata(new_pixels)
    img.save(output_path)
    print("Imagem convertida salva em:", output_path)

if __name__ == "__main__":
    # Altere 'input_image.png' para o caminho da sua imagem e defina o nome de saída.
    input_image = "images/sprite_sheet.png"
    output_image = "images/sprite_sheet_transparent.png"
    
    # Chama a função; ajuste a tolerância se necessário
    remove_green_background(input_image, output_image, target_green=(0, 255, 0), tolerance=50)
