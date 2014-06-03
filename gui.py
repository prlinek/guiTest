__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import readdata as rd
import matplotlib.pyplot as plt  # temporarly here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


class TkDialog(Tkinter.Frame):

    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        # options for a button
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 1}
        radio_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 1}
        # defining buttons
        Tkinter.Button(self, text='Load Data', command=self.askopenfilename).pack(**button_opt)
        Tkinter.Button(self, text='Plot', command=self.showplot).pack(**button_opt)
        # defining variable for radio buttons
        self.radio_selection = Tkinter.IntVar()
        # defining radio buttons
        Tkinter.Radiobutton(self, text='Single file', variable=self.radio_selection, value=1).pack(**radio_opt)
        Tkinter.Radiobutton(self, text='Multiple file', variable=self.radio_selection, value=2).pack(**radio_opt)

        # fig = plt.figure()
        # canvas = FigureCanvasTkAgg(fig)
        # toolbar = NavigationToolbar2TkAgg(canvas)
        # canvas.get_tk_widget()

        #define options for opening files
        self.file_opt = options = {}
        # options['initialdir'] = 'C:/'
        options['parent'] = root
        options['title'] = 'Title'

    def askopenfilename(self):
        if self.radio_selection.get() == 1:
            filename = tkFileDialog.askopenfilename(**self.file_opt)
            if filename:
                rd.readFile(filename)
                return rd.data
        elif self.radio_selection.get() == 2:
            list_of_files = tkFileDialog.askopenfilenames(**self.file_opt)
            list_of_files = list_of_files.split()
            # print list_of_files
            rd.readFiles(list_of_files)
            return rd.x

    def showplot(self):
        if self.radio_selection.get() == 1:
            magnitude = rd.data[:, 1]
            wavelength = rd.data[:, 0]
            # plt.clf()
            plt.plot(wavelength, magnitude)
            plt.title("Plot from single file")
            plt.ylabel("magnitude")
            plt.xlabel("wavelength")
            plt.grid()
            # plt.draw()
            # plt.gcf().canvas.draw()
            plt.show()
        elif self.radio_selection.get() == 2:
            # for now it shows plot from first chosen data file
            magnitude = rd.x[0][:, 1]
            wavelength = rd.x[0][:, 0]
            plt.plot(wavelength, magnitude)
            plt.title("Plot from multi")
            plt.ylabel("magnitude")
            plt.xlabel("wavelength")
            plt.grid()
            plt.show()
            # print "not implemented"
        else:
            print "Something went wrong"

if __name__ == '__main__':
    root = Tkinter.Tk()
    TkDialog(root).pack()
    root.mainloop()