import random


class RandomCreator:
    def __init__(self, note_per_second, length_in_second, bpm):
        bps = bpm / 60
        nbr_of_notes = note_per_second * length_in_second
        self.beat_saber_map = [[i * bps / note_per_second, random.randint(0, 3), random.randint(0, 3), random.randint(0, 1), random.randint(0, 7)]for i in nbr_of_notes]