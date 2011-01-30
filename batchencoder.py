#!/usr/bin/python

import sys
import os
import re
import string
from getopt import getopt

CompletedMediaPath  = '~/Media/Encoded'
HandbrakePgm        = '/usr/local/bin/HandbrakeCLI'
HandbrakeProfile    = 'AppleTV 2'
MediaTypesAllowed   = ['avi', 'mkv']
ProcessTVShows      = True
ProcessMovies       = False
Debug               = False
ReadOnly            = False

OldMagicWordsList = ['xxx', 'xvidvd', 'xvid', 'x264', 'www', 'ws', 'unrated', 'ts', 
              'telesync', 'telecine', 'tc', 'swedish', 'svcd', 'se', 'screener', 
              'retail', 'rerip', 'repack', 'read.nfo', 'r5', 'r3', 'proper', 
              'pdtv', 'pal', 'ogm', 'ogg', 'ntsc', 'nfofix', 'multisubs',
              'lol', 'limited', 'internal', 'hrhdtv', 'hrhd', 'hdtvrip', 
              'hdtv', 'hdrip', 'hddvd', 'h264', 'german', 'fs', 'fragment', 
              'fov', 'dvdscreener', 'dvdscr', 'dvdrip', 'dvdivx', 'dvd', 
              'dutch', 'dts', 'dsrip', 'dsr', 'divx5', 'divx', 'dc', 'custom', 
              'cd[1-9]', 'cam', 'brrip', 'bluray', 'bdrip', 'bd5', 'ac3', 
              '720p', '720i', '576p', '576i', '480p', '480i', '1080p', '1080i']

MagicWords = ['xvid', 'x264', 'hdtv', 'fqm', 'ctu', '720p', 'lol', 'dimension', '2hd',
                'fever', 'fov', 'bia', 'proper', 'real']

class VideoMetadata:
    show    = None
    season  = None
    episode = None
    title   = None
    
    def getFormattedName(self):
        self.cleanMetadata()
        newName = ''
        
        if self.show != '':
            newName = newName + self.show + ' - '
        
        if self.season != '':
            newName = newName + self.season
        else:
            newName = newName + '0'
        
        if self.episode != '':
            newName = newName + 'x' + self.episode
        else:
            newName = newName + 'x00'
        
        if self.title != '':
            newName = newName + ' - ' + self.title
        
        newName = newName + '.m4v'
        return newName
    
    def cleanMetadata(self):
        self.show    = ' '.join(self.show.split()).title()
        self.title   = ' '.join(self.title.split()).title()
        self.season  = self.season.lstrip('0')
        self.episode = self.episode.zfill(2)
        return
    

