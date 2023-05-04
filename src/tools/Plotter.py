from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotx
import numpy as np

class oquareGraphs:

    """Plotter class which makes use of matplotlib

    The responsabilities of the class consist on the visual representation of the 
    metrics data that was extracted according to the type of data is handling. 

    Its able to plot both current run data aswell as evolution data.

    Makes use of additional matplotx library for style adjustments.
    
    """

    def plot_oquare_values(self, data: dict, file: str, output_path: str):
        """Plotting method for oquare model values

        Line plotting, shows evolution of general quality of ontology.
        Dotted plot with red dots on X axis ticks

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        output_path -- Path to where the figure will be saved to

        """

        dates = list(data.keys())
        values = list(data.values())
        xpos = range(len(values))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.rc('font', size=10)
            plt.ylim([0, 5.5])
            plt.plot(xpos, values, '-ko', mfc='red')
            plt.xticks(xpos, dates, fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
            plt.gca().grid(True, which='major', axis='both', color='#888888', linestyle='--')
            plt.title('OQuaRE model values')
            plt.savefig(output_path + '/img/' + file + '_OQuaRE_model_values.png', format="png", bbox_inches='tight')

        plt.clf()

    def plot_oquare_characteristics(self, data: dict, file: str, output_path: str):
        """Plotting method for characteristics

        Uses a spider graph which shows both the general quality of the ontology
        at a quick glance, as well as the values of each characteristic.
        Scaled on range of 0 to 5 (values are on scale 1 to 5).

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        file -- File name of the ontology being plotted
        output_path -- Path to where the figure will be saved to
        
        """
        names = list(data.keys())
        values = list(data.values())
        value_range = range(len(values))

        # Calculates angles and closes the plots by repeating first item
        angles = [i/len(names) * 2 * np.pi for i in value_range]
        values += values[:1]
        angles += angles[:1]

        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], names, color='grey', size=12)
        plt.yticks([1, 2, 3, 4], ["1", "2", "3", "4"], color="grey", size='7')
        plt.ylim([0, 5])
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'skyblue', alpha=0.4)

        plt.title('OQuaRE characteristics values')
        plt.savefig(output_path + '/img/' + file + "_characteristics_values.png", format="png", bbox_inches='tight')
        
        plt.clf()


    def plot_metrics(self, data: dict, file: str, output_path: str, scaled: bool):
        """Plotting method for metrics

        Uses horizontal lollipop/stem graph with value label next to the stem with annotations. 
        Allows for easy knowledge of current values for each metric

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        file -- File name of the ontology being plotted
        output_path -- Path to where the figure will be saved to
        scaled -- Indicates if the plotting is making use of scaled metrics or not. If True,
        plot is then scaled on range 0 to 5.5 (for right side margin its added an extra 0.5).
        
        """
        names = list(data.keys())
        values = list(data.values())
        ypos = range(len(names))

        with plt.style.context(matplotx.styles.ayu["light"]):
            plt.hlines(y=ypos, xmin=0, xmax=values, color='skyblue')

            if scaled:
                plt.xlim([0, 5.5])
            plt.yticks(ypos, names)
            plt.plot(values, ypos, "D")

            for i in ypos:
                if scaled:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.2, i - 0.15), textcoords='data', fontsize=8)
                else:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.3, i - 0.15), textcoords='data', fontsize=8)

            if scaled:
                plt.title('OQuaRE scaled metrics')
                plt.savefig(output_path + '/img/' + file + "_scaled_metrics.png", format="png", bbox_inches='tight')
            else:
                plt.title('OQuaRE metrics')
                plt.savefig(output_path + '/img/' + file + "_metrics.png", format="png", bbox_inches='tight')
        
        plt.clf()


    def plot_oquare_subcharacteristics(self, data: dict, file: str, output_path: str) -> None:
        """Plotting method for subcharacteristics

        Uses horizontal bars with annotations instead of stems like in metrics. 
        This is due to the fact that in some cases there is a single subcharacteristics 
        per characteristics, or just 2 of them. In which a stem graph would not look good at all.

        Bars have adjusted width depending on the amount of values its plotting.
        Checks are for 1 and 2 subcharacteristics, everything else automatically scale.

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        file -- File name of the ontology being plotted
        output_path -- Path to where the figure will be saved to
        
        """
        for characteristic in data.keys():
            subcharacteristics: dict = data.get(characteristic).get('subcharacteristics')

            names = list(subcharacteristics.keys())
            values = list(subcharacteristics.values())
            ypos = range(len(values))

            with plt.style.context(matplotx.styles.ayu["light"]):

                if len(values) == 1:
                    plt.ylim(-1,1)
                    plt.barh(ypos, values, height=0.6)
                elif len(values) == 2:
                    plt.ylim(-1, 2)
                    plt.barh(ypos, values, height=0.8)
                else:
                    plt.barh(ypos, values)
                plt.yticks(ypos, names)
                plt.xlim([0, 5.5])

                for i in ypos:
                    plt.annotate('%s' % values[i], xy=(values[i] + 0.1, i), textcoords='data', fontsize=8)
                    
                plt.title(characteristic + ' metrics')
                plt.savefig(output_path + '/img/' + file + "_" + characteristic + "_subcharacteristics_metrics.png", format="png", bbox_inches='tight')
                plt.clf()
    
    def plot_oquare_characteristics_evolution(self, data: dict, file: str,  output_path: str) -> None:
        """Plotting method for characteristics evolution

        Multiple colored plot lines that represent the evolution of each characteristics

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        output_path -- Path to where the figure will be saved to

        """
        line_labels = list(data.keys())
        with plt.style.context(matplotx.styles.ayu["light"]):
            
            # For each characteristic, plot its evolution data.
            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                plt.plot(dates, values, label=label)

            plt.rc('font', size=8)
            plt.ylim([0, 5.5])
            plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
            plt.yticks(fontsize=10)
            plt.rc('figure', titlesize=12)
            plt.title('characteristics evolution over time')
            matplotx.line_labels()
            plt.savefig(output_path + '/img/' + file + '_characteristics_evolution.png', format='png', bbox_inches='tight')
        plt.clf()
    
    def plot_oquare_subcharacteristics_evolution(self, data: dict, file:str,  output_path: str) -> None:
        """Plotting method for subcharacteristics evolution

        Multiple colored plot lines that represent the evolution of each subcharacteristics

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        output_path -- Path to where the figure will be saved to

        """

        for characteristic, subcharacteristics_data in data.items():
            line_labels = list(subcharacteristics_data.keys())
            with plt.style.context(matplotx.styles.ayu["light"]):
                
                for label in line_labels:
                    values = subcharacteristics_data.get(label).values()
                    dates = subcharacteristics_data.get(label).keys()
                    plt.plot(dates, values, label=label)
                plt.rc('font', size=8)
                plt.ylim([0, 5.5])
                plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
                plt.yticks(fontsize=10)
                plt.title(characteristic + ' metrics evolution over time', fontsize=11)
                matplotx.line_labels()
                plt.savefig(output_path + '/img/' + file + "_" + characteristic + '_subcharacteristics_evolution.png', format='png', bbox_inches='tight')
            plt.clf() 


    def plot_metrics_evolution(self, data: dict, file: str, output_path: str) -> None:
        """Plotting method for metrics evolution

        Individual evolution plot for each metric due to the difference in scales.

        Keyword arguments:
        data -- Dictionary which holds the values to plot
        output_path -- Path to where the figure will be saved to

        """
        line_labels = list(data.keys())
        with plt.style.context(matplotx.styles.ayu["light"]):

            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                plt.plot(dates, values, label=label)
                plt.xticks(fontsize=8, rotation=-45, ha="left", rotation_mode="anchor")
                plt.yticks(fontsize=10)
                plt.title(label + ' evolution over time')
                plt.savefig(output_path + '/img/' + file + '_' + label +'_metric_evolution.png', format='png', bbox_inches='tight')
                plt.clf()

    def plot_scaled_metrics_evolution(self, data: dict, file: str, output_path: str) -> None:

        line_labels = list(data.keys())
        
        with plt.style.context(matplotx.styles.ayu["light"]):

            fig, axs = plt.subplots(4, 5, figsize=(12,12))
            
            row = 0
            col = 0
            plt.ylim([0, 5.5])
            for label in line_labels:
                values = data.get(label).values()
                dates = data.get(label).keys()
                axs[row, col].plot(range(len(dates)), values, label=label)
                axs[row, col].set_xticks(range(len(dates)))
                axs[row, col].set_xticklabels(range(len(dates)), fontsize=5)
                axs[row, col].set_ylim(0, 5.5)
                axs[row, col].set_title(label, fontsize=9)

                col += 1
                if col %5 == 0:
                    row += 1
                    col = 0

            plt.delaxes(axs[3, 4])
            for ax in axs.flat:
                    ax.label_outer()
            
            plt.savefig(output_path + '/img/' + file + '_scaled_metrics_evolution.png', format='png', bbox_inches='tight')




        return