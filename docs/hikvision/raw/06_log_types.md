<!-- source_file: ISAPI/Region Code (1).pdf -->
<!-- real_content: B.1 Log Types for ISAPI -->
<!-- source_sha256: 353409e916913f076d3ea0da8883f2866c08154244f7bd70304e91e5d5f7e5be -->
<!-- converter: markitdown_mcp.convert_to_markdown (MarkItDown MCP) -->



<!-- page: 1 -->

B.1 Log Types for ISAPI
There are four major log types, i.e., alarm log, exception log, operation log, event log, and
information log. And each major type contains multiple minor types, see details in the following
contents.
Alarm Logs

| Log Type      |     |     |                       | Description  |
| ------------- | --- | --- | --------------------- | ------------ |
| shortCircuit  |     |     | Short Circuit Alarm z |              |
k
| dataPrealarm  |     |     | Data warning  | .   |
| ------------- | --- | --- | ------------- | --- |
a
| vehicleMonitor  |     |     | Vehicle armting alarm  |     |
| --------------- | --- | --- | ---------------------- | --- |
h
| peopleCounting  |     |     | People counting alarm  |     |
| --------------- | --- | --- | ---------------------- | --- |
@
n
| framesPeopleCounting  |     |     | Regional people counting alarm  |     |
| --------------------- | --- | --- | ------------------------------- | --- |
i
k
| brokenCircuit  |     |     | Open Circuit Alarm  |     |
| -------------- | --- | --- | ------------------- | --- |
i
uAlarm Reset
alarmReset
h
| alarmNormal  |     | c   | Return to Normal  |     |
| ------------ | --- | --- | ----------------- | --- |
.
| passwordError  | y   |     | AIncorrect Password  |     |
| -------------- | --- | --- | -------------------- | --- |
T
i
| idCardIllegally  |     | HInvalid Card ID  |     |     |
| ---------------- | --- | ----------------- | --- | --- |
l
i
| keyPADRemove  | s   |     | Keypad Tampered  |     |
| ------------- | --- | --- | ---------------- | --- |
a
| keyPADRemoveRestore  |     |     | Keypad Restored  |     |
| -------------------- | --- | --- | ---------------- | --- |
v
| devRemove         |     |     | Device Tampered  |     |
| ----------------- | --- | --- | ---------------- | --- |
| devRemoveRestore  |     |     | Device Restored  |     |
belowAlarmLimit1  Sensor Value is Lower than Alarm Limit Value 1
belowAlarmLimit2  Sensor Value is Lower than Alarm Limit Value 2
belowAlarmLimit3  Sensor Value is Lower than Alarm Limit Value 3
belowAlarmLimit4  Sensor Value is Lower than Alarm Limit Value 4
aboveAlarmLimit1  Sensor Value is Higher than Alarm Limit Value 1
aboveAlarmLimit2  Sensor Value is Higher than Alarm Limit Value 2
aboveAlarmLimit3  Sensor Value is Higher than Alarm Limit Value 3
aboveAlarmLimit4  Sensor Value is Higher than Alarm Limit Value 4
| UrgencyBtnON  |     |     | Panic Button Triggered  |     |
| ------------- | --- | --- | ----------------------- | --- |

<!-- page: 2 -->

Log Type  Description
| UrgencyBtnOFF         |     | Panic Button Restored           |
| --------------------- | --- | ------------------------------- |
| virtualDefenceBandit  |     | Virtual Zone Burglary Alarm     |
| virtualDefenceFire    |     | Virtual Zone Fire Alarm         |
| virtualDefenceUrgent  |     | Virtual Zone Panic Alarm        |
| motDetStart           |     | Motion Detection Alarm Started  |
| motDetStop            |     | Motion Detection Alarm Stopped  |
| hideAlarmStart        |     | Device Blocked                  |
z
| hideAlarmStop  |     | Device Blocking Alarm Restored  |
| -------------- | --- | ------------------------------- |
k
.
| UPSAlarm  |     | UPS Alarm  |
| --------- | --- | ---------- |
a
t
| electricityMeterAlarm  |     | Coulombmeter Alarm  |
| ---------------------- | --- | ------------------- |
h
@
| switchPowerAlarm  |     | Switch Power Supply Alarm  |
| ----------------- | --- | -------------------------- |
n
| GasDetectSys  |     | Gias Detection Alarm  |
| ------------- | --- | --------------------- |
k
| transformerTempAlarm  |     | iTransformer Temperature Alarm  |
| --------------------- | --- | ------------------------------- |
u
| tempHumiAlarm  |     | Temperature and Humidity Sensor Alarm  |
| -------------- | --- | -------------------------------------- |
h
c
| UPSAlarmRestore               | .                             | UPS Alarm Restored  |
| ----------------------------- | ----------------------------- | ------------------- |
|                               | y                             | A                   |
| electricityMeterAlarmRestore  | TCoulombmeter Alarm Restored  |                     |
i
H
l
| switchPowerAlarmRestore  |     | Switch Power Supply Alarm Restored  |
| ------------------------ | --- | ----------------------------------- |
i
s
| GasDetectSysRestore  |     | Gas Detection Alarm Restored  |
| -------------------- | --- | ----------------------------- |
a
transformerTempAvlarmRestore
Transformer Temperature Alarm Restored
tempHumiAlarmRestore  Temperature-Humidity Sensor Alarm Restored
waterLevelSensorAlarm  Temperature-Humidity Sensor Alarm Restored
| waterLevelSensorAlarmRestore  |     | Flood Sensor Restored                 |
| ----------------------------- | --- | ------------------------------------- |
| dustNoiseAlarm                |     | Dust and Noise Sensor Alarm           |
| dustNoiseAlarmRestore         |     | Dust and Noise Sensor Alarm Restored  |
| environmentalLogger           |     | Environmental Data Collector Alarm    |
environmentalLoggerAlarm  Environmental Data Collector Restored
| triggerTemper         |     | Detector Tampered  |
| --------------------- | --- | ------------------ |
| triggerTemperRestore  |     | Detector Restored  |
| emergencyCallHelp     |     | Panic Alarm        |

<!-- page: 3 -->

