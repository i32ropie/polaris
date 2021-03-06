# -*- coding: utf-8 -*-
from __main__ import *
from utils import *


commands = [
    '^map',
    '^m ',
    '^position',
    '^pos ',
    '^p ',
]

parameters = {('location', True)}

description = 'Returns a photo with a map for a specified location. Use *' + config['command_start'] + 'position* to get the position.'
action = 'find_location'


def run(msg):
    input = get_input(msg['text'])

    if not input:
        doc = get_doc(commands, parameters, description)
        return send_message(msg['chat']['id'], doc, parse_mode="Markdown")

    lat, lon, locality, country = get_coords(input)

    if get_command(msg['text']).startswith('m'):
        photo_url = 'https://maps.googleapis.com/maps/api/staticmap'
        photo_params = {
            'size': '640x320',
            'markers': 'color:red|label:·|' + str(lat) + ',' + str(lon),
            'key': config['api']['googledev']
        }

        message = locality + ' (' + country + ')'

        map = download(photo_url, params=photo_params)

        if map:
            send_photo(msg['chat']['id'], map)
        else:
            send_error(msg, 'download')
    else:
        if not send_location(msg['chat']['id'], lat, lon):
            send_error(msg, 'unknown')
