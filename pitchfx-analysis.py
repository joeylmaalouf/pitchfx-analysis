import os
import sys
from xml.etree import ElementTree as ET


def main(argv):
  # if no data path is supplied, use our default
  data_path = "./data/" if len(argv) < 2 else argv[1]

  # walk through the data path and make our list of inning files
  data_filenames = []
  for root, dirnames, filenames in os.walk(data_path):
    for filename in filenames:
      if "inning" in filename.lower():
        data_filenames.append(root + "/" + filename)

  classifications = {
    "FT": "fast", "FF": "fast", "FA": "fast", "FS": "fast",
    "CU": "curve", "CB": "curve",
    "SL": "slide"
  }

  # parse our .xml files via an element tree
  pitch_types = []
  for filename in data_filenames:
    try:
      game = ET.parse(filename)
    except ET.ParseError:
      # if the file can't be parsed, skip it
      continue

    # for every game, iterate through the elements to find the pitch types in all of the atbats
    for inning in game.getroot():
      for half in inning:
        for event in half:
          if event.tag == "atbat":
            pitches = [classifications.get(action.attrib["pitch_type"], "misc")
                       for action in event
                       if action.tag == "pitch" and "pitch_type" in action.attrib]
            print(pitches)


if __name__ == "__main__":
  main(sys.argv)