Log Type  Description
| emergencyCallHelpRestore  |     | Panic Alarm Restored          |
| ------------------------- | --- | ----------------------------- |
| consult                   |     | Consultation Alarm            |
| consultRestore            |     | Consultation Alarm Restored   |
| deviceMoveAlarm           |     | Device Motion Alarm           |
| deviceMoveAlarmRestore    |     | Device Motion Alarm Restored  |
| earlyWarningAlarm         |     | Early Warning Zone Alarm      |
| earlyWarningAlarmRestore  |     | Early Warning Zone Restored   |
z
| warningAlarm  |     | Warning Zone Alarm  |
| ------------- | --- | ------------------- |
k
.
| warningAlarmRestore  |     | Warning Zone Restored  |
| -------------------- | --- | ---------------------- |
a
t
wirelessOutputModTamperEvident  Wireless Output Expander Tampered
h
@
wirelessOutputModTamperEvidentReset  Wireless Output Expander tamper Restored
n
| wirelessRepeaterTamperEvident  |     | Wiireless Repeater Tampered  |
| ------------------------------ | --- | ---------------------------- |
k
wirelessRepeaterTamperEvidentReset  iWireless Repeater tamper Restored
u
| wirelessSirenTamperEvident  |     | Wireless Siren Tampered  |
| --------------------------- | --- | ------------------------ |
h
c
wirelessSirenTamperEvidentReset . Wireless Siren Tamper Restored
|                             | y   | A                          |
| --------------------------- | --- | -------------------------- |
| wirelessKeypadTamperEvident |     | TWireless Keypad Tampered  |
i
H
l
wirelessKeypadTamperEvidentReset  Wireless Keypad Tamper Restored
i
s
wirelessCardReaderTamperEvident  Wireless Card Reader Tampered
a
wirelessCardReadevrTamperEvidentReset
Wireless Card Reader Tamper Restored
| softZoneMedicalAlarm           |     | Virtual Zone Medical Alarm             |
| ------------------------------ | --- | -------------------------------------- |
| accessControllerEvent          |     | Access Controller Event                |
| videoIntercomEvent             |     | Video Intercom Event                   |
| GJDEvent                       |     | GJD Security Control Panel Event       |
| LuminateEvent                  |     | LUMINITE Security Control Panel Event  |
| OPTEXEvent                     |     | OPTEX Security Control Panel Event     |
| cameraDetectorEvent            |     | Detector Event                         |
| securityControlPanelEvent      |     | Security Control Panel Event           |
| RS-485AlarmInputModuleEvident  |     | RS-485 Zone Module Tampered            |
RS-485AlarmInputModuleTamperReset  RS-485 Zone Module Tampering Reset

<!-- page: 4 -->

Log Type  Description
RS-485WirelessReceiverTamperEvident  RS-485 Wireless Receiver Module Tampered
RS-485 Wireless Receiver Module Tampering
RS-485WirelessReceiverTamperEvidentReset
Reset
| dredgerDetectionAlarm  |     | Dredger Detection Alarm       |
| ---------------------- | --- | ----------------------------- |
| crossLineAlarm         |     | Line Crossing Alarm           |
| crossLineAlarmRestore  |     | Line Crossing Alarm Restored  |
HFPDAlarmStart  High Frequently Appeared Person Alarm Started
High Frequently Appzeared Person Alarm
HFPDAlarmStop
k
Stopped
.
a
| LFPDAlarmStart  |     | Low Frequency Person Alarm Started  |
| --------------- | --- | ----------------------------------- |
t
| LFPDAlarmStop  |     | Low Freqhuency Person Alarm Stopped  |
| -------------- | --- | ------------------------------------ |
@
| safetyHelmetAlarmStart  |     | Harnd Hat Detection Alarm Started  |
| ----------------------- | --- | ---------------------------------- |
i
| safetyHelmetAlarmStop  |     | kHard Hat Detection Alarm Stopped  |
| ---------------------- | --- | ---------------------------------- |
i
| dataPrealarm  | uTraffic Pre-alarm  |     |
| ------------- | ------------------- | --- |
h
| playCellphoneStart  |     | Playing Cellphone Alarm Started  |
| ------------------- | --- | -------------------------------- |
c
.
| playCellphoneStop  |     | Playing Cellphone Alarm Stopped  |
| ------------------ | --- | -------------------------------- |
|                    | y   | A                                |
T
| sleepOnDutyStart  | i   | Sleeping on Duty Alarm Started  |
| ----------------- | --- | ------------------------------- |
H
l
i
| sleepOnDutyStop  |     | Sleeping on Duty Alarm Stopped  |
| ---------------- | --- | ------------------------------- |
s
| vibrationDetectionStaart  |     | Vibration Detection Alarm Started  |
| ------------------------- | --- | ---------------------------------- |
v
| vibrationDetectionStop  |     | Vibration Detection Alarm Stopped  |
| ----------------------- | --- | ---------------------------------- |
fireEscapeDetectionStart  Fire Engine Access Detection Started
| fireEscapeDetectionStop       |     | Fire Engine Access Detection Ended  |
| ----------------------------- | --- | ----------------------------------- |
| takingElevatorDetectionStart  |     | Elevator Detection Started          |
| takingElevatorDetectionStop   |     | Elevator Detection Ended            |
unregisteredStreetVendorStart  Unlicensed Business Vendor Detection Started
unregisteredStreetVendorStop  Unlicensed Business Vendor Detection Ended
stallOutsideShopStart  Business Outside Store Detection Started
stallOutsideShopStop  Business Outside Store Detection Ended
stallOccupyingRoadStart  Business on Sidewalk Detection Started
stallOccupyingRoadStop  Business on Sidewalk Detection Ended

<!-- page: 5 -->

Log Type

Description

illegalHeapStart

illegalHeapStop

illParkofNonMotorVehicleStart

illParkofNonMotorVehicleStop

Pile Goods or Materials in Chaos Detection
Started

Pile Goods or Materials in Chaos Detection
Ended

Non-Motor Vehicles Parking in Chaos Detection
Started

Non-Motor Vehicles Parking in Chaos Detection
Ended

illegalOutdoorAdvertisementStop

illegalOutdoorAdvertisementStart

Unauthorized Outdoor Advertisement Detection
Started

Unauthorized Outdoor Advertisement Detection
Ended

Packaged Garbage Detection Started

Packaged Garbage Detection Ended

vasiliy.chuikin@hta.kz

HTA

Overflowing Dustbin Detection Started

Overflowing Dustbin Detection Ended

Exposed Garbage Detection Started

Exposed Garbage Detection Ended

Running Business with Patio Umbrella Detection
Started

