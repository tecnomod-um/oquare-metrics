
import glob
from tools.Plotter import oquareGraphs
from tools.Parser import MetricsParser
from tools.Reporter import readmeGen

class Controller:
    """Controller class that handles file system and additional tool calls

    This class is designed with file system managing responsability in mind, as well
    as calling additional tooling for different purposes. Its responsability lies in
    extracting the paths to metric files aswell as storing and managing extracted data.

    This class makes uses of functionality provided by Plotter, Parser and Reporter classes
    so that it can extract data from metrics files, plot them on different ways and finally
    generate a report which shows different metrics in a visual way.

    """

    def __init__(self):
        """ Controller init method

        Class has a plotter and reporter instances as fields for easy usage

        """
        self.graphPlotter = oquareGraphs()
        self.readmeGenerator = readmeGen()

    def store_metrics_evolution(self, metrics: dict, data_store: dict, date: str) -> None:
        """Stores values of metrics at a certain date in a dictionary
        
        Keyword arguments:
        metrics -- Dictionary which contains all 19 metrics and their values
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the metrics values are associated to

        """
        for metric, value in metrics.items():
            if not data_store.get(metric):
                data_store[metric] = {}
            data_store.get(metric)[date] = value
    
    def store_features_evolution(self, features: dict, data_store: dict, date: str) -> None:
        """Stores values of features at a certain date in a dictionary
        
        Keyword arguments:
        features -- Dictionary which contains features information such as value
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the features values are associated to

        """
        for feature, values in features.items():
            if not data_store.get(feature):
                data_store[feature] = {}
            
            data_store.get(feature)[date] = values.get('value')
    
    def store_subfeatures_evolution(self, features: dict, data_store: dict, date: str) -> None:
        """Stores values of subfeatures at a certain date in a dictionary
        
        Keyword arguments:
        features -- Dictionary which contains features information such as subfeatures values
        data_store -- Dictionary to store the values for a given date
        date -- Date to which the features values are associated to

        """
        for feature, values in features.items():
            if not data_store.get(feature):
                data_store[feature] = {}

            subfeatures = values.get('subfeatures')

            for subfeature, value in subfeatures.items():
                if not data_store.get(feature).get(subfeature):
                    data_store.get(feature)[subfeature] = {}

                data_store.get(feature).get(subfeature)[date] = value        

    def parse_entry(self, base_path: str, file_path: str, data_store: dict, parse_type: str) -> None:
        """Parses a file entry to extract its date and store the values on a dict by dates
        
        Keyword arguments:
        base_path -- Path that contains date entries for a given ontology
        file_path -- Full path to an ontology metrics file
        data_store -- Dictionary to store the values for a given date
        parse_type -- Indicates which data should be extracted from metrics and its handling

        """
        entry = file_path.rsplit(base_path, 1)[1]
        entry_date = entry.rsplit('/')[0]
        parsed_metrics = MetricsParser(file_path)

        if parse_type == 'oquare_value':
            data_store[entry_date] = parsed_metrics.parse_oquare_value()
        elif parse_type == 'metrics':
            metrics = parsed_metrics.parse_metrics()
            self.store_metrics_evolution(metrics, data_store, entry_date)
        elif parse_type == 'metrics-scaled':
            scaled_metrics = parsed_metrics.parse_scaled_metrics()
            self.store_metrics_evolution(scaled_metrics, data_store, entry_date)
        elif parse_type == 'features':
            features = parsed_metrics.parse_features_metrics()
            self.store_features_evolution(features, data_store, entry_date)
        elif parse_type == 'subfeatures':
            features = parsed_metrics.parse_features_metrics()
            self.store_subfeatures_evolution(features, data_store, entry_date)

    def handle_features(self, temp_path: str, file: str) -> None:
        """Handles features data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        oquare_features_values = {}

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        features = parsed_metrics.parse_features_metrics()
        for feature, values in features.items():
            oquare_features_values[feature] = values.get('value')
        
        self.graphPlotter.plot_oquare_features(oquare_features_values, file, temp_path)
        self.readmeGenerator.append_features(file, temp_path)

    def handle_subfeatures(self, temp_path: str, file: str) -> None:
        """Handles subfeatures data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        features = parsed_metrics.parse_features_metrics()
        self.graphPlotter.plot_oquare_subfeatures(features, file, temp_path)
        self.readmeGenerator.append_subfeatures(file, temp_path, list(features.keys()))


    def handle_metrics(self, temp_path: str, file: str) -> None:
        """Handles metrics data extraction, plotting and reporting
        
        Keyword arguments:
        temp_path -- Fully structured path to current execution temp_folder. The path is
        as it follows: input_path/temp_results/ontology_source/file/date. No trailing slash
        file -- Current ontology file being analysed

        """
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        metrics = parsed_metrics.parse_metrics()
        scaled_metrics = parsed_metrics.parse_scaled_metrics()

        self.graphPlotter.plot_metrics(metrics, file, temp_path, False)
        self.graphPlotter.plot_metrics(scaled_metrics, file, temp_path, True)
        self.readmeGenerator.append_metrics(file, temp_path)
     
    def handle_oquare_model(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles oquare model evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution

        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        oquare_model_values = {}


        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, oquare_model_values, 'oquare_value') 

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, oquare_model_values, 'oquare_value')

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        oquare_model_values[date] = parsed_metrics.parse_oquare_value()

        self.graphPlotter.plot_oquare_values(oquare_model_values, file, temp_path)
        self.readmeGenerator.append_oquare_value(file, temp_path)


    def handle_metrics_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles metrics evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution

        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        metrics_evolution = {}
        metrics_evolution_scaled = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, metrics_evolution, 'metrics')
            self.parse_entry(archive_path, path, metrics_evolution_scaled, 'metrics-scaled')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, metrics_evolution, 'metrics')
            self.parse_entry(results_path, results_file_path, metrics_evolution_scaled, 'metrics-scaled')

        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        metrics = parsed_metrics.parse_metrics()
        scaled_metrics = parsed_metrics.parse_scaled_metrics()
        self.store_metrics_evolution(metrics, metrics_evolution, date)
        self.store_metrics_evolution(scaled_metrics, metrics_evolution_scaled, date)
            
        self.graphPlotter.plot_metrics_evolution(metrics_evolution, file, temp_path)
        self.graphPlotter.plot_scaled_metrics_evolution(metrics_evolution_scaled, file, temp_path)
        self.readmeGenerator.append_scaled_metrics_evolution(file, temp_path)
        self.readmeGenerator.append_metrics_evolution(file, temp_path, list(metrics_evolution.keys()))

    def handle_features_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles features evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        features_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, features_evolution, 'features')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, features_evolution, 'features')
                
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        features = parsed_metrics.parse_features_metrics()
        self.store_features_evolution(features, features_evolution, date)

        self.graphPlotter.plot_oquare_features_evolution(features_evolution, file, temp_path)
        self.readmeGenerator.append_features_evolution(file, temp_path)


    def handle_subfeatures_evolution(self, file: str, input_path: str, ontology_source: str, date: str) -> None:
        """Handles subfeatures evolution data extraction, plotting and reporting
        
        Keyword arguments:
        file -- Current ontology file being analysed
        input_path -- Folder which stores generated results
        ontology_source -- Source folder which contains ontology file being analysed
        date -- Current date of module execution
        
        """
        archive_path = input_path + '/archives/' + ontology_source + '/' + file + '/'
        results_path = input_path + '/results/' + ontology_source + '/' + file + '/'
        temp_path = input_path + '/temp_results/' + ontology_source + '/' + file + '/' + date
        subfeatures_evolution = {}

        archive_list = sorted(glob.glob(archive_path + '*/metrics/' + file + '.xml'))[-18:]
        for path in archive_list:
            self.parse_entry(archive_path, path, subfeatures_evolution, 'subfeatures')

        results_file_path = glob.glob(results_path + '*/metrics/' + file + '.xml')
        if len(results_file_path) > 0:
            results_file_path = results_file_path[0]
            self.parse_entry(results_path, results_file_path, subfeatures_evolution, 'subfeatures')
                
        parsed_metrics = MetricsParser(temp_path + '/metrics/' + file + '.xml')
        features = parsed_metrics.parse_features_metrics()
        self.store_subfeatures_evolution(features, subfeatures_evolution, date)

        self.graphPlotter.plot_oquare_subfeatures_evolution(subfeatures_evolution, file, temp_path)
        self.readmeGenerator.append_subfeatures_evolution(file, temp_path, list(features.keys()))
            