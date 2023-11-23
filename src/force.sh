#!/bin/bash

# Inputs
contents_folder=$1
force_parse=$2
reasoner=$3
model_plot=$4
characteristics_plot=$5
subcharacteristics_plot=$6
metrics_plot=$7
evolution_plot=$8
modified_files=$9

date="$(date +%Y-%m-%d_%H-%M-%S)"
for file in $force_parse
do
    if [ -z "$(printf '%s\n' "$modified_files" | grep -Fx "$file")" ]
    then
        dir=$(dirname "$file")
        outputFile=$(basename "$file")
        outputFile="${outputFile%.*}"

        # Remove folder if it exist. It will override results obtained on previous steps if the situation occurs.

        rm -rf $contents_folder/temp_results/$dir/$outputFile
        mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/metrics
        mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/img
        outputFilePath="$contents_folder/temp_results/$dir/$outputFile/$date/metrics/$outputFile.xml"
        java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$file" --reasoner "$reasoner" --outputFile "$outputFilePath"

        if [ -f "$outputFilePath" ]
        then
            python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $dir -f $outputFile -d $date \
                -M $model_plot -c $characteristics_plot -S $subcharacteristics_plot -m $metrics_plot -e $evolution_plot
        fi
    fi
done