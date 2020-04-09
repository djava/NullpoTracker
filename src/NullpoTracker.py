from gameTracker import dataCollection
import gui


if __name__ == '__main__':
    dataCollection.findReplays()
    gui.CSV_FILE.seek(0)
    gui.CSV_READER = list(gui.csv.DictReader(gui.CSV_FILE))
    gui.initGui()
