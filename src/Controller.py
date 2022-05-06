
import glob
import os
from pprint import pprint
import sys
from tools.Plotter import oquareGraphs
from tools.Parser import MetricsParser
from tools.Reporter import readmeGen


class Controller:

    def __init__(self):
        self.graphPlotter = oquareGraphs()
        self.readmeGenerator = readmeGen()

    def handle_categories(self, temp_path: str, file: str) -> None:
        oquare_category_values = {}

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            for category, values in categories.items():
                oquare_category_values[category] = values.get('value')
            
            self.graphPlotter.plot_oquare_categories(oquare_category_values, file, temp_path)
            self.graphPlotter.plot_oquare_subcategories(categories, file, temp_path)
            self.readmeGenerator.append_category(file, temp_path)
            self.readmeGenerator.append_subcategory(file, temp_path, list(categories.keys()))

        except FileNotFoundError as e:
            print("Error CATEGORY PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()
    
    def handle_oquare_model(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        archive_path = input_path + '\\archives\\'
        results_path = input_path + '\\results\\'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        oquare_model_values = {}


        archive_list = sorted(glob.glob(archive_path + ontology_source + '\\' + file + '/*/' + 'metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            entry = path.rsplit(archive_path + ontology_source + '\\' + file + '\\', 1)[1]
            archive_date = entry.rsplit('\\')[0]

            parsed_metrics = MetricsParser(path)
            oquare_model_values[archive_date] = parsed_metrics.parse_oquare_value()
        

        results_file_path = glob.glob(results_path + ontology_source + '\\' + file + '/*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            entry = results_file_path.rsplit(archive_path + ontology_source + '\\' + file + '\\', 1)[1]
            results_date = entry.rsplit('\\')[0]

            parsed_metrics = MetricsParser(results_file_path)
            oquare_model_values[results_date] = parsed_metrics.parse_oquare_value()

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            oquare_model_values[date] = parsed_metrics.parse_oquare_value()

            self.graphPlotter.plot_oquare_values(oquare_model_values, temp_path)
            self.readmeGenerator.append_oquare_value(temp_path)
            
        except FileNotFoundError as e:
            print("Error MODEL PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()    
        
    def handle_category_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:

        archive_path = input_path + '\\archives\\'
        results_path = input_path + '\\results\\'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        category_evolution = {}

        archive_list = sorted(glob.glob(archive_path + ontology_source + '\\' + file + '/*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            entry = path.rsplit(archive_path + ontology_source + '\\' + file + '\\', 1)[1]
            archive_date = entry.rsplit('\\')[0]

            parsed_metrics = MetricsParser(path)
            categories = parsed_metrics.parse_category_metrics()

            for category, values in categories.items():
                if not category_evolution.get(category):
                    category_evolution[category] = {}
                
                category_evolution.get(category)[archive_date] = values.get('value')

        results_file_path = glob.glob(results_path + ontology_source + '\\' + file + '/*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            entry = results_file_path.rsplit(archive_path + ontology_source + '\\' + file + '\\', 1)[1]
            results_date = entry.rsplit('\\')[0]

            parsed_metrics = MetricsParser(results_file_path)
            categories = parsed_metrics.parse_category_metrics()
            for category, values in categories.items():
                if not category_evolution.get(category):
                    category_evolution[category] = {}
                category_evolution.get(category)[results_date] = values.get('value')

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            for category, values in categories.items():
                if not category_evolution.get(category):
                    category_evolution[category] = {}
                category_evolution.get(category)[date] = values.get('value')
            
            self.graphPlotter.plot_oquare_category_evolution(category_evolution, temp_path)
            self.readmeGenerator.append_category_evolution(temp_path)
            
        except FileNotFoundError as e:
            print("Error CATEGORY EVOLUTION PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()




        #filepath = glob.glob(results_path + '*/**/' + file + '/metrics/' + file + '.xml', recursive=True)
        #if (len(filepath) > 0):
        #    filepath = filepath[0]
        #    dir = os.path.dirname(os.path.dirname(filepath))
        #    parsed_metrics = MetricsParser(filepath)
        #    categories = parsed_metrics.parse_category_metrics()

        #    for category, values in categories.items():
        #        category_evolution.get(category)[current_date] = values.get('value')

        #    self.graphPlotter.plot_oquare_category_evolution(category_evolution, current_date, dir)
        #    self.readmeGenerator.append_category_evolution(dir)
