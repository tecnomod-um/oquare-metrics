
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

    def __scan_entry(self, basepath: str, entry: str, value_dict: dict) -> None:
        
        for filepath in glob.iglob(basepath + entry + '/**/*.xml', recursive=True):
            ontology_name = os.path.basename(filepath).rsplit('.', 1)[0]
            if not value_dict.get(ontology_name):
                value_dict[ontology_name] = {}
            
            parsed_metrics = MetricsParser(filepath)
            value_dict.get(ontology_name)[entry] = parsed_metrics.parse_oquare_value()

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
            print("Error: " + e.strerror + ". Abort", flush=True)
            sys.exit()


    def handle_oquare_model(self, basepath: str, input_path: str) -> None:
        oquare_model_values = {}

        for filepath in glob.iglob(basepath + '**/*.xml', recursive=True):
            parsed_metrics = MetricsParser(filepath)
            ontology_name = os.path.basename(filepath).rsplit('.', 1)[0]
            oquare_model_values[ontology_name] = parsed_metrics.parse_oquare_value()
        
        self.graphPlotter.plot_oquare_values(oquare_model_values, input_path)
        self.readmeGenerator.append_oquare_value(input_path)

    def handle_historic(self, input_path: str) -> None:
        archive_path = input_path + '/archives/'
        results_path = input_path + '/results/'
        oquare_model_values_historic = {}
        entries = sorted(os.listdir(archive_path))
        current_date = os.listdir(results_path)[0]
        dates = []

        if len(entries) < 19:
            dates = entries
            for entry in entries:
                self.__scan_entry(archive_path, entry, oquare_model_values_historic)
        else:
            for i in range(len(entries)-19, len(entries)):
                entry = entries[i]
                dates.append(entry)
                self.__scan_entry(archive_path, entry, oquare_model_values_historic)
        
        dates.append(current_date)
        self.__scan_entry(results_path, current_date, oquare_model_values_historic)

        self.graphPlotter.plot_historic(oquare_model_values_historic, current_date, input_path)
        self.readmeGenerator.append_oquare_historic(input_path, current_date)
    

    def handle_category_evolution(self, file: str, input_path: str) -> None:

        archive_path = input_path + '\\archives\\'
        results_path = input_path + '\\results\\'
        category_evolution = {}
        current_date = os.listdir(results_path)[0]

        archive_list = sorted(glob.glob(archive_path + '*/**/' + file + '/metrics/' + file + '.xml', recursive=True))[-19:]
        for path in archive_list:
            entry = path.rsplit(archive_path, 1)[1]
            date = entry.rsplit('\\')[0]

            parsed_metrics = MetricsParser(path)
            categories = parsed_metrics.parse_category_metrics()

            for category, values in categories.items():
                if not category_evolution.get(category):
                    category_evolution[category] = {}
                
                category_evolution.get(category)[date] = values.get('value')
        
        filepath = glob.glob(results_path + '*/**/' + file + '/metrics/' + file + '.xml', recursive=True)
        if (len(filepath) > 0):
            filepath = filepath[0]
            dir = os.path.dirname(os.path.dirname(filepath))
            parsed_metrics = MetricsParser(filepath)
            categories = parsed_metrics.parse_category_metrics()

            for category, values in categories.items():
                category_evolution.get(category)[current_date] = values.get('value')

            self.graphPlotter.plot_oquare_category_evolution(category_evolution, current_date, dir)
            self.readmeGenerator.append_category_evolution(dir)


    def handle_category_evolution_old(self, basePath: str, file: str, inputPath: str) -> None:
        
        # REMAKE
        
        archive_path = inputPath + '/archives/'
        results_path = inputPath + '/results/'
        category_evolution = {}
        entries = sorted(os.listdir(archive_path))
        current_date = os.listdir(results_path)[0]
        dates = []

        if len(entries) < 19:
            dates = entries
            for entry in entries:
                self.__scan_entry(archive_path, entry, category_evolution)
        else:
            for i in range(len(entries)-19, len(entries)):
                entry = entries[i]
                dates.append(entry)
                self.__scan_entry(archive_path, entry, category_evolution)
        
        
        dates.append(current_date)
        for filepath in glob.iglob(results_path + entry + '/**/*.xml', recursive=True):
            
            ontology_name = os.path.basename(filepath).rsplit('.', 1)[0]
            if not category_evolution.get(ontology_name):
                category_evolution[ontology_name] = {}
            
            category_evolution.get(ontology_name)['dir'] = os.path.pardir(filepath)
            parsed_metrics = MetricsParser(filepath)
            category_evolution.get(ontology_name)[current_date] = parsed_metrics.parse_category_metrics()

        for ontology in category_evolution.keys():
            self.graphPlotter.plot_oquare_category_evolution(ontology)
