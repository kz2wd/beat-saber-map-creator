import torch
import numpy as np

from NN_stuff import neural_network_trainer as nnt
from NN_stuff import neural_network_class as nnc

import audio_analysis


class NotesFromMusic:
    def __init__(self, music_path, len_data=nnt.LEN_DATA, note_per_s=nnt.NOTE_PER_S, freq=nnt.FREQ):
        self.music_path = music_path
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq

        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            print("Running on the GPU")
        else:
            self.device = torch.device("cpu")
            print("Running on the CPU")

        self.nn_model = nnc.Net(self.len_data, self.note_per_s, self.freq).to(self.device)

        self.nn_model.load_state_dict(torch.load("NN_stuff/my_network.pth"))
        self.nn_model.eval()

        self.audio_analyzer = audio_analysis.AudioCollector()
        self.song_data = self.audio_analyzer.collect_music(self.music_path, self.freq)

    def music_to_notes(self):
        data_size = self.len_data * self.freq
        self.song_data = np.append(self.song_data, np.zeros(data_size - len(self.song_data) % data_size))
        
        song_parts = np.split(self.song_data, len(self.song_data) / data_size)
        notes = []
        for song_part in song_parts:
            X = torch.Tensor(song_part).view(-1, data_size).to(self.device)
            notes.append(self.nn_model(X))
            np_notes = np.array([])
            for i in range(len(notes)):
                np_notes = np.append(np_notes, notes[i].cpu().detach().numpy())

        np_notes = np.split(np_notes, len(np_notes) / 5)
        notes = []
        i = 0
        to_add = 0
        time_batch = self.len_data * self.note_per_s
        for note in np_notes:
            i += 1
            if i == time_batch:
                to_add += self.len_data
                i = 0
            notes.append([round((float(note[0]) % self.len_data) + to_add, 1), int(note[1] % 4), int(note[2] % 4), int(note[3] % 2), int(note[4] % 8)])

        notes = sorted(notes)

        return notes

"""
converter = NotesFromMusic("H:/Grind and Hustle - Droeloe.egg")
converter.music_to_notes()

"""
