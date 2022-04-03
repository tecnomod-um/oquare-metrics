from Parser import MetricsParser
import matplotlib.pyplot as plt

class oquareGraphs:

    def plot_oquare_values(self, data: dict, outputPath: str = 'OQuaRE'):
        names = list(data.keys())
        values = list(data.values())

        ax = plt.gca()
        ax.set_ylim([0, 5])

        plt.bar(names, values, width=0.1)
        plt.savefig(outputPath + '/temp_results/OQuaRE_model_values.png', format="png")