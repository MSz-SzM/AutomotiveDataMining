# MOD (Mobile Object's Detection) metrics for automatic KPI calculation.
# Copyright (C) 2022 Paweł Kowalczyk and Marcin Szelest
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import sys
import numpy
import math
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook
import xlsxwriter
import numpy as np
import pandas as pd
import csv
from pylab import *
import matplotlib.patches as mpatches
import ot

class MODinput:
    MODlocation = str
    DataList=[]
    PairedCSV=[]
    
    def __init__(self, MODlocation):
        __class__.MODlocation = MODlocation
        if  os.path.exists(self.MODlocation) :
            __class__.DataList=os.listdir(self.MODlocation)
            __class__.PairedCSV=self.PairedData()
        else:
            raise Exception("The MOD data inputs directory doesn`t exist. Make sure that ./data directory exists and its relative to the script`s work directory")


    def GetCSV(self):
        path = self.MODlocation + "/Results"
        if not os.path.exists(path):
            os.makedirs(path)
        print("In progress...")
        for i in range(0,len(self.PairedCSV)):
            print("   Log "+str(i+1)+" out of "+str(len(self.PairedCSV)))
            try:
                L=Log(i)
                filename=self.PairedCSV[L.DataPairIndex][0].replace(self.MODlocation,"").replace("_GT.csv","_MOD_ByEventMeasureOfFit.xlsx")
                filename2=self.PairedCSV[L.DataPairIndex][0].replace(self.MODlocation,"").replace("_GT.csv","_MOD_ByFrameMeasureOfFit.xlsx")
                filename3=self.PairedCSV[L.DataPairIndex][0].replace(self.MODlocation,"").replace("_GT.csv","_MOD_FalsePositivesAnalysis.xlsx")
                workbook = xlsxwriter.Workbook(path+"/"+filename)
                workbook2 = xlsxwriter.Workbook(path+"/"+filename2)
                workbook3 = xlsxwriter.Workbook(path+"/"+filename3)
                worksheet=workbook.add_worksheet()
                worksheet2=workbook2.add_worksheet()
                worksheet3=workbook3.add_worksheet()

                ######### InTime
                worksheet.write(0, 0, 'MOD Number')
                worksheet.write(0, 1, 'Avg Height')
                worksheet.write(0, 2, 'Avg Width')
                worksheet.write(0, 3, 'Start Point')
                worksheet.write(0, 4, 'End Point')
                worksheet.write(0, 5, 'First Detection')
                worksheet.write(0, 6, 'Frame Range')
                worksheet.write(0, 7, 'Frame before First Detection')
                worksheet.write(0, 8, 'Frame with Recognition')
                worksheet.write(0, 9, 'General Measure Of Similarity')
                worksheet.write(0, 10, 'Distance Similarity')
                worksheet.write(0, 11, 'Area Similarity')
                worksheet.write(0, 12, 'Shape Similarity')
                worksheet.write(0, 13, 'Jaccard Rate')


                ######## InFrame
                worksheet2.write(0,0, 'Frame Number')
                worksheet2.write(0,1, 'MOD Number')
                worksheet2.write(0,2, 'General Measure Of Similarity')
                worksheet2.write(0,3, 'Distance Similarity')
                worksheet2.write(0,4, 'Area Similarity')
                worksheet2.write(0,5, 'Shape Similarity')
                worksheet2.write(0,6, 'Jaccard')
                worksheet2.write(0,7, 'Base Difference')
                worksheet2.write(0,8, 'MODS in Frame')
                worksheet2.write(0,9, 'Recognized')
                worksheet2.write(0,10, 'False Positive')
                worksheet2.write(0,11, 'SlowDownLED')
                worksheet2.write(0,12, 'SlowDownWith')
                worksheet2.write(0,13, 'BlinkenLED')
                worksheet2.write(0,14, 'BlinkenWarn')
                worksheet2.write(0,15, 'View')
                worksheet2.write(0,16, 'MainLane')

                
                ####### FelasePositive
                worksheet3.write(0,0, 'FP Number')
                worksheet3.write(0,1, 'Lenght')
                worksheet3.write(0,2, 'Start Point')
                worksheet3.write(0,3, 'End Point')
                worksheet3.write(0,4, 'Avg Height')
                worksheet3.write(0,5, 'Avg Width')
                worksheet3.write(0,6, 'Position')
                worksheet3.write(0,7, 'Type')

                ####### Formats InTime
                boldpercent = workbook.add_format()
                boldpercent.set_bold()
                boldpercent.set_num_format('0.00')
                percent = workbook.add_format()
                percent.set_num_format('0.00')
                size = workbook.add_format()
                size.set_num_format('##0')
                comma = workbook.add_format()
                comma.set_num_format('##0.0')

                
                ####### InTime
                row=1
                row2=1
                row3=1
                column=0
                for p3d in L.MODS3D:
                    try:
                        worksheet.write(row,0, p3d.MODnumber)
                        worksheet.write(row,1, p3d.AvgHeight, comma)
                        worksheet.write(row,2, p3d.AvgWidth, comma)
                        worksheet.write(row,3, p3d.Start, size)
                        worksheet.write(row,4, p3d.End, size)
                        worksheet.write(row,5, p3d.FirstDetection, size)
                        worksheet.write(row,6, len(p3d.FramesNumbers), size)
                        worksheet.write(row,7, len(p3d.FrBeforeFirstDet), size)
                        worksheet.write(row,8, len(p3d.FramesWithRecognition), size)
                        worksheet.write(row,9, p3d.SIM, boldpercent)
                        worksheet.write(row,10, p3d.SDIST, percent)
                        worksheet.write(row,11, p3d.SAREA, percent)
                        worksheet.write(row,12, p3d.SSHAPE, percent)
                        worksheet.write(row,13, p3d.JaccardRatio, boldpercent)
                        row+=1
                    except TypeError:
                        print("TypeError in MOD"+str( p3d.MODnumber))
                        pass
                workbook.close()

                ####### Formats InFrame
                boldpercent = workbook2.add_format()
                boldpercent.set_bold()
                boldpercent.set_num_format('0.00')
                percent = workbook2.add_format()
                percent.set_num_format('0.00')
                size = workbook2.add_format()
                size.set_num_format('##0')
                comma = workbook2.add_format()
                comma.set_num_format('##0.0')

                
                ##### InFrame
                for f in L.Frames:
                    worksheet2.write(row2,8, len(f.Mod), size)
                    worksheet2.write(row2,9, f.Detected, size)
                    worksheet2.write(row2,10, f.FalsePositives, size)
                    if len(f.Mod)>0:
                        for p in f.Mod:
                            worksheet2.write(row2,0, p.FrameNumber, size)
                            worksheet2.write(row2,1, p.Number, size)
                            #worksheet2.write(row2,column+1, p.Type)
                            worksheet2.write(row2,2, p.Sim, boldpercent)
                            worksheet2.write(row2,3, p.SDist, percent)
                            worksheet2.write(row2,4, p.SArea, percent)
                            worksheet2.write(row2,5, p.SShape, percent)
                            worksheet2.write(row2,6, p.OR, boldpercent)
                            worksheet2.write(row2,7, p.BaseDif, comma)
                            worksheet2.write(row2,11, p.SlowDownLED)
                            worksheet2.write(row2,12, p.SlowDownWith)
                            worksheet2.write(row2,13, p.BlinkenLED)
                            worksheet2.write(row2,14, p.BlinkenWarn)
                            worksheet2.write(row2,15, p.View)
                            worksheet2.write(row2,16, p.MainLane)
                            row2+=1
                    else:
                        worksheet2.write(row2,column, f.Number)
                        #worksheet2.write(row2,column+1, '-')
                        worksheet2.write(row2,column+1, '-')
                        worksheet2.write(row2,column+2, '-')
                        worksheet2.write(row2,column+3, '-')
                        worksheet2.write(row2,column+4, '-')
                        worksheet2.write(row2,column+5, '-')
                        worksheet2.write(row2,column+6, '-')
                        worksheet2.write(row2,column+7, '-')
                        row2+=1
                workbook2.close()

                ####### Formats FP
                boldpercent = workbook3.add_format()
                boldpercent.set_bold()
                boldpercent.set_num_format('0.00')
                percent = workbook3.add_format()
                percent.set_num_format('0.00')
                size = workbook3.add_format()
                size.set_num_format('##0')
                comma = workbook3.add_format()
                comma.set_num_format('##0.0')
                
                ###### FalsePositives
                for fp in L.FP3D:
                    worksheet3.write(row3,column, fp.Number)
                    worksheet3.write(row3,column+1, fp.Lenght)
                    worksheet3.write(row3,column+2, int(fp.StartFrameNumber))
                    worksheet3.write(row3,column+3, int(fp.EndFrameNumber))
                    worksheet3.write(row3,column+4, fp.AvgHeight, comma)
                    worksheet3.write(row3,column+5, fp.AvgWidth, comma)
                    worksheet3.write(row3,column+6, fp.Position)
                    #worksheet3.write(row3,column+7, fp.Type)
                    row3+=1
                workbook3.close()
                print('Visualisation...')
                try:
                    L.ShowLog()
                    #L.ShowLogJaccard()
                    L.ShowFP()
                except ValueError:
                    print('Visualisation is too large for '+self.PairedCSV[i][1]+' try to resize picture')
                print('Completed')
            except ValueError:
                print("Make sure that in CSV "+self.PairedCSV[i][1]+" with system results is in correct format")


                
    def PairedData(self):
        key_gt = "_GT.csv"
        key_sys = "_system_output.csv"
        SystemData=[]
        LabelsData=[]
        Paired=[]
        for i in self.DataList:
            if i.endswith(key_gt):
                LabelsData.append(i)
            if i.endswith(key_sys):
                SystemData.append(i)
        for i in LabelsData:
            for k in SystemData:
                if i.rstrip(key_gt)[len(i.rstrip(key_gt))-36:len(i.rstrip(key_gt))]==k.rstrip(key_sys)[len(k.rstrip(key_sys))-36:len(k.rstrip(key_sys))]:
                    Paired.append([self.MODlocation+"/"+i,self.MODlocation+"/"+k])
                    break
        if len(Paired)==0:
            print("Make sure that csv with labels ends with "+ key_gt +" and csv with system results ends with "+ key_sys)
        return Paired

class WrongDiagonalForm(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)

class SysData:
    source=str
    table=[]
    def __init__(self, source):
        self.source=source
        self.table = pd.read_csv(self.source)
        self.table.drop_duplicates(subset=['Image_Number'],keep='first',inplace=True)
        self.table.set_index(self.table.columns[0])
        print("System data loaded")

class LabelsData:
    source=str
    table=[]
    def __init__(self, source):
        self.source=source
        with open(self.source,'r') as fp:
            reader = csv.reader(fp, delimiter=',')
            ldata = np.array([row for row in reader])
        self.table=pd.DataFrame(data=ldata[1:,0:], index=ldata[1:,0], columns=ldata[0,0:])
        self.table.set_index(ldata[1:,0])  #table.loc['framenumber']['colname']
        print("GT data loaded")

###########################################################################
#########################      3D-analysis     ############################
###########################################################################        

