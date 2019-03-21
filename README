# Gstream Tools for Encoder Development in the NERVE Center



## Gstreamer

### Comand Break down 

 will launch the stream:

``` $ bash gstreamer.sh <IP of stream> <file for our ecnoders it will 0 or 1> <optional latency var>```
``` $ bash gstreamer.sh 10.10.10.151 1 ```
the above commands launchs the substream 1 of the camera 10.10.10.151

```
gst-launch-1.0 rtspsrc location="$location" latency=$latency ! video/x-raw,width=640,height=320 ! rtph264depay ! avdec_h264 ! autovideosink
```
* rtspsrc: defines the source file we are looking for will an rtsp file 
* location: where the file is found can be represented in a rtsp://<host>/<file>
* latecny: The latency is the time it takes for a sample captured at timestamp 0 to reach the sink
* rtph264depay: decodes h264 videos 
* avdec_h264: is a decoder for h.264 audio and video 
* autovideosink: is a video sink that automatically detects an appropriate video sink to use 
* video/x-raw,width=640,height=320: determines the video size 
## FFSERVE
Development resource

This is responsible for launching an rtsp server file. Which allows for development outside of having encoders on. Just produces an rtsp stream. 


## Know_Ips

The HD encoders at NERVE:
* 10.10.10.131
* 10.10.10.142
* 10.10.10.151
* 10.10.10.236

## Resources ( From a while ago):
https://github.com/hadware/gstreamer-python-player
https://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html
https://github.com/GStreamer/gst-python
https://lazka.github.io/pgi-docs/#GstRtsp-1.0/functions.html
https://coderwall.com/p/xll1aa/low-latency-desktop-stream-to-raspberry-pi-using-hardware-decoding
https://www.videolan.org/streaming-features.html

