from PIL import Image, ImageDraw, ImageFont
import os
import argparse

dirname = "./output-dir/"
filepath = "./images-dir/"
width_param = 4
height_param = 5
fonttype = "./Arial.ttf"

def watermarking(filename,watermark_text,fontsize, opacity, rotation_angle):
	# Open the original image
	main = Image.open(filepath+filename)

	# Create the watermark layer
	watermark = Image.new("RGBA", main.size)
	waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")

	# Define the font size
	fnt = ImageFont.truetype(fonttype, fontsize)

	# Get image height and width
	image_height = main.height
	image_width = main.width
	w1 = image_width/width_param
	h1 = image_height/height_param

	# Add text to image	
	waterdraw.text((w1, h1), watermark_text, font=fnt)
   	
	# Rotate text on image  
	watermark=watermark.rotate(rotation_angle)

	# Set the text opacity
	watermask = watermark.convert("L").point(lambda x: min(x,opacity))

	# Copy the watermask to the alpha layer of the current image
	watermark.putalpha(watermask)

	# Repeat the watermark 
	for left in range(0,image_height,h1):
		for right in range(0,image_width,w1):
			main.paste(watermark, (right, left), watermark)
			
		
	# Save file as JPG
	main.save(dirname+filename, "JPEG")

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description="Places watermarks in batch on images located under image-dir")
	

	parser.add_argument("--text", help="Set watermark text.", nargs='?', const="YOUR TEXT!", default="YOUR TEXT")
	parser.add_argument("--opacity", help="Set opacity.", nargs='?', const=30,  type=int, default=30)
	parser.add_argument("--fontsize", help="Set text font size.", nargs='?', const=100, type=int, default="100")
	parser.add_argument("--angle", help="Set rotation angle.", nargs='?', const=15, type=int, default="15")

	args = parser.parse_args()

	# Place watermark for all files in the directory listed in filepath
	for filename in os.listdir(filepath):
        	if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):	
			watermarking(filename, args.text, args.fontsize, args.opacity, args.angle)

