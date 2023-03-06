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


def makeCollage(games, aspect_ratio=1, max_images=-1):
    if max_images == -1:
        max_images = len(games)
    images = []
    extra = 0
    for (index, game) in tqdm(enumerate(games), desc="Downloading images", total=max_images, unit="images"):
        if index >= max_images + extra:
            break
        try:
            images.append(getImageForGameId(game["appid"]))
        except:
            print(f"Error getting image for game: {game['name']}")
            extra += 1

    THUMB_WIDTH = 460
    THUMB_HEIGHT = 215
    # find how many rows and columns we need
    num_images = len(images)
    num_cols = int(num_images ** 0.5)
    num_rows = int(num_images / num_cols)
    if num_rows * num_cols < num_images:
        num_rows += 1
    # create a new image with the right size
    collage_width = num_cols * THUMB_WIDTH
    collage_height = num_rows * THUMB_HEIGHT
    collage = Image.new("RGB", (collage_width, collage_height))
    # paste the images into the right position
    for i, image in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        x = col * THUMB_WIDTH
        y = row * THUMB_HEIGHT
        collage.paste(image, (x, y))
    return collage


def serve_pil_image(pil_img: Image):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
