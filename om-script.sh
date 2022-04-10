#!/bin/bash

# Setup folders in case they dont exist
mkdir -p ${CONTENTS_FOLDER}
mkdir -p ${CONTENTS_FOLDER}/results
mkdir -p ${CONTENTS_FOLDER}/archives
mkdir -p ${CONTENTS_FOLDER}/temp_results

# Find and copy previous results
if [${ANY_CHANGED} == 'true'] 
then
    cp -r $(find ${CONTENTS_FOLDER}/results/* -maxdepth 0)/* ${CONTENTS_FOLDER}/temp_results
fi

# If any ontology file was renamed, delete nonmatching folders from temp_folder
if [${RENAMED_FILES}] 
then
    comm -13 <(ls -1 ${ONTOLOGY_FOLDER} | sed s/.owl//g) <( ls -1 ${CONTENTS_FOLDER}/temp_results) | while read file 
    do 
        rm -r ${CONTENTS_FOLDER}/temp_results/${file};
    done
fi

# Call oquare library
if [${ANY_CHANGED} == 'true'] 
then
    for file in ${ALL_CHANGED_FILES} 
    do
        outputFile=$(basename "$file" .owl)
        mkdir -p ${CONTENTS_FOLDER}/temp_results/${outputFile}/metrics
        outputFilePath="${CONTENTS_FOLDER}/temp_results/${outputFile}/metrics/${outputFile}.xml"
        rm "$outputFilePath"
        java -jar libs/oquare-versions.jar --ontology "$file" --reasoner "${REASONER}" --outputFile "$outputFilePath"
        python scripts/main.py -i ${CONTENTS_FOLDER} -c -f "$outputFile"
    done
    # Evaluate and plot oquare model value
    python scripts/main.py -i ${CONTENTS_FOLDER} -m

    # Archive previous results
    touch ${CONTENTS_FOLDER}/results/temp_file
    mv -v ${CONTENTS_FOLDER}/results/* ${CONTENTS_FOLDER}/archives/
    rm -f ${CONTENTS_FOLDER}/archives/temp_file

    # Move results to results folder and tag it with a date
    mv ${CONTENTS_FOLDER}/temp_results ${CONTENTS_FOLDER}/results/"$(date +%d-%m-%Y_%H-%M-%S)"
fi

