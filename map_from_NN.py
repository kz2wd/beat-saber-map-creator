import torch
import numpy as np

from NN_stuff.NN_2 import neural_network_class as nnc, neural_network_trainer as nnt

# switch NN_1 to NN_2 to change model, don't forget to check the size of data

import audio_analysis


class NotesFromMusic:
    def __init__(self, music_path, bpm, len_data=nnt.LEN_DATA, note_per_s=nnt.NOTE_PER_S, freq=nnt.FREQ):
        self.music_path = music_path
        self.bpm = bpm
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
        # print(self.song_data)

    def music_to_notes(self):
        data_size = self.len_data * self.freq
        self.song_data = np.append(self.song_data, np.zeros(data_size - len(self.song_data) % data_size))
        print(self.song_data.shape)
        
        song_parts = np.split(self.song_data, len(self.song_data) / data_size)
        notes = []
        for song_part in song_parts:
            song_part = np.insert(song_part, 0, self.bpm)
            X = torch.Tensor(song_part).view(-1, data_size + 1).to(self.device)  # CAUTION TO SIZE
            notes.append(self.nn_model(X))
            np_notes = np.array([])
            for i in range(len(notes)):
                np_notes = np.append(np_notes, notes[i].cpu().detach().numpy())

        np_notes = np.split(np_notes, len(np_notes) / 5)
        notes = []
        i = 0
        to_add = 0
        time_to_add = self.len_data * self.bpm / 60
        time_batch = self.len_data * self.note_per_s
        for note in np_notes:
            i += 1
            if i == time_batch:
                to_add += time_to_add
                i = 0
            # if note[0] > 0 and note[1] > 0 and note[2] > 0 and note[3] > 0 and note[4] > 0:
            notes.append([round(abs(float(note[0])) + to_add, 1), min(abs(int(note[1])), 4), min(abs(int(note[2])), 4), min(abs(int(note[3])), 2), min(abs(int(note[4])), 8)])
            # notes.append([round(abs(float(note[0])) + to_add, 1), abs(int(note[1])) % 4, abs(int(note[2])) % 4, abs(int(note[3])) % 2, abs(int(note[4])) % 8])
            #notes.append([note[0] + to_add, note[1], note[2], note[3],note[4]])

        notes = sorted(notes)

        return notes

    def clean_notes(self, notes, gap=1):  # not working
        print("Clean_notes is not working, don't use it yet")
        # gap between note in second
        note_time = 3
        adjust = 0
        for i, note in enumerate(notes):

            if note[0] - note_time < gap:
                notes.pop(i - adjust)
                adjust += 1
            else:
                note_time = notes[i - adjust][0]

        print("Removed ", adjust, "Notes")
        return notes


"""
converter = NotesFromMusic("H:/Grind and Hustle - Droeloe.egg")
converter.music_to_notes()

"""
