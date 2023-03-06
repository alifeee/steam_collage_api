# Alfie Renn
# 13/7/2020
# An attempt at scraping my steam profile for pictures

import requests
from bs4 import BeautifulSoup
import re
import json
from io import BytesIO
from PIL import Image
import string
import sys
import os

# Location for the cached images
CACHE_DIR = "./cache/"
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)
img_path = CACHE_DIR

# User configuration
user = input(
    "Steam custom URL or profile ID (e.g. 'alifeee' or '5164879451874'):\n")
max_images = int(input("Number of games to display (0 for all):\n"))
while True:
    desired_ratio = input(
        "Aspect Ratio: a)1:1 b)2:1 c)1:2 d)4:3 e)16:9\nor choose a custom aspect ratio in the format n:m\n")
    if desired_ratio == 'a':
        aspect_ratio = (1, 1)
        break
    elif desired_ratio == 'b':
        aspect_ratio = (2, 1)
        break
    elif desired_ratio == 'c':
        aspect_ratio = (1, 2)
        break
    elif desired_ratio == 'd':
        aspect_ratio = (4, 3)
        break
    elif desired_ratio == 'e':
        aspect_ratio = (16, 9)
        break
    else:
        rats = re.findall("\d+", desired_ratio)
        if len(rats) != 2:
            print(
                "Your aspect ratio was not understood. Please enter one in the format 'n:m'")
            continue
        aspect_ratio = (int(rats[0]), int(rats[1]))
        break

# If the user has a custom URL (which should usually contain text),
# the URL path changes slightly
if user.isdecimal():
    lib_url = "https://steamcommunity.com/profiles/"+user+"/games/?tab=all"
else:
    lib_url = "https://steamcommunity.com/id/"+user+"/games/?tab=all"

# A dictionary of all games is found in the last script on the page
# under the variable name 'rgGames' so we search for this
r = requests.get(lib_url)
soup = BeautifulSoup(r.text, 'html.parser')
games_container = soup.find(id="games_list_rows")
scripts = soup.find_all("script")
script = scripts[-1]
script = script.string
games_string_groups = re.search("(?<=rgGames = ).*", script)
games_string = games_string_groups.group(0)
games = json.loads(games_string[0:-2])


def open_cached(game_name):
    # Open the image from the local cache on the user's machine
    im = Image.open(img_path + game_name + '.png')
    return im


def open_internet(game_name, pic_url):
    # Open the image from steam's website and cache it
    response = requests.get(pic_url)
    im = Image.open(BytesIO(response.content))
    im.save(img_path + game_name + '.png')
    return im


def make_valid_filename(fn):
    # Remove all characters that would screw up a filename in windows
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in fn if c in valid_chars)


# If no games were loaded because the user's library is private
if len(games) == 0:
    print("This profile's library is private!")
    sys.exit("This profile's library is private!")

# Create a list of images from the cached and non-cached images
images = []
for i, game in enumerate(games):
    filename = make_valid_filename(game['name'])
    try:
        img = open_cached(filename)
    except:
        print("({})Cache not found! Retrieving from URL: {}".format(
            i, game['name']))
        try:
            img = open_internet(filename, game['logo'])
        except Exception as e:
            print("Error: ", e)
            continue
    images.append(img)

# Choose the number of small icons in the image
if max_images <= 0:
    num_images = len(images)
elif max_images < len(images) and max_images > 0:
    num_images = max_images
else:
    num_images = len(images)

# Work out the discrete number of icons per row and per column
aspect_ratio = (aspect_ratio[0], aspect_ratio[1] * (184/69))
aspect_frac = aspect_ratio[0] / aspect_ratio[1]
side_length = int(num_images**.5)
n = side_length * aspect_frac**.5  # horiz
m = side_length / aspect_frac**.5  # vert
n = int(round(n))
m = int(m)
while n*m < num_images:
    m += 1

# The size of the large image and the size of each thumbnail
master_size = (n*184, m*69)
master_image = Image.new('RGBA', master_size)
thumb_box = (0, 0, 184, 69)

# Copy and paste each small image onto the large image
for i, img in enumerate(images):
    if i >= num_images:
        break
    box = ((184*(i % n)), (69*((int(i/n)) % m)), 184 +
           (184*(i % n)), 69+(69*((int(i/n)) % m)))
    thumb = img.crop(thumb_box)
    master_image.paste(thumb, box)

# Save the image to cache and preview it
SAVE_PATH = "./images/"
input(f"Image saved to {SAVE_PATH}/{user}.png. Press enter to preview.")
master_image.save(SAVE_PATH+user+".png")
preview = Image.open(SAVE_PATH+user+".png")
preview.show()
