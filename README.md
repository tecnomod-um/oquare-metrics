# oquare-metrics

A module to automatically obtain and save metrics from ontology files based of OQuaRE framework for ontology quality evaluation, generating visual reports which showcase the quality of each ontology and saving them within the repository itself

## OQuaRE

OQuaRE is a framework developed by Astrid Duque Ramos which defines an ontology evaluation system based on ISO/IEC 25000:2005 (SQuaRE), which is presented as an ontology quality evaluation adapted to software quality standard SQuaRE which allows trazability within requirements and metrics of an ontology, with the goal of measuring in an objetive and reproducible way its characteristics as well as bringin assitance to users and developers in taking informed decisions

This module makes use of said framework to bring its capabilities to ontology repositories hosted in GitHub, so that users may evaluate ontologies making use of an stadardized system.

## Features

* Robust tool for ontology metrics, based of OQuaRE framework for ontology quality evaluation
* Easy to configure and use on both existing and new pipelines
* Compatible with Docker
* Set of different reports, showcasing different aspects of the quality of each ontology
* Archive of metrics generated from previous versions of ontologies contained within the repository.
* Visual representation of how modifications done to an ontology affect the quality of that ontology.
* Restrict folders to scan for ontologies on a repository
* Two different ontology reasoners for ontology metrics calculation (ELK and HermiT)

## Usage
> NOTE: :warning:
> 
> * **IMPORTANT:** Currently you must have both Java and Python installed in the runner machine. This can be done by either a Docker image which has both, or by calling actions/setup-java and actions/setup-python
> * The module has been tested to work under Java 8 Temurin Distribution as well as Python 3.9.4
> * By default the module will search for ontologies on ./ontologies from the repository, and will also save the generated contents in a folder named ./OQuaRE

```yaml
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    name: Evaluate ontologies
    steps:
      - uses: actions/checkout@v2
      # Configuration
      # Java setup
      - uses: actions/setup-java@v2
        with:
          distribution: 'temurin'
          java-version: '8'
      # Python setup
      - uses: actions/setup-python@v3
        with:
          python-version: '3.9'
          
      - name: OQuaRE module
        uses: Emdien/oquare-metrics@v0.0.16 
```

## Inputs

| Input           | Type   | Required | Default      | Description                                                                                      |
|-----------------|--------|----------|--------------|--------------------------------------------------------------------------------------------------|
| ontology-folder | string | true     | 'ontologies' | Sets the folder to search ontologies within the repository                                      |
| contents-folder | string | true     | 'OQuaRE'     | Sets the folder on which the module will save all generated content                              |
| reasoner        | string | true     | 'ELK'        | Sets the reasoner to be used when evaluating an ontology                                         |
| category-plots  | string (ELK/HERMIT) | false    | 'true'       | Indicates the module to generate category values plots                                           |
| model-plot      | string | false    | 'true'       | Indicates the module to generate OQuaRE model value plot                                         |
| archive-plot    | string | false    | 'false'      | Indicates the module to generate OQuaRE model value plot across the latest 20 version of metrics |

## Examples

```yaml
          
    # Assuming that the ontologies that we want to evaluate are stored on src/ontologies/production
    # And we want to store the metrics on src/ontologies/metrics
    - name: Ontology folder configuration
    uses: Emdien/oquare-metrics@v0.0.16 
    with:
        ontology-folder: src/ontologies/production
        contents-folder: src/ontologies/metrics
    
    # Setting up a different reasoner
    - name: Ontology folder configuration
    uses: Emdien/oquare-metrics@v0.0.16 
    with:
        reasoner: HERMIT

    # Only generate model and archive plots, but not categories
    - name: Ontology folder configuration
    uses: Emdien/oquare-metrics@v0.0.16 
    with:
        category-plots: 'false'
        model-plot: 'true'
        archive-plot: 'true'
  
```

## Results

TODO

## Known Limitations

> * Currently there is no way to set multiple ontology source folders to search ontologies on the repository. This feature is currently being worked on
> * Currently there is no way to exclude certain files with .owl extension from the module file search.
> * The module currently requires of previous, first hand setup of Java and Python. This is done so there is no compatibility issues with some Docker images

## Bug Report

For bug report, you can contact the following emals: (TODO)
* email1@um.es
* email2@um.es
