class readmeGen:

    def append_features(self, file_name: str, path: str):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE features values\n')
        readme_file.write('Each feature has a value on a scale of 1 to 5, indicating how good the ontology is for each features\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_features_values.png"/>\n')
        readme_file.write('</p>\n\n')
        readme_file.close()

    def append_oquare_value(self, file_name: str, path: str):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE model value\n')
        readme_file.write('Represents the quality of the ontology when taking in all the values obtained after evaluation across the latest 20 versions.' 
                        + 'On a scale of 1 to 5, 5 represents the highest quality attainable according to the OQuaRE framework\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_OQuaRE_model_values.png"/>\n')
        readme_file.write('</p>\n\n')
        readme_file.close()

    def append_subfeatures(self, file_name: str, path: str, features: list):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE subfeatures metrics\n')
        readme_file.write('Each feature has a set of subfeatures with metrics on a scale of 1 to 5, which makes up the features end value\n\n')
        readme_file.write('<p align="center" width="100%">\n')

        for feature in features:
            readme_file.write('\t<img width="600px" style="object-fit: scale;" src="img/' + file_name + '_' + feature + '_subfeatures_metrics.png"/>\n')
        
        readme_file.write('</p>\n\n')
        readme_file.close()
        
    
    def append_subfeatures_evolution(self, file_name: str, path: str, features: list):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE subfeatures metrics evolution\n')
        readme_file.write('Evolution of each feature subfeatures values overtime on a scale of 1 to 5\n\n')
        readme_file.write('<p align="center" width="100%">\n')

        for feature in features:
            readme_file.write('\t<img width="600px" style="object-fit: scale;" src="img/' + file_name + '_' + feature + '_subfeatures_evolution.png"/>\n')
        
        readme_file.write('</p>\n\n')
        readme_file.close()
    
    def append_features_evolution(self, file_name: str, path: str, ):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE features evolution\n')
        readme_file.write('Evolution of each feature overtime on a scale of 1 to 5\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_features_evolution.png"/>\n')
        readme_file.write('</p>\n\n')
        readme_file.close()

    def append_metrics(self, file_name: str, path: str): 
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE metrics values\n')
        readme_file.write('Fine grained metrics, lowest level of ontology analysis provided. Scaled version uses a 1 to 5 scale\n\n')
        
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img width="450px" height="350px" src="img/' + file_name + '_metrics.png"/>\n')
        readme_file.write('\t<img width="450px" height="350px" src="img/' + file_name + '_scaled_metrics.png"/>\n')
        readme_file.write('</p>\n\n')

        readme_file.write('<div style="margin: 5px;">\n')
        readme_file.write('<p align="center" width="100%">\n')

        readme_file.write('</p>\n</div>\n</div>\n\n')
        readme_file.close()

    def append_metrics_evolution(self, file_name: str, path: str, metrics: list):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE metrics evolution\n')
        readme_file.write('Evolution of each of the 19 metrics obtained from an ontology\n')
        
        for metric in metrics:
            readme_file.write('<div>\n')
            readme_file.write('<h3 align="center" width="100%">' + metric +' evolution</h3>\n\n')
            readme_file.write('<p align="center" width="100%">\n')
            readme_file.write('\t<img width="615px" style="object-fit: scale;" src="img/' + file_name + '_' + metric + '_metric_evolution.png"/>\n')
            readme_file.write('</p>\n')
            readme_file.write('</div>\n\n')
            readme_file.write
        readme_file.close()
    
    def append_scaled_metrics_evolution(self, file_name: str, path: str):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE scaled metrics evolution\n')
        readme_file.write('Evolution of each of the 19 scaled metrics obtained from an ontology\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_scaled_metrics_evolution.png"/>\n')
        readme_file.write('</p>\n\n')
        readme_file.close()