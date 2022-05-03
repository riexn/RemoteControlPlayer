import os

def getVideoPath(video):
    videoSplit = video.split("*")
    videoPath = videoSplit[2]
    return videoPath

def getVideoDuration(nextLine):
    nextSplit = nextLine.split("*")
    duration = nextSplit[2]
    return duration

def convertPlaylistVideosToRawData(currentVideos):
    result = []
    for index, video in enumerate(currentVideos):
        thisIterationIsDurationLine = "*duration2*" in video
        thisIterationIsPlayedLine = "*played*" in video
        thisIterationIsInvalidLine = "*invalid*" in video
        if  thisIterationIsDurationLine or thisIterationIsPlayedLine or thisIterationIsInvalidLine:
            continue

        # this is where the logic starts
        videoPath = getVideoPath(video)
        # initial object before checking if it has a duration set for it
        x = {"file":videoPath, "duration":None}
        try:
            nextLine = currentVideos[index + 1]
            nextLineIsPlayed = "*played*"  in nextLine
            if nextLineIsPlayed:
                continue
            nextLineHasDurationOfThisVideo = "*duration2*" in nextLine
            if nextLineHasDurationOfThisVideo:
                x['duration'] = getVideoDuration(nextLine)
            result.append(x)
        except:
            result.append(x)
            return result
def convertFolderVideosToRawData(folderVideos, folderPath):
    result = []
    for video in folderVideos:
        x = {"file":folderPath+ "\\" + video + "\n", "duration":None}
        result.append(x)
    return result
# converts lines to dpl file for playlist
def writeToPlaylistFile(config, rawData, playlistPath):
    playlistLines = config
    for index, item in enumerate(rawData):
        playlistLines.append(f"{index+1}*file*{item['file']}")
        if(item['duration']):
            playlistLines.append(f"{index+1}*duration2*{item['duration']}")
    with open(playlistPath, 'w', encoding='utf-8') as f:
        for line in playlistLines:
            f.write(line)


def sortRawData(rawData):
    newData = sorted(rawData, key=lambda d:d['file'])
    return newData

def getFolderVideos(videosFolderPath):
    dirContent = os.listdir(videosFolderPath)
    return dirContent


def combineRawData(rawData, folderVideos, videosFolderPath):
    rawDataVideos = [item['file'].split('\\')[-1].strip() for item in rawData]
    rawDataVideosSet = set(rawDataVideos)
    folderVideosSet = set(folderVideos)
    newVideos = list(folderVideosSet.difference(rawDataVideosSet))
    result=rawData
    for videoPath in newVideos:
        item = {"file":videosFolderPath+ "\\" + videoPath + '\n', "duration":None}
        result.append(item)
    return result


def createNewPlaylistFile(playlistPath, videosFolderPath):
    playlistConfig = ["DAUMPLAYLIST\n","playtime=0\n","topindex=0\n","saveplaypos=0\n"]
    folderVideos = getFolderVideos(videosFolderPath)
    rawData = convertFolderVideosToRawData(folderVideos, videosFolderPath)
    writeToPlaylistFile(playlistConfig, rawData, playlistPath)
    pass

def updatePlaylistFile(playlistPath, videosFolderPath):
    with open(playlistPath, encoding='utf-8') as f:
        lines = f.readlines()
        # find config last line
        configLastLineList = [idx for idx, string in enumerate(lines) if 'saveplaypos=' in string]
        if not configLastLineList:
            print('last config line not found, cannot update the playlist. Exiting.')
            return 
        configLastLineIndex = configLastLineList[0]
        playlistConfig = lines[:configLastLineIndex+1]
        currentVideos = lines[configLastLineIndex+1:]
        rawData = convertPlaylistVideosToRawData(currentVideos)
        newVideos = getFolderVideos(videosFolderPath)
        combinedRawData = combineRawData(rawData, newVideos, videosFolderPath )
        sortedRawData = sortRawData(combinedRawData)
        writeToPlaylistFile(playlistConfig, sortedRawData, playlistPath)

def generatePlaylist(playlistPath, videosFolderPath):
    fileExists = os.path.exists(playlistPath)
    videosFolderExists = os.path.exists(videosFolderPath)
    if not videosFolderExists:
        print("videos folder does not exist, existing")
        exit()
        
    if not fileExists:
        createNewPlaylistFile(playlistPath, videosFolderPath)
    else:
        updatePlaylistFile(playlistPath, videosFolderPath)

