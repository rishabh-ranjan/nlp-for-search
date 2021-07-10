import argparse
import itertools
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from tqdm import tqdm

def main(args):
    actions = []
    with open(args.input, 'r') as infile:
        for line in tqdm(infile, desc=args.input, total=args.count, unit='', unit_scale=True):
            action = json.loads(line)
            action['_op_type'] = 'index'
            action['_index'] = args.name
            actions.append(action)

    client = Elasticsearch(timeout=60, max_retries=10, retry_on_timeout=True)
    for _ in tqdm(parallel_bulk(client, actions, refresh='wait_for', thread_count=args.threads, chunk_size=args.chunk_size),
            desc='parallel bulk', total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add ElasticSearch json docs to existing ElasticSearch index')
    parser.add_argument('-i', '--input', required=True, help='ElasticSearch docs as jsonl file')
    parser.add_argument('-n', '--name', required=True, help='ElasticSearch index name')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    parser.add_argument('-t', '--threads', type=int, default=2, help='threads for parallel bulk loading')
    parser.add_argument('-k', '--chunk-size', type=int, default=100, help='chunk size for parallel bulk loading')
    args = parser.parse_args()
    main(args)
