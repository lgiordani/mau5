#!/bin/bash

BASE_DIR="e2e"
SOURCE_DIR="${BASE_DIR}/source"
OUTPUT_DIR="${BASE_DIR}/output"
REF_DIR="${BASE_DIR}/ref"

source_files=$(ls ${SOURCE_DIR})

if [[ ! -d ${OUTPUT_DIR} ]]; then mkdir ${OUTPUT_DIR}; fi

rm -fR ${OUTPUT_DIR}/* > /dev/null

for source_file in ${source_files}
do
    echo "Processing ${source_file}"
    
    output_file=${source_file/.mau/.yaml}
    mau -i ${SOURCE_DIR}/${source_file} -f yaml -o ${OUTPUT_DIR}/${output_file}

    echo "Diffing..."
    diff ${REF_DIR}/${output_file} ${OUTPUT_DIR}/${output_file}
done

