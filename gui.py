__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import tkMessageBox
import readdata as rd
import matplotlib.pyplot as plt  # temporarly here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


class TkDialog(Tkinter.Frame):

    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        root.title("Program")
        # options for a button
        button_opt = {'fill': Tkconstants.X, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP}
        radio_opt = {'fill': Tkconstants.X, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP}
        # defining variable for radio buttons
        self.radio_selection = Tkinter.IntVar()
        self.radio_selection.set(1)
        # defining radio buttons
        Tkinter.Radiobutton(self, text='Single file   ', variable=self.radio_selection, value=1).pack(**radio_opt)
        Tkinter.Radiobutton(self, text='Multiple file', variable=self.radio_selection, value=2).pack(**radio_opt)
        # defining buttons
        Tkinter.Button(self, text='Load Data', command=self.askopenfilename).pack(**button_opt)
        # Tkinter.Button(self, text='Plot Data', command=self.showplot).pack(**button_opt)
        # creating new frame for containing plot and toolbar
        frame = Tkinter.Frame(root)
        frame.pack(side=Tkconstants.RIGHT)
        # creating canvas for plot
        self.f = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.f, master=frame)
        self.canvas.get_tk_widget().pack(side=Tkconstants.BOTTOM, fill=Tkconstants.BOTH, expand=1)
        self.canvas.show()
        #creating toolbar for plot
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, frame)
        self.toolbar.pack(side=Tkconstants.BOTTOM, fill=Tkconstants.BOTH, expand=1)
        self.toolbar.update()
        #define options for opening files
        self.file_opt = options = {}
        options['initialdir'] = '../'
        options['parent'] = root
        options['title'] = 'Load file(s)'

    def askopenfilename(self):
        if self.radio_selection.get() == 1:
            filename = tkFileDialog.askopenfilename(**self.file_opt)
            if filename:
                rd.readFile(filename)
                self.showplot()
                return rd.data
        elif self.radio_selection.get() == 2:
            list_of_files = tkFileDialog.askopenfilenames(**self.file_opt)
            list_of_files = list_of_files.split()
            # print list_of_files
            rd.readFiles(list_of_files)
            if list_of_files:
                self.showplot()
            return rd.x

    def showplot(self):
        if self.radio_selection.get() == 1:
            magnitude = rd.data[:, 1]
            wavelength = rd.data[:, 0]
            self.f.clear()
            self.fig = self.f.add_subplot(111)
            self.fig.plot(wavelength, magnitude)
            self.fig.set_title("Plot from single file")
            self.fig.set_ylabel('magnitude')
            self.fig.set_xlabel('wavelength')
            self.fig.grid()
            self.canvas.draw()
        elif self.radio_selection.get() == 2:
            # for now it shows plot from first chosen data file
            magnitude = rd.x[0][:, 1]
            wavelength = rd.x[0][:, 0]
            self.f.clear()
            self.fig = self.f.add_subplot(111)
            self.fig.plot(wavelength, magnitude)
            self.fig.set_title("Plot from first file")
            self.fig.set_ylabel('magnitude')
            self.fig.set_xlabel('wavelength')
            self.fig.grid()
            self.canvas.draw()
            # print "not implemented"
        else:
            print "load data first"

    def nextplot(self):
        pass

if __name__ == '__main__':
    root = Tkinter.Tk()
    TkDialog(root).pack()
    root.mainloop()