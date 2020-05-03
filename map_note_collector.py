import os
import sys
import pickle
import time

import audio_analysis
import numpy as np


class NoteCollector:
    def __init__(self, maps_directory, data_dir):
        self.maps_directory = maps_directory
        self.data_dir = data_dir
        self.audio_collector = audio_analysis.AudioCollector()

    def collect(self, stop_on_error=False):

        expert_data_count = 0
        expert_plus_data_count = 0
        music_count = -1  # start at -1 because value is increased before it is used
        folder_count = 0

        time_start = time.time()
        print("Process started, it will take some time . . . ")

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

            if take_music:
                # create a new folder
                try:
                    os.mkdir(self.data_dir + "\\data_set " + str(folder_count))

                except FileExistsError:
                    print("ERROR - File name data set already taken. Clean data folder and retry.")
                    if stop_on_error:
                        break

            for ele in x[2]:

                if ele == 'ExpertPlus.dat':

                    with open(x[0] + "\\" + ele, "r") as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\data_set " + str(folder_count) + "\\ExpertPlus " + str(expert_plus_data_count) + " - song " + str(music_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_plus_data_count += 1

                elif ele == 'Expert.dat':
                    
                    with open(x[0] + "\\" + ele, "r") as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\data_set " + str(folder_count) + "\\Expert " + str(expert_data_count) + " - song " + str(music_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_data_count += 1

                # music
                elif ".egg" in ele or ".ogg" in ele:
                    if take_music:
                        time_1 = time.time()

                        music_path = x[0] + "/" + ele
                        song = self.audio_collector.collect_music(music_path)

                        with open(self.data_dir + "\\data_set " + str(folder_count) + "\\song " + str(music_count), "wb") as music_data:
                            pickle.dump(song, music_data)

                        time_2 = time.time()
                        print("New music data created : ", ele.split(".")[0], music_count,  ", took :", round(time_2 - time_1, 2), "s / total :",
                              round(time_2 - time_start, 2), "s")

            if take_music:
                folder_count += 1

        time_end = time.time()
        print("Expert map collected :", expert_data_count)
        print("ExpertPlus map collected :", expert_plus_data_count)
        print("Successfully created", expert_data_count + expert_plus_data_count, "notes data")

        print("Collected", music_count + 1, "musics")
        print("Created", folder_count, "folders")
        print("Took", round(time_end - time_start, 2), "s")

    def load_data(self, count=1, len_data=10, note_per_s=5, freq=1000):
        # len_data : in seconds
        if count == -1:  # not up to date
            for x in os.walk(self.data_dir):
                for data_set in x[1]:
                    for (_, _, map_data) in os.walk(self.data_dir + "/" + data_set):
                        for data_file in map_data:

                            if "Expert" in data_file:
                                with open(self.data_dir + "/" + data_set + "/" + data_file, "rb") as notes_file:
                                    note_data = pickle.load(notes_file)

                                for (path, d_names, files_names) in os.walk(self.data_dir):
                                    for file in files_names:
                                        if file == data_file.split("- ")[-1]:
                                            with open(self.data_dir + "/" + data_set + "/" + file, "rb") as song_file:
                                                song_data = pickle.load(song_file)

                                            yield note_data, song_data
        else:
            for x in os.walk(self.data_dir):
                for data_set in x[1]:
                    for (_, _, map_data) in os.walk(self.data_dir + "/" + data_set):
                        for data_file in map_data:

                            if "Expert" in data_file:
                                if count <= 0:
                                    break
                                with open(self.data_dir + "/" + data_set + "/" + data_file, "rb") as notes_file:
                                    note_data = pickle.load(notes_file)

                                for (path, d_names, files_names) in os.walk(self.data_dir):
                                    for file in files_names:
                                        if file == data_file.split("- ")[-1]:
                                            with open(self.data_dir + "/" + data_set + "/" + file, "rb") as song_file:
                                                song_data = pickle.load(song_file)

                                            # now we have the song data and the notes data
                                            # we are going to split them in more usable data of chosen length

                                            go_next_note_data = False
                                            time_limit = len(song_data) / 1000
                                            time_counter = 0
                                            previous_index = 0
                                            for index, note in enumerate(note_data):
                                                if count <= 0:
                                                    break
                                                if not go_next_note_data:
                                                    if float(note[0]) >= time_limit:
                                                        go_next_note_data = True
                                                    if float(note[0]) - time_counter >= len_data:
                                                        time_counter += len_data

                                                        notes_limit = note_data[previous_index:index]
                                                        previous_index = index
                                                        if len(notes_limit) < len_data * note_per_s:
                                                            for i in range(len_data * note_per_s - len(notes_limit)):
                                                                notes_limit.append([0, 0, 0, 0, 0])
                                                        else:
                                                            notes_limit = notes_limit[:len_data * note_per_s]

                                                        for i in range(len(notes_limit)):
                                                            try:
                                                                notes_limit[i][0] = float(notes_limit[i][0]) % len_data
                                                                notes_limit[i][1] = int(notes_limit[i][1])
                                                                notes_limit[i][2] = int(notes_limit[i][2])
                                                                notes_limit[i][3] = int(notes_limit[i][3])
                                                                notes_limit[i][4] = int(notes_limit[i][4])
                                                            except ValueError:
                                                                """print(notes_limit[i][4])
                                                                print('indice :', i)
                                                                print("pos note :", index)
                                                                print("note :", note)
                                                                print("file :", notes_file)"""
                                                                notes_limit[i][4] = 0
                                                                # I don't know why but in the file data set 143 the expert 124 has 20 broken notes


                                                        song_limit = song_data[count * len_data * freq:(count + 1) * len_data * freq]
                                                        len_song_limit = len(song_limit)
                                                        size_song = len_data * freq

                                                        if len_song_limit < size_song:
                                                            song_limit = np.append(song_limit, np.zeros(size_song - len_song_limit))

                                                        yield song_limit, notes_limit
                                                        count -= 1

    def get_data_amount(self, len_data=10):  # NOT WORKING
        data_count = 0
        for x in os.walk(self.data_dir):
            for data_set in x[1]:
                for (_, _, map_data) in os.walk(self.data_dir + "/" + data_set):
                    for data_file in map_data:

                        if "Expert" in data_file:
                            with open(self.data_dir + "/" + data_set + "/" + data_file, "rb") as notes_file:
                                note_data = pickle.load(notes_file)

                            for (path, d_names, files_names) in os.walk(self.data_dir):
                                for file in files_names:
                                    if file == data_file.split("- ")[-1]:
                                        with open(self.data_dir + "/" + data_set + "/" + file, "rb") as song_file:
                                            song_data = pickle.load(song_file)

                                        # now we have the song data and the notes data
                                        # we are going to split them in more usable data of chosen length

                                        time_counter = 0
                                        previous_index = 0
                                        for index, note in enumerate(note_data):
                                            if float(note[0]) - time_counter >= len_data:
                                                time_counter += len_data

                                                data_count += 1
        return data_count


NC = NoteCollector("H:/CustomLevels", "H:/map data")
# NC.collect()
# print(NC.get_data_amount())

"""count = 0
for (song, notes) in NC.load_data(30, 10, 2):
    print(notes)
    count += 1

print(count)
"""