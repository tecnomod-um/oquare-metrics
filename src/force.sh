#!/bin/bash

# Inputs
contents_folder=$1
force_parse=$2
ignore_files=$3
reasoner=$4
model_plot=$5
features_plot=$6
subfeatures_plot=$7
metrics_plot=$8
evolution_plot=$9

date="$(date +%Y-%m-%d_%H-%M-%S)"
for file in $force_parse
do
    dir=$(dirname "$file")
    outputFile=$(basename "$file" .owl)

    # Remove folder if it exist. It will override results obtained on previous steps if the situation occurs.

    rm -f $contents_folder/temp_results/$dir/$outputFile
    mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/metrics
    mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/img
    outputFilePath="$contents_folder/temp_results/$dir/$outputFile/$date/metrics/$outputFile.xml"
    java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$file" --reasoner "$reasoner" --outputFile "$outputFilePath"

    if [ -f "$outputFilePath" ]
    then
        python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $dir -f $outputFile -d $date \
            -M $model_plot -c $features_plot -S $subfeatures_plot -m $metrics_plot -e $evolution_plot
    fi
done