#!/usr/bin/env python3
import sys
import argparse
import os


from effects import dither, textify
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from enum import Enum



def process(img, output, effects):

    for effect in effects:
        img = effect(img)

EFFECTS = {
    "dither": dither, 
    "textify":textify
    }

def verify(input_path, output_directory, filters):
    
    try:
        image = pygame.image.load(input_path)
    except FileNotFoundError:
        print(f"Could not find file: {input_path}")
        return -1
        
    if not os.path.isdir(output_directory):
        print(f"This directory does not exist: {output_directory}")
        return -1

    if filters == None:
        print(f"No effects applied, no file created. Use -p <effect_one> <effect_two> etc.")
        return -1
    

    pipeline = [EFFECTS[e.lower()] for e in list(filters) if e.lower() in EFFECTS]
    
    if(len(pipeline) != len(filters)):
        print(f"Processes/Filters not found: {[e for e in list(filters) if not e.lower() in EFFECTS]}")
        return -1
    
    process(image, output_directory, pipeline)


def main():
    parser = argparse.ArgumentParser(
            prog = os.path.basename(__file__),
            usage = "%(prog)s process <input_image> <output_path> -f <effects>",
            description="Command-Line Tool for Image Processing", 
            add_help=False
        )
    
    subparsers = parser.add_subparsers(dest="command")
    list_parser = subparsers.add_parser('list', help = "List the shit")
    process_parser = subparsers.add_parser('process', help = "Process the shit")


    parser.add_argument("-h", "-help", "--help", action="help", help = "Show this help message and exit")
    process_parser.add_argument("-f", action="append", nargs = "*", help = "Add an effect/filter to the image")
    
    
    if len(sys.argv) <= 1:
        print(f"usage: {parser.prog} process <input_image> <output_path> -f <effects>")
        sys.exit()
    
    args = parser.parse_args()
    print(args)
    # verify(args.input_image, args.output_path, args.process)

if __name__ == "__main__":
    main()


"""impro
Usage: impro process <input_image> <output_path> -f <effects>
"""


""" impro -h
Command-Line for Image Processing

Commands:
List                                            Lists all possible filters
Process [Input] [Output] <Filters>              Processes image

Options:
-h, --help,                                     Show this help message and exit
-f, --filter [Filtername] <Parameters>          Used with Process to specify filters

"""

""" impro list
Filters/effects to use with process
Example usage: impro input_image output_path -f dither 3 -f textify 1.1 4

dither <arg1> <arg2>            Description of filter and parameters. Could be quite long.
textify <arg1>                  Description of filter and parameters

"""


""" impro -h dither
dither <arg1> <arg2>            Description of filter and parameters for dither specifically.

"""

