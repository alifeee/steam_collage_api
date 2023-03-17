# Grabs image from url, or from cache if it exists

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from io import BytesIO

CACHE_DIR = "./cache/"
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

THUMB_WIDTH = 460
THUMB_HEIGHT = 215


def getImageUrlForGameId(game_id: int):
    """Get image url for game id

    Args:
        game_id (int): Game id

    Returns:
        str: Image url
    """
    return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"


def bytesFromPilImage(pil_img: Image):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io


def getImageForGameId(game_id: int):
    """Get image for game id

    Args:
        game_id (int): Game id

    Raises:
        ValueError: If image URL cannot be opened

    Returns:
        Image: Image (PIL)
    """
    url = getImageUrlForGameId(game_id)
    img_path = CACHE_DIR + str(game_id) + ".jpg"
    if os.path.exists(img_path):
        return Image.open(img_path)
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError(f"404: Image not found for game id: {game_id}.")
    try:
        img_bytes = BytesIO(response.content)
        img = Image.open(img_bytes)
    except Exception as e:
        raise ValueError(
            f"Error opening image for game id: {game_id}. Error: {e}")
    img.save(img_path)
    return img


def makeCollage(games, columns_rows):
    columns, rows = columns_rows

    MAX_WIDTH = 3900
    MAX_HEIGHT = 2200
    thumb_scaled_width = min(THUMB_WIDTH, MAX_WIDTH // columns)
    thumb_scaled_height = min(THUMB_HEIGHT, MAX_HEIGHT // rows)

    old_aspect_ratio = THUMB_WIDTH / THUMB_HEIGHT  # ~ 2.1
    new_aspect_ratio = thumb_scaled_width / thumb_scaled_height
    if new_aspect_ratio > old_aspect_ratio:
        thumb_scaled_width = int(thumb_scaled_height * old_aspect_ratio)
    else:
        thumb_scaled_height = int(thumb_scaled_width / old_aspect_ratio)

    width_px = max(thumb_scaled_width * columns, 1)
    height_px = max(thumb_scaled_height * rows, 1)

    images = []
    extra = 0
    max_images = columns * rows

    for (index, game) in tqdm(enumerate(games), total=min(max_images, len(games))):
        if index >= max_images + extra:
            break
        try:
            img = getImageForGameId(game["appid"])
            img = img.resize((thumb_scaled_width, thumb_scaled_height))
            images.append(img)
        except Exception as e:
            print(f"Error getting image for game: {game['name']}")
            print(e)
            extra += 1

    collage = Image.new("RGB", (width_px, height_px))
    for i, image in enumerate(images):
        row = i // columns
        col = i % columns
        x = col * thumb_scaled_width
        y = row * thumb_scaled_height
        collage.paste(image, (x, y))
    return collage
