# Exercise 1: topN

> Write a program, topN, that given an arbitrarily large file and a number, N, containing individual numbers on each line (e.g. 200Gb file), will output the largest N numbers, highest first. Tell me about the run time/space complexity of it, and whether you think there's room for improvement in your approach.


# Complexity

## Runtime

1. Given a list of `M` numbers, read the first `N` numbers and create a priority queue with them.
2. For each remaining number (`M-N`):
  1. If it is greater than the last number of the queue: `O(1)`
    1. Remove the last number in the queue: `O(log N)`
    2. Insert the current number in its sorted position: `O(log N)`

Total complexity: **`O(M log(N))`**

## Space

The program only needs keep the list of the largest `N` numbers: **`O(N)`**


# Improvements

If we knew the amount of numbers (`M`) contained in the file before starting the algorithm we could check if `M <= N` and in that case run a sorting algorithm like quicksort over the whole file instead using the priority queue approach.

Also if the numbers in the file were byte-encoded instead in ASCII, the file would be processed faster.

# Requirements

Python 3.4+

# Usage

The main program is `topn.py`.

```
usage: topn.py [-h] N

Output N largest numbers from the input, highest first.

positional arguments:
  N           Amount of numbers to extract from the list.

optional arguments:
  -h, --help  show this help message and exit
```

## Example

```bash
python topn.py 2 << EOF
5
2
7
-4
EOF
# 7
# 5
```

`generator.py` is a script that helps creating sample files of a given size (in MB). By default outputs a random number per line until it reaches 100MB.

```bash
python generator.py > sample.in
ls -lh sample.in
# -rw-rw-r-- 1 finn finn 101M Jun  7 12:25 sample.in
wc -l sample.in
# 8135440 sample.in
tail sample.in
# 541855440073
# 363559583058
# 135547599532
# 880318202358
# 104644134337
# 687389829385
# 695289411441
# 45780076021
# 435696289502
# 133588668494
```

So, if we want to get the top 100 largest numbers from 10MB of random numbers:

```bash
python generator.py -s 10 | time python topn.py 100 > sample.out
# python topn.py 100 > sample.out  0.75s user 0.02s system 19% cpu 3.984 total
wc -l sample.out
# 100 sample.out
head sample.out
# 999999104753
# 999998232450
# 999997673931
# 999995638866
# 999995591080
# 999994686085
# 999993942255
# 999991785145
# 999991293681
# 999990697761

```

And the top 1000 largest numbers from 200GB of random numbers:

```bash
python generator.py -s $(( 200*1024 )) | time python topn.py 1000 > sample.out
# 100659.00user 3293.17system 272:22:00elapsed 10%CPU (0avgtext+0avgdata 7232maxresident)k
# 0inputs+32outputs (0major+1934minor)pagefaults 0swaps

wc -l sample.out
# 1000 sample.out

head sample.out
# 999999999974
# 999999999956
# 999999999912
# 999999999901
# 999999999867
# 999999999846
# 999999999697
# 999999999626
# 999999999607
# 999999999433

tail sample.out
# 999999942391
# 999999942387
# 999999942273
# 999999942270
# 999999942236
# 999999942142
# 999999942052
# 999999941829
# 999999941719
# 999999941642
```

It took 980520 seconds (~11 days) on a Amazon EC2 `t2.micro` instance, but the CPU load was only 10%.
Looks like the generator is a bottleneck.



## Testing

Tests are built with the python unit testing framework

```bash
python test.py
# ....
# ----------------------------------------------------------------------
# Ran 4 tests in 1.819s
#
# OK
```