Running Business with Patio Umbrella Detection
Ended

packGarbageStart

packGarbageStop

stallUnderUmbrellaStart

stallUnderUmbrellaStop

dustbinOverflowStart

dustbinOverflowStop

exposeGarbageStart

exposeGarbageStop

hangClothingAlongStreetStart

Hanging Clothes On Street Detection Started

hangClothingAlongStreetStop

Hanging Clothes On Street Detection Ended

ATMPanelStart

ATMPanelStop

ATMSurroundStart

ATMSurroundStop

ATMFaceStart

ATMFaceStop

ATMSafetyCabinStart

ATMSafetyCabinStop

ATM Panel Alarm Started

ATM Panel Alarm Ended

ATM Surround Alarm Started

ATM Surround Alarm Ended

ATM Face Alarm Started

ATM Face Alarm Ended

ATM Safety Cabin Alarm Started

ATM Safety Cabin Alarm Ended



<!-- page: 6 -->

Log Type

Description

soundIntensityMutation

Sudden Increase of Sound Intensity Detection

soundIntensityMutationStop

Sudden Increase of Sound Intensity Detection
Ended

soundIntensitySteepFall

Sudden Decrease of Sound Intensity Detection

soundIntensitySteepFallStop

Sudden Decrease of Sound Intensity Detection
Ended

moveAlarm

Motion Alarm

lowTemperatureAlarmRestored

Low Temperature Alarm Restored

moveAlarmRestored

lowTemperatureAlarm

highTemperatureAlarm

highTemperatureAlarmRestored

High Temperature Alarm Restored

TemperatureIntervalMeasurementStart

Interval Temperature Measurement Started

TemperatureIntervalMeasurementStop

Interval Temperature Measurement Stopped

laneOccupationbyMotorVehicleStart

Lane Occupation by Motor Vehicle Detection
Started

humanBodyStart

Mass Incident Detection Started

Motion Alarm Restored

Low Temperature Alarm

High Temperature Alarm

vasiliy.chuikin@hta.kz

HTA

hangingOutdoorBannerStart

Hanging Banner Outdoors Detection Started

illegalAdvertisementStart

Illegal Advertisement Detection Started

illegalAdvertisementBannerStart

Illegal Advertisement Banner Detection Started

dirtyWaterbodyStart

Dirty Waters Detection Started

puttingTemporaryShelterIllegallyStart

Illegally Putting Temporary Shelter Detection
Started

dirtyRoadStart

Dirty Road Detection Started

heapingWasteIllegallyStart

Illegally Heaping Waste Detection Started

stagnantRoadStart

Stagnant Road Detection Started

burningRubbishandLeavesStart

Burning Garbage and Leaves Detection Started

destroyingandOccupyingGreenBeltStart

laneOccupationbyConstructionStart

Destroying and Occupying the Green Belt
Detection Started

Lane Occupation by Construction Detection
Started



<!-- page: 7 -->

Log Type

Description

improperRubbishBinStart

abandonedFurnitureStart

outsideAirConditionerHangingLowStart

puttingInflatableArchIllegallyStart

Improper Dustbin Detection Started

Abandoned Furniture Detection Started

Hanging the Air Conditioner Lowly Outside
Detection Started

Illegally Putting Inflatable Arch Detection
Started

roadDamagedStart

Road Damaged Detection Started

wasteWaterDischargedonRoadStart

laneOccupationbyWasteRecyclingStart

barbecueStallinPublicSitesStart

Barbecue Stall in Public Sites Detection Started

Lane Occupation by Waste Recycling Detection
Started

Waste Water Discharged on Road Detection
Started

constructionMaterialsMisplacedStart

Construction Materials Misplaced Detection
Started

settingUpSlopeIllegallyStart

Illegally Setting Up Slope Detection Started

vasiliy.chuikin@hta.kz

HTA

litteringWasteonRoadStart

Littering Waste on Road Detection Started

distributingFlyersinPublicSitesStart

Distributing Flyers in Public Sites Detection
Started

roadCollapsedStart

Road Collapsed Detection Started

constructionWasteMisplacedStart

Construction Water Misplaced Detection
Started

greeningWasteStart

Greening Waste Detection Started

nonDecorativeHangingonTreeStart

installingWiresandPipesIllegallyStart

Non-Decorative Tree Hangings Detection
Started

Illegally Installing Wires and Pipes Detection
Started

raisingDomesticAnimalsStart

Raising Domestic Animals Detection Started

carcassNotClearedStart

Carcass Not Cleared Detection Started

streetSlaughterStart

Slaughtering Animals Along the Street Detection
Started

dustbinExceptionStart

Dustbin Exception Detection Started

shortcutIsolationPileExceptionStart

Shortcut Isolation Pile Exception Detection
Started



<!-- page: 8 -->

Log Type

Description

laneSeparatorDamagedStart

Lane Separator Damaged Detection Started

antiCollisionBarrelDamagedStart

Anti-Collision Barrel Damaged Detection Started

fireFightingFacilityDamagedStart

Fire Facility Damaged Detection Started

electricPowerFacilityExceptionStart

Power Facility Damaged Detection Started

transformerTankExceptionStart

Transformer Box Exception Detection Started

streetTreeExceptionStart

Street Tree Exception Detection Started

illegalAdvertisementBannerStop

Illegal Advertisement Banner Detection Ended

humanBodyStop

Mass Incident Detection Ended

treeProtectionFacilityDamagedStart

Tree-Protection Facility Damaged Detection
Started

manholeCoverExceptionStart

Manhole Cover Exception Detection Started

drainGratingDamagedStart

Drain Grating Damaged Detection Started

billboardDamagedStart

Billboard Damaged Detection Started

advertisingSignDamagedStart

Advertising Sign Damaged Detection Started

laneOccupationbyMotorVehicleStop

Lane Occupation by Motor Vehicle Detection
Ended

vasiliy.chuikin@hta.kz

HTA

hangingOutdoorBannerStop

Hanging Banner Outdoors Detection Ended

illegalAdvertisementStop

Illegal Advertisement Detection Ended

puttingTemporaryShelterIllegallyStop

Illegally Putting Temporary Shelter Detection
Ended

dirtyRoadStop

Dirty Road Detection Ended

heapingWasteIllegallyStop

Illegally Heaping Waste Detection Ended

stagnantRoadStop

Stagnant Road Detection Ended

burningRubbishandLeavesStop

