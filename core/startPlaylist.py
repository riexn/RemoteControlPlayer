from .generatePlaylist import generatePlaylist
from .potPlayer import closePotPlayer
import os
import logging

#Creating and Configuring Logger

# Log_Format = "%(levelname)s %(asctime)s - %(message)s"
# repoPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# logging.basicConfig(filename = repoPath+"\\logfile.log",
#                     filemode = "w",
#                     format = Log_Format, 
#                     level = logging.ERROR)

# logger = logging.getLogger()

#Testing our Logger

def startPlaylist(videosFolderPath):
    # generate playlist path based on folder name
    repoPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    playlistName = videosFolderPath.split('\\')[-1]
    playlistPath = f"{repoPath}\playlists\{playlistName}.dpl"
    closePotPlayer()
    generatePlaylist(playlistPath, videosFolderPath)
    os.system("start " + playlistPath)

