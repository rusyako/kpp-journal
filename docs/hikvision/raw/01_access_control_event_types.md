<!-- source_file: ISAPI/Country and Region Code (1).pdf -->
<!-- real_content: Access Control Event Types and Event Linkage Types -->
<!-- source_sha256: 3c0c62995179eed4dd55c66d14f9cdafa6db3b47816d45b754b962bfc9a777f0 -->
<!-- converter: markitdown_mcp.convert_to_markdown (MarkItDown MCP) -->



<!-- page: 1 -->

Access Control Event Types
The access control events are classified as four major types, i.e., alarm events (0x1), exception
events (0x2), operation events (0x3), additional information (0x4) and other events (0x5). Each
major type corresponds to multiple minor types, see details below.
Alarm Events (0x1)

| Value  |     |     | Description  |     |
| ------ | --- | --- | ------------ | --- |
z
| 0x1  | Alarm Input  |     |     |     |
| ---- | ------------ | --- | --- | --- |
k
| 0x2  | Alarm Output  |     |     | .   |
| ---- | ------------- | --- | --- | --- |
a
| 0x3  | Motion Detection Alarm Starts  |     |     |     |
| ---- | ------------------------------ | --- | --- | --- |
t
| 0x4  | Motion Detection Alarm Stops  |     |     |     |
| ---- | ----------------------------- | --- | --- | --- |
h
| 0x5  | Tampering Alarm Starts  |     |     | @   |
| ---- | ----------------------- | --- | --- | --- |
n
| 0x6  | Tampering Alarm Stops  |     |     |     |
| ---- | ---------------------- | --- | --- | --- |
i
| 0x7  | VCA Alarm Starts  |     |     |     |
| ---- | ----------------- | --- | --- | --- |
k
| 0x8  | VCA Alarm Stops  |     | i   |     |
| ---- | ---------------- | --- | --- | --- |
u
| 0xb  | Network Alarm Starts  |     |     |     |
| ---- | --------------------- | --- | --- | --- |
h
| 0xc  | Network Alarm Stops  |     |     |     |
| ---- | -------------------- | --- | --- | --- |
c
| 0xd    | Restore Network. Alarm  |                         |     |     |
| ------ | ----------------------- | ----------------------- | --- | --- |
|        |                         | y                       | A   |     |
| 0x400  | Zone Short C            | ircuit AttemTpts Alarm  |     |     |
i
H
l
| 0x401  | Zone Disconnected Alarm  |     |     |     |
| ------ | ------------------------ | --- | --- | --- |
i
s
| 0x402  | Zone Exception Alarm  |     |     |     |
| ------ | --------------------- | --- | --- | --- |
a
| 0x403  | Zvone Restored                             |     |     |     |
| ------ | ------------------------------------------ | --- | --- | --- |
| 0x404  | Zone Tampering Alarm                       |     |     |     |
| 0x405  | Zone Tampering Restored                    |     |     |     |
| 0x406  | Card Reader Tampering Alarm                |     |     |     |
| 0x407  | Card Reader Tampering Restored             |     |     |     |
| 0x408  | Alarm Input Alarm Triggered                |     |     |     |
| 0x409  | Alarm Input Restored                       |     |     |     |
| 0x40a  | Duress Alarm                               |     |     |     |
| 0x40b  | No Memory Alarm for Offline Events         |     |     |     |
| 0x40c  | Maximum Failed Card Authentications Alarm  |     |     |     |
| 0x40d  | SD Card Full Alarm                         |     |     |     |

<!-- page: 2 -->

| Value  |                                              |     | Description  |     |
| ------ | -------------------------------------------- | --- | ------------ | --- |
| 0x40e  | Capture Linkage Alarm                        |     |              |     |
| 0x40f  | Secure Door Control Unit Tampering Alarm     |     |              |     |
| 0x410  | Secure Door Control Unit Tampering Restored  |     |              |     |
| 0x411  | POS Starts                                   |     |              |     |
| 0x412  | POS Stops                                    |     |              |     |
| 0x413  | Low Face Picture Quality                     |     |              |     |
| 0x414  | Low Fingerprint Picture Quality              |     |              |     |
| 0x415  | Fire Input Short Circuit Attempts Alarm      |     |              |     |
z
| 0x416  | Fire Input Open Circuit Attempts Alarm  |     |     |     |
| ------ | --------------------------------------- | --- | --- | --- |
k
.
| 0x417  | Fire Input Restored  |     |     |     |
| ------ | -------------------- | --- | --- | --- |
a
t
| 0x418  | Fire Button Triggered  |     |     |     |
| ------ | ---------------------- | --- | --- | --- |
h
| 0x419  | Fire Button Resumed  |     |     | @   |
| ------ | -------------------- | --- | --- | --- |
n
| 0x41a  | Maintenance Button Triggeredi  |     |     |     |
| ------ | ------------------------------ | --- | --- | --- |
k
| 0x41b  | Maintenance Button Resuimed  |     |     |     |
| ------ | ---------------------------- | --- | --- | --- |
u
| 0x41c  | Panic Button Triggered  |     |     |     |
| ------ | ----------------------- | --- | --- | --- |
h
c
| 0x41d  | Panic Button Resumed  |     |     |     |
| ------ | --------------------- | --- | --- | --- |
.
|        |                                                  | y   | A   |     |
| ------ | ------------------------------------------------ | --- | --- | --- |
| 0x41e  | Distributed Elevator Controller Tampering Alarm  |     |     |     |
T
i
H
l
| 0x41f  | Distributed Elevator Controller Tampering Restored  |     |     |     |
| ------ | --------------------------------------------------- | --- | --- | --- |
i
| 0x420  | Peopsle Density Overload Alarm Starts  |     |     |     |
| ------ | -------------------------------------- | --- | --- | --- |
| 0x421  | Peoaple Density Overload Alarm Stops   |     |     |     |
v
| 0x422  | Lane Controller Tampering Alarm                  |     |     |     |
| ------ | ------------------------------------------------ | --- | --- | --- |
| 0x423  | Lane Controller Tampering Alarm Restored         |     |     |     |
| 0x424  | Lane Controller Fire Input Alarm                 |     |     |     |
| 0x425  | Lane Controller Fire Input Alarm Restored        |     |     |     |
| 0x426  | Heart Rate Exception Alarm Starts                |     |     |     |
| 0x427  | Heart Rate Exception Alarm Stops                 |     |     |     |
| 0x428  | Blood Oxygen Exception Alarm Starts              |     |     |     |
| 0x429  | Blood Oxygen Exception Alarm Stops               |     |     |     |
| 0x42a  | Systolic Blood Pressure Exception Alarm Starts   |     |     |     |
| 0x42b  | Systolic Blood Pressure Exception Alarm Stops    |     |     |     |
| 0x42c  | Diastolic Blood Pressure Exception Alarm Starts  |     |     |     |
| 0x42d  | Diastolic Blood Pressure Exception Alarm Stops   |     |     |     |
| 0x42e  | Absence Detection Starts                         |     |     |     |
| 0x42f  | Absence Detection Stops                          |     |     |     |

<!-- page: 3 -->

| Value  |                                       |     | Description  |     |     |
| ------ | ------------------------------------- | --- | ------------ | --- | --- |
| 0x430  | Standing Detection Starts             |     |              |     |     |
| 0x431  | Standing Detection Stops              |     |              |     |     |
| 0x434  | People Counting Change Starts         |     |              |     |     |
| 0x435  | People Counting Change Stops          |     |              |     |     |
| 0x438  | People Running Starts                 |     |              |     |     |
| 0x439  | People Running Stops                  |     |              |     |     |
| 0x43a  | Violent Motion Detection Starts       |     |              |     |     |
| 0x43b  | Violent Motion Detection Stops        |     |              |     |     |
| 0x43c  | People Falling Down Detection Starts  |     |              |     |     |
| 0x43d  | People Falling Down Detection Stops   |     |              |     |     |
z
| 0x43e  | People Overstay Detection Starts  |     |     |     |     |
| ------ | --------------------------------- | --- | --- | --- | --- |
k
| 0x43f  | People Overstay Detection Stops  |     |     |     | .   |
| ------ | -------------------------------- | --- | --- | --- | --- |
a
| 0x440  | No Paper in Printer Alarm                                    |     |     | t   |     |
| ------ | ------------------------------------------------------------ | --- | --- | --- | --- |
| 0x441  | Failed Attempts of Opening Door via Password Exceeded Limit  |     |     | h   |     |
@
| 0x442  | No Memory Alarm for Valid Offlinne Events  |     |     |     |     |
| ------ | ------------------------------------------ | --- | --- | --- | --- |
i
0x900 to 0x93f  Access Control: Custom Alarkm Event 1 to Custom Alarm Event 64
i
| 0x950  | Smart Lock Duress Alarm (Fingerprint)  |     |     |     |     |
| ------ | -------------------------------------- | --- | --- | --- | --- |
u
| 0x951  | Smart Lock Duress Alarm (Password)  |     |     |     |     |
| ------ | ----------------------------------- | --- | --- | --- | --- |
h
| 0x952  | Smart Lock Broken cAlarm  |     |     |     |     |
| ------ | ------------------------- | --- | --- | --- | --- |
.
| 0x953  | Smart Lock Locked Alarm  |                    |     |     |     |
| ------ | ------------------------ | ------------------ | --- | --- | --- |
|        |                          | y                  | A   |     |     |
| 0x954  | Smart Lock L             | ow Voltage ATlarm  |     |     |     |
i
Smart Loclk Blocklist AlHarm
0x955
i
| 0x956  | Smart Lock Device Offline Alarm  |     |     |     |     |
| ------ | -------------------------------- | --- | --- | --- | --- |
s
| 0x957  | Smaart Lock Unlatched Alarm                   |     |     |     |     |
| ------ | --------------------------------------------- | --- | --- | --- | --- |
| 0x958  | Svmart Lock User Not In Alarm                 |     |     |     |     |
| 0x959  | Magnetic Contact Detector Alarm               |     |     |     |     |
| 0x95a  | Infrared Detector Alarm                       |     |     |     |     |
| 0x95b  | Fingerprint Locked Alarm                      |     |     |     |     |
| 0x95c  | Password Locked Alarm                         |     |     |     |     |
| 0x95d  | Smart Door Lock Duress Alarm                  |     |     |     |     |
| 0x95e  | Access Module Fire Input Short Circuit Alarm  |     |     |     |     |
| 0x95f  | Restore Access Module Fire Input              |     |     |     |     |
| 0x960  | Network Loop Alarm                            |     |     |     |     |
| 0x961  | Restore Network Loop Alarm                    |     |     |     |     |

Exception Events (0x2)

<!-- page: 4 -->

