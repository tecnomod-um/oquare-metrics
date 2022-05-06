from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotx

class oquareGraphs:

    def plot_oquare_values(self, data: dict, output_path: str):
        dates = list(data.keys())
        values = list(data.values())
        xpos = range(len(values))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.rc('font', size=10)
            plt.ylim([0, 5])
            plt.plot(xpos, values, '-ko', mfc='red')
            plt.xticks(xpos, dates, fontsize=8, rotation=90)
            plt.gca().grid(True, which='major', axis='both', color='#888888', linestyle='--')
            plt.title('OQuaRE model values')
            plt.savefig(output_path + 'OQuaRE_model_values.png', format="png", bbox_inches='tight')

        plt.clf()

    def plot_oquare_categories(self, data: dict, fileName: str, basePath: str):

        names = list(data.keys())
        values = list(data.values())
        xpos = range(len(values))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.ylim([0, 5])
            plt.bar(xpos, values)
            plt.xticks(xpos, names, fontsize=10, rotation=-45, ha="left", rotation_mode="anchor")
            matplotx.show_bar_values("{:.2f}")
            plt.title('OQuaRE category values')
            plt.savefig(basePath + '/' + fileName + "_category_values.png", format="png", bbox_inches='tight')
        
        plt.clf()

    def plot_historic(self, data: dict, date: str, outputPath: str):

        line_labels = list(data.keys())
        
        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.rc('font', size=10)

            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                plt.plot(dates, values, label=label)

            plt.ylim([0, 5])
            plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
            plt.yticks(fontsize=10)
            plt.title("OQuaRE historic values")
            matplotx.line_labels()
            plt.savefig(outputPath + '/results/' + date + '/OQuaRE_historic_model_value.png', format="png", bbox_inches='tight')

        plt.clf()

    def plot_oquare_subcategories(self, data: dict, fileName: str, basePath: str) -> None:

        for category in data.keys():
            subcategories: dict = data.get(category).get('subcategories')

            names = list(subcategories.keys())
            values = list(subcategories.values())
            xpos = range(len(values))

            with plt.style.context(matplotx.styles.ayu["light"]):
                plt.ylim([0, 5])
                plt.bar(xpos, values)
                plt.xticks(xpos, names, fontsize=10, rotation=-45, ha="left", rotation_mode="anchor")
                plt.title(category + ' metrics')
                plt.gca().grid(True, which='major', axis='y', color='#aaaaaa', linestyle='--')
                plt.savefig(basePath + '/' + fileName + "_" + category + "_metrics.png", format="png", bbox_inches='tight')
                plt.clf()
    
    def plot_oquare_category_evolution(self, data: dict, dir: str) -> None:

        line_labels = list(data.keys())
        with plt.style.context(matplotx.styles.ayu["light"]):
            
            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                plt.plot(dates, values, label=label)
        
        plt.ylim([0, 5])
        plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
        plt.yticks(fontsize=10)
        plt.title('Categories evolution over time')
        matplotx.line_labels()
        plt.savefig(dir + '\\categories_evolution.png', format='png', bbox_inches='tight')