Burning Garbage and Leaves Detection Ended

destroyingandOccupyingGreenBeltStop

laneOccupationbyConstructionStop

improperRubbishBinStop

abandonedFurnitureStop

Destroying and Occupying the Green Belt
Detection Ended

Lane Occupation by Construction Detection
Ended

Improper Dustbin Detection Ended

Abandoned Furniture Detection Ended

dirtyWaterbodyStop

Dirty Waters Detection Ended



<!-- page: 9 -->

Log Type

Description

outsideAirConditionerHangingLowStop

Hanging the Air Conditioner Lowly Outside
Detection Ended

puttingInflatableArchIllegallyStop

Illegally Putting Inflatable Arch Detection Ended

roadDamagedStop

Road Damaged Detection Ended

constructionMaterialsMisplacedStop

Construction Materials Misplaced Detection
Ended

settingUpSlopeIllegallyStop

Illegally Setting Up Slope Detection Ended

barbecueStallinPublicSitesStop

Barbecue Stall in Public Sites Detection Ended

laneOccupationbyWasteRecyclingStop

wasteWaterDischargedonRoadStop

Lane Occupation by Waste Recycling Detection
Ended

Waste Water Discharged on Road Detection
Ended

litteringWasteonRoadStop

Littering Waste on Road Detection Ended

distributingFlyersinPublicSitesStop

Distributing Flyers in Public Sites Detection
Ended

roadCollapsedStop

Road Collapsed Detection Ended

vasiliy.chuikin@hta.kz

HTA

constructionWasteMisplacedStop

Construction Water Misplaced Detection Ended

greeningWasteStop

Greening Waste Detection Ended

nonDecorativeHangingonTreeStop

Non-Decorative Tree Hangings Detection Ended

installingWiresandPipesIllegallyStop

Illegally Installing Wires and Pipes Detection
Ended

raisingDomesticAnimalsStop

Raising Domestic Animals Detection Ended

carcassNotClearedStop

Carcass Not Cleared Detection Ended

streetSlaughterStop

Slaughtering Animals Along the Street Detection
Ended

dustbinExceptionStop

Dustbin Exception Detection Ended

shortcutIsolationPileExceptionStop

Shortcut Isolation Pile Exception Detection
Ended

laneSeparatorDamagedStop

Lane Separator Damaged Detection Ended

antiCollisionBarrelDamagedStop

Anti-Collision Barrel Damaged Detection Ended

fireFightingFacilityDamagedStop

Fire Facility Damaged Detection Ended

electricPowerFacilityExceptionStop

Power Facility Damaged Detection Ended



<!-- page: 10 -->

Log Type

Description

transformerTankExceptionStop

Transformer Box Exception Detection Ended

streetTreeExceptionStop

Street Tree Exception Detection Ended

treeProtectionFacilityDamagedStop

Tree-Protection Facility Damaged Detection
Ended

manholeCoverExceptionStop

Manhole Cover Exception Detection Ended

drainGratingDamagedStop

Drain Grating Damaged Detection Ended

billboardDamagedStop

Billboard Damaged Detection Ended

advertisingSignDamagedStop

Advertising Sign Damaged Detection Ended

thermalCalibrationFileExceptionStart

Calibration file exception alarm started

thermalCalibrationFileExceptionStop

Calibration file exception alarm ended

Log Type

vasiliy.chuikin@hta.kz

HTA

WDT Reset

Power off

Power on

Low Battery Voltage

Description

Resolution of the detection stream in AI open
platform exceeds the limit

Resolution of the detection stream in Embedded
Open Platform exceeds the limit

AIOPDetResolutionOverflow

HEOPDetResolutionOverflow

WDTReset

lowBatteryVoltage

Exception Logs

powerOn

powerOff

ACLoss

ACRestore

RTCException

netFailure

netRestore

telLineBroken

telLineRestore

expanderBusLoss

expanderBusRestore

AC Power Disconnected

AC Power Restored

RTC Real-time Clock Exception

Network Disconnected

Network Connected

Telephone Line Disconnected

Telephone Line Connected

Bus Expander Disconnected

Bus Expander Connected



<!-- page: 11 -->

Log Type

Description

keypadBusLoss

keypadBusRestore

sensorFailure

sensorRestore

RS485DisConnect

RS485Connect

Keypad Expander Disconnected

Keypad Expander Connected

Analog Sensor Fault

Analog Sensor Restored

RS-485 Channel Disconnected

RS-486 Channel Connected

batteryVoltageRestore

Battery Voltage Restored

GPRS Restored

GPRS Exception

3G Network Exception

Wired Network Restored

Wired Network Exception

vasiliy.chuikin@hta.kz

HTA

3G Network Restored

SIM Card Exception

SIM Card Restored

MODEM Disconnected

Illegal Login

Video Loss

HDD Error

HDD Full

wiredNetAbnormal

wiredNetRestore

GPRSAbnormal

GPRSRestore

3GAbnormal

3GRestore

SIMCardAbnormal

SIMCardRestore

VILost

illegalAccess

HDFull

HDError

DCDLost

IPConflict

netbroken

recError

VIError

IP Address Conflicted

Network Disconnected

Recording Error

Video Input Exception(Only for Analog Channel)

formatHDDError

Remote HDD Formatting Failed

USBError

USBRestore

printError

printRestore

USB Communication Error

USB Communication Error Restored

Printer Error

Printer Error Restored



<!-- page: 12 -->

Log Type

Description

subsystemCommunicationError

Sub-board Communication Error

Network Camera IP Address Conflicted

Video Standard Mismatches

MCU Restarted

GPRS Module Fault

Telephone Module Fault

Wi-Fi Exception

IPCIPconflict

VIMisMatch

MCURestart

GprsMouleFault

telephoneFault

wifiAbnormal

wifiRestore

RFAbornal

RFRestore

detectorOnline

detectorOffline

detectorBatteryNormal

detectorBatteryLow

dataTrafficOverflow

radarSignalFault

radarSignalFaultRestore

RF Restored

RF Exception

Wi-Fi Restored

Detector Connected

Detector Disconnected

vasiliy.chuikin@hta.kz

HTA

Radar Transmitter Restored

Detector Battery Restored

Radar Transmitter Fault

Detector Battery Low

Cellular Network Data Exceeded

wirelessOutputModOffline

Wireless Output Expander Disconnected

wirelessOutputModOnline

Wireless Output Expander Connected

