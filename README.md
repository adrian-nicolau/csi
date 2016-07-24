# csi
Client-AP Angle Measurement with 802.11n Channel State Information

    +--------------------+                                   +-----------------+
    |Lenovo T400 Equipped|            802.11n CSI            |Nexus 7 [2013] as|
    |with Intel 5300 NIC +-----------------------------------+Portable Hotspot |
    +--------------------+                                   +-----------------+


## dev

```bash
# Collect CSI
[csi] $ sudo ./run_collect.sh
# Display CSI plots
[csi] $ eog png/data_0724_01_01/0001.png
# Find current position based on what has been collected before
[csi] $ sudo ./run_findme.sh json/data_0724.json

# (Optional) Start real-time CSI visualizer
[csi/electron] $ sudo npm start
```
