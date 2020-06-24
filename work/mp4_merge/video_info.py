#-*- coding: utf8 -*-
import os,re,json,sys

def getJsonString(strFileName):
    strCmd =  'ffprobe -v quiet -print_format json -show_format -show_streams -i "' +  strFileName  + '"'
    mystring = os.popen(strCmd).read()
    return  mystring


def getVideoInfo(strFileName):
    # UnicodeDecodeError: 'utf8' codec can't decode byte 0xc0 in position 57: invalid start byte
    filecontent = getJsonString(strFileName)
    try:
        js = json.loads(filecontent)
    except Exception,e:
        print Exception,":",e, strFileName
    iVideoWidth = 0
    iVideoHeight = 0
    iVideoBitRate = 0
    iAllBitRate = 0
    strCodecName = ''
    iVideoDuration = 0
    arrStreams = js['streams']

    for stream in arrStreams:
        if(stream['codec_type'] == 'video'):
            strCodecName = stream['codec_name']
            iVideoWidth = int(stream['width'])
            iVideoHeight = int(stream['height'])
            iVideoDuration = float(stream['duration'])
            # h264 可能没有这一项
            if  'bit_rate'  in stream.keys() :
                iVideoBitRate = int (stream['bit_rate'])
            break
    iAllBitRate = int(js['format']['bit_rate'])
    iVideoSize = int(js['format']['size'])
    return {'width': iVideoWidth, 'height': iVideoHeight, 'size': iVideoSize,  'duration': iVideoDuration}

if __name__ == '__main__':
    print getVideoInfo(sys.argv[1])
