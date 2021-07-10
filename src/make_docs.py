import argparse
import json

import torch
from tqdm import tqdm

from embed import Embedder

def main(args):
    if args.query_type == 'cosine':
        torch.set_num_threads(args.threads)
        embedder = Embedder(args.model_path)

        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:

            def flush(buf):
                docids, bodies = zip(*buf)
                buf.clear()
                embs = embedder(list(bodies))
                for docid, emb in zip(docids, embs):
                    json.dump({
                        'docid': docid,
                        'emb': emb
                    }, outfile)
                    outfile.write('\n')

            buf = []
            for line in tqdm(infile, desc=args.input, total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
                docid, _, _, body = line.split('\t')
                buf.append((docid, body))
                if len(buf) == args.batch_size:
                    flush(buf)
            if buf:
                flush(buf)

    elif args.query_type == 'match':
        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
            for line in tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True):
                docid, _, _, body = line.split('\t')
                json.dump({
                    'docid': docid,
                    'body': body
                }, outfile)
                outfile.write('\n')

    elif args.query_type == 'rematch':
        docid_to_body = {}
        with open(args.docs, 'r') as docsfile:
            for line in tqdm(docsfile, desc=args.docs, total=args.docs_count, unit='', unit_scale=True):
                docid, _, _, body = line.split('\t')
                docid_to_body[docid] = body

        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
            for line in tqdm(infile, desc=args.input, total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
                qid, _, docid, _, _, _ = line.split(' ')
                json.dump({
                    'qid': qid,
                    'docid': docid,
                    'body': docid_to_body[docid]
                }, outfile)
                outfile.write('\n')

    elif args.query_type == 'rerank':
        torch.set_num_threads(args.threads)
        embedder = Embedder(args.model_path)

        docid_to_body = {}
        with open(args.docs, 'r') as docsfile:
            for line in tqdm(docsfile, desc=args.docs, total=args.docs_count, unit='', unit_scale=True):
                docid, _, _, body = line.split('\t')
                docid_to_body[docid] = body

        with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:

            def flush(buf):
                qids, docids, bodies = zip(*buf)
                buf.clear()
                embs = embedder(list(bodies))
                for qid, docid, emb in zip(qids, docids, embs):
                    json.dump({
                        'qid': qid,
                        'docid': docid,
                        'emb': emb
                    }, outfile)
                    outfile.write('\n')

            buf = []
            for line in tqdm(infile, desc=args.input, total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
                qid, _, docid, _, _, _ = line.split(' ')
                buf.append((qid, docid, docid_to_body[docid]))
                if len(buf) == args.batch_size:
                    flush(buf)
            if buf:
                flush(buf)

    else:
        assert False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process MS-MARCO tsv docs into ElasticSearch json docs with embeddings')
    parser.add_argument('-i', '--input', required=True, help='MS-MARCO docs as tsv file / retrieved docs as trec results file')
    parser.add_argument('-o', '--output', required=True, help='ElasticSearch docs as jsonl file')
    parser.add_argument('-q', '--query-type', required=True, help='cosine | match | rematch | rerank')
    parser.add_argument('-d', '--docs', default=None, help='tsv file with MS-MARCO docs for rerank queries')
    parser.add_argument('-m', '--model-path', default=None, help='path to model directory')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    parser.add_argument('-C', '--docs-count', type=int, default=None, help='count of MS-MARCO docs')
    parser.add_argument('-b', '--batch-size', type=int, default=100, help='number of docs to embed at a time')
    parser.add_argument('-t', '--threads', type=int, default=2, help='threads for pytorch')
    args = parser.parse_args()
    main(args)
