import matplotlib.pyplot as plt
import os
import sys
from lxml import etree as ET


def main(argv):
  # if no data path is supplied, use our default
  data_path = "./data/" if len(argv) < 2 else argv[1]

  # walk through the data path and make our list of inning files
  data_filenames = []
  for root, dirnames, filenames in os.walk(data_path):
    for filename in filenames:
      if "inning" in filename.lower():
        data_filenames.append(root + "/" + filename)

  # pitch classification conversion to our three categories
  pitch_classes = {
    "FT": "fast", "FF": "fast", "FA": "fast", "FS": "fast",
    "CU": "curve", "CB": "curve",
    "SL": "slide"
  }

  # outcome classification conversion to our four categories
  outcome_classes = {
    "Home Run": "hit", "Triple": "hit", "Double": "hit", "Single": "hit", "Field Error": "hit", "Fielders Choice": "hit",
    "Groundout": "hitout", "Flyout": "hitout", "Bunt Groundout": "hitout", "Pop Out": "hitout", "Bunt Pop Out": "hitout", "Double Play": "hitout", "Grounded Into DP": "hitout", "Runner Out": "hitout", "Forceout": "hitout", "Sac Bunt": "hitout", "Sac Fly": "hitout", "Sacrifice Bunt DP": "hitout", "Sac Fly DP": "hitout", "Fielders Choice Out": "hitout", "Lineout": "hitout", "Bunt Lineout": "hitout",
    "Strikeout": "strikeout", "Strikeout - DP": "strikeout", "Batter Interference": "strikeout",
    "Walk": "walk", "Intent Walk": "walk", "Hit By Pitch": "walk", "Fan interference": "walk", "Catcher Interference": "walk"
  }

  # the results dictionary, listing the number of each type of events each sequence leads to
  results = {
    ("fast", "fast", "curve"):  { "hit": 0, "hitout": 0, "strikeout": 0, "walk": 0 },
    ("fast", "fast", "fast"):   { "hit": 0, "hitout": 0, "strikeout": 0, "walk": 0 },
    ("fast", "slide", "slide"): { "hit": 0, "hitout": 0, "strikeout": 0, "walk": 0 },
    ("slide", "fast", "slide"): { "hit": 0, "hitout": 0, "strikeout": 0, "walk": 0 }
  }

  # parse our .xml files via an element tree
  for filename in data_filenames:
    try:
      game = ET.parse(filename)
    except ET.XMLSyntaxError:
      # if the file can't be parsed, skip it
      continue

    # for every game, iterate through the elements to find the pitch types in all of the atbats
    for inning in game.getroot():
      for half in inning:
        for event in half:
          if event.tag == "atbat":
            pitches = tuple(pitch_classes.get(action.attrib["pitch_type"], "misc")
                            for action in event
                            if action.tag == "pitch" and "pitch_type" in action.attrib)
            sequence = pitches[-3:]
            if sequence in results.keys():
              outcome = outcome_classes[event.attrib["event"]]
              results[sequence][outcome] += 1

  # create a side-by-side absolute bar chart to compare the results
  plt.figure()
  plt.title("Absolute Comparison", fontweight = "bold")
  for i, (k, v) in enumerate(results.items()):
    plt.bar(i - 0.3, v["hit"],       width = 0.2, align = "center", color = "r")
    plt.bar(i - 0.1, v["hitout"],    width = 0.2, align = "center", color = "g")
    plt.bar(i + 0.1, v["strikeout"], width = 0.2, align = "center", color = "b")
    plt.bar(i + 0.3, v["walk"],      width = 0.2, align = "center", color = "k")
  plt.xticks(range(len(results)), [", ".join(throws) for throws in results.keys()], rotation = 30)
  plt.legend(["hit", "hitout", "strikeout", "walk"], fancybox = True, shadow = True)
  plt.tight_layout()
  plt.show()

  # turn the raw results into ratios
  ratios = { sequence:
             { key:
               100.0 * val / sum(counts.values())
              for key, val in results[sequence].items() }
            for sequence, counts in results.items() }

  # create a pie chart to compare the results
  fig, axes = plt.subplots(2, 2)
  axes = axes.reshape(4)
  fig.suptitle("Percentage Comparison", fontweight = "bold")
  colors = ["r", "g", "b", "k"]
  for i, (k, v) in enumerate(ratios.items()):
    axes[i].pie([v["hit"], v["hitout"], v["strikeout"], v["walk"]],
                labels = ["hit", "hitout", "strikeout", "walk"],
                labeldistance = 1.1, colors = colors,
                shadow = True, counterclock = False)
    axes[i].axis("equal")
    axes[i].set_xlabel(", ".join(k))
  plt.tight_layout(pad = 3.0)
  plt.show()


if __name__ == "__main__":
  main(sys.argv)