| Value  |                                  |     | Description  |     |     |
| ------ | -------------------------------- | --- | ------------ | --- | --- |
| 0x21   | Video Signal Loss                |     |              |     |     |
| 0x22   | Illegal Access                   |     |              |     |     |
| 0x23   | HDD Full                         |     |              |     |     |
| 0x24   | HDD Error                        |     |              |     |     |
| 0x25   | MODEM Offline                    |     |              |     |     |
| 0x26   | IP Address Conflict              |     |              |     |     |
| 0x27   | Network Disconnected             |     |              |     |     |
| 0x28   | Recording Error                  |     |              |     |     |
| 0x29   | Network Camera Connection Error  |     |              | z   |     |
| 0x2a   | Video Input Exception            |     |              | k   |     |
.
| 0x2b  | Network Camera IP Address Conflicted  |     |     |     |     |
| ----- | ------------------------------------- | --- | --- | --- | --- |
a
| 0x2e  | Video Standard Mismatch                         |     |     | t   |     |
| ----- | ----------------------------------------------- | --- | --- | --- | --- |
| 0x31  | Video Management System: Fan Statuhs Exception  |     |     |     |     |
@
| 0x32  | Video Management System: Fan Status Recovered  |     |     |     |     |
| ----- | ---------------------------------------------- | --- | --- | --- | --- |
n
| 0x33  | Video Management System: 64i76 Reboot Exception      |     |     |     |     |
| ----- | ---------------------------------------------------- | --- | --- | --- | --- |
| 0x34  | Video Management System:k dm6467 Exception (Buzzer)  |     |     |     |     |
i
| 0x35  | Network Exception  |     |     |     |     |
| ----- | ------------------ | --- | --- | --- | --- |
u
| 0x36  | Memory Status Excephtion  |     |     |     |     |
| ----- | ------------------------- | --- | --- | --- | --- |
| 0x37  | File Status Exceptiocn    |     |     |     |     |
.
| 0x3a  | RS485 Connec | y tion ExceptioAn  |     |     |     |
| ----- | ------------ | ------------------ | --- | --- | --- |
T
i
| 0x3b  | RS485 Con | nection ResHtored  |     |     |     |
| ----- | --------- | ------------------ | --- | --- | --- |
l
i
| 0x400  | Power on  |     |     |     |     |
| ------ | --------- | --- | --- | --- | --- |
s
| 0x401  | Power off  a |     |     |     |     |
| ------ | ------------ | --- | --- | --- | --- |
v
| 0x402  | Watchdog Reset                       |     |     |     |     |
| ------ | ------------------------------------ | --- | --- | --- | --- |
| 0x403  | Low Battery Voltage                  |     |     |     |     |
| 0x404  | Battery Voltage Restored             |     |     |     |     |
| 0x405  | AC Power Disconnected                |     |     |     |     |
| 0x406  | AC Power Restored                    |     |     |     |     |
| 0x407  | Network Restored                     |     |     |     |     |
| 0x408  | Flash Reading and Writing Exception  |     |     |     |     |
| 0x409  | Card Reader Offline                  |     |     |     |     |
| 0x40a  | Card Reader Online                   |     |     |     |     |
| 0x40b  | Indicator Turns off                  |     |     |     |     |
| 0x40c  | Indicator Resumed                    |     |     |     |     |

<!-- page: 5 -->

Value

Description

0x40d

0x40e

0x40f

0x410

0x411

0x412

0x413

0x414

0x415

0x416

0x417

0x418

0x419

0x41a

0x41b

0x41c

0x41d

0x41e

0x41f

0x420

0x421

0x422

0x423

0x424

0x425

0x426

0x427

0x428

Lane Controller Offline

Lane Controller Online

Secure Door Control Unit Offline

Secure Door Control Unit Online

Low Battery Voltage (Only for Face Recognition Terminal)

Battery Voltage Recovered (Only for Face Recognition Terminal)

Network of Distributed Access Controller Disconnected

Distributed Access Controller Online

Distributed Access Controller Offline

RS485 Loop of Main Access Controller Connected

Network of Distributed Access Controller Restored

RS485 Loop of Main Access Controller Disconnected

Downstream RS485 Loop of Distributed Access Control
Disconnected

vasiliy.chuikin@hta.kz

HTA

Distributed Elevator Controller Offline

Distributed Elevator Controller Online

Fingerprint Module Disconnected

ID Card Reader Disconnected

ID Card Reader Connected

Downstream RS485 Loop of Distributed Access Control Connected

Fingerprint Module Connected

Camera Disconnected

Camera Connected

COM Port Disconnected

COM Port Connected

Device Unauthorized

Face Recognition Terminal Online

Face Recognition Terminal Offline

Local Login Lock



<!-- page: 6 -->

| Value  |                                                       |     | Description  |
| ------ | ----------------------------------------------------- | --- | ------------ |
| 0x429  | Local Login Unlock                                    |     |              |
| 0x42a  | Communication with Anti-passing Back Server Failed    |     |              |
| 0x42b  | Communication with Anti-passing Back Server Restored  |     |              |
| 0x42c  | Motor or Sensor Exception                             |     |              |
| 0x42d  | CAN Bus Exception                                     |     |              |
| 0x42e  | CAN Bus Exception Restored                            |     |              |
| 0x42f  | Too High Pedestal Temperature                         |     |              |
z
| 0x430  | Active Infrared Intrusion Detector Exception  |     |     |
| ------ | --------------------------------------------- | --- | --- |
k
.
| 0x431  | Active Infrared Intrusion Detector Restored  |     |     |
| ------ | -------------------------------------------- | --- | --- |
a
t
| 0x432  | Communication with Light Board Failed  |     |     |
| ------ | -------------------------------------- | --- | --- |
h
@
| 0x433  | Communication with Light Board Restored  |     |     |
| ------ | ---------------------------------------- | --- | --- |
n
| 0x434  | Communication with IR Adaptoir Failed  |     |     |
| ------ | -------------------------------------- | --- | --- |
k
| 0x435  | Communication with IR Adiaptor Restored  |     |     |
| ------ | ---------------------------------------- | --- | --- |
u
| 0x436  | Printer Online  |     |     |
| ------ | --------------- | --- | --- |
h
c
| 0x437  | Printer Offline  | .      |     |
| ------ | ---------------- | ------ | --- |
|        |                  | y      | A   |
| 0x438  | 4G Module O      | nline  | T   |
i
H
l
| 0x439  | 4G Module Offline  |     |     |
| ------ | ------------------ | --- | --- |
i
DSP Sstarting Failed
0x43a
a
| 0x43b  | Smart Rule Not Supported  |     |     |
| ------ | ------------------------- | --- | --- |
v
| 0x43c  | Auxiliary Board Disconnected                 |     |     |
| ------ | -------------------------------------------- | --- | --- |
| 0x43d  | Auxiliary Board Connected                    |     |     |
| 0x43e  | Secure ID Card Unit Exception                |     |     |
| 0x43f  | Secure ID Card Unit Restored                 |     |     |
| 0x440  | Fingerprint Collection Peripheral Exception  |     |     |
| 0x441  | Fingerprint Collection Peripheral Restored   |     |     |
| 0x442  | Repetitive Attack                            |     |     |
| 0x443  | TLS Communication Exception                  |     |     |
| 0x444  | Smart Disk Offline                           |     |     |
| 0x445  | Smart Disk Online                            |     |     |
| 0x446  | Lock Refund                                  |     |     |
| 0x447  | Coding Disk Online                           |     |     |
| 0x448  | Coding Disk Offline                          |     |     |

<!-- page: 7 -->

| Value  |                    |     | Description  |
| ------ | ------------------ | --- | ------------ |
| 0x449  | Keypad Offline     |     |              |
| 0x44a  | Keypad Online      |     |              |
| 0x44b  | 5G Module Online   |     |              |
| 0x44c  | 5G Module Offline  |     |              |
Extension Module (Modules Externally Accessed via USB and
0x44d  Supporting Hot Swapping: E.g., ID Card Reader, Fingerprint Sensor,
Bluetooth, QR Code) Online
Extension Module (Modules Externally Accessed via USB and
0x44e  Supporting Hot Swapping: E.g., ID Card Reader, Fingerprint Sensor,
Bluetooth, QR Code) Offline  z
k
| 0x44f  | Disconnect from Multi-Door Interlocking Server  |     |     |
| ------ | ----------------------------------------------- | --- | --- |
.
0x450  Restore Communication with Multi-Door Ianterlocking Server
t
| 0x451  | QR Code Reader Offline  |     |     |
| ------ | ----------------------- | --- | --- |
h
| 0x452  | QR Code Reader Online  |     |     |
| ------ | ---------------------- | --- | --- |
@
| 0x453  | Lock Health Information Exceptionn   |     |     |
| ------ | ------------------------------------ | --- | --- |
| 0x454  | Unlock Health Information Exception  |     | i   |
k
| 0x455  | Optional Board Offline  |     |     |
| ------ | ----------------------- | --- | --- |
i
| 0x456  | Restore Optional Boardu Offline  |     |     |
| ------ | -------------------------------- | --- | --- |
| 0x457  | Lock Offline                     | h   |     |
c
| 0x458  | Restore Lock Offline  |     |     |
| ------ | --------------------- | --- | --- |
.
| 0x459  | Doorbell Offlinye  |     | A   |
| ------ | ------------------ | --- | --- |
T
| 0x45a  | Restore Doorbell Offline  | i   |     |
| ------ | ------------------------- | --- | --- |
H
l
| 0x45b  | Exit Button Offline  |     |     |
| ------ | -------------------- | --- | --- |
i
| 0x45c  | Restosre Exit Button Offline  |     |     |
| ------ | ----------------------------- | --- | --- |
a
| 0x45d  | Lock Low Battery  |     |     |
| ------ | ----------------- | --- | --- |
v
| 0x45e  | Lock Low Battery Restored         |     |     |
| ------ | --------------------------------- | --- | --- |
| 0x45f  | Lock Battery to Be Depleted       |     |     |
| 0x460  | Card Reader Low Battery           |     |     |
| 0x461  | Card Reader Low Battery Restored  |     |     |
| 0x462  | Exit Button Low Battery           |     |     |
| 0x463  | Exit Button Low Battery Restored  |     |     |
| 0x464  | Unlocking Stops Unexpectedly      |     |     |
| 0x465  | Locking Stops Unexpectedly        |     |     |
| 0x466  | Relay Offline                     |     |     |
| 0x467  | Restore Relay Offline             |     |     |
| 0x468  | Relay Low Battery                 |     |     |
| 0x469  | Relay Low Battery Restored        |     |     |
| 0x46a  | Lock Extremely Low Battery        |     |     |
Access Control: Custom Exception Event 1 to Custom Exception
0x900 to 0x93f
Event 64

<!-- page: 8 -->

Value  Description
| 0x950  | Switch to Wired Network     |     |
| ------ | --------------------------- | --- |
| 0x951  | Switch to Wireless Network  |     |
| 0x952  | Restore Smart Lock Offline  |     |
| 0x953  | USB Camera Online           |     |
| 0x954  | USB Camera Offline          |     |
0x955  Communication Exception Occurred During Distributed Controller
Backup
| 0x956  | Social Security Card Reader Online      |     |
| ------ | --------------------------------------- | --- |
| 0x957  | Social Security Card Reader Offline     |     |
| 0x958  | Turnstile Infrared Component Exception  |     |
z
| 0x959  | Turnstile Infrared Running Exception  |     |
| ------ | ------------------------------------- | --- |
k
| 0x95a  | Turnstile Infrared Detection Exception  | .   |
| ------ | --------------------------------------- | --- |
a
0x95b  No Calibration Target in Turnstile Infrared Detection
t
0x95c  Incorrect Calibration Distance from Turnstile Infrared Target
h
0x95d  Channel Width Not Applied to Turn@stile Infrared Detector
n
| 0x95e  | Lock Control Board Online  |     |
| ------ | -------------------------- | --- |
i
| 0x95f  | Lock Control Board Offline  |     |
| ------ | --------------------------- | --- |
k
   i
u
Operation Events (0x3)
h
c
  .
