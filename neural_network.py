# inputs : 30 s of audio at 1000Hz : 30 000
# outputs : average of 5 notes / s, a note is 5 values : 750

# First try with 10 s based data

import torch
import torchvision
from torchvision import transforms, datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np
import matplotlib.pyplot as plt

import map_note_collector as mnc

LEN_DATA = 10
NOTE_PER_S = 3
FREQ = 1000
DATA_AMOUNT = 10000
# data_amount should be at least 20, else, there will be no test data and will return an error

built_data = False


class MyDataHandler:
    def __init__(self, len_data=10, note_per_s=5, freq=1000):
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq
        self.training_data = []

    def get_training_data(self, amount):
        self.training_data = []
        for (song, notes) in mnc.NC.load_data(amount, self.len_data, self.note_per_s, self.freq):
            new_notes = []
            for note in notes:
                new_notes += note
            self.training_data.append([song, np.array(new_notes)])
            # print(new_notes)

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)


class Net(nn.Module):
    def __init__(self, len_data=10, note_per_s=5, freq=1000):
        self.len_data = len_data
        self.note_per_s = note_per_s
        self.freq = freq
        super().__init__()

        self.fc1 = nn.Linear(len_data * freq, 3000)
        self.fc2 = nn.Linear(3000, 1500)
        self.fc3 = nn.Linear(1500, 1500)
        self.fc4 = nn.Linear(1500, self.note_per_s * len_data * 5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return x


if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print("Running on the GPU")
else:
    device = torch.device("cpu")
    print("Running on the CPU")

net = Net(LEN_DATA, NOTE_PER_S, FREQ).to(device)
print(net)



"""X = torch.rand(10000)
X = X.view(-1, 10000)
print(X)

output = net(X)
"""

if built_data:  # build training data
    data_handler = MyDataHandler(LEN_DATA, NOTE_PER_S, FREQ)
    data_handler.get_training_data(DATA_AMOUNT)

training_data = np.load("training_data.npy", allow_pickle=True)
print("Training data length :", len(training_data))

loss_function = nn.MSELoss()
X = torch.Tensor([i[0] for i in training_data]).view(-1, FREQ * LEN_DATA)
y = torch.Tensor([i[1] for i in training_data])

VAL_PCT = 0.05
val_size = int(len(X) * VAL_PCT)


train_X = X[:-val_size]
train_y = y[:-val_size]

test_X = X[-val_size:]
test_y = y[-val_size:]



def train(net):
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    BATCH_SIZE = 100
    EPOCHS = 10
    for epoch in range(EPOCHS):
        for i in range(0, len(train_X), BATCH_SIZE):  # from 0, to the len of x, stepping BATCH_SIZE at a time.
            # print(f"{i}:{i+BATCH_SIZE}")
            batch_X = train_X[i:i + BATCH_SIZE].view(-1, FREQ * LEN_DATA)
            batch_y = train_y[i:i + BATCH_SIZE]

            batch_X, batch_y = batch_X.to(device), batch_y.to(device)

            net.zero_grad()

            outputs = net(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()  # Does the update
    print("loss", loss)

"""            print("batch done")
            print("output", outputs)
        print("\n Epoch done \n")"""



def test(net, amount=1):
    with torch.no_grad():
        if amount <= len(test_X):
            for i in range(amount):
                net_out = net(test_X[i].view(-1, FREQ * LEN_DATA).to(device))[0]

                yield net_out


train(net)
print("train done")

for map_seq in test(net):
    pass

np_map_seq = [i for i in map_seq]
plt.plot(np_map_seq)
plt.show()




