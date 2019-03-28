import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
import Bitrate

#calculation of PSNR-YUV
def psnr():
    df=pd.read_csv(string_value1,sep=' ',header=None)
    num=df.shape[0]
    n=1
    psnr_avg=0
    while n<=num:
        stringY=df.iloc[n-1,6]
        stringU=df.iloc[n-1,6]
        stringV=df.iloc[n-1,6]
        psnr_avg=psnr_avg+(float(stringY[7:])*6+float(stringU[7:])+float(stringV[7:]))/8
        n=n+1
    psnr_total_avg=psnr_avg/num
    return(psnr_total_avg)

#plotting
def graph(x1,x2,x3,y1,y2,y3):
    
    plt.title('Result Analysis')
    plt.plot(x1, y1, color='green', label='X264')
    plt.plot(x2, y2, color='red', label='HEVC')
    plt.plot(x3, y3,  color='skyblue', label='VP9')
    plt.legend() 
     
    plt.xlabel('bitrate(Kbps)')
    plt.ylabel('PSNR-YUV(dB)')
    plt.savefig("BitrateSaving.png")

#X264 test
videoname=input("Please enter the video file name you want to test.->")
resolution=input("Please enter the video resolution with a format like 'x*y'->")
filename=videoname+"_X264.csv"  
foldername1=videoname+"_X264_finalresult"
foldername2=videoname+"_X264_data"
foldername3=videoname+"_file"
os.system("mkdir %s"%(foldername1))
os.system("mkdir %s"%(foldername2)) 
os.system("mkdir %s"%(foldername3))
X264_qp=["22","27","32","37"]
with open(filename,"a+") as csvfile:
    writer = csv.writer(csvfile)                             
    writer.writerows([["quantization parameter","psnr_average","bitrate (kbps)"]])
i=0
while i<=3:
    string_name=str(X264_qp[i])
    string_value1=videoname+'_psnr_X264_qp'+string_name
    string_value2='encoded_X264_qp'+string_name+'.mp4'
    os.system("./ffmpeg -i %s -c:v libx264 -preset placebo -tune psnr -subq 8 -bf 0 -g 9999 -keyint_min 9999 -refs 4 -trellis 2 -b_strategy 2 -me_range 24 -qp %s %s" %(videoname,string_name,string_value2))
    os.system("./ffmpeg -i %s testdec.yuv"%(string_value2))
    os.system("./ffmpeg -i %s origindec.yuv"%(videoname))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi psnr=%s -f null -"%(resolution,resolution,string_value1))
    os.system("./ffmpeg -i %s 2>&1 | grep 'bitrate' | cut -d ' ' -f 8| tee bitrate.csv"%(string_value2))
    os.system("rm testdec.yuv origindec.yuv")
    doc=pd.read_csv('bitrate.csv',sep=' ',header=None)
    bitrate=doc.iloc[0,0]
    os.system("rm bitrate.csv")
    psnr_total_avg=psnr()
    with open(filename,"a+") as csvfile: 
        writer = csv.writer(csvfile)                             
        writer.writerows([[X264_qp[i],psnr_total_avg,bitrate]])
    i=i+1
    #collect the data
    os.system("mv %s %s"%(string_value1,foldername2))
    os.system("mv %s %s"%(string_value2,foldername2))
R1= pd.read_csv(filename, sep = ',')["bitrate (kbps)"].values
PSNR1= pd.read_csv(filename, sep = ',')["psnr_average"].values
os.system("mv %s %s"%(filename,foldername1))
os.system("mv %s %s"%(foldername1,foldername2))
os.system("mv %s %s"%(foldername2,foldername3))

#X265 test
filename=videoname+"_X265.csv"  
foldername1=videoname+"_X265_finalresult"
foldername2=videoname+"_X265_data"
os.system("mkdir %s"%(foldername1))
os.system("mkdir %s"%(foldername2)) 
X265_qp=["22","27","32","37"]
i=0
with open(filename,"a+") as csvfile:
    writer = csv.writer(csvfile)                             
    writer.writerows([["quantization parameter","psnr_average","bitrate (kbps)"]])
