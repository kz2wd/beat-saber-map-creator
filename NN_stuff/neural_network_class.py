import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, len_data=10, note_per_s=5, freq=1000):
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq
        super().__init__()

        self.fc1 = nn.Linear(len_data * freq + 1, 3000)  # + 1 for the bpm value
        self.fc2 = nn.Linear(3000, 1500)
        self.fc3 = nn.Linear(1500, 1500)
        self.fc4 = nn.Linear(1500, self.note_per_s * len_data * 5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return x

