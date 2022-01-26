from wave import open
from struct import unpack_from
import numpy as np
import sys
import aubio
#pip install git+https://github.com/aubio/aubio/
from math import isnan





class signal:
    def __init__(self, filename):
        self.filename = filename
        self.frameRate = 0
        self.signalArr = 0
        self.lengthOfSignal = 0
        self.result = 0

    def getSignal(self):
        waveFile = open('{}'.format(self.filename), 'r')
        waveFileParams = waveFile.getparams()
        waveFileFrames = waveFile.readframes(waveFileParams[0] * waveFileParams[3]) #nchannels*nframes
        out = unpack_from("%dh" % waveFileParams[0] * waveFileParams[3], waveFileFrames)
        self.frameRate = waveFileParams[2]
        if waveFileParams[0] == 2:
            left = np.array(out[0::2], dtype='float32') / 2
            right = np.array(out[1::2], dtype='float32') / 2
            self.signalArr = left + right
        else:
            self.signalArr = np.array(out, dtype='float32')
        self.lengthOfSignal = len(self.signalArr)


    def compute(self):

        f = []
        for i in range(0, int(self.lengthOfSignal/1024)):
            tolerance = 0.2
            win_s =  1024
            hop_s = 1024
            pitch_o = aubio.pitch("yin", win_s, hop_s,self.frameRate)
            pitch_o.set_unit("Hz")
            pitch_o.set_tolerance(tolerance)
            freq = pitch_o(self.signalArr[i*1024:(i+1)*1024])[0]
            if freq > 0 and freq < 500:
                f.append(freq)

        if isnan(np.median(f)):
            self.result = 0
        else:
            self.result = np.median(f)

    def getresult(self):
        if self.result <= 165:
            return 'M'
        else:
            return 'K'


def test(name):
    try:
        newSig = signal(name)
        newSig.getSignal()
        newSig.compute()
        print(newSig.getresult())
    except:
        print("M")


test(sys.argv[1])



