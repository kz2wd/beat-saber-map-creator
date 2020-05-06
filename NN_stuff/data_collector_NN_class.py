import numpy as np
import map_note_collector as mnc


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
            self.training_data.append([np.insert(song, info[0], 0), np.array(new_notes)])
            # print(new_notes)

        np.random.shuffle(self.training_data)
        np.save("NN_stuff/training_data.npy", self.training_data)
