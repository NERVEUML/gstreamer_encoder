#!/usr/bin/env python

# activate our virtual environment
import os
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
base_dir = os.path.dirname(os.path.abspath(__file__))
activate_this = os.path.join(base_dir, 'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
#done activating virtualenv

import time
import requests
import xml.etree.ElementTree as et
from pprint import pprint
import xmltodict
import multiprocessing

class EncoderHTTPAPI():
    # wifi_ap_mode is basically a boolean, where 1 means yes, it's an AP
    def __init__(self,ip,auth=None,timeout=2):
        #timeout in seconds
        self.ip = ip
        self.port = 80
        self.timeout = timeout
        if auth:
            self.auth = requests.auth.HTTPBasicAuth(*auth)
        else:
            self.auth = None
        self.baseurl = "http://%s:%d/"%(self.ip,self.port)

        #no test if alive
        mydata = self.get_sys()
        self.mac = mydata["mac"]
        self.hostname = mydata["hostname"]
        self.name = "%s-%s-%s"%(self.hostname,self.ip,self.mac)

    def ping(self):
        try:
            return bool(self.get_status())
        except Exception as e:
            return False

    def get_status(self):
        return self.encoder_getopts("status")
    def get_wifi(self):
        return self.encoder_getopts("wifi")
    def get_sys(self):
        return self.encoder_getopts("sys")

    def get_output(self,output_idx):
        payload = {
                "output":output_idx
                }
        return self.encoder_getopts("output", payload)

    @staticmethod
    def parse_xmlopts(s):
        root = et.fromstring(s)
        return { child.tag: child.text for child in root}

    def encoder_getopts(self,what="sys",payload=None):
        #merge this and setopts
        #what=sys will be like /get_sys
        if payload is None:
            payload = {}
        payload["_"] = time.time()
        if what == "output":
            payload["input"] = 0
        r = requests.get(self.baseurl + "get_%s"%(what), auth=self.auth, params=payload, timeout=self.timeout)
        opts = EncoderHTTPAPI.parse_xmlopts(r.text)
        opts = xmltodict.parse(r.text)
        # pprint(opts)
        return opts[what] #always in a root level tag called what we got

    def encoder_setopts(self,what="sys",payload=None):
        #send as GET params in url
        #do i have to send all or can i just send modified ones?
        r = requests.get(self.baseurl + "set_%s"%(what), auth=self.auth, params=payload, timeout=self.timeout)
        return r.status_code == 200
        

    def set_output(self,output_idx,values):
        payload = {
                "output":output_idx
                }
        for k,v in values.items():
            payload[k] = v
        return self.encoder_setopts("output", payload)

class multiple_encoders():
    def __init__(self,ips_as_list,auth):
        self.my_encoders = []
        for ip in ips_as_list:
            self.my_encoders.append( EncoderHTTPAPI(ip,auth) )

    def __getitem__(self,key):
        return self.my_encoders[ key ];
    def __len__(self):
        return len(self.my_encoders)


    def do(self,name,args=None):
        if args is None:
            args = []
        results = {}
        for e in self.my_encoders:
            fn = getattr(e, name)
            results[e.name] = fn(*args)
        return results


def test_set_resolution_of_substream_1(e1, width, height):
    before = e1.get_output(1)
    #print("Currently have %s x %s"%(before["venc_width"],before["venc_height"]))
    e1.set_output(1,{"venc_width":width,"venc_height":height})
    after = e1.get_output(1)
    #print("Currently have %s x %s"%(after["venc_width"],after["venc_height"]))
    return after["venc_width"] == str(width) and after["venc_height"] == str(height)

def main():
    #use nmap to find them based on fingerprint
    auth=("admin","admin")
    ips = [
            "10.10.10.181"
            ]
    es = multiple_encoders(ips,auth)
    e1 = es[0]
    test_set_resolution_of_substream_1(e1, 1024,576)
    import pdb; pdb.set_trace()



if __name__ == "__main__":
    main()



#curl 'http://10.10.10.181/get_sys?_=1526324644526' -H 'Accept: application/xml, text/xml, */*' --compressed -H 'Accept-Language: en-US,en;q=0.5' -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Host: 10.10.10.181' -H 'Referer: http://10.10.10.181/WifiSetE.html' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0' -H 'X-Requested-With: XMLHttpRequest'


output="""
<?xml version="1.0" encoding="UTF-8"?>
<sys>
<ip>192.168.1.168</ip>
<netmask>255.255.255.0</netmask>
<gateway>192.168.1.1</gateway>
<mac>00:13:14:15:B8:FA</mac>
<dhcp_enable>0</dhcp_enable>
<g4_dev_exist>1</g4_dev_exist>
<g4_enable>1</g4_enable>
<g4_apn></g4_apn>
<wifi_dev_exist>1</wifi_dev_exist>
<wifi_enable>1</wifi_enable>
<wifi_ap_mode>0</wifi_ap_mode>
<wifi_hostap_essid>AP_Encoder_47354</wifi_hostap_essid>
<wifi_hostap_psk>12345678</wifi_hostap_psk>
<wifi_hostap_channel>6</wifi_hostap_channel>
<wifi id="0">
<wifi_essid>NERVE-staff</wifi_essid>
<wifi_psk>hic.sunt.robotics</wifi_psk>
<wifi_ip>192.168.1.169</wifi_ip>
<wifi_netmask>255.255.255.0</wifi_netmask>
<wifi_gateway>192.168.1.1</wifi_gateway>
<wifi_dhcp_enable>1</wifi_dhcp_enable>
</wifi>
<wifi id="1">
<wifi_essid></wifi_essid>
<wifi_psk></wifi_psk>
<wifi_ip>192.168.0.168</wifi_ip>
<wifi_netmask>255.255.255.0</wifi_netmask>
<wifi_gateway>192.168.0.1</wifi_gateway>
<wifi_dhcp_enable>0</wifi_dhcp_enable>
</wifi>
<wifi id="2">
<wifi_essid></wifi_essid>
<wifi_psk></wifi_psk>
<wifi_ip>192.168.0.168</wifi_ip>
<wifi_netmask>255.255.255.0</wifi_netmask>
<wifi_gateway>192.168.0.1</wifi_gateway>
<wifi_dhcp_enable>0</wifi_dhcp_enable>
</wifi>
<dns0>8.8.8.8</dns0>
<dns1>192.168.1.1</dns1>
<http_port>8080</http_port>
<rtsp_port>8554</rtsp_port>
<rtsp_g711>0</rtsp_g711>
<rtsp_g711_8k>1</rtsp_g711_8k>
<ts_over_rtsp>0</ts_over_rtsp>
<rtp_multicast>0</rtp_multicast>
<udp_ttl>64</udp_ttl>
<html_password>admin</html_password>
<hostname>encoder</hostname>
<language>english</language>
</sys>
"""
"""
reboot:
    curl 'http://10.10.10.181/reboot?_=1526325043886' -H 'Accept: text/plain, */*' --compressed -H 'Accept-Language: en-US,en;q=0.5' -H 'Authorization: Basic YWRtaW46YWRtaW4=' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Host: 10.10.10.181' -H 'Referer: http://10.10.10.181/RebootE.html' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0' -H 'X-Requested-With: XMLHttpRequest'


get_output for 1
<output>
<input>0</input>
<output>1</output>
<aenc_codec>0</aenc_codec>
<aenc_bitrate>128000</aenc_bitrate>
<venc_enable>1</venc_enable>
<venc_codec>96</venc_codec>
<venc_gop>30</venc_gop>
<vi_cap_width>1920</vi_cap_width>
<vi_cap_height>1080</vi_cap_height>
<venc_width_height_same_as_input>0</venc_width_height_same_as_input>
<venc_width>1280</venc_width>
<venc_height>720</venc_height>
<venc_framerate>30</venc_framerate>
<venc_profile>1</venc_profile>
<venc_rc_mode>1</venc_rc_mode>
<venc_bitrate>1800</venc_bitrate>
<http_private_enable>0</http_private_enable>
<http_private_uri>/1.pte</http_private_uri>
<http_ts_enable>0</http_ts_enable>
<http_ts_uri>/1.ts</http_ts_uri>
<http_hls_enable>0</http_hls_enable>
<http_hls_uri>/1.m3u8</http_hls_uri>
<http_flv_enable>0</http_flv_enable>
<http_flv_uri>/1.flv</http_flv_uri>
<rtsp_enable>1</rtsp_enable>
<rtsp_uri>/1</rtsp_uri>
<rtmp_enable>0</rtmp_enable>
<rtmp_publish_uri>rtmp://192.168.1.50/live/1</rtmp_publish_uri>
<multicast_enable>0</multicast_enable>
<multicast_ip>238.0.0.1</multicast_ip>
<multicast_port>1235</multicast_port>
<unicast_enable>0</unicast_enable>
<unicast_ip></unicast_ip>
<unicast_port>1000</unicast_port>
</output>
"""
"""
host="10.10.10.181"
baseuri='http://${host}/set_output?' 
curl "$baseuri"
'set_output?
input=0
output=1
venc_framerate=30
venc_gop=30
venc_width=1280
venc_height=720
venc_rc_mode=1
venc_bitrate=1800
http_ts_uri=%2F1.ts
http_flv_uri=%2F1.flv
rtsp_uri=%2F1
rtmp_publish_uri=rtmp%3A%2F%2F192.168.1.50%2Flive%2F1
rtmp_enable=0
http_ts_enable=0
http_flv_enable=0
rtsp_enable=1
venc_profile=1
http_hls_uri=%2F1.m3u8
http_hls_enable=0
venc_width_height_same_as_input=0
multicast_ip=238.0.0.1
multicast_port=1235
multicast_enable=0
_=1526323710764' 


--compressed 
-H 'Accept: text/plain, */*' 
-H 'Accept-Language: en-US,en;q=0.5' 
-H 'Authorization: Basic YWRtaW46YWRtaW4=' 
-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0' 
-H 'X-Requested-With: XMLHttpRequest'

"""
