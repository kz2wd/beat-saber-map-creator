import os
import sys
import pickle


class NoteCollector:
    def __init__(self, maps_directory, data_dir):
        self.maps_directory = maps_directory
        self.data_dir = data_dir

    def collect(self):

        expert_data_count = 0
        expert_plus_data_count = 0

        for x in os.walk(self.maps_directory):

            for ele in x[2]:
                if ele == 'ExpertPlus.dat':

                    with open(x[0] + "\\" + ele) as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\ExpertPlus " + str(expert_plus_data_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_plus_data_count += 1

                elif ele == 'Expert.dat':
                    
                    with open(x[0] + "\\" + ele) as f:
                        notes = f.read().split("_notes")[-1].split("_obstacles")[0].replace("\"", "").split("{")[1:]
                        notes = [[nt.split(":") for nt in note.split(",")[:5]] for note in notes]

                        notes = [[note[0][1], note[1][1],  note[2][1],  note[3][1],  note[4][1][0]] for note in notes]

                        with open(self.data_dir + "\\Expert " + str(expert_data_count),  'wb') as data_file:
                            pickle.dump(notes, data_file)

                    expert_data_count += 1

        print("Expert map collected :", expert_data_count)
        print("ExpertPlus map collected :", expert_plus_data_count)
        print("Successfully created", expert_data_count + expert_plus_data_count, "data")


NC = NoteCollector("H:/CustomLevels", "H:/map data")
NC.collect()
