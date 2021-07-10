import argparse

from tqdm import tqdm

def main(args):
    docids = set()
    with open(args.qrels, 'r') as qfile:
        for line in tqdm(qfile, desc=args.qrels, unit='', unit_scale=True):
            _, _, docid, _ = line.split(' ')
            docids.add(docid)

    with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
        for line in tqdm(infile, desc=args.input, unit='', unit_scale=True):
            docid, _, _, _ = line.split('\t')
            if docid in docids:
                outfile.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select all documents appearing in the qrels file')
    parser.add_argument('-i', '--input', required=True, help='ms-marco docs as tsv file')
    parser.add_argument('-q', '--qrels', required=True, help='qrels file')
    parser.add_argument('-o', '--output', required=True, help='selected docs as tsv file')
    args = parser.parse_args()
    main(args)
