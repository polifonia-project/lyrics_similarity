from lyrics_sim import *
import csv, tqdm

csv.field_size_limit(131072*2)


def compare(input_folder, type, out_path, files):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(os.path.join(out_path,type+'.tsv'), 'w') as fw:
        writer = csv.writer(fw, delimiter='\t')
        writer.writerow(['hash1', 'hash2', 'folder1', 'folder2', 'artist1', 'artist2', 'title1', 'title2', 'similarity'])
        for fname1 in files:
            with open(os.path.join(input_folder, 'lyrics-' + fname1 + '.csv')) as f1:
                reader = csv.reader(f1, delimiter=',')
                lyrics1 = [row for row in reader]
            for fname2 in files:
                with open(os.path.join(input_folder, 'lyrics-' + fname2 + '.csv')) as f2:
                    reader = csv.reader(f2, delimiter=',')
                    lyrics2 = [row for row in reader]
                for song1 in tqdm.tqdm(lyrics1[1:]):
                    hash1, lang1, folder1, file_1, artist1, title1, lyrics1_ = song1
                    for song2 in tqdm.tqdm(lyrics2[1:]):
                        hash2, lang2, folder2, file_2, artist2, title2, lyrics2_ = song2
                        if hash1 != hash2:
                            similarity = overall_sim('embeddings', fname1, fname2, '__'.join([artist1, title1]).replace('/','_'), '__'.join([artist2, title2]).replace('/','_'))
                            writer.writerow([hash1, hash2, fname1, fname2, artist1, artist2, title1, title2, similarity])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='lyrics')
    parser.add_argument('--type', type=str, default='lyrics')
    parser.add_argument('--output', type=str, default='comparison')
    parser.add_argument('--files', type=list, default=['songfacts', 'genius'])
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    compare(args.input, args.type, args.output, args.files)