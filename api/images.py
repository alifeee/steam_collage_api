# Grabs image from url, or from cache if it exists

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from io import BytesIO
from flask import send_file

CACHE_DIR = "./cache/"
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


def getImageUrlForGameId(game_id: int):
    """Get image url for game id

    Args:
        game_id (int): Game id

    Returns:
        str: Image url
    """
    return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"


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
    else:
        response = requests.get(url)
        try:
            img = Image.open(BytesIO(response.content))
        except:
            raise ValueError(f"Error opening image for game id: {game_id}")
        img.save(img_path)
        return img


def makeCollage(games, image_size):
    max_images = image_size[0] * image_size[1]
    images = []
    extra = 0
    for (index, game) in tqdm(enumerate(games), total=max(max_images, len(games))):
        if index >= max_images + extra:
            break
        try:
            images.append(getImageForGameId(game["appid"]))
        except:
            print(f"Error getting image for game: {game['name']}")
            extra += 1

    THUMB_WIDTH = 460
    THUMB_HEIGHT = 215

    total_columnolumns = image_size[0]
    total_rows = image_size[1]
    collage_width = total_columnolumns * THUMB_WIDTH
    collage_height = total_rows * THUMB_HEIGHT

    collage = Image.new("RGB", (collage_width, collage_height))
    for i, image in enumerate(images):
        row = i // total_columnolumns
        col = i % total_columnolumns
        x = col * THUMB_WIDTH
        y = row * THUMB_HEIGHT
        collage.paste(image, (x, y))
    return collage


def serve_pil_image(pil_img: Image):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
