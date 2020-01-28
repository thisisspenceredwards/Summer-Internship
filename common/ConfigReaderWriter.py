""" ConfigReaderWriter.py """
import json
from pathlib import Path


class ConfigReaderWriter:

    def __init__(self):
        self._configFilePath = '../'
        self._configFileName = 'rPiConfig.json'


    def setFilePath(self, sstr):
        self._configFilePath = sstr

    def setFileName(self, sstr):
        self._configFileName = sstr


    def write(self, rPiConfig):
        """ Write the Raspberry config file """
                                        # convert the config into a json style string
                                        # with newlines and indent of 4, but with no 
                                        # spaces around the delimiters
        jstr = json.dumps(rPiConfig, indent=4, separators=(',', ':'))
        pth = Path(self._configFilePath + self._configFileName)
        pth.write_text(jstr)            # overwrites existing file
        return jstr


    def read(self):
        """ Read the Raspberry config file """
                                        # read the json formatted string from the disk file
        pth = Path(self._configFilePath + self._configFileName)
        sstr = pth.read_text()
        config = json.loads(sstr)       #convert to python data structure: a list of dictionaries
        return config

#
