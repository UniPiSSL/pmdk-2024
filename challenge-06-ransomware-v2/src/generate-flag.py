#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Load flag
flag = 'FLAG{this-is-an-example-flag}'
if os.path.exists('flag.txt'):
	flag = open('flag.txt', 'r').read().strip()
else:
	print('WARNING! Using example flag.')


def generate_image_with_text(text, output, image_size=(800, 200), text_color=(0, 0, 0), background_color=(255, 255, 255), font_size=40):
	# Create a blank image with the specified background color
	img = Image.new("RGB", image_size, background_color)
	
	# Create a draw object
	draw = ImageDraw.Draw(img)
	
	# Use a basic font (you can specify your own font file)
	font = ImageFont.truetype("./UbuntuMono-Regular.ttf", font_size)
	
	# Calculate the position to center the text
	text_width, text_height = draw.textsize(text, font)
	x = (image_size[0] - text_width) // 2
	y = (image_size[1] - text_height) // 2
	
	# Draw the text on the image
	draw.text((x, y), text, font=font, fill=text_color)
	
	# Save the image or display it
	img.save(output)

if __name__ == "__main__":
	# Call the function with the desired parameters
	generate_image_with_text(flag, "ch4ll3ng_flag.png")
