# inputs : 30 s of audio at 1000Hz : 30 000
# outputs : average of 5 notes / s, a note is 5 values : 750

# First try with 10 s based data

import torch
import torchvision
from torchvision import transforms, datasets

import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim

import map_note_collector as mnc

mnc.NC.load_data()

trainset =


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(10000, 3000)
        self.fc2 = nn.Linear(3000, 1500)
        self.fc3 = nn.Linear(1500, 1500)
        self.fc4 = nn.Linear(1500, 250)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return F.log_softmax(x, dim=1)


net = Net()
print(net)

X = torch.rand(10000)
X = X.view(-1, 10000)
print(X)

output = net(X)


optimizer = optim.Adam(net.parameters(), lr=0.001)

EPOCHS = 3

for epoch in range(EPOCHS):
    for data in trainset:
        pass





