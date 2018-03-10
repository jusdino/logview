'''
Created on Mar 7, 2018

@author: jusdino
'''

import pyinotify
import sys
import os
from flask_socketio import SocketIO
from pyinotify import WatchManager


class EventHandler(pyinotify.ProcessEvent):

    sio = SocketIO(message_queue=os.environ['REDIS_URI'])

    def __init__(self, wm: WatchManager):
        super(EventHandler, self).__init__()
        stat = os.stat(WATCH_FILE_PATH)
        self.inode = stat.st_ino
        self.file = open(WATCH_FILE_PATH, 'r')
        self.file.seek(0, 2)
        self.wm = wm

    def process_IN_MODIFY(self, event):
        line = self.file.read()
        if len(line) == 0:
            current = self.file.tell()
            self.file.seek(0, 2)
            eof = self.file.tell()
            self.file.seek(0)
            line = self.file.read()
            self.sio.emit('message', '<file truncated>')

        self.sio.emit('message', line)

    def process_IN_ATTRIB(self, event):
        self.file.close()
        try:
            stat = os.stat(WATCH_FILE_PATH)
        except FileNotFoundError as exc:
            print('File overwritten!', file=sys.stderr)
            raise exc

        self.inode = stat.st_ino
        self.file = open(WATCH_FILE_PATH, 'r')
        self.wm.add_watch(WATCH_FILE_PATH, pyinotify.ALL_EVENTS)
        line = self.file.read()
        self.sio.emit('message', '<File truncated>')
        self.sio.emit('message', line)
        wds = [wd for wd in self.wm.watches.keys()]
        for wd in wds:
            wm.del_watch(wd)
        self.wm.add_watch(WATCH_FILE_PATH, pyinotify.ALL_EVENTS)

    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    WATCH_FILE_PATH = os.environ['WATCH_FILE_PATH']

    wm = WatchManager()
    eh = EventHandler(wm)
    notifier = pyinotify.Notifier(wm, eh)
    wm.add_watch(WATCH_FILE_PATH, pyinotify.ALL_EVENTS)
    print('Monitoring file: {}'.format(WATCH_FILE_PATH), file=sys.stderr)
    notifier.loop()
    print('Stopped monitoring', file=sys.stderr)