class MODintime:
    MODnumber=str
    #MODType=str 
    FramesNumbers=[] 
    MODinFrames=[]
    IgnoreBeginning=8 #PAR
    CritInd=8  #PAR
    FirstDetection=str
    R=int 
    LenL=int 
    FrAfterFirstDet=[] 
    FrBeforeFirstDet=[] 
    FrBefFDandAfCI=[] 
    Wages=[] 
    SIM=float
    SAREA=float
    SSHAPE=float
    SDIST=float
    AverageBaseDif=float 
    FramesWithRecognition=[]
    Start=str
    End=str
    AvgHeight=float
    AvgWidth=float
    JaccardRatio=float

    def __init__(self,p):  
        self.MODnumber=p[0].Number
        #self.MODType=p[0].Type
        self.MODinFrames=p
        self.FramesNumbers, self.Start, self.End=self.GetFramesNumbers()
        self.FirstDetection=self.GetFirstDetection()
        self.LenL=len(self.FramesNumbers)
        self.R=self.GetR()
        self.FrAfterFirstDet=self.GetFrAfterFirstDet()
        self.FrBeforeFirstDet=self.GetFrBeforeFirstDet()
        self.FrBefFDandAfCI=self.GetFrBefFDandAfCI()
        self.Wages=self.GetWages()
        self.SIM=self.GetSIM()
        self.SAREA=self.GetSAREA()
        self.SSHAPE=self.GetSSHAPE()
        self.SDIST=self.GetSDIST()
        self.AverageBaseDif=self.GetAverageBaseDif()
        self.FramesWithRecognition=self.GetFramesWithRecognition()
        self.AvgHeight, self.AvgWidth=self.GetAvgHeightAndWidth()
        self.JaccardRatio=self.GetJaccardRatio()
        

    def VisualizeEvaluation(self):
        cdict = {'red': ((0.0,   1.0,   1.0),
                 
                 (0.8,   1,   1),
                 (1.0,   0.19,  0.19)),
         'green': ((0.0,   0.0,   0.0),
                   
                   (0.8,   1,   1),
                   (1.0,   0.6,   0.6)),
         'blue': ((0.0,   0.1,   0.1),
                  
                  (0.8,   0.5,   0.5),
                  (1.0,   0.19,   0.19))}
        my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        cm=my_cmap
        my_yticks = ['SIM='+str(round(self.SIM,2)),'SDIST='+str(round(self.SDIST,2)),'SAREA='+str(round(self.SAREA,2)),'SSHAPE='+str(round(self.SSHAPE,2))]
        x = self.FramesNumbers
        ySIM = [1 for i in range(0,len(self.FramesNumbers))]
        yDIST = [2 for i in range(0,len(self.FramesNumbers))]
        yAREA = [3 for i in range(0,len(self.FramesNumbers))]
        ySHAPE = [4 for i in range(0,len(self.FramesNumbers))]
        yJACCARD = [5 for i in range(0,len(self.FramesNumber))]
        zSIM = [p.Sim for p in self.MODinFrames]
        zDIST = [p.SDist for p in self.MODinFrames]
        zAREA = [p.SArea for p in self.MODinFrames]
        zSHAPE = [p.SShape for p in self.MODinFrames]
        zJACCARD = [p.OR for p in self.MODinFrames]
        fig = plt.figure(figsize=(int(len(self.FramesNumbers)/3),1.5))
        sc = fig.add_subplot(111)
        plt.yticks([1,2,3,4],my_yticks)
        plt.xticks(np.arange(min(x), max(x)+1, 10), rotation='vertical')
        sc.get_xaxis().get_major_formatter().set_useOffset(False)
        sc = plt.scatter(x, ySIM, c=zSIM, vmin=0, vmax=1, marker="s", s=350, cmap=cm)
        sc = plt.scatter(x, yDIST, c=zDIST, vmin=0, vmax=1, marker="s", s=350, cmap=cm)
        sc = plt.scatter(x, yAREA, c=zAREA, vmin=0, vmax=1, marker="s", s=350, cmap=cm)
        sc = plt.scatter(x, ySHAPE, c=zSHAPE, vmin=0, vmax=1, marker="s", s=350, cmap=cm)
        sc = plt.scatter(x, yJACCARD, c=zJACCARD, vmin=0, vmax=1, marker="s", s=350, cmap=cm)       
        plt.colorbar(sc)
        plt.show()
        
    def GetJaccardRatio(self):
        correct=0
        for i in self.MODinFrames:
            if i.Detected:
                if i.OR>=0.7:
                    correct+=1
        mian=len(self.MODinFrames)
        if len(self.MODinFrames)>=self.IgnoreBeginning:
            for i in range(0,self.IgnoreBeginning):
                if self.MODinFrames[i].OR<0.7 and mian>1: 
                    mian=mian-1
                else:
                    break
            return correct/mian
        else:
            return correct/mian

    def GetFramesNumbers(self):
        numbers=[]
        start=self.MODinFrames[0].FrameNumber
        end=self.MODinFrames[len(self.MODinFrames)-1].FrameNumber
        for i in self.MODinFrames:
            numbers.append(int(i.FrameNumber))
        return numbers, start, end

    def GetAvgHeightAndWidth(self):
        rect=[]
        for i in self.MODinFrames:
            rect.append(i.Lab)
        heights=[]
        widths=[]
        for i in rect:
            heights.append(i.End().Y()-i.Beg().Y())
            widths.append(i.End().X()-i.Beg().X())
        return numpy.mean(heights), numpy.mean(widths)
        
    
    def GetFirstDetection(self):
        numd=[]
        for i in self.MODinFrames:
            if i.Detected:
                numd.append(int(i.FrameNumber))
        if len(numd)==0:
            return 'Not Detected'
        else:
            return str(min(numd))

    def GetR(self):
        first=0
        c=0
        for i in self.MODinFrames:
            if i.Detected and first==0:
                first=i.FrameNumber
            if first != 0:
                c+=1
        return c

    def FindMOD(self,nr):
        for i in self.MODinFrames:
            if str(nr)==i.FrameNumber:
                return i
            
    def GetFrAfterFirstDet(self):
        zb=[]
        start=0
        for i in self.FramesNumbers:
            if self.FindMOD(i).Detected or start==1:
                zb.append(i)
                start=1
        return zb



    def GetFrBeforeFirstDet(self):
        zb=[]
        for i in self.FramesNumbers:
            if i not in self.FrAfterFirstDet:
                zb.append(i)
        return zb


    
    def GetFrBefFDandAfCI(self):
        if self.FirstDetection=="Not Detected":
            return "Not Detected"
        else:
            overCI=[e for e in self.FrBeforeFirstDet]
            if len(self.FrBeforeFirstDet)<self.CritInd:
                return set([])
            else:
                overCI=overCI[self.CritInd-1:len(overCI)]
                return overCI

    def GetWages2(self):
        if self.FirstDetection=="Not Detected":
            return "Not Detected"
        else:
            LW=[]
            HW=[]
            SW=float
            if len(self.FrBeforeFirstDet)<self.CritInd:
                HW=[]
                coefficients=np.polyfit([1,self.CritInd-1], [0.01,1], 1)
                a=coefficients[0]
                b=coefficients[1]
                k=1
                for i in self.FrBeforeFirstDet:
                    LW.append((1/self.LenL)*(a*k+b))
                    k+=1
                SW=(self.LenL-sum(LW))/self.R
                return LW+HW+[SW for k in range(0,self.R)]
            else:
                LW=[]
                HW=[]
                SW=float
                coefficients=np.polyfit([1,self.CritInd-1], [0.01,1], 1)
                a=coefficients[0]
                b=coefficients[1]
                k=1
                for i in range(0,self.CritInd-1):
                    LW.append((1/self.LenL)*(a*k+b))
                    k+=1
                P=(self.LenL-sum(LW))
                o=0
                d=2
                for i in self.FrBefFDandAfCI:
                    o+=d
                    d+=1
                o+=self.R
                x=P/o

                s=2
                for i in self.FrBefFDandAfCI:
                    HW.append(s*x)
                    s+=1
                return LW+HW+[x for k in range(0,self.R)]
                    
    def GetWages(self):
        if self.FirstDetection=="Not Detected":
            return "Not Detected"
        else:
            LW=[]      #wages before first detection and before critical index
            HW=[]      #wages after critical index and before first detection
            SW=float   #wages after first detection
            if len(self.FrBeforeFirstDet)<=self.CritInd:
                HW=[]
                coefficients=np.polyfit([1,self.CritInd-1], [0.01,1], 1)
                a=coefficients[0]
                b=coefficients[1]
                k=1
                for i in range(0,len(self.FrBeforeFirstDet)):
                    LW.append((1/self.LenL)*(a*k+b))
                    k+=1
                SW=(self.LenL-sum(LW))/len(self.FrAfterFirstDet)
                return LW+HW+[SW for k in range(0,len(self.FrAfterFirstDet))]
            elif len(self.FrBeforeFirstDet)>self.CritInd:
                LW=[]
                HW=[]
                SW=float
                skala=2 #PAR must be highier than 1.01
                coef=np.polyfit([1,len(self.FrBeforeFirstDet)-self.CritInd], [1.01,skala], 1)
                a1=coef[0]
                b1=coef[1]
                coefl=np.polyfit([1,self.CritInd], [0.01,1], 1)
                a2=coefl[0]
                b2=coefl[1]
                #obliczanie standardowej wagi x po FD
                lw=0
                l=1
                for i in range(0,self.CritInd):
                    lw+=a2*l+b2
                    l+=1
                hw=0
                h=1
                for i in range(0,len(self.FrBeforeFirstDet)-self.CritInd):
                    hw+=a1*h+b1
                    h+=1
                x=self.LenL/(lw+hw+len(self.FrAfterFirstDet))

                l=1
                for i in range(0,self.CritInd):
                    LW.append((a2*l+b2)*x)
                    l+=1
                h=1
                for i in range(0,len(self.FrBeforeFirstDet)-self.CritInd):
                    HW.append((a1*h+b1)*x)
                    h+=1
                if len(LW)+len(HW)+len(self.FrAfterFirstDet) != self.LenL:
                    raise Exception("Wrong number of wages")
                if np.fabs(sum(LW+HW+[x for k in range(0,len(self.FrAfterFirstDet))])-self.LenL)>0.001:
                    raise Exception("Sum of wages is not equal to labels lenght")
                return LW+HW+[x for k in range(0,len(self.FrAfterFirstDet))]
                

    
    def GetSIM(self):
        suma=0
        if self.Wages=='Not Detected':
            return 0
        else:
            if len(self.Wages) != len(self.FramesNumbers):
                raise Exception("Number of calculated wages is incorrect" + self.MODnumber)
            for i in range(0,len(self.FramesNumbers)):
                suma+=self.Wages[i]*self.FindMOD(self.FramesNumbers[i]).Sim
            return suma/len(self.FramesNumbers)
    
    def GetSAREA(self):
        suma=0
        if self.Wages=='Not Detected':
            return 0
        else:
            if len(self.Wages) != len(self.FramesNumbers):
                raise Exception("Number of calculated wages is incorrect" + self.MODnumber)
            for i in range(0,len(self.FramesNumbers)):
                suma+=self.Wages[i]*self.FindMOD(self.FramesNumbers[i]).SArea
            return suma/len(self.FramesNumbers)
        
    def GetSSHAPE(self):
        suma=0
        if self.Wages=='Not Detected':
            return 0
        else:
            if len(self.Wages) != len(self.FramesNumbers):
                raise Exception("Number of calculated wages is incorrect" + self.MODnumber)
            for i in range(0,len(self.FramesNumbers)):
                suma+=self.Wages[i]*self.FindMOD(self.FramesNumbers[i]).SShape
            return suma/len(self.FramesNumbers)
    
    def GetSDIST(self):
        suma=0
        if self.Wages=='Not Detected':
            return 0
        else:
            if len(self.Wages) != len(self.FramesNumbers):
                raise Exception("Number of calculated wages is incorrect" + self.MODnumber)
            for i in range(0,len(self.FramesNumbers)):
                suma+=self.Wages[i]*self.FindMOD(self.FramesNumbers[i]).SDist
            return suma/len(self.FramesNumbers)

    def GetAverageBaseDif(self):
        obsval=[]
        for i in range(0,len(self.FramesNumbers)):
            if self.FindMOD(self.FramesNumbers[i]).BaseDif != 'not detected':
                obsval.append(self.FindMOD(self.FramesNumbers[i]).BaseDif)
        if obsval==[]:
            return 'Not Detected'
        else:
            return sum(obsval)/len(obsval)
        
    def GetFramesWithRecognition(self):
        rec=[]
        for i in self.FramesNumbers:
            if self.FindMOD(i).Detected:
                rec.append(self.FindMOD(i).FrameNumber)
        return rec
        
