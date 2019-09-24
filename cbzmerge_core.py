#Copyright (C) 2019 Luca Dessì
#
#Author: Luca Dessì
#
#This file is part of cbzmerge.
#
#cbzmerge is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#cbzmerge is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Nome-Programma.  If not, see http://www.gnu.org/licenses/

import os
import tempfile
import zipfile

class cbzunite:
    
    def __init__(self, sourcefiles):
        self.filelist = sourcefiles

    def getsourcefiles(self):
        return self.filelist

    def removeall(self):
        del self.filelist[:]

    def remove(self, files):
        for item in files:
            self.filelist.remove(item)

    def addfiles(self, files):
        self.filelist.extend(files)

    def MassRename(self,dir,prefix,DstDir):
        for filename in os.listdir(dir):
            src = os.path.join(dir, filename)
            dst = os.path.join(DstDir, prefix + '_' + filename)
            os.rename(src, dst)

    def ExtractCBZ(self,file,MergeDir,prefix):
        with tempfile.TemporaryDirectory() as ExtractionDir:
            with zipfile.ZipFile(file, 'r') as cbz:
                cbz.extractall(ExtractionDir)           
            self.MassRename(ExtractionDir,prefix,MergeDir)

    def MergeCBZ(self, outputfilename, progress_callback = None):
        with tempfile.TemporaryDirectory() as MergeDir:
            if progress_callback:
                progress_callback(0)
            i=0
            zeros=len(str(len(self.filelist)))+1
            for inputfile in self.filelist:
                self.ExtractCBZ(inputfile,MergeDir,str(i).zfill(zeros))
                i=i+1
                if progress_callback:
                    progress = 100/len(self.filelist)*i
                    progress_callback(progress)
        
            with zipfile.ZipFile(outputfilename, 'w') as MergedCBZ:
                for filename in os.listdir(MergeDir):
                    MergedCBZ.write(os.path.join(MergeDir, filename), filename)
