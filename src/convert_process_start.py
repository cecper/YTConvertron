from youtube_converter import convert
import sys
try:
    url = sys.argv[1]
    format = sys.argv[2]
    outputPath = sys.argv[3]
    convert(url,format,outputPath)
except IndexError:
    print("Please provide the url, format and output path as arguments.")
