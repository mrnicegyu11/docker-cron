streamingURL = "rtmp://live.twitch.tv/app/live_57691527_7uNBylESUWlqVDgyfGAgEafdEI77Va"
#streamingURL = "rtmp://a.rtmp.youtube.com/live2/uc1v-57x4-31ud-521v-aa6c"
targetDirectory = "/djsets/"
iterFileName = "/var/tmp/" + "lastfile.dockerstreaming"
#targetDirectory = "./"
# via https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
import glob
import os
import datetime
import time
filenames = glob.glob(targetDirectory + "*.mp4")
listOfRawFiles = []
for filename in filenames:
    print("-")
    if "_" not in filename and "-" not in filename and " " not in filename:
        #curMD5 = md5(filename)
        #print(filename, curMD5)
        print("Processing: " + str(filename))
        date_time_obj = "ERROR"
        try:
            date_time_obj = datetime.datetime.strptime(filename.split("/")[-1][:-4], '%d%b%Y')
        except:
            print("Could not determine datetime from file named: " + str(filename.split("/")[-1][:-4]))
            print("Aborting.")
            exit(-1)
        listOfRawFiles.append([filename, date_time_obj.timestamp()])
#
print("-------\ List of Files: \n")
print(listOfRawFiles)
print("---")
#
#
# via https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
# Python code to sort the tuples using second element  
# of sublist Function to sort using sorted() 
def Sort(sub_li): 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: x[1]))
#
#
#
listOfRawFiles = Sort(listOfRawFiles)
from pathlib import Path
lastIter = 0
my_file = Path(iterFileName)
if my_file.is_file():
    with open(my_file, "r+") as inStream:
        lines = inStream.readlines()
        try:
            lastIter = int(lines[0])
        except:
            print("Critical Error")
            exit(-1)
def stream(filename_in,streamingURL_in,datetime_in):
    # Append _streaming
    cmdString = ""
    if True:
        cmdString += "cd /home; rm bannerfull.png; rm banner1.png; rm banner2.png;"
        datestring = datetime.datetime.fromtimestamp(datetime_in).strftime("%b%d %Y")
        text1 = "Recording from " + datestring
        text2 = "Streaming live every monday 5:30pm berlin time"
        cmdString += "convert -size 1200x85 xc:transparent -font Bookman-DemiItalic -pointsize 40 -channel RGBA -blur 0x6 -fill darkred -stroke magenta -draw \"text 20,55 '" + text1 + "'\" banner1.png && convert -size 1200x85 xc:transparent -font Bookman-DemiItalic -pointsize 40 -channel RGBA -blur 0x6 -fill darkred -stroke magenta -draw \"text 20,55 '" + text2 + "'\" banner2.png && convert banner1.png banner2.png -append bannerfull.png; "
    cmdString += "/usr/local/bin/ffmpeg -re -i " + filename_in + " -i bannerfull.png -filter_complex \"[0:v][1:v] overlay=25:25\" -ac 2 -ar 44100 -acodec aac -vcodec libx264 -pix_fmt yuv420p -profile:v main -preset \"ultrafast\" -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 2500k -maxrate 2500k -bufsize 2500k -f flv " + streamingURL_in
    print("Executing >>" + cmdString + "<<")
    time.sleep(1)
    os.system(cmdString)
    return
print("Streaming now file: " + str(listOfRawFiles[lastIter][0]) + " with index " + str(lastIter))
stream(listOfRawFiles[lastIter][0],streamingURL,listOfRawFiles[lastIter][1])
#
if lastIter == len(listOfRawFiles) - 1:
    lastIter = 0
with open(iterFileName, 'w') as cal: # file would be created if not exists
    try:
        cal.write(str(lastIter + 1) + "\n")
    except:
        print("ERROR")
        exit(-1)




# if today is not monday
# for file in /djsets/
# if mp4
# create list, sort by md5hash
# Check if lastfile.dockerstreaming exists
# if not create and write down iterator
# if yes, get iterator
# check if streaming format exists
# if not, convert to streaming format
# if yes, stream to target link (ENV VAR?)
# 
# afterwards, convert next weeks video