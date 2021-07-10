# Deep Language Models for Semantic Search in Full-text Search Engines

2021 summer internship project completed at Samsung Electronics Co., Ltd., South Korea

---

## Introduction

Enterprise search engines such as Apache Solr and ElasticSearch (both of which are based on the Apache Lucene Java library) are industry standards for large scale distributed full-text search. However, these platforms use traditional text-matching based algorithms and therefore can't support semantic search out of the box, where user intent is more important than the keywords used to express the search query. With recent advancements in Natural Language Processing, particularly the Tranformer based language models such as Google's BERT, it has been possible to support semantic text similarity search like never before. Deep Learning research is advancing at a tremendous pace and more recent techniques are showing even better promise for semantic text search.

## Goal

My internship project was to explore these advancements in the field and to evaluate the different techniques with the aim of suggesting the best alternatives. An important requirement was to be show how to use these techniques along with the production-level search engines like Apache Solr and ElasticSearch mentioned earlier. This addresses the divide between academic research and industrial deployment. I was able to identify, implement and evaluate the most promising methods leading to a successful completion of the internship goal.

## Contents

This repo contains all the code I wrote in the process along with the final internship presentation describing the problem, methodology, findings, recommedations, etc. I have deliberately avoided links and citations in either this README or the project presentation. Links tend to die and for most purposes I felt a web search of the terms involved would be much more informative to the reader than any links I may provide.

## Code

All the important code is present as python scripts with command-line interfaces implemented using the lovely `argparse` library. So a description will be available by using the `-h` flag when calling the respective scripts. Even though the code and the directory structure used are not heavily documented, the code itself is well-written, readable and easily understandable. Further the `run.sh` script which I used to evaluate the models is also provided, which makes the entire pipeline crystal-clear.

## Environment

For evaluation I use the implementation used officially by TREC: `trec_eval` (available online). The pre-trained PyTorch models were downloaded from the Huggingface Model Hub (`nboost/pt-tinybert-msmarco`, `nboost/pt-bert-base-uncased-msmarco`, `castorini/ance-msmarco-doc-firstp`, `castorini/ance-msmarco-doc-maxp`) or from the links provided in the official implementations (for PROP model and HDCT retrieved top-100 MS-MARCO docs) depending on availability. I used a conda environment for the project. This has been exported as `environment.yml`. For ElasticSearch, I ran a pre-configured server using a Docker container. The `docker-compose.yml` file is provided. `docker compose up` in the same directory starts the ElasticSearch server with the required port bindings and creates its own Docker volume for indexing and search purposes.
