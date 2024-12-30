#!/usr/bin/env python3
import sys
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
            prog = os.path.basename(__file__),
            usage = "%(prog)s [input_image] [output_path] -p [processes]",
            description="Command-Line Tool for Image Processing", 
            add_help=False
            
        )
    
    parser.add_argument("input_image", help = "Specify the path to the input image")
    parser.add_argument("output_path", help = "Specify the directory to output the processed image")
    parser.add_argument("-h", "-help", "--help", action="help", help = "Show this help message and exit")
    parser.add_argument("-p", "-process", action = "store", nargs="+", help = "Comma separated list of effects to apply to image, in order")

    if len(sys.argv) <= 1:
        print(f"{parser.prog} [input_image] [output_path] -p [processes]")
        sys.exit()
    
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()