import argparse
import json

from tqdm import tqdm

def main(args):
    if args.input.endswith('.jsonl'):
        with open(args.input, 'r') as infile, open(args.queries, 'r') as qfile, open(args.output, 'w') as outfile:
            for line, qline in zip(tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True), qfile):
                obj = json.loads(line)
                qobj = json.loads(qline)
                for i, hobj in enumerate(obj['hits']['hits']):
                    print(qobj['qid'], 'Q0', hobj['_source']['docid'], i+1, hobj['_score'], 'STANDARD', file=outfile)

    elif args.input.endswith('.tsv'):
        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
            prev_qid = None
            for line in tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True):
                qid, query, docid, url, title, body, zo = line.split('\t')
                if qid != prev_qid:
                    rank = 0
                    prev_qid = qid
                rank += 1
                print(qid, 'Q0', docid, rank, 1/rank, 'STANDARD', file=outfile)

    else:
        assert False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make trec file from json search results')
    parser.add_argument('-i', '--input', required=True, help='jsonl file containing search results / tsv file for hdct')
    parser.add_argument('-o', '--output', required=True, help='trec results file')
    parser.add_argument('-q', '--queries', default=None, help='jsonl file containing queries')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    args = parser.parse_args()
    main(args)
