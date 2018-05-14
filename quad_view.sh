#!/bin/bash

#gst-launch-1.0 rtspsrc location="$location" latency=$latency ! rtph264depay ! avdec_h264 ! autovideosink


latency=100
i1="rtsp://togo:8301/a720.mp4"
i2="rtsp://togo:8301/a720.mp4"
i3="rtsp://togo:8301/a720.mp4"
i4="rtsp://togo:8301/a720.mp4"

i1="rtsp://10.10.10.181/1"
i2="rtsp://10.10.10.181/1"
i3="rtsp://10.10.10.181/1"
i4="rtsp://10.10.10.181/1"

source_1="videotestsrc"
source_2="videotestsrc"
source_3="videotestsrc"
source_4="videotestsrc"

tcptimeout=1000000
timeouttoretrywithtcp=0
rtspsrc="rtspsrc timeout=$timeouttoretrywithtcp tcp-timeout=$tcptimeout "
source_1="$rtspsrc location="$i1" latency="$latency" ! rtph264depay ! avdec_h264"
source_2="$rtspsrc location="$i2" latency="$latency" ! rtph264depay ! avdec_h264"
source_3="$rtspsrc location="$i3" latency="$latency" ! rtph264depay ! avdec_h264"
source_4="$rtspsrc location="$i4" latency="$latency" ! rtph264depay ! avdec_h264"


#source_1="v4l2src"
#source_2="videotestsrc pattern="snow""
#gst-launch-1.0 $source_1  ! autovideosink
#exit

echo Sources:
echo $source_1
echo $source_2
echo $source_3
echo $source_4

get_rtsp_res(){
  url="$1"
  ffprobe "$1" 2>&1 |grep Stream |grep Video |grep -oP "\d+x\d+"
}
res_axb=$(get_rtsp_res $i1)
source_x=$(echo $res_axb | cut -d "x" -f 1 )
source_y=$(echo $res_axb | cut -d "x" -f 2 )

xpos=$(($source_x))
ypos=$(($source_y))
echo x:$xpos
echo y:$ypos

gst-launch-1.0 glvideomixer name=mix \
  sink_0::xpos=0 sink_0::ypos=0 \
  sink_1::xpos=$xpos sink_1::ypos=0 \
  sink_2::xpos=0 sink_2::ypos=$ypos \
  sink_3::xpos=$xpos sink_3::ypos=$ypos ! autovideosink sync=false \
  $source_1 ! mix. \
  $source_2 ! mix. \
  $source_3 ! mix. \
  $source_4 ! mix.

#removed videoconvert before autovideosink, unsure what that does but seems to still work with it removed

#gst-launch-1.0 videomixer name=mix \
  #sink_0::xpos=0 sink_0::ypos=0 \
  #sink_1::xpos=960 sink_1::ypos=0 \
  #sink_2::xpos=0 sink_2::ypos=540 \
  #sink_3::xpos=960 sink_3::ypos=540 ! videoconvert ! autovideosink sync=false \
  #videotestsrc ! mix. \
  #videotestsrc ! mix. \
  #videotestsrc ! mix. \
  #videotestsrc ! mix.

#gst-launch-1.0 videomixer name=mix \
  #sink_0::xpos=0 sink_0::ypos=0 \
  #sink_1::xpos=960 sink_1::ypos=0 \
  #sink_2::xpos=0 sink_2::ypos=540 \
  #sink_3::xpos=960 sink_3::ypos=540 ! videoconvert ! autovideosink sync=false \
  #$source_1 ! rtph264depay ! avdec_h264 ! mix. \
  #$source_2 ! rtph264depay ! avdec_h264 ! mix. \
  #$source_3 ! rtph264depay ! avdec_h264 ! mix. \
  #$source_4 ! rtph264depay ! avdec_h264 ! mix.
