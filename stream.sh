#!/bin/bash
raspivid -o - -t 0 -n -w 1024 -h 768 -fps 24 | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264 --h264-fps=24

