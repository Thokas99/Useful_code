#!/bin/bash
set -euo pipefail

INDEX="$HOME/ssd2/t.sirchi/alevin_fry/GRCh38_2024A_splici_piscem_idx/index/piscem_idx"
T2G="$HOME/ssd2/t.sirchi/alevin_fry/GRCh38_2024A_splici/splici_fl146_t2g_3col.tsv"
R1_DIR="$HOME/ssd2/t.sirchi/alevin_fry/Fastq1_link"
R2_DIR="$HOME/ssd2/t.sirchi/alevin_fry/Fastq2_link"
OUTBASE="$HOME/ssd2/t.sirchi/alevin_fry/quant_out"

for SAMPLE in ROC-25-0074 ROC-25-0075 ROC-25-0076 ROC-25-0077; do

    echo "===== Processing $SAMPLE ====="

    simpleaf quant \
        --reads1 ${R1_DIR}/${SAMPLE}_R1.fastq.gz \
        --reads2 ${R2_DIR}/${SAMPLE}_R2.fastq.gz \
        --index  ${INDEX} \
        --t2g-map ${T2G} \
        --chemistry 10xv3 \
        --resolution cr-like \
        --expected-ori fw \
        --threads 16 \
        --knee \
        --output ${OUTBASE}/${SAMPLE}

done
