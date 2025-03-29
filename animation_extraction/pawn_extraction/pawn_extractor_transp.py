from PIL import Image
import os

def remove_green_background(image, green_threshold=150, non_green_max=100):
    """
    Converte o fundo verde da imagem em transparente.

    Se o pixel for predominantemente verde (canal verde acima de green_threshold e os canais vermelho e azul abaixo de non_green_max),
    então o pixel se torna transparente.
    
    Parâmetros:
      image: Imagem em modo RGBA.
      green_threshold: Limite para o canal verde.
      non_green_max: Valor máximo permitido para os canais vermelho e azul.
    """
    image = image.convert("RGBA")
    pixels = image.getdata()
    new_pixels = []
    
    for pixel in pixels:
        r, g, b, a = pixel
        # Se o pixel é predominantemente verde
        if g >= green_threshold and r <= non_green_max and b <= non_green_max:
            new_pixels.append((r, g, b, 0))
        else:
            new_pixels.append(pixel)
    
    image.putdata(new_pixels)
    return image

def extract_red_walk_u_sprites(image_path, output_folder,
                               offset_x, offset_y,
                               sprite_width, sprite_height,
                               count=7):
    """
    Extrai 7 sprites da área "Red Walk U" (peão andando para cima) da sprite sheet,
    converte o fundo verde para transparente e salva cada sprite como um arquivo PNG individual.
    
    Parâmetros:
      image_path: Caminho da sprite sheet.
      output_folder: Pasta onde os arquivos extraídos serão salvos.
      offset_x: Posição X do canto superior esquerdo do primeiro sprite.
      offset_y: Posição Y do canto superior esquerdo do primeiro sprite.
      sprite_width: Largura de cada sprite (em pixels).
      sprite_height: Altura de cada sprite (em pixels).
      count: Número de sprites a extrair (default 7).
    """
    # Cria a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        sheet = Image.open(image_path)
    except IOError:
        print(f"Erro ao abrir {image_path}")
        return

    # Extrai os sprites dispostos horizontalmente
    for i in range(count):
        left   = offset_x + i * sprite_width
        upper  = offset_y
        right  = left + sprite_width
        lower  = upper + sprite_height
        
        sprite = sheet.crop((left, upper, right, lower))
        sprite = remove_green_background(sprite)
        
        sprite_filename = os.path.join(output_folder, f"pawn_up_{i+1}.png")
        sprite.save(sprite_filename)
        print(f"Sprite salvo: {sprite_filename}")

if __name__ == "__main__":
    # Caminho para a sprite sheet
    image_path = "sprite_sheet.png"  # Atualize para o caminho real do arquivo
    # Pasta de saída para os sprites extraídos
    output_folder = "output_sprites"
    
    # Parâmetros conforme informados:
    offset_x = 52       # Posição X do primeiro sprite (contabilizando o texto 'Walk U')
    offset_y = 40       # Posição Y logo abaixo da palavra "Red"
    sprite_width = 27   # Largura de cada sprite (em pixels)
    sprite_height = 42  # Altura de cada sprite (em pixels)
    
    extract_red_walk_u_sprites(image_path, output_folder,
                               offset_x, offset_y,
                               sprite_width, sprite_height)
