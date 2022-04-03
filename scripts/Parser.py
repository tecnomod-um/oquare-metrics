import xml.etree.ElementTree as ET

class MetricsParser:
    def __init__(self, metrics_file: str):
        self.tree = ET.parse(metrics_file)
        self.root = self.tree.getroot()
        self.oquare_value = self.__parse_oquare_value()
        self.scaled_metrics = self.__parse_scaled_metrics()
        self.category_metrics = self.__parse_category_metrics()

    def __parse_oquare_value(self) -> float:
        oquare_value = float(self.root.find('oquareModel').attrib.get('oquareValue'))
        return oquare_value
    
    def __parse_scaled_metrics(self):
        scaled_metrics = self.root.findall('./oquareMetricsScaled/')
        metrics_dict = {}
        for metric in scaled_metrics:
            metrics_dict[metric.tag] = metric.text
        
        return metrics_dict

    def __parse_category_metrics(self):
        oquare_model = self.root.findall('oquareModel/')
        oquare_model_dict = {}
        for metric in oquare_model:
            metric_name, metric_value = next(iter(metric.attrib.items()))

            oquare_category = {}
            oquare_category['value'] = float(metric_value)
            
            oquare_sub_categories = {}
            
            # Get subcategories
            subcategories = self.root.findall('oquareModel/' + metric.tag + '/')
            for subcategory in subcategories:
                oquare_sub_categories[subcategory.tag] = subcategory.text

            # Put subcategories under the main category
            oquare_category['subcategories'] = oquare_sub_categories

            # Put each category inside the oquare_model_dict
            oquare_model_dict[metric_name] = oquare_category

        # {
        #   category_name: {
        #       value: number
        #       subcategories: {
        #           subcat_1: value
        #           ...
        #       } 
        #   } 
        # 
        # }
        return oquare_model_dict
    
    def get_oquare_value(self):
        return self.oquare_value

    def get_scaled_metrics(self):
        return self.scaled_metrics

    def get_category_metrics(self):
        return self.category_metrics
