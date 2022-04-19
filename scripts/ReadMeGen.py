

class readmeGen:

    def append_category(self, fileName: str, path: str):
        readme_file = open(path + '/temp_results/'+ fileName + '/' + 'README.md', 'a')
        readme_file.write('# OQuaRE category values  ')
        readme_file.write('![category values plot](' + fileName + 'category_values.png)  ')
        readme_file.write('Each category has a value on a scale of 1 to 5, indicating how good the ontology is for each category  ')
        readme_file.close()

    def append_oquare_value(self, path: str):
        readme_file = open(path + '/temp_results/README.md', 'a')
        readme_file.write('# OQuaRE metrics results  ')
        readme_file.write('## OQuaRE model value  ')
        readme_file.write('![OQuaRE model value plot](OQuaRE_model_values.png)  ')
        readme_file.write('\nRepresents the quality of the ontology when taking in all the values obtained after evaluation.' 
                        + 'On a scale of 1 to 5, 5 represents the highest quality attainable according to the OQuaRE framework  ')
        readme_file.close()

    def append_oquare_historic(self, path: str, date: str):
        readme_file = open(path + '/results/' + date +'/README.md', 'a')
        readme_file.write('## OQuaRE historic model value  ')
        readme_file.write('![OQuaRE historic values plot](OQuaRE_historic_model_value.png)  ')
        readme_file.write('Progress of each analyzed ontology across the latest 20 versions on a scale of 1 to 5  ')
        readme_file.close()