y A
Value  TDescription
i
H
| 0x41  | Startup  l |     |
| ----- | ---------- | --- |
i
| 0x42  | Shutdown  |     |
| ----- | --------- | --- |
s
| 0x43  | Shautdown Exception  |     |
| ----- | -------------------- | --- |
vLocal: Device Restart
0x44
| 0x50  | Local Login                       |     |
| ----- | --------------------------------- | --- |
| 0x51  | Local Logout                      |     |
| 0x52  | Local: Configuration              |     |
| 0x53  | Local: Playback/Download by File  |     |
| 0x54  | Local: Playback/Download by Time  |     |
| 0x55  | Local: Start Recording            |     |
| 0x56  | Local: Stop Recording             |     |
| 0x59  | Local: Edit Time                  |     |
| 0x5a  | Local Upgrade                     |     |
| 0x5b  | Local: Back Up Recording File(s)  |     |
| 0x5c  | Local: Initialize HDD             |     |
| 0x5d  | Local: Export Configuration File  |     |
| 0x5e  | Local: Import Configuration File  |     |

<!-- page: 9 -->

| Value  |                                           |     | Description  |     |
| ------ | ----------------------------------------- | --- | ------------ | --- |
| 0x5f   | Local: Back Up Files                      |     |              |     |
| 0x60   | Local: Lock Recording Files               |     |              |     |
| 0x61   | Local: Unlock Recording Files             |     |              |     |
| 0x62   | Local: Manually Clear and Trigger Alarms  |     |              |     |
| 0x66   | Local: Start Backup                       |     |              |     |
| 0x67   | Local: Stop Backup                        |     |              |     |
| 0x68   | Local: Start Time of Backup               |     |              |     |
| 0x69   | Local: End Time of Backup                 |     |              |     |
| 0x6d   | Local: Restore Admin's Default Password   |     |              |     |
| 0x70   | Remote Login                              |     |              | z   |
k
| 0x71  | Remote Logout  |     |     |     |
| ----- | -------------- | --- | --- | --- |
.
a
| 0x72  | Remote: Start Recording  |     |     |     |
| ----- | ------------------------ | --- | --- | --- |
t
| 0x73  | Remote: Stop Recording  |     |     |     |
| ----- | ----------------------- | --- | --- | --- |
h
| 0x74  | Start Transparent Transmission  |     | @   |     |
| ----- | ------------------------------- | --- | --- | --- |
n
| 0x75  | Stop Transparent Transmission  |     |     |     |
| ----- | ------------------------------ | --- | --- | --- |
i
| 0x76  | Remote: Get Parameters  |     |     |     |
| ----- | ----------------------- | --- | --- | --- |
k
| 0x77  | Remote: Configure Paramieters  |     |     |     |
| ----- | ------------------------------ | --- | --- | --- |
u
| 0x78  | Remote: Get Status  |     |     |     |
| ----- | ------------------- | --- | --- | --- |
h
| 0x79  | Remote Arming  |     |     |     |
| ----- | -------------- | --- | --- | --- |
c
.
| 0x7a  | Remote Disarm | y ing  | A   |     |
| ----- | ------------- | ------ | --- | --- |
T
i
| 0x7b  | Remote Reboot  | H   |     |     |
| ----- | -------------- | --- | --- | --- |
l
| 0x7c  | Start Twio-Way Audio  |     |     |     |
| ----- | --------------------- | --- | --- | --- |
s
| 0x7d  | Stop Two-Way Audio  |     |     |     |
| ----- | ------------------- | --- | --- | --- |
a
| 0x7e  | vRemote Upgrade                              |     |     |     |
| ----- | -------------------------------------------- | --- | --- | --- |
| 0x7f  | Remote: Playback/Download by File            |     |     |     |
| 0x80  | Remote: Playback/Download by Time            |     |     |     |
| 0x83  | Remote: Shutdown                             |     |     |     |
| 0x84  | Remote: Lock File                            |     |     |     |
| 0x85  | Remote: Unlock File                          |     |     |     |
| 0x86  | Remote Operation: Export Configuration File  |     |     |     |
| 0x87  | Remote Operation: Import Configuration File  |     |     |     |
| 0x88  | Remote: Export Recording Files               |     |     |     |
| 0x89  | Remote: Manually Clear and Trigger Alarms    |     |     |     |
| 0x8a  | Remote: Add Network Camera                   |     |     |     |
| 0x8b  | Remote: Delete Network Camera                |     |     |     |
| 0x8c  | Remote: Set Network Camera                   |     |     |     |

<!-- page: 10 -->

Value  Description
| 0x9a  | Remote: Delete Exceptional HDD                   |     |
| ----- | ------------------------------------------------ | --- |
| 0x9b  | Remote: Load HDD                                 |     |
| 0x9c  | Remote: Uninstall HDD                            |     |
| 0x9d  | Local: Lock                                      |     |
| 0x9e  | Local: Unlock                                    |     |
| 0xd6  | Remote Operation: Enable Alarm Output Manually   |     |
| 0xd7  | Remote Operation: Disable Alarm Output Manually  |     |
z
| 0x137  | Remote: Lock Login  |     |
| ------ | ------------------- | --- |
k
| 0x138  | Remote: Unlock Login  |     |
| ------ | --------------------- | --- |
.
| 0x200  | Other Operations  | a   |
| ------ | ----------------- | --- |
t
| 0x400  | Door Remotely Open  |     |
| ------ | ------------------- | --- |
h
@
| 0x401  | Door Remotely Closed  |     |
| ------ | --------------------- | --- |
n
i
| 0x402  | Remain Open Remotely  |     |
| ------ | --------------------- | --- |
k
i
| 0x403  | Remain Closed Remotely  |     |
| ------ | ----------------------- | --- |
u
| 0x404  | Remote: Manual Timhe Sync  |     |
| ------ | -------------------------- | --- |
c
| 0x405  | Network Time Pr.otocol Synchronization  |     |
| ------ | --------------------------------------- | --- |
y A
| 0x406  | Remote Opeiration: ClearT All Card No.  |     |
| ------ | --------------------------------------- | --- |
H
l
| 0x407  | Remotei Operation: Restore Defaults  |     |
| ------ | ------------------------------------ | --- |
s
| 0x408  | Zone Arming  |     |
| ------ | ------------ | --- |
a
v
| 0x409  | Zone Disarming                     |     |
| ------ | ---------------------------------- | --- |
| 0x40a  | Local Operation: Restore Defaults  |     |
| 0x40b  | Remote Operation: Capture          |     |
| 0x40c  | Edit Network Parameters            |     |
| 0x40d  | Edit GPRS Parameters               |     |
| 0x40e  | Edit Control Center Parameters     |     |
| 0x40f  | Enter Dismiss Code                 |     |
| 0x410  | Auto Renumber                      |     |
| 0x411  | Auto Supplement Number             |     |
| 0x412  | Import Configuration File          |     |
| 0x413  | Export Configuration File          |     |

<!-- page: 11 -->

Value  Description
| 0x414  | Import Card Permission Parameters   |     |
| ------ | ----------------------------------- | --- |
| 0x415  | Export Card Permission Parameters   |     |
| 0x416  | Upgrade Device via USB Flash Drive  |     |
| 0x417  | Visitor Calling Elevator            |     |
| 0x418  | Resident Calling Elevator           |     |
| 0x419  | Remotely Arming                     |     |
| 0x41a  | Remotely Disarming                  |     |
z
| 0x41b  | Operation Failed: Keyfob Not Pairing  |     |
| ------ | ------------------------------------- | --- |
k
.
| 0x41c  | Keyfob Operation: Close Door  |     |
| ------ | ----------------------------- | --- |
a
t
| 0x41d  | Keyfob Operation: Open Door  |     |
| ------ | ---------------------------- | --- |
h
@
| 0x41e  | Keyfob Operation: Remain Door Open  |     |
| ------ | ----------------------------------- | --- |
n
| 0x41f  | M1 Card Encryption Verificatioin Enabled  |     |
| ------ | ----------------------------------------- | --- |
k
| 0x420  | M1 Card Encryption Verifiication Disabled  |     |
| ------ | ------------------------------------------ | --- |
u
| 0x421  | Opening Door with NhFC Card Enabled  |     |
| ------ | ------------------------------------ | --- |
c
| 0x422  | Opening Door w.ith NFC Card Disabled  |     |
| ------ | ------------------------------------- | --- |
y A
| 0x423  | Export Offlin | e Collected TData  |
| ------ | ------------- | ------------------ |
i
H
l
| 0x42d  | Establish SSH Connection  |     |
| ------ | ------------------------- | --- |
i
s
| 0x42e  | Disconnect SSH Connection  |     |
| ------ | -------------------------- | --- |
a
| 0x42f  | vLocal: Import Person Data   |     |
| ------ | ---------------------------- | --- |
| 0x430  | Local: Export Person Data    |     |
| 0x431  | Create Certificate           |     |
| 0x432  | Upload Certificate           |     |
| 0x433  | Delete Certificate           |     |
| 0x434  | Consumption Armed            |     |
| 0x435  | Consumption Disarmed         |     |
| 0x436  | Change QR Code Secret Key    |     |
| 0x437  | Remote: Upgrade Lock         |     |
| 0x438  | Remote: Upgrade Card Reader  |     |
| 0x439  | Remote: Upgrade Exit Button  |     |
| 0x43a  | Remote: Upgrade Doorbell     |     |
| 0x43b  | AP Mode Switch               |     |
| 0x43c  | Enable Registration Mode     |     |
| 0x43d  | Card Reader Added            |     |
| 0x43e  | Lock Added                   |     |

<!-- page: 12 -->

| Value  |                    | Description  |     |
| ------ | ------------------ | ------------ | --- |
| 0x43f  | Doorbell Added     |              |     |
| 0x440  | Exit Button Added  |              |     |
0x441  Delete Card Reader (Unbound from Security Control Panel)
0x442  Delete Door Lock (Unbound from Security Control Panel)
0x443  Delete Doorbell (Unbound from Security Control Panel)
0x444  Delete Exit Button (Unbound from Security Control Panel)
| 0x445  | Enable Card Swiping on Card Reader   |     |     |
| ------ | ------------------------------------ | --- | --- |
| 0x446  | Disable Swiping Card on Card Reader  |     |     |
| 0x447  | Enable Card Reader Button            |     |     |
| 0x448  | Disable Card Reader Button           |     |     |
z
| 0x449  | Enable Card Reader Proximity Sensor  |     |     |
| ------ | ------------------------------------ | --- | --- |
k
| 0x44a  | Disable Card Reader Proximity Sensor  |     | .   |
| ------ | ------------------------------------- | --- | --- |
a
| 0x44b  | Enable Card Reader Buzzer  |     |     |
| ------ | -------------------------- | --- | --- |
t
| 0x44c  | Disable Card Reader Buzzer  |     |     |
| ------ | --------------------------- | --- | --- |
h
| 0x44d  | Enable Card Reader Bluetooth  |     | @   |
| ------ | ----------------------------- | --- | --- |
n
| 0x44e  | Disable Card Reader Bluetooth  |     |     |
| ------ | ------------------------------ | --- | --- |
i
| 0x44f  | Remote: Upgrade Relay  |     |     |
| ------ | ---------------------- | --- | --- |
k
| 0x450  | Relay Added  | i   |     |
| ------ | ------------ | --- | --- |
u
| 0x451  | Delete Relay  |     |     |
| ------ | ------------- | --- | --- |
h
Access Control: Cucstom Operation Event 1 to Custom Operation
0x900-0x93f
.
Event 64
y A
T
| 0x940  | Live Broadcaist  |     |     |
| ------ | ---------------- | --- | --- |
H
l
| 0x941  | Scheduled Broadcast  |     |     |
| ------ | -------------------- | --- | --- |
i
| 0x942  | Local: Import Cuisine Data  s |     |     |
| ------ | ----------------------------- | --- | --- |
| 0x943  | Loacal: Export Cuisine Data   |     |     |
v
| 0x950  | Set Wi-Fi Parameters                      |     |     |
| ------ | ----------------------------------------- | --- | --- |
| 0x951  | Log In to Cloud Service                   |     |     |
| 0x952  | Log Out from Cloud Service                |     |     |
| 0x953  | Add Smart Lock                            |     |     |
| 0x954  | Delete Smart Lock                         |     |     |
| 0x955  | Get Smart Lock Status                     |     |     |
| 0x956  | Apply Temporary Password of Smart Lock    |     |     |
| 0x957  | Set Smart Lock Mute Parameters            |     |     |
| 0x958  | Set Smart Lock Late-Return Notifications  |     |     |
| 0x959  | Link Smart Lock with Network Camera       |     |     |
| 0x95a  | Unlink Smart Lock with Network Camera     |     |     |
| 0x95b  | Link Smart Lock with Detector             |     |     |
| 0x95c  | Unlink Smart Lock with Detector           |     |     |
| 0x95d  | Enable Smart Lock Message Notification    |     |     |
| 0x95e  | Disable Smart Lock Message Notification   |     |     |
| 0x95f  | Set Smart Lock Heartbeat                  |     |     |

