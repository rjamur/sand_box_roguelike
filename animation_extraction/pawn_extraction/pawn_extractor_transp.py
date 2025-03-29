from PIL import Image
import os

def remove_green_background(image, green_threshold=200, non_green_max=50):
    """
    Converte o fundo verde da imagem em transparente.
    
    Critério: Se o canal verde do pixel for >= green_threshold e os canais
    vermelho e azul forem <= non_green_max (ou seja, próximo de (0,255,0)),
    o pixel receberá alpha 0.
    """
    image = image.convert("RGBA")
    pixels = image.getdata()
    new_pixels = []
    
    for pixel in pixels:
        r, g, b, a = pixel
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
    Extrai 7 sprites da área "Red Walk U" da sprite sheet, converte o fundo verde para transparente
    e salva cada sprite como um arquivo PNG individual.
    
    Parâmetros:
      image_path: Caminho para a sprite sheet.
      output_folder: Pasta onde os sprites extraídos serão salvos.
      offset_x: Posição X do canto superior esquerdo do primeiro sprite.
      offset_y: Posição Y do canto superior esquerdo do primeiro sprite.
      sprite_width: Largura de cada sprite (em pixels).
      sprite_height: Altura de cada sprite (em pixels).
      count: Número de sprites a serem extraídos (default 7).
    """
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        sheet = Image.open(image_path)
    except IOError:
        print(f"Erro ao abrir {image_path}")
        return
    
    for i in range(count):
        left = offset_x + i * sprite_width
        upper = offset_y
        right = left + sprite_width
        lower = upper + sprite_height
        
        sprite = sheet.crop((left, upper, right, lower))
        sprite = remove_green_background(sprite, green_threshold=200, non_green_max=50)
        
        sprite_filename = os.path.join(output_folder, f"pawn_up_{i+1}.png")
        sprite.save(sprite_filename)
        print(f"Sprite salvo: {sprite_filename}")

if __name__ == "__main__":
    # Caminho para a sprite sheet – ajuste conforme necessário.
    image_path = "sprite_sheet.png"
    # Pasta de saída para os sprites extraídos.
    output_folder = "output_sprites"
    
    # Parâmetros conforme informado:
    offset_x = 52       # Posição X do primeiro sprite (contabilizando o texto "Walk U")
    offset_y = 40       # Posição Y logo abaixo da palavra "Red"
    sprite_width = 27   # Largura de cada sprite (em pixels)
    sprite_height = 42  # Altura de cada sprite (em pixels)
    
    extract_red_walk_u_sprites(image_path, output_folder, 
                               offset_x, offset_y, 
                               sprite_width, sprite_height, count=7)
