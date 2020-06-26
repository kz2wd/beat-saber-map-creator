class ParameterDataCollector:

    def __init__(self):
        self.note_added = 0
        self.music_segment_with_notes_added = 0
        self.song_data_removed = 0
        self.average_note_value_wt = 0  # average of the sum of all value in a note without the time
        self.average_note = []


P_data_collect = ParameterDataCollector()

