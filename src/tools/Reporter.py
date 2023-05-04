class readmeGen:

    def append_characteristics(self, file_name: str, path: str):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE characteristics values\n')
        readme_file.write('Each characteristic has a value on a scale of 1 to 5, indicating how good the ontology is for each characteristics\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_characteristics_values.png"/>\n')
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

    def append_subcharacteristics(self, file_name: str, path: str, characteristics: list):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE subcharacteristics metrics\n')
        readme_file.write('Each characteristic has a set of subcharacteristics with metrics on a scale of 1 to 5, which makes up the characteristics end value\n\n')
        readme_file.write('<p align="center" width="100%">\n')

        for characteristic in characteristics:
            readme_file.write('\t<img width="600px" style="object-fit: scale;" src="img/' + file_name + '_' + characteristic + '_subcharacteristics_metrics.png"/>\n')
        
        readme_file.write('</p>\n\n')
        readme_file.close()
        
    
    def append_subcharacteristics_evolution(self, file_name: str, path: str, characteristics: list):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE subcharacteristics metrics evolution\n')
        readme_file.write('Evolution of each characteristic subcharacteristics values overtime on a scale of 1 to 5\n\n')
        readme_file.write('<p align="center" width="100%">\n')

        for characteristic in characteristics:
            readme_file.write('\t<img width="600px" style="object-fit: scale;" src="img/' + file_name + '_' + characteristic + '_subcharacteristics_evolution.png"/>\n')
        
        readme_file.write('</p>\n\n')
        readme_file.close()
    
    def append_characteristics_evolution(self, file_name: str, path: str, ):
        readme_file = open(path + '/README.md', 'a')
        readme_file.write('## OQuaRE characteristics evolution\n')
        readme_file.write('Evolution of each characteristic overtime on a scale of 1 to 5\n\n')
        readme_file.write('<p align="center" width="100%">\n')
        readme_file.write('\t<img src="img/' + file_name + '_characteristics_evolution.png"/>\n')
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