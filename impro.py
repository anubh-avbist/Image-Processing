#!/usr/bin/env python3
import sys
import argparse
import os, time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from effects import dither, scale_2, sobel, textify, identity, quantize, swizzle, aberrate, scale
from effects import grayscale
import pygame
from enum import Enum

EFFECTS = {
    "identity": identity.Identity,
    "sobel": sobel.Sobel,          
    "textify": textify.Textify,
    "dither": dither.Dither,
    "quantize": quantize.Quantize,
    "swizzle": swizzle.Swizzle,
    "aberrate": aberrate.Aberrate,
    "scale": scale.Scale,
    "scale2": scale_2.Scale2,
    "grayscale": grayscale.Grayscale
}

def list_effects():
    print(f"Filters/effects to use with process\nExample usage: impro input_image output_path -f dither 3 -f textify 1.1 4)\n")
    
    for effect in EFFECTS.keys():
        required_parameters = EFFECTS[effect].required_parameters
        optional_parameters = EFFECTS[effect].optional_parameters
        required_string = " ".join( map(lambda s : f"[{s}]", required_parameters))
        optional_string = " ".join( map(lambda s : f"<{s}>", optional_parameters))
        output = f"| {effect} {required_string} {optional_string}"
        print(f"{output :<30}{f"\n{" "*30}" if len(output)>30 else ""}{EFFECTS[effect].description}")

def process(filename, img:pygame.Surface, output_directory, args: list[list[str]], debug = False):
    
    processed_image:pygame.Surface = img
    filters = []
    for arg in args:
        start = time.process_time()
        effect = EFFECTS[arg[0]]
        filters.append(arg[0])
        processed_image = effect.apply(processed_image, *arg[1:])

        if debug:
            
            print(f"Time taken for {arg[0] :<20}{f"\n{" "*20}" if len(arg[0])>20 else ""}{float(time.process_time()-start):.5f}")

    output = f"{output_directory}/{os.path.splitext(filename)[0]}_{'_'.join(filters)}{os.path.splitext(filename)[1]}"
    pygame.image.save(processed_image, output)
    print(f"Image successfully created at: {output}")

def verify(input_path, output_directory, filters: list[list[str]], debug = False):
    filename = os.path.basename(input_path)
    try:
        image = pygame.image.load(input_path)
    except FileNotFoundError:
        print(f"Could not find file: {input_path}")
        return -1
    except: 
        print(f"Could not properly load image: {input_path}")
        return -1
    
        
    if not os.path.isdir(output_directory):
        print(f"This directory does not exist: {output_directory}")
        return -1

    if filters == None:
        print(f"No effects applied, no file created. Use -f <effect_one> <effect_two> etc.")
        return -1
    

    pipeline = [e for e in list(filters) if e[0].lower() in EFFECTS]
    
    if(len(pipeline) != len(filters)):
        print(f"Processes/Filters not found: {[e[0] for e in list(filters) if not e[0].lower() in EFFECTS]}")
        return -1
    
    process(filename, image, output_directory, pipeline, debug)


def main():
    parser = argparse.ArgumentParser(
            prog = os.path.basename(__file__),
            description="Command-Line Tool for Image Processing", 
            add_help=False
        )
    
    subparsers = parser.add_subparsers(dest="command")
    list_parser = subparsers.add_parser('list', help = "List all currently implemented image effects/filters")
    process_parser = subparsers.add_parser('process', help = "Apply filters on image and output to specified directory")

    
    parser.add_argument("-h", "-help", action="help", help = "Show this help message and exit")
    process_parser.add_argument("input_image", action = "store")
    process_parser.add_argument("output_directory", action = "store")
    process_parser.add_argument("--debug", action="store_true", help = "Get debug information.")
    process_parser.add_argument("-f", "-filter", action="append", nargs = "*", help = "Add an effect/filter to the image")
    
    
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    
    args = parser.parse_args()
    

    if args.command.lower() == "process":
        verify(args.input_image, args.output_directory, args.f, args.debug)
    
    elif args.command.lower() == "list":
        list_effects()

if __name__ == "__main__":
    main()


