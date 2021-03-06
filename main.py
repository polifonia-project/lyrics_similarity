import argparse
import os, csv, tqdm, pickle, re, urllib
from laserembeddings import Laser

csv.field_size_limit(131072*2)

def embedder(lines):
    model = Laser()
    return model.embed_sentences(lines, lang='en')


def clean_lines(lyrics, min_line_len):
    lines = lyrics.split('\n')
    lines = [re.sub(' +', ' ', line).strip() for line in lines]
    lines = [line for line in lines if
             len(line) > min_line_len and
             line.startswith(('Lyrics licensed', 'Publisher: ', 'Writer/s: ')) == False]
    return lines

def update_files():
    urllib.request.urlretrieve('https://github.com/polifonia-project/sonar2021_demo/raw/datasets/output/lyrics-genius.csv',
                       'lyrics/lyrics-genius.csv')
    urllib.request.urlretrieve('https://github.com/polifonia-project/sonar2021_demo/raw/datasets/output/lyrics-songfacts.csv',
                       'lyrics/lyrics-songfacts.csv')

def embed(input_folder, output_folder, files, update_files_, min_line_len):
    if update_files_ == True:
        update_files()
    for fname in files:
        out_path = os.path.join(output_folder, fname)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        with open(os.path.join(input_folder, 'lyrics-' + fname +'.csv')) as f:
            reader = csv.reader(f, delimiter=',')
            lyrics = [row for row in reader]
        for song in tqdm.tqdm(lyrics[1:]):
            hash, lang, folder, file_, artist, title, lyrics = song
            out_file = os.path.join(out_path, '__'.join([artist, title]).replace('/','_')+'.pkl')
            if not os.path.exists(out_file):
                lines = clean_lines(lyrics, min_line_len)
                embeddings = embedder(lines)
                song_emb = {}
                for i, line in enumerate(lines):
                    song_emb.setdefault(i, {})
                    song_emb[i]['line'] = line
                    song_emb[i]['embedding'] = embeddings[i]
                with open(out_file, 'wb') as fw:
                    pickle.dump(song_emb, fw)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='lyrics')
    parser.add_argument('--output', type=str, default='embeddings')
    parser.add_argument('--files', type=list, default=['songfacts', 'genius'])
    parser.add_argument('--update_files', type=bool, default=False)
    parser.add_argument('--min_line_len', type=int, default=10)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    embed(args.input, args.output, args.files, args.update_files, args.min_line_len)