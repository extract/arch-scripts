#!/usr/bin/python
import dbus
import dbus.glib
import subprocess

from gi.repository import GObject

class PlaybackCtl:
    prev_playback_status = None
    proc = None

    def playback_update(self, dbus_dic):
        # TODO(extract): check if spotify? or keep all media player?
        if not "PlaybackStatus" in dbus_dic:
            return

        status = dbus_dic["PlaybackStatus"]
        if status != self.prev_playback_status:
            self.prev_playback_status = status
            self.playback_change(status)

    def playback_change(self, status):
        print("Playback status changed!")
        if status == "Playing":
            if (self.proc == None):
                self.proc = subprocess.Popen("glava")
        else:
            if (self.proc != None):
                self.proc.terminate()
                self.proc = None

def catchall_handler(*args, **kwargs):
    for arg in args:
        if type(arg) is dbus.Dictionary:
            playback.playback_update(arg)

loop = GObject.MainLoop()
playback = PlaybackCtl()

bus = dbus.SessionBus()
bus.add_signal_receiver(catchall_handler,
                        interface_keyword='dbus_interface',
			            path='/org/mpris/MediaPlayer2')
loop.run()
