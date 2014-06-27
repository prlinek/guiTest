__author__ = "PRL"
import Tkinter
import Tkconstants
import tkFileDialog
import readdata as rd
import matplotlib.pyplot as plt  # temporarily here, plot functions will be moved to separate file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import peakdetect as pd
import numpy as np


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

        # smoothing checkbox
        self.smoothing = Tkinter.IntVar()
        self.smoothing.set(0)
        self.smoothed = Tkinter.Checkbutton(self, text='Smoothing', command=self.updatePlot, variable=self.smoothing,
                                            onvalue=1, offvalue=0)
        # self.smoothed = Tkinter.Checkbutton(self, text='Smoothing', variable=self.smoothing,
        #                                     onvalue=1, offvalue=0)
        self.smoothed.pack()

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

        Tkinter.Button(self, text='Show Intensity plot', command=self.showIntensityPlot).pack()
        # Tkinter.Button(self, text='Show wv', command=self.showFitedData).pack()

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
        options['initialdir'] = '../DataPack1'
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
                # self.slide.set(0)
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

    def set_Data(self):
        if self.radio_selection.get() == 1:
            self.xdata = rd.data[:, 0]
            self.ydata = rd.data[:, 1]
        elif self.radio_selection.get() == 2:
            self.xdata = rd.x[self.plotnum.get()][:, 0]
            self.ydata = rd.x[self.plotnum.get()][:, 1]

        if self.smoothing.get() == 1:
                self.ydata = self.smooth(self.ydata, window_len=51)

        return self.xdata, self.ydata

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

    def newShowPlot(self, xdata, ydata):
        self.initPlot()
        self.fig.plot(xdata, ydata, 'b')
        self.canvas.draw()

    # def showpeaks(self):
    #     if self.peak_opt.get() == 1 and self.radio_selection.get() == 1:
    #         self.fig.cla()
    #         self.initPlot()
    #         # x, y = self.set_Data()
    #         self.peakdet1_setdata_single()
    #         self.peakdet1_showdata()
    #         self.enable_pd1_controls()
    #         self.disable_pd2_controls()
    #
    #     elif self.peak_opt.get() == 1 and self.radio_selection.get() == 2:
    #         self.fig.cla()
    #         self.initPlot()
    #         self.peakdet1_setdata_multi()
    #         self.peakdet1_showdata()
    #         self.enable_pd1_controls()
    #         self.disable_pd2_controls()
    #
    #     elif self.peak_opt.get() == 0:
    #         # x, y = self.set_Data()
    #         # self.newShowPlot(x, y)
    #         self.showplot()
    #         self.disable_pd1_controls()
    #         self.disable_pd2_controls()
    #
    #     elif self.peak_opt.get() == 2 and self.radio_selection.get() == 1:
    #         self.fig.cla()
    #         self.initPlot()
    #         self.peakdet2_showdata_single()
    #         self.enable_pd2_controls()
    #         self.disable_pd1_controls()
    #
    #     elif self.peak_opt.get() == 2 and self.radio_selection.get() == 2:
    #         self.fig.cla()
    #         self.initPlot()
    #         self.peakdet2_showdata_multi()
    #         self.enable_pd2_controls()
    #         self.disable_pd1_controls()
    #
    def showpeaks(self, x, y):
        if self.peak_opt.get() == 1 and self.radio_selection.get() == 1:
            self.fig.cla()
            self.initPlot()
            # x, y = self.set_Data()
            self.peakdet1_setdata_single(x, y)
            self.peakdet1_showdata(x, y)
            self.enable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 1 and self.radio_selection.get() == 2:
            self.fig.cla()
            self.initPlot()
            # x, y = self.set_Data()
            self.peakdet1_setdata_multi(x, y)
            self.peakdet1_showdata(x, y)
            self.enable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 0:
            # x, y = self.set_Data()
            self.newShowPlot(x, y)
            # self.showplot()
            self.disable_pd1_controls()
            self.disable_pd2_controls()

        elif self.peak_opt.get() == 2 and self.radio_selection.get() == 1:
            self.fig.cla()
            self.initPlot()
            # x, y = self.set_Data()
            self.peakdet2_showdata_single(x, y)
            self.enable_pd2_controls()
            self.disable_pd1_controls()

        elif self.peak_opt.get() == 2 and self.radio_selection.get() == 2:
            self.fig.cla()
            self.initPlot()
            # x, y = self.set_Data()
            self.peakdet2_showdata_multi(x, y)
            self.enable_pd2_controls()
            self.disable_pd1_controls()

    def updatePlot(self):
        x, y = self.set_Data()
        if self.radio_selection.get() == 2 or self.radio_selection.get() == 1:
            if self.peak_opt.get() == 0:
                self.newShowPlot(x, y)
            elif self.peak_opt.get() == 1:
                self.showpeaks(x, y)
            elif self.peak_opt.get() == 2:
                self.showpeaks(x, y)
        # elif self.radio_selection.get() == 1:
        else:
            pass

    def onScale(self, scale_val):
        self.plotnum.set(scale_val)
        self.updatePlot()

    def nextplot(self):
        if self.plotnum.get() + 1 < len(self.list_of_files):
            self.plotnum.set(self.plotnum.get() + 1)
            self.slide.set(self.plotnum.get())
        elif self.plotnum.get() + 1 == len(self.list_of_files):
            self.plotnum.set(0)
            self.slide.set(0)

        x, y = self.set_Data()
        if self.peak_opt.get() == 0:
            # self.showplot()
            self.newShowPlot(x, y)
        elif self.peak_opt.get() == 1:
            self.showpeaks(x, y)
        elif self.peak_opt.get() == 2:
            self.showpeaks(x, y)

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

    # def peakdet1_setdata_single(self):
    #     x_res = (rd.data[len(rd.data) - 1, 0] - rd.data[0, 0]) / len(rd.data)
    #     # x_res = (xdata[len(xdata) - 1] - xdata[0]) / len(xdata)
    #     lookahead = int(self.win_size.get() / x_res)
    #     self._max, self._min = pd.peakdetect(rd.data[:, 1], rd.data[:, 0], lookahead, 0.30)

    def peakdet1_setdata_single(self, xdata, ydata):
        x_res = (xdata[len(xdata) - 1] - xdata[0]) / len(xdata)
        lookahead = int(self.win_size.get() / x_res)
        self._max, self._min = pd.peakdetect(ydata, xdata, lookahead, 0.30)

    # def peakdet1_setdata_multi(self):
    #     x_res = (rd.x[self.plotnum.get()][len(rd.x) - 1, 0] - rd.x[self.plotnum.get()][0, 0]) / len(rd.x)
    #     lookahead = int(self.win_size.get() / x_res)
    #     self._max, self._min = pd.peakdetect(rd.x[self.plotnum.get()][:, 1], rd.x[self.plotnum.get()][:, 0], lookahead,
    #                                          0.30)

    def peakdet1_setdata_multi(self, xdata, ydata):
        x_res = (xdata[len(xdata) - 1] - xdata[0]) / len(xdata)
        lookahead = int(self.win_size.get() / x_res)
        self._max, self._min = pd.peakdetect(ydata, xdata, lookahead, 0.30)

    # def peakdet1_showdata(self):
    #     xm = [p[0] for p in self._max]
    #     ym = [p[1] for p in self._max]
    #     xn = [p[0] for p in self._min]
    #     yn = [p[1] for p in self._min]
    #
    #     if self.radio_selection.get() == 1:
    #         self.fig.plot(wavelength, magnitude, 'b', xm, ym, 'rs', xn, yn, 'go')
    #     elif self.radio_selection.get() == 2:
    #         self.fig.plot(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], 'b', xm, ym, 'rs', xn, yn,
    #                       'go')
    #     self.canvas.draw()

    def peakdet1_showdata(self, xdata, ydata):
        xm = [p[0] for p in self._max]
        ym = [p[1] for p in self._max]
        xn = [p[0] for p in self._min]
        yn = [p[1] for p in self._min]

        if self.radio_selection.get() == 1:
            self.fig.plot(xdata, ydata, 'b', xm, ym, 'rs', xn, yn, 'go')
        elif self.radio_selection.get() == 2:
            self.fig.plot(xdata, ydata, 'b', xm, ym, 'rs', xn, yn, 'go')
        self.canvas.draw()

    def pd1_param_update(self):
        x, y = self.set_Data()
        self.showpeaks(x, y)

    # def peakdet2_showdata_single(self):
    #     self.pf = pd.PeakFinder(wavelength, magnitude)
    #     self.peaks = self.pf.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
    #     self.fig.plot(wavelength, magnitude, 'b', [p[0] for p in self.peaks], [p[2] for p in self.peaks], 'go',
    #                   markersize=5)
    #     self.tr = pd.PeakFinder(wavelength, magnitude, inverse=True)
    #     self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
    #     self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
    #     self.canvas.draw()
    #
    def peakdet2_showdata_single(self, xdata, ydata):
        self.pf = pd.PeakFinder(xdata, ydata)
        self.peaks = self.pf.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot(xdata, ydata, 'b', [p[0] for p in self.peaks], [p[2] for p in self.peaks], 'go',
                      markersize=5)
        self.tr = pd.PeakFinder(xdata, ydata, inverse=True)
        self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
        self.canvas.draw()

    # def peakdet2_showdata_multi(self):
    #     self.pf = pd.PeakFinder(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1])
    #     self.peaks = self.pf.get_peaks(snr=self.snr_val.get(),
    #                                    ridge_length=self.ridg_len.get())  # snr=self.snr_val.get(), ridge_length=self.ridg_len.get()
    #     self.fig.plot(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], 'b', [p[0] for p in self.peaks],
    #                   [p[2] for p in self.peaks], 'go', markersize=5)
    #     self.tr = pd.PeakFinder(rd.x[self.plotnum.get()][:, 0], rd.x[self.plotnum.get()][:, 1], inverse=True)
    #     self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
    #     self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
    #     self.canvas.draw()

    def peakdet2_showdata_multi(self, xdata, ydata):
        self.pf = pd.PeakFinder(xdata, ydata)
        self.peaks = self.pf.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot(xdata, ydata, 'b', [p[0] for p in self.peaks], [p[2] for p in self.peaks], 'go', markersize=5)
        self.tr = pd.PeakFinder(xdata, ydata, inverse=True)
        self.troughs = self.tr.get_peaks(snr=self.snr_val.get(), ridge_length=self.ridg_len.get())
        self.fig.plot([t[0] for t in self.troughs], [t[2] for t in self.troughs], 'ro', markersize=5)
        self.canvas.draw()

    def pd2_param_update(self):
        x, y = self.set_Data()
        self.showpeaks(x, y)

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

    def showIntensityPlot(self):
        xdata = rd.x[0][:, 0]
        ydata = []
        zdata = []
        for t in enumerate(self.list_of_files):
            ydata.append(rd.x[t[0]][:, 1])
            zdata.append(t[0])
        # creating a mesh of size newxdata X newzdata
        newxdata, newzdata = np.meshgrid(xdata, zdata)
        # masking data so colorbar can be used
        ydata = np.ma.array(ydata)
        plt.figure()
        plt.title('Intensity plot')
        plt.xlabel('wavelength')
        plt.ylabel('Data No.')
        plt.pcolormesh(newxdata, newzdata, ydata)
        plt.colorbar()
        plt.show(block=False)

    def showFitedData(self):
        x = rd.x[0][:, 0]
        y = rd.x[0][:, 1]
        # testing different windows
        # windows = ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
        # for w in windows:
        #     plt.plot(x, self.smooth(y, 11, w))
        #     plt.legend(windows)

        ys = self.smooth(y, window_len=6, window='blackman')
        # print len(ys)
        plt.plot(x, y, 'r', label='data')
        plt.plot(x, ys, 'b', label='smothed')
        plt.legend()
        plt.grid()
        # plt.title('Fig. 3 - Fit for Time Constant')
        plt.xlabel('wavelength')
        plt.ylabel('magnitude')
        plt.show(block=False)
        x, y = self.set_Data()
        print x, y

    def get_mean(self):
        mean_sum = 0
        for i in range(len(self.list_of_files)):
            mean_sum += np.mean(rd.x[i][:, 1])
        mean = mean_sum / len(self.list_of_files)
        return mean

    def get_std(self):
        std_sum = 0
        for i in range(len(self.list_of_files)):
            std_sum += np.std(rd.x[i][:, 1])
        std = std_sum / len(self.list_of_files)
        return std

    def smooth(self, x, window_len=20, window='hanning'):

        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")

        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")

        if window_len < 3:
            return x

        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

        s = np.r_[x[window_len-1:0:-1], x, x[-1:-window_len:-1]]
        if window == 'flat':  # moving average
            w = np.ones(window_len, 'd')
        else:
            w = eval('np.'+window+'(window_len)')

        y = np.convolve(w/w.sum(), s, mode='valid')
        return y[(window_len / 2 - 1):(-window_len / 2)]


if __name__ == '__main__':
    root = Tkinter.Tk()
    stat = Tkinter.BooleanVar(root)
    stat.set(True)
    TkDialog(root).pack()
    root.mainloop()