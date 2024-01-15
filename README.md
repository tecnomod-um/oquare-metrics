# oquare-metrics

A module to automatically obtain metrics from ontology files based of OQuaRE framework for ontology quality evaluation, generating visual reports which showcase the quality of each ontology 
## OQuaRE

OQuaRE is a framework developed by Astrid Duque Ramos which defines an ontology evaluation system based on ISO/IEC 25000:2005 (SQuaRE), which is presented as an ontology quality evaluation adapted to software quality standard SQuaRE which allows trazability within requirements and metrics of an ontology, with the goal of measuring in an objetive and reproducible way its characteristics as well as bringin assitance to users and developers in taking informed decisions

This module makes use of said framework to bring its capabilities to ontology repositories hosted in GitHub, so that users may evaluate ontologies making use of an stadardized system.

## Important note 13 of October 2023

This repository has been transfered from the personal account of the developer to the tecnomod-um organization, which is part of University of Murcia. 
Current repositories using this Action do NOT need to change the references to this module, as it redirects correctly.
However it is HIGHLY ADVISED to update the reference from Emdien/oquare-metrics to tecnomod-um/oquare-metrics in the future to prevent confusion and possible errors.

## Features

* Robust tool for ontology metrics, based on OQuaRE framework for ontology quality evaluation
* Easy to configure and use on both new and existing pipelines
* Set of different plots and graphs, showcasing different aspects of the quality of each ontology and how modifications affects them
* Multiple ontology source folders
* Two different ontology reasoners for ontology metrics calculation (ELK and HermiT)
* Possibility to ignore certain files that might not want to be parsed
* Individual ontology file parsing instead of by folders
* Out of the box functionality with very little configuration needed

## 15th of January 2024 Update
* Upgraded action dependencies to their latest version (checkout, setup-java v4, setup-python v5)
* Upgraded OQuaRE library to a more recent version (bugfixes, java 17)
* Upgraded action to use Java 17 instead of Java 8

## Usage
> NOTE: :warning:
> 
> * **IMPORTANT:** Currently you must have both Java and Python installed in the runner machine. This can be done by either a Docker image which has both, or by calling actions/setup-java and actions/setup-python
> * This action module creates new files and modifies the repository. Make sure to either allow actions to read and write in the repository, or to add a permissions entry with contents: write.
> * The module has been tested to work under Java 8 and 17 (Temurin Distribution) as well as Python 3.9.4.
> * By default the module will save the generated contents in a folder named ./OQuaRE

```yaml
name: CI

on: [push]

# If repository allows actions write by default, this is not needed.
permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    name: Evaluate ontologies
    steps:
      - uses: actions/checkout@v4
      # Configuration
      # Java setup
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      # Python setup
      - uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          
      - name: OQuaRE module
        uses: tecnomod-um/oquare-metrics@v3.0
        with:
          ontology-folders: ontologies
```
### Release mode example
```yaml

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    name: Evaluate ontologies - release mode
    steps:
      - uses: actions/checkout@v4
      # Configuration
      # Java setup
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      # Python setup
      - uses: actions/setup-python@v3
        with:
          python-version: '3.9'
          
      - name: OQuaRE module
        uses: tecnomod-um/oquare-metrics@v3.0
        with:
          ontology-folders: ontologies
          release: true
```

## Inputs

| Input           | Type   | Required | Default      | Description                                                                                      |
|-----------------|--------|----------|--------------|--------------------------------------------------------------------------------------------------|
| ontology-folders | string | true     | 'ontologies' | Sets the folders to track ontologies. Space separated values, no trailing slash needed          |
| ontology-files  | string | false    | ''           | Set of individual ontologies to parse. Space separated values.                                   |
| contents-folder | string | true     | 'OQuaRE'     | Sets the folder on which the module will save all generated content                              |
| ignore-files    | string | false    | ''           | Set of files that the module will ignore when analysing ontology files. Space separated values   |
| reasoner        | string (ELK/HERMIT) | true     | 'ELK'        | Sets the reasoner to be used when evaluating an ontology                            |
| model-plot      | boolean   | false    |  true        | Indicates the module to plot OQuaRE model metrics                                                |
| feature-plot   | boolean   | false    |  true        | Indicates the module to plot OQuaRE features metrics                                           |
| subfeature-plot  | boolean   | false |  true        | Indicates the module to plot OQuaRE subfeatures metrics                                        |
| metrics-plots   | boolean   | false    |  true        | Indicates the module to plot OQuaRE fine-grained metrics                                         |
| evolution-plot  | boolean   | false    |  true        | Indicates if you want the plotting of the evolution of the previous inputs that are set as True  |
| release         | boolean   | false    | false      | Used to obtain the metrics for all of the ontologies. Intended to be used paired with a on release workflow. DANGER: enabling this on normal runs might cause duplicates and parse non-modified ontologies all the time |

## Examples

```yaml
          
    # Assuming that the ontologies that we want to evaluate are stored on src/ontologies/production and src/ontologies/imports
    # And we want to store the metrics on src/ontologies/metrics
    - name: Ontology folder configuration
    uses: tecnomod-um/oquare-metrics@v3.0
    with:
        ontology-folders: src/ontologies/production src/ontologies/imports
        contents-folder: src/ontologies/metrics
    
    # Setting up a different reasoner
    - name: Ontology reasoner configuration
    uses: tecnomod-um/oquare-metrics@v3.0
    with:
        reasoner: HERMIT

    # Only plot model, subfeatures and metrics but not features and their evolution
    - name: Ontology plots configurtion
    uses: tecnomod-um/oquare-metrics@v3.0
    with:
        feature-plot: false
        evolution-plot: false

    # Ignore src/ontologies/imports/null_ontology.owl since its empty
    # Also parse ontology_file.owl which is stored on the root folder
    - name: Ontology file configuration
    uses: tecnomod-um/oquare-metrics@v3.0
    with:
        ontology-folders: src/ontologies/imports
        ontology-files: ontology_file.owl
        ignore-files: src/ontologies/imports/null_ontology.owl
    
  
```

## Known Limitations

> * The module currently requires of previous, first hand setup of Java and Python. This is done so there is no compatibility issues with some Docker images
> * Currently when doing a release, it will ONLY update master branch. Can't update any other branch or add the commit to the release

## Contact
If there is any issue regarding this action, please contact me on gonzalo.nicolasm@um.es, or make an issue in this repository explaining the error. Thank you!

