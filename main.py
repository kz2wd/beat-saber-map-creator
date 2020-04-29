import sys
import os


class BsMapCreator:
    def __init__(self, custom_map_folder, map_name, map_cover, map_song, bps, difficulty='Expert', version="2.0.0"):
        self.custom_map_folder = custom_map_folder
        self.map_name = map_name
        self.map_cover = map_cover
        self.map_song = map_song
        self.bps = bps
        self.difficulty = difficulty
        self.version = version
        self.files = []

        self.map_dict = {"_version": self.version,
                         "_BPMChanges": [],
                         "_events": [],
                         "_notes": [],
                         "_obstacles": []}

    def generate_map_files(self):
        # map folder
        map_is_created = False
        counter = 0
        while not map_is_created:
            try:
                os.mkdir(self.custom_map_folder + "/" + self.map_name + " " + str(counter))
                map_is_created = True
            except FileExistsError:
                counter += 1
            finally:
                if counter > 100:
                    break
                    # act as a security to prevent creating 38 959 folders like me

        path = self.custom_map_folder + "/" + self.map_name + " " + str(counter) + "/"

        # info file

        file_dict = {"_version": self.version,
                     "_songName": self.map_name,
                     "_songSubName": "",
                     "_songAuthorName": "",
                     "_levelAuthorName": "",
                     "_beatsPerMinute": self.bps,
                     "_songTimeOffset": 0,
                     "_shuffle": 0,
                     "_shufflePeriod": 0.5,
                     "_previewStartTime": 12,
                     "_previewDuration": 10,
                     "_songFilename": self.map_song.split("/")[-1].split("\\")[-1],
                     "_coverImageFilename": self.map_cover.split("/")[-1].split("\\")[-1],
                     "_environmentName": "NiceEnvironment",
                     "_customData": {
                         "_contributors": [],
                         "_customEnvironment": "",
                         "_customEnvironmentHash": ""
                     },
                     "_difficultyBeatmapSets":
                         [{"_beatmapCharacteristicName": "Standard", "_difficultyBeatmaps": [
                             {"_difficulty": "Expert", "_difficultyRank": 7, "_beatmapFilename": "Expert.dat",
                              "_noteJumpMovementSpeed": 0.0, "_noteJumpStartBeatOffset": 0.0}]}]}

        info_file_path = path + "/" + "info.DAT"

        sys.stdout = open(info_file_path, "w")  # change std out to the file map
        print(file_dict)  # write the dictionary to file map
        sys.stdout.close()  # close the file
        sys.stdout = sys.__stdout__  # reset the std out

        # read the file and change some char
        # ' => "
        with open(info_file_path, "r+") as f:
            data = f.read().replace("\'", "\"")

        # re-open the file and write the corrected data
        with open(info_file_path, "w") as f:
            f.write(data)

        # difficulties files

        diff_path_file = path + self.difficulty + ".DAT"

        sys.stdout = open(diff_path_file, "w")  # change std out to the file map
        print(self.map_dict)  # write the dictionary to file map
        sys.stdout.close()  # close the file
        sys.stdout = sys.__stdout__  # reset the std out

        # read the file and change some char
        # ' => " and delete spaces
        with open(diff_path_file, "r+") as f:
            data = f.read().replace("\'", "\"").replace(" ", "")

        # re-open the file and write the corrected data
        with open(diff_path_file, "w") as f:
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


creator = BsMapCreator('H:/create map here', 'my_super_map', "", "", 130)

note_number = 20
lvl_notes = [creator.create_note(i, i % 4, 1, 1, 1) for i in range(note_number)]
lvl_notes += [creator.create_note(i, 0, i % 4, 1, 1) for i in range(note_number, 2 * note_number)]
lvl_notes += [creator.create_note(i, 0, 0, i % 2, 1) for i in range(2 * note_number, 3 * note_number)]
lvl_notes += [creator.create_note(i, 0, 0, 0, i % 8) for i in range(3 * note_number, 4 * note_number)]

creator.add_notes(lvl_notes)
creator.generate_map_files()


