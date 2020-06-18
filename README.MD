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