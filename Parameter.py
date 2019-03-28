import os
import pandas as pd
import csv
import matplotlib.pyplot as plt

# calculation of average PSNR
def psnr():
    df=pd.read_csv(string_value1,sep=' ',header=None)
    num=df.shape[0]
    n=1
    psnr_avg=0
    while n<=num:
        string=df.iloc[n-1,5]
        psnr_avg=psnr_avg+float(string[9:])
        n=n+1
    psnr_total_avg=psnr_avg/num
    return(psnr_total_avg)
#calculation of SSIM   
def ssim():
    df=pd.read_csv(string_value2,sep=' ',header=None)
    num=df.shape[0]
    n=1
    ssim_avg=0
    while n<=num:
        string=df.iloc[n-1,4]
        ssim_avg=ssim_avg+float(string[4:])
        n=n+1
    ssim_total_avg=ssim_avg/num
    return(ssim_total_avg)
# obtain VMAF scores
def vmaf():
    df=pd.read_csv('vmaf.csv',sep=' ',header=None)
    string=df.iloc[2,3]
    vmaf_value=float(string)
    return(vmaf_value)
# encoding and decoding implementation
def measure(form):
    os.system("./ffmpeg -i %s testdec.yuv"%(form))
    os.system("./ffmpeg -i %s origindec.yuv"%(videoname))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi psnr=%s -f null -"%(resolution,resolution,string_value1))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi ssim=%s -f null -"%(resolution,resolution,string_value2))
    os.system("./ffmpeg -s %s -i testdec.yuv -s %s -i origindec.yuv -lavfi libvmaf='model_path=./model/vmaf_v0.6.1.pkl:psnr=1:log_fmt=json' -f null - | tee vmaf.csv"%(resolution,resolution))
    os.system("rm %s testdec.yuv origindec.yuv"%(form))
#write data into csv file    
def write(para):
    with open(filename,"a+") as csvfile: 
        writer = csv.writer(csvfile)                             
        writer.writerows([[para,psnr_total_avg,ssim_total_avg,vmaf_value]])
#collect data
def fold():
    os.system("rm vmaf.csv")
    os.system("mv %s %s"%(string_value1,foldername2))
    os.system("mv %s %s"%(string_value2,foldername2))
#name the file and folders   
def name(para,codec):
    filename=videoname+"_"+str(para)+".csv"
    foldername1=videoname+"_"+codec+"_"+str(para)+"_finalresult"
    foldername2=videoname+"_"+codec+"_"+str(para)+"_data"
    os.system("mkdir %s %s"%(foldername1,foldername2))
    return(filename,foldername1,foldername2)
#plotting
def graph(column1,column2,column3,column4,name):
    x= pd.read_csv(filename, sep = ',')[column1].values
    y= pd.read_csv(filename, sep = ',')[column2].values
    z= pd.read_csv(filename, sep = ',')[column3].values
    w= pd.read_csv(filename, sep = ',')[column4].values

    fig = plt.figure()
    ax1=fig.add_subplot(311)
    plt.plot(x,y,'b')
    ax2=fig.add_subplot(312)
    plt.plot(x,z,'y')
    ax3=fig.add_subplot(313)
    plt.plot(x,w,'r')  
    ax1.set_xlabel(column1)
    ax2.set_xlabel(column1)
    ax3.set_xlabel(column1)
    ax1.set_ylabel(column2)
    ax2.set_ylabel(column3)
    ax3.set_ylabel(column4)
    plt.savefig(name+".png")    
    
