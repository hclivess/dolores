from datetime import date
import datetime
import glob
import os
import re
import feedparser
import ssl
import time
import subprocess
import textwrap
dirpath = os.path.dirname(os.path.abspath(__file__))

datenow=str(datetime.datetime.now())[:16]
timenow = str(time.time())
today = date.today()
print timenow
print today
print datenow

newspath = dirpath+"\\output\\"+timenow+".txt"
imgpath = dirpath+"\\output\\"+timenow+".png"
mp3path = dirpath+"\\output\\"+timenow+".mp3"
mp4path = dirpath+"\\output\\"+timenow+".mov"
voice = "\"IVONA 2 Salli\""

rss = "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&output=rss"

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
feed = feedparser.parse(rss) #<<WORKS!!

#print[field for field in feed]

#import pprint
#pprint.pprint(entry for entry in feed['entries'])
titles = [entry.title for entry in feed['entries']]

news = ""
news_balabolka = ""
noduplicates = 0
for title in titles:

    
    #title = re.sub("(.{10})", '\\1\n', title, 0, re.DOTALL)
    #print title
    title = title.encode("utf-8")
    title_nosource=re.sub("\s\-\s.*","",title)
    ###title_nosource = r"\n".join(textwrap.wrap(title_nosource, 85))
    
    title_source=re.sub(".*\s\-\s","",title)
    
    isduplicate = 0
    filenames = glob.glob("output/*.txt")
    print filenames
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                if title_nosource[:85] in line[:85]:
                    isduplicate = 1                    
   
    if isduplicate == 0:
        print "no duplicate"
        noduplicates =+ 1

        news = news+(title_source.upper()+": "+r"\n".join(textwrap.wrap(title_nosource, 85))+r"\n"r"\n")
        #news_balabolka = news_balabolka+(title_source+" reports: "+title_nosource+". ")
        news_balabolka = news_balabolka+(title_nosource+". ")
    else:
        print "duplicate"
    
#print news


if noduplicates > 0:

    #pointsize = 15000/len(news)
    pointsize = 28
    print pointsize

    f = open(newspath, 'wb+')
    f.write(news)
    f.close()

    #subprocess.check_output(["magick", "-background", "transparent", "-gravity","center", "-fill","white", "-font","Verdana", "-size","1820x980", "-density", "120", "-strokewidth", "10", "-stroke", "black", "label:"+news, "-bordercolor", "transparent", "-border", "50x50", imgpath],shell=True)    
    subprocess.check_output(["magick","-pointsize", str(pointsize), "-fill", "white", "-background", "transparent", "-font", "Arial", "-size","1820x980", "-strokewidth", "1", "-stroke", "white", "label: News for "+datenow+r"\n"r"\n"+news,"-bordercolor", "transparent", "-border", "50x50", imgpath],shell=True)
    subprocess.call(["magick", "composite", imgpath, "background.jpg", imgpath])
    
    f = open('test.cmd', 'w+')
    f.write(""+dirpath+"\\balcon.exe -s 0 -sb 500 -se 500 -n "+voice+" -t \""+news_balabolka+"\" -w "+mp3path+"")
    #f.write(""+dirpath+"\\balcon.exe -n "+voice+" -fr 48 -t "+line+" -o --raw | "+dirpath+"\\lame.exe -r -s 48 -m m -h - "+dirpath+"\\mp3path")
    f.close()



    os.system("runas /savecred /profile /user:Honza "+dirpath+"\\test.cmd")
    time.sleep(10)
    os.system("lame.exe -V2 wavpath mp3path")
    time.sleep(10)
    subprocess.check_output(["ffmpeg.exe", "-y","-loop", "1", "-i", imgpath, "-i", mp3path, "-c:v", "libx264", "-c:a", "copy", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-shortest", mp4path], shell=True)
    
    subprocess.call(dirpath+"\\output\\upload.py", shell=True)

os.remove(mp3path)
os.remove(imgpath)
print "Media processing done."
