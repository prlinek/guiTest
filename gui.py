__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import readdata as rd
import matplotlib.pyplot as plt  # temporarly here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import peakdetect as pd


class TkDialog(Tkinter.Frame):

    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        root.title("Program")
        self.plotnum = Tkinter.IntVar()
        self.plotnum.set(0)
        # options for a button
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP}
        radio_opt = {'fill': Tkconstants.X, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP}
        # defining variable for radio buttons
        self.radio_selection = Tkinter.IntVar()
        self.radio_selection.set(1)
        self.list_of_files = []
        # defining radio buttons
        Tkinter.Radiobutton(self, text='Single file   ', variable=self.radio_selection, value=1).pack(**radio_opt)
        Tkinter.Radiobutton(self, text='Multiple file', variable=self.radio_selection, value=2).pack(**radio_opt)
        # defining buttons
        Tkinter.Button(self, text='Load Data', command=self.askopenfilename).pack(**button_opt)
        self.nextbtn = Tkinter.Button(self, text='Next Data', command=self.nextplot)
        self.nextbtn.pack(**button_opt)
        self.prevbtn = Tkinter.Button(self, text='Previous Data', command=self.prevplot)
        self.prevbtn.pack(**button_opt)

        self.playcheck = Tkinter.IntVar(0)
        self.playbtn = Tkinter.Button(self, text='Play', command=self.playplot)
        self.playbtn.pack(**button_opt)
        # playbtn.config(state=Tkconstants.DISABLED)
        self.pausebtn = Tkinter.Button(self, text='Pause', command=self.pauseplot)
        self.pausebtn.pack(**button_opt)

        self.peak_opt = Tkinter.IntVar()
        self.peak_opt.set(0)
        self.labelframe = Tkinter.LabelFrame(self, text='Peak detection')
        self.labelframe.pack()
        self.radio1 = Tkinter.Radiobutton(self.labelframe, text='none', variable=self.peak_opt, value=0, command=self.showpeaks)
        self.radio1.pack()
        self.radio2 = Tkinter.Radiobutton(self.labelframe, text='peakdet1', variable=self.peak_opt, value=1, command=self.showpeaks)
        self.radio2.pack()

        if self.radio_selection.get() == 1:
            self.disableButtons()

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
                self.disableButtons()
                return rd.data
        elif self.radio_selection.get() == 2:
            self.list_of_files = tkFileDialog.askopenfilenames(**self.file_opt)
            self.list_of_files = self.list_of_files.split()
            rd.readFiles(self.list_of_files)
            if self.list_of_files:
                self.plotnum.set(0)
                self.showplot()
                self.enableButtons()
            return rd.x

    def disableButtons(self):
        self.nextbtn.config(state=Tkconstants.DISABLED)
        self.prevbtn.config(state=Tkconstants.DISABLED)
        self.playbtn.config(state=Tkconstants.DISABLED)
        self.pausebtn.config(state=Tkconstants.DISABLED)

    def enableButtons(self):
        self.nextbtn.config(state=Tkconstants.NORMAL)
        self.prevbtn.config(state=Tkconstants.NORMAL)
        self.playbtn.config(state=Tkconstants.NORMAL)
        self.pausebtn.config(state=Tkconstants.NORMAL)

    def initPlot(self):
        self.f.clear()
        self.fig = self.f.add_subplot(111)
        self.fig.set_ylabel('magnitude')
        self.fig.set_xlabel('wavelength')
        self.fig.grid()
        if self.radio_selection.get() == 1:
            self.fig.set_title("Plot from single file")
        elif self.radio_selection.get() == 2:
            self.fig.set_title("Plot from file no. %s" % self.plotnum.get())

    def showplot(self):
        global wavelength, magnitude
        self.initPlot()
        if self.radio_selection.get() == 1:
            magnitude = rd.data[:, 1]
            wavelength = rd.data[:, 0]
            self.fig.plot(wavelength, magnitude, 'b')

        elif self.radio_selection.get() == 2:
            magnitude = rd.x[self.plotnum.get()][:, 1]
            wavelength = rd.x[self.plotnum.get()][:, 0]
            self.fig.plot(wavelength, magnitude, 'b')

        else:
            print "load data first"

        self.canvas.draw()

    def showpeaks(self):
        if self.peak_opt.get() == 1 and self.radio_selection.get() == 1:
            self.fig.cla()
            self.initPlot()
            self.peakdet1_setdata_single()
            self.peakdet1_showdata()
        elif self.peak_opt.get() == 1 and self.radio_selection.get() == 2:
            self.fig.cla()
            self.initPlot()
            self.peakdet1_setdata_multi()
            self.peakdet1_showdata()
        elif self.peak_opt.get() == 0:
            self.showplot()

    def nextplot(self):
        if self.plotnum.get() + 1 < len(self.list_of_files):
            self.plotnum.set(self.plotnum.get() + 1)
        elif self.plotnum.get() + 1 == len(self.list_of_files):
            self.plotnum.set(0)

        if self.peak_opt.get() == 0:
            self.showplot()
        elif self.peak_opt.get() == 1:
            self.showpeaks()

    def prevplot(self):
        if self.plotnum.get() > 0:
            self.plotnum.set(self.plotnum.get() - 1)
        elif self.plotnum.get() == 0:
            self.plotnum.set(len(self.list_of_files) - 1)
        self.showplot()

    def playplot(self):
        self.playbtn.config(state=Tkconstants.DISABLED)
        self.nextbtn.config(state=Tkconstants.DISABLED)
        self.prevbtn.config(state=Tkconstants.DISABLED)
        if len(self.list_of_files) != 0:
            for n in self.list_of_files:
                if stat.get():
                    self.nextplot()
                else:
                    stat.set(True)
                    break
                root.update()

        self.playbtn.config(state=Tkconstants.NORMAL)
        self.nextbtn.config(state=Tkconstants.NORMAL)
        self.prevbtn.config(state=Tkconstants.NORMAL)

    def pauseplot(self):
        stat.set(False)

    def peakdet1_setdata_single(self):
        self._max, self._min = pd.peakdetect(rd.data[:, 1], rd.data[:, 0], 20, 0.30)

    def peakdet1_setdata_multi(self):
        self._max, self._min = pd.peakdetect(rd.x[self.plotnum.get()][:, 1], rd.x[self.plotnum.get()][:, 0], 20, 0.30)

    def peakdet1_showdata(self):
        xm = [p[0] for p in self._max]
        ym = [p[1] for p in self._max]
        xn = [p[0] for p in self._min]
        yn = [p[1] for p in self._min]

        self.fig.plot(wavelength, magnitude, 'b', xm, ym, 'rs', xn, yn, 'go')
        self.canvas.draw()

if __name__ == '__main__':
    root = Tkinter.Tk()
    stat = Tkinter.BooleanVar(root)
    stat.set(True)
    TkDialog(root).pack()
    root.mainloop()