<!-- page: 13 -->

| Value  |                                       | Description  |     |     |     |
| ------ | ------------------------------------- | ------------ | --- | --- | --- |
| 0x960  | Reboot Smart Lock                     |              |     |     |     |
| 0x961  | Clear Users of Smart Lock             |              |     |     |     |
| 0x962  | Format Smart Lock                     |              |     |     |     |
| 0x963  | Change Smart Lock Fingerprint         |              |     |     |     |
| 0x964  | Change Smart Lock Password            |              |     |     |     |
| 0x965  | Change Smart Lock Card Information    |              |     |     |     |
| 0x966  | Change Smart Lock User Information    |              |     |     |     |
| 0x967  | Change Smart Lock System Information  |              |     |     |     |
| 0x968  | Add User to Smart Lock                |              |     |     |     |
| 0x969  | Delete User from Smart Lock           |              |     |     |     |
z
| 0x96a  | Change Username of Smart Lock's Custom Usekr  |     |     |     |     |
| ------ | --------------------------------------------- | --- | --- | --- | --- |
| 0x96b  | Change Smart Lock Keyfob Information          |     |     | .   |     |
a
| 0x96c  | Add Fingerprint to Smart Lock  |     |     |     |     |
| ------ | ------------------------------ | --- | --- | --- | --- |
t
| 0x96d  | Delete Fingerprint from Smart Lock  |     |     |     |     |
| ------ | ----------------------------------- | --- | --- | --- | --- |
h
| 0x96e  | Add Password to Smart Lock  |     | @   |     |     |
| ------ | --------------------------- | --- | --- | --- | --- |
n
| 0x96f  | Delete Password from Smart Lock  |     |     |     |     |
| ------ | -------------------------------- | --- | --- | --- | --- |
i
| 0x970  | Add Card to Smart Lock  |     |     |     |     |
| ------ | ----------------------- | --- | --- | --- | --- |
k
| 0x971  | Delete Card from Smart Loick  |     |     |     |     |
| ------ | ----------------------------- | --- | --- | --- | --- |
u
| 0x972  | Change Smart Lock Network Status  |     |     |     |     |
| ------ | --------------------------------- | --- | --- | --- | --- |
h
| 0x973  | Clear Smart Lock Ncetwork Data  |     |     |     |     |
| ------ | ------------------------------- | --- | --- | --- | --- |
| 0x974  | Clear Smart Lock. Hosts         |     |     |     |     |
y A
| 0x975  | Clear Smart Lock Guests  |     |     |     |     |
| ------ | ------------------------ | --- | --- | --- | --- |
T
i
| 0x976  | Clear Keylfob User InfoHrmation                  |     |     |     |     |
| ------ | ------------------------------------------------ | --- | --- | --- | --- |
| 0x977  | Clear Niormal Users' Fingerprints on Smart Lock  |     |     |     |     |
s
| 0x978  | Clear All Cards on Smart Lock  |     |     |     |     |
| ------ | ------------------------------ | --- | --- | --- | --- |
a
| 0x979   | vClear All Smart Lock Passwords                   |     |     |     |     |
| ------- | ------------------------------------------------- | --- | --- | --- | --- |
| 0x97a   | Enable Device Hotspot                             |     |     |     |     |
| 0x97b   | Disable Device Hotspot                            |     |     |     |     |
| 0x97c   | Authorize Panic Management Card to Normal Card    |     |     |     |     |
| 0x97d   | Change Channel Mode                               |     |     |     |     |
| 0x97e   | Doorbell Event (Triggered by Lock Operation)      |     |     |     |     |
| 0x97f   | Access Module Restarts                            |     |     |     |     |
| 0x980   | Restore Access Module Parameters                  |     |     |     |     |
| 0x981   | Local: Restore Default Parameters of AP Password  |     |     |     |     |
| 0xf0    | Local: Activate Device                            |     |     |     |     |
| 0xf1    | Remote: Activate Device                           |     |     |     |     |
| 0xf2    | Local: Restore Default Settings                   |     |     |     |     |
| 0xf3    | Remote: Restore Default Settings                  |     |     |     |     |
| 0x2600  | Local: Reset Admin Login Password                 |     |     |     |     |
| 0x2601  | Remote: Reset Admin Login Password                |     |     |     |     |

<!-- page: 14 -->

Additional Information (0x4)
| Value  |                                    | Description  |     |
| ------ | ---------------------------------- | ------------ | --- |
| 0xa1   | HDD information                    |              |     |
| 0xaa   | System Running Status Information  |              |     |
| 0xbd   | Global Error Information           |              |     |
| 0xbe   | Buffer Status Log                  |              |     |
| 0xbf   | HDD Error Detailed Information     |              |     |
| 0xc0   | Cloud Storage Data Expired         |              |     |
| 0xc1   | Platform Information               |              |     |
| 0xc2   | Dial-Up Status                     |              |     |
z
| 0xc3  | Unlocking Log  |     |     |
| ----- | -------------- | --- | --- |
k
| 0xc4  | Zone Alarm  |     | .   |
| ----- | ----------- | --- | --- |
a
| 0xc5  | Call Log  |     |     |
| ----- | --------- | --- | --- |
t
| 0xc6  | Accessory Board Information  |     |     |
| ----- | ---------------------------- | --- | --- |
h
| 0xc9  | Smart Board Status  | @   |     |
| ----- | ------------------- | --- | --- |
n
| 0xcb  | Auto Time Sync  |     |     |
| ----- | --------------- | --- | --- |
i
| 0xcc  | Cloud Service Running Status  |     |     |
| ----- | ----------------------------- | --- | --- |
k
| 0xd8  | Formatting HDD Starts i |     |     |
| ----- | ----------------------- | --- | --- |
u
| 0xd9  | Formatting HDD Stops  |     |     |
| ----- | --------------------- | --- | --- |
h
| 0x400  | Enable Live Facial Detection  |     |     |
| ------ | ----------------------------- | --- | --- |
c
| 0x401  | Disable Live Fa.cial Detection  |     |     |
| ------ | ------------------------------- | --- | --- |
y A
| 0x402  | Clear Collected Data  |     |     |
| ------ | --------------------- | --- | --- |
T
i
| 0x403  | Delete  Collected DaHta  |     |     |
| ------ | ------------------------ | --- | --- |
l
| 0x404  | Expoirt Collected Data  |     |     |
| ------ | ----------------------- | --- | --- |
s
| 0x405  | Set Card Length  |     |     |
| ------ | ---------------- | --- | --- |
a
| 0x406  | Initializing Database Failed  |     |     |
| ------ | ----------------------------- | --- | --- |
v
| 0x407  | Upgrade Database Patch                      |     |     |
| ------ | ------------------------------------------- | --- | --- |
| 0x408  | Insert Psam Card                            |     |     |
| 0x409  | Pull out Psam Card                          |     |     |
| 0x40a  | Hardware Restarts Unexpectedly (hardFault)  |     |     |
| 0x40b  | Psam Card Overcurrent Protection            |     |     |
| 0x40c  | Stack Overflow                              |     |     |
| 0x40d  | Configure Parameters                        |     |     |
| 0x40e  | Clear All Users                             |     |     |
| 0x40f  | Clear All Cards                             |     |     |
| 0x410  | Clear All Fingerprints by Card Reader       |     |     |
| 0x411  | Clear All Fingerprints by Card No.          |     |     |
| 0x412  | Clear All Fingerprints by Employee ID       |     |     |
| 0x413  | Delete a Fingerprint                        |     |     |
| 0x414  | Clear All Weekly Permission Schedules       |     |     |
| 0x415  | Set Weekly Permission Schedule              |     |     |

<!-- page: 15 -->

| 0x416  | Set Holiday Permission Schedule               |     |     |
| ------ | --------------------------------------------- | --- | --- |
| 0x417  | Clear All Holiday Permission Schedules        |     |     |
| 0x418  | Set Holiday Group Permission Schedule         |     |     |
| 0x419  | Clear All Holiday Group Permission Schedules  |     |     |
| 0x41a  | Clear All Permission Schedules                |     |     |
| 0x41b  | Set Permission Schedule                       |     |     |
| 0x41c  | Add Card                                      |     |     |
| 0x41d  | Edit Card                                     |     |     |
| 0x41e  | Add Fingerprint by Card No.                   |     |     |
| 0x41f  | Add Fingerprint by Employee ID                |     |     |
| 0x420  | Edit Fingerprint by card No.                  |     |     |
z
| 0x421  | Edit Fingerprint by Employee ID  |     |     |
| ------ | -------------------------------- | --- | --- |
k
| 0x422  | Import User List (Collected Offline)  |     |     |
| ------ | ------------------------------------- | --- | --- |
.
| 0x423  | USB Login  |     | a   |
| ------ | ---------- | --- | --- |
t
| 0x424  | USB Logout  |     |     |
| ------ | ----------- | --- | --- |
h
| 0x425  | ISAPI and HTTP Login  |     |     |
| ------ | --------------------- | --- | --- |
@
| 0x426  | ISAPI and HTTP Logout  |     | n   |
| ------ | ---------------------- | --- | --- |
| 0x427  | ISAPI and HTTPS Login  |     | i   |
k
| 0x428  | ISAPI and HTTPS Logout  |     |     |
| ------ | ----------------------- | --- | --- |
i
| 0x429  | ISUP Online   | u   |     |
| ------ | ------------- | --- | --- |
| 0x42a  | ISUP Offline  | h   |     |
c
| 0x42b  | Fingerprint Card Issuing Records  |     |     |
| ------ | --------------------------------- | --- | --- |
.
| 0x42c  | Face Picturey Card IssuingA Records  |     |     |
| ------ | ------------------------------------ | --- | --- |
T
| 0x42d  | Add Iris  i |     |     |
| ------ | ----------- | --- | --- |
H
l
| 0x42e  | Edit Iris  |     |     |
| ------ | ---------- | --- | --- |
i
| 0x42f  | Deslete Users' Irises (By Employee ID)  |     |     |
| ------ | --------------------------------------- | --- | --- |
| 0x430  | a Delete All Irises                     |     |     |
v
| 0x431  | Edit Iris Parameters                        |     |     |
| ------ | ------------------------------------------- | --- | --- |
| 0x432  | Add Person Information                      |     |     |
| 0x433  | Edit Person Information                     |     |     |
| 0x434  | Delete Person Information (by Employee ID)  |     |     |
| 0x435  | Delete Card by Card No. or Employee ID      |     |     |
| 0x436  | Delete All Cards                            |     |     |
| 0x437  | SIM Card Inserted                           |     |     |
| 0x438  | SIM Card Unplugged                          |     |     |
| 0x439  | Enable Fingerprint Recognition              |     |     |
| 0x43a  | Disable Fingerprint Recognition             |     |     |
| 0x43b  | Enable Face Capture                         |     |     |
| 0x43c  | Disable Face Capture                        |     |     |
| 0x43d  | Reset Online Card Reader                    |     |     |
| 0x43e  | Clear Registered Iris Pictures              |     |     |
| 0x43f  | Add Voiceprint                              |     |     |