wirelessRepeaterOffline

Wireless Repeater Disconnected

wirelessRepeaterOnline

Wireless Repeater Connected

triggerOffline

triggerOnline

wirelessSirenOffline

wirelessSirenOnline

sirenLowPower

sirenPowerRecovery

ipcDisconnect

ipcConnectRecovery

Trigger Disconnected

Trigger Connected

Wireless Siren Disconnected

Wireless Siren Connected

Siren Battery Low

Siren Battery Restored

Network Camera Disconnected

Network Camera Connected



<!-- page: 13 -->

Log Type  Description
| sendMailFailed  |     | Sending Email Failed  |
| --------------- | --- | --------------------- |
eventUploadException  Uploading Event Failed or Uploaded Event Lost
| keyfobLowPower       |     | Low Keyfob Battery            |
| -------------------- | --- | ----------------------------- |
| keyfobPowerRecovery  |     | Normal Keyfob Battery         |
| detectorOvertime     |     | Detector Heartbeat Timed Out  |
detectorOvertimeRecovery  Detector Heartbeat Timeout Restored
| wSirenOvertime  |     | Wireless Siren Heartbeat Timed Out  |
| --------------- | --- | ----------------------------------- |
z
wSirenOvertimeRecovery  Wireless Siren Heartbeat Timeout Restored
k
.
| wOutputOvertime  |     | Wireless Output Module Heartbeat Timed Out  |
| ---------------- | --- | ------------------------------------------- |
a
t
Wireless Output Module Heartbeat Timeout
wOutputOvertimeRecovery  h
Restored
@
n
| wRepeaterOvertime  |     | Wireless Repeater Heartbeat Timed Out  |
| ------------------ | --- | -------------------------------------- |
i
k
wRepeaterOvertimeRecovery  Wireless Repeater Heartbeat Timeout Restored
i
u
| rfJamming  |     | RF Wireless Communication Blocked  |
| ---------- | --- | ---------------------------------- |
h
rfJammingRecovery  cRF Wireless Communication Blocking Restored
.
y A
| batteryMiss  |     | S torage Battery Loss  |
| ------------ | --- | ---------------------- |
T
i
HStorage Battery Restored
| batteryMissRecovery  | l   |     |
| -------------------- | --- | --- |
i
| ARCUploadFailed  | s   | Uploading to ARC Failed  |
| ---------------- | --- | ------------------------ |
a
| ARCUploadSuccessed  |     | Uploaded to ARC  |
| ------------------- | --- | ---------------- |
v
| ARCUploadRecovery      |     | Uploading to ARC Restored     |
| ---------------------- | --- | ----------------------------- |
| wirelessKeypadOffline  |     | Wireless Keypad Disconnected  |
| wirelessKeypadOnline   |     | Wireless Keypad Connected     |
wirelessCardReaderOffline  Wireless Card Reader Disconnected
| wirelessCardReaderOnline  |     | Wireless Card Reader Connected  |
| ------------------------- | --- | ------------------------------- |
| keypadLowPower            |     | Low Keypad Battery              |
| keypadLowPowerRecovery    |     | Low Keypad Battery Recovered    |
| cardReaderLowPower        |     | Low Card Reader Battery         |
cardReaderLowPowerRecovery  Low Card Reader Battery Recovered
| wKeypadOvertime  |     | Wireless Keypad Heartbeat Timed Out  |
| ---------------- | --- | ------------------------------------ |

<!-- page: 14 -->

Log Type  Description
wKeypadOvertimeRecovery  Wireless Keypad Heartbeat Timeout Recovered
wCardReaderOvertime  Wireless Card Reader Heartbeat Timed Out
Wireless Card Reader Heartbeat Timeout
wCardReaderOvertimeRecovery
Recovered
| ATSFailed      |     | ATS Failed                           |
| -------------- | --- | ------------------------------------ |
| ATSRecovery    |     | ATS Recovered                        |
| LANPathFailed  |     | Wired or Wireless Connection Failed  |
Wired or Wireless Connzection Recovered
LANPathRecovery
k
| mobileNetPathFailed  |     | Mobile Network C.onnection Failed  |
| -------------------- | --- | ---------------------------------- |
a
| mobileNetPathRecovery  |     | Mobile Netwotrk Connection Recovered  |
| ---------------------- | --- | ------------------------------------- |
h
RS-485AlarmInputModuleDisconnected  RS-485 Zone Module Offline
@
n
| RS-485AlarmInputModuleConnected  |     | RS-485 Zone Module Online  |
| -------------------------------- | --- | -------------------------- |
i
k
RS-485WirelessReceiverDisconnected  RS-485 Wireless Receiver Module Offline
i
u
RS-485WirelessReceiverConnected  RS-485 Wireless Receiver Module Online
h
| keypadDisconnected  | cKeypad Offline  |     |
| ------------------- | ---------------- | --- |
.
y A
| keypadConnected  |     | K eypad Online  |
| ---------------- | --- | --------------- |
T
i
HHigh Supply Voltage
| overvoltage  | l   |     |
| ------------ | --- | --- |
i
| undervoltage  | s   | Low Supply Voltage  |
| ------------- | --- | ------------------- |
a
| highHDTemperature  |     | HDD High Temperature  |
| ------------------ | --- | --------------------- |
v
| lowHDTemperature       |     | HDD Low Temperature           |
| ---------------------- | --- | ----------------------------- |
| hdImpact               |     | HDD Impact                    |
| hdBadBlock             |     | HDD Bad Sector                |
| severeHDFailure        |     | HDD Severe Fault              |
| safetyHelmetException  |     | Hard Hat Detection Exception  |
| ezvizUpgradeException  |     | EZ Upgrade Exception          |

Operation Logs

Log Type  Description
| guard  |     | Normal Arming  |
| ------ | --- | -------------- |

<!-- page: 15 -->

Log Type

Description

unguard

bypass

duressAccess

localReboot

remoteReboot

localUpgrade

remoteUpgrade

Normal Disarming

Bypass

Duress

Local Reboot

Remote Reboot

Local Upgrade

Remote Upgrade

Remote Alarm Output Control

Siren: On

Access Control: Open

Access Control : Closed

Restore Default Settings

vasiliy.chuikin@hta.kz

HTA

RS-485 Channel Settings

Alarm Output Settings

Added Administrator

Dialing Settings

Sensor Settings

Zone Settings

Edited Administrator

Siren: Off

