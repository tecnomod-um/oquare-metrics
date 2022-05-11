from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotx
import numpy as np

class oquareGraphs:

    def plot_oquare_values(self, data: dict, output_path: str):
        dates = list(data.keys())
        values = list(data.values())
        xpos = range(len(values))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.rc('font', size=10)
            plt.ylim([0, 5])
            plt.plot(xpos, values, '-ko', mfc='red')
            plt.xticks(xpos, dates, fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
            plt.gca().grid(True, which='major', axis='both', color='#888888', linestyle='--')
            plt.title('OQuaRE model values')
            plt.savefig(output_path + '/OQuaRE_model_values.png', format="png", bbox_inches='tight')

        plt.clf()

    def plot_oquare_categories(self, data: dict, file: str, temp_path: str):

        names = list(data.keys())
        values = list(data.values())
        xpos = range(len(values))

        angles = [i/len(names) * 2 * np.pi for i in xpos]
        values += values[:1]
        angles += angles[:1]

        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], names, color='grey', size=12)
        plt.yticks([1, 2, 3, 4], ["1", "2", "3", "4"], color="grey", size='7')
        plt.ylim([0, 5])
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'skyblue', alpha=0.4)

        plt.title('OQuaRE category values')
        plt.savefig(temp_path + '/' + file + "_category_values.png", format="png", bbox_inches='tight')
        
        plt.clf()


    def plot_metrics(self, data: dict, file: str, temp_path: str, scaled: bool):
        names = list(data.keys())
        values = list(data.values())
        ypos = range(len(names))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.hlines(y=ypos, xmin=0, xmax=values, color='skyblue')

            if scaled:
                plt.xlim([0, 5.5])
            plt.yticks(ypos, names)
            plt.plot(values, ypos, "D")

            #plt.gca().grid(True, which='major', axis='x', color='#888888', linestyle='--')

            for i in ypos:
                if scaled:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.2, i - 0.15), textcoords='data', fontsize=8)
                else:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.3, i - 0.15), textcoords='data', fontsize=8)

            if scaled:
                plt.title('OQuaRE scaled metrics')
                plt.savefig(temp_path + '/' + file + "_scaled_metrics.png", format="png", bbox_inches='tight')
            else:
                plt.title('OQuaRE metrics')
                plt.savefig(temp_path + '/' + file + "_metrics.png", format="png", bbox_inches='tight')
        
        plt.clf()


    def plot_oquare_subcategories(self, data: dict, fileName: str, basePath: str) -> None:

        for category in data.keys():
            subcategories: dict = data.get(category).get('subcategories')

            names = list(subcategories.keys())
            values = list(subcategories.values())
            ypos = range(len(values))

            with plt.style.context(matplotx.styles.ayu["light"]):

                if len(values) == 1:
                    plt.ylim(-1,1)
                    plt.barh(ypos, values, height=0.6)
                elif len(values) < 3 and len(values) > 1:
                    plt.ylim(-1, 2)
                    plt.barh(ypos, values, height=0.8)
                else:
                    plt.barh(ypos, values)
                plt.yticks(ypos, names)
                plt.xlim([0, 5.5])

                for i in ypos:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.1, i), textcoords='data', fontsize=8)
                    
                plt.title(category + ' metrics')
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
            plt.savefig(dir + '/categories_evolution.png', format='png', bbox_inches='tight')
        plt.clf()

    def plot_metrics_evolution(self, data: dict, dir: str) -> None:
        line_labels = list(data.keys())
        with plt.style.context(matplotx.styles.ayu["light"]):

            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                plt.plot(dates, values, label=label)
        
                plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
                plt.yticks(fontsize=10)
                plt.title(label + ' evolution over time')
                matplotx.line_labels()
                plt.savefig(dir + '/' + label +'_metric_evolution.png', format='png', bbox_inches='tight')
                plt.clf()