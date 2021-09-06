# Lyrics similarity
### A simple library to embed lyrics and compute similarities among them
The embedding is computed using *[LASER](https://github.com/yannvgn/laserembeddings)*.

### How to use it
The required packages are listed in *requirements.txt*

*main.py* compute the embeddings. Different parameters can be used.

*sim.py* computes the cosine similarity among all the lines of two lyrics (if `--sim_type sentence` is passed) or the overall similarity (if `--sim_type overall` is passed)   

