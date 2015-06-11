# Exercise 2: words

> Write some code that will, give a word, e.g. dog, and another word, e.g. cat, will output a sequence of valid words (in a dictionary), where each pair of adjacent words are only different by 1 character. e.g. dog -> dot -> cot -> cat. If you can, also output the entire list of all such paths between two words.


# Requirements

Python 3.4+

# Solution

## Finding the adjacent words

In order to find all the adjacent words efficiently, a [trie](http://en.wikipedia.org/wiki/Trie) is built with all the words of the dictionary. It is a common data structure for string lookups.
The index is built by `index.py` and persisted into a file through python [`pickle`](https://docs.python.org/3.4/library/pickle.html) serialization.

The adjacent words lookup algorithm uses an adapted version of the [Levenshtein distance](http://en.wikipedia.org/wiki/Levenshtein_distance) function for trie traversal that stops when the distance is bigger than 1.

## Searching the word sequence

The program uses a graph where the nodes are the words and each of them is connected with their adjacent words.

It is traversed with [BFS](http://en.wikipedia.org/wiki/Breadth-first_search) and a
[heap](http://en.wikipedia.org/wiki/Heap_%28data_structure%29) as a [priority queue](http://en.wikipedia.org/wiki/Priority_queue) in order to find the shortests paths first.


# Usage

By default the program uses the [Unix `words`](http://en.wikipedia.org/wiki/Words_%28Unix%29) standard file (~1 MB) as the dictionary.

## Index

In first place we need to build the index from the dictionary:

```bash
python index.py --verbose
# Trie built in 1.42521 s
# Index saved in 0.575739 s
```

## Query

Now we can search:

```bash
python query.py dog cat --limit 10 --verbose
# Index loaded in 0.9412 s
# dog -> cog -> cot -> cat
# dog -> dot -> cot -> cat
# dog -> cog -> cot -> coat -> cat
# dog -> dot -> cot -> coat -> cat
# dog -> cog -> cot -> cut -> cat
# dog -> dot -> cot -> cut -> cat
# dog -> cog -> cob -> cab -> cat
# dog -> cog -> cod -> cad -> cat
# dog -> cog -> con -> can -> cat
# dog -> cog -> cop -> cap -> cat
# Search finished in 0.584854 s

```

```bash
python query.py cat dog -l 1
# cat -> cot -> cog -> dog
```


## Testing

Tests are built with the python unit testing framework

```bash
python test.py
# ......
# ----------------------------------------------------------------------
# Ran 6 tests in 0.010s
#
# OK
```

# Example with Don Quixote

Don Quixote is a Spanish novel published in 1605 and written by Miguel de Cervantes.
In plain text it is about 2 MB.

```bash
# Download the book and split words into lines
curl http://www.gutenberg.org/cache/epub/2000/pg2000.txt | \
  grep -o '[[:alpha:]]*' > quixote.in

python index.py --dict quixote.in --index index/quixote.pickle -v
# Trie built in 1.63081 s
# Index saved in 0.152427 s

python query.py lugar mancha -l 50 --index index/quixote.pickle -v > sample.out
# Index loaded in 0.167227 s
# Search finished in 13.2537 s
wc -l sample.out
# 100 sample.out
head sample.out
# lugar -> lunar -> luna -> lana -> mana -> manca -> mancha
# lugar -> lunar -> luna -> lana -> mana -> manda -> manca -> mancha
# lugar -> lunar -> luna -> lana -> mana -> manga -> manca -> mancha
# lugar -> lunar -> luna -> lana -> mana -> mansa -> manca -> mancha
# lugar -> lunar -> luna -> lana -> mana -> manta -> manca -> mancha
# lugar -> lunar -> luna -> lana -> gana -> mana -> manca -> mancha
# lugar -> lunar -> luna -> lana -> rana -> mana -> manca -> mancha
# lugar -> lunar -> luna -> lana -> sana -> mana -> manca -> mancha
# lugar -> lunar -> luna -> lana -> vana -> mana -> manca -> mancha
# lugar -> lunar -> luna -> lana -> mana -> manca -> marca -> marcha -> mancha
```
