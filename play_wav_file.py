#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Play Wav File
# Generated: Sun Mar  6 03:32:48 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class play_wav_file(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Play Wav File")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source("/home/pi/Media-Convert_test2_PCM_Mono_VBR_8SS_48000Hz.wav", False)
        (self.blocks_wavfile_source_0).set_max_output_buffer(1)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("/home/pi/output.wav", 1, samp_rate, 8)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_wavfile_sink_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = play_wav_file()
    tb.Start(True)
    tb.Wait()
