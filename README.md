# csi
Client-AP Angle Measurement with 802.11n Channel State Information

    +--------------------+                                   +-----------------+
    |Lenovo T400 Equipped|            802.11n CSI            |Nexus 7 [2013] as|
    |with Intel 5300 NIC +-----------------------------------+Portable Hotspot |
    +--------------------+                                   +-----------------+


## dev

`[csi] $ sudo ./run.sh`

`[csi] $ eog png/data_0721_01_01/0001.png`

`[csi] $ ./src/fingerprint.py json/data_0721.json`

`[csi/electron] $ sudo npm start`