recoveryDefultParam

outpulAlarm

accessOpen

accessClose

sirenOpen

sirenClose

modZoneConfig

modAlarmoutConfig

modAnalogConfig

RS485Config

phoneConfig

addAdmin

modAdminParam

delAdmin

addNetUser

modNetUserParam

delNetUser

addOperator

modOperatorPw

delOperator

addKeyPadUser

delKeyPadUser

Deleted Administrator

Added DVR/NVR Operator

Edited DVR/NVR Operator

Deleted DVR/NVR Operator

Added Camera Operator

Edited Camera Operator Password

Deleted Camera Operator Password

Added Keypad/Card Reader User

Deleted Keyboard/Card Reader User



<!-- page: 16 -->

Log Type

Description

Remote Login

Remote Logout

Remote Arming

Remote Disarming

Edited Control Panel Settings

Bypass Restored

Turned on Output

Edited Subsystem Parameters

Group Bypass

Turned off Output

Group Bypass Restored

Edited GPRS Parameters

vasiliy.chuikin@hta.kz

HTA

Remote: Stopped Recording

Remote: Started Recording

Edited Uploading Mode

Two-way Audio Started

Edited Access Control Settings

Edited Network Report Settings

Transparent Transmission Started

Transparent Transmission Stopped

remoteUserLogin

remoteUserLogout

remoteGuard

remoteUnguard

modHostConfig

restoreBypass

alarmOutOpen

alarmOutClose

modSubsystemParam

groupBypass

groupBypassRestore

modGprsParam

modNetReportParam

modReportMode

modGatewayParam

remoteStartRec

remoteStopRec

transChanStart

transChanStop

startVoiceTalk

stopVoiceTalk

remotePlayByFile

remotePlayByTime

remotePTZCtrl

remoteLockFile

remoteUnlockFile

remoteFormatHd

Two-way Audio Terminated

Remote: Playback or Downloaded by File

Remote: Playback by Time

Remote: PTZ Control

Remote: Locked File

Remote: Unlocked File

Remote: Formatted HDD

remoteDownloadCfgFile

Remote: Exported Configuration Files

remoteUploadCfgFile

Remote: Imported Configuration Files



<!-- page: 17 -->

Log Type

Description

remoteDownloadRecFile

Remote: Exported File

stayArm

quickArm

keyswitchArm

keyswitckDisarm

clearAlarm

modFaultConfig

Stay Arming

Instant Arming

Key Zone Arming

Key Zone Disarming

Alarm Cleared

Edited System Fault Settings

modAlarmOutConfig

searchExternalModule

registerExternalModule

closeKeypadAlarm

mod3GConfig

modPrintConfig

SDCardFormat

upgradeSubsystem

planArmConfig

phoneArm

phoneStayArm

phoneQuickArm

phoneDisarm

phoneClearAlarm

whiteConfig

timeTriggerConfig

pictureConfig

tamperConfig

Edited Event Alarm Output Settings

Re-registered External Module

Searched for External Module

Disabled Keypad Beep

Edited Mobile Parameters

vasiliy.chuikin@hta.kz

HTA

Edited Printer Parameters

Upgraded Sub-board

SMS Instant Arming

Formatted SD Card

SMS Stay Arming

SMS Arming

SMS Disarming

Arming/Disarming Schedule Configuration

SMS Alarm Cleared

Allowlist Settings

Enabled/Disabled Trigger Configuration by
Schedule

Capture Settings

Zone Tamper-Proof Settings

remoteKeypadUpgrade

Remote: Upgraded Keypad

singlePartionArmORDisarm

Single-Zone Arming/Disarming

cardConfiguration

Card Settings



<!-- page: 18 -->

Log Type

Description

cardAramORDisarm

Arming/Disarming by Card

expendNetCenterConfig

Extension Network Center Settings

netCardConfig

DDNSConfig

RS485BusConfig

RS485BusReRegistration

remoteOpenElectricLock

NIC Settings

DDNS Settings

RS-485 Bus Settings

RS-485 Bus Re-registration

Remote: Unlocked

remoteCloseElectricLock

localOpenElectricLock

localCloseElectricLock

openAlarmLamp

closeAlarmLamp

oneKeyAwayArm

oneKeyStayArm

singleZoneArm

singleZoneDisarm

HIDDNSConfig

remoteKeypadUpdata

Remote: Turned On Alarm Lamp

Local: Locked

Local: Unlocked

Remote: Locked

Remote: Turned Off Strobe

vasiliy.chuikin@hta.kz

HTA

One-Push Away Arming

One-Push Stay Arming

Single-Zone Disarming

Single-Zone Arming

Remote: Upgraded Keypad

HiDDNS Settings

remoteDelAllVideoAnalysisTask

Empty All Video Analysis Tasks Remotely

temporaryPassword

Operation Record of Temporary Password

zoneAddDetector

zoneDelDetector

qureyDetectorSignal

qureyDetectorBattery

setDetectorGuard

setDetectorUnguard

setWifiParm

voiceOpen

Added Detector

Deleted Detector

Checked Detector Signal Strength on Security
Control Panel

Checked Detector Remaining Battery on Security
Control Panel

Detector Arming

Detector Disarming

Wi-Fi Settings

Audio On



<!-- page: 19 -->

Log Type

Description

voiceClose

functionKeyEnable

functionKeyDisable

readCard

localDeviceActive

localFactoryDefault

Mute

Enabled Function Key

Disabled Panel Function Button

Swiped Patrol Card

Activated Device Remotely

Restored Factory Settings Locally

remoteFactoryDefault

Restored Factory Settings Remotely

Deleted Wireless Output Module

Added Wireless Output Module

Mobile Phone Number Settings

Added Wireless Repeater

Deleted Wireless Repeater

vasiliy.chuikin@hta.kz

HTA

Cellular Data Limit Settings

Deleted Wireless Siren

Added Wireless Siren

Checked RF Signal

Deleted Keyfob

Added Keyfob

Added Card

Deleted Card

addWirelessOutputMod

delWirelessOutputMod

addWirelessRepeater

delWirelessRepeater

telListConfig

searchRFSignal

addWirelessSiren

delWirelessSiren

flowConfig

addRemoter

delRemoter

addCard

delCard

remoteAddIpc

remoteDelIpc

remoteSetIpc

Added Network Camera

Deleted Network Camera

Edited Network Camera

localAddressFilterConfig/remoteAddressFi
lterConfig

