import numpy as np
import map_note_collector as mnc

import parameter_data_collector as pdc

import random
random.seed(1)


# little useful function to check data
def display_data(data):
    for i in range(0, len(data), 5):
        print(" ".join(str(round(data[j + i], 1)) for j in range(5)))


class MyDataHandler:
    def __init__(self, len_data=10, note_per_s=5, freq=1000):
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq

        self.training_data = []

    def get_training_data(self, amount):
        self.training_data = []
        for (song, notes, info) in mnc.NC.load_data(amount, self.len_data, self.note_per_s, self.freq):
            new_notes = []
            for note in notes:
                new_notes += note
            song = np.insert(song, 0, info[0])
            if song.shape == (self.len_data * self.freq + 1,):
                self.training_data.append([song, np.array(new_notes)])
            else:
                # DATA COLLECTING
                pdc.P_data_collect.song_data_removed += 1

        np.random.shuffle(self.training_data)

        # Just before we save it, display some musics

        """ for i in range(5):
            display_data(self.training_data[i][1])
        """
        np.save("A:/Python/Pycharm project/beat-saber-map-creator/NN_stuff/NN_2/training_data.npy", self.training_data)
