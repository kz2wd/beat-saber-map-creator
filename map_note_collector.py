import os
import sys
import pickle
import time

import audio_analysis
import numpy as np

import parameter_data_collector as pdc


class NoteCollector:
    def __init__(self, maps_directory, data_dir):
        self.maps_directory = maps_directory
        self.data_dir = data_dir
        self.audio_collector = audio_analysis.AudioCollector()

        self.info_data = None
        self.count = None
        self.len_data = None
        self.note_per_s = None
        self.freq = None
        self.song_data = None

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

                            with open(self.data_dir + "\\data_set " + str(folder_count) + "\\ExpertPlus " + str(expert_plus_data_count),  'wb') as data_file:
                                pickle.dump(notes, data_file)

                        expert_plus_data_count += 1

                    elif ele == 'Expert.dat':

                        with open(x[0] + "\\" + ele, "r") as f:
                            notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                            notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                            notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                            with open(self.data_dir + "\\data_set " + str(folder_count) + "\\Expert " + str(expert_data_count),  'wb') as data_file:
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

                    elif "info" in ele:

                        with open(x[0] + "\\" + ele, "r") as f:
                            try:
                                bpm = int(f.read().split("\"_beatsPerMinute\":")[-1].split(",")[0])
                            except ValueError:
                                print("error in :", self.data_dir + "\\data_set " + str(folder_count))
                                print("due to :", x[2])

                            map_info = [bpm]

                            with open(self.data_dir + "\\data_set " + str(folder_count) + "\\info file",  'wb') as data_file:
                                pickle.dump(map_info, data_file)

                if take_music:
                    folder_count += 1

        time_end = time.time()
        print("Expert map collected :", expert_data_count)
        print("ExpertPlus map collected :", expert_plus_data_count)
        print("Successfully created", expert_data_count + expert_plus_data_count, "notes data")

        print("Collected", music_count + 1, "musics")
        print("Created", folder_count, "folders")
        print("Took", round(time_end - time_start, 2), "s")

    def load_data_old(self, count=1, len_data=10, note_per_s=5, freq=1000):
        for x in os.walk(self.data_dir):
            for data_set in x[1]:
                for (_, _, map_data) in os.walk(self.data_dir + "/" + data_set):
                    for data_file in map_data:

                        if "Expert" in data_file:
                            if count <= 0:
                                break
                            with open(self.data_dir + "/" + data_set + "/" + data_file, "rb") as notes_file:
                                note_data = pickle.load(notes_file)

                            song_collected = False
                            info_collected = False
                            for (path, d_names, files_names) in os.walk(self.data_dir):
                                for file in files_names:

                                    if "song" in file:
                                        with open(path + "/" + file, "rb") as song_file:
                                            song_data = pickle.load(song_file)
                                            song_collected = True

                                    if "info file" in file:
                                        with open(path + "/" + file, "rb") as info_file:
                                            info_data = pickle.load(info_file)
                                            info_collected = True

                                        # now we have the song data and the notes data
                                        # we are going to split them in more usable data of chosen length

                                    if song_collected and info_collected:
                                        beat_per_s = info_data[0] / 60  # bpm / 60 = beat per second
                                        go_next_note_data = False
                                        time_limit = len(song_data) / freq * beat_per_s
                                        time_to_add = len_data * beat_per_s
                                        time_counter = 0
                                        previous_index = 0
                                        for index, note in enumerate(note_data):
                                            if count <= 0:
                                                break
                                            if not go_next_note_data:
                                                if float(note[0]) >= time_limit:
                                                    go_next_note_data = True
                                                if float(note[0]) - time_counter >= time_to_add:
                                                    time_counter += time_to_add

                                                    notes_limit = note_data[previous_index:index]
                                                    previous_index = index
                                                    if len(notes_limit) < len_data * note_per_s:
                                                        for i in range(len_data * note_per_s - len(notes_limit)):
                                                            notes_limit.append([0, 0, 0, 0, 0])
                                                    else:
                                                        notes_limit = notes_limit[:len_data * note_per_s]

                                                    for i in range(len(notes_limit)):
                                                        try:
                                                            notes_limit[i][0] = float(notes_limit[i][0]) % time_to_add
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

                                                    yield song_limit, notes_limit, info_data
                                                    count -= 1

    def load_data(self, count=1, len_data=10, note_per_s=5, freq=1000):
        self.count = count
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq

        for (path, folders, files) in os.walk(self.data_dir):

            expert_collected = False
            expertplus_collected = False
            song_collected = False
            info_collected = False

            for data_file in files:
                if "Expert" in data_file and "Plus" not in data_file:  # check for expert
                    with open(path + "/" + data_file, "rb") as notes_file:
                        expert_note_data = pickle.load(notes_file)
                        expert_collected = True

                if "ExpertPlus" in data_file:  # check for expert plus
                    with open(path + "/" + data_file, "rb") as notes_file:
                        expertplus_note_data = pickle.load(notes_file)
                        expertplus_collected = True

                if "song" in data_file:
                    with open(path + "/" + data_file, "rb") as song_file:
                        self.song_data = pickle.load(song_file)
                        song_collected = True

                if "info file" in data_file:
                    with open(path + "/" + data_file, "rb") as info_file:
                        self.info_data = pickle.load(info_file)
                        info_collected = True

                    # now we have the song data and the notes data
                    # we are going to split them in more usable data of chosen length

            if song_collected and info_collected:
                if expert_collected:
                    for data in self.proceed_data(expert_note_data):
                        yield data

                if expertplus_collected:
                    for data in self.proceed_data(expertplus_note_data):
                        yield data

    def proceed_data(self, difficulty_note_data):
        beat_per_s = self.info_data[0] / 60  # bpm / 60 = beat per second

        beat_limit = self.len_data * beat_per_s

        song_parts_counter = 0

        beat_counter = 0
        previous_index = 0

        for index, note in enumerate(difficulty_note_data):

            if self.count <= 0:
                break

            # if there is a note past the 'batch' we are creating, create it
            if float(note[0]) - beat_counter >= beat_limit:
                beat_counter += beat_limit

                notes_limit = difficulty_note_data[previous_index:index]
                previous_index = index

                len_notes_limit = len(notes_limit)

                # convert str to float or int
                for i in range(len(notes_limit)):
                    try:
                        notes_limit[i][0] = float(notes_limit[i][0]) % beat_limit
                        notes_limit[i][1] = int(notes_limit[i][1])
                        notes_limit[i][2] = int(notes_limit[i][2])
                        notes_limit[i][3] = int(notes_limit[i][3])
                        notes_limit[i][4] = int(notes_limit[i][4])
                    except ValueError:
                        notes_limit[i][4] = 0
                        # it may happens that a note doesn't have a beat time
                        # maybe, fix it in the data creation

                # let's make the length of the list the good size
                if len_notes_limit < self.len_data * self.note_per_s:
                    # prevent from having too short list
                    nbr_note_to_add = self.len_data * self.note_per_s - len_notes_limit
                    for i in range(nbr_note_to_add):
                        notes_limit.append([0, 0, 0, 0, 0])
                    # adding notes at the end of the list may not be the best solution
                    # maybe think about inserting elements inside the list and not only at the end

                    # DATA COLLECTING
                    pdc.P_data_collect.note_added += nbr_note_to_add

                else:
                    # prevent from having too long list
                    notes_limit = notes_limit[
                                  :self.len_data * self.note_per_s]  # cutting may not be the best solution
                    # maybe think about popping elements inside the list and not only the end

                # now, our notes are good, let's do the song part
                song_limit = self.song_data[
                             song_parts_counter * self.len_data * self.freq:(song_parts_counter + 1) * self.len_data * self.freq]
                # we just have to reduce the length of the song because it can't be too short
                """explanation :
                If you take 30 sec of data, and your music is 20 sec long, what will happen is
                that, the note part won't be created if there is no note past the length of data you
                choose, and so there will be no song to return.

                So now with a real example, if you take 30 sec of data, and your music is 2 min and 20
                sec long, you will create 4 batches of data, and then, because there is no notes after
                the 5th, it won't be created."""

                yield song_limit, notes_limit, self.info_data
                self.count -= 1
                song_parts_counter += 1


NC = NoteCollector("H:/bd/project beat saber folders/CustomLevels", "H:/bd/project beat saber folders/map data")
# NC.collect()

# check averrage (i did that fast)
"""
averages = [0, 0, 0, 0, 0]

my_nbs = []
h = 0
for (song, notes, info) in NC.load_data(5000, 10, 1):
    for note in notes:
        my_nbs.append([])
        for i in range(5):
            my_nbs[h].append(note[i])
        h += 1

sums = [0, 0, 0, 0, 0]
length = len(my_nbs)
for nb in my_nbs:
    for j in range(5):
        sums[j] += nb[j]

for i in range(5):
    sums[i] /= length

print(sums)

"""