You though it was a read me, but it was me ! The logs !


18/06/2020 : Im back again on the project. The main problem is that the map is wrongly generated.
My latest test show that the neural network return almost only 0's.
I will try to get at least one field working, like time used to, then maybe change the data to fit more.

Update : It was due to the moving of the files, i didn't modified correctly the paths, so there where no training data.
Now let's visualize the time factor. There is still the problem with the other field returning almost every time 0, when we expect number from 0 to 7 and we have only few 1 and 2.

So time is going okay, it grow linearly.
To fix the other fields problem's, I have though of different solutions.
We could create 5 different neural networks, one for each field, so they wouldn't be influenced.
It could allow us to build more complex map as it will require less RAM if we use them one by one.
But on the other hand, it would make this mess much more a mess, and would be way harder to manage.
So the other idea i have is to multiply some field in order to increase or decrease the value of the number in it to make it have less or more influence.
The way I see the problem is that the time is way bigger than the other field. In order to get the most accuracy, the network only try to have a good time and put the other value to 0.
I could also be the fault of the filling part of the code that just places note full of 0.
Ok, enough talking, I try this and i'll come back. 

First time with the field factor, doesn't seem the change anything.
Ok I forgot to rebuild and retrain.
Our data seems to be way more chaotic and degenerated, the time is still kind of growing well but I think this is only due to the manual increase.
However it doesn't fixed the initial problem. Still nothing bigger than 3, except time of course.

So I will undo the factor field because it only add complexity. I push it on github and delete it.
We are back at the start but we have more knowledge. I think the problem come from the training data.
I think that everything work very well but the training data are ruining everything somehow.
Now the focus is to inspect those training data.

22/06/2020 : I'm back, let's visualize the training data. They seem correct.
This mean our problem is somewhere else.
What i'm going to do is to try with other music.
I don't think this is fixing it.
I think the problem come from my neural network.
There is 2 things I can do still.
Change my data and change my network.
I think it could help if I find a better way to work with my data but the idea behind the network is that he have to treat them itself.
So we are going to change the network.
What I can change is the optimizer, the size of it, and maybe, what could be the most effective is adding my function to the layer.
Indeed, instead of using a simple linear for the last layer, i want to make all parameters except time an int.
Learning pytorch stuff can only help I guess.

25 / 06 / 2020 : I decided to try to do a side project. The goal is to build a neural network that guess when notes should be placed in a song to make a beat saber map.
This will allow us to make a simpler neural network in order to have a better understanding of how it work and how to use pytorch.
It might also be useful later if we use it. At this moment, a map will have a number of notes depending on the note per second and not really when it need one.

26/06/2020 : Doing a side project is stupid, I will encounter the same problems and it won't be as efficient as directly fixing was is wrong in our neural network.
I'll fix this. Somewhere, somehow, might be an issue, or a way to make this work.
I might be looking at the wrong place, I remember that before I fixed the time and the beat per minute problem, some maps used to have a lot variety of notes.
There were broken of course, but they were kind of interesting.
I tried with EPOCHS at 20 and got better result.
So what I will try is to give a way to the neural network to 'disable' a note.
Now, the notes added to the song when they don't have enough will be filled with -1 and not 0.
Also, if a created note is filled with -1, it will be removed.
I did it and it changed nothing.

It seems like we don't have enough information to know were to go.
I need to know the influence of each parameter on the network, and also if his size is good.

Let's start with my parameters.
Here is a list of them :
- number of note added
- number of song for input data removed because of a wrong shape
- number of music segment with notes added
- the average of the sum of the notes except the time
- the average note

Ok guys I found the problem while I was implementing this. Eventually, I would have seen it in the statistic.
I don't really want to talk about it but it was because I was referring to the wrong variable.
In map_note_collector.py, at the line 324, I was using expert_note_data instead of expertplus_note_data.
So about 1/3 of my data was like [0, 0, 0, 0, 0] ...
But it is good now. And we are going in the good direction.
