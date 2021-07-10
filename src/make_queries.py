import argparse
import json

import torch
from tqdm import tqdm

from embed import Embedder

def main(args):
    if args.query_type == 'cosine' or args.query_type == 'rerank':
        torch.set_num_threads(args.threads)
        embedder = Embedder(args.model_path)

        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:

            def flush(buf):
                qids, queries = zip(*buf)
                buf.clear()
                embs = embedder(list(queries))
                for qid, emb in zip(qids, embs):
                    json.dump({
                        'qid': qid,
                        'emb': emb
                    }, outfile)
                    outfile.write('\n')

            buf = []
            for line in tqdm(infile, desc=args.input, total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
                buf.append(line.split('\t'))
                if len(buf) == args.batch_size:
                    flush(buf)
            if buf:
                flush(buf)

    elif args.query_type == 'match' or args.query_type == 'rematch':
        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
            for line in tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True):
                qid, query = line.split('\t')
                json.dump({
                    'qid': qid,
                    'query': query
                }, outfile)
                outfile.write('\n')

    else:
        assert False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MS-MARCO queries to json queries with embeddings')
    parser.add_argument('-i', '--input', required=True, help='tsv file with MS-MARCO queries')
    parser.add_argument('-o', '--output', required=True, help='jsonl output file')
    parser.add_argument('-q', '--query-type', required=True, help='cosine | match | rematch | rerank')
    parser.add_argument('-m', '--model-path', default=None, help='path to model directory')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    parser.add_argument('-b', '--batch-size', type=int, default=32, help='number of docs to embed at a time')
    parser.add_argument('-t', '--threads', type=int, default=4, help='threads for pytorch')
    args = parser.parse_args()
    main(args)
