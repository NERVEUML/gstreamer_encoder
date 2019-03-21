latency=$3
if [[ "x$latency" == "x" ]]; then
	latency=200
fi
file=$2
if [[ "x$file" == "x" ]]; then
	file=a.mov
fi
host=$1
location=rtsp://$host/$file

gst-launch-1.0 rtspsrc location="$location" latency=$latency ! video/x-raw,width=640,height=320 ! rtph264depay ! avdec_h264 ! autovideosink
#gst-launch-1.0 rtspsrc location=rtsp://<Host Ip:port>/<file name> latency=$latency ! rtph264depay ! avdec_h264 ! autovideosink
