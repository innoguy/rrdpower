#!/bin/bash

DB="/var/log/cirrus-rrd/power"
capture_window=1   # seconds to capture packet
heartbeat=300      # seconds sleep between captures
capture_space=600  # seconds between recorded values

if [ ! -f "$DB.rrd" ]
then
	rrdtool create $DB.rrd --step $capture_space \
		DS:PortA_V:GAUGE:$capture_space:U:U \
        DS:PortA_I:GAUGE:$capture_space:U:U \
		DS:PortA_PF:GAUGE:$capture_space:U:U \
        DS:PortB_V:GAUGE:$capture_space:U:U \
		DS:PortB_I:GAUGE:$capture_space:U:U \
		DS:PortB_PF:GAUGE:$capture_space:U:U \
		DS:SPI1_V:GAUGE:$capture_space:U:U \
        DS:SPI1_I:GAUGE:$capture_space:U:U \
        DS:SPI1_PF:GAUGE:$capture_space:U:U \
		DS:SPI2_V:GAUGE:$capture_space:U:U \
		DS:SPI2_I:GAUGE:$capture_space:U:U \
		DS:SPI2_PF:GAUGE:$capture_space:U:U \
        RRA:AVERAGE:0.5:1:1000 
fi

if [ ! -f "$PWD/powermonitoring.service" ]
then
	echo "[Unit]" > powermonitoring.service
	echo "Description=Power monitoring values to round robin database" >> powermonitoring.service
	echo "DefaultDependencies=no" >> powermonitoring.service
	echo "After=network.target" >> powermonitoring.service
	echo "" >> powermonitoring.service
	echo "[Service]" >> powermonitoring.service
	echo "ExecStart=sudo python3 $PWD/powermonitor.py " >> powermonitoring.service
	echo "Restart=always" >> powermonitoring.service
	echo "RestartSec=5s" >> powermonitoring.service
	echo "[Install]" >> powermonitoring.service
    echo "WantedBy=multi-user.target" >> powermonitoring.service
fi

if [ ! -f "/etc/systemd/system/powermonitoring.service" ]
then
    ln -s $PWD/powermonitoring.service /etc/systemd/system/powermonitoring.service
fi

sudo systemctl daemon-reload
sudo systemctl enable powermonitoring
sudo systemctl start powermonitoring
sudo systemctl status powermonitoring