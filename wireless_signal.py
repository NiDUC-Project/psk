import matplotlib.pylab as plt
# import plotly.graph_objects as go


class WirelessSignal:
    def __init__(self, linspace, sinwave):
        """ Set default parameters for modulation

            Parameters
            ----------
            linspace : list or np.array
                Linspace, timeline for signal.
            sinwave: list or np.array
                signal values
        """
        self.__linspace = linspace
        self.__sinwave = sinwave
        self.was_odd = False

    def get_linspace(self):
        """ Gets linspace of WirelessSignal

           Returns
           -------
           list
               linspace of the WirelessSignal
        """
        return self.__linspace

    def get_sinwave(self):
        """ Gets sinwave of WirelessSignal object

           Returns
           -------
           list, numpy.sin
               sinwave of the WirelessSignal
        """
        return self.__sinwave

    def set_linspace(self, linspace):
        """ Sets linspace of WirelessSignal object

            Parameters
            ----------
            linspace: list
                linspace to set
        """
        self.__linspace = linspace

    def set_sinwave(self, sinwave):
        """ Sets sinwave of WirelessSignal object

            Parameters
            ----------
            sinwave: list, numpy.sin prefered
                linspace to set
        """
        self.__sinwave = sinwave

    def show_signal(self):
        """ Show WirelessSignal on the plot """
        try:
            plt.plot(self.__linspace, self.__sinwave)
            plt.xlabel('time[s]')
            plt.ylabel('sin(x)')
            plt.axis('tight')
            plt.grid(True)
            plt.title("Wireless signal")
            plt.show()

        # # plotting
            # fig = go.Figure(layout=dict(xaxis=dict(title='Time (sec)'), yaxis=dict(title='Amplitude')))
            # fig.add_scatter(self.__linspace, self.__sinwave)
            # fig.show()
        except Exception as error:
            print("Exception: {0}".format(error))
