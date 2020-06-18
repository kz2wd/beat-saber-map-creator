import numpy as np
import map_note_collector as mnc
import random
random.seed(1)


class MyDataHandler:
    def __init__(self, len_data=10, note_per_s=5, freq=1000, field_factor=None):
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq

        if field_factor is None:
            self.field_factor = [1, 1, 1, 1, 1]
        else:
            self.field_factor = field_factor

        self.training_data = []

    def get_training_data(self, amount):
        self.training_data = []
        for (song, notes, info) in mnc.NC.load_data(amount, self.len_data, self.note_per_s, self.freq):
            new_notes = []
            for note in notes:
                # apply field factor
                for i in range(5):
                    note[i] *= self.field_factor[i]

                new_notes += note
            song = np.insert(song, 0, info[0])
            if song.shape == (self.len_data * self.freq + 1,):
                self.training_data.append([song, np.array(new_notes)])

        np.random.shuffle(self.training_data)
        np.save("A:/Python/Pycharm project/beat-saber-map-creator/NN_stuff/NN_2/training_data.npy", self.training_data)
