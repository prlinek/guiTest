__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import readdata as rd
import matplotlib.pyplot as plt  # temporarly here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import scipy.signal as s
import numpy as np
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
        # self.checkbut = Tkinter.Checkbutton(self, text='Play/Pause', command=self.playplot, variable=self.playcheck, onvalue=1, offvalue=0).pack()
        self.playbtn = Tkinter.Button(self, text='Play', command=self.playplot)
        self.playbtn.pack(**button_opt)
        # playbtn.config(state=Tkconstants.DISABLED)
        self.pausebtn = Tkinter.Button(self, text='Pause', command=self.pauseplot)
        self.pausebtn.pack(**button_opt)

        if self.radio_selection.get() == 1:
            self.nextbtn.config(state=Tkconstants.DISABLED)
            self.prevbtn.config(state=Tkconstants.DISABLED)
            self.playbtn.config(state=Tkconstants.DISABLED)
            self.pausebtn.config(state=Tkconstants.DISABLED)
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
                self.nextbtn.config(state=Tkconstants.DISABLED)
                self.prevbtn.config(state=Tkconstants.DISABLED)
                self.playbtn.config(state=Tkconstants.DISABLED)
                self.pausebtn.config(state=Tkconstants.DISABLED)
                # print len(rd.data[:, 1])
                return rd.data
        elif self.radio_selection.get() == 2:
            self.list_of_files = tkFileDialog.askopenfilenames(**self.file_opt)
            self.list_of_files = self.list_of_files.split()
            rd.readFiles(self.list_of_files)
            if self.list_of_files:
                self.plotnum.set(0)
                self.showplot()
                self.nextbtn.config(state=Tkconstants.NORMAL)
                self.prevbtn.config(state=Tkconstants.NORMAL)
                # self.playbtn.config(state=Tkconstants.NORMAL)
                # self.pausebtn.config(state=Tkconstants.NORMAL)
            return rd.x

    def showplot(self):
        global wavelength, magnitude
        self.f.clear()
        self.fig = self.f.add_subplot(111)
        self.fig.set_ylabel('magnitude')
        self.fig.set_xlabel('wavelength')
        self.fig.grid()
        if self.radio_selection.get() == 1:
            magnitude = rd.data[:, 1]
            wavelength = rd.data[:, 0]
            self.fig.set_title("Plot from single file")
            # d = rd.data[:, 1]
            # calling function for peak detection
            # p = s.find_peaks_cwt(d, np.arange(1, 30), gap_thresh=15)
            # pk = pd.peakdetect(rd.data[:, 1], rd.data[:, 0])

            # creating peak vector of zeroes
            # peaks = np.zeros(len(rd.data))
            # peak_pos = []
            # peak_val = []
            # # for all indices k obtained from function 'find_peaks_cwt' assign values of data to peaks
            # for k in p:
            #     # peaks[k] = rd.data[k, 1]
            #     peak_pos.append(rd.data[k, 0])
            #     peak_val.append(rd.data[k, 1])
            # self.fig.plot(wavelength, magnitude, 'b', peak_pos, peak_val, 'rs')
            _max, _min = pd.peakdetect(rd.data[:, 1], rd.data[:, 0], 20, 0.30)

            xm = [p[0] for p in _max]
            ym = [p[1] for p in _max]
            xn = [p[0] for p in _min]
            yn = [p[1] for p in _min]

            self.fig.plot(wavelength, magnitude, 'b', xm, ym, 'rs', xn, yn, 'go')

        elif self.radio_selection.get() == 2:
            magnitude = rd.x[self.plotnum.get()][:, 1]
            wavelength = rd.x[self.plotnum.get()][:, 0]
            self.fig.set_title("Plot from file no. %s" % self.plotnum.get())

            # peaks = []
            # peak_pos = []
            # peak_val = []
            # for z in self.list_of_files:
            #     d = rd.x[self.plotnum.get()][:, 1]
            #     p = s.find_peaks_cwt(d, np.arange(1, 10), gap_thresh=5)
            #     peaks.append(p)
            # for k in peaks[self.plotnum.get()]:
            #     peak_pos.append(rd.x[self.plotnum.get()][k, 0])
            #     peak_val.append(rd.x[self.plotnum.get()][k, 1])
            # self.fig.plot(wavelength, magnitude, 'b', peak_pos, peak_val, 'rs')

            _max, _min = pd.peakdetect(rd.x[self.plotnum.get()][:, 1], rd.x[self.plotnum.get()][:, 0], 20, 0.30)

            xm = [p[0] for p in _max]
            ym = [p[1] for p in _max]
            xn = [p[0] for p in _min]
            yn = [p[1] for p in _min]

            self.fig.plot(wavelength, magnitude, 'b', xm, ym, 'rs', xn, yn, 'go')

        else:
            print "load data first"

        # self.fig.plot(wavelength, magnitude)
        self.canvas.draw()

    def nextplot(self):
        if self.plotnum.get() + 1 < len(self.list_of_files):
            self.plotnum.set(self.plotnum.get() + 1)
        elif self.plotnum.get() + 1 == len(self.list_of_files):
            self.plotnum.set(0)
        self.showplot()


    def prevplot(self):
        if self.plotnum.get() > 0:
            self.plotnum.set(self.plotnum.get() - 1)
        elif self.plotnum.get() == 0:
            self.plotnum.set(len(self.list_of_files) - 1)
        self.showplot()

    def playplot(self):
        # # if self.playcheck.get() == 1:
        # # self.playcheck.set(0)
        # self.playbtn.config(state=Tkconstants.DISABLED)
        # self.nextbtn.config(state=Tkconstants.DISABLED)
        # self.prevbtn.config(state=Tkconstants.DISABLED)
        # if len(self.list_of_files) != 0:
        #     for n in self.list_of_files:
        #         self.nextplot()
        #         if self.playcheck.get() == 1:
        #             break
        #         # else:
        #         #     continue
        #         # time.sleep(0.5)
        #     self.playbtn.config(state=Tkconstants.NORMAL)
        #     self.nextbtn.config(state=Tkconstants.NORMAL)
        #     self.prevbtn.config(state=Tkconstants.NORMAL)
        # else:
        pass

    def pauseplot(self):
        pass
        # self.playcheck.set(1)
        # print self.playcheck.get()


if __name__ == '__main__':
    root = Tkinter.Tk()
    TkDialog(root).pack()
    root.mainloop()