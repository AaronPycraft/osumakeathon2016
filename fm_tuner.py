#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Fm Tuner
# Generated: Sun Mar  6 05:26:26 2016
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import threading
import time
import wx

class fm_tuner(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Fm Tuner")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.tuning_frequency = tuning_frequency = 90.5e6
        self.volume = volume = 1
        self.transition = transition = 1000000
        self.samp_rate = samp_rate = 2000000
        self.quadrature = quadrature = 500000
        self.low_cutoff = low_cutoff = tuning_frequency-0.1e6
        self.high_cutoff = high_cutoff = tuning_frequency+0.1e6
        self.frequency = frequency = tuning_frequency
        self.cutoff = cutoff = 100000
        self.center_freq_probe = center_freq_probe = 0
        self.ave_mag_probe = ave_mag_probe = 0
        self.audio_decimation = audio_decimation = 10

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(tuning_frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(30, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.analog_probe_avg_mag_sqrd_x_0 = analog.probe_avg_mag_sqrd_c(0, 1)
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label="Volume",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=2000,
                decimation=500,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, cutoff, transition, firdes.WIN_HAMMING, 6.76))
        _frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frequency_sizer,
        	value=self.frequency,
        	callback=self.set_frequency,
        	label='frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frequency_sizer,
        	value=self.frequency,
        	callback=self.set_frequency,
        	minimum=88e6,
        	maximum=110e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frequency_sizer)
        def _center_freq_probe_probe():
        	while True:
        		val = self.rtlsdr_source_0.get_center_freq()
        		try: self.set_center_freq_probe(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _center_freq_probe_thread = threading.Thread(target=_center_freq_probe_probe)
        _center_freq_probe_thread.daemon = True
        _center_freq_probe_thread.start()
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        def _ave_mag_probe_probe():
        	while True:
        		val = self.analog_probe_avg_mag_sqrd_x_0.level()
        		try: self.set_ave_mag_probe(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _ave_mag_probe_thread = threading.Thread(target=_ave_mag_probe_probe)
        _ave_mag_probe_thread.daemon = True
        _ave_mag_probe_thread.start()
        self.audio_sink_0 = audio.sink(samp_rate, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quadrature,
        	audio_decimation=audio_decimation,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.analog_probe_avg_mag_sqrd_x_0, 0))


# QT sink close method reimplementation

    def get_tuning_frequency(self):
        return self.tuning_frequency

    def set_tuning_frequency(self, tuning_frequency):
        self.tuning_frequency = tuning_frequency
        self.set_low_cutoff(self.tuning_frequency-0.1e6)
        self.set_high_cutoff(self.tuning_frequency+0.1e6)
        self.set_frequency(self.tuning_frequency)
        self.rtlsdr_source_0.set_center_freq(self.tuning_frequency, 0)
        self.rtlsdr_source_0.set_center_freq(self.tuning_frequency, 1)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)

    def get_transition(self):
        return self.transition

    def set_transition(self, transition):
        self.transition = transition
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature

    def get_low_cutoff(self):
        return self.low_cutoff

    def set_low_cutoff(self, low_cutoff):
        self.low_cutoff = low_cutoff

    def get_high_cutoff(self):
        return self.high_cutoff

    def set_high_cutoff(self, high_cutoff):
        self.high_cutoff = high_cutoff

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._frequency_slider.set_value(self.frequency)
        self._frequency_text_box.set_value(self.frequency)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

    def get_center_freq_probe(self):
        return self.center_freq_probe

    def set_center_freq_probe(self, center_freq_probe):
        self.center_freq_probe = center_freq_probe

    def get_ave_mag_probe(self):
        return self.ave_mag_probe

    def set_ave_mag_probe(self, ave_mag_probe):
        self.ave_mag_probe = ave_mag_probe

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = fm_tuner()
    tb.Start(True)
    tb.Wait()

