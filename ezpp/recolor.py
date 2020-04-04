#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageColor
import argparse
import os
import re
import colorsys

using_color = "-c The color in hex value in formate of #RRGGBB  or #RGB. For example :#00ff00 or #0f0 make a  green version of your pic"
using_hsv = "HSV:{hue(0-360),saturation[-1.0,1.0],value[-1.0,1.0]},-c will be ignore when using -hsv."
is_color_re = re.compile(r'^#?([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$')
color3_re = re.compile(
    r'^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$'
)
color6_re = re.compile(
    r'^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$'
)


def create_cmd_parser(subparsers):
    parser_recolor = subparsers.add_parser(
        'recolor', help='recolor a pic')
    parser_recolor.add_argument("--infile",
                                "-i",
                                help="the file to be recolor")
    parser_recolor.add_argument("--color",
                                "-c",
                                help=using_color)

    parser_recolor.add_argument("--hue",
                                "-u",
                                help=using_hsv)

    parser_recolor.add_argument("--saturation",
                                "-s",
                                help=using_hsv)

    parser_recolor.add_argument("--value",
                                "-v",
                                help=using_hsv)

    parser_recolor.add_argument("--outfile",
                                "-o",
                                help="Optional the output file")
    parser_recolor.set_defaults(on_args_parsed=_on_args_parsed)


def repeat2(str_tobe_repeat):
    if len(str_tobe_repeat) > 1:
        return str_tobe_repeat
    return str_tobe_repeat+str_tobe_repeat


def _on_args_parsed(args):
    params = vars(args)
    filename = params['infile']
    outfile = params['outfile']
    color = params['color']
    hue = params['hue']
    saturation = params['saturation']
    value = params['value']

    print(f"hue{hue},saturation{saturation},value{value}")

    if hue != None or saturation != None or value != None:
        recolor_hsv(filename, outfile, hue, saturation, value)
        return

    recolor(filename, outfile, color)


def deta_float(origin, deta):
    return max(min(origin + deta, 1.0), 0.0)


def recolor_hsv(filename, outfile, dst_h, dst_s, dst_v):
    bar_filename, ext = os.path.splitext(filename)
    print(f"dst_h:{dst_h}, dst_s:{dst_s}, dst_v:{dst_v}")

    hsv_name = f"_h-{dst_h}" if dst_h != None else f""
    hsv_name += f"_s({dst_s})" if dst_s != None else f""
    hsv_name += f"_v({dst_v})" if dst_v != None else f""

    new_filename = outfile if outfile else f"{bar_filename}{hsv_name}{ext}"
    print(f"{filename} + hsv{hsv_name} -> {new_filename}")
    img = Image.open(filename).convert('RGBA')
    width = img.width
    height = img.height
    px = img.load()

    img_new = Image.new('RGBA', (width, height))
    px_new = img_new.load()

    for y in range(0, height):
        for x in range(0, width):
            r, g, b, a = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            rn, gn, bn = colorsys.hsv_to_rgb(
                int(dst_h) if dst_h != None else h,
                deta_float(s, float(dst_s)) if dst_s != None else s,
                deta_float(v, float(dst_v)) if dst_v != None else v)

            px_new[x, y] = (int(255*rn), int(255*gn), int(255*bn), a)

    img_new.save(new_filename, 'PNG')


def recolor(filename, outfile, color):

    if not is_color_re.match(color):
        print(using_color+using_hsv)
        exit(2)

    color_re = color6_re if len(color) > 4 else color3_re
    color_m = color_re.match(color)
    red = repeat2(color_m.group(1))
    green = repeat2(color_m.group(2))
    blue = repeat2(color_m.group(3))
    bar_filename, ext = os.path.splitext(filename)
    # src_h, src_s, src_v = colorsys.rgb_to_hsv(0, 152/255, 1)
    dst_h, dst_s, dst_v = colorsys.rgb_to_hsv(
        int(red, base=16)/255, int(green, base=16)/255, int(blue, base=16)/255)

    print(f"dst_h:{dst_h}, dst_s:{dst_s}, dst_v:{dst_v}")

    color = f"{red}{green}{blue}"
    new_filename = outfile if outfile else f"{bar_filename}_0x{color}{ext}"
    print(f"{filename} + #{color} -> {new_filename}")
    img = Image.open(filename).convert('RGBA')
    width = img.width
    height = img.height
    px = img.load()

    img_new = Image.new('RGBA', (width, height))
    px_new = img_new.load()

    for y in range(0, height):
        for x in range(0, width):
            r, g, b, a = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            rn, gn, bn = colorsys.hsv_to_rgb(dst_h, s, v)
            px_new[x, y] = (int(255*rn), int(255*gn), int(255*bn), a)

    img_new.save(new_filename, 'PNG')
