from PIL import Image
import os

def extract_red_walk_u_sprites(image_path, output_folder, offset_x, offset_y, sprite_width, sprite_height, count=7):
    """
    Extrai os 7 sprites da área "Red Walk U" (peão andando para cima) da sprite sheet
    e os salva como arquivos PNG individuais.

    Parâmetros:
      image_path: Caminho para a sprite sheet.
      output_folder: Pasta onde os sprites extraídos serão salvos.
      offset_x: Coordenada x (em pixels) do canto superior esquerdo do primeiro sprite desejado.
      offset_y: Coordenada y (em pixels) do canto superior esquerdo do primeiro sprite desejado.
      sprite_width: Largura de cada sprite (em pixels).
      sprite_height: Altura de cada sprite (em pixels).
      count: Número de sprites a serem extraídos (padrão = 7).
    """
    # Cria a pasta de saída, se ainda não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Abre a sprite sheet
    try:
        sheet = Image.open(image_path)
    except IOError:
        print(f"Erro ao abrir {image_path}")
        return

    # Para cada sprite desejado (assumindo que estão lado a lado)
    for i in range(count):
        left   = offset_x + i * sprite_width
        upper  = offset_y
        right  = left + sprite_width
        lower  = upper + sprite_height
        sprite = sheet.crop((left, upper, right, lower))
        
        sprite_filename = os.path.join(output_folder, f"pawn_up_{i+1}.png")
        sprite.save(sprite_filename)
        print(f"Sprite salvo: {sprite_filename}")

if __name__ == "__main__":
    # Caminho para a sprite sheet (substitua pelo nome do seu arquivo)
    image_path = "images/sprite_sheet.png"
    
    # Pasta onde os sprites extraídos serão salvos
    output_folder = "output_sprites"
    
    # Valores extraídos da imagem:
    offset_x = 52        # Início do primeiro sprite (contando a área do texto "Walk U")
    offset_y = 40        # Abaixo da palavra "Red"
    sprite_width = 27    # Largura de cada sprite (em pixels)
    sprite_height = 42   # Altura de cada sprite (em pixels)
    
    extract_red_walk_u_sprites(image_path, output_folder, offset_x, offset_y, sprite_width, sprite_height)