Local/Remote Address Filter Configuration

enterProgramMode

existProgramMode

localIOTCfgFileInput

Programming Mode Enabled for Keypad

Programming Mode Disabled for Keypad

Local operation: import IoT configuration file

localIOTCfgFileOutput

Local operation: export IoT configuration file



<!-- page: 20 -->

Log Type

Description

remoteIOTCfgFileInput

Remote operation: import IoT configuration file

remoteIOTCfgFileOutput

Remote operation: export IoT configuration file

Local operation: add IoT channel

Remote operation: add IoT channel

Local operation: delete IoT channel

Remote operation: delete IoT channel

Local operation: configure IoT channel

Remote operation: configure IoT channel

localIOTAdd

remoteIOTAdd

localIOTDelete

remoteIOTDelete

localIOTSet

remoteIOTSet

armWithFault

entryDelay

modArmConfig

entryPaceTest

exitPaceTest

addNetOperator

modNetOperator

delNetOperator

addNetInstaller

modNetInstaller

delNetInstaller

modCertificateStandard

Armed with Fault

Edit Arming Parameters

Entering and Exiting Delay

Edit Authentication Standard

vasiliy.chuikin@hta.kz

HTA

Edit Operator Information

Edit Installer Information

Pacing Mode Entered

Pacing Mode Exited

Delete Operator

Add Operator

Add Installer

Delete Installer

addManufacturer

modManufacturer

delManufacturer

upgradeSuccessed

upgradeFailed

zoneDisabled

localCfgSecurity

Add Manufacturer

Edit Manufacturer Information

Delete Manufacturer

Upgraded

Upgrading Failed

Zone Shielded

Security Parameter Configured Locally

remoteCfgSecurity

Security Parameter Configured Remotely

remoteGetParaSecurity

Security Parameters Obtained Remotely



<!-- page: 21 -->

Log Type

Description

delRS-485InputModule

RS-485 Zone Module Deleted

delRS-485OutputModule

RS-485 Output Module Deleted

delRS-485WirelessReceiver

RS-485 Wireless Receiver Module Deleted

enrollRS-485InputModule

RS-485 Zone Module Registered

enrollRS-485OutputModule

RS-485 Output Module Registered

delRS-485OutputModule

RS-485 Output Module Deleted

enrollRS-485WirelessReceiver

RS-485 Wireless Receiver Module Registered

scheduledAngleCalibration

enrollKeypad

delKeypad

addZone

modZone

delZone

addAlarmLine

modAlarmLine

delAlarmLine

Edited Zone

Added Zone

Keypad Deleted

Keypad Registered

Scheduled Angle Calibration

vasiliy.chuikin@hta.kz

HTA

Deleted Trigger Line

Added Trigger Line

Edited Trigger Line

Deleted Zone

remoteHFPDconfig/localHFPDconfig

remoteLFPDconfig

Remote/Local Configuration of Frequently
Appeared Person Detection

Remote Configuration of Low Frequency Person
Detection

modifyUserPassword

Password Changed

logOut

indicatorStatusSettings

wiredNetworkSettings

notificationSettings

alarmCenterSettings

Logged Out

Indicator Switch Settings

Wired Network Settings

Message Notification Settings

Alarm Receiving Center Settings

videoRecordStrategySettings

Video Recording Strategy Settings

cameraLinkageSettings

Camera Linkage Settings

armingDisarmingScheduleSettings

Arming and Disarming Schedule Settings

alarmSpeedSettings

Speed Threshold Settings for Triggering Alarms



<!-- page: 22 -->

Log Type

Description

videoTrackingSwitchSettings

Video Tracking Switching Settings

frequencySettings

Frequency Band Settings

masterSlaveTrackingSettings

Smart Linkage Settings

parkingPointSettings

administratorEdited

securityConfigured

Parking Point Settings

Administrator Parameters Edited

Security Settings

relayParametersEdited

Relay Parameters Edited

radarSensitivitySettings

detectAngandDistanceSettings

Detector Angle and Range Settings

masterSlaveRadarSettings

Main Radar and Sub Radar Settings

remoteCheckTime

Remote: Manual Time Synchronization

remoteParamSimpleDefault

Remote: Partly Restore to Default Settings

remoteParamFactoryDefault

Remote: Restore All to Default Settings

localAutoSwitchConfig

Configure Auto Power On or Off Locally

remoteAutoSwitchConfig

Configure Auto Power On or Off Remotely

Radar Sensitivity Settings

vasiliy.chuikin@hta.kz

HTA

remoteCfgWirelessDialParam

Configure wireless dial-up parameters remotely

localCfgWirelessDialParam

Configure wireless dial-up parameters locally

localCfgWirelessSmsParam

Configure wireless message parameters locally

remoteCfgWirelessSmsSelfHelp

Configure SMS self-service parameters remotely

remoteCfgWirelessSmsParam

Configure wireless message parameters remotely

localCfgWirelessSmsSelfHelp

Configure SMS self-service parameters locally

remoteCfgWirelessNetFlowParam

Configure wireless traffic parameters remotely

localCfgWirelessNetFlowParam

Configure wireless traffic parameters locally

scaleCfg

radarTrailCfg

MapImportCfg

radarCalibrationCfg

LocalEzvizOperation

RemoteEzvizOperation

Scale Settings

Radar Pattern Settings

Map Importing Settings

Radar Calibration Settings

Local EZ Operations

Remote EZ Operations



<!-- page: 23 -->

Log Type

Description

SSHEnabled

SSHDisabled

SSH Enabled

SSH Disabled

installationModeEntered

Installation Mode Enabled

installationModeExited

Installation Mode Disabled

diagnosisModeConfigured

Diagnosis Mode Configured

fileExported

audioFileUploaded

File Exported

Audio File Uploaded

audioFileDeleted

PIRCAMCapture

SIPIntercomStarted

SIPIntercomEnded

enrollmentModeEntered

enrollmentModeExited

cardReaderunlocked

cardReaderlocked

previewStart

previewStop

PIRCAM Captured

Audio File Deleted

SIP Intercom Ended

SIP Intercom Started

Registration Mode Enabled

vasiliy.chuikin@hta.kz

HTA

Registration Mode Disabled

Card Reader Unlocked

Card Reader Locked

Live View Started

Live View Stopped

videoAudioSelfCheckStarted

Self-Test of Audio and Video Started

videoAudioSelfCheckStopped

