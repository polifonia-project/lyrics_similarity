import argparse
import os, pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_matrices(input, folder1, lyrics1, folder2, lyrics2):
    in_file = os.path.join(input, folder1, lyrics1 + '.pkl')
    with open(in_file, 'rb') as fr:
        song1_emb = pickle.load(fr)
    in_file = os.path.join(input, folder2, lyrics2 + '.pkl')
    with open(in_file, 'rb') as fr:
        song2_emb = pickle.load(fr)
    return song1_emb, song2_emb


def overall_sim(input, folder1, folder2, lyrics1, lyrics2):
    song1_emb, song2_emb = get_matrices(input, folder1, lyrics1, folder2, lyrics2)
    matrix1 = np.array([song1_emb[k]['embedding'].tolist() for k in song1_emb.keys()])
    matrix2 = np.array([song2_emb[k]['embedding'].tolist() for k in song2_emb.keys()])
    vector1 = np.mean(matrix1, axis=0)
    vector2 = np.mean(matrix2, axis=0)
    sim = cosine_similarity(np.array([vector1.tolist(), vector2.tolist()]))[0,1]
    print('The overall similarity between the two lyrics is {}'.format(sim))
    return sim

def sim(input, folder1, folder2, lyrics1, lyrics2, min_similarity):
    song1_emb, song2_emb = get_matrices(input, folder1, lyrics1, folder2, lyrics2)
    matrix1 = np.array([song1_emb[k]['embedding'].tolist() for k in song1_emb.keys()])
    matrix2 = np.array([song2_emb[k]['embedding'].tolist() for k in song2_emb.keys()])
    sim_mat = cosine_similarity(matrix1, matrix2)
    similarities = np.where(sim_mat > min_similarity)
    print('Found {} similar lines:'.format(len(similarities[0])))
    for x, y in zip(similarities[0],similarities[1]):
        print(sim_mat[x, y])
        print(song1_emb[x]['line'])
        print(song2_emb[y]['line'])
        print('')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='embeddings')
    parser.add_argument('--folder1', type=str)
    parser.add_argument('--folder2', type=str)
    parser.add_argument('--lyrics1', type=str)
    parser.add_argument('--lyrics2', type=str)
    parser.add_argument('--min_similarity', type=float, default=.75)
    parser.add_argument('--sim_type', type=str, default='sentence')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.sim_type == 'sentence':
        sim(args.input, args.folder1, args.folder2, args.lyrics1, args.lyrics2, args.min_similarity)
    if args.sim_type == 'overall':
        overall_sim(args.input, args.folder1, args.folder2, args.lyrics1, args.lyrics2)


# Queen__Breakthru
# Queen__A Kind Of Magic