class FPinTime:
    Number=int
    StartFrameNumber=str
    EndFrameNumber=str
    AvgHeight=float
    AvgWidth=float
    Diagonals=[]
    Lenght=int
    Position=str
    Type=str
    FPFrames=[]
    JPGfolder=str
    CutFP=[] #2d Distributions of grayscale in box
    PadFP=[]
    GTdiagonals=[]
    GTroot=[]
    ContextData=[]
    Barycenter=[]

    def __init__(self,table,num,logName):
        self.Number=num
        self.StartFrameNumber=table[0][1]
        self.EndFrameNumber=table[-1][1]
        self.Diagonals=table
        self.Lenght=len(self.Diagonals)
        self.AvgHeight=self.GetAvgHeight()
        self.AvgWidth=self.GetAvgWidth()
        self.Position=self.GetPosition()
        #self.Type=typ
        self.FPFrames=[e[1] for e in table]
        #self.JPGfolder=MODinput().JPGlocation+"/"+logName.rstrip("LBL.csv")+"IMG"
    
    def Img2ProbNorm(self,img): # standard normalization
        return img/np.sum(img)

    def ShowBoxContext(self,nr):
        fnumbers=[e[1] for e in self.Diagonals]
        if str(nr) in fnumbers:
            if self.CutFP=="FP is not rooted":
                print("FP is not rooted")
            else:
                cv2.imshow(str(nr), self.CutFP[fnumbers.index(str(nr))])
        else:
            if self.CutFP=="FP is not rooted":
                print("FP is not rooted")
            else:
                print("FP range from "+str(fnumbers[0])+" to "+str(fnumbers[-1]))

    def GetAvgHeight(self):
        table=[]
        for i in self.Diagonals:
            table.append(i[0].End().Y()-i[0].Beg().Y())
        return numpy.mean(table)
    
    def GetAvgWidth(self):
        table=[]
        for i in self.Diagonals:
            table.append(i[0].End().X()-i[0].Beg().X())
        return numpy.mean(table)

    def GetPosition(self):
        pos=[]
        for i in self.Diagonals:
            pos.append((i[0].Beg().X()+i[0].End().X())/2)
        p=numpy.mean(pos)
        if p<300:
            return 'Left'
        elif p>900:
            return 'Right'
        else:
            return 'Center'

########################################################################################################
############################################## LOG #####################################################
########################################################################################################


class Log(MODinput):
    Name=str
    DataPairIndex=int
    ldata=[]
    sdata=[]
    Frames=[]
    MissingRes=[]
    modnumbers=[]
    MODS3D=[]
    FP3D=[]
    Conditions=[]
    JPG=str

    def __init__(self,i):
        self.Name = self.PairedCSV[i][0].replace(self.MODlocation+"/", "").replace("_GT.csv","")
        print("Creating Log: "+self.Name)
        print("Reconstruction and comparison of parallel scenarios...")
        self.DataPairIndex=i
        self.sdata=SysData(self.PairedCSV[self.DataPairIndex][1])
        self.ldata=LabelsData(self.PairedCSV[self.DataPairIndex][0])
        self.Frames=self.GetFrames()
        self.modnumbers=self.GetMODnumbers()
        print(" ")
        print("In-time events analysis...")
        self.MODS3D=self.GetMODsInTime()
        print(" ")
        print("Log contains " + str(len(self.MODS3D)) + " compact events")
        print("False positive analysis...")
        self.FP3D = self.GetFP3D()
        print(" ")
        print("Rooting and context analysis of FP...")
        self.ConnectFalsePositives()
        print(" ")
        print("Log contains " + str(len(self.FP3D)) + " False Positive events")
        #self.JPG=self.GetJPGfolder()
        print("Analysis completed")

    def GetJPGfolder(self):
        return 'C:/.../' + MODinput().PairedCSV[self.DataPairIndex][0].replace('GT.csv',"").replace(MODinput().MODlocation,'IMG')

    def ImportGTdiagonalsToFP(self):
        for fp in self.FP3D:
            GTinfo=[]
            if fp.Number.endswith("POST") or fp.Number.endswith("PRE"):
                for fr in self.Frames:
                    if fr.Number in fp.FPFrames:
                        GTinfo.append([[e[0] for e in fr.Labels],fr.Number])
            else:
                GTinfo="FP is not rooted"
            fp.GTdiagonals=GTinfo
                
                
    def MergeFP(self,startindex):
        Diagonals=[]
        FPFrames=[]
        index=startindex
        currentFP=self.Frames[startindex].FPresults[0]
        if startindex==len(self.Frames)-1:
            return [currentFP], self.Frames[startindex], self.Frames[startindex], '-'
        else:
            Type='-'
            if startindex-1 != -1:
                if currentFP.IsSimilarFPinTable3(self.Frames[startindex-1].Labels):
                    Type='Post-label'
            while (index+1 != len(self.Frames)-1 and (currentFP.IsSimilarFPinTable(self.Frames[index+1].FPresults) or (currentFP.IsSimilarFPinTable2(self.Frames[index+1].FPresults) and int(self.Frames[index+1].Number)-int(self.Frames[index].Number)>2))):
                if currentFP.IsSimilarFPinTable(self.Frames[index+1].FPresults):
                    Diagonals.append(currentFP)
                    FPFrames.append(self.Frames[index].Number)
                    self.Frames[index].FPresults.remove(currentFP)
                    currentFP=currentFP.SimilarFPinTable(self.Frames[index+1].FPresults)
                    index+=1
                elif currentFP.IsSimilarFPinTable2(self.Frames[index+1].FPresults) and (int(self.Frames[index+1].Number)-int(self.Frames[index].Number))>2:
                    Diagonals.append(currentFP)
                    FPFrames.append(self.Frames[index].Number)
                    self.Frames[index].FPresults.remove(currentFP)
                    currentFP=currentFP.SimilarFPinTable2(self.Frames[index+1].FPresults)
                    index+=1
                else:
                    print('ERROR')
            Diagonals.append(currentFP)
            FPFrames.append(self.Frames[index].Number)
            self.Frames[index].FPresults.remove(currentFP)
            if len(Diagonals)==0:
                Diagonals.append(currentFP)
            return Diagonals, self.Frames[startindex].Number, self.Frames[index].Number, Type, FPFrames
        
    def GetFP3D(self):
        FP3D = []
        ID = 0
        event = []
        seen = []
        for i in range(0, len(self.Frames)):
            progressBar(i,len(self.Frames)) #progBAR
            for j in range(0, len(self.Frames[i].FP)):
                currentFP = self.Frames[i].FP[j]
                if currentFP not in seen:
                    seen.append(currentFP)
                    event.append(currentFP)
                    missed = 0
                    for k in range(i + 1, len(self.Frames)):
                        candidates = []
                        for l in range(0, len(self.Frames[k].FP)):
                            nextFP = self.Frames[k].FP[l]
                            # Current and next object touching left border
                            if currentFP[0].Beg().X() == 0 and nextFP[0].Beg().X() == 0:
                                if nextFP not in seen and currentFP[0].ShapeSimilarity(nextFP[0]) >= 0.94:
                                    candidates.append((currentFP[0].ShapeSimilarity(nextFP[0]), nextFP))
                            # Current and next object touching right border
                            elif currentFP[0].End().X() == 1280.0 and nextFP[0].End().X() == 1280.0:
                                if nextFP not in seen and currentFP[0].ShapeSimilarity(nextFP[0]) >= 0.94:
                                    candidates.append((currentFP[0].ShapeSimilarity(nextFP[0]), nextFP))
                            # Next object touching left border
                            elif currentFP[0].Beg().X() < 200 and nextFP[0].Beg().X() == 0:
                                if nextFP not in seen and currentFP[0].ShapeSimilarity(nextFP[0]) >= 0.94:
                                    candidates.append((currentFP[0].ShapeSimilarity(nextFP[0]), nextFP))
                            # Next object touching right border
                            elif currentFP[0].End().X() > 1080 and nextFP[0].End().X() == 1280.0:
                                if nextFP not in seen and currentFP[0].ShapeSimilarity(nextFP[0]) >= 0.94 and currentFP[0].SHarm(nextFP[0]) >= 0.45:
                                    candidates.append((currentFP[0].ShapeSimilarity(nextFP[0]), nextFP))
                            # Object not touching any borders
                            else:
                                if nextFP not in seen and currentFP[0].SHarm(nextFP[0]) >= 0.6:
                                    candidates.append((currentFP[0].SHarm(nextFP[0]), nextFP))
                        # Break if no FP detected
                        if len(candidates) == 0:
                            # Allows 1 missed frame
                            if missed == 1:
                                break
                            else:
                                missed += 1
                                continue
                        else:
                            # Pick the best candidate and append it to the events
                            bestResult = max(candidates)
                            nextFP = bestResult[1]
                            seen.append(nextFP)
                            event.append(nextFP)
                            currentFP = nextFP
                            missed = 0
                    # No more similar objects - finish event
                    FP3D.append(FPinTime(event, str(ID), self.Name))
                    event = []
                    ID += 1
        return FP3D
        
    # CHANGED
    # Modification for matching FPs parents
    def ConnectFalsePositives(self):
        # Check for False Positives before the PED
        for pedestrians in self.MODS3D:
            beg = pedestrians.MODinFrames[0]
            for falsepositive in self.FP3D:
                for fp in falsepositive.Diagonals:
                    if int(beg.FrameNumber) == int(falsepositive.FPFrames[-1]) + 1:
                        # Current and next object touching left border
                        if beg.Lab.Beg().X() == 0 and fp[0].Beg().X() == 0 and beg.Lab.ShapeSimilarity(fp[0]) >= 0.94:
                            falsepositive.Number = pedestrians.MODnumber + "-PRE"
                        # Current and next object touching right border
                        elif beg.Lab.End().X() == 1280.0 and fp[0].End().X() == 1280.0 and beg.Lab.ShapeSimilarity(fp[0]) >= 0.94:
                            falsepositive.Number = pedestrians.MODnumber + "-PRE"
                        # Next object touching left border
                        elif beg.Lab.Beg().X() < 200 and fp[0].Beg().X() == 0 and beg.Lab.ShapeSimilarity(fp[0]) >= 0.94:
                            falsepositive.Number = pedestrians.MODnumber + "-PRE"
                        # Next object touching right border
                        elif beg.Lab.End().X() > 1080 and fp[0].End().X() == 1280.0 and beg.Lab.ShapeSimilarity(fp[0]) >= 0.94:
                            falsepositive.Number = pedestrians.MODnumber + "-PRE"
                        # Object not touching any borders
                        elif beg.Lab.SHarm(fp[0]) >= 0.7:
                            falsepositive.Number = pedestrians.MODnumber + "-PRE"
        # Check for False Positives after the PED
        for pedestrians in self.MODS3D:
            end = pedestrians.MODinFrames[-1]
            for falsepositive in self.FP3D:
                for fp in falsepositive.Diagonals:
                    if int(end.FrameNumber) == int(falsepositive.FPFrames[0]) - 1:
                        # Current and next object touching left border
                        if end.Lab.Beg().X() == 0 and fp[0].Beg().X() == 0 and (end.Lab.ShapeSimilarity(fp[0]) >= 0.98 or end.Lab.SHarm(fp[0]) >= 0.45):
                            falsepositive.Number = pedestrians.MODnumber + "-POST"
                        # Current and next object touching right border
                        elif end.Lab.End().X() == 1280.0 and fp[0].End().X() == 1280.0 and (end.Lab.ShapeSimilarity(fp[0]) >= 0.98 or end.Lab.SHarm(fp[0]) >= 0.45):
                            falsepositive.Number = pedestrians.MODnumber + "-POST"
                        elif end.Lab.Beg().X() < 200 and fp[0].Beg().X() == 0 and (end.Lab.ShapeSimilarity(fp[0]) >= 0.98 or end.Lab.SHarm(fp[0]) >= 0.45):
                            falsepositive.Number = pedestrians.MODnumber + "-POST"
                        # Next object touching right border
                        elif end.Lab.End().X() > 1080 and fp[0].End().X() == 1280.0 and (end.Lab.ShapeSimilarity(fp[0]) >= 0.98 or end.Lab.SHarm(fp[0]) >= 0.45):
                            falsepositive.Number = pedestrians.MODnumber + "-POST"
                        # Object not touching any borders
                        elif end.Lab.SHarm(fp[0]) >= 0.7:
                            falsepositive.Number = pedestrians.MODnumber + "-POST"
        # Give all false positives different ID if no connection to parents found
        maxID = int(self.MODS3D[-1].MODnumber) + 1
        for falsepositives in self.FP3D:
            if not (falsepositives.Number.endswith("-PRE") or falsepositives.Number.endswith("-POST")):
                falsepositives.Number = str(maxID)
                maxID += 1
                
    def MergeFalsePositives(self, startindex):
        Diagonals = []
        FPFrames = []
        index = startindex
        currentFP = self.Frames[startindex].FPresults[0]
        if startindex == len(self.Frames) - 1:
            return [currentFP], startindex, startindex, self.Frames[startindex], '-'
        else:
            Type = '-'
            if startindex - 1 != -1 and currentFP.IsSimilarFPinTable3(self.Frames[startindex - 1].Labels):
                Type = 'Post-label'
            while index + 1 != len(self.Frames) - 1 and (currentFP.IsSimilarFPinTable(self.Frames[index + 1].FPresults) or (currentFP.IsSimilarFPinTable2(self.Frames[index + 1].FPresults) and int(self.Frames[index + 1].Number) - int(self.Frames[index].Number) > 2)):
                if currentFP.IsSimilarFPinTable(self.Frames[index + 1].FPresults):
                    Diagonals.append(currentFP)
                    FPFrames.append(self.Frames[index].Number)
                    self.Frames[index].FPresults.remove(currentFP)
                    currentFP = currentFP.SimilarFPinTable(self.Frames[index + 1].FPresults)
                    index += 1
                elif currentFP.IsSimilarFPinTable2(self.Frames[index + 1].FPresults) and (int(self.Frames[index + 1].Number) - int(self.Frames[index].Number)) > 2:
                    Diagonals.append(currentFP)
                    FPFrames.append(self.Frames[index].Number)
                    self.Frames[index].FPresults.remove(currentFP)
                    currentFP = currentFP.SimilarFPinTable2(self.Frames[index + 1].FPresults)
                    index += 1
                else:
                    print('ERROR in MergeFalsePositives')
            Diagonals.append(currentFP)
            FPFrames.append(self.Frames[index].Number)
            self.Frames[index].FPresults.remove(currentFP)
            if len(Diagonals) == 0:
                Diagonals.append(currentFP)
            return Diagonals, self.Frames[startindex].Number, self.Frames[index].Number, Type, FPFrames
                
    def GetMODsInTime(self):
        Mods3d=[]
        numer=0
        for num in self.modnumbers:
            progressBar(numer, len(self.modnumbers)-1)
            try:
                full=[]
                for fram in self.Frames:
                    for pd in fram.Mod:
                        if pd.Number==num:
                            full.append(pd)
                Mods3d.append(MODintime(full))
            except IndexError:
                print('Not a single frame with MOD'+str(num)+' in csv with system results (probably GT starts earlier than system results)')
            numer+=1
        return Mods3d
                        
                

    def GetMODnumbers(self):
        numbers=[]
        for i in self.ldata.table.columns:
            if i.startswith('Obj_') and i.endswith('_X1'):
                if len(i)==8:
                    numbers.append(str(i[4]))
                elif len(i)==9:
                    numbers.append(str(i[4:6]))
                else:
                    numbers.append(str(i[4:7]))
        return numbers
            
        

    def GetFrames(self):
        self.MissingRes=[]
        f=[]
        current=0
        for i in self.ldata.table.loc[:,'ImageNumber']:
            progressBar(current,len(self.ldata.table.loc[:, 'ImageNumber']))
            if int(i) in self.sdata.table['Image_Number'].values:
                f.append(Frame(i,self.sdata,self.ldata))
            else:
                self.MissingRes.append(i)
            current+=1
        return f


