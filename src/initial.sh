#!/bin/bash

# Inputs
contents_folder=$1
ontology_folders=$2
ignore_files=$3
ontology_files=$4
reasoner=$5
model_plot=$6
category_plot=$7
subcategory_plot=$8
metrics_plot=$9
shift
evolution_plot=$9


if [ -z "$(ls -A ./$contents_folder/results)" ]
then
    date="$(date +%Y-%m-%d_%H-%M-%S)"
    for ontology_source in $ontology_folders
    do
    if [ -d "$ontology_source" ]
    then
        find $ontology_source -maxdepth 1 -type f -name "*.owl" | while read file
        do
        outputFile=$(basename "$file")
        if [ -z $(printf '%s\n' "$ignore_files" | grep -Fx $file)] && [ -z $(printf '%s\n' "$ontology_files" | grep -Fx $file)]
        then
            outputFile=$(basename "$file" .owl) 
            mkdir -p $contents_folder/temp_results/$ontology_source/$outputFile/$date/metrics
            mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/img
            outputFilePath="$contents_folder/temp_results/$ontology_source/$outputFile/$date/metrics/$outputFile.xml"
            java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$file" --reasoner "$reasoner" --outputFile "$outputFilePath"
            

            python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $ontology_source -f $outputFile -d $date \
                -M $model_plot -c $category_plot -S $subcategory_plot -m $metrics_plot -e $evolution_plot

        fi
        done
    fi
    done

    for ontology_file in $ontology_files
    do
    if [ -f "$ontology_file" ]
    then
        dir=$(dirname "$ontology_file")
        outputFile=$(basename "$ontology_file" .owl)
        mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/metrics
        mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/img
        outputFilePath="$contents_folder/temp_results/$dir/$outputFile/$date/metrics/$outputFile.xml"
        rm -f "$outputFilePath"
        rm -f "$contents_folder/temp_results/$dir/$outputFile/$date/README.md"
        java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$ontology_file" --reasoner "$reasoner" --outputFile "$outputFilePath"

        python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $dir -f $outputFile -d $date \
            -M $model_plot -c $category_plot -S $subcategory_plot -m $metrics_plot -e $evolution_plot

    fi
    done

    if [ "$(ls -A ./$contents_folder/temp_results)" ] 
    then
    mv -v $contents_folder/temp_results/* $contents_folder/results/
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add $contents_folder/
    git commit -m "Ontology metrics calculated - OQuaRE"
    git push
    fi
fi