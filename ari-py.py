#!/usr/bin/env python
import ari
import logging
logger = logging.getLogger(__name__)
logging.basicConfig()


__author__ = "Reza Baher"
__copyright__ = "Copyright 2018, The Riling Project"
__credits__ = ["rezabaher"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Reza Baher"
__email__ = "rezabaher2001@gmail.com"
__status__ = "Production"

class AriManager(object):
    STASIS_APP = "Mookey"
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.ari_username='ari-username'
        self.ari_password='ari-password'
        self.client = ari.connect('http://127.0.0.1:8088', self.ari_username, self.ari_password)
        self.client.on_channel_event('StasisStart', self.stasis_start_cb)
        self.client.on_channel_event('StasisEnd', self.stasis_end_cb)
        self.recording= ''
        self.playback=''
        self.channel=''
        self.factory = self.Factory(self.client)
        self.step=0

    def stasis_start_cb(self, channel, event):
        self.channel=channel
        self.step = 0
        print "stasis started"
        channel = channel['channel']
        channel_name = channel.json.get('name')
        channel.setChannelVar(variable='DENOISE(rx)')
        channel.setChannelVar(variable='TALK_DETECT')
        channel.setChannelVar(variable='TALK_DETECT(set)', value='2000')
        args=0
        channel.on_event('ChannelTalkingStarted', self.record , callback_args=[args])
        channel.on_event('ChannelTalkingFinished', self.stoprecord , callback_args=[args])
        channel.on_event('ChannelDtmfReceived', self.on_dtmf_received)
        channel.answer()

    def stasis_end_cb(self,channel, ev):

        print "%s has left the application" % channel.json.get('name')


    def record(self,channel, ev , callback_args):
        try:
            self.playback.stop()
        except:
            pass
        self.recording = channel.record(name="%s-%s"%(self.step,channel.json.get('id')), format='wav')


    def stoprecord(self,channel, ev ,callback_args):
        self.recording.stop()
        self.playback=channel.play(media='sound:http://localhost:8088/ari/recordings/stored/%s-%s/file?api_key=%s:%s'%(self.step,channel.json.get('id'),self.ari_username,self.ari_password))
        self.step = self.step + 1


    def on_dtmf_received(self, channel, event):
        pass


    class Factory(object):

        def __init__(self, client):
            self.client = client
            self.STASIS_APP = "Mookey"



    def Mookey(self):
        self.factory.client.run(self.factory.STASIS_APP)

    def run(self):
        self.client.run(self.STASIS_APP)


AriManager.get_instance().Mookey()