while True:
    print (""" 
    1.X264
    2.X265
    3.VP9
    4.Exit/Quit
        """)

    respon=input("What codec would you like to test? ->") 
    if respon=="1":
        while True:
            videoname=input("Please enter the video file name you want to test. ->")
            if os.path.isfile(videoname):
                resolution=input("Please enter the video resolution with a format like 'x*y' ->")
                break
            else:
                print("File Doesn't Exist, Please Try Again.")
                continue
        while True:
          print ("""
                 1. CRF value
                 2. 2 Pass bitrate
                 3. CBR bitrate
                 4. Quantization Parameter
                 5. Back to main menu""")
          respon1=input("What parameter would you like to test? ->")
          if respon1=="1":
              X264_crf=3
              (filename,foldername1,foldername2)=name("crf","X264")
              os.system("mkdir %s %s"%(foldername1,foldername2))          
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["crf_value","psnr_average","ssim_average","vmaf_value"]])
              while X264_crf<=51:
                  string_name=str(X264_crf)
                  string_value1='psnr_crf_'+string_name
                  string_value2='ssim_crf_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx264 -crf %s test.mp4" %(videoname,X264_crf))
                  measure("test.mp4")                  
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X264_crf)
                  X264_crf=X264_crf+3
                  fold()
              graph("crf_value","psnr_average","ssim_average","vmaf_value","X264_crf")
              string_value3="X264_crf.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))

          elif respon1=="2":
              X264_bitrate1=1
              (filename,foldername1,foldername2)=name("2pass_bitrate","X264")
              os.system("mkdir %s %s"%(foldername1,foldername2))           
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(Mbps)","psnr_average","ssim_average","vmaf_value"]])
              while X264_bitrate1<=10:
                  string_name=str(X264_bitrate1)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system(" ./ffmpeg -y -i %s -c:v libx264 -b:v %s -pass 1  -an -f mp4 /dev/null &&\
                  ./ffmpeg -i %s -c:v libx264 -b:v %s -pass 2 test.mp4" %(videoname,string_name,videoname,string_name))
                  measure("test.mp4")       
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X264_bitrate1)
                  X264_bitrate1=X264_bitrate1+1
                  fold()
              graph("bitrate(Mbps)","psnr_average","ssim_average","vmaf_value","X264_2pass_bitrate")
              string_value3="X264_2pass_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="3":
              X264_bitrate=1
              (filename,foldername1,foldername2)=name("bitrate","X264")
              os.system("mkdir %s %s"%(foldername1,foldername2))           
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(Mbps)","psnr_average","ssim_average","vmaf_value"]])
              while X264_bitrate<=10:
                  string_name=str(X264_bitrate)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx264 -b:v %s -minrate %s -maxrate %s -bufsize 2M test.mp4" %(videoname,string_name,string_name,string_name))
                  measure("test.mp4")       
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X264_bitrate)
                  X264_bitrate=X264_bitrate+1
                  fold()
              graph("bitrate(Mbps)","psnr_average","ssim_average","vmaf_value","X264_CBR_bitrate")
              string_value3="X264_CBR_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))

          elif respon1=="4":
              X264_qp=3
              (filename,foldername1,foldername2)=name("qp","X264")
              os.system("mkdir %s %s"%(foldername1,foldername2)) 
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["qp_value","psnr_average","ssim_average","vmaf_value"]])
              while X264_qp<=51:
                  string_name=str(X264_qp)
                  string_value1='psnr_qp_'+string_name
                  string_value2='ssim_qp_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx264 -qp %s  test.mp4" %(videoname,X264_qp))
                  measure("test.mp4")            
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X264_qp)
                  X264_qp=X264_qp+3
                  fold()
              graph("qp_value","psnr_average","ssim_average","vmaf_value","X264_qp_value")  
              string_value3="X264_qp_value.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="5":
              break
    elif respon=="2":
        while True:
            videoname=input("Please enter the video file name you want to test. ->")
            if os.path.isfile(videoname):
                resolution=input("Please enter the video resolution with a format like 'x*y' ->")
                break
            else:
                print("File Doesn't Exist, Please Try Again.")
                continue
        while True:
          print ("""
                 1. CRF value
                 2. 2 Pass bitrate
                 3. CBR bitrate
                 4. Quantization Parameter
                 5. Back to main menu""")
          respon1=input("What parameter would you like to test? ->")
          if respon1=="1":
              X265_crf=3
              (filename,foldername1,foldername2)=name("crf","X265")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["crf_value","psnr_average","ssim_average","vmaf_value"]])
              while X265_crf<=51:
                  string_name=str(X265_crf)
                  string_value1='psnr_crf_'+string_name
                  string_value2='ssim_crf_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx265 -crf %s test.mp4" %(videoname,X265_crf))
                  measure("test.mp4")               
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X265_crf)
                  X265_crf=X265_crf+3
                  fold()
              graph("crf_value","psnr_average","ssim_average","vmaf_value","X265_crf") 
              string_value3="X265_crf.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="2":
              X265_bitrate1=1
              (filename,foldername1,foldername2)=name("2pass_bitrate","X265")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(Mbps)","psnr_average","ssim_average","vmaf_value"]])
              while X265_bitrate1<=10:
                  string_name=str(X265_bitrate1)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system("./ffmpeg -y -i %s -c:v libx265 -b:v %s -x265-params pass=1 -an -f mp4 /dev/null && \
                             ./ffmpeg -i %s -c:v libx265 -b:v %s -x265-params pass=2  test.mp4" %(videoname,string_name,videoname,string_name))
                  measure("test.mp4")             
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write( X265_bitrate1)
                  X265_bitrate1=X265_bitrate1+1
                  fold()
              graph("bitrate(Mbps)","psnr_average","ssim_average","vmaf_value","X265_2pass_bitrate")
              string_value3="X265_2pass_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="3":
              X265_bitrate=1
              (filename,foldername1,foldername2)=name("bitrate","X265")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(Mbps)","psnr_average","ssim_average","vmaf_value"]])
              while X265_bitrate<=10:
                  string_name=str(X265_bitrate)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx265 -b:v %s -minrate %s -maxrate %s -bufsize 2M test.mp4" %(videoname,string_name,string_name,string_name))
                  measure("test.mp4")             
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X265_bitrate)
                  X265_bitrate=X265_bitrate+1
                  fold()
              graph("bitrate(Mbps)","psnr_average","ssim_average","vmaf_value","X265_CBR_bitrate")
              string_value3="X265_CBR_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="4":
              X265_qp=3
              (filename,foldername1,foldername2)=name("qp","X265")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["qp_value","psnr_average","ssim_average","vmaf_value"]])
              while X265_qp<=51:
                  string_name=str(X265_qp)
                  string_value1='psnr_qp_'+string_name
                  string_value2='ssim_qp_'+string_name
                  os.system("./ffmpeg -i %s -c:v libx265 -x265-params qp=%s  test.mp4" %(videoname,X265_qp))
                  measure("test.mp4")             
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(X265_qp)
                  X265_qp=X265_qp+3
                  fold()
              graph("qp_value","psnr_average","ssim_average","vmaf_value","X265_qp_value")  
              string_value3="X265_qp_value.png"
              os.system("mv %s %s"%(filename,foldername1))   
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="5":
              break
    elif respon=="3":
        while True:
            videoname=input("Please enter the video file name you want to test. ->")
            if os.path.isfile(videoname):
                resolution=input("Please enter the video resolution with a format like 'x*y' ->")
                break
            else:
                print("File Doesn't Exist, Please Try Again.")
                continue
        while True:
          print ("""
                 1. Crf Value
                 2. 2 Pass bitrate
                 3. Single Pass Bitrate
                 4. Speed
                 5. Back to Main Menu""")
          respon1=input("What parameter would you like to test? ->")
          if respon1=="1":
              VP9_crf=3
              (filename,foldername1,foldername2)=name("crf","VP9")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["crf_value","psnr_average","ssim_average","vmaf_value"]])
              while VP9_crf<=63:
                  string_name=str(VP9_crf)
                  string_value1='psnr_crf_'+string_name
                  string_value2='ssim_crf_'+string_name
                  os.system("./ffmpeg -i %s -c:v libvpx-vp9 -crf %s -b:v 0 test.webm" %(videoname,VP9_crf))
                  measure("test.webm")               
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(VP9_crf)
                  VP9_crf=VP9_crf+3
                  fold()
              graph("crf_value","psnr_average","ssim_average","vmaf_value","VP9_crf") 
              string_value3="VP9_crf.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
          elif respon1=="2":
              VP9_bitrate1=1
              (filename,foldername1,foldername2)=name("2pass_bitrate","VP9")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(kbps)","psnr_average","ssim_average","vmaf_value"]])
              while VP9_bitrate1<=10:
                  string_name=str(VP9_bitrate1)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system("./ffmpeg -y -i %s -c:v libvpx-vp9 -b:v %s -pass 1 -an -f webm /dev/null && \
                             ./ffmpeg -i %s -c:v libvpx-vp9 -b:v %s -pass 2  test.webm" %(videoname,string_name,videoname,string_name))
                  measure("test.webm")         
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(VP9_bitrate1)
                  VP9_bitrate1=VP9_bitrate1+1
                  fold()
              graph("bitrate(kbps)","psnr_average","ssim_average","vmaf_value","VP9_2pass_bitrate")
              string_value3="VP9_2pass_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))              
          elif respon1=="3":
              VP9_bitrate=1
              (filename,foldername1,foldername2)=name("bitrate","VP9")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["bitrate(kbps)","psnr_average","ssim_average","vmaf_value"]])
              while VP9_bitrate<=10:
                  string_name=str(VP9_bitrate)+'M'
                  string_value1='psnr_bitrate_'+string_name
                  string_value2='ssim_bitrate_'+string_name
                  os.system("./ffmpeg -i %s -c:v libvpx-vp9 -b:v %s -crf 30 test.webm" %(videoname,string_name))
                  measure("test.webm")         
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(VP9_bitrate)
                  VP9_bitrate=VP9_bitrate+1
                  fold()
              graph("bitrate(kbps)","psnr_average","ssim_average","vmaf_value","VP9_CBR_bitrate")
              string_value3="VP9_CBR_bitrate.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="4":
              VP9_speed=0
              (filename,foldername1,foldername2)=name("speed","VP9")
              os.system("mkdir %s %s"%(foldername1,foldername2))
              with open(filename,"a+") as csvfile:
                  writer = csv.writer(csvfile)                             
                  writer.writerows([["speed","psnr_average","ssim_average","vmaf_value"]])
              while VP9_speed<=4:
                  string_name=str(VP9_speed)
                  string_value1='psnr_speed_'+string_name
                  string_value2='ssim_speed_'+string_name
                  os.system("./ffmpeg -i %s -c:v vp9  -b:v 2000k \
                   -minrate 1500k -maxrate 2500k -quality good -speed %s  -c:a libvorbis \
                    test.webm" %(videoname,string_name))
                  measure("test.webm")               
                  psnr_total_avg=psnr()
                  ssim_total_avg=ssim()
                  vmaf_value=vmaf()
                  write(VP9_speed)
                  VP9_speed=VP9_speed+1
                  fold()
              graph("speed","psnr_average","ssim_average","vmaf_value","VP9_speed")  
              string_value3="VP9_speed.png"
              os.system("mv %s %s"%(filename,foldername1))
              os.system("mv %s %s"%(string_value3,foldername1))
              os.system("mv %s %s"%(foldername1,foldername2))
              
          elif respon1=="5":
              break
    elif respon=="4":
      print("\n Goodbye") 
      break
    elif respon !="":
      print("\n Not Valid Choice Try again") 


