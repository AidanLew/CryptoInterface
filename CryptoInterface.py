import os
import json
import signal
import subprocess
import psutil
import pyautogui as gui
from time import sleep
from datetime import datetime


class CryptoInterface:

    def __init__(self, miningProgram, miningAlgorithm, miningServer, miningAddress, workerName, miningArgs, useETHlargement, idleTime):

        self.miningProgram = miningProgram
        self.miningAlgorithm = miningAlgorithm
        self.miningServer = miningServer
        self.miningAddress = miningAddress
        self.workerName = workerName
        self.miningArgs = miningArgs
        self.useETHlargement = useETHlargement
        self.idleTime = int(idleTime)

        self.lastPosition = (0, 0)
        self.lastMove = 0
        self.isMining = False

    def terminateSubprocess(self, masterPID):

        masterPID = psutil.Process(masterPID)
        subPID = masterPID.children(recursive=True)
        for pid in subPID:
            os.kill(pid.pid, signal.SIGTERM)
        os.kill(masterPID.pid, signal.SIGTERM)

    def getTime(self):

        return datetime.now().strftime("%H:%M:%S")

    def startMining(self): 

        if self.useETHlargement == "True":
            self.ETHlargement = subprocess.Popen('ETHlargementPill-r2.exe')

        if self.miningProgram == "Gminer":
            self.mining = subprocess.Popen(f'Gminer.exe --algo {self.miningAlgorithm} --server {self.miningServer} --user {self.miningAddress}.{self.workerName} {self.miningArgs}')
        else:
            self.stopMining()
            raise ValueError('Invalid Mining Software!')

        self.isMining = True

    def stopMining(self):

        if self.useETHlargement == "True":
            self.terminateSubprocess(self.ETHlargement.pid)

        if self.isMining:
            self.terminateSubprocess(self.mining.pid)

        self.isMining = False
    
    def isIdle(self):

        if self.lastPosition == gui.position():
            self.lastMove += 1
        else:
            self.lastPosition = gui.position()
            self.lastMove = 0
        
        if self.lastMove >= self.idleTime:
            return True
        else:
            return False


with open('config.json') as config:
    config = json.load(config)

interface = CryptoInterface(**config)

while True:

    if interface.isIdle():

        if interface.isMining is False:

            print(f"{interface.getTime()} Starting Mining!")
            interface.startMining()
    else:

        if interface.isMining:

            print(f"{interface.getTime()} Terminating Mining.")
            interface.stopMining()

    sleep(1)