while i<=3:
    string_name=str(X265_qp[i])
    string_value1=videoname+'_psnr_X265_qp'+string_name
    string_value2='encoded_X265_qp'+string_name+'.mp4'
    os.system("./ffmpeg -i %s -c:v libx265 -profile main -preset placebo -tune psnr -x265-params rd=6:qp=%s:keyint=9999:min_keyint=9999 %s" %(videoname,string_name,string_value2))
    os.system("./ffmpeg -i %s testdec.yuv"%(string_value2))
    os.system("./ffmpeg -i %s origindec.yuv"%(videoname))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi psnr=%s -f null -"%(resolution,resolution,string_value1))
    os.system("./ffmpeg -i %s 2>&1 | grep 'bitrate' | cut -d ' ' -f 8| tee bitrate.csv"%(string_value2))
    os.system("rm testdec.yuv origindec.yuv")
    doc=pd.read_csv('bitrate.csv',sep=' ',header=None)
    bitrate=doc.iloc[0,0]
    os.system("rm bitrate.csv")
    psnr_total_avg=psnr()
    with open(filename,"a+") as csvfile: 
        writer = csv.writer(csvfile)                             
        writer.writerows([[X265_qp[i],psnr_total_avg,bitrate]])
    i=i+1
    #collect the data
    os.system("mv %s %s"%(string_value1,foldername2))
    os.system("mv %s %s"%(string_value2,foldername2))
R2= pd.read_csv(filename, sep = ',')["bitrate (kbps)"].values
PSNR2= pd.read_csv(filename, sep = ',')["psnr_average"].values
os.system("mv %s %s"%(filename,foldername1))
os.system("mv %s %s"%(foldername1,foldername2))
os.system("mv %s %s"%(foldername2,foldername3))

#VP9 test
filename=videoname+"_VP9.csv"  
foldername1=videoname+"_VP9_finalresult"
foldername2=videoname+"_VP9_data"
os.system("mkdir %s"%(foldername1))
os.system("mkdir %s"%(foldername2)) 
VP9_qp=["22","27","32","37"]
with open(filename,"a+") as csvfile:
    writer = csv.writer(csvfile)                             
    writer.writerows([["quantization parameter","psnr_average","bitrate (kbps)"]])
i=0
while i<=3:
    string_name=str(VP9_qp[i])
    string_value1=videoname+'_psnr_VP9_qp'+string_name
    string_value2='encoded_VP9_qp'+string_name+'.webm'
    os.system("./ffmpeg -i %s -c:v libvpx-vp9 -quality good -speed 0 -g 9999 -tune psnr -qmin %s -qmax %s %s" %(videoname,string_name,string_name,string_value2))
    os.system("./ffmpeg -i %s testdec.yuv"%(string_value2))
    os.system("./ffmpeg -i %s origindec.yuv"%(videoname))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi psnr=%s -f null -"%(resolution,resolution,string_value1))
    os.system("./ffmpeg -i %s 2>&1 | grep 'bitrate' | cut -d ' ' -f 8| tee bitrate.csv"%(string_value2))
    os.system("rm testdec.yuv origindec.yuv")
    doc=pd.read_csv('bitrate.csv',sep=' ',header=None)
    bitrate=doc.iloc[0,0]
    os.system("rm bitrate.csv")
    psnr_total_avg=psnr()
    with open(filename,"a+") as csvfile: 
        writer = csv.writer(csvfile)                             
        writer.writerows([[VP9_qp[i],psnr_total_avg,bitrate]])
    i=i+1
    #collect the data
    os.system("mv %s %s"%(string_value1,foldername2))
    os.system("mv %s %s"%(string_value2,foldername2))
R3= pd.read_csv(filename, sep = ',')["bitrate (kbps)"].values
PSNR3= pd.read_csv(filename, sep = ',')["psnr_average"].values
graph(R1,R2,R3,PSNR1,PSNR2,PSNR3)
string_value3="BitrateSaving.png"
os.system("mv %s %s"%(filename,foldername1))
os.system("mv %s %s"%(foldername1,foldername2))
os.system("mv %s %s"%(string_value3,foldername3))
os.system("mv %s %s"%(foldername2,foldername3))

rate1=Bitrate.BD_RATE(R1, PSNR1, R2, PSNR2, piecewise=0)
rate2=Bitrate.BD_RATE(R2, PSNR2, R1, PSNR1, piecewise=0)
rate3=Bitrate.BD_RATE(R3, PSNR3, R2, PSNR2, piecewise=0)
rate4=Bitrate.BD_RATE(R2, PSNR2, R3, PSNR3, piecewise=0)
rate5=Bitrate.BD_RATE(R1, PSNR1, R3, PSNR3, piecewise=0)
rate6=Bitrate.BD_RATE(R3, PSNR3, R1, PSNR1, piecewise=0)

filename1=videoname+"_BitrateSaving.csv" 
with open(filename1,"a+") as csvfile:
    writer = csv.writer(csvfile)                             
    writer.writerows([["","X265 vs X264","X264 vs X265","X265 vs VP9","VP9 vs X265","VP9 vs X264","X264 vs VP9"]])
    writer.writerows([["BD Rate",rate1,rate2,rate3,rate4,rate5,rate6]])


os.system("mv %s %s"%(filename1,foldername3))