#######################################   VISUALISATION   ##################################################

    # CHANGED
    # This function creates a visualization and saves the results in a pdf file
    def ShowLog(self):
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (0.8, 1, 1),
                         (1.0, 0.19, 0.19)),
                 'green': ((0.0, 0.0, 0.0),
                           (0.8, 1, 1),
                           (1.0, 0.6, 0.6)),
                 'blue': ((0.0, 0.1, 0.1),
                          (0.8, 0.5, 0.5),
                          (1.0, 0.19, 0.19))}
        cm = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
        # Create x and y ticks
        x_ticks = [float(f.Number) for f in self.Frames]
        y_ticks = ['MOD' + str(nr.MODnumber) for nr in self.MODS3D] + ['FP' + str(nr.Number) for nr in self.FP3D if not (nr.Number.endswith("-PRE") or nr.Number.endswith("-POST"))]
        # Scaling variables to divide x and y data
        x_scale = 7
        if len(self.MODS3D) == 1:
            y_scale = 1
            scaling_ratio = 3 / 4
        elif len(self.Frames) < 1200:
            y_scale = 2
            scaling_ratio = 1 / 3
        elif len(self.Frames) < 2200:
            y_scale = 1.5
            scaling_ratio = 1 / 4
        else:
            y_scale = 1
            scaling_ratio = 1 / 6
        # Set up the canvas and create a new figure
        # Ignore low dpi (matplotlib has a rendering bug)
        # Low dpi allows to generate very big visualizations but color bar is crappy
        # If you get MemoryError: In RendererAgg: Out of memory, lower dpi
        length = int(len(self.Frames) / x_scale)
        width = int(len(self.MODS3D) / y_scale)
        if len(self.Frames) < 1000:
            dpi = 80
        elif len(self.Frames) < 2000:
            dpi = 60
        elif len(self.Frames) < 3000:
            dpi = 20
        else:
            dpi = 10
            
            
            
        fig = plt.figure(figsize=(length, width), dpi=dpi)
        ax = fig.add_subplot(111)
        # Scale the figure down if the size is bigger than 200 x 200 inches
        picture_scale = 1
        if length > 200 or width > 200:
            if length > width:
                picture_scale = (length // 200) + 1
            else:
                picture_scale = (width // 200) + 1
        plt.Figure.set_size_inches(fig, (length / picture_scale), (width / picture_scale))
        # Arrange x and y ticks
        plt.xticks(np.arange(min(x_ticks), max(x_ticks) + 1, 1), rotation='vertical')
        plt.yticks([i for i in range(1, len(y_ticks) + 1)], y_ticks)
        if len(self.Frames) < 3000:
            ax.set_xlim(min(x_ticks) - 10, max(x_ticks) + 10)
            ax.set_ylim(-2, len(y_ticks) + 2)
            ax.xaxis.set_ticks(np.arange(min(x_ticks), max(x_ticks), 5))
        else:
            ax.set_xlim(min(x_ticks) - 20, max(x_ticks) + 20)
            ax.set_ylim(-4, len(y_ticks) + 4)
            ax.xaxis.set_ticks(np.arange(min(x_ticks), max(x_ticks), 10))
        # Set up graph labels and margins
        plt.xlabel('Frame Number', fontsize=40)
        plt.ylabel('MOD ID', fontsize=40)
        plt.margins(0.005, 0.01)
        
        # Algorithm used to generate data for the visualization using TSR3D
        y = 1
        for veh in self.MODS3D:
            Y = [y for i in range(0, len(self.Frames))]
            zBEG = []
            zSIM = []
            j = 0
            found = 0
            for f in x_ticks:
                if f in veh.FramesNumbers:
                    if j < 1:  # PAR = CriticalIndex
                        zBEG.append(veh.MODinFrames[j].Sim)
                        zSIM.append(np.nan)
                    else:
                        zSIM.append(veh.MODinFrames[j].Sim)
                        zBEG.append(np.nan)
                    j += 1
                    if found == 0:
                        start = f
                        found = 1
                else:
                    zSIM.append(np.nan)
                    zBEG.append(np.nan)
            # Plot data and flags on the graph
            plt.scatter(x_ticks, Y, c=zBEG, vmin=0, vmax=1, marker="+", s=60, cmap=cm)
            sc = plt.scatter(x_ticks, Y, c=zSIM, vmin=0, vmax=1, marker="s", s=160, cmap=cm)
            plt.annotate(y_ticks[y - 1] + '     Len=' + str(len(veh.FramesNumbers)) + '     Sim=' + str(round(veh.SIM * 100, 1)) + '%', (start + 1.5, Y[0] - scaling_ratio / 2 * picture_scale))
            y += 1
        # Algorithm used to generate data for the visualization using FP3D
        y = 0
        for falsepositives in self.FP3D:
            # Regular False Positives
            if not (falsepositives.Number.endswith("-PRE") or falsepositives.Number.endswith("-POST")):
                Y = [y + len(self.MODS3D) + 1 for i in range(0, len(self.Frames))]
                z = []
                found = 0
                # Find False Positives
                for frame in x_ticks:
                    if str(int(frame)) in falsepositives.FPFrames:
                        z.append(0.4)
                        if found == 0:
                            start = frame
                            found = 1
                    else:
                        z.append(np.nan)
                # Plot data and flags on the graph
                if falsepositives.Position == 'Center':
                    if falsepositives.AvgWidth > 100:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="^", s=600, cmap='Greys')
                    elif falsepositives.AvgWidth > 80:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="^", s=300, cmap='Greys')
                    else:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="^", s=100, cmap='Greys')
                elif falsepositives.Position == 'Right':
                    if falsepositives.AvgWidth > 100:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker=">", s=600, cmap='Greys')
                    elif falsepositives.AvgWidth > 80:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker=">", s=300, cmap='Greys')
                    else:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker=">", s=100, cmap='Greys')
                elif falsepositives.Position == 'Left':
                    if falsepositives.AvgWidth > 100:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="<", s=600, cmap='Greys')
                    elif falsepositives.AvgWidth > 80:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="<", s=300, cmap='Greys')
                    else:
                        plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker="<", s=100, cmap='Greys')
                # Annotate the graph with length
                plt.annotate(y_ticks[y + len(self.MODS3D)] + '   Len=' + str(len(falsepositives.FPFrames)), (start - (1 / 2), Y[0] - scaling_ratio / 2 * picture_scale))
                y += 1
            else:
                # False Positives with parents
                start = int(falsepositives.Number.split('-')[0])
                Y = [start + 1 for i in range(0, len(self.Frames))]
                z = []
                # Find False Positives
                for frame in x_ticks:
                    if str(int(frame)) in falsepositives.FPFrames:
                        z.append(1)
                    else:
                        z.append(np.nan)
                # Plot data and flags on the graph
                plt.scatter(x_ticks, Y, c=z, vmin=0, vmax=1, marker='s', s=160, cmap='gray', facecolors='none', edgecolors='gray')
        # Set up a color bar
        cbar = plt.colorbar(sc)
        cbar.ax.tick_params(labelsize=max(18, min(70, int(len(self.MODS3D) / 2))))
        cbar.ax.set_ylabel('Quality of detection', fontsize=40, rotation=270, labelpad=40)
        # Save and close the graph
        fig.savefig(self.MODlocation + '/Results/' + self.Name.rstrip('.csv') + '_MOD_QualityVisualisation' + '.pdf', bbox_inches='tight', format='pdf')
        plt.close()
        



