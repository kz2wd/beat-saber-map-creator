import os
import sys
import pickle
import time

import audio_analysis


class NoteCollector:
    def __init__(self, maps_directory, data_dir):
        self.maps_directory = maps_directory
        self.data_dir = data_dir
        self.audio_collector = audio_analysis.AudioCollector()

    def collect(self):

        expert_data_count = 0
        expert_plus_data_count = 0
        music_count = -1  # start at -1 because value is increased before it is used

        time_start = time.time()
        print("Process started, it will took some time . . . ")

        for x in os.walk(self.maps_directory):

            # check if there is the difficulty required
            take_music = False
            do_check = True
            for ele in x[2]:
                if do_check:
                    if ele == 'ExpertPlus.dat' or ele == 'Expert.dat':
                        take_music = True
                        music_count += 1
                        do_check = False
                        # this prevent from increasing 2 times if the folder contains an Expert and an ExpertPlus level

            for ele in x[2]:

                if ele == 'ExpertPlus.dat':

                    with open(x[0] + "\\" + ele, "r") as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\ExpertPlus " + str(expert_plus_data_count) + " - song " + str(music_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_plus_data_count += 1

                elif ele == 'Expert.dat':
                    
                    with open(x[0] + "\\" + ele, "r") as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\Expert " + str(expert_data_count) + " - song " + str(music_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_data_count += 1

                # music
                elif ".egg" in ele or ".ogg" in ele:
                    if take_music:
                        time_1 = time.time()

                        music_path = x[0] + "/" + ele
                        song = self.audio_collector.collect_music(music_path)

                        with open(self.data_dir + "\\song  " + str(music_count), "wb") as music_data:
                            pickle.dump(song, music_data)

                        time_2 = time.time()
                        print("New music data created : ", ele.split(".")[0], music_count,  ", took :", round(time_2 - time_1, 2), "s")

        time_end = time.time()
        print("Expert map collected :", expert_data_count)
        print("ExpertPlus map collected :", expert_plus_data_count)
        print("Successfully created", expert_data_count + expert_plus_data_count, "notes data")

        print("Collected", music_count, "musics")
        print("Took", round(time_end - time_start, 2), "s")

    def load_data(self, count=-1):
        if count == -1:
            for x in os.walk(self.data_dir):
                for data_file in x[2]:
                    with open(self.data_dir + "/" + data_file, "rb") as notes_file:
                        yield pickle.load(notes_file)
        else:
            for x in os.walk(self.data_dir):
                for data_file in x[2]:
                    if count <= 0:
                        break
                    with open(self.data_dir + "/" + data_file, "rb") as notes_file:
                        yield pickle.load(notes_file)
                    count -= 1


NC = NoteCollector("H:/temp cl", "H:/map data")
NC.collect()

# for note in NC.load_data(1):
    # print(len(note))