<!-- page: 16 -->

| 0x440  | Edit Voiceprint                                |     |     |
| ------ | ---------------------------------------------- | --- | --- |
| 0x441  | Delete Voiceprint                              |     |     |
| 0x442  | Delete All Voiceprints                         |     |     |
| 0x443  | Face Picture Data Library Upgrade Log Records  |     |     |

Other Events (0x5)
Value  Description
| 0x01  | Valid Card Authentication Completed         |     |     |
| ----- | ------------------------------------------- | --- | --- |
| 0x02  | Card and Password Authentication Completed  |     | z   |
k
| 0x03  | Card and Password Authentication Failed  |     |     |
| ----- | ---------------------------------------- | --- | --- |
.
a
| 0x04  | Card and Password Authentication Timed Out  |     |     |
| ----- | ------------------------------------------- | --- | --- |
t
h
| 0x05  | Card and Password Authentication Timed Out  |     |     |
| ----- | ------------------------------------------- | --- | --- |
@
n
| 0x06  | No Permission  |     |     |
| ----- | -------------- | --- | --- |
i
| 0x07  | Invalid Card Swiping Time Pkeriod  |     |     |
| ----- | ---------------------------------- | --- | --- |
i
| 0x08  | Expired Card  | u   |     |
| ----- | ------------- | --- | --- |
h
| 0x09  | Card No. Not Existc  |     |     |
| ----- | -------------------- | --- | --- |
.
| 0x0a  | Anti-passing B | y ack AuthentAication Failed  |     |
| ----- | -------------- | ----------------------------- | --- |
T
i
| 0x0b  | Interlock ing Door NotH Closed  |     |     |
| ----- | ------------------------------- | --- | --- |
l
i
| 0x0c  | Card Not in Multiple Authentication Group  |     |     |
| ----- | ------------------------------------------ | --- | --- |
s
| 0x0d  | Card Not in Multiple Authentication Duration  a |     |     |
| ----- | ----------------------------------------------- | --- | --- |
v
0x0e  Multiple Authentications: Super Password Authentication Failed
| 0x0f  | Multiple Authentication Completed  |     |     |
| ----- | ---------------------------------- | --- | --- |
| 0x10  | Multiple Authenticated             |     |     |
| 0x11  | Open Door with First Card Started  |     |     |
| 0x12  | Open Door with First Card Stopped  |     |     |
| 0x13  | Remain Open Started                |     |     |
| 0x14  | Remain Open Stopped                |     |     |
| 0x15  | Door Unlocked                      |     |     |
| 0x16  | Door Locked                        |     |     |
| 0x17  | Exit Button Pressed                |     |     |
| 0x18  | Exit Button Released               |     |     |

<!-- page: 17 -->

0x19

0x1a

0x1b

0x1c

0x1d

0x1e

0x1f

0x20

0x21

0x22

0x23

0x24

0x25

0x26

0x27

0x28

0x29

0x2a

0x2b

0x2c

0x2d

0x2e

0x2f

0x30

0x31

0x32

0x33

0x34

0x35

0x36

Door Open (Contact)

Door Closed (Contact)

Door Abnormally Open (Contact)

Door Open Timed Out (Contact)

Alarm Output Enabled

Alarm Output Disabled

Remain Closed Started

Remain Closed Stopped

Doorbell Ring

Fingerprint Matched

Multiple Authentications Timed Out

Multiple Authentications: Remotely Open Door

Multiple Authentications: Repeated Authentication

Multiple Authentications: Super Password Authentication
Completed

vasiliy.chuikin@hta.kz

Card and Fingerprint and Password Authentication Failed

HTA

Card and Fingerprint Authentication Completed

Card and Fingerprint Authentication Timed Out

Card and Fingerprint Authentication Failed

Fingerprint Mismatched

Card and Fingerprint and Password Authentication Completed

Card and Fingerprint and Password Authentication Timed Out

Fingerprint and Password Authentication Completed

Fingerprint and Password Authentication Failed

Fingerprint and Password Authentication Timed Out

Fingerprint Not Exists

Card Platform Authentication

Call Center

Fire Relay Closed: Door Remains Open

Fire Relay Opened: Door Remains Closed

Access Granted by Face and Fingerprint



<!-- page: 18 -->

| 0x37  | Access Denied by Face and Fingerprint           |     |     |
| ----- | ----------------------------------------------- | --- | --- |
| 0x38  | Access Timed Out by Face and Fingerprint        |     |     |
| 0x39  | Access Granted by Face and PIN                  |     |     |
| 0x3a  | Access Denied by Face and PIN                   |     |     |
| 0x3b  | Access Timed Out by Face and PIN                |     |     |
| 0x3c  | Access Granted by Face and Card                 |     |     |
| 0x3d  | Access Denied by Face and Card                  |     |     |
| 0x3e  | Access Timed Out by Face and Card               |     |     |
| 0x3f  | Access Granted by Face, PIN, and Fingerprint    |     |     |
| 0x40  | Access Denied by Face, PIN, and Fingerprint     |     |     |
| 0x41  | Access Timed Out by Face, PIN, and Fingerprint  |     |     |
z
| 0x42  | Access Granted by Face, Card, and Fingerprint  |     |     |
| ----- | ---------------------------------------------- | --- | --- |
k
| 0x43  | Access Denied by Face, Card, and Fingerprint  |     |     |
| ----- | --------------------------------------------- | --- | --- |
.
| 0x44  | Access Timed Out by Face, Card, and Fingearprint  |     |     |
| ----- | ------------------------------------------------- | --- | --- |
t
| 0x45  | Employee ID and Fingerprint Authentication Completed  |     |     |
| ----- | ----------------------------------------------------- | --- | --- |
h
@
| 0x46  | Employee ID and Fingerprint Authentication Failed  |     |     |
| ----- | -------------------------------------------------- | --- | --- |
n
| 0x47  | Employee ID and Fingerprint Aiuthentication Timed Out  |     |     |
| ----- | ------------------------------------------------------ | --- | --- |
k
Employee ID and Fingerpriint and Password Authentication
| 0x48  |     | u   |     |
| ----- | --- | --- | --- |
Completed
h
| 0x49  | Employee ID and Fingerprint and Password Authentication Failed  | c   |     |
| ----- | --------------------------------------------------------------- | --- | --- |
.
|     | Employee ID aynd Fingerpri | A   |     |
| --- | -------------------------- | --- | --- |
nt and Password Authentication Timed
| 0x4a  |     | T   |     |
| ----- | --- | --- | --- |
i
|     | Out  | H   |     |
| --- | ---- | --- | --- |
l
i
| 0x4b  | Face Authentication Completed  |     |     |
| ----- | ------------------------------ | --- | --- |
s
| 0x4c  | Faace Authentication Failed  |     |     |
| ----- | ---------------------------- | --- | --- |
v
| 0x4d  | Employee ID and Face Authentication Completed  |     |     |
| ----- | ---------------------------------------------- | --- | --- |
| 0x4e  | Employee ID and Face Authentication Failed     |     |     |
| 0x4f  | Employee ID and Face Authentication Timed Out  |     |     |
| 0x50  | Face Recognition Failed                        |     |     |
| 0x51  | First Card Authorization Started               |     |     |
| 0x52  | First Card Authorization Ended                 |     |     |
| 0x53  | Lock Input Short Circuit Attempts Alarm        |     |     |
| 0x54  | Lock Input Open Circuit Attempts Alarm         |     |     |
| 0x55  | Lock Input Exception Alarm                     |     |     |
| 0x56  | Contact Input Short Circuit Attempts Alarm     |     |     |
| 0x57  | Contact Input Open Circuit Attempts Alarm      |     |     |

<!-- page: 19 -->

| 0x58  | Contact Input Exception Alarm                   |     |     |
| ----- | ----------------------------------------------- | --- | --- |
| 0x59  | Exit Button Input Short Circuit Attempts Alarm  |     |     |
| 0x5a  | Exit Button Input Open Circuit Attempts Alarm   |     |     |
| 0x5b  | Exit Button Input Exception Alarm               |     |     |
| 0x5c  | Unlocking Exception                             |     |     |
| 0x5d  | Unlocking Timed Out                             |     |     |
| 0x5e  | Unauthorized First Card Opening Failed          |     |     |
| 0x5f  | Call Elevator Relay Open                        |     |     |
z
| 0x60  | Call Elevator Relay Closed  |     |     |
| ----- | --------------------------- | --- | --- |
k
.
| 0x61  | Auto Button Relay Open  |     |     |
| ----- | ----------------------- | --- | --- |
a
t
| 0x62  | Auto Button Relay Closed  |     |     |
| ----- | ------------------------- | --- | --- |
h
@
| 0x63  | Button Relay Open  |     |     |
| ----- | ------------------ | --- | --- |
n
| 0x64  | Button Relay Closed  |     | i   |
| ----- | -------------------- | --- | --- |
k
| 0x65  | Employee ID and Passworid Authentication Completed  |     |     |
| ----- | --------------------------------------------------- | --- | --- |
u
| 0x66  | Employee ID and Pashsword Authentication Failed  |     |     |
| ----- | ------------------------------------------------ | --- | --- |
c
| 0x67  | Employee ID and. Password Authentication Timed Out  |                 |     |
| ----- | --------------------------------------------------- | --------------- | --- |
|       |                                                     | y               | A   |
| 0x68  | Human Det                                           | ection FailedT  |     |
i
H
l
| 0x69  | Person and ID Card Matched  |     |     |
| ----- | --------------------------- | --- | --- |
i
s
| 0x70  | Person and ID Card Mismatched  |     |     |
| ----- | ------------------------------ | --- | --- |
a
vBlocklist Event
0x71
| 0x72  | Valid Message    |     |     |
| ----- | ---------------- | --- | --- |
| 0x73  | Invalid Message  |     |     |
Authentication Failed: Door Remain Closed or Door in Sleeping
0x75
Mode
0x76  Authentication Failed: Authentication Schedule in Sleeping Mode
| 0x77  | Card Encryption Verification Failed       |     |     |
| ----- | ----------------------------------------- | --- | --- |
| 0x78  | Anti-passing Back Server Response Failed  |     |     |
Open Door via Exit Button Failed When Door Remain Closed or in
0x82
Sleeping Mode
0x84  Door Linkage Open Failed During Door Remain Close or Sleeping
| 0x85  | Tailgating  |     |     |
| ----- | ----------- | --- | --- |