######  ShowFP  ########
    def ShowFP(self):
        cdict = {'red': ((0.0,   1.0,   1.0),
                    (1.0,   0.19,  0.19)),
         'green': ((0.0,   0.0,   0.0),
                   (1.0,   0.6,   0.6)),
         'blue': ((0.0,   0.1,   0.1),
                  (1.0,   0.19,   0.19))}
        my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        cm=my_cmap
        my_yticks = ['FP'+str(nr.Number) for nr in self.FP3D]
        x=[int(f.Number) for f in self.Frames]
        #fig = plt.figure(figsize=(int(len(self.Frames)/15),int(len(self.FP3D)/15)))
        fig = plt.figure(figsize=(min(int(len(self.Frames)/15),900),min(int(len(self.FP3D)/3),100)))
        sc = fig.add_subplot(111)
        plt.yticks([i for i in range(1,len(self.FP3D)+1)],my_yticks)
        plt.xticks(np.arange(min(x), max(x)+1, 10), rotation='vertical')
        plt.xlabel('Frame Number', fontsize=max(18,min(70,int(len(self.FP3D)/4))))
        plt.ylabel('FP ID', fontsize=max(18,min(70,int(len(self.FP3D)/4))))
        plt.margins(0.005,0.01)
        sc.get_xaxis().get_major_formatter().set_useOffset(False)
        y=1
        for veh in self.FP3D:
            Y=[y for i in range(0,len(self.Frames))]
            z=[]
            j=0
            found=0
            for f in x:
                if str(f) in veh.FPFrames:
                    if veh.Type=='Post-label' or len(veh.FPFrames)<=10:
                        z.append(1)
                        j+=1
                        if found==0:
                            start=f
                            found=1
                    else:
                        z.append(0)
                        j+=1
                        if found==0:
                            start=f
                            found=1
                else:
                    z.append(np.nan)
            if veh.Position=='Center':
                if veh.AvgWidth>100:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="^", s=600, cmap=cm)
                elif veh.AvgWidth>80:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="^", s=300, cmap=cm)
                else:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="^", s=100, cmap=cm)
            elif veh.Position=='Right':
                if veh.AvgWidth>100:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker=">", s=600, cmap=cm)
                elif veh.AvgWidth>80:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker=">", s=300, cmap=cm)
                else:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker=">", s=100, cmap=cm)
            elif veh.Position=='Left':
                if veh.AvgWidth>100:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="<", s=600, cmap=cm)
                elif veh.AvgWidth>80:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="<", s=300, cmap=cm)
                else:
                    sc = plt.scatter(x, Y, c=z, vmin=0, vmax=1, marker="<", s=100, cmap=cm)
            plt.annotate(my_yticks[y-1]+'     Len='+str(len(veh.FPFrames)),(start-(1/2),Y[0]))
            y+=1
        red_patch = mpatches.Patch(color='red', label='Unclassified and long')
        green_patch = mpatches.Patch(color='green', label='Post-label or short')
        plt.legend(handles=[red_patch, green_patch], loc=4)
        fig.savefig(self.MODlocation+'/Results/'+self.Name.rstrip('.csv')+'_MOD_FalsePositiveVisualization'+'.pdf', bbox_inches='tight')
        plt.close()


    def ShowLogJaccard(self):
        cdict = {'red': ((0.0,   1.0,   1.0),
                 (0.7,   1,   1),
                 (1.0,   0.19,  0.19)),
         'green': ((0.0,   0.0,   0.0),
                   (0.7,   1,   1),
                   (1.0,   0.6,   0.6)),
         'blue': ((0.0,   0.1,   0.1),
                  (0.7,   0.5,   0.5),
                  (1.0,   0.19,   0.19))}
        my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        #cm=my_cmap
        cm = plt.cm.get_cmap('RdYlGn')
        my_yticks = ['MOD'+str(nr.MODnumber) for nr in self.MODS3D]
        x=[float(f.Number) for f in self.Frames]
        fig = plt.figure(figsize=(int(len(self.Frames)/15),int(len(self.MODS3D)/3)))
        sc = fig.add_subplot(111)
        plt.yticks([i for i in range(1,len(self.MODS3D)+1)],my_yticks)
        plt.xticks(np.arange(min(x), max(x)+1, 10), rotation='vertical')
        plt.xlabel('Frame Number', fontsize=20)               #max(18,min(70,int(len(self.MODS3D)/4))))
        plt.ylabel('MOD ID', fontsize=20)                  #max(18,min(70,int(len(self.MODS3D)/4))))
        plt.margins(0.005,0.1)
        sc.get_xaxis().get_major_formatter().set_useOffset(False)
        y=1
        for veh in self.MODS3D:
            Y=[y for i in range(0,len(self.Frames))]
            zSIM=[]
            j=0
            found=0
            for f in x:
                if f in veh.FramesNumbers:
                    zSIM.append(veh.MODinFrames[j].OR)
                    j+=1
                    finish=f
                    if found==0:
                        start=f
                        found=1
                else:
                    zSIM.append(np.nan)
            sc = plt.scatter(x, Y, c=zSIM, vmin=0, vmax=1, marker="s", s=200, cmap=cm)
            plt.annotate(my_yticks[y-1]+'     Len='+str(len(veh.FramesNumbers))+'     Jaccard='+str(round(veh.JaccardRatio*100,1))+'%',(start-(1/2),Y[0]-(1/4)))
            y+=1
        cbar=plt.colorbar(sc)
        #cbar.ax.tick_params(labelsize=max(18,min(70,int(len(self.MODS3D)/2))))
        fig.savefig(self.MODlocation+'/Results/'+self.Name.rstrip('.csv')+'_MOD_JaccardQualityVisualisation'+'.pdf', bbox_inches='tight')
        plt.close()

    def ShowEvaluation(self,nr):
        for i in self.MODS3D:
            if i.MODnumber==str(nr):
                i.VisualizeEvaluation()
                break
    
    def ShowFrame(self,nr):
        for i in self.Frames:
            if str(nr)==i.Number:
                plt.figure(figsize=(15,12))
                plt.ylim(0, 971)
                plt.xlim(0, 1280)
                for l in i.Labels:
                    plt.plot([l[0].Beg().X(),l[0].End().X()],[l[0].Beg().Y(),l[0].Beg().Y()],color="red")
                    plt.plot([l[0].Beg().X(),l[0].End().X()],[l[0].End().Y(),l[0].End().Y()],color="red")
                    plt.plot([l[0].Beg().X(),l[0].Beg().X()],[l[0].Beg().Y(),l[0].End().Y()],color="red")
                    plt.plot([l[0].End().X(),l[0].End().X()],[l[0].Beg().Y(),l[0].End().Y()],color="red")
                for r in i.Results:
                    plt.plot([r.Beg().X(),r.End().X()],[r.Beg().Y(),r.Beg().Y()],linestyle="-.",color="blue")
                    plt.plot([r.Beg().X(),r.End().X()],[r.End().Y(),r.End().Y()],linestyle="-.",color="blue")
                    plt.plot([r.Beg().X(),r.Beg().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="blue")
                    plt.plot([r.End().X(),r.End().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="blue")
                for r in i.FP:
                    plt.plot([r.Beg().X(),r.End().X()],[r.Beg().Y(),r.Beg().Y()],linestyle="-.",color="yellow")
                    plt.plot([r.Beg().X(),r.End().X()],[r.End().Y(),r.End().Y()],linestyle="-.",color="yellow")
                    plt.plot([r.Beg().X(),r.Beg().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="yellow")
                    plt.plot([r.End().X(),r.End().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="yellow")
                plt.show()

    def ShowFrameWithJPG(self,nr):
        if int(nr) > int(self.Frames[-1].Number):
            print('Log ends at frame '+str(self.Frames[-1].Number))
        if int(nr) < int(self.Frames[0].Number):
            print('Log starts at frame '+str(self.Frames[0].Number))
        JPGfolder='C:/...' #path to folder with frames
        for i in self.Frames:
            if str(nr)==i.Number:
                fig=plt.figure(figsize=(15,12))
                plt.ylim(0, 971)
                plt.xlim(0, 1280)
                wysopi=10
                plt.annotate(r''+str(nr),xy=(600,10),xytext=(600,10),fontsize=12, color="white")
                for l in i.Labels:
                    plt.plot([l[0].Beg().X(),l[0].End().X()],[l[0].Beg().Y(),l[0].Beg().Y()],color="red")
                    plt.plot([l[0].Beg().X(),l[0].End().X()],[l[0].End().Y(),l[0].End().Y()],color="red")
                    plt.plot([l[0].Beg().X(),l[0].Beg().X()],[l[0].Beg().Y(),l[0].End().Y()],color="red")
                    plt.plot([l[0].End().X(),l[0].End().X()],[l[0].Beg().Y(),l[0].End().Y()],color="red")
                    plt.annotate(r'MOD'+l[1], xy=(l[0].End().X(), l[0].End().Y()), xycoords='data', xytext=(-5, +wysopi), textcoords='offset points', fontsize=8, color="red", arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0", color="red"))
                    wysopi+=10
                for r in i.Results:
                    plt.plot([r.Beg().X(),r.End().X()],[r.Beg().Y(),r.Beg().Y()],linestyle="-.",color="blue")
                    plt.plot([r.Beg().X(),r.End().X()],[r.End().Y(),r.End().Y()],linestyle="-.",color="blue")
                    plt.plot([r.Beg().X(),r.Beg().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="blue")
                    plt.plot([r.End().X(),r.End().X()],[r.Beg().Y(),r.End().Y()],linestyle="-.",color="blue")
                for r in i.FP:
                    plt.plot([r[0].Beg().X(),r[0].End().X()],[r[0].Beg().Y(),r[0].Beg().Y()],linestyle="-",color="yellow")
                    plt.plot([r[0].Beg().X(),r[0].End().X()],[r[0].End().Y(),r[0].End().Y()],linestyle="-",color="yellow")
                    plt.plot([r[0].Beg().X(),r[0].Beg().X()],[r[0].Beg().Y(),r[0].End().Y()],linestyle="-",color="yellow")
                    plt.plot([r[0].End().X(),r[0].End().X()],[r[0].Beg().Y(),r[0].End().Y()],linestyle="-",color="yellow")
                    plt.annotate(r'FP', xy=(r[0].End().X(), r[0].End().Y()), xycoords='data', xytext=(-5, +wysopi), textcoords='offset points', fontsize=8, color="yellow", arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0", color="yellow"))
                    wysopi+=10
                img = imread(JPGfolder+'/'+'FrameId_'+str(nr)+'.jpg')
                plt.imshow(img,zorder=0,extent=[0,1280,0,971])
                plt.show()
                fig.savefig('C:/.../Results/Frames/'+str(nr)+'.png')
                
        for i in self.Frames:
            if str(nr)==i.Number:
                print("-------------------------")
                print("-------------------------")
                print('Objects: '+str(len(i.Mod)))
                print('Detected: '+str(i.Detected))
                print('False Positives: '+str(i.FalsePositives))
                print("-------------------------")
                print("-------------------------")
                for p in i.Mod:
                    print("MOD"+p.Number)
                    if p.Detected==False:
                        print(p.Result)
                        print("-------------------------")
                    else:
                        print("Detected")
                        print("%.2f - Distance" %p.SDist)
                        print("%.2f - Area" %p.SArea)
                        print("%.2f - Shape" %p.SShape)
                        print("%.2f %s" %(p.Sim, '- Similarity'))
                        print("%.2f - Jaccard Index" %p.OR)
                        print("-------------------------")

    def ShowMODSWithJPG(self,nr):
        if int(nr) > int(self.Frames[-1].Number):
            print('Log ends at frame '+str(self.Frames[-1].Number))
        if int(nr) < int(self.Frames[0].Number):
            print('Log starts at frame '+str(self.Frames[0].Number))
        
        JPGfolder='C:/...' #path to folder with frames from ADTF_frame_grabber_2.0.9
        for i in self.Frames:
            if str(nr)==i.Number:
                plt.figure(figsize=(15,12))
                plt.ylim(0, 971)
                plt.xlim(0, 1280)
                wysopi=10
                for p in i.Mod:
                    plt.plot([p.Lab.Beg().X(),p.Lab.End().X()],[p.Lab.Beg().Y(),p.Lab.Beg().Y()],color="red")
                    plt.plot([p.Lab.Beg().X(),p.Lab.End().X()],[p.Lab.End().Y(),p.Lab.End().Y()],color="red")
                    plt.plot([p.Lab.Beg().X(),p.Lab.Beg().X()],[p.Lab.Beg().Y(),p.Lab.End().Y()],color="red")
                    plt.plot([p.Lab.End().X(),p.Lab.End().X()],[p.Lab.Beg().Y(),p.Lab.End().Y()],color="red")
                    plt.annotate(r'MOD'+p.Number, xy=(p.Lab.End().X(), p.Lab.End().Y()), xycoords='data', xytext=(-5, +wysopi), textcoords='offset points', fontsize=8, color="red", arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0", color="red"))
                    wysopi+=10
                    if p.Detected:
                        plt.scatter([p.Lab.Beg().X(),],[p.Lab.Beg().Y(),], 30, color ='yellow')
                        plt.scatter([p.Result.Beg().X(),],[p.Result.Beg().Y(),], 30, color ='yellow')
                        plt.plot([p.Lab.Beg().X(),p.Result.Beg().X()],[p.Lab.Beg().Y(),p.Result.Beg().Y()],linestyle="-",color="yellow")
                        plt.plot([p.Result.Beg().X(),p.Result.End().X()],[p.Result.Beg().Y(),p.Result.Beg().Y()],linestyle="-.",color="aqua")
                        plt.plot([p.Result.Beg().X(),p.Result.End().X()],[p.Result.End().Y(),p.Result.End().Y()],linestyle="-.",color="aqua")
                        plt.plot([p.Result.Beg().X(),p.Result.Beg().X()],[p.Result.Beg().Y(),p.Result.End().Y()],linestyle="-.",color="aqua")
                        plt.plot([p.Result.End().X(),p.Result.End().X()],[p.Result.Beg().Y(),p.Result.End().Y()],linestyle="-.",color="aqua")
                img = imread(JPGfolder+'/'+'FrameId_'+str(nr)+'.jpg')
                plt.imshow(img,zorder=0,extent=[0,1280,0,971])
                plt.show()
        for i in self.Frames:
            if str(nr)==i.Number:
                print("-------------------------")
                print("-------------------------")
                print('Objects: '+str(len(i.Mod)))
                print('Detected: '+str(i.Detected))
                print('False Positives: '+str(i.FalsePositives))
                print("-------------------------")
                print("-------------------------")
                for p in i.Mod:
                    print("MOD"+p.Number)
                    if p.Detected==False:
                        print(p.Result)
                        print("-------------------------")
                    else:
                        print("Detected")
                        print("%.2f %% - Distance Similarity" %p.SDist)
                        print("%.2f %% - Area Similarity" %p.SArea)
                        print("%.2f %% - Shape Similarity" %p.SShape)
                        print("%.2f %s" %(p.Sim, '% - General Similarity'))
                        print("%.3f %% - Luminescence Distance Similarity" % p.Lab.LumDistanceSimilarity(p.Result))
                        print("%.2f %% - Jaccard Index" %p.OR)

                        #print("Label:  "+p.Lab.ShowDiagonal() )
                        #print("Result: "+p.Result.ShowDiagonal())
                        print("-------------------------")


    def SSF(self,nr): #StorySoFar
        
        cdict = {'red': ((0.0,   1.0,   1.0),
                 (0.8,   1,   1),
                 (1.0,   0.19,  0.19)),
         'green': ((0.0,   0.0,   0.0),
                   (0.8,   1,   1),
                   (1.0,   0.6,   0.6)),
         'blue': ((0.0,   0.1,   0.1),
                  (0.8,   0.5,   0.5),
                  (1.0,   0.19,   0.19))}
        my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        cm=my_cmap

        if int(nr) > int(self.Frames[-1].Number):
            print('Log ends at frame '+str(self.Frames[-1].Number))
        if int(nr) < int(self.Frames[0].Number):
            print('Log starts at frame '+str(self.Frames[0].Number))
        JPGfolder=self.JPG #path to folder with frames from ADTF_frame_grabber_2.0.9
        for i in self.Frames:
            if str(nr)==i.Number:
                fig=plt.figure(figsize=(15,12))
                plt.ylim(0, 971)
                plt.xlim(0, 1280)
                wysopi=20
                plt.annotate(r''+str(nr),xy=(600,10),xytext=(600,10),fontsize=12, color="white")
                for l in i.Mod:
                    plt.plot([l.Lab.Beg().X(),l.Lab.End().X()],[l.Lab.Beg().Y(),l.Lab.Beg().Y()],color="red")
                    plt.plot([l.Lab.Beg().X(),l.Lab.End().X()],[l.Lab.End().Y(),l.Lab.End().Y()],color="red")
                    plt.plot([l.Lab.Beg().X(),l.Lab.Beg().X()],[l.Lab.Beg().Y(),l.Lab.End().Y()],color="red")
                    plt.plot([l.Lab.End().X(),l.Lab.End().X()],[l.Lab.Beg().Y(),l.Lab.End().Y()],color="red")
                    plt.annotate(r'MOD'+l.Number, xy=(l.Lab.End().X(), l.Lab.End().Y()), xycoords='data', xytext=(-5, +wysopi), textcoords='offset points', fontsize=8, color="red", arrowprops=dict(arrowstyle='-', connectionstyle="arc3,rad=0", color="red"))
                    for j in self.MODS3D:
                        if l.Number==j.MODnumber:
                            story=j
                    k=0
                    while story.FramesNumbers[k]!=nr and k<len(story.FramesNumbers):
                        k+=1
                    w=0
                    for q in range(0,k+1):
                        size=max(5,(l.Lab.End().X()-l.Lab.Beg().X())/4)
                        #plot(l.Lab.Beg().X()+((l.Lab.End().X()-l.Lab.Beg().X())/8), l.Lab.End().Y()+30+k+w, color=cm(story.PEDinFrames[q].SArea), marker='s', linestyle='dashed', linewidth=2, markersize=size)
                        #plot(l.Lab.End().X()-((l.Lab.End().X()-l.Lab.Beg().X())/8), l.Lab.End().Y()+30+k+w, color=cm(story.PEDinFrames[q].SShape), marker='s', linestyle='dashed', linewidth=2, markersize=size)
                        plot((l.Lab.Beg().X()+l.Lab.End().X())/2, l.Lab.End().Y()+40+k+w, color=cm(story.MODinFrames[q].SDist), marker='s', linestyle='dashed', linewidth=2, markersize=size)
                        w=w-1
                    wysopi+=10
                for r in i.Results:
                    plt.plot([r.Beg().X(),r.End().X()],[r.Beg().Y(),r.Beg().Y()],linestyle="-",color="blue")
                    plt.plot([r.Beg().X(),r.End().X()],[r.End().Y(),r.End().Y()],linestyle="-",color="blue")
                    plt.plot([r.Beg().X(),r.Beg().X()],[r.Beg().Y(),r.End().Y()],linestyle="--",color="aqua")
                    plt.plot([r.End().X(),r.End().X()],[r.Beg().Y(),r.End().Y()],linestyle="--",color="aqua")
                for r in i.FP:
                    #plt.plot([r.Beg().X(),r.End().X()],[r.Beg().Y(),r.Beg().Y()],linestyle="-",color="yellow")
                    #plt.plot([r.Beg().X(),r.End().X()],[r.End().Y(),r.End().Y()],linestyle="-",color="yellow")
                    plt.plot([r.Beg().X(),r.Beg().X()],[r.Beg().Y(),r.End().Y()],linestyle="--",color="yellow")
                    plt.plot([r.End().X(),r.End().X()],[r.Beg().Y(),r.End().Y()],linestyle="--",color="yellow")
                for fp3d in self.FP3D:
                    if i.Number in fp3d.FPFrames:
                        fp=fp3d.Diagonals[fp3d.FPFrames.index(i.Number)]
                        if (fp3d.Type=='-' and fp3d.Lenght>10):
                            plt.plot([fp.Beg().X(),fp.End().X()],[fp.Beg().Y(),fp.Beg().Y()],linestyle="-",color="yellow")
                            plt.plot([fp.Beg().X(),fp.End().X()],[fp.End().Y(),fp.End().Y()],linestyle="-",color="yellow")
                            plt.plot([fp.Beg().X(),fp.Beg().X()],[fp.Beg().Y(),fp.End().Y()],linestyle="-",color="yellow")
                            plt.plot([fp.End().X(),fp.End().X()],[fp.Beg().Y(),fp.End().Y()],linestyle="-",color="yellow")
                            
                        
                    
                img = imread(JPGfolder+'/'+'FrameId_'+str(nr)+'.jpg')
                plt.imshow(img,zorder=0,extent=[0,1280,0,971])
                plt.show()
                fig.savefig('C:/.../Results/Frames/'+str(nr)+'.png') # to save as png
                plt.close()





################################################### FRAME #####################################################





class Frame:
    Number=str
    Sdata=[]
    Ldata=[]
    Labels=[] #labels as [DIAGONAL,PEDnum,ObjTypeString] sorted from the smallest to the largest
    Results=[] 
    Mod=[]
    Detected=int
    FalsePositives=int
    FPresults=[]
    FP=[]
    
    def __init__(self,nr,sdata,ldata):
        self.Number=str(nr)
        self.Sdata=sdata
        self.Ldata=ldata
        self.Results=self.GetSysResults()
        self.Labels=self.GetLabels()
        try:
            self.Mod, self.FalsePositives, self.FPresults=self.MatchResults()
            self.Detected=self.GetDetected()
            self.FP=[e for e in self.FPresults]   #only when you need to draw FP
        except ZeroDivisionError:
            print((self.Number)+"ZeroDivisionError")

    def __eq__(self,other):
        if self.Number==other.Number:
            return True
        else:
            return False
        
        
    def GetSysResults(self):
        sysres=[]
        wrongform=0
        for i in self.Sdata.table.columns:
            if i.startswith('Obj_') and i.endswith('_ImagePosLeft'):
                Left=float(self.Sdata.table.loc[self.Sdata.table["Image_Number"] == int(self.Number), i].iloc[0])
                c1=i
            if i.startswith('Obj_') and i.endswith('_ImagePosRight'):
                Right=float(self.Sdata.table.loc[self.Sdata.table["Image_Number"] == int(self.Number), i].iloc[0])
                if Right==0:
                    Right+=1
                c2=i
            if i.startswith('Obj_') and i.endswith('_ImagePosTop'):
                Top=960-float(self.Sdata.table.loc[self.Sdata.table["Image_Number"] == int(self.Number), i].iloc[0])
                c3=i
            if i.startswith('Obj_') and i.endswith('_ImagePosBottom'):
                Bot=960-float(self.Sdata.table.loc[self.Sdata.table["Image_Number"] == int(self.Number), i].iloc[0])
                c4=i
                if c1.rstrip('Left')==c2.rstrip('Right') and c3.rstrip('Top')==c4.rstrip('Bottom') and c1.rstrip('Left')==c3.rstrip('Top'):
                    if Dot(Left,Bot)==Dot(Right,Top):
                        pass
                    else:
                        try:
                            if Left==1280:
                                Left=Left-1
                            sysres.append(Diagonal(Dot(Left,Bot),Dot(Right,Top)))
                        except WrongDiagonalForm:
                            print("System result has wrong diagonal form")
                            wrongform+=1
                            pass
        return sysres


    def GetLabels(self):
        lab=[]
        sortedlabs=[]
        if self.Number in self.Ldata.table.iloc[0:]['ImageNumber']:
            for i in self.Ldata.table.columns:
                #c1=c2=c3=c4=c5=''
                if i.startswith('Obj_') and i.endswith('_X1') and self.Ldata.table.loc[self.Number][i] != '':
                    Left=float(self.Ldata.table.loc[self.Number][i])
                    c1=i
                    if len(i)==8:
                        MODnum=str(i[4])
                    elif len(i)==9:
                        MODnum=str(i[4:6])
                    else:
                        MODnum=str(i[4:7])
                if i.startswith('Obj_') and i.endswith('_X2') and self.Ldata.table.loc[self.Number][i] != '':
                    Right=float(self.Ldata.table.loc[self.Number][i])
                    c2=i
                if i.startswith('Obj_') and i.endswith('_Y1') and self.Ldata.table.loc[self.Number][i] != '':
                    Top=960-float(self.Ldata.table.loc[self.Number][i])+8 #labels shifted (?)
                    c3=i
                if i.startswith('Obj_') and i.endswith('_Y2') and self.Ldata.table.loc[self.Number][i] != '':
                    Bot=960-float(self.Ldata.table.loc[self.Number][i])+8
                    c4=i
                    if c1.rstrip('1')==c2.rstrip('2') and c3.rstrip('1')==c4.rstrip('2') and c1.rstrip('X1')==c3.rstrip('Y1'):
                        
                        lab.append([Diagonal(Dot(Left,Bot),Dot(Right,Top)),MODnum,0,0,0,0,'No Data',0])
                    else:
                        print("Bounding box coordinates are in wrong form in csv with GT for "+i.rstrip('_Y2'))
                                                
            lab1=lab
            for i in range(0,len(lab)):
                best=lab1[0]
                for j in lab1:
                    if best[0].DiagonalLen()>=j[0].DiagonalLen():
                        best=j
                sortedlabs.append(best)
                lab1.remove(best)
            return sortedlabs
                
        else:
            raise Exception("Frame can not be found in paired csv with labelled frames")


#################################################### MATCHING ###########################################################

        
    def MatchResults(self):
        Rest=[e for e in self.Results]
        mod=[]
        for l in self.Labels:
            best=[]
            for s in Rest:
                if (l[0].SHarm(s)>=0.1 and l[0].DistanceSimilarity(s)>=0.2) or l[0].SHarm(s)>=0.3:
                    best.append(s)
            best1=[]
            for s in best:
                if l[0].BaseDistance(s)<=20 and l[0].DistanceSimilarity(s)>=0.1:
                    best1.append(s)
            if  len(best1)>=1:
                best2=best1[0]
                for s in best1:
                    if l[0].SHarm(s)>l[0].SHarm(best2):
                        best2=s
                mod.append(MOD(l,best2,self.Number))
                Rest.remove(best2)
            else:
                best3=[]
                for s in best:
                    if (l[0].AreaSimilarity(s)>=0.5 and l[0].DistanceSimilarity(s)>=0.1) or (l[0].ShapeSimilarity(s)>=0.5 and l[0].DistanceSimilarity(s)>=0.1):
                        best3.append(s)
                if len(best3)==0:
                    mod.append(MOD(l,"not detected",self.Number))
                elif len(best3)>=1:           
                    best4=best3[0]
                    for s in best3:
                        if l[0].SHarm(s)>l[0].SHarm(best4):
                            best4=s
                    mod.append(MOD(l,best4,self.Number))
                    Rest.remove(best4)
        falsepositve=len(Rest)
        Rest=[[e,self.Number] for e in Rest]
        return mod, falsepositve, Rest

    def LookForMOD(self,nr):
        present=False
        for i in self.Mod:
            if i.Number==str(nr):
                present=True
                found=i
                break
        if present:
            return found
        else:
            return 'not present'

    def GetDetected(self):
        det=0
        for i in self.Mod:
            if i.Detected:
                det+=1
        return det
            
                
class MOD:
    FrameNumber=str
    Lab=[]
    Number=str
    Detected=False
    #Type=str
    Result='not detected'
    SArea=float
    SShape=float
    SDist=float
    Sim=float
    BaseDif='not detected'
    OR=float
    SlowDownLED=int
    SlowDownWith=int
    BlinkenLED=int
    BlinkenWarn=int
    View=str
    MainLane=int

    def __init__(self,l,d,f):
        self.FrameNumber=f
        self.Lab=l[0]
        self.Number=l[1]
        self.SlowDownLED=l[2]
        self.SlowDownWith=l[3]
        self.BlinkenLED=l[4]
        self.BlinkenWarn=l[5]
        self.View=l[6]
        self.MainLane=l[7]
        if isinstance(d, str):
            self.SArea=0
            self.SShape=0
            self.SDist=0
            self.Sim=0
            self.OR=0
        else:
            self.Detected=True
            self.Result=d
            self.SArea=self.Lab.AreaSimilarity(self.Result)
            self.SShape=self.Lab.ShapeSimilarity(self.Result)
            self.SDist=self.Lab.DistanceSimilarity(self.Result)
            self.Sim=self.Lab.SHarm(self.Result)
            self.BaseDif=self.Lab.BaseDistance(self.Result)
            self.OR=self.Lab.Jaccard(self.Result)



            
####################################################################################################################
########################################## BOUNDING BOX FUNCTIONS ##################################################
####################################################################################################################

 
 
class Dot:
    def __init__(self,x,y):
        self.a=x
        self.b=y
    def X(self):
        return self.a
    def Y(self):
        return self.b
    def __eq__(self,other):
        if self.X()==other.X() and self.Y()==other.Y():
            return True
        else:
            return False

    def __lt__(self,other):
        if self.X()<other.X() and self.Y()<other.Y():
            return True
        else:
            return False

    def __gt__(self,other):
        if self.X()>other.X() and self.Y()>other.Y():
            return True
        else:
            return False

                                                #PAR - imortant parameters

class Diagonal:
    Qg=0.95  #PAR
    Qb=0.1  #PAR
    def __init__(self,b,e): # b point where diagonal starts, e point where diagonal ends
        if isinstance(b,Dot):
            self.p=b
        else:
            raise Exception("Diagonal's begining must be an point")
        if isinstance(e,Dot):
            self.k=e
            if (b.X()==e.X() and b.Y()==e.Y()):
                raise Exception("Diagonal can not starts and ends at the same point")
        else:
            raise Exception("Diagonal's ending must be an point")
        if b<e:
            pass
        else:
            raise WrongDiagonalForm("We need to consider diagonals that are directed at the top right corner")
    def __eq__(self,other):
        if self.Beg()==other.Beg() and self.End()==other.End():
            return True
        else:
            return False
    def Beg(self):
        return self.p
    def End(self):
        return self.k
    def ShowDiagonal(self):
        #print ("Diagonal form: [(%.1f,%.1f),(%.1f,%.1f)]" %(self.Beg().X(),self.Beg().Y(),self.End().X(),self.End().Y()))
        return "Diagonal[(%.1f,%.1f),(%.1f,%.1f)]" %(self.Beg().X(),self.Beg().Y(),self.End().X(),self.End().Y())
    def LineDir(self):
        return (self.Beg().Y()-self.End().Y())/(self.Beg().X()-self.End().X())
    def DiagonalLen(self):
        return math.sqrt((self.Beg().X()-self.End().X())**2+(self.Beg().Y()-self.End().Y())**2)
    
    def DiagonalMiddle(self):
        return Dot((self.Beg().X()+self.End().X())/2,(self.Beg().Y()+self.End().Y())/2)

    def BaseDistance(self,other):
        return math.fabs(self.Beg().Y()-other.Beg().Y())
    
    def MidBaseDistance(self, other):
        return math.sqrt((((self.Beg().X()+self.End().X())/2)-((other.Beg().X()+other.End().X())/2))**2+(self.Beg().Y()-other.Beg().Y())**2)

    def INTERSECTION_OF_WIDTH_BOXES(self,other):
        if (self.End().X()<other.End().X() and self.End().X()>other.Beg().X()) or (self.Beg().X()<other.End().X() and self.Beg().X()>other.Beg().X()) or (self.Beg().X()<=other.Beg().X() and self.End().X()>=other.End().X()):
            return min(self.End().X(),other.End().X())-max(self.Beg().X(),other.Beg().X())
        else:
            return 0
        
    def UNION_OF_WIDTH_BOXES(self,other):
        if (self.End().X()<other.End().X() and self.End().X()>other.Beg().X()) or (self.Beg().X()<other.End().X() and self.Beg().X()>other.Beg().X()) or (self.Beg().X()<=other.Beg().X() and self.End().X()>=other.End().X()):
            return max(self.End().X(),other.End().X())-min(self.Beg().X(),other.Beg().X())
        else:
            print(self.ShowDiagonal())
            print(other.ShowDiagonal())
                
    def JaccardWidth(self,other):
        return self.INTERSECTION_OF_WIDTH_BOXES(other)/self.UNION_OF_WIDTH_BOXES(other)

    def Jaccard(self, other):
        if ((self.End().Y()<other.End().Y() and self.End().Y()>other.Beg().Y()) or (self.Beg().Y()<other.End().Y() and self.Beg().Y()>other.Beg().Y()) or (self.Beg().Y()<=other.Beg().Y() and self.End().Y()>=other.End().Y())) and ((self.End().X()<other.End().X() and self.End().X()>other.Beg().X()) or (self.Beg().X()<other.End().X() and self.Beg().X()>other.Beg().X()) or (self.Beg().X()<=other.Beg().X() and self.End().X()>=other.End().X())):
            intersection=(min(self.End().Y(),other.End().Y())-max(self.Beg().Y(),other.Beg().Y()))*(min(self.End().X(),other.End().X())-max(self.Beg().X(),other.Beg().X()))
            union=(self.End().X()-self.Beg().X())*(self.End().Y()-self.Beg().Y())+(other.End().X()-other.Beg().X())*(other.End().Y()-other.Beg().Y())-intersection
            return intersection/union
        else:
            return 0

    def AdjDiagonalMiddle(self): #Adjusted diagonal middle for high objects
        b=self.End().Y()-self.Beg().Y()
        a=self.End().X()-self.Beg().X()
        if b>a:
            return Dot((self.Beg().X()+self.End().X())/2,(self.Beg().Y()+self.End().Y())/2 - (1/4)*b*(1/(1+math.exp(-4.5*(b/a-1.65)))))
        else:
            return Dot((self.Beg().X()+self.End().X())/2,(self.Beg().Y()+self.End().Y())/2)

    def AreaSimilarity(self,other):
        a1=(self.End().X()-self.Beg().X())*(self.End().Y()-self.Beg().Y())
        a2=(other.End().X()-other.Beg().X())*(other.End().Y()-other.Beg().Y())
        return min(a1,a2)/max(a1,a2)

    def ShapeSimilarity(self,other):
        p=17 #PAR
        return (numpy.sqrt(1/(((self.LineDir()-other.LineDir())/(1+self.LineDir()*other.LineDir()))**2+1)))**p #increase p to lower quality for little deviations

    def P1(self,other): #PARameter that describes the moment since quality falls below Qb (assuming that self is label)
        return (3/5)*self.DiagonalLen()+(1/16)*other.DiagonalLen()   

    def P2(self,other): #PARameter that describes the moment since quality rises over Qg (assuming that self is label)
        return (1/18)*self.DiagonalLen()

    def Beta(self,other):
        return math.log(math.log(self.Qb,self.Qg),self.P1(other)/self.P2(other))

    def Alpha(self,other):
        return ((-1)*math.log(self.Qb))/self.P1(other)**(self.Beta(other))

    def DistARG(self,other):  #Distance between two points (defoult is distance between centers of masses) used as argument in similarity measure based on distance
        return (math.sqrt((self.DiagonalMiddle().X()-other.DiagonalMiddle().X())**2+(self.DiagonalMiddle().Y()
                    -other.DiagonalMiddle().Y())**2) )
                #+(math.fabs(self.Beg().X()-other.Beg().X())+math.fabs(self.End().X()-other.End().X()))/2)

    def AdjDistARG(self,other):
        return (math.sqrt((self.AdjDiagonalMiddle().X()-other.AdjDiagonalMiddle().X())**2+(self.AdjDiagonalMiddle().Y()
                    -other.AdjDiagonalMiddle().Y())**2) )
                    #+(math.fabs(self.Beg().X()-other.Beg().X())+math.fabs(self.End().X()-other.End().X()))/2)

    def DistanceSimilarity(self,other):
        if self.Beta(other)<=1:
            print('Delta <=1')
        if other.End().Y()-other.Beg().Y()>self.End().Y()-self.Beg().Y():
            return max(math.exp((-1)*self.Alpha(other)*self.DistARG(other)**(self.Beta(other))),0.000000000000000000000000000001)
        else:
            return max(math.exp((-1)*self.Alpha(other)*self.AdjDistARG(other)**(self.Beta(other))),0.000000000000000000000000000001)
        
    def SAr(self,other):
        wA=7/7
        wS=3/7
        wD=11/7
        return (wA*self.AreaSimilarity(other)+wS*self.ShapeSimilarity(other)+wD*self.DistanceSimilarity(other))/3

    def SHarm(self,other):
        wA=8/7  #PAR
        wS=2/7  #PAR
        wD=11/7 #PAR
        return (wA+wS+wD)/(wA/self.AreaSimilarity(other)+wS/self.ShapeSimilarity(other)+wD/self.DistanceSimilarity(other))

    def SGeo(self,other):
        wA=7/7
        wS=3/7
        wD=11/7
        return math.exp((wA*math.log(self.AreaSimilarity(other))+wS*math.log(self.ShapeSimilarity(other))+wD*math.log(self.DistanceSimilarity(other)))/(wA+wS+wD))


############ FalsePositiveFunctions
    
    def IsFPSimilar(self,other):
        if self.FPDistanceSimilarity(other)>0.3 and self.AreaSimilarity(other)>=0.4 and self.ShapeSimilarity(other)>=0.6:
            return True
        else:
            if self.Beg().X()==0 and other.Beg().X()==0 and math.fabs(self.Beg().Y()-other.Beg().Y())<200:
                return True
            else:
                if self.End().X()==1280 and other.End().X()==1280 and math.fabs(self.End().Y()-other.End().Y())<200:
                    return True
                else:
                    return False

    def IsFPSimilar2(self,other): # for discontinuous fp
        if self.FPDistanceSimilarity(other)>0.1 and self.ShapeSimilarity(other)>=0.3:
            return True
        else:
            if self.Beg().X()==0 and other.Beg().X()==0 and math.fabs(self.Beg().Y()-other.Beg().Y())<200:
                return True
            else:
                if self.End().X()==1280 and other.End().X()==1280 and math.fabs(self.End().Y()-other.End().Y())<200:
                    return True
                else:
                    return False

    def IsFPSimilar3(self,other): #for post-labels
        if self.FPDistanceSimilarity3(other)>0.6 and self.AreaSimilarity(other)>=0.5 and self.ShapeSimilarity(other)>=0.6:
            return True
        else:
            if self.Beg().X()==0 and other.Beg().X()==0 and math.fabs(self.Beg().Y()-other.Beg().Y())<200:
                return True
            else:
                if self.End().X()==1280 and other.End().X()==1280 and math.fabs(self.End().Y()-other.End().Y())<200:
                    return True
                else:
                    return False

    def FPSHarm(self,other):
        wA=9/7  #PAR
        wS=2/7  #PAR
        wD=10/7 #PAR
        return (wA+wS+wD)/(wA/self.AreaSimilarity(other)+wS/self.ShapeSimilarity(other)+wD/self.FPDistanceSimilarity(other))

    def IsSimilarFPinTable(self,table):
        for i in table:
            if self.IsFPSimilar(i):
                return True
        return False

    def IsSimilarFPinTable2(self,table): # for discontinuous fp
        for i in table:
            if self.IsFPSimilar2(i):
                return True
        return False

    def IsSimilarFPinTable3(self,table): # for post-labels
        for i in table:
            if self.IsFPSimilar3(i[0]):
                return True
        return False

    def SimilarFPinTable(self,table):
        for i in table:
            if self.IsFPSimilar(i):
                return i
        return False
    
    def SimilarFPinTable2(self,table):
        for i in table:
            if self.IsFPSimilar2(i):
                return i
        return False

    def FPDistanceSimilarity(self,other):
        return max(math.exp((-1)*self.FPAlpha(other)*(math.sqrt((self.DiagonalMiddle().X()-other.DiagonalMiddle().X())**2+(self.DiagonalMiddle().Y()-other.DiagonalMiddle().Y())**2))**(self.FPBeta(other))),0.000000000000000000000000000001)

    def FPP1(self,other): #PARameter that describes the moment since quality falls below Qb (assuming that self is GT)
        return (1/2)*self.DiagonalLen()+(1/2)*other.DiagonalLen()

    def FPP2(self,other): #PARameter that describes the moment since quality rises over Qg (assuming that self is GT)
        return (1/3)*self.DiagonalLen()+(1/3)*other.DiagonalLen()

    def FPBeta(self,other):
        return math.log(math.log(self.Qb,self.Qg),self.FPP1(other)/self.FPP2(other)) 

    def FPAlpha(self,other):
        return ((-1)*math.log(self.Qb))/self.FPP1(other)**(self.FPBeta(other)) 

    ##### for post-labels

    def FPDistanceSimilarity3(self,other):
        return max(math.exp((-1)*self.FPAlpha3(other)*(math.sqrt((self.DiagonalMiddle().X()-other.DiagonalMiddle().X())**2+(self.DiagonalMiddle().Y()-other.DiagonalMiddle().Y())**2))**(self.FPBeta3(other))),0.000000000000000000000000000001)

    def FPP13(self,other): #PARameter that describes the moment since quality falls below Qb (assuming that self is GT)
        return (2/3)*self.DiagonalLen()+(1/16)*other.DiagonalLen()

    def FPP23(self,other): #PARameter that describes the moment since quality rises over Qg (assuming that self is GT)
        return (1/10)*self.DiagonalLen()

    def FPBeta3(self,other):
        return math.log(math.log(self.Qb,self.Qg),self.FPP13(other)/self.FPP23(other)) 

    def FPAlpha3(self,other):
        return ((-1)*math.log(self.Qb))/self.FPP13(other)**(self.FPBeta3(other)) 

    def LumDistanceSimilarity(self,other):
        labcenter, rescenter = self.MiddleOfLuminescence(other)
        if self.Beta(other)<=1:
            print("DELTA lower than 1 !!!")
        if self.Beg().Y()>=350 and self.End().Y()-self.Beg().Y()<=100:
            return max(math.exp((-1)*self.Alpha(other)*(math.sqrt((labcenter.X()-rescenter.X())**2+(labcenter.Y()-rescenter.Y())**2))**(self.Beta(other))),0.000000000000000000000000000001)
        else:
            return max(math.exp((-1)*self.Alpha(other)*((math.sqrt((labcenter.X()-rescenter.X())**2+(labcenter.Y()-rescenter.Y())**2)+math.fabs(self.Beg().Y()-other.Beg().Y()))/2)**(self.Beta(other))),0.000000000000000000000000000001)

    def MiddleOfLuminescence(self,other):
        picture = "C:/..."
        imag = Image.open(picture)
        # Convert the image te RGB if it is a .gif for example
        imag = imag.convert('RGB')
        label = np.asarray(imag.crop((self.Beg().X(),971-self.End().Y() ,self.End().X() ,971-self.Beg().Y())).convert('L'))
        print(label.size)
        result = np.asarray(imag.crop((other.Beg().X(),971-other.End().Y() ,other.End().X() ,971-other.Beg().Y())).convert('L'))
        labelcenter = absndimage.measurements.center_of_mass(label)
        print(labelcenter)
        resultcenter = ndimage.measurements.center_of_mass(result)
        labelcenter_onimage = Dot(self.End().X()-labelcenter[1], self.Beg().Y()+labelcenter[0])
        print(labelcenter_onimage.X(), labelcenter_onimage.Y())
        resultcenter_onimage = Dot(other.End().X()-resultcenter[1], other.Beg().Y()+resultcenter[0])
        return labelcenter_onimage, resultcenter_onimage

    
def progressBar(completed, total, bar_length=30):
    bar_length_unit_value = (total / bar_length)
    completed_bar_part = math.ceil(completed / bar_length_unit_value)
    progress = "#" * completed_bar_part
    remaining = "-" * (bar_length - completed_bar_part)
    percent_done = "%.f" % ((completed / total) * 100)
    result = '\r[{}{}] {}%'.format(progress, remaining, percent_done)
    sys.stdout.write(result)
    sys.stdout.flush()



def main():
    MODlocation = '.'  # location of csv GT and system output data
    MOD = MODinput(MODlocation)
    MOD.GetCSV()

if __name__ == "__main__":
    main()
