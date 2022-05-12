
import glob
import os
import sys
from tools.Plotter import oquareGraphs
from tools.Parser import MetricsParser
from tools.Reporter import readmeGen


class Controller:

    def __init__(self):
        self.graphPlotter = oquareGraphs()
        self.readmeGenerator = readmeGen()

    def store_metrics_evolution(self, metrics: dict, data_store: dict, date: str) -> None:
        for metric, value in metrics.items():
            if not data_store.get(metric):
                data_store[metric] = {}
            data_store.get(metric)[date] = value
    
    def store_categories_evolution(self, categories: dict, data_store: dict, date: str) -> None:
        for category, values in categories.items():
            if not data_store.get(category):
                data_store[category] = {}
            
            data_store.get(category)[date] = values.get('value')

    def parse_entry(self, base_path: str, file_path: str, data_store: dict, parse_type: str) -> None:
        entry = file_path.rsplit(base_path, 1)[1]
        entry_date = entry.rsplit('/')[0]
        parsed_metrics = MetricsParser(file_path)

        if parse_type == 'oquare_value':
            data_store[entry_date] = parsed_metrics.parse_oquare_value()
        elif parse_type == 'metrics':
            metrics = parsed_metrics.parse_metrics()
            self.store_metrics_evolution(metrics, data_store, entry_date)
        elif parse_type == 'categories':
            categories = parsed_metrics.parse_category_metrics()
            self.store_categories_evolution(categories, data_store, entry_date)

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

    def handle_metrics(self, temp_path: str, file: str) -> None:
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            metrics = parsed_metrics.parse_metrics()
            scaled_metrics = parsed_metrics.parse_scaled_metrics()

            self.graphPlotter.plot_metrics(metrics, file, temp_path, False)
            self.graphPlotter.plot_metrics(scaled_metrics, file, temp_path, True)
            self.readmeGenerator.append_metrics(file, temp_path)

        except FileNotFoundError as e:
            print("Error METRICS: " + e.strerror + ". Abort", flush=True)
     
    def handle_oquare_model(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        oquare_model_values = {}


        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, oquare_model_values, 'oquare_value') 

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, oquare_model_values, 'oquare_value')

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            oquare_model_values[date] = parsed_metrics.parse_oquare_value()

            self.graphPlotter.plot_oquare_values(oquare_model_values, temp_path)
            self.readmeGenerator.append_oquare_value(temp_path)
            
        except FileNotFoundError as e:
            print("Error MODEL PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()    

    def handle_metrics_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        metrics_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, metrics_evolution, 'metrics')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, metrics_evolution, 'metrics')

        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            metrics = parsed_metrics.parse_metrics()
            self.store_metrics_evolution(metrics, metrics_evolution, date)
                
            self.graphPlotter.plot_metrics_evolution(metrics_evolution, temp_path)
            self.readmeGenerator.append_metrics_evolution(temp_path, list(metrics_evolution.keys()))
        except FileNotFoundError as e:
            print("Error METRICS EVOLUTION: " + e.strerror + ". Abort", flush=True)
            sys.exit()  

    def handle_category_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        categories_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-19:]
        for path in archive_list:
            self.parse_entry(archive_path, path, categories_evolution, 'categories')

        results_file_path = glob.glob(results_path + ontology_source + '/' + file + '/*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, categories_evolution, 'categories')
                
        try:
            parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
            categories = parsed_metrics.parse_category_metrics()
            self.store_categories_evolution(categories, categories_evolution, date)

            self.graphPlotter.plot_oquare_category_evolution(categories_evolution, temp_path)
            self.readmeGenerator.append_category_evolution(temp_path)
            
        except FileNotFoundError as e:
            print("Error CATEGORY EVOLUTION PLOTTING: " + e.strerror + ". Abort", flush=True)
            sys.exit()
