import argparse

from tqdm import tqdm

def main(args):
    with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
        for line in tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True):
            cols = line.split('\t')
            if len(cols) == 4: # ms-marco
                docid, url, title, body = cols
                body = ' '.join(body.strip().split(' ')[:args.words])
                print(docid, url, title, body, sep='\t', file=outfile)
            elif len(cols) == 7: # hdct
                qid, query, docid, url, title, body, zo = cols
                body = ' '.join(body.strip().split(' ')[:args.words])
                print(qid, query, docid, url, title, body, zo.strip(), sep='\t', file=outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trim MS-MARCO docs')
    parser.add_argument('-i', '--input', required=True, help='original MS-MARCO docs as tsv file')
    parser.add_argument('-o', '--output', required=True, help='trimmed MS-MARCO docs as tsv file')
    parser.add_argument('-w', '--words', type=int, required=True, help='number of words in trimmed body')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    args = parser.parse_args()
    main(args)
