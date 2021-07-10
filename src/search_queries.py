import argparse
import itertools
import json

from elasticsearch import Elasticsearch
from tqdm import tqdm

def main(args):
    client = Elasticsearch()

    if args.query_type == 'cosine':
        query_obj = {
            'script_score': {
                'query': {
                    'match_all': {}
                },
                'script': {
                    'source': 'cosineSimilarity(params.emb, "emb") + 1.0',
                    'params': {
                        'emb': None
                    }
                }
            }
        }

    elif args.query_type == 'match':
        query_obj = {
            'match': {
                'body': None
            }
        }

    elif args.query_type == 'rematch':
        query_obj = {
            'bool': {
                'must': {
                    'match': {
                        'body': None
                    },
                },
                'filter': {
                    'term': {
                        'qid': None
                    }
                }
            }
        }

    elif args.query_type == 'rerank':
        query_obj = {
            'script_score': {
                'query': {
                    'bool': {
                        'filter': {
                            'term': {
                                'qid': None
                            }
                        }
                    }
                },
                'script': {
                    'source': 'cosineSimilarity(params.emb, "emb") + 1.0',
                    'params': {
                        'emb': None
                    }
                }
            }
        }

    else:
        assert False

    with open(args.input, 'r') as infile, open(args.output, 'w') as outfile:
        for line in tqdm(infile, desc=args.input, total=args.count, miniters=1, maxinterval=1, unit='', unit_scale=True):
            query = json.loads(line)

            if args.query_type == 'cosine':
                query_obj['script_score']['script']['params']['emb'] = query['emb']

            elif args.query_type == 'match':
                query_obj['match']['body'] = query['query']

            elif args.query_type == 'rematch':
                query_obj['bool']['must']['match']['body'] = query['query']
                query_obj['bool']['filter']['term']['qid'] = query['qid']

            elif args.query_type == 'rerank':
                query_obj['script_score']['query']['bool']['filter']['term']['qid'] = query['qid']
                query_obj['script_score']['script']['params']['emb'] = query['emb']

            else:
                assert False

            response = client.search(
                    index = args.name,
                    body = {
                        '_source': ['docid'],
                        'size': args.size,
                        'query': query_obj
                    })
            json.dump(response, outfile)
            outfile.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search ElasticSearch index for queries given as jsonl file')
    parser.add_argument('-i', '--input', required=True, help='jsonl file of queries')
    parser.add_argument('-o', '--output', required=True, help='jsonl file of results as json docs')
    parser.add_argument('-q', '--query-type', required=True, help='cosine | match | rematch | rerank')
    parser.add_argument('-n', '--name', required=True, help='index name')
    parser.add_argument('-s', '--size', required=True, type=int, help='number of hits to return')
    parser.add_argument('-c', '--count', type=int, default=None, help='count of items in input')
    args = parser.parse_args()
    main(args)
