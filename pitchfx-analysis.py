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

  # parse our .xml files via an element tree
  pitch_types = []
  for filename in data_filenames:
    try:
      game = ET.parse(filename)
    except ET.ParseError:
      # if the file can't be parsed, skip it
      continue

    # for every game, iterate through the elements to find the pitch types
    for inning in game.getroot():
      for half in inning:
        for event in half:
          if event.tag == "atbat":
            for action in event:
              if action.tag == "pitch":
                pitch = action.get("pitch_type", None)
                if pitch:
                  pitch_types.append(pitch)
  print(len(pitch_types))


if __name__ == "__main__":
  main(sys.argv)