class MediaFile:
    isTVShow = False
    meta     = VideoMetadata()
    
    basename = None     # ex.  'Doctor Who (2005) - 5x03 - Lingering.avi'
    ext      = None     # ex.  '.avi'
    filename = None     # ex.  'Doctor Who (2005) - 5x03 - Lingering'
    
    def __init__(self, file):
        printDebug('__init__()')
        self.basename = os.path.basename(file)
        self.filename, self.ext = os.path.splitext(self.basename)
        
        printDebug('basename  = ' + self.basename)
        printDebug('filename  = ' + self.filename)
        printDebug('extension = ' + self.ext)
        
        printDebug('')
        return
    
    def isAllowedExt( self ):
        for checkExt in MediaTypesAllowed:
            extAllowed = '.' + checkExt
            
            if self.ext == extAllowed:
                return True
                
        return False
    
    def checkIfTVShow( self ):
        self.isTVShow = True
        testList = [
        '\[[Ss]([0-9]+)\]_\[[Ee]([0-9]+)([^\\/]*)',                #  <!-- foo_[s01]_[e01] -->
        '[\._ \-]([0-9]+)x([0-9]+)([^\\/]*)',                      #  <!-- foo.1x09 -->
        '[\._ \-][Ss]([0-9]+)[\.\-]?[Ee]([0-9]+)([^\\/]*)',        #  <!-- foo s01e01, foo.s01.e01, foo.s01-e01 -->
        '[\._ \-]([0-9]+)([0-9][0-9])([\._ \-][^\\/]*)',           #  <!-- foo.103 -->
        '[\._ \-]p(?:ar)?t[._ -]()([ivxlcdm]+)([\._ \-][^\\/]*)'   #  <!-- Pt.I, Part XIV -->
        ]
        return
    
    def isValidVideo( self ):
        if not self.isAllowedExt():
            return False
        
        self.checkIfTVShow()
        
        if self.isTVShow == True and ProcessTVShows == True:
            return True
        
        if self.isTVShow == False and ProcessMovies == True:
            return True
        
        return False
    
    def getOutputFile( self ):
        self.setCleanFilename()
        self.setFilenameMeta()
        
        outputPath = os.path.expanduser(CompletedMediaPath)
        
        if self.meta.show == 'Unknown':
            outputFile = os.path.join(outputPath, self.filename + '.m4v')
        else:
            outputFilename = self.meta.getFormattedName()
            outputFile = os.path.join(outputPath, outputFilename)
        return outputFile
    
    def setCleanFilename( self ):
        printDebug('setCleanFilename()')
        
        cleanStringList = [
            ['[*]', re.compile(r'(\[.*\])'), ''],
            ['*.*', re.compile(r'([A-Za-z0-9\'\.]?)(?<!Mrs)(?<!Mr|Dr)\.([A-Za-z0-9\' ]*)'), '\g<1> \g<2>']
            #['variety', re.compile(r'([\ _\,\.\(\)\[\]\-]+)(ac3|dts|custom|dc|divx|divx5|dsr|dsrip|dutch|dvd|dvdrip|dvdscr|dvdscreener|screener|dvdivx|cam|fragment|fs|hdtv|hdrip|hdtvrip|internal|limited|multisubs|ntsc|ogg|ogm|pal|pdtv|proper|repack|rerip|retail|r3|r5|bd5|se|svcd|swedish|german|read.nfo|nfofix|unrated|ws|telesync|ts|telecine|tc|brrip|bdrip|480p|480i|576p|576i|720p|720i|1080p|1080i|hrhd|hrhdtv|hddvd|bluray|x264|h264|xvid|xvidvd|xxx|www.www|lol|fov|cd[1-9]|\[.*\])([ _\,\.\(\)\[\]\-]|$)', re.I), '\g<1>']            
        ]
        
        printDebug('Orig Name = ' + self.filename)
        workingString = self.filename
        
        for cleanString in cleanStringList:
            workingString = cleanString[1].sub(cleanString[2], workingString, 0)
            #printDebug('     ...... (' + str(fixcount) + ') ' + workingString)
        
        for checkWord in MagicWords:
            workingString = re.sub(r'(?i)([\ _\,\.\(\)\[\]\-]*)\b'+checkWord+r'\b', '', workingString)
        
        self.filename = workingString
        printDebug('New Name  = ' + self.filename)
        printDebug('')
        return
    
    def setFilenameMeta( self ):
        printDebug('setFilenameMeta()')
        
        showString = '([A-Za-z0-9\(\)\ \-]*[A-Za-z0-9\(\)]+)[\-\.\ ]+'
        titleString = '[\-\.\ ]*([A-Za-z0-9\(\)\ \-\.]*[A-Za-z0-9\(\)\.]*)'
        
        searchStringList = [
            ['test', '(?i)[\. _-]s(\d{1,2})[\. _-]?e(\d{1,2})(.*)'],
            ['{p}*S{s}E{e}*', showString + 'S([0-9]+)E([0-9]+)' + titleString],
            ['{p}*{s}x{e}{t}*', showString + '([0-9]+)x([0-9]+)' + titleString]
        ]
        
        printDebug('filename  = ' + self.filename)
        for searchString in searchStringList:
            checkForMatch = re.match(searchString[1], self.filename)
            
            if checkForMatch is not None:
                show, season, episode, title = checkForMatch.groups()
                printDebug('Regex Match Found!')
                printDebug('Form      =  ' + searchString[0])
                printDebug('Regex Str =  ' + searchString[1])
                printDebug('Meta      =  ' + show + ' ' + season + ' ' + episode + ' ' + title)
                self.meta.show = show
                self.meta.season = season
                self.meta.episode = episode
                self.meta.title = title
                printDebug('')
                return
        
        self.meta.show = 'Unknown'
        self.meta.season = '0'
        self.meta.episode = '00'
        self.meta.title = 'Unknown'
        printDebug('No regex match!\n')
        return
    

class HandbrakeHandler:
    def createHBCommand(self, inputFile, outputFile):
        cmd = HandbrakePgm + ' -v0 --preset ' + repr(HandbrakeProfile)
        cmd = cmd + ' -i ' + repr(inputFile)
        cmd = cmd + ' -o ' + repr(outputFile)
        return cmd
    
    def encode(self, inputFile, outputFile):
        cmd = self.createHBCommand(inputFile, outputFile)
        printDebug(cmd)
        if not ReadOnly:
            os.system(cmd)


def main(f):
    printDebug('==== ' + f + ' ===\n')
    
    thisFile = MediaFile(f)
    
    if thisFile.isValidVideo() == False:
        printError('Skipping.  Not a valid file:  ' + f)
        return 1
        
    inputFile  = f
    outputFile = thisFile.getOutputFile()
    
    print inputFile  + "  -->  " + outputFile
    
    handbrake.encode(inputFile, outputFile)

def printDebug(outputString):
    if Debug == True:
        if outputString == '':
            sys.stderr.write('\n')
        else:
            sys.stderr.write('[D]  ' + outputString + '\n')
    return

def printError( outputString ):
    sys.stderr.write( '[E]  ' + outputString + '\n' )
    return

handbrake = HandbrakeHandler()

if __name__ == "__main__":
    options, args = getopt(sys.argv[1:], 'd','dry-run')

    #Option parsing loop
    for option in options:
        if option[0] == '-d':
            Debug = True
        if option[0] == '--dry-run':
            ReadOnly = True
    
    for f in args:
	    main( f )
