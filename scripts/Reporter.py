

class readmeGen:

    def append_category(self, file_name: str, path: str):
        readme_file = open(path + file_name + '/' + 'README.md', 'a')
        readme_file.write('# OQuaRE category values\n')
        readme_file.write('Each category has a value on a scale of 1 to 5, indicating how good the ontology is for each category\n\n')
        readme_file.write('![category values plot](' + file_name + '_category_values.png)\n')
        readme_file.close()

    def append_oquare_value(self, path: str):
        readme_file = open(path + '/temp_results/README.md', 'a')
        readme_file.write('# OQuaRE metrics results\n')
        readme_file.write('## OQuaRE model value\n')
        readme_file.write('Represents the quality of the ontology when taking in all the values obtained after evaluation.' 
                        + 'On a scale of 1 to 5, 5 represents the highest quality attainable according to the OQuaRE framework\n\n')
        readme_file.write('![OQuaRE model value plot](OQuaRE_model_values.png)\n')
        readme_file.close()

    def append_oquare_historic(self, path: str, date: str):
        readme_file = open(path + '/results/' + date +'/README.md', 'a')
        readme_file.write('## OQuaRE historic model value\n')
        readme_file.write('Progress of each analyzed ontology across the latest 20 versions on a scale of 1 to 5\n\n')
        readme_file.write('![OQuaRE historic values plot](OQuaRE_historic_model_value.png)\n')
        readme_file.close()

    def append_subcategory(self, file_name: str, path: str, categories: list):
        readme_file = open(path + file_name + '/' + 'README.md', 'a')
        readme_file.write('## OQuaRE subcategories metrics\n')
        readme_file.write('Each category has a set of subcategories with metrics on a scale of 1 to 5, which makes up the category end value\n\n')
        
        for category in categories:
            readme_file.write('![' + category + ' metrics plot](' + file_name + "_" + category + '_metrics.png)\n')
        readme_file.close()
    
    def append_category_evolution(self, path: str):
        readme_file = open(path + '/' + 'README.md', 'a')
        readme_file.write('## OQuaRE category evolution\n')
        readme_file.write('Evolution of each category overtime on a scale of 1 to 5\n\n')
        readme_file.write('![category values plot](categories_evolution.png)\n')
        readme_file.close()


