# csi
Client-AP Angle Measurement with 802.11n Channel State Information

    +--------------------+                                   +-----------------+
    |Lenovo T400 Equipped|            802.11n CSI            |Nexus 7 [2013] as|
    |with Intel 5300 NIC +-----------------------------------+Portable Hotspot |
    +--------------------+            Human Body             +-----------------+


## dev

```bash
# Collect CSI
[csi] $ sudo ./collect.sh
      What is your X? 21
      What is your Y? 42
      You are at (21, 42)
# Display CSI plots
[csi] $ eog png/data_0724_01_01/0001.png
# Find current position based on what has been collected today
[csi] $ sudo ./findme.sh
      You are probably located at (21, 42)
# Clean everything collected today (plots, JSON files)
[csi] $ sudo ./clean_today.sh

# (Optional) Start real-time CSI visualizer
[csi/electron] $ sudo npm start
```
