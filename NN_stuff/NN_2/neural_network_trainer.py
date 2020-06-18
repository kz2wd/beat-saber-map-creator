# inputs : 30 s of audio at 1000Hz : 30 000
# outputs : average of 5 notes / s, a note is 5 values : 750

# First try with 10 s based data

import torch
import torch.nn as nn
import torch.optim as optim

import numpy as np
import matplotlib.pyplot as plt

import NN_stuff.NN_2.data_collector_NN_class as data_collect
import NN_stuff.NN_2.neural_network_class as myNN


LEN_DATA = 10
NOTE_PER_S = 3
FREQ = 1000
DATA_AMOUNT = 10000  # this is the max amount

T = True
F = False

built_data = T
do_train = T
show_data = T
show_time = T

field_factor = [1, 3, 3, 10, 2]

def train(net):
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    BATCH_SIZE = 100
    EPOCHS = 10
    for epoch in range(EPOCHS):
        for i in range(0, len(train_X), BATCH_SIZE):  # from 0, to the len of x, stepping BATCH_SIZE at a time.
            # print(f"{i}:{i+BATCH_SIZE}")
            batch_X = train_X[i:i + BATCH_SIZE].view(-1, FREQ * LEN_DATA + 1)  # 1 = len(info_data)
            batch_y = train_y[i:i + BATCH_SIZE]

            batch_X, batch_y = batch_X.to(device), batch_y.to(device)  # very important line

            net.zero_grad()

            outputs = net(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()  # Does the update


def create_map_from_tests(net, amount=1):
    with torch.no_grad():
        if amount <= len(test_X):
            for i in range(amount):
                net_out = net(test_X[i].view(-1, FREQ * LEN_DATA + 1).to(device))[0]  # 1 = len(info_data)

                yield net_out


if built_data:  # build training data
    data_handler = data_collect.MyDataHandler(LEN_DATA, NOTE_PER_S, FREQ, field_factor)
    data_handler.get_training_data(DATA_AMOUNT)
    print("data built")

if do_train:

    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("Running on the GPU")
    else:
        device = torch.device("cpu")
        print("Running on the CPU")

    net = myNN.Net(LEN_DATA, NOTE_PER_S, FREQ).to(device)
    print(net)

    training_data = np.load("A:/Python/Pycharm project/beat-saber-map-creator/NN_stuff/NN_2/training_data.npy", allow_pickle=True)
    print("Training data length :", len(training_data))

    loss_function = nn.MSELoss()
    X = torch.Tensor([i[0] for i in training_data]).view(-1, FREQ * LEN_DATA + 1)  # 1 = len(info_data)
    y = torch.Tensor([i[1] for i in training_data])

    VAL_PCT = 0.05
    # val_size = int(len(X) * VAL_PCT)
    val_size = 1

    train_X = X[:-val_size]
    train_y = y[:-val_size]

    test_X = X[-val_size:]
    test_y = y[-val_size:]

    train(net)
    print("train done")
    torch.save(net.state_dict(), "A:/Python/Pycharm project/beat-saber-map-creator/NN_stuff/my_network.pth")

    for map_seq in create_map_from_tests(net):
        if show_data:
            np_map_seq = [i for i in map_seq]
            plt.plot(np_map_seq)
            plt.show()

        if show_time:
            np_map_seq = [map_seq[i] for i in range(0, len(map_seq), 5)]
            plt.plot(np_map_seq)
            plt.show()



# net.save_state_dict('mytraining.pt')


