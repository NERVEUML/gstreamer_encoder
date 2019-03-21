latency=$2
if [[ "x$latency" == "x" ]]; then
	latency=200
fi
file=$1
if [[ "x$file" == "x" ]]; then
	file=a.mov
fi
host=192.168.1.106:8301
location=rtsp://$host/$file

gst-launch-1.0 rtspsrc location="$location" latency=$latency ! rtph264depay ! avdec_h264 ! autovideosink
#gst-launch-1.0 rtspsrc location=rtsp://togo:8301/a.mp4 latency=$latency ! rtph264depay ! avdec_h264 ! autovideosink
#gst-launch-1.0 rtspsrc location=rtsp://togo:8301/a.mp4 latency=100 ! rtph264depay ! avdec_h264 ! autovideosink
#gst-launch-1.0 rtspsrc location=rtsp://togo:8301/a.mp4 latency=0 ! rtph264depay ! avdec_h264 ! autovideosink


#gst-launch-1.0 rtspsrc location=rtsp://togo:8301/a.mp4 ! queue ! tee name=t ! rtph264depay t. !  h264parse t. ! capsfilter caps="video/x-h264,width=1280,height=800,framerate=(fraction)25/1" t. !  avdec_h264 t. ! autovideosink t. ! queue !  rtpg726depay ! avdec_g726 !  audioconvert ! audioresample ! autoaudiosink
