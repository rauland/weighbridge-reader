"""Module parses config files"""
import configparser
from pathlib import Path

ini = Path("config.ini").resolve()
if not ini.is_file():
    config = configparser.ConfigParser()
    config['GUI']       = { 'windowsposition':'200x60-0-50' }
    config['DEFAULT']   = { 'port':'1749' }
    config['scale1']    = { 'ip':'127.0.0.1',
                            'port':'1749' }
    config['scale2']    = { 'ip':'127.0.0.1',
                            'port':'1749' }
    with open(ini, 'w', encoding="utf-8") as configfile:
        config.write(configfile)

conf = configparser.ConfigParser()
conf.read(ini)

scales = {
    section: dict(conf[section])
    for section in conf.sections()
    if section != 'GUI'
}

windowsposition = conf['GUI']['windowsposition']
