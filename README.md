# sqlite3_test
sqlite3 python perfomance testing examples

Hi

Some days ago somebody asked me about sqllite3 and is it possible to use it under multiprocessing.
Hm... I know that sqlite3 shall do such thigs and I've used sqllite before but I didn't tried to pass it through multiprocessing.
Let's double check. I guess my python example could help somebody who interesting in it like me.

Firstly we need to understand that we are taling about multiprocessing but about treading.
That mean we shall use multiprocessing lib. Another things that I'm interesting to do a testing
for several cases. 
1. One reader and one writer
2. Several reader trying to read DB simultaneously 
3. Several writer trying to write to DB simultaneously
4. mixed

OK. let's take a look at source code:

