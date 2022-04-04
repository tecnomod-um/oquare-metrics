import matplotlib.pyplot as plt

class oquareGraphs:

    def plot_oquare_values(self, data: dict, outputPath: str = 'OQuaRE'):
        plt.figure()
        names = list(data.keys())
        values = list(data.values())

        ax = plt.gca()
        ax.set_ylim([0, 5])

        plt.bar(names, values, width=0.1)
        plt.savefig(outputPath + '/temp_results/OQuaRE_model_values.png', format="png")
    
    def plot_oquare_categories(self, data: dict, fileName: str, outputPath: str = 'OQuaRE'):

        plt.figure(figsize=(15.5, 5))
        names = list(data.keys())
        values = list(data.values())
        ax = plt.gca()
        ax.set_title('OQuaRE model category values')
        ax.set_ylim([0, 5])

        ax.tick_params(
            axis='x',
            which='both',
            bottom=False,
            labelbottom=False
        )
        ax.grid()
        
        plt.plot(range(len(names)), values, '-ko', mfc='red')
        
        for i in range(len(names)):
            ax.annotate('%s' % names[i], xy=(i - 0.25, values[i] + 0.2), textcoords='data')

        plt.savefig(outputPath + '/temp_results/' + fileName + '/' + fileName + "category_values.png", format="png", bbox_inches='tight')