<!-- page: 20 -->

| 0x86  | Reverse Passing                          |     |     |
| ----- | ---------------------------------------- | --- | --- |
| 0x87  | Force Accessing                          |     |     |
| 0x88  | Climb Over                               |     |     |
| 0x89  | Passing Timed Out                        |     |     |
| 0x8a  | Intrusion Alarm                          |     |     |
| 0x8b  | Authentication Failed When Free Passing  |     |     |
| 0x8c  | Barrier Obstructed                       |     |     |
| 0x8d  | Barrier Restored                         |     |     |
z
| 0x8e  | Failed to Update Local Face Modeling by Device  |     |     |
| ----- | ----------------------------------------------- | --- | --- |
k
| 0x8f  | Overstay  |     |     |
| ----- | --------- | --- | --- |
.
| 0x90  | Allowlist Authentication Succeeded  |     | a   |
| ----- | ----------------------------------- | --- | --- |
t
| 0x91  | Authenticating Allowlist Failed  |     |     |
| ----- | -------------------------------- | --- | --- |
h
0x92  Face Picture Collecting Event (No A@uthentication, Uploaded
during Remote Verification)  n
i
0x93  Card Collecting Event (No Authentication, Uploaded during
k
Remote Verification)
i
0x94  Failed Attempts of Authuentication via Password Reached Limit
| 0x95  | ID Card Collecting Event (No Authentication, Uploaded during  | h   |     |
| ----- | ------------------------------------------------------------- | --- | --- |
c
Remote Verification)
.
| 0x96  | Authenticatioyn via PasswoArd Failed  |     |     |
| ----- | ------------------------------------- | --- | --- |
T
i
| 0x97  | Password s MismatcheHd  |     |     |
| ----- | ----------------------- | --- | --- |
l
i
| 0x98  | Employee ID Not Exists  |     |     |
| ----- | ----------------------- | --- | --- |
s
a
| 0x99  | Combined Authentication Completed  |     |     |
| ----- | ---------------------------------- | --- | --- |
v
| 0x9a  | Combined Authentication Timed Out       |     |     |
| ----- | --------------------------------------- | --- | --- |
| 0x9b  | Authentication Type Mismatched          |     |     |
| 0x9c  | Authenticated via QR Code               |     |     |
| 0x9d  | Authentication via QR Code Failed       |     |     |
| 0x9e  | Authenticated via Householder           |     |     |
| 0x9f  | Authenticated via Bluetooth             |     |     |
| 0xa0  | Authentication via Bluetooth Failed     |     |     |
| 0xa1  | Verifying Passport Failed               |     |     |
| 0xa2  | Authentication Failed: Invalid M1 Card  |     |     |
| 0xa3  | Verifying CPU Card Encryption Failed    |     |     |
| 0xa4  | Disabling NFC Verification Failed       |     |     |
| 0xa5  | LoRa Module Online                      |     |     |

<!-- page: 21 -->

| 0xa6  | LoRa Module Offline            |     |     |     |
| ----- | ------------------------------ | --- | --- | --- |
| 0xa7  | MQTT Connection Status         |     |     |     |
| 0xa8  | EM Card Recognition Disabled   |     |     |     |
| 0xa9  | M1 Card Recognition Disabled   |     |     |     |
| 0xaa  | CPU Card Recognition Disabled  |     |     |     |
| 0xab  | ID Card Recognition Disabled   |     |     |     |
| 0xac  | Importing Key to Card Failed   |     |     |     |
| 0xad  | Local Upgrade Failed           |     |     |     |
| 0xae  | Remote Upgrade Failed          |     |     | z   |
k
| 0xaf  | Extension Module is Remotely Upgraded  |     |     |     |
| ----- | -------------------------------------- | --- | --- | --- |
.
a
| 0xb0  | Upgrading Extension Module Remotely Failed  |     |     |     |
| ----- | ------------------------------------------- | --- | --- | --- |
t
| 0xb1  | Fingerprint Module is Remotely Upgrhaded  |     |     |     |
| ----- | ----------------------------------------- | --- | --- | --- |
@
Upgrading Fingerprint Module Rnemotely Failed
0xb2
i
| 0xb3  | Dynamic Verification Code Akuthenticated  |     |     |     |
| ----- | ----------------------------------------- | --- | --- | --- |
i
| 0xb4  | Authentication with Veurification Code Failed  |     |     |     |
| ----- | ---------------------------------------------- | --- | --- | --- |
h
| 0xb5  | Password Authenticated  |     |     |     |
| ----- | ----------------------- | --- | --- | --- |
c
.
| 0xb6  | Consumption Timed Out  |         |     |     |
| ----- | ---------------------- | ------- | --- | --- |
|       |                        | y       | A   |     |
| 0xb7  | Refund Tim             | ed Out  | T   |     |
i
Consumpltion AmountH Exceeded Limit
0xb8
i
| 0xb9  | Consumption Times Reached Limit  |     |     |     |
| ----- | -------------------------------- | --- | --- | --- |
s
| 0xba  | Consumption Confirmation Timed Out  |     |     |     |
| ----- | ----------------------------------- | --- | --- | --- |
a
| 0xbb  | vNumber of Blocklists Reached Limit                    |     |     |     |
| ----- | ------------------------------------------------------ | --- | --- | --- |
| 0xbc  | Verifying Desfire Card Encryption Failed               |     |     |     |
| 0xbd  | Desfire Card Reading Disabled                          |     |     |     |
| 0xbe  | Access Granted by Iris                                 |     |     |     |
| 0xbf  | Access Denied via Iris                                 |     |     |     |
| 0xc0  | Iris Anti-Spoofing Detection Failed                    |     |     |     |
| 0xc1  | Number of People Exceeds 90% of Capacity               |     |     |     |
| 0xc2  | Local Attendance Records Exceeded Limit                |     |     |     |
| 0xc3  | Authentication of Dynamic Authentication Code Expired  |     |     |     |
| 0xc4  | Meeting Not Checked In                                 |     |     |     |
| 0xc5  | Meeting Check-In                                       |     |     |     |
| 0xc6  | Meeting Late                                           |     |     |     |
| 0xc9  | Deleting Multi-Door Interlocking Failed                |     |     |     |
0xca  Authentication Failed: Fingerprint Recognition Not Enabled
| 0xcb  | Authentication Failed: Face Capture Disabled  |     |     |     |
| ----- | --------------------------------------------- | --- | --- | --- |

<!-- page: 22 -->

| 0xcc  | Open Door During Live View               |     |     |
| ----- | ---------------------------------------- | --- | --- |
| 0xcd  | Restore Card Reader to Factory Settings  |     |     |
| 0xce  | Card Reader ID Conflict                  |     |     |
| 0xcf  | FeliCa Card Recognition Disabled         |     |     |
0xd0  Authentication Failed Due to Abnormal Features (e.g., Not
Wearing Mask or Hard Hat, Abnormal Temperature)
| 0xd1  | Non Meeting Participant Check-In               |     |     |
| ----- | ---------------------------------------------- | --- | --- |
| 0xd2  | Meeting Participant Check-In In Vacant Status  |     |     |
| 0xd3  | Duplicate Check-In by Meeting Participant      |     |     |
| 0xd4  | Person Authentication Times Reached Limit      |     |     |
0xd5  Upgrading Face Modeling Failed Due to Incompatible Version
z
| 0xd6  | Upload Device Unlocking Record Event  |     |     |
| ----- | ------------------------------------- | --- | --- |
k
| 0xd7  | Door Not-Opened Alarm  |     |     |
| ----- | ---------------------- | --- | --- |
.
| 0xd8  | Door Not-Closed Alarm  |     | a   |
| ----- | ---------------------- | --- | --- |
t
| 0xd9  | Verifying QR Code Secret Key Failed  |     |     |
| ----- | ------------------------------------ | --- | --- |
h
| 0xda  | Passing Event  |     |     |
| ----- | -------------- | --- | --- |
@
| 0xdb  | Person and Social Security Card Mnatched     |     |     |
| ----- | -------------------------------------------- | --- | --- |
| 0xdc  | Person and Social Security Carid Mismatched  |     |     |
k
| 0xdd  | Wearing Mask  |     |     |
| ----- | ------------- | --- | --- |
i
| 0xdf  | Captured Picture Too Sumall  |     |     |
| ----- | ---------------------------- | --- | --- |
| 0xe0  | Access Module Upgrhaded      |     |     |
c
| 0xe1  | Upgrading Access Module Failed  |     |     |
| ----- | ------------------------------- | --- | --- |
.
| 0xe2  | Access Granteyd by EmployAee ID  |     |     |
| ----- | -------------------------------- | --- | --- |
T
| 0xe3  | Access Granited by NFC  |     |     |
| ----- | ----------------------- | --- | --- |
H
l
| 0xe4  | Access Denied by NFC  |     |     |
| ----- | --------------------- | --- | --- |
i
| 0xe5  | Unlosck by Public Password Event  |     |     |
| ----- | --------------------------------- | --- | --- |
| 0xe6  | Caard Reader Upgraded             |     |     |
v
| 0xe7  | Upgrading Card Reader Failed  |     |     |
| ----- | ----------------------------- | --- | --- |
0x500 to 0x53f  Access Control: Custom Event 1 to Custom Event 64
| 0x540  | Electrostatic Discharge Testing Passed  |     |     |
| ------ | --------------------------------------- | --- | --- |
0x541  Electrostatic Discharge Testing Not Passed (Door Not Opened)
0x542  Electrostatic Discharge Testing Not Passed (Door Opened)
| 0x543  | Electrostatic Discharge Testing Timed Out  |     |     |
| ------ | ------------------------------------------ | --- | --- |
| 0x544  | Remotely Import Person Data                |     |     |
| 0x545  | Remotely Export Person Data                |     |     |
| 0x600  | Smart Lock: Open Door with Fingerprint     |     |     |
| 0x601  | Smart Lock: Open Door with Password        |     |     |
| 0x602  | Smart Lock: Open Door by Card Swiping      |     |     |
| 0x603  | Smart Lock: Open Door by Center            |     |     |
| 0x604  | Smart Lock: Open Door with App             |     |     |
| 0x605  | Smart Lock: Open Door with Key             |     |     |
| 0x606  | Smart Lock: Open Door with Keyfob          |     |     |

<!-- page: 23 -->

