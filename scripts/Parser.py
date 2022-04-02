import string
import xml.etree.ElementTree as ET

class MetricsParser:
    def __init__(self, metrics_file: string):
        self.tree = ET.parse(metrics_file)
        self.root = self.tree.getroot()

    def parse_oquare_value(self) -> float:
        oquare_value = self.root.find('oquareModel').attrib.get('oquareValue')
        return oquare_value
    
    def parse_scaled_metrics(self):
        scaled_metrics = self.root.findall('./oquareMetricsScaled/')
        metrics_dict = {}
        for metric in scaled_metrics:
            metrics_dict[metric.tag] = metric.text
        
        return metrics_dict

    def parse_category_metrics(self):
        oquare_model = self.root.findall('oquareModel/')
        oquare_model_dict = {}
        for metric in oquare_model:
            metric_name, metric_value = next(iter(metric.attrib.items()))

            oquare_category = {}
            oquare_category['value'] = metric_value
            
            oquare_sub_categories = {}
            
            # Get subcategories
            subcategories = self.root.findall('oquareModel/' + metric.tag + '/')
            for subcategory in subcategories:
                oquare_sub_categories[subcategory.tag] = subcategory.text

            # Put subcategories under the main category
            oquare_category['subcategories'] = oquare_sub_categories

            # Put each category inside the oquare_model_dict
            oquare_model_dict[metric_name] = oquare_category

        return oquare_model_dict
        

if __name__ == '__main__':
    parser = MetricsParser('../OQuaRE/results/20-03-2022_15-49-21/ontologyCEPH2/metrics/ontologyCEPH2.xml')
    value = parser.parse_oquare_value()
    scaled = parser.parse_scaled_metrics()
    category_metrics = parser.parse_category_metrics()

    for category in category_metrics:
        data = category_metrics.get(category)
        value = data.get('value')
        subcategories = data.get('subcategories')

        for subcategory in subcategories:
            print(subcategories.get(subcategory))