__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import readdata as rd
import matplotlib.pyplot as plt  # temporarily here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import peakdetect as pd


class TkDialog(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        root.title("Program")

        self.plotnum = Tkinter.IntVar()
        self.plotnum.set(0)
        self.slide_len = int(0)
        # options for a button
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP}
        radio_opt = {'fill': Tkconstants.X, 'padx': 5, 'pady': 1, 'side': Tkconstants.TOP, 'anchor': Tkconstants.W}

        # defining variable for radio buttons
        self.radio_selection = Tkinter.IntVar()
        self.radio_selection.set(1)
        self.list_of_files = []
        # defining radio buttons
        self.dataradio1 = Tkinter.Radiobutton(self, text='Single file', variable=self.radio_selection, value=1)
        self.dataradio1.pack(**radio_opt)
        self.dataradio1.config(anchor=Tkconstants.W)
        self.dataradio2 = Tkinter.Radiobutton(self, text='Multiple file', variable=self.radio_selection, value=2)
        self.dataradio2.pack(**radio_opt)
        self.dataradio2.config(anchor=Tkconstants.W)

        # defining buttons
        Tkinter.Button(self, text='Load Data', command=self.askopenfilename).pack(**button_opt)

        self.playbtn = Tkinter.Button(self, text='Play', command=self.playplot)
        self.playbtn.pack(**button_opt)
        self.pausebtn = Tkinter.Button(self, text='Pause', command=self.pauseplot)
        self.pausebtn.pack(**button_opt)

        # selection of peak detection algorithm
        self.peak_opt = Tkinter.IntVar()
        self.peak_opt.set(0)
        self.labelframe = Tkinter.LabelFrame(self, text='Peak detection')
        self.labelframe.pack(**radio_opt)
        self.radio1 = Tkinter.Radiobutton(self.labelframe, text='none', variable=self.peak_opt, value=0,
                                          command=self.showpeaks)
        self.radio1.pack(**radio_opt)
        self.radio1.config(anchor=Tkconstants.W)
        self.radio2 = Tkinter.Radiobutton(self.labelframe, text='peakdet1', variable=self.peak_opt, value=1,
                                          command=self.showpeaks)
        self.radio2.pack(**radio_opt)
        self.radio2.config(anchor=Tkconstants.W)
        self.radio3 = Tkinter.Radiobutton(self.labelframe, text='peakdet2', variable=self.peak_opt, value=2,
                                          command=self.showpeaks)
        self.radio3.pack(**radio_opt)
        self.radio3.config(anchor=Tkconstants.W)

        # setting parameter for 'peakdet1'
        self.pd1lf = Tkinter.LabelFrame(self, text='Peakdet1 parameter')
        self.pd1lf.pack()
        Tkinter.Label(self.pd1lf, text='Window size').pack()
        self.win_size = Tkinter.IntVar()
        self.win_size.set(5)
        self.win = Tkinter.Entry(self.pd1lf, textvariable=self.win_size)
        self.win.pack()
        self.pd1_but = Tkinter.Button(self.pd1lf, text='Update parameter', command=self.pd1_param_update)
        self.pd1_but.pack(**button_opt)

        # setting parameters for 'peakdet2'
        self.pd2lf = Tkinter.LabelFrame(self, text='Peakdet2 parameters')
        self.pd2lf.pack()
        Tkinter.Label(self.pd2lf, text='SNR').pack()
        self.snr_val = Tkinter.IntVar()
        self.snr_val.set(2.5)
        self.snr = Tkinter.Entry(self.pd2lf, textvariable=self.snr_val)
        self.snr.pack()
        Tkinter.Label(self.pd2lf, text='Ridge length').pack()
        self.ridg_len = Tkinter.IntVar()
        self.ridg_len.set(15)
        self.ridglen = Tkinter.Entry(self.pd2lf, textvariable=self.ridg_len)
        self.ridglen.pack()
        self.pd2_but = Tkinter.Button(self.pd2lf, text='Update parameters', command=self.pd2_param_update)
        self.pd2_but.pack(**button_opt)

        self.disable_pd1_controls()
        self.disable_pd2_controls()
        if self.radio_selection.get() == 1:
            self.disableButtons()

        # creating new frame for containing plot and toolbar
        self.frame = Tkinter.Frame(root)
        self.frame.pack(side=Tkconstants.RIGHT)
        # creating canvas for plot
        self.f = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tkconstants.BOTTOM, fill=Tkconstants.BOTH, expand=1)
        self.canvas.show()
        # creating toolbar for plot
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.pack(side=Tkconstants.BOTTOM, fill=Tkconstants.BOTH, expand=1)
        self.toolbar.update()

        self.slide = Tkinter.Scale(self.frame, orient='horizontal', length=600, from_=0, to=self.slide_len, command=self.onScale)
        self.slide.set(0)
        self.slide.pack()

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
                self.radio1.config(state=Tkconstants.NORMAL)
                self.radio2.config(state=Tkconstants.NORMAL)
                self.radio3.config(state=Tkconstants.NORMAL)
                self.peak_opt.set(0)
                self.slide.destroy()
                self.slide_len = int(0)
                self.slide = Tkinter.Scale(self.frame, orient='horizontal', length=600, from_=0, to=self.slide_len, command=self.onScale)
                self.slide.set(0)
                self.slide.pack()
                return rd.data

        elif self.radio_selection.get() == 2:
            self.list_of_files = tkFileDialog.askopenfilenames(**self.file_opt)
            self.list_of_files = self.list_of_files.split()
            rd.readFiles(self.list_of_files)
            if self.list_of_files:
                self.plotnum.set(0)
                self.showplot()
                self.enableButtons()
                self.peak_opt.set(0)

                if self.slide_len != len(self.list_of_files):
                    self.slide.destroy()
                    self.slide_len = len(self.list_of_files) - 1
                    self.slide = Tkinter.Scale(self.frame, orient='horizontal', length=600, from_=0, to=self.slide_len, command=self.onScale)
                    self.slide.set(0)
                    self.slide.pack()
            return rd.x

    def disableButtons(self):
        self.playbtn.config(state=Tkconstants.DISABLED)
        self.pausebtn.config(state=Tkconstants.DISABLED)
        self.radio1.config(state=Tkconstants.DISABLED)
        self.radio2.config(state=Tkconstants.DISABLED)
        self.radio3.config(state=Tkconstants.DISABLED)

    def enableButtons(self):
        self.playbtn.config(state=Tkconstants.NORMAL)
        self.pausebtn.config(state=Tkconstants.NORMAL)
        self.radio1.config(state=Tkconstants.NORMAL)
        self.radio2.config(state=Tkconstants.NORMAL)
        self.radio3.config(state=Tkconstants.NORMAL)

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
            self.enable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 1 and self.radio_selection.get() == 2:
            self.fig.cla()
            self.initPlot()
            self.peakdet1_setdata_multi()
            self.peakdet1_showdata()
            self.enable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 0:
            self.showplot()
            self.disable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 2 and self.radio_selection.get() == 1:
            self.fig.cla()
            self.initPlot()
            self.peakdet2_showdata_single()
            self.enable_pd2_controls()
            self.disable_pd1_controls()

        elif self.peak_opt.get() == 2 and self.radio_selection.get() == 2:
            self.fig.cla()
            self.initPlot()
            self.peakdet2_showdata_multi()
            self.enable_pd2_controls()
            self.disable_pd1_controls()

    def onScale(self, scale_val):
        self.plotnum.set(scale_val)
        if self.radio_selection.get() == 2:
            if self.peak_opt.get() == 0:
                self.showplot()
            elif self.peak_opt.get() == 1:
                self.showpeaks()
            elif self.peak_opt.get() == 2:
                self.showpeaks()
        else:
            pass

    def nextplot(self):
        if self.plotnum.get() + 1 < len(self.list_of_files):
            self.plotnum.set(self.plotnum.get() + 1)
            self.slide.set(self.plotnum.get())
        elif self.plotnum.get() + 1 == len(self.list_of_files):
            self.plotnum.set(0)
            self.slide.set(0)

        if self.peak_opt.get() == 0:
            self.showplot()
        elif self.peak_opt.get() == 1:
            self.showpeaks()
        elif self.peak_opt.get() == 2:
            self.showpeaks()