| 0x607  | Smart Lock: Open Door with Temporary Password         |     |     |     |
| ------ | ----------------------------------------------------- | --- | --- | --- |
| 0x608  | Smart Lock: Open Door by Bluetooth                    |     |     |     |
| 0x609  | Smart Lock: Open Door by Multi-Factor Authentication  |     |     |     |
| 0x700  | Voiceprint Anti-Spoofing Detection Failed             |     |     |     |
| 0x701  | Voiceprint Authentication Failed                      |     |     |     |
| 0x702  | Channel Upgrading                                     |     |     |     |
| 0x703  | Channel Learning                                      |     |     |     |
| 0x704  | Device Self-Testing                                   |     |     |     |
| 0x705  | Motor Self-Testing                                    |     |     |     |
| 0x706  | Barrier Angle Adjusting                               |     |     |     |
| 0x707  | Access Granted by Palmprint and Palm Veins            |     |     |     |
z
| 0x708  | Access Denied by Palmprint and Palm Veins  |     |     |     |
| ------ | ------------------------------------------ | --- | --- | --- |
k
0x709  Palmprint and Palm Veins Anti-Spoofing Detection Failed
.
| 0x800  | Security Area Is Not Clear  |     |     | a   |
| ------ | --------------------------- | --- | --- | --- |
t
| 0x801  | Anti-Pinch area Is Not Clear  |     |     |     |
| ------ | ----------------------------- | --- | --- | --- |
h
| 0x802  | Motor Brake Is Operating  |     |     |     |
| ------ | ------------------------- | --- | --- | --- |
@
| 0x803  | Infrared Self-Test Failed  |     | n   |     |
| ------ | -------------------------- | --- | --- | --- |
| 0x804  | Motor Studying Failed      |     | i   |     |
k
| 0x805  | Do Not Open Barrier When Lane Is Not Clear  |     |     |     |
| ------ | ------------------------------------------- | --- | --- | --- |
i
| 0x806  | Exception Occurred In Muotor Drive Board  |     |     |     |
| ------ | ----------------------------------------- | --- | --- | --- |
| 0x807  | Exception Occurred Ihn Motor Encoder      |     |     |     |
c
| 0x808  | Motor Is Over Current  |     |     |     |
| ------ | ---------------------- | --- | --- | --- |
.
| 0x809  | Motor Is Overy Voltage  |     | A   |     |
| ------ | ----------------------- | --- | --- | --- |
T
| 0x80a  | Motor Is Under Voltage  | i   |     |     |
| ------ | ----------------------- | --- | --- | --- |
H
l
| 0x80b  | Exception Occurred In Motor  |     |     |     |
| ------ | ---------------------------- | --- | --- | --- |
i
| 0x80c  | Permsission Authentication Is Intercepted  |     |     |     |
| ------ | ------------------------------------------ | --- | --- | --- |
| 0x80d  | Access Granted by Keyfob  a                |     |     |     |
v
| 0x80e  | Access Denied via Keyfob                              |     |     |     |
| ------ | ----------------------------------------------------- | --- | --- | --- |
| 0x80f  | Invalid Face Recognition Angle                        |     |     |     |
| 0x810  | Secondary Authentication of Large Consumption Failed  |     |     |     |
| 0x811  | Secondary Authentication of Similar Consumer Failed   |     |     |     |
| 0x812  | Door Offline                                          |     |     |     |
| 0x813  | Door Interlocking Delaying                            |     |     |     |
| 0x814  | Passing Allowed (Door Not Used)                       |     |     |     |
0x815  Lock When Failed Attempts to Authenticate via Card No. Exceed
Limit
| 0x816  | Secure Door Control Unit Not Matched             |     |     |     |
| ------ | ------------------------------------------------ | --- | --- | --- |
| 0x817  | Exceptional IR Auto Shield                       |     |     |     |
| 0x818  | Auto-Restore Exceptional IR                      |     |     |     |
| 0x819  | Incorrect Cabinet User Type for Article Deposit  |     |     |     |

<!-- page: 24 -->

Event Linkage Types
For event card linkages, if the linkage type is event, four major event linkage types are available: 0-
device event linkage, 1-alarm input event linkage, 2-access control point (e.g., doors, elevators,
etc.) event linkage, and 3-authentication unit (e.g., card reader, fingerprint module, etc.) event
linkage. Each major event linkage type corresponds multiple minor types of event linkage, see
details in the following content.
Device Event Linkage
z
| Value  |     | Description  |
| ------ | --- | ------------ |
k
.
| 0   | Access Controller Tampering Alarm  |     |
| --- | ---------------------------------- | --- |
a
t
| 1   | No Memory Alarm  |     |
| --- | ---------------- | --- |
h
| 2   | Network Disconnected  | @   |
| --- | --------------------- | --- |
n
| 3   | Network Connected  |     |
| --- | ------------------ | --- |
i
k
| 4   | Low Battery Voltage  | i   |
| --- | -------------------- | --- |
u
| 5   | Battery Fully Charged  |     |
| --- | ---------------------- | --- |
h
c
| 6   | AC Power Off  |     |
| --- | ------------- | --- |
.
y A
| 7   | AC Power On  |     |
| --- | ------------ | --- |
T
i
H
l
| 8   | SD Card Full Alarm  |     |
| --- | ------------------- | --- |
i
Capture Lsinkage Event Alarm
9
a
| 10  | Low vFace Picture Quality                          |     |
| --- | -------------------------------------------------- | --- |
| 11  | Low Fingerprint Picture Quality                    |     |
| 12  | Low Battery Voltage                                |     |
| 13  | Battery Fully Charged                              |     |
| 14  | Fire Input Short Circuit Attempts Alarm            |     |
| 15  | Fire Input Open Circuit Attempts Alarm             |     |
| 16  | Fire Input Alarm Restored                          |     |
| 17  | RS485 Loop of Main Access Controller Disconnected  |     |
| 18  | RS485 Loop of Main Access Controller Connected     |     |
| 19  | Distributed Access Controller Offline              |     |
| 20  | Distributed Access Controller Online               |     |

<!-- page: 25 -->

| Value  |     |     | Description  |
| ------ | --- | --- | ------------ |
21  Downstream RS485 Loop of Distributed Access Control Disconnected
22  Downstream RS485 Loop of Distributed Access Control Connected
| 23  | Distributed Elevator Controller Online   |     |     |
| --- | ---------------------------------------- | --- | --- |
| 24  | Distributed Elevator Controller Offline  |     |     |
| 25  | Fire Button Pressed                      |     |     |
| 26  | Fire Button Released                     |     |     |
| 27  | Maintenance Button Pressed               |     |     |
z
| 28  | Maintenance Button Released  |     |     |
| --- | ---------------------------- | --- | --- |
k
.
| 29  | Panic Button Pressed  |     |     |
| --- | --------------------- | --- | --- |
a
t
| 30  | Panic Button Released  |     |     |
| --- | ---------------------- | --- | --- |
h
@
| 32  | Communication with Anti-passing Back Server Failed  |     |     |
| --- | --------------------------------------------------- | --- | --- |
n
| 33  | Communication with Anti-passing Biack Server Restored  |     |     |
| --- | ------------------------------------------------------ | --- | --- |
k
| 34  | Remotely Armed  |     | i   |
| --- | --------------- | --- | --- |
u
| 35  | Remotely Disarmed  |     |     |
| --- | ------------------ | --- | --- |
h
c
| 36  | Motor or Sensor Exce.ption  |     |     |
| --- | --------------------------- | --- | --- |
|     |                             | y   | A   |
| 37  | CAN Bus Excepti             | on  | T   |
i
H
l
| 38  | CAN Bus Restored  |     |     |
| --- | ----------------- | --- | --- |
i
s
| 39  | Too High Pedestal Temperature  |     |     |
| --- | ------------------------------ | --- | --- |
a
Activve Infrared Intrusion Detector Exception
40
| 41  | Active Infrared Intrusion Detector Restored  |     |     |
| --- | -------------------------------------------- | --- | --- |
| 42  | Communication with Light Board Failed        |     |     |
| 43  | Communication with Light Board Restored      |     |     |
| 44  | Communication with IR Adaptor Failed         |     |     |
| 45  | Communication with IR Adaptor Restored       |     |     |
| 46  | Lane Controller Tampering Alarm              |     |     |
| 47  | Lane Controller Tampering Alarm Restored     |     |     |
| 48  | Lane Controller Fire Input Alarm             |     |     |
| 49  | Lane Controller Fire Input Alarm Restored    |     |     |
| 50  | Staying Event                                |     |     |

<!-- page: 26 -->

| Value  |                                                     | Description  |     |
| ------ | --------------------------------------------------- | ------------ | --- |
| 51     | No Memory for Unreported and Access Granted Events  |              |     |
| 52     | Fire Input Alarm                                    |              |     |
| 53     | No-Mask Alarm                                       |              |     |
| 54     | Upload Fire Alarm Matrix                            |              |     |
| 55     | Lock Health Information Exception                   |              |     |
| 56     | Unlock Health Information Exception                 |              |     |
| 57     | Upload Network Camera Event                         |              |     |
| 58     | Optional Board Offline                              |              |     |
| 59     | Restore Optional Board                              |              |     |
| 60     | Access Module Fire Input Short Circuit Alarm        |              |     |
z
| 61  | Restore Access Module Fire Input  |     |     |
| --- | --------------------------------- | --- | --- |
k
| 62  | Access Module Tempering Alarm  |     | .   |
| --- | ------------------------------ | --- | --- |
a
| 63  | Restore Access Module Tempering Alarm  |     |     |
| --- | -------------------------------------- | --- | --- |
t
| 64  | Panic Alarm  |     |     |
| --- | ------------ | --- | --- |
h
| 65  | Consultation Calling  | @   |     |
| --- | --------------------- | --- | --- |
n
| 66  | Main Station Calling  |     |     |
| --- | --------------------- | --- | --- |
i
| 67  | VoIP Calling  |     |     |
| --- | ------------- | --- | --- |
k
| 68  | Terminal Zone Alarm  | i   |     |
| --- | -------------------- | --- | --- |
u
| 69  | Terminal Tempering Alarm  |     |     |
| --- | ------------------------- | --- | --- |
h
70  Terminal: Sudden Increcase/Decrease of Sound Intensity Alarm
   .
y A
| Alarm Input Event Linkaige  |     | T   |     |
| --------------------------- | --- | --- | --- |
H
l
i

s
| Value  |     | Description  |     |
| ------ | --- | ------------ | --- |
a
v
| 0   | Zone Short Circuit Attempts Alarm  |     |     |
| --- | ---------------------------------- | --- | --- |
| 1   | Zone Open Circuit Attempts Alarm   |     |     |
| 2   | Zone Exception Alarm               |     |     |
| 3   | Zone Alarm Restored                |     |     |
| 4   | Alarm Input Alarm                  |     |     |
| 5   | Alarm Input Alarm Restored         |     |     |
| 6   | I/O Port Short Circuit Alarm       |     |     |

Access Control Point Event Linkage
| Value  |                                    | Description  |     |
| ------ | ---------------------------------- | ------------ | --- |
| 0      | Open Door with First Card Started  |              |     |

<!-- page: 27 -->

