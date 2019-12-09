#   Copyright 2019 Oliver Hamilton
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import requests
import ssdp3 as ssdp
import urllib.parse
import time


class VirtualKeys:
    UP = "38"
    DOWN = "40"
    LEFT = "37"
    RIGHT = "39"
    OK = "13"
    PLAY = "415"
    PAUSE = "19"
    STOP = "413"
    FAST_FWD = "417"
    REWIND = "412"
    TRACK_NEXT = "425"
    TRACK_PREV = "424"
    RECORD = "416"
    KP_0 = "48"
    KP_1 = "49"
    KP_2 = "50"
    KP_3 = "51"
    KP_4 = "52"
    KP_5 = "53"
    KP_6 = "54"
    KP_7 = "55"
    KP_8 = "56"
    KP_9 = "57"
    RED = "403"
    GREEN = "404"
    YELLOW = "405"
    BLUE = "406"
    BACK = "461"
    INFO = "457"
    ESCAPE = "27"
    TELETEXT = "459"
    CHANNEL_UP = "427"
    CHANNEL_DOWN = "428"
    SUBTITLE = "460"
    AUDIO_DESCRIPTION = "450"
    VOLUME_UP = "447"
    VOLUME_DOWN = "448"
    MUTE = "449"


class FreesatChannels:
    # a few samples
    BBC1 = '101'
    BBC2_HD = '102'
    ITV = '103'
    C4 = '104'
    C5_HD = '105'
    BBC1_HD = '106'


class HUMAX(object):

    found_box = False

    def __init__(self, auto_search=False):
        if auto_search:
            self.find_on_lan()

    def parse_hostport(self, hp):
        # urlparse() and urlsplit() insists on absolute URLs starting with "//"
        result = urllib.parse.urlsplit(hp)
        self.humax_ip = result.hostname
        self.humax_port = str(result.port)

    def find_on_lan(self):
        st = 'urn:rc-freetime-tv:service:freetimerc:1'
        found = ssdp.discover(st, mx=4)
        for item in found:
            if st in item.usn:
                print(item.location)
                self.parse_hostport(item.location)
                self.found_box = True
                return True

        self.found_box = False
        print('Box not found')
        return False

    def send_command(self, command):
        if self.found_box:
            url = f'http://{self.humax_ip}:{self.humax_port}/rc/remote'
            control_data = f'<?xml version="1.0" ?><remote><key code="{command}"/></remote>'
            headers = {'User-Agent': 'FreesatRemoteControlClient', 'Content-type': 'application/xaml'}
            x = requests.post(url, data=control_data, headers=headers)
        else:
            self.find_on_lan()

    def turn_to(self, channel):
        for digit in channel:
            kp_command = str(int(digit) + 48)
            self.send_command(kp_command)
            time.sleep(0.5)  # todo - find the limit

    def power(self, state, timeout=60):
        pass


freesat = HUMAX(auto_search=True)
time.sleep(1)
freesat.turn_to(FreesatChannels.BBC1_HD)
time.sleep(10)
freesat.turn_to(FreesatChannels.BBC1)

