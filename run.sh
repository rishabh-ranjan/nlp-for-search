#!/usr/bin/env bash
set -e

N=20		# queries
TOPK=100	# retrieved docs per query
B=64		# embedding batch-size
C=3213835	# total docs in MS-MARCO
K=100		# chunk size for parallel bulk loading
T=2		# threads

eval "$( conda shell.bash hook )"
conda activate samsung-intern

for NAME in tinybert ance-maxp prop bert-base ance-firstp bert-large
do

for BASE in ms-marco hdct
do

set +x
echo
echo ===
echo NAME: $NAME
echo BASE: $BASE
echo ---

Q_TSV=ms-marco/msmarco-docdev-queries.$N.tsv
Q_JSONL=gen/$BASE+$NAME/queries.$N.jsonl
M_PATH=models/$NAME
B_SSV=$BASE/trec.$N.ssv
D_JSONL=gen/$BASE+$NAME/docs.$N.jsonl
D_TSV=ms-marco/msmarco-docs.trim_50.tsv
I_JSON=src/index_rerank.json
I_NAME=$BASE+$NAME.$N
R_JSONL=gen/$BASE+$NAME/results.$N.jsonl
T_SSV=gen/$BASE+$NAME/trec.$N.ssv
T_TSV=ms-marco/msmarco-docdev-qrels.tsv
E_TXT=gen/$BASE+$NAME/eval.$N.txt

mkdir -p gen/$BASE+$NAME

PS4='\n\033[1;34m[$(date +%H:%M:%S)]\033[0m '
set -x

python3 src/make_queries.py -i $Q_TSV -o $Q_JSONL -q rerank -m $M_PATH -c $N -b $B -t $T

python3 src/make_docs.py -i $B_SSV -o $D_JSONL -q rerank -d $D_TSV -m $M_PATH -c $(( N * TOPK )) -C $C -b $B -t $T

python3 src/make_index.py -i $I_JSON -n $I_NAME

python3 src/index_docs.py -i $D_JSONL -n $I_NAME -c $(( N * TOPK )) -t $T -k $K

python3 src/search_queries.py -i $Q_JSONL -o $R_JSONL -q rerank -n $I_NAME -s $TOPK -c $N

python3 src/make_trec.py -i $R_JSONL -o $T_SSV -q $Q_JSONL -c $N

trec_eval/trec_eval $T_TSV $T_SSV > $E_TXT

cat $E_TXT

done
done
