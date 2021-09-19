#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Framebuffer helper that makes lots of simplifying assumptions

bits_per_pixel    assumed memory layout
16                rgb565
24                rgb
32                argb

"""
import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy
import time
import logging
import threading


def _read_and_convert_to_ints(filename):
    with open(filename, "r") as fp:
        content = fp.read()
        tokens = content.strip().split(",")
        return [int(t) for t in tokens if t]


def _converter_argb(image: Image):
    return bytes([x for r, g, b in image.getdata() for x in (255, r, g, b)])


def _converter_rgb565(image: Image):
    return bytes([x for r, g, b in image.getdata()
                  for x in ((g & 0x1c) << 3 | (b >> 3), r & 0xf8 | (g >> 3))])


def _converter_1_argb(image: Image):
    return bytes([x for p in image.getdata()
                  for x in (255, p, p, p)])


def _converter_1_rgb(image: Image):
    return bytes([x for p in image.getdata()
                  for x in (p, p, p)])


def _converter_1_rgb565(image: Image):
    return bytes([(255 if x else 0) for p in image.getdata()
                  for x in (p, p)])


def _converter_rgba_rgb565_numpy(image: Image):
    flat = numpy.frombuffer(image.tobytes(), dtype=numpy.uint32)
    # note,  this is assumes little endian byteorder and results in
    # the following packing of an integer:
    # bits 0-7: red, 8-15: green, 16-23: blue, 24-31: alpha
    flat = ((flat & 0xf8) << 8) | ((flat & 0xfc00) >> 5) | ((flat & 0xf80000) >> 19)
    return flat.astype(numpy.uint16).tobytes()


def _converter_no_change(image: Image):
    return image.tobytes()


# anything that does not use numpy is hopelessly slow
_CONVERTER = {
    ("RGBA", 16): _converter_rgba_rgb565_numpy,
    ("RGB", 16): _converter_rgb565,
    ("RGB", 24): _converter_no_change,
    ("RGB", 32): _converter_argb,
    ("RGBA", 32): _converter_no_change,
    # note numpy does not work well with mode="1" images as
    # image.tobytes() loses pixel color info
    ("1", 16): _converter_1_rgb565,
    ("1", 24): _converter_1_rgb,
    ("1", 32): _converter_1_argb,
}


class Framebuffer(threading.Thread):
    image: Image = None
    dirty: bool = True

    def __init__(self, device_no: int):
        super().__init__()
        self.path = "/dev/fb%d" % device_no
        config_dir = "/sys/class/graphics/fb%d/" % device_no
        self.size = tuple(_read_and_convert_to_ints(
            config_dir + "/virtual_size"))
        self.stride = _read_and_convert_to_ints(config_dir + "/stride")[0]
        self.bits_per_pixel = _read_and_convert_to_ints(
            config_dir + "/bits_per_pixel")[0]
        assert self.stride == self.bits_per_pixel // 8 * self.size[0]

        self.image = Image.new("RGBA", self.size, "#000000")
        self.shutdown = threading.Event()

    def __str__(self):
        args = (self.path, self.size, self.stride, self.bits_per_pixel)
        return "%s  size:%s  stride:%s  bits_per_pixel:%s" % args

    def __del__(self):
        self.blank()

    # Note: performance is terrible even for medium resolutions
    def show(self, image: Image):
        if image != self.image:
            self.image = image
            self.dirty = True

    def redraw_screen(self):
        if self.dirty:
            # logging.debug(_CONVERTER[(self.image.mode, self.bits_per_pixel)])
            converter = _CONVERTER[(self.image.mode, self.bits_per_pixel)]
            assert self.image.size == self.size
            out = converter(self.image)
            try:
                with open(self.path, "wb") as fp:
                    fp.write(out)
            except NameError:
                pass
            self.dirty = False

    def run(self):
        thread_process = threading.Thread(target=self.loop)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()
        self.shutdown.wait()

    def loop(self):
        while not self.shutdown.is_set():
            self.redraw_screen()
            time.sleep(0.1)

    def blank(self):
        self.image = Image.new("RGBA", self.size)
        self.redraw_screen()

    def text(self, text, margin=5, font='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', fontsize=14,
             background_color=None, foreground_color="#FFFFFF", wrap=True):
        wrapped_text = ''
        if wrap:
            line_width = round(self.size[0] / (fontsize / 2))
            for text_line in text.split('\n'):
                lines = textwrap.wrap(text_line, width=line_width)
                for line in lines:
                    wrapped_text += line + '\n'
        else:
            wrapped_text = text

        if background_color:
            self.image = Image.new('RGBA', self.size, background_color)
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font, fontsize)

        draw.text((margin, margin), wrapped_text, font=font, fill=foreground_color)
        self.redraw_screen()


if __name__ == "__main__":
    def test_frame_buffer(i):
        fb = Framebuffer(i)
        print(fb)
        image = Image.new("RGBA", fb.size)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), fb.size), fill="green")
        draw.ellipse(((0, 0), fb.size), fill="blue", outline="read")
        draw.line(((0, 0), fb.size), fill="gfireofxs-", width=2)
        start = time.time()
        for i in range(5):
            fb.show(image)
        stop = time.time()
        print("fps: %.2f" % (10 / (stop - start)))


    for i in [1]:
        test_frame_buffer(i)
