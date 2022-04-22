

import os
from Graphs import oquareGraphs
from Parser import MetricsParser
from ReadMeGen import readmeGen


class Controller:

    def __init__(self):
        self.graphPlotter = oquareGraphs()
        self.readmeGenerator = readmeGen()

    def __scan_entry(self, basepath: str, entry: str, value_dict: dict) -> None:
        with os.scandir(basepath + entry) as ontologies:
            for ontology in ontologies:
                if ontology.is_dir():
                    if not value_dict.get(ontology.name):
                        value_dict[ontology.name] = {}

                    parsed_metrics = MetricsParser(ontology.path + '/metrics/' + ontology.name + '.xml')
                    value_dict.get(ontology.name)[entry] = parsed_metrics.parse_oquare_value()

    def handle_categories(self, basepath: str, file: str, inputPath: str) -> None:
        oquare_category_values = {}
        parsed_metrics = MetricsParser(basepath + file + '/metrics/' + file + '.xml')
        categories = parsed_metrics.parse_category_metrics()
        for category, values in categories.items():
            oquare_category_values[category] = values.get('value')
        
        self.graphPlotter.plot_oquare_categories(oquare_category_values, file, inputPath)
        self.readmeGenerator.append_category(file, inputPath)

    def handle_oquare_model(self, basepath: str, inputPath: str) -> None:
        oquare_model_values = {}
        with os.scandir(basepath) as entries:
            for entry in entries:
                if entry.is_dir():
                    parsed_metrics = MetricsParser(entry.path + '/metrics/' + entry.name + ".xml")
                    oquare_model_values[entry.name] = parsed_metrics.parse_oquare_value()
        
        self.graphPlotter.plot_oquare_values(oquare_model_values, inputPath)
        self.readmeGenerator.append_oquare_value(inputPath)

    def handle_historic(self, basepath: str, inputPath: str) -> None:
        archive_path = inputPath + '/archives/'
        results_path = inputPath + '/results/'
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

        self.graphPlotter.plot_historic(oquare_model_values_historic, current_date, inputPath)
        self.readmeGenerator.append_oquare_historic(inputPath, current_date)