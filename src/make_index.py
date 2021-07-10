import argparse
import json

from elasticsearch import Elasticsearch

def main(args):
    client = Elasticsearch()
    client.indices.delete(index=args.name, ignore=[404])
    with open(args.input, 'r') as infile:
        body = json.load(infile)
        if 'tiny' in args.name:
            body['mappings']['properties']['emb']['dims'] = 312
        elif 'large' in args.name:
            body['mappings']['properties']['emb']['dims'] = 1024
        body = json.dumps(body)
        client.indices.create(index=args.name, body=body)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create a fresh ElasticSearch index (deletes old index if present)')
    parser.add_argument('-i', '--input', required=True, help='json file for index')
    parser.add_argument('-n', '--name', required=True, help='index name')
    args = parser.parse_args()
    main(args)