| Value  |                                  |     | Description  |
| ------ | -------------------------------- | --- | ------------ |
| 1      | Open Door with First Card Ended  |     |              |
| 2      | Remain Open Started              |     |              |
| 3      | Remain Open Ended                |     |              |
| 4      | Remain Closed Started            |     |              |
| 5      | Remain Closed Ended              |     |              |
| 6      | Door Unlocked                    |     |              |
| 7      | Door Locked                      |     |              |
z
| 8   | Exit Button Pressed  |     |     |
| --- | -------------------- | --- | --- |
k
.
| 9   | Exit Button Released  |     |     |
| --- | --------------------- | --- | --- |
a
t
| 10  | Door Open (Contact)  |     |     |
| --- | -------------------- | --- | --- |
h
@
| 11  | Door Closed (Contact)  |     |     |
| --- | ---------------------- | --- | --- |
n
| 12  | Door Abnormally Open (Contact)  |     | i   |
| --- | ------------------------------- | --- | --- |
k
| 13  | Door Open Timed Out (Contacit)  |     |     |
| --- | ------------------------------- | --- | --- |
u
| 14  | Door Remotely Open  |     |     |
| --- | ------------------- | --- | --- |
h
c
| 15  | Door Remotely Close.d  |         |     |
| --- | ---------------------- | ------- | --- |
|     |                        | y       | A   |
| 16  | Remain Open Re         | motely  | T   |
i
H
l
| 17  | Remain Closed Remotely  |     |     |
| --- | ----------------------- | --- | --- |
i
s
| 18  | Card Not in Multiple Authentication Group  |     |     |
| --- | ------------------------------------------ | --- | --- |
a
Cardv Not in Multiple Authentication Duration
19
20  Multiple Authentication Mode: Super Password Authentication Failed
21  Multiple Authentication Mode: Remote Authentication Failed
| 22  | Multiple Authentication Completed            |     |     |
| --- | -------------------------------------------- | --- | --- |
| 23  | Multiple Authentication: Remotely Open Door  |     |     |
24  Multiple Authentication: Super Password Authentication Completed
| 25  | Multiple Authentication: Repeated Authentication Failed  |     |     |
| --- | -------------------------------------------------------- | --- | --- |
| 26  | Multiple Authentication Timed Out                        |     |     |
| 27  | Remote Capture                                           |     |     |
| 28  | Doorbell Ring                                            |     |     |
| 29  | Secure Door Control Unit Tampering Alarm                 |     |     |

<!-- page: 28 -->

| Value  |                                             |     | Description  |
| ------ | ------------------------------------------- | --- | ------------ |
| 30     | Center Event                                |     |              |
| 31     | First Card Authentication Started           |     |              |
| 32     | First Card Authentication End               |     |              |
| 33     | Lock Input Short Circuit Attempts Alarm     |     |              |
| 34     | Lock Input Open Circuit Attempts Alarm      |     |              |
| 35     | Lock Input Exception Alarm                  |     |              |
| 36     | Contact Input Short Circuit Attempts Alarm  |     |              |
z
| 37  | Contact Input Open Circuit Attempts Alarm  |     |     |
| --- | ------------------------------------------ | --- | --- |
k
.
| 38  | Contact Input Exception Alarm  |     |     |
| --- | ------------------------------ | --- | --- |
a
t
| 39  | Exit Button Input Short Circuit Attempts Alarm  |     |     |
| --- | ----------------------------------------------- | --- | --- |
h
@
| 40  | Exit Button Input Open Circuit Attempts Alarm  |     |     |
| --- | ---------------------------------------------- | --- | --- |
n
| 41  | Exit Button Input Exception Alarm i |     |     |
| --- | ----------------------------------- | --- | --- |
k
| 42  | Unlocking Exception  |     | i   |
| --- | -------------------- | --- | --- |
u
| 43  | Unlocking Timed Out  |     |     |
| --- | -------------------- | --- | --- |
h
c
| 44  | Unauthorized First Ca.rd Opening Failed  |          |     |
| --- | ---------------------------------------- | -------- | --- |
|     |                                          | y        | A   |
| 45  | Call Elevator Rel                        | ay Open  | T   |
i
H
l
| 46  | Call Elevator Relay Closed  |     |     |
| --- | --------------------------- | --- | --- |
i
s
| 47  | Auto Button Relay Open  |     |     |
| --- | ----------------------- | --- | --- |
a
Autov Button Relay Closed
48
| 49  | Button Relay Open          |     |     |
| --- | -------------------------- | --- | --- |
| 50  | Button Relay Closed        |     |     |
| 51  | Visitor Calling Elevator   |     |     |
| 52  | Resident Calling Elevator  |     |     |
| 53  | Valid Message              |     |     |
| 54  | Invalid Message            |     |     |
| 55  | Tailgating                 |     |     |
| 56  | Reverse Passing            |     |     |
| 57  | Force Collision            |     |     |
| 58  | Climbing Over              |     |     |

<!-- page: 29 -->

| Value  |                                          | Description  |
| ------ | ---------------------------------------- | ------------ |
| 59     | Passing Timed Out                        |              |
| 60     | Intrusion Alarm                          |              |
| 61     | Authentication Failed When Free Passing  |              |
| 62     | Barrier Obstructed                       |              |
| 63     | Barrier Restored                         |              |
| 64     | Door Closed via Keyfob                   |              |
| 65     | Door Opened via Keyfob                   |              |
z
| 66  | Remain Open via Keyfob  |     |
| --- | ----------------------- | --- |
k
   .
a
Authentication Unit Event Linkage  t
h
@
| Value  |     | Description  n |
| ------ | --- | -------------- |
i
| 0   | Duress Alarm  |     |
| --- | ------------- | --- |
k
i
| 1   | Card Reader Tampering Alarm  |     |
| --- | ---------------------------- | --- |
u
| 2   | Valid Card Authentication Completed  | h   |
| --- | ------------------------------------ | --- |
c
Card and Password A.uthentication Completed
3
y A
Card and Passwoird AuthenticTation Failed
4
H
l
| 5   | Card and Paissword Authentication Timed Out  |     |
| --- | -------------------------------------------- | --- |
s
| 6   | Card Aauthentication Attempts Reach Limit  |     |
| --- | ------------------------------------------ | --- |
v
| 7   | No Permission for Card                         |     |
| --- | ---------------------------------------------- | --- |
| 8   | Invalid Card Swiping Time Period               |     |
| 9   | Expired Card                                   |     |
| 10  | Card No. Not Exist                             |     |
| 11  | Anti-passing Back Authentication Failed        |     |
| 12  | Interlocking Door Not Closed                   |     |
| 13  | Fingerprint Matched                            |     |
| 14  | Fingerprint Mismatched                         |     |
| 15  | Card and Fingerprint Authentication Completed  |     |
| 16  | Card and Fingerprint Authentication Failed     |     |
| 17  | Card and Fingerprint Authentication Timed Out  |     |

<!-- page: 30 -->

Value  Description
18  Card, Fingerprint, and Password Authentication Completed
| 19  | Card and Fingerprint Authentication Failed         |     |
| --- | -------------------------------------------------- | --- |
| 20  | Card and Fingerprint Authentication Timed Out      |     |
| 21  | Fingerprint and Password Authentication Completed  |     |
| 22  | Fingerprint and Password Authentication Failed     |     |
| 23  | Fingerprint and Password Authentication Timed Out  |     |
| 24  | Fingerprint Not Exist                              |     |
z
| 42  | Employee ID and Fingerprint Authentication Completed  |     |
| --- | ----------------------------------------------------- | --- |
k
.
| 43  | Employee ID and Fingerprint Authentication Failed  |     |
| --- | -------------------------------------------------- | --- |
a
t
| 44  | Employee ID and Fingerprint Authentication Timed Out  |     |
| --- | ----------------------------------------------------- | --- |
h
@
45  Employee ID, Fingerprint, and Password Authentication Completed
n
46  Employee ID, Fingerprint, and Passiword Authentication Failed
k
47  Employee ID, Fingerprint, and iPassword Authentication Timed Out
u
| 52  | Employee ID and Passworhd Authentication Completed  |     |
| --- | --------------------------------------------------- | --- |
c
| 52  | Employee ID and Pas.sword Authentication Failed  |     |
| --- | ------------------------------------------------ | --- |
y A
| 53  | Employee ID and |  Password ATuthentication Timed Out  |
| --- | --------------- | ------------------------------------ |
i
H
l
Authentication Failed When Door Remain Closed or Door in Sleeping
i
57
|     | Mode  s |     |
| --- | ------- | --- |
a
58  Authentication Failed When Authentication Schedule in Sleeping Mode
v
| 59  | Card Encryption Verification Failed               |     |
| --- | ------------------------------------------------- | --- |
| 60  | Anti-passing Back Server Response Failed          |     |
| 61  | Password Mismatched                               |     |
| 62  | Employee ID Not Exist                             |     |
| 63  | Combined Authentication Completed                 |     |
| 64  | Combined Authentication Timed Out                 |     |
| 65  | Authentication Type Mismatched                    |     |
| 67  | Maximum Password Authentication Failure Attempts  |     |
| 68  | Password Authenticated                            |     |
| 69  | Password Authentication Failed                    |     |

<!-- page: 31 -->

| Value  |                                         |     | Description  |     |
| ------ | --------------------------------------- | --- | ------------ | --- |
| 70     | QR Code Authenticated                   |     |              |     |
| 71     | QR Code Authentication Failed           |     |              |     |
| 72     | Resident Authorization Authenticated    |     |              |     |
| 73     | Bluetooth Authenticated                 |     |              |     |
| 74     | Bluetooth Authentication Failed         |     |              |     |
| 75     | Authentication Failed: Invalid M1 Card  |     |              |     |
| 76     | Verifying CPU Card Encryption Failed    |     |              |     |
z
| 77  | Disabling NFC Verification Failed  |     |     |     |
| --- | ---------------------------------- | --- | --- | --- |
k
.
| 78  | EM Card Recognition Disabled  |     |     |     |
| --- | ----------------------------- | --- | --- | --- |
a
t
| 7   | M1 Card Recognition Disabled  |     |     |     |
| --- | ----------------------------- | --- | --- | --- |
h
@
| 80  | CPU Card Recognition Disabled  |     |     |     |
| --- | ------------------------------ | --- | --- | --- |
n
| 81  | ID Card Recognition Disabled  |     | i   |     |
| --- | ----------------------------- | --- | --- | --- |
k
| 82  | Importing Key to Card Failed  |     | i   |     |
| --- | ----------------------------- | --- | --- | --- |
u
| 83  | Verifying Desfire Card Encryption Failed  |     |     |     |
| --- | ----------------------------------------- | --- | --- | --- |
h
| 84  | Desfire Card Reading Dcisabled  |     |     |     |
| --- | ------------------------------- | --- | --- | --- |
.
| 85  | Access Granted by Iris  |         |     |     |
| --- | ----------------------- | ------- | --- | --- |
|     |                         | y       | A   |     |
| 86  | Access Denied b         | y Iris  | T   |     |
i
Iris Anti-Spoofling DetectionH Failed
87
i
| 88  | FeliCa Card Recognition Disabled  |     |     |     |
| --- | --------------------------------- | --- | --- | --- |
s
| 89  | QR Code Recognized  |     |     |     |
| --- | ------------------- | --- | --- | --- |
a
| 90  | Voicveprint Anti-Spoofing Detection Failed  |     |     |     |
| --- | ------------------------------------------- | --- | --- | --- |
| 91  | Voiceprint Authentication Failed            |     |     |     |
| 92  | Electrostatic Discharge Testing Passed      |     |     |     |
93  Electrostatic Discharge Testing Not Passed (Door Opened)
94  Electrostatic Discharge Testing Not Passed (Door Not Opened)
| 95   | Electrostatic Discharge Testing Timed Out   |     |     |     |
| ---- | ------------------------------------------- | --- | --- | --- |
| 96   | Person and Social Security Card Matched     |     |     |     |
| 97   | Person and Social Security Card Mismatched  |     |     |     |
| 98   | Access Granted by Palmprint and Palm Veins  |     |     |     |
| 99   | Access Denied by Palmprint and Palm Veins   |     |     |     |
| 100  | Blocklist Event                             |     |     |     |