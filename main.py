import sys
import os


class BsMapCreator:
    def __init__(self, difficulty="Expert", version="2.0.0"):
        self.difficulty = difficulty
        self.version = version
        self.file = None

        self.map_dict = {"_version": self.version,
                         "_BPMChanges": [],
                         "_events": [],
                         "_notes": [],
                         "_obstacles": []}

    def generate_map_file(self, use_dict=True):
        if not use_dict:
            self.file = open(self.difficulty + ".DAT", "w")
            self.file.write("{\"_version\":\"" + self.version + "\",\"_BPMChanges\":[],")
            self.file.write("\"_events\":[]")
            self.file.write("\"_notes\":[]")
            self.file.write("\"_obstacles\":[]")

            self.file.write("}")
            self.file.close()
        else:
            sys.stdout = open(self.difficulty + ".DAT", "w")
            print(self.map_dict)
            sys.stdout.close()
            sys.stdout = sys.__stdout__

            with open(self.difficulty + ".DAT", "r+") as f:
                data = f.read().replace("\'", "\"").replace(" ", "")

            with open(self.difficulty + ".DAT", "w") as f:
                f.write(data)

    def add_notes(self, notes):
        for note in notes:
            self.map_dict["_notes"].append(note)

    def create_note(self, time, line_index, line_layer, note_type,  cut_direction):
        # time => in sec
        # line_index => 0, 1, 2, 3
        # line_layer => 0, 1, 2, 3
        # note_type => 0 for blue, 1 for red
        # cut_direction => 0 to 7 ?
        return {"_time": str(time),
                "_lineIndex": str(line_index),
                "_lineLayer": str(line_layer),
                "_type": str(note_type),
                "_cutDirection": str(cut_direction)}


creator = BsMapCreator()

note_number = 20
lvl_notes = [creator.create_note(i, i % 4, 1, 1, 1) for i in range(note_number)]
lvl_notes += [creator.create_note(i, 0, i % 4, 1, 1) for i in range(note_number, 2 * note_number)]
lvl_notes += [creator.create_note(i, 0, 0, i % 2, 1) for i in range(2 * note_number, 3 * note_number)]
lvl_notes += [creator.create_note(i, 0, 0, 0, i % 8) for i in range(3 * note_number, 4 * note_number)]

creator.add_notes(lvl_notes)
creator.generate_map_file()


