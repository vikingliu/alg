#coding=utf-8
import os
import video_info
import sys

def merge_mp4(files, out):
    tss = '|'.join(files)
    merge_cmd = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (tss, out)
    rm(out)
    os.popen(merge_cmd).read()


def resize_mp4(i, out, width, height):
    resize_cmd = 'ffmpeg -i %s -vf scale=%dx%d,setdar=%d:%d %s' % (i, width, height, width, height, out)
    if  os.path.exists(out):
        os.remove(out)
    os.popen(resize_cmd).read()


def convert_ts(i, out):
    convert_cmd = 'ffmpeg -i %s -vcodec copy -acodec copy -vbsf h264_mp4toannexb %s' % (i, out)
    rm(out)
    os.popen(convert_cmd).read()

def water_mp4(i,out, logo, logow, logoh, corner, w, h):
    if corner == 1:
        location = '%d:%d' % (w, h)
    elif corner  == 2:
        location = '%d: main_h-overlay_h-%d' % (w, h)
    elif corner == 3:
        location = 'main_w-overlay_w-%d:main_h-overlay_h-%d' % (w, h)
    elif corner == 4:
        location = 'main_w-overlay_w-%d:%d' % (w, h)
    water_cmd = 'ffmpeg -i %s -vf  "movie=%s,scale=%d: %d[watermask]; [in] [watermask] overlay=%s [out]" %s' % (i, logo, logow, logoh, location, out)
    rm(out)
    os.popen(water_cmd).read()

def rm(out):
    if  os.path.exists(out):
        os.remove(out)

def convert_water_mp4(i, o, width, height, logo, logow, logoh, corner, w, h):
    resize_mp4(i, 'resize.mp4', width, height)
    water_mp4('resize.mp4', 'water.mp4', logo, logow, logoh, corner, w, h)
    rm('resize.mp4')
    convert_ts('water.mp4', o)
    rm('water.mp4')

def convert_mp4(i, o, width, height):
    resize_mp4(i, 'resize.mp4', width, height)
    convert_ts('resize.mp4', o,)
    rm('resize.mp4')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        os.popen('wget "%s" -O i.mp4'% sys.argv[1])
    info = video_info.getVideoInfo('i.mp4')
    convert_mp4('CTA1_1.mp4', 'CTA1_1.ts', 640, 640)
    convert_mp4('CTA4_3.mp4', 'CTA4_3.ts', 800, 600)
    convert_mp4('CTA16_9.mp4', 'CTA16_9.ts', 720, 480)

    if info:
        if info['duration'] < 10 or info['duration'] > 30:
            print 'duration = %s must be in [10,30]' % (info['duration'])
        else:
            rate = info['width'] / info['height'] * 1.0
            if 0.95 < rate < 1.05:
                width = 640
                height = 640
                cta = 'CTA1_1.ts'
            elif 1.3 < rate < 1.36:
                width = 800
                height = 600
                cta = 'CTA4_3.ts'
            elif 1.75 < rate < 1.8:
                width = 720
                height = 480
                cta = 'CTA16_9.ts'

            #convert_water_mp4('1.mp4', '1.ts', width, height, 'logo.png', 60, 60, 4, 25, 25 )
            convert_mp4('i.mp4', 'i.ts', width, height)
            merge_mp4(['i.ts', cta], 'output.mp4')
            rm('i.ts')
