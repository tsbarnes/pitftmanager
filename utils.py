import textwrap
import settings
from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters


def wrapped_text(text, image_size, font_name=settings.FONT, font_size=20, color="white", background_color="black"):
    image = Image.new("RGBA", image_size, background_color)
    font = ImageFont.truetype(font_name, font_size)
    draw = ImageDraw.Draw(image)

    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int((image.size[0] * .95) / avg_char_width)

    scaled_wrapped_text = textwrap.fill(text=text, width=max_char_count)
    draw.text((5, 5), scaled_wrapped_text, font=font, fill=color)

    return image
