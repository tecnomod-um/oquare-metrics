#!/bin/bash

# Inputs
contents_folder=$1
ontology_folders=$2
ignore_files=$3
ontology_files=$4
reasoner=$5
model_plot=$6
characteristics_plot=$7
subcharacteristics_plot=$8
metrics_plot=$9
shift
release=$9
shift
if [ $release == 'true' ]
then
    evolution_plot=$9
else
    evolution_plot='false'
fi



if [ -z "$(ls -A ./$contents_folder/results)" ] || [ $release == 'true' ]
then
    date="$(date +%Y-%m-%d_%H-%M-%S)"
    for ontology_source in $ontology_folders
    do
        if [ -d "$ontology_source" ]
        then
            find $ontology_source -maxdepth 1 -type f \( -name "*.rdf" -o -name "*.owl" -o -name "*.ttl" -o -name "*.nt" -o -name "*.n3" -o -name "*.jsonld" \) | while read file
            do
                outputFile=$(basename "$file")
                if [ -z $(printf '%s\n' "$ignore_files" | grep -Fx "$file")] && [ -z $(printf '%s\n' "$ontology_files" | grep -Fx "$file")]
                then
                    outputFile=$(basename "$file")
                    outputFile="${outputFile%.*}" 
                    mkdir -p $contents_folder/temp_results/$ontology_source/$outputFile/$date/metrics
                    mkdir -p $contents_folder/temp_results/$ontology_source/$outputFile/$date/img
                    outputFilePath="$contents_folder/temp_results/$ontology_source/$outputFile/$date/metrics/$outputFile.xml"
                    java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$file" --reasoner "$reasoner" --outputFile "$outputFilePath"
                    
                    if [ -f "$outputFilePath" ]
                    then
                        python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $ontology_source -f $outputFile -d $date \
                            -M $model_plot -c $characteristics_plot -S $subcharacteristics_plot -m $metrics_plot -e $evolution_plot
                    fi
                fi
            done
        fi
    done

    for ontology_file in $ontology_files
    do
        if [ -f "$ontology_file" ]
        then
            dir=$(dirname "$ontology_file")
            outputFile=$(basename "$ontology_file")
            outputFile="${outputFile%.*}"
            mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/metrics
            mkdir -p $contents_folder/temp_results/$dir/$outputFile/$date/img
            outputFilePath="$contents_folder/temp_results/$dir/$outputFile/$date/metrics/$outputFile.xml"
            java -jar $GITHUB_ACTION_PATH/libs/oquare-versions.jar --ontology "$ontology_file" --reasoner "$reasoner" --outputFile "$outputFilePath"

            if [ -f "$outputFilePath" ]
            then
                python $GITHUB_ACTION_PATH/src/main.py -i $contents_folder -s $dir -f $outputFile -d $date \
                    -M $model_plot -c $characteristics_plot -S $subcharacteristics_plot -m $metrics_plot -e $evolution_plot
            fi
        fi
    done
fi