# not used anymore <- no 'Prvious data' button
    # def prevplot(self):
    #     if self.plotnum.get() > 0:
    #         self.plotnum.set(self.plotnum.get() - 1)
    #     elif self.plotnum.get() == 0:
    #         self.plotnum.set(len(self.list_of_files) - 1)
    #
    #     if self.peak_opt.get() == 0:
    #         self.showplot()
    #     elif self.peak_opt.get() == 1:
    #         self.showpeaks()
    #     elif self.peak_opt.get() == 2:
    #         self.showpeaks()

    def playplot(self):
        self.playbtn.config(state=Tkconstants.DISABLED)

        if len(self.list_of_files) != 0:
            for n in self.list_of_files:
                if stat.get():
                    self.nextplot()
                else:
                    stat.set(True)
                    break
                root.update()
                if self.plotnum.get() == (len(self.list_of_files) - 1):
                    stat.set(True)
                    self.nextplot()
                    break

        self.playbtn.config(state=Tkconstants.NORMAL)

    def pauseplot(self):
        stat.set(False)

    def peakdet1_setdata_single(self):
        x_res = (rd.data[len(rd.data) - 1, 0] - rd.data[0, 0]) / len(rd.data)
        lookahead = int(self.win_size.get() / x_res)
        self._max, self._min = pd.peakdetect(rd.data[:, 1], rd.data[:, 0], lookahead, 0.30)

    def peakdet1_setdata_multi(self):
        x_res = (rd.x[self.plotnum.get()][len(rd.x) - 1, 0] - rd.x[self.plotnum.get()][0, 0]) / len(rd.x)
        lookahead = int(self.win_size.get() / x_res)
        self._max, self._min = pd.peakdetect(rd.x[self.plotnum.get()][:, 1], rd.x[self.plotnum.get()][:, 0], lookahead,
                                             0.30)

    def peakdet1_showdata(self):
        xm = [p[0] for p in self._max]
        ym = [p[1] for p in self._max]
        xn = [p[0] for p in self._min]
        yn = [p[1] for p in self._min]
        if self.radio_selection.get() == 1:
            self.fig.plot(wavelength, magnitude, 'b', xm, ym, 'rs', xn, yn, 'go')
        elif self.radio_selection.get() == 2:
            self.fig.plot(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], 'b', xm, ym, 'rs', xn, yn,
                          'go')
        self.canvas.draw()

    def pd1_param_update(self):
        self.showpeaks()

    def peakdet2_showdata_single(self):
        self.pf = pd.PeakFinder(wavelength, magnitude)
        self.peaks = self.pf.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot(wavelength, magnitude, 'b', [p[0] for p in self.peaks], [p[2] for p in self.peaks], 'go',
                      markersize=5)
        self.tr = pd.PeakFinder(wavelength, magnitude, inverse=True)
        self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
        self.canvas.draw()

    def peakdet2_showdata_multi(self):
        self.pf = pd.PeakFinder(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1])
        self.peaks = self.pf.get_peaks(snr=self.snr_val.get(),
                                       ridge_length=self.ridg_len.get())  # snr=self.snr_val.get(), ridge_length=self.ridg_len.get()
        self.fig.plot(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], 'b', [p[0] for p in self.peaks],
                      [p[2] for p in self.peaks], 'go', markersize=5)
        self.tr = pd.PeakFinder(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], inverse=True)
        self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
        self.canvas.draw()

    def pd2_param_update(self):
        self.showpeaks()

    def disable_pd1_controls(self):
        self.win.config(state=Tkconstants.DISABLED)
        self.pd1_but.config(state=Tkconstants.DISABLED)

    def enable_pd1_controls(self):
        self.win.config(state=Tkconstants.NORMAL)
        self.pd1_but.config(state=Tkconstants.NORMAL)

    def disable_pd2_controls(self):
        self.snr.config(state=Tkconstants.DISABLED)
        self.ridglen.config(state=Tkconstants.DISABLED)
        self.pd2_but.config(state=Tkconstants.DISABLED)

    def enable_pd2_controls(self):
        self.snr.config(state=Tkconstants.NORMAL)
        self.ridglen.config(state=Tkconstants.NORMAL)
        self.pd2_but.config(state=Tkconstants.NORMAL)


if __name__ == '__main__':
    root = Tkinter.Tk()
    stat = Tkinter.BooleanVar(root)
    stat.set(True)
    TkDialog(root).pack()
    root.mainloop()