Self-Test of Audio and Video Stopped

videoAudioSelfCheckEnded

Self-Test of Audio and Video Ended

remoteDelAllVideoAnalysisTask

All Video Analysis Tasks Cleared (One-Touch)

localSSDOperateStart

localSSDOperateStop

remoteSSDOperateStart

remoteSSDOperateStop

AITargetBPAdd

AITargetBPDelete

AITargetBPSearch

Local SSD operation (firmware operations) started

Local SSD operation (firmware operations) ended

Remote SSD operation (firmware operations)
started

Remote SSD operation (firmware operations)
ended

Reference picture for AI target comparison added

Reference picture for AI target comparison deleted

Reference picture for AI target comparison AI



<!-- page: 24 -->

Log Type  Description
searched for
Reference picture for AI target comparison
AITargetBPUpdate
updated
| AIRuleConfigTrigger  | AI rule linkage configured             |     |
| -------------------- | -------------------------------------- | --- |
| AudioFileImport      | Audio file imported                    |     |
| AudioFileDownLoad    | Audio file downloaded                  |     |
| cardNoNotRegistered  | Card No. not registered                |     |
| LocalBackupConfig    | Local hot spare device zconfiguration  |     |
k
| RemoteBackupConfig  | Remote hot spare device configuration  |     |
| ------------------- | -------------------------------------- | --- |
.
a
| remoteAIModelAdd  | Model package added  | t   |
| ----------------- | -------------------- | --- |
h
| remoteAIModelQuery  | Model package searched  |     |
| ------------------- | ----------------------- | --- |
@
n
| remoteAIModelDelete  | Model package deleted  |     |
| -------------------- | ---------------------- | --- |
i
| remoteAIModelUpdate  | Mkodel package updated  |     |
| -------------------- | ----------------------- | --- |
i
uPicture polling analysis task added
remoteAIPicturePollingTaskAdd
h
remoteAIPicturePollingTaskQuery  cPicture polling analysis task searched
.
remoteAIPicturePollingTaskDeletye  PAicture polling analysis task deleted
T
i
remoteAIPicturePollingTaskM odify  HPicture polling analysis task edited
l
i
| remoteAIVideoTaskAdd  | Video analysis task added  |     |
| --------------------- | -------------------------- | --- |
s
a
| remoteAIVideoTaskQuery  | Video analysis task searched  |     |
| ----------------------- | ----------------------------- | --- |
v
| remoteAIVideoTaskDelete    | Video analysis task deleted     |     |
| -------------------------- | ------------------------------- | --- |
| remoteAIVideoTaskModify    | Video analysis task edited      |     |
| remoteAIPictureTaskAdd     | Picture analysis task added     |     |
| remoteAIPictureTaskQuery   | Picture analysis task searched  |     |
| remoteAIPictureTaskDelete  | Picture analysis task deleted   |     |
| remoteAIPictureTaskModify  | Picture analysis task edited    |     |
remoteAIVideoPollingTaskAdd  Video polling analysis task added
remoteAIVideoPollingTaskQuery  Video polling analysis task searched
remoteAIVideoPollingTaskDelete  Video polling analysis task deleted
remoteAIVideoPollingTaskModify  Video polling analysis task edited
| AIRuleConfig  | AI rule configuration  |     |
| ------------- | ---------------------- | --- |

<!-- page: 25 -->

Log Type

Description

localParamFactoryDefault

Restore to default settings locally

remoteParamFactoryDefault

Restore to default settings remotely

remoteDeleteAllVerifyOrCapPics

localDeleteAllVerifyOrCapPics

Delete all authenticated or captured face pictures
remotely

Delete all authenticated or captured face pictures
locally

remoteDeleteEventsAtSpecTime

Delete events by specified time remotely

localDeleteEventsAtSpecTime

Delete events by specified time locally

remoteOpenSummerTime

localOpenSummerTime

remoteCloseSummerTime

localCloseSummerTime

remoteEZVIZUnbind

localEZVIZUnbind

enterLocalUIBackground

Unbind from EZ cloud remotely

Enable DST locally

Disable DST locally

Enable DST remotely

Disable DST remotely

vasiliy.chuikin@hta.kz

HTA

Unbind from EZ cloud locally

Enter UI background

Enhance SVC

Remotely configure event type

SVCEnhanced

remoteEventTypeCfg

remoteDeleteFaceBaseMap

Delete registered face pictures remotely

localDeleteFaceBaseMap

Delete registered face pictures locally

remoteImportEventTableFile

Remotely import the customized list of events

remoteExportEventTableFile

Remotely export the customized list of events

Event Logs

Log Type

Description

SDKSchool

SDK Synchronization

presetsSatatusChange

Status of preset changed

selfTimeSchool

insertSubsystem

pullOutSubsystem

Time Synchronization by Schedule

Plugged in Sub-board

Pulled out Sub-board



<!-- page: 26 -->

autoArm

autoDisarm

triggerOn

triggerOff

autoArmFailed

autoDisarmFailed

triggerOnFailed

triggerOffFailed

mandatoryAlarm

keyPADlocked

keyPADunlocked

insetUSB

pulloutUSB

lateRemind

keypadUnlocked

timeSynchronization

armFailed

ARCStart

locked

Log Type

Description

Auto Arming

Auto Disarming

Activated Trigger by Schedule

Deactivated Trigger by Schedule

Auto Arming Failed

Auto Disarming Failed

Activating Trigger Failed

Forced Arming

Keypad Locked

Keypad Unlocked

Plugged in USB Flash Drive

Deactivating Trigger Failed

vasiliy.chuikin@hta.kz

HTA

Removed USB Flash Drive

Time Synchronization

Unlocked Keypad

ARC Connected

Late to Disarm

Arming Failed

Locked

Information Logs

Log Type

Description

doubleVerificationPass

Double Verification Completed

hdFormatStart

hdFormatStop

Formatting HDD Started

Formatting HDD Stopped

wirelessRunningStatus

Wireless Network Running Status

BackupInfo

addUserInfo

Hot Spare Information

Added person information (access control
permission)



<!-- page: 27 -->

Log Type

Description

modifyUserInfo

clearUserInfo

clearAllUser

ezvizLinkageInfo

Edit person information (access control permission)

Delete person information by employee No.
(access control permission)

Delete all person information (access control
permission)

EZ linkage information

vasiliy.chuikin@hta.kz

HTA

