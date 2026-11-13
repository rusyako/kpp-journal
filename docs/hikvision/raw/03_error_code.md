<!-- source_file: ISAPI/Field Dictionary (1).xlsx -->
<!-- real_content: ErrorCode (status/sub-status/error codes) -->
<!-- source_sha256: fbc5c3f4ccfbd69d6a235684387d764d6814b1037f823c6da0ae4c7d9f67a5f1 -->
<!-- converter: markitdown_mcp.convert_to_markdown (MarkItDown MCP) -->

## Sheet1
| Status Code | Status String | Sub Status Code | Error Code | Description |
| --- | --- | --- | --- | --- |
| 1.0 | OK | ok | 0x1 | Succeeded |
| 1.0 | OK | riskPassword | 0x10000002 | Risky password. |
| 1.0 | OK | MutexWithStream3 | 0x10000003 | NaN |
| 1.0 | OK | illegalPassword | 0x10000004 | Invalid password. Password cannot contain user name. |
| 1.0 | OK | restartLiveSetting | 0x10000005 | The settings will take effect after restarting the live view. |
| 1.0 | OK | wndPositionAdjusted | 0x10000006 | Window location adjusted by device. |
| 1.0 | OK | normalInternalParameterList | 0x10000007 | Existing internal parameter list is normal. No need to update internal parameter list. |
| 1.0 | OK | internalParameterUpdateSuccess | 0x10000008 | Exception occurred when checking existing internal parameter list. Internal parameter list is updated. |
| 1.0 | OK | connectedWiFiCheck | 0x10000009 | Check whether the device is successfully connected.  \nFor devices with indicators: \nIf the Wi-Fi is connected, the indicator flashes blue every 2 seconds.  \nIf the Wi-Fi connection failed, the indicator flashes blue every 0.2 seconds. Try again. |
| 1.0 | OK | timeReminder | 0x1000000A | Countdown reminder for arming delayed zone under non-arming process. |
| 2.0 | Device Busy | noMemory | 0x20000001 | Not enough memory. |
| 2.0 | Device Busy | serviceUnavailable | 0x20000002 | Service is not available. |
| 2.0 | Device Busy | upgrading | 0x20000003 | Upgrading. |
| 2.0 | Device Busy | deviceBusy | 0x20000004 | Device is busy or no response. |
| 2.0 | Device Busy | reConnectIpc | 0x20000005 | Reconnecting network camera. |
| 2.0 | Device Busy | transferUpgradePackageFailed. | 0x20000006 | Transmitting device upgrade data failed. |
| 2.0 | Device Busy | startUpgradeFailed. | 0x20000007 | Starting upgrading device failed. |
| 2.0 | Device Busy | getUpgradeProcessfailed. | 0x20000008 | Getting upgrade status failed. |
| 2.0 | Device Busy | networkError | 0x20000009 | Network error. |
| 2.0 | Device Busy | configOperating | 0x2000000A | The device is importing or exporting. |
| 2.0 | Device Busy | certificateExist | 0x2000000B | The authentication certificate already exists. |
| 2.0 | Device Busy | formatting | 0x2000000C | NaN |
| 2.0 | Device Busy | batchAddDeviceNow | 0x2000000D | Batch adding devices. |
| 2.0 | Device Busy | searchTimeout | 0x2000000E | Searching timed out. Narrow search range. |
| 3.0 | Device Error | deviceError | 0x30000001 | Device hardware error. |
| 3.0 | Device Error | badFlash | 0x30000002 | Flash operation error. |
| 3.0 | Device Error | 28181Uninitialized | 0x30000003 | 28181 is not initialized. |
| 3.0 | Device Error | createSocketError | 0x30000004 | Creating socket failed. |
| 3.0 | Device Error | socketConnectError | 0x30000005 | Connecting to socket failed. |
| 3.0 | Device Error | sendRequestError | 0x30000006 | Sending request failed. |
| 3.0 | Device Error | receiveError | 0x30000007 | Receiving response message failed. |
| 3.0 | Device Error | passwordDecodeError | 0x30000008 | Decrypting password failed. |
| 3.0 | Device Error | passwordEncryptError | 0x30000009 | Encrypting password failed. |
| 3.0 | Device Error | deletePictureError | 0x3000000A | Deleting picture failed. |
| 3.0 | Device Error | pictureUploadFailed | 0x3000000B | Uploading picture failed. |
| 3.0 | Device Error | pictureSizeExceedLimit | 0x3000000C | Picture size exceeded limit. |
| 3.0 | Device Error | clearCacheError | 0x3000000D | Clearing cache failed. |
| 3.0 | Device Error | connecteDatabaseError | 0x3000000E | Connecting to database failed. |
| 3.0 | Device Error | updateDatabasError | 0x3000000F | Updating database failed. |
| 3.0 | Device Error | searchDatabaseError | 0x30000010 | Searching in the database failed. |
| 3.0 | Device Error | writeDatabaseError | 0x30000011 | Writing to database failed. |
| 3.0 | Device Error | deleteDatabaseError | 0x30000012 | Deleting database element failed. |
| 3.0 | Device Error | searchDatabaseElementError | 0x30000013 | Getting number of database elements failed. |
| 3.0 | Device Error | internalError | 0x30000014 | System error. |
| 3.0 | Device Error | diskError | 0x30000015 | HDD error. |
| 3.0 | Device Error | cloudAutoUpgradeException | 0x30000016 | Downloading upgrade package from cloud and upgrading failed. |
| 3.0 | Device Error | fileSizeExceedLimit | 0x30000017 | File size exceeded limit. |
| 3.0 | Device Error | fileTypeError | 0x30000018 | File type error. |
| 3.0 | Device Error | upgradeError | 0x30000019 | Upgrading failed. |
| 3.0 | Device Error | upgradeErrorAndReboot | 0x3000001a | Upgrading failed and device restarted. |
| 3.0 | Device Error | HBPException | 0x30001000 | HBP exception. |
| 3.0 | Device Error | UDEPException | 0x30001001 | UDEP exception |
| 3.0 | Device Error | elasticSearchException | 0x30001002 | Elastic exception. |
| 3.0 | Device Error | kafkaException | 0x30001003 | Kafka exception. |
| 3.0 | Device Error | HBaseException | 0x30001004 | Hbase exception. |
| 3.0 | Device Error | sparkException | 0x30001005 | Spark exception. |
| 3.0 | Device Error | yarnException | 0x30001006 | Yarn exception. |
| 3.0 | Device Error | cacheException | 0x30001007 | Cache exception. |
| 3.0 | Device Error | trafficException | 0x30001008 | Monitoring point big data server exception. |
| 3.0 | Device Error | faceException | 0x30001009 | Face big data server exception. |
| 3.0 | Device Error | wifiException | 0x3000100A | Wi-Fi big data server exception. |
| 3.0 | Device Error | uninitialized | 0x3000100C | Uninitialized. |
| 3.0 | Device Error | structException | 0x3000100D | Video structurization server exception. |
| 3.0 | Device Error | SSDFileSystemIsUpgrading | 0x3000100E | SSD file system is upgrading. |
| 3.0 | Device Error | SSDFileSystemNoDisk | 0x3000100F | Repairing SSD file system failed. No backup HDD. |
| 3.0 | Device Error | SSDFileSystemDiskfull | 0x30001010 | Repairing SSD file system failed. Backup HDD full. |
| 3.0 | Device Error | SSDFileSystemBackupfailure | 0x30001011 | Repairing SSD file system failed. Data backup failed. |
| 3.0 | Device Error | SSDFileSystemIsFormat | 0x30001012 | SSD is formatting. |
| 3.0 | Device Error | SSDFileSystemIsError | 0x30001013 | SSD file system error (error occurred when it is non-Ext4 file system). |
| 3.0 | Device Error | insufficientSSDCapacityForFPD | 0x30001014 | Not enough SSD space for person frequency detection. |
| 3.0 | Device Error | noLinkageResource | 0x30001015 | Not enough linkage resources. |
| 3.0 | Device Error | noArmingResource | 0x30001016 | Not enough arming resources. |
| 3.0 | Device Error | noSDCard | 0x30002011 | No SD card. |
| 3.0 | Device Error | pictureDeleted | 0x30002012 | The picture is deleted. |
| 3.0 | Device Error | mirrorAndEISEnabled | 0x30002013 | Mirror and EIS can not be enabled at the same time. |
| 3.0 | Device Error | manualPTZLock | 0x30002014 | This channel is in motion locked status. Unlock it first. |
| 3.0 | Device Error | engineAbnormal | 0x30002015 | Engine Exception |
| 3.0 | Device Error | engineInitialization | 0x30002016 | Initializing engine… |
| 3.0 | Device Error | algorithmLoadingFailed | 0x30002017 | Loading model failed. |
| 3.0 | Device Error | algorithmDownloadFailed | 0x30002018 | Downloading model failed. |
| 3.0 | Device Error | algorithmDecryptionFailed | 0x30002019 | Decrypting model failed. |
| 3.0 | Device Error | unboundChannel | 0x30002020 | Channel(s) must be unbound before new model(s) can be added. |
| 3.0 | Device Error | unsupportedResolution | 0x30002021 | Resolution is not supported. |
| 3.0 | Device Error | unsupportedSteamType | 0x30002022 | Stream type is not supported. |
| 3.0 | Device Error | insufficientDecRes | 0x30002023 | Not enough decoding resources. |
| 3.0 | Device Error | insufficientEnginePerformance | 0x30002024 | Not enough engine resources. Number of channels to be analyzed exceeded limit. |
| 3.0 | Device Error | improperResolution | 0x30002025 | Picture resolution exceeded limit (4096\*4096). |
| 3.0 | Device Error | improperPicSize | 0x30002026 | Picture size exceeded limit (5M). |
| 3.0 | Device Error | URLDownloadFailed | 0x30002027 | Downloading picture failed. |
| 3.0 | Device Error | unsupportedImageFormat | 0x30002028 | Invalid format of uploaded picture. Upload pictures in the format of JPG. |
| 3.0 | Device Error | unsupportedPollingIntervalTime | 0x30002029 | Auto-switch interval should be longer than 10 seconds. |
| 3.0 | Device Error | exceedImagesNumber | 0x30002030 | Number of pictures exceeded limit (100). |
| 3.0 | Device Error | unsupportedMPID | 0x30002031 | Updating failed. The MPID does not exist in device. |
| 3.0 | Device Error | modelPackageNotMatchLabel | 0x30002032 | Model and description file mismatch. |
| 3.0 | Device Error | modelPackageNotMatchTask | 0x30002033 | Task and model type mismatch. |
| 3.0 | Device Error | insufficientSpace | 0x30002034 | Adding failed. Not enough memory fpr the model package. |
| 3.0 | Device Error | engineUnLoadingModelPackage | 0x30002035 | Applying task failed. The engine is not bound with a model. |
| 3.0 | Device Error | engineWithModelPackage | 0x30002036 | Binding failed: The engine has already been bound to model. Unbind first. |
| 3.0 | Device Error | modelPackageDelete | 0x30002037 | Binding failed: The model has already been deleted. |
| 3.0 | Device Error | deleteTaskFailed | 0x30002038 | Stopping the task failed. |
| 3.0 | Device Error | modelPackageNumberslimited | 0x30002039 | Adding model package failed: Number of model packages exceeded limit. |
| 3.0 | Device Error | modelPackageDeleteFailed | 0x30002040 | Deleting model package failed. |
| 3.0 | Device Error | noDeletionAllowed | 0x30002041 | Deleting failed. Model package is running. |
| 3.0 | Device Error | licensKeyMissing | 0x30002042 | License file is required. |
| 3.0 | Device Error | checkFailure | 0x30002043 | Verification failed. No permission. |
| 3.0 | Device Error | LicenskeyFileMismatch | 0x30002044 | Licensekey file mismatch. |
| 3.0 | Device Error | ModelLoading | 0x30002045 | Loading model… |
| 3.0 | Device Error | ChannelNoIEDRule | 0x30002046 | No IED rule is configured to this channel. |
| 3.0 | Device Error | ChannelNotMatchTask ID | 0x30002047 | Channel and task ID mismatch. The task is not configured to the channel. |
| 3.0 | Device Error | EngineNotMatchTask ID | 0x30002048 | Engine and task ID mismatch. The task is not configured to the engine. |
| 3.0 | Device Error | EngineNotRunning | 0x30002049 | Task on the engine is not running normally or the engine has not started running. |
| 3.0 | Device Error | TaskIDNotExist | 0x30002050 | Sending picture failed. Task ID does not exist. |
| 3.0 | Device Error | calibrationTimeout | 0x30002051 | Calibration timed out. |
| 3.0 | Device Error | rebootTheCascadingDeviceAfterUpgraded | 0x30002052 | Restart the device manually after upgrading cascading device to prevent it from being disconnected from network. |
| 3.0 | Device Error | ModelSchedulingFailure | 0x30002053 | Operating AI algorithm model package failed. |
| 3.0 | Device Error | ModelSchedulingConfigFailure | 0x30002054 | Task is in process. Configuring dispatch model failed. |
| 3.0 | Device Error | streamDealError | 0x30005000 | Handling stream data failed. |
| 3.0 | Device Error | captureTimeout | 0x30006000 | Data collection timed out. |
| 3.0 | Device Error | lowScore | 0x30006001 | Low quality of collected data. |
| 3.0 | Device Error | certificateNotmatch | 0x30006002 | Certificate mismatch. SSL/TLS public and private key certificates should be matched in pairs. |
| 3.0 | Device Error | deviceAckTimeOut | 0x30006003 | Device response timed out. |
| 3.0 | Device Error | notFindStorageMedium | 0x30006004 | No storage device is found. |
| 3.0 | Device Error | securityModuleOffline | 0x30006005 | Access control module disconnected. Opening door failed. |
| 3.0 | Device Error | moduleHandleFailed | 0x30006006 | Processing module command failed. |
| 3.0 | Device Error | moduleConnectFailed | 0x30006007 | Connecting to module failed. |
| 3.0 | Device Error | fingerPrintFeatureMergeFailed | 0x30006008 | Merging modules or algorithm templates failed when calling teh API during the collection. |
| 3.0 | Device Error | moduleIllegalParamter | 0x30006009 | Invalid module parameter. |
| 3.0 | Device Error | fingerPrintFeatureNumInvalid | 0x3000600A | Invalid number of merged modules or algorithm fingerprints when calling the API during the collection. |
| 3.0 | Device Error | fingerPrintLowQulity | 0x3000600B | Low quality of fingerprint when calling the API during the collection. |
| 3.0 | Device Error | upgradeObjectNoSupport | 0x3000600C | Upgrade object is not supported. |
| 3.0 | Device Error | upgradeObjectNoOline | 0x3000600D | Upgrade object is offline. |
| 3.0 | Device Error | upgradeDataErrLength | 0x3000600E | Upgrade package data length exception. |
| 3.0 | Device Error | hardDiskError | 0x3000600F | HDD exception (possible reasons: HDD does not exist, incompatible, encrypted, not enough capacity, formatting exception, array exception, array incompatible, etc.) |
| 3.0 | Device Error | fileSizeExceedError | 0x30006010 | Applying face picture failed. File size exceeded limit. |
| 3.0 | Device Error | receiveUpgradePackageError | 0x30006011 | Receiving upgrade package failed. |
| 3.0 | Device Error | upgradeFailed | 0x30006012 | Upgrading failed. |
| 3.0 | Device Error | noStorageSpace | 0x30007000 | Not enough file space. |
| 3.0 | Device Error | invalidInstallationFile | 0x30007001 | Invalid installation file. |
| 3.0 | Device Error | androidSysError | 0x30007002 | System error. |
| 3.0 | Device Error | noPermissionUninstall | 0x30007003 | No uninstallation permission. |
| 3.0 | Device Error | uploadingFailed | 0x30007004 | Uploading failed |
| 3.0 | Device Error | noPTOFile | 0x30007005 | Calibration file (.pto) is required. |
| 3.0 | Device Error | RS485ConnectFail | 0x30008000 | Communicating with RS-485 series port failed. |
| 4.0 | Invalid Operation | notSupport | 0x40000001 | Not supported. |
| 4.0 | Invalid Operation | lowPrivilege | 0x40000002 | No permission. |
| 4.0 | Invalid Operation | badAuthorization | 0x40000003 | Authentication failed. |
| 4.0 | Invalid Operation | methodNotAllowed | 0x40000004 | Invalid HTTP method. |
| 4.0 | Invalid Operation | notSetHdiskRedund | 0x40000005 | Setting spare HDD failed. |
| 4.0 | Invalid Operation | invalidOperation | 0x40000006 | Invalid input command. |
| 4.0 | Invalid Operation | notActivated | 0x40000007 | Inactivated. |
| 4.0 | Invalid Operation | hasActivated | 0x40000008 | Activated. |
| 4.0 | Invalid Operation | certificateAlreadyExist | 0x40000009 | Certificate already exists. |
| 4.0 | Invalid Operation | invalidContent | 0x4000000A | Invalid message. |
| 4.0 | Invalid Operation | maxSessionUserLink | 0x4000000B | Number of users exceeded limit. |
| 4.0 | Invalid Operation | loginPasswordError | 0x4000000C | Incorrect login password. |
| 4.0 | Invalid Operation | maxPreviewCount | 0x4000000D | Number of live view channels exceeded limit. |
| 4.0 | Invalid Operation | 3DModelNotSupport | 0x4000000E | The operation is not supported in 3D mode. |
| 4.0 | Invalid Operation | fileError | 0x4000000F | Incorrect upgrading file. |
| 4.0 | Invalid Operation | USBNotExist | 0x40000010 | USB device is not connected. |
| 4.0 | Invalid Operation | logFileNotExist | 0x40000011 | Log file does not exist. |
| 4.0 | Invalid Operation | gainPPPoEError | 0x40000012 | Getting PPPoE parameter failed. |
| 4.0 | Invalid Operation | configPPPoEError | 0x40000013 | Setting PPPoE parameter failed. |
| 4.0 | Invalid Operation | gainDHCPServerError | 0x40000014 | Getting DHCPServer parameter failed. |
| 4.0 | Invalid Operation | configDHCPServerError | 0x40000015 | Setting DHCPServer parameter failed. |
| 4.0 | Invalid Operation | testReportExcept | 0x40000016 | Network detection report is not generated normally. |
| 4.0 | Invalid Operation | uncertifiedDevice | 0x40000017 | Unauthorized device. |
| 4.0 | Invalid Operation | bitRateExceedLimited | 0x40000018 | Bit rate exceeded limit. |
| 4.0 | Invalid Operation | verifyError | 0x40000019 | Verification failed. |
| 4.0 | Invalid Operation | canotWakeUpWhenNotStandby | 0x4000001A | Cannot be awaken. Not standby. |
| 4.0 | Invalid Operation | canotStandbyWhenStandby | 0x4000001B | Cannot be standby. Already standby. |
| 4.0 | Invalid Operation | upgradePackageMorethan2GB | 0x40001000 | Upgrade packages to be uploaded cannot be larger than 2 GB. |
| 4.0 | Invalid Operation | IDNotexist | 0x40001001 | ID does not exist. |
| 4.0 | Invalid Operation | interfaceOperationError | 0x40001002 | API operation failed. |
| 4.0 | Invalid Operation | synchronizationError | 0x40001003 | Synchronization failed. |
| 4.0 | Invalid Operation | synchronizing | 0x40001004 | Synchronizing… |
| 4.0 | Invalid Operation | importError | 0x40001005 | Importing failed. |
| 4.0 | Invalid Operation | importing | 0x40001006 | Importing... |
| 4.0 | Invalid Operation | fileAlreadyExists | 0x40001007 | File already exists. |
| 4.0 | Invalid Operation | invalidID | 0x40001008 | Invalid ID. |
| 4.0 | Invalid Operation | backupnodeNotAlloweLog | 0x40001009 | Accessing backup node is not allowed. |
| 4.0 | Invalid Operation | exportingError | 0x4000100A | Exporting failed. |
| 4.0 | Invalid Operation | exporting | 0x4000100B | Exporting... |
| 4.0 | Invalid Operation | exportEnded | 0x4000100C | Exporting stopped. |
| 4.0 | Invalid Operation | exported | 0x4000100D | Exported. |
| 4.0 | Invalid Operation | IPOccupied | 0x4000100E | IP address is already occupied. |
| 4.0 | Invalid Operation | IDAlreadyExists | 0x4000100F | ID No. already exists. |
| 4.0 | Invalid Operation | exportItemsExceedLimit | 0x40001010 | No more items can be exported. |
| 4.0 | Invalid Operation | noFiles | 0x40001011 | File does not exist. |
| 4.0 | Invalid Operation | beingExportedByAnotherUser | 0x40001012 | Being exported by others. |
| 4.0 | Invalid Operation | needReAuthentication | 0x40001013 | Authentication is required after upgrade. |
| 4.0 | Invalid Operation | openFileError | 0x40001014 | Opening file failed. |
| 4.0 | Invalid Operation | unitAddNotOnline | 0x40001015 | The added data analysis server is offline. |
| 4.0 | Invalid Operation | unitControl | 0x40001016 | The data analysis server is already added. |
| 4.0 | Invalid Operation | unitFull | 0x40001017 | No more data analysis server can be added. |
| 4.0 | Invalid Operation | unitIDError | 0x40001018 | The data analysis server ID does not exist. |
| 4.0 | Invalid Operation | unitExit | 0x40001019 | The data analysis server already exists in the list. |
| 4.0 | Invalid Operation | unitSearch | 0x4000101A | Searching data analysis server in the list failed. |
| 4.0 | Invalid Operation | unitNotOnline | 0x4000101B | The data analysis server is offline. |
| 4.0 | Invalid Operation | unitInfoEror | 0x4000101C | Getting data analysis server information failed. |
| 4.0 | Invalid Operation | unitGetNodeInfoError | 0x4000101D | Getting node information failed. |
| 4.0 | Invalid Operation | unitGetNetworkInfoError | 0x4000101E | Getting network information of data analysis server failed |
| 4.0 | Invalid Operation | unitSetNetworkInfoError | 0x4000101F | Setting network information of data analysis server failed |
| 4.0 | Invalid Operation | setSmartNodeInfoError | 0x40001020 | Setting node information failed. |
| 4.0 | Invalid Operation | setUnitNetworkInfoError | 0x40001021 | Setting data analysis server network information failed. |
| 4.0 | Invalid Operation | unitRestartCloseError | 0x40001022 | Rebooting or shutting down analysis server failed. |
| 4.0 | Invalid Operation | virtualIPnotAllowed | 0x40001023 | Adding virtual IP address is not allowed. |
| 4.0 | Invalid Operation | unitInstalled | 0x40001024 | The data analysis server is already installed. |
| 4.0 | Invalid Operation | badSubnetMask | 0x40001025 | Invalid subnet mask. |
| 4.0 | Invalid Operation | uintVersionMismatched | 0x40001026 | Data analysis server version mismatch. |
| 4.0 | Invalid Operation | deviceMOdelMismatched | 0x40001027 | Adding failed. Device model mismatch. |
| 4.0 | Invalid Operation | unitAddNotSelf | 0x40001028 | Adding peripherals is not allowed. |
| 4.0 | Invalid Operation | noValidUnit | 0x40001029 | No valid data analysis server. |
| 4.0 | Invalid Operation | unitNameDuplicate | 0x4000102A | Duplicate data analysis server name. |
| 4.0 | Invalid Operation | deleteUnitFirst | 0x4000102B | Delete the added data analysis server of the node first. |
| 4.0 | Invalid Operation | getLocalInfoFailed | 0x4000102C | Getting server information failed. |
| 4.0 | Invalid Operation | getClientAddedNodeFailed | 0x4000102D | Failed to get information of nodes where data analysis servers are added. |
| 4.0 | Invalid Operation | taskExit | 0x4000102E | Task already exists. |
| 4.0 | Invalid Operation | taskInitError | 0x4000102F | Initializing task failed. |
| 4.0 | Invalid Operation | taskSubmitError | 0x40001030 | Submitting task failed. |
| 4.0 | Invalid Operation | taskDelError | 0x40001031 | Deleting task failed. |
| 4.0 | Invalid Operation | taskPauseError | 0x40001032 | Pausing task failed. |
| 4.0 | Invalid Operation | taskContinueError | 0x40001033 | Starting task failed. |
| 4.0 | Invalid Operation | taskPacking | 0x40001034 | Resource occupied. |
| 4.0 | Invalid Operation | taskSeverNoCfg | 0x40001035 | Full-text search server is not configured. |
| 4.0 | Invalid Operation | taskPicSeverNoCfg | 0x40001036 | Picture server is not configured. |
| 4.0 | Invalid Operation | taskStreamError | 0x40001037 | Streaming information exception. |
| 4.0 | Invalid Operation | taskRecSDK | 0x40001038 | History recording is not supported. |
| 4.0 | Invalid Operation | taskNoRecFile | 0x40001039 | Video file does not exist. |
| 4.0 | Invalid Operation | taskCasaError | 0x4000103A | Cascading is not supported. |
| 4.0 | Invalid Operation | taskVCARuleError | 0x4000103B | Invalid VCA rule. |
| 4.0 | Invalid Operation | taskNoRun | 0x4000103C | Task is not executed. |
| 4.0 | Invalid Operation | unitLinksNoStorageNode | 0x4000103D | No node is linked with the data analysis server. Configure node first. |
| 4.0 | Invalid Operation | searchFailed | 0x4000103E | Searching video files failed. |
| 4.0 | Invalid Operation | searchNull | 0x4000103F | No video file. |
| 4.0 | Invalid Operation | userScheOffline | 0x40001040 | The task scheduler service is offline. |
| 4.0 | Invalid Operation | updateTypeUnmatched | 0x40001041 | Upgrade package type mismatch. |
| 4.0 | Invalid Operation | updateLangUnmatched | 0x40001042 | Language of upgrading package mismatch. |
| 4.0 | Invalid Operation | userExist | 0x40001043 | User already exists. |
| 4.0 | Invalid Operation | userCannotDelAdmin | 0x40001044 | Administrator cannot be deleted. |
| 4.0 | Invalid Operation | userInexistence | 0x40001045 | User name does not exist. |
| 4.0 | Invalid Operation | userCannotCreatAdmin | 0x40001046 | Administrator cannot be created. |
| 4.0 | Invalid Operation | userMaxNum | 0x40001047 | No more users can be added. |
| 4.0 | Invalid Operation | monitorCamExceed | 0x40001048 | Up to 3000 cameras can be added. |
| 4.0 | Invalid Operation | monitorCunitOverLimit | 0x40001049 | Adding failed. Up to 5 lower-levels are supported by control center. |
| 4.0 | Invalid Operation | monitorReginOverLimit | 0x4000104A | Adding failed. Up to 5 lower-levels are supported by the area. |
| 4.0 | Invalid Operation | monitorArming | 0x4000104B | The camera is already armed. Disarm the camera and try again. |
| 4.0 | Invalid Operation | monitorSyncCfgNotSet | 0x4000104C | The system parameters are not configured. |
| 4.0 | Invalid Operation | monitorNodeOverLimit | 0x4000104D | Adding failed. Upper limit reached. |
| 4.0 | Invalid Operation | monitorFdSyncing | 0x4000104E | Synchronizing FD. Try again after completing the synchronization. |
| 4.0 | Invalid Operation | monitorParseFailed | 0x4000104F | Parsing camera information failed. |
| 4.0 | Invalid Operation | monitorCreatRootFailed | 0x40001050 | Creating resource node failed. |
| 4.0 | Invalid Operation | deleteArmingInfo | 0x40001051 | Camera is arming. Delete arming information and try again. |
| 4.0 | Invalid Operation | cannotModify | 0x40001052 | Editing is not allowed. Select again. |
| 4.0 | Invalid Operation | cannotDel | 0x40001053 | Deletion is not allowed. Select again. |
| 4.0 | Invalid Operation | deviceExist | 0x40001054 | Device already exists. |
| 4.0 | Invalid Operation | pwdErrorLoginFailed | 0x40001055 | Login failed. Check user name and password. |
| 4.0 | Invalid Operation | IPErrorConnectFailed | 0x40001056 | Connection failed. Check network port. |
| 4.0 | Invalid Operation | cannotAdd | 0x40001057 | Only capture cameras can be added. |
| 4.0 | Invalid Operation | serverExist | 0x40001058 | Server already exists. |
| 4.0 | Invalid Operation | fullTextParamError | 0x40001059 | Incorrect full-text search parameters. |
| 4.0 | Invalid Operation | storParamError | 0x4000105A | Incorrect storage server parameters. |
| 4.0 | Invalid Operation | picServerFull | 0x4000105B | Picture storage server is full. |
| 4.0 | Invalid Operation | NTPUnconnect | 0x4000105C | Connecting to NTP server failed. Check the parameters. |
| 4.0 | Invalid Operation | storSerConnectFailed | 0x4000105D | Connecting to storage server failed. Check the network port. |
| 4.0 | Invalid Operation | storSerLoginFailed | 0x4000105E | Logging in to storage server failed. Check the user name and password. |
| 4.0 | Invalid Operation | searchSerConnectFailed | 0x4000105F | Connecting to full-text search server failed. Check the network port. |
| 4.0 | Invalid Operation | searchSerLoginFailed | 0x40001060 | Logging in to full-text search server failed. Check the user name and password. |
| 4.0 | Invalid Operation | kafkaConnectFailed | 0x40001061 | Connecting to Kafka failed. Check the network port. |
| 4.0 | Invalid Operation | mgmtConnectFailed | 0x40001062 | Connecting to system failed. Check the network port. |
| 4.0 | Invalid Operation | mgmtLoginFailed | 0x40001063 | Logging in to system failed. Check the user name and password. |
| 4.0 | Invalid Operation | TDAConnectFailed | 0x40001064 | Connecting to traffic data access server failed. Checking the server status. |
| 4.0 | Invalid Operation | 86sdkConnectFailed | 0x40001065 | Connecting to listening port of iVMS-8600 System failed. Check the parameters. |
| 4.0 | Invalid Operation | nameExist | 0x40001066 | Duplicate server name. |
| 4.0 | Invalid Operation | batchProcessFailed | 0x40001067 | Batch processing failed. |
| 4.0 | Invalid Operation | IDNotExist | 0x40001068 | The server ID does not exist. |
| 4.0 | Invalid Operation | serviceNumberReachesLimit. | 0x40001069 | Number of servers reached limit. |
| 4.0 | Invalid Operation | invalidServiceType. | 0x4000106A | Invalid service type. |
| 4.0 | Invalid Operation | clusterGetInfo | 0x4000106B | Getting cluster group information failed. |
| 4.0 | Invalid Operation | clusterDelNode | 0x4000106C | Deleting node failed. |
| 4.0 | Invalid Operation | clusterAddNode | 0x4000106D | Adding node failed. |
| 4.0 | Invalid Operation | clusterInstalling | 0x4000106E | Creating cluster… Do not operate. |
| 4.0 | Invalid Operation | clusterUninstall | 0x4000106F | Resetting cluster… Do not operate. |
| 4.0 | Invalid Operation | clusterInstall | 0x40001070 | Creating cluster failed. |
| 4.0 | Invalid Operation | clusterIpError | 0x40001071 | Invalid IP address of task scheduler server. |
| 4.0 | Invalid Operation | clusterNotSameSeg | 0x40001072 | Main node and sub node must be on the same network segment. |
| 4.0 | Invalid Operation | clusterVirIpError | 0x40001073 | Automatically getting virtual IP address failed. Enter it manually. |
| 4.0 | Invalid Operation | clusterNodeUnadd | 0x40001074 | Specified main (sub) node is not added. |
| 4.0 | Invalid Operation | clusterNodeOffline | 0x40001075 | Task scheduler server is offline. |
| 4.0 | Invalid Operation | nodeNotCurrentIP | 0x40001076 | Analysis node of the current IP address is required when adding main and sub nodes. |
| 4.0 | Invalid Operation | addNodeNetFailed | 0x40001077 | Adding node failed. Network disconnected. |
| 4.0 | Invalid Operation | needTwoMgmtNode | 0x40001078 | Two management nodes are required when adding main and sub nodes. |
| 4.0 | Invalid Operation | ipConflict | 0x40001079 | Virtual IP address and data analysis server's IP address conflict. |
| 4.0 | Invalid Operation | ipUsed | 0x4000107A | Virtual IP address has been occupied. |
| 4.0 | Invalid Operation | cloudAlalyseOnline | 0x4000107B | The cloud analytic server is online. |
| 4.0 | Invalid Operation | virIP&mainIPnotSameNetSegment | 0x4000107C | Virtual IP address is not on the same network segment with the IP address of master/slave node. |
| 4.0 | Invalid Operation | getNodeDispatchInfoFailed | 0x4000107D | Getting node scheduler information failed. |
| 4.0 | Invalid Operation | unableModifyManagementNetworkIP | 0x4000107E | Editing management network interface failed. Analysis board is in the cluster. |
| 4.0 | Invalid Operation | notSpecifyVirtualIP | 0x4000107F | Virtual IP address should be specified for main and sub cluster. |
| 4.0 | Invalid Operation | armingFull | 0x40001080 | No more device can be armed. |
| 4.0 | Invalid Operation | armingNoFind | 0x40001081 | Arming information does not exist. |
| 4.0 | Invalid Operation | disArming | 0x40001082 | Disarming failed. |
| 4.0 | Invalid Operation | setArmingError | 0x40001083 | Setting arming information failed. |
| 4.0 | Invalid Operation | getArmingError | 0x40001084 | Obtaining arming information failed. |
| 4.0 | Invalid Operation | refreshArmingError | 0x40001085 | Refreshing arming information failed. |
| 4.0 | Invalid Operation | ArmingPlateSame | 0x40001086 | The license plate number is repeatedly armed. |
| 4.0 | Invalid Operation | ArmingParseXLSError | 0x40001087 | Parsing arming information file failed. |
| 4.0 | Invalid Operation | ArmingTimeError | 0x40001088 | Invalid arming time period. |
| 4.0 | Invalid Operation | ArmingSearchTimeError | 0x40001089 | Invalid searching time period. |
| 4.0 | Invalid Operation | armingRelationshipReachesLimit | 0x4000108A | No more arming relation can be created. |
| 4.0 | Invalid Operation | duplicateAarmingName | 0x4000108B | The arming relation name already exists. |
| 4.0 | Invalid Operation | noMoreArmingListAdded | 0x4000108C | No more blocklist library can be armed. |
| 4.0 | Invalid Operation | noMoreCamerasAdded | 0x4000108D | No more camera can be armed. |
| 4.0 | Invalid Operation | noMoreArmingListAddedWithCamera | 0x4000108E | No more arming relation can be linked to the camera. |
| 4.0 | Invalid Operation | noMoreArmingPeriodAdded | 0x4000108F | No more time period can be added to the arming schedule. |
| 4.0 | Invalid Operation | armingPeriodsOverlapped | 0x40001090 | The time periods in the arming schedule are overlapped. |
| 4.0 | Invalid Operation | noArmingAlarmInfo | 0x40001091 | Alarm information does not exist. |
| 4.0 | Invalid Operation | armingAlarmUnRead | 0x40001092 | Getting number of unread alarms failed. |
| 4.0 | Invalid Operation | getArmingAlarmError | 0x40001093 | Getting alarm information failed. |
| 4.0 | Invalid Operation | searchByPictureTimedOut | 0x40001094 | Searching picture by picture timeout. Search again. |
| 4.0 | Invalid Operation | comparisonTimeRangeError | 0x40001095 | Comparison time period error. |
| 4.0 | Invalid Operation | selectMonitorNumberUpperLimit | 0x40001096 | No more monitoring point ID can be filtered. |
| 4.0 | Invalid Operation | noMoreComparisonTasksAdded | 0x40001097 | No more comparison task can be executed at the same time. |
| 4.0 | Invalid Operation | GetComparisonResultFailed | 0x40001098 | Getting comparison result failed. |
| 4.0 | Invalid Operation | comparisonTypeError | 0x40001099 | Comparison type error. |
| 4.0 | Invalid Operation | comparisonUnfinished | 0x4000109A | Comparison is not completed. |
| 4.0 | Invalid Operation | facePictureModelInvalid | 0x4000109B | Invalid face model. |
| 4.0 | Invalid Operation | duplicateLibraryName. | 0x4000109C | Library name already exists. |
| 4.0 | Invalid Operation | noRecord | 0x4000109D | No record found. |
| 4.0 | Invalid Operation | countingRecordsFailed. | 0x4000109E | Calculating number of records failed. |
| 4.0 | Invalid Operation | getHumanFaceFrameFailed | 0x4000109F | Getting face frame from picture failed. |
| 4.0 | Invalid Operation | modelingFailed. | 0x400010A0 | Modeling face according to picture URL failed. |
| 4.0 | Invalid Operation | 1V1FacePictureComparisonFailed | 0x400010A1 | 1 VS 1 face picture comparison failed. |
| 4.0 | Invalid Operation | libraryArmed | 0x400010A2 | Blocklist library is armed. |
| 4.0 | Invalid Operation | licenseExeedLimit | 0x400010A3 | Dongle limit. |
| 4.0 | Invalid Operation | licenseExpired | 0x400010A4 | Dongle expired. |
| 4.0 | Invalid Operation | licenseDisabled | 0x400010A5 | Unavailable dongle. |
| 4.0 | Invalid Operation | licenseNotExist | 0x400010A6 | Dongle does not exist. |
| 4.0 | Invalid Operation | SessionExpired | 0x400010A7 | Session expired. |
| 4.0 | Invalid Operation | beyondConcurrentLimit | 0x400010A8 | Exceeded concurrent limit. |
| 4.0 | Invalid Operation | stopSync | 0x400010A9 | Synchronization stopped. |
| 4.0 | Invalid Operation | getProgressFaild | 0x400010AA | Getting progress failed. |
| 4.0 | Invalid Operation | uploadExtraCaps | 0x400010AB | No more files can be uploaded. |
| 4.0 | Invalid Operation | timeRangeError | 0x400010AC | Time period error. |
| 4.0 | Invalid Operation | dataPortNotConnected | 0x400010AD | Data port is not connected. |
| 4.0 | Invalid Operation | addClusterNodeFailed | 0x400010AE | Adding to cluster failed. The device is already added to another cluster. |
| 4.0 | Invalid Operation | taskNotExist | 0x400010AF | Task does not exist. |
| 4.0 | Invalid Operation | taskQueryFailed | 0x400010B0 | Searching task failed. |
| 4.0 | Invalid Operation | taskModifyFailed | 0x400010B1 | Task modification failed. |
| 4.0 | Invalid Operation | modifyTimeRuleFailed | 0x400010B2 | Task already exists. Editing time rule is not allowed. |
| 4.0 | Invalid Operation | modifySmartRuleFailed | 0x400010B3 | The task already exists. Editing VAC rule is not allowed. |
| 4.0 | Invalid Operation | queryHistoryVideoFailed | 0x400010B4 | Searching history video(s) failed. |
| 4.0 | Invalid Operation | addDeviceFailed | 0x400010B5 | Adding device(s) failed. |
| 4.0 | Invalid Operation | addVideoFailed | 0x400010B6 | Adding video files failed. |
| 4.0 | Invalid Operation | deleteAllVideoFailed | 0x400010B7 | Deleting all video files failed. |
| 4.0 | Invalid Operation | createVideoIndexFailed | 0x400010B8 | Indexing video files failed. |
| 4.0 | Invalid Operation | videoCheckTypeFailed | 0x400010B9 | Verifying video files types failed. |
| 4.0 | Invalid Operation | configStructuredAddressFailed | 0x400010BA | Configuring a structuralization server address to forwarding server failed. |
| 4.0 | Invalid Operation | configPictureServerAddressFailed | 0x400010BB | Configuring a picture server address to forwarding server failed. |
| 4.0 | Invalid Operation | getDeviceInfoFailed | 0x400010BC | Getting the device information failed. |
| 4.0 | Invalid Operation | storageServiceIPNotExist | 0x400010BD | The storage server IP address does not exist. |
| 4.0 | Invalid Operation | syncBackupDatabaseFailed | 0x400010BE | Synchronizing standby server database failed. Please try again. |
| 4.0 | Invalid Operation | syncBackupNTPTimeFailed | 0x400010BF | Synchronizing NTP time of the standby server failed. |
| 4.0 | Invalid Operation | clusterNotSelectLoopbackAddress | 0x400010C0 | Loopback address is not applicable to the main and backup cluster. |
| 4.0 | Invalid Operation | addFaceRecordFailed | 0x400010C1 | Adding the face record failed. |
| 4.0 | Invalid Operation | deleteFaceRecordFailed | 0x400010C2 | Deleting the face record failed. |
| 4.0 | Invalid Operation | modifyFaceRecordFailed | 0x400010C3 | Editing the face record failed. |
| 4.0 | Invalid Operation | queryFaceRecordFailed | 0x400010C4 | Searching face record(s) failed. |
| 4.0 | Invalid Operation | faceDetectFailed | 0x400010C5 | Face detection failed. |
| 4.0 | Invalid Operation | libraryNotExist | 0x400010C6 | The library does not exist. |
| 4.0 | Invalid Operation | blackListQueryExporting | 0x400010C7 | Exporting matched blocklists. |
| 4.0 | Invalid Operation | blackListQueryExported | 0x400010C8 | The matched blocklists are exported. |
| 4.0 | Invalid Operation | blackListQueryStopExporting | 0x400010C9 | Exporting matched blocklists is stopped. |
| 4.0 | Invalid Operation | blackListAlarmQueryExporting | 0x400010CA | Exporting matched blocklist alarms. |
| 4.0 | Invalid Operation | blackListAlarmQueryExported | 0x400010CB | The matched blocklists alarms are exported. |
| 4.0 | Invalid Operation | blackListAlarmQueryStopExporting | 0x400010CC | Exporting matched blocklist alarms is stopped. |
| 4.0 | Invalid Operation | getBigDataCloudAnalysisFailed | 0x400010CD | Getting the information about big data cloud analysis failed. |
| 4.0 | Invalid Operation | setBigDataCloudAnalysisFailed | 0x400010CE | Configuring big data cloud analysis failed. |
| 4.0 | Invalid Operation | submitMapSearchFailed | 0x400010CF | Submitting the task of searching picture by picture failed. |
| 4.0 | Invalid Operation | controlRelationshipNotExist | 0x400010D0 | The arming relation does not exist. |
| 4.0 | Invalid Operation | getHistoryAlarmInfoFailed | 0x400010D1 | Getting the history alarm information failed. |
| 4.0 | Invalid Operation | getFlowReportFailed | 0x400010D2 | Getting the people counting report failed. |
| 4.0 | Invalid Operation | addGuardFailed | 0x400010D3 | Adding the alarm arming configuration failed. |
| 4.0 | Invalid Operation | deleteGuardFailed | 0x400010D4 | Deleting the alarm arming configuration failed. |
| 4.0 | Invalid Operation | modifyGuardFailed | 0x400010D5 | Editing the arming configuration failed. |
| 4.0 | Invalid Operation | queryGuardFailed | 0x400010D6 | Searching alarm arming configuration(s) failed. |
| 4.0 | Invalid Operation | uploadUserSuperCaps | 0x400010D7 | No more user information can be uploaded. |
| 4.0 | Invalid Operation | bigDataServerConnectFailed | 0x400010D8 | Connecting to big data server failed. |
| 4.0 | Invalid Operation | microVideoCloudRequestInfoBuildFailed | 0x400010D9 | Adding request information of micro video cloud failed. |
| 4.0 | Invalid Operation | microVideoCloudResponseInfoBuildFailed | 0x400010DA | Parsing response information of micro video cloud failed. |
| 4.0 | Invalid Operation | transcodingServerRequestInfoBuildFailed | 0x400010DB | Adding request information of transcoding server failed. |
| 4.0 | Invalid Operation | transcodingServerResponseInfoParseFailed | 0x400010DC | Parsing response information of transcoding server failed. |
| 4.0 | Invalid Operation | transcodingServerOffline | 0x400010DD | Transcoding server is offline. |
| 4.0 | Invalid Operation | microVideoCloudOffline | 0x400010DE | Micro video cloud is offline. |
| 4.0 | Invalid Operation | UPSServerOffline | 0x400010DF | UPS monitoring server is offline. |
| 4.0 | Invalid Operation | statisticReportRequestInfoBuildFailed | 0x400010E0 | Adding request information of statistics report failed. |
| 4.0 | Invalid Operation | statisticReportResponseInfoParseFailed | 0x400010E1 | Parsing response information of statistics report failed. |
| 4.0 | Invalid Operation | DisplayConfigInfoBuildFailed | 0x400010E2 | Adding display configuration information failed. |
| 4.0 | Invalid Operation | DisplayConfigInfoParseFailed | 0x400010E3 | Parsing display configuration information failed. |
| 4.0 | Invalid Operation | DisplayConfigInfoSaveFailed | 0x400010E4 | Saving display configuration information failed. |
| 4.0 | Invalid Operation | notSupportDisplayConfigType | 0x400010E5 | The display configuration type is not supported. |
| 4.0 | Invalid Operation | noDiskSpace | 0x400010E6 | Not enough disk space. |
| 4.0 | Invalid Operation | passError | 0x400010E7 | Incorrect password. |
| 4.0 | Invalid Operation | cannotSameAsOldPassword | 0x400010E8 | New password cannot be the same as the old one. |
| 4.0 | Invalid Operation | originalPassError | 0x400010E9 | Incorrect old password. |
| 4.0 | Invalid Operation | writeFileError | 0x400010EA | Writing file error. |
| 4.0 | Invalid Operation | upgradePackageLarge | 0x400010EB | The upgrade package is too large. |
| 4.0 | Invalid Operation | sesssionUserReachesLimit | 0x400010EC | No more user can log in through session. |
| 4.0 | Invalid Operation | ISO 8601TimeFormatError | 0x400010ED | Invalid ISO 8601 time format. |
| 4.0 | Invalid Operation | clusterDissolutionFailed | 0x400010EE | Dissolving the cluster failed. |
| 4.0 | Invalid Operation | getServiceNodeInfoFailed | 0x400010EF | Getting the service node information failed. |
| 4.0 | Invalid Operation | getUPSInfoFailed | 0x400010F0 | Getting the UPS configuration information failed. |
| 4.0 | Invalid Operation | getDataStatisticsReportFailed | 0x400010F1 | Getting the data statistic report failed. |
| 4.0 | Invalid Operation | getDisplayConfigInfoFailed | 0x400010F2 | Getting display configuration(s) failed. |
| 4.0 | Invalid Operation | renamingAnalysisBoardNotAllowed | 0x400010F3 | Renaming existing analysis board(s) is not supported. |
| 4.0 | Invalid Operation | onlyDrawRegionsOfConvexPolygon | 0x400010F4 | Only drawing convex polygon areas is supported. |
| 4.0 | Invalid Operation | bigDataServerResponseInfoParseFailed | 0x400010F5 | Parsing response message of big data service failed. |
| 4.0 | Invalid Operation | bigDataServerReturnFailed | 0x400010F6 | No response is returned by big data service. |
| 4.0 | Invalid Operation | microVideoReturnFailed | 0x400010F7 | No response is returned by micro video cloud service. |
| 4.0 | Invalid Operation | transcodingServerReturnFailed | 0x400010F8 | No response is returned by transcoding service. |
| 4.0 | Invalid Operation | UPSServerReturnFailed | 0x400010F9 | No response is returned by UPS monitoring service. |
| 4.0 | Invalid Operation | forwardingServer ReturnFailed | 0x400010FA | No response is returned by forwarding service. |
| 4.0 | Invalid Operation | storageServer ReturnFailed | 0x400010FB | No response is returned by storage service. |
| 4.0 | Invalid Operation | cloudAnalysisServerReturnFailed | 0x400010FC | No response is returned by cloud analytic service. |
| 4.0 | Invalid Operation | modelEmpty | 0x400010FD | The obtained model is empty. |
| 4.0 | Invalid Operation | mainAndBackupNodeCannotModifyManagementNetworkInterfaceIP | 0x400010FE | Editing management interface IP address of main and backup node is not allowed. |
| 4.0 | Invalid Operation | IDTooLong | 0x400010FF | The ID is too long. |
| 4.0 | Invalid Operation | pictureCheckFailed | 0x40001100 | Picture detection failed. |
| 4.0 | Invalid Operation | pictureModelingFailed | 0x40001101 | Picture modeling failed. |
| 4.0 | Invalid Operation | setCloudAnalsisDefaultProvinceFailed | 0x40001102 | Setting the default province of cloud analysis failed. |
| 4.0 | Invalid Operation | InspectionAreasNumberExceedLimit | 0x40001103 | The number of detection areas exceeded limit. |
| 4.0 | Invalid Operation | accessFileDirectoryFailed | 0x40001104 | Accessing directory for files failed. |
| 4.0 | Invalid Operation | picturePixelsTooLarge | 0x40001105 | The picture resolution is too high. |
| 4.0 | Invalid Operation | picturePixelsTooSmall | 0x40001106 | The picture resolution is too low. |
| 4.0 | Invalid Operation | storageServiceIPEmpty | 0x40001107 | The storage server IP address is required. |
| 4.0 | Invalid Operation | bigDataServerRequestInfoBuildFail | 0x40001108 | Creating request message of big data service failed. |
| 4.0 | Invalid Operation | analysiTimedOut | 0x40001109 | Analysis timed out. |
| 4.0 | Invalid Operation | high-performanceModeDisabled. | 0x4000110A | High-performance mode is disabled. |
| 4.0 | Invalid Operation | configuringUPSMonitoringServerTimedOut | 0x4000110B | Configuring the UPS monitoring server timed out. Check the IP address. |
| 4.0 | Invalid Operation | cloudAnalysisRequestInformationBuildFailed | 0x4000110C | Creating request message of cloud analysis failed. |
| 4.0 | Invalid Operation | cloudAnalysisResponseInformationParseFailed | 0x4000110D | Parsing response message of cloud analysis failed. |
| 4.0 | Invalid Operation | allCloudAnalysisInterfaceFailed | 0x4000110E | Calling the cloud analysis API(s) failed. |
| 4.0 | Invalid Operation | cloudAnalysisModelCompareFailed | 0x4000110F | Model comparison of cloud analysis failed. |
| 4.0 | Invalid Operation | cloudAnalysisFacePictureQualityRatingFailed | 0x40001110 | Getting face quality grading of cloud analysis failed. |
| 4.0 | Invalid Operation | cloudAnalysisExtractFeaturePointsFailed | 0x40001111 | Extracting feature of cloud analysis failed. |
| 4.0 | Invalid Operation | cloudAnalysisExtractPropertyFailed | 0x40001112 | Extracting property of cloud analysis failed. |
| 4.0 | Invalid Operation | getAddedNodeInformationFailed | 0x40001113 | Getting added nodes information of the analysis unit failed. |
| 4.0 | Invalid Operation | noMoreAnalysisUnitsAdded | 0x40001114 | No more analysis unit can be added. |
| 4.0 | Invalid Operation | detectionAreaInvalid | 0x40001115 | Invalid detection region. |
| 4.0 | Invalid Operation | shieldAreaInvalid | 0x40001116 | Invalid shielded region. |
| 4.0 | Invalid Operation | noMoreShieldAreasAdded | 0x40001117 | The number of shielded regions reached limit. |
| 4.0 | Invalid Operation | onlyAreaOfRectangleShapeAllowed | 0x40001118 | Only drawing rectangle is allowed in a detection area. |
| 4.0 | Invalid Operation | numberReachedLlimit | 0x40001119 | The number reached limit. |
| 4.0 | Invalid Operation | wait1~3MinutesGetIPAfterSetupDHCP | 0x4000111A | Wait 1 to 3 minutes to get IP address after configuring DHCP. |
| 4.0 | Invalid Operation | plannedTimeMustbeHalfAnHour | 0x4000111B | Schedule time period must be the multiple of 30 minutes. |
| 4.0 | Invalid Operation | oneDeviceCannotBuildCluster | 0x4000111C | Creating the host and backup cluster requires at least two devices. |
| 4.0 | Invalid Operation | unKnownErrorCode | 0x4000111D | Unknown error code. |
| 4.0 | Invalid Operation | updatePackageFileNotUploaded | 0x4000111E | The upgrade package is not uploaded. |
| 4.0 | Invalid Operation | highPerformanceTasksNotSupportDrawingDetectionRegions | 0x4000111F | Drawing detection area(s) is not allowed under high-performance mode. |
| 4.0 | Invalid Operation | controlCenterIDDoesNotExist | 0x40001120 | The control center ID does not exist. |
| 4.0 | Invalid Operation | regionIDDoesNotExist | 0x40001121 | The area ID does not exist. |
| 4.0 | Invalid Operation | licensePlateFormatError | 0x40001122 | Invalid license plate format. |
| 4.0 | Invalid Operation | managementNodeDoesNotSupportThisOperation | 0x40001123 | The operation is not supported. |
| 4.0 | Invalid Operation | searchByPictureResourceNotConfiged | 0x40001124 | The conditions for searching picture by picture are not configured. |
| 4.0 | Invalid Operation | videoFileEncapsulationFormatNotSupported | 0x40001125 | The video container format is not supported. |
| 4.0 | Invalid Operation | videoPackageFailure | 0x40001126 | Converting video container format failed. |
| 4.0 | Invalid Operation | videoCodingFormatNotSupported | 0x40001127 | The video coding format is not supported. |
| 4.0 | Invalid Operation | deviceVervisionNotMatch | 0x40001128 | Device version mismatches. |
| 4.0 | Invalid Operation | monitorOfDeviceArmingdeleteArmingInfo | 0x40001129 | The camera is armed. Disarm it and try again. |
| 4.0 | Invalid Operation | getVideoSourceTypeFailed | 0x4000112A | Getting video source type failed. |
| 4.0 | Invalid Operation | smartRulesBuildFailed | 0x4000112B | Creating VAC rule failed. |
| 4.0 | Invalid Operation | smartRulesParseFailed | 0x4000112C | Parsing VAC rule failed. |
| 4.0 | Invalid Operation | timeRulesBuildFailed | 0x4000112D | Creating time rule failed. |
| 4.0 | Invalid Operation | timeRulesParseFailed | 0x4000112E | Parsing time rule failed. |
| 4.0 | Invalid Operation | monitoInfoInvalid | 0x4000112F | Invalid camera information. |
| 4.0 | Invalid Operation | addingFailedVersionMismatches | 0x40001130 | Adding failed. The device version mismatches. |
| 4.0 | Invalid Operation | theInformationReturnedAfterCloudAnalysisIsEmpty | 0x40001131 | The information returned by the cloud analysis is empty. |
| 4.0 | Invalid Operation | selectingIpAddressOfHostAndSpareNodeFailedCheckTheStatus | 0x40001132 | Selecting IP address for the host and backup node failed. Check the node status. |
| 4.0 | Invalid Operation | theSearchIdDoesNotExist | 0x40001133 | The search ID does not exist. |
| 4.0 | Invalid Operation | theSynchronizationIdDoesNotExist | 0x40001134 | The synchronization ID does not exist. |
| 4.0 | Invalid Operation | theSessionIdDoesNotExist | 0x40001135 | The session ID does not exist |
| 4.0 | Invalid Operation | theUserIdDoesNotExist | 0x40001136 | The user ID does not exist |
| 4.0 | Invalid Operation | theCameraIdDoesNotExist | 0x40001137 | The monitor ID does not exist |
| 4.0 | Invalid Operation | theIndexCodeDoesNotExist | 0x40001138 | The indexCode does not exist |
| 4.0 | Invalid Operation | theControlCenterIdDoesNotExist | 0x40001139 | The control center ID does not exist. |
| 4.0 | Invalid Operation | theAreaIdDoesNotExist | 0x4000113A | The area ID does not exist. |
| 4.0 | Invalid Operation | theDeviceIdDoesNotExist | 0x4000113B | The device ID does not exist. |
| 4.0 | Invalid Operation | theArmingLinkageIdDoesNotExist | 0x4000113C | The arming relationship ID does not exist. |
| 4.0 | Invalid Operation | theListLibraryIdDoesNotExist | 0x4000113D | The list library ID does not exist. |
| 4.0 | Invalid Operation | invalidCityCode | 0x4000113E | Invalid city code. |
| 4.0 | Invalid Operation | synchronizingThePasswordOfSpareServerFailed | 0x4000113F | Synchronizing system password of the standby server failed. |
| 4.0 | Invalid Operation | editingStreamingTypeIsNotSupported | 0x40001140 | Editing streaming type is not supported. |
| 4.0 | Invalid Operation | switchingScheduledTaskToTemporaryTaskIsNotSupported | 0x40001141 | Switching scheduled task(s) to temporary task(s) is not supported. |
| 4.0 | Invalid Operation | switchingTemporaryTaskToScheduledTaskIsNotSupported | 0x40001142 | Switching temporary task(s) to scheduled task(s) is not supported. |
| 4.0 | Invalid Operation | theTaskIsNotDispatchedOrItIsUpdating | 0x40001143 | The task is not dispatched or is updating. |
| 4.0 | Invalid Operation | thisTaskDoesNotExist | 0x40001144 | The task does not exist. |
| 4.0 | Invalid Operation | duplicatedSchedule | 0x40001145 | Schedule period cannot be overlapped. |
| 4.0 | Invalid Operation | continuousScheduleWithSameAlgorithmTypeShouldBeMerged | 0x40001146 | The continuous schedule periods with same algorithm type should be merged. |
| 4.0 | Invalid Operation | invalidStreamingTimeRange | 0x40001147 | Invalid streaming time period. |
| 4.0 | Invalid Operation | invalidListLibraryType | 0x40001148 | Invalid list library type. |
| 4.0 | Invalid Operation | theNumberOfMatchedResultsShouldBeLargerThan0 | 0x40001149 | The number of search results should be larger than 0. |
| 4.0 | Invalid Operation | invalidValueRangeOfSimilarity | 0x4000114A | Invalid similarity range. |
| 4.0 | Invalid Operation | invalidSortingType | 0x4000114B | Invalid sorting type. |
| 4.0 | Invalid Operation | noMoreListLibraryCanBeLinkedToTheDevice | 0x4000114C | No more lists can be linked to the device. |
| 4.0 | Invalid Operation | InvalidRecipientAddressFormat | 0x4000114D | Invalid address format of result receiver. |
| 4.0 | Invalid Operation | creatingClusterFailedTheDongleIsNotPluggedIn | 0x4000114E | Insert the dongle before creating cluster. |
| 4.0 | Invalid Operation | theURLIsTooLong | 0x4000114F | Length of the URL is too long. |
| 4.0 | Invalid Operation | noScheduleIsConfiguredForTheTask | 0x40001150 | No schedule configured for the task. |
| 4.0 | Invalid Operation | theDongleIsExpiried | 0x40001151 | Dongle expired. |
| 4.0 | Invalid Operation | dongleException | 0x40001152 | Dongle exception. |
| 4.0 | Invalid Operation | invalidKey | 0x40001153 | Invalid authorization service key. |
| 4.0 | Invalid Operation | decryptionFailed | 0x40001154 | Decrypting authorization service failed. |
| 4.0 | Invalid Operation | encryptionFailed | 0x40001155 | Encrypting authorization service failed. |
| 4.0 | Invalid Operation | AuthorizeServiceResponseError | 0x40001156 | Authorization service response exception. |
| 4.0 | Invalid Operation | incorrectParameter | 0x40001157 | Authorization service parameter error. |
| 4.0 | Invalid Operation | operationFailed | 0x40001158 | Authorization service operation failed. |
| 4.0 | Invalid Operation | noAnalysisResourceOrNoDataInTheListLibrary | 0x40001159 | No cloud analysis resources or no data in the list library. |
| 4.0 | Invalid Operation | calculationException | 0x4000115A | Compute nodes exception. |
| 4.0 | Invalid Operation | allocatingList | 0x4000115B | Allocating list... |
| 4.0 | Invalid Operation | thisOperationIsNotSupportedByTheCloudAnalytics | 0x4000115C | This operation is not supported by the cloud analysis. |
| 4.0 | Invalid Operation | theCloudAnalyticsIsInterrupted | 0x4000115D | The operation of cloud analysis is interrupted. |
| 4.0 | Invalid Operation | theServiceIsNotReady | 0x4000115E | The service is not ready. |
| 4.0 | Invalid Operation | searchingForExternalApiFailed | 0x4000115F | Searching external APIs failed. |
| 4.0 | Invalid Operation | noOnlineNode | 0x40001160 | No node is online. |
| 4.0 | Invalid Operation | noNodeAllocated | 0x40001161 | No allocated node. |
| 4.0 | Invalid Operation | noMatchedList | 0x40001162 | No matched list. |
| 4.0 | Invalid Operation | allocatingFailedTooManyFacePictureLists | 0x40001163 | Allocation failed. Too many lists of big data service. |
| 4.0 | Invalid Operation | searchIsNotCompletedSearchAgain | 0x40001164 | Current searching is not completed. Search again. |
| 4.0 | Invalid Operation | allocatingListIsNotCompleted | 0x40001165 | Allocating list is not completed. |
| 4.0 | Invalid Operation | searchingForCloudAnalyticsResultsFailed | 0x40001166 | Cloud analysis searching timeout. |
| 4.0 | Invalid Operation | noDataOfTheCurrentLibraryFound | 0x40001167 | No data in the current library. Make sure there is data in the Hbase. |
| 4.0 | Invalid Operation | noFacePictureLibraryIsArmed | 0x40001168 | No face picture library is armed for big data service. |
| 4.0 | Invalid Operation | noAvailableDataSlicingVersionInformationArmFirstAndSliceTheData | 0x40001169 | Invalid standard version information. |
| 4.0 | Invalid Operation | duplicatedOperationDataSlicingIsExecuting | 0x4000116A | Slicing failed. Duplicate operation. |
| 4.0 | Invalid Operation | slicinDataFailedNoArmedFacePictureLibrary | 0x4000116B | Slicing failed. No arming information in the face big data. |
| 4.0 | Invalid Operation | GenerateBenchmarkFileFailedSlicingAgain | 0x4000116C | Generating sliced file failed. Slice again. |
| 4.0 | Invalid Operation | NonprimaryNodeIsProhibitedFromSlcingData | 0x4000116D | Slicing is not allowed by the backup node. |
| 4.0 | Invalid Operation | NoReadyNodeToClusterServers | 0x4000116E | Creating the cluster failed. No ready node. |
| 4.0 | Invalid Operation | NodeManagementServiceIsOffline | 0x4000116F | The node management server is offline. |
| 4.0 | Invalid Operation | theCamera(s)OfTheControlCenterAreAlreadyArmed.DisarmThemFirst | 0x40001170 | Some cameras in control center are already armed. Disarm them and try again. |
| 4.0 | Invalid Operation | theCamera(s)OfTheAreaAreAlreadyArmed.DisarmThemFirst | 0x40001171 | Some cameras in this area are already armed. Disarm them and try again. |
| 4.0 | Invalid Operation | configuringHigh-frequencyPeopleDetectionFailed | 0x40001172 | Configuring frequently appeared person detection failed. |
| 4.0 | Invalid Operation | searchingForHigh-frequencyPeopleDetectionLogsFailed. | 0x40001173 | Searching detection event logs of frequently appeared person detection failed. |
| 4.0 | Invalid Operation | gettingDetailsOfSearchedHigh-frequencyPeopleDetectionLogsFailed. | 0x40001174 | Getting the search result details of frequently appeared person alarms failed. |
| 4.0 | Invalid Operation | theArmedCamerasAlreadyExistInTheControlCenter | 0x40001175 | Some cameras in control center are already armed. |
| 4.0 | Invalid Operation | gettingResourceNodeInformationFailed | 0x40001176 | Getting resource node information failed. |
| 4.0 | Invalid Operation | disarmingFailedTheCameraIsNotArmed | 0x40001177 | Disarming failed. The camera is not armed. |
| 4.0 | Invalid Operation | noDataReturned | 0x40001178 | No response is returned by the big data service. |
| 4.0 | Invalid Operation | preallocFailure | 0x40001179 | Pre-Allocating algorithm resource failed. |
| 4.0 | Invalid Operation | overDogLimit | 0x4000117A | Configuration failed. No more resources can be pre-allocated. |
| 4.0 | Invalid Operation | analysisServicesDoNotSupport | 0x4000117B | Not supported. |
| 4.0 | Invalid Operation | commandAndDispatchServiceError | 0x4000117C | Scheduling service of cloud analytic service error. |
| 4.0 | Invalid Operation | engineModuleError | 0x4000117D | Engine module of cloud analytic service error. |
| 4.0 | Invalid Operation | streamingServiceError | 0x4000117E | Streaming component of cloud analytic service error. |
| 4.0 | Invalid Operation | faceAnalysisModuleError | 0x4000117F | Face analysis module of cloud analytic service error. |
| 4.0 | Invalid Operation | vehicleAnalysisModuleError | 0x40001180 | Vehicle pictures analytic module of cloud analytic service error. |
| 4.0 | Invalid Operation | videoStructuralAnalysisModuleError | 0x40001181 | Video structuring module of cloud analytic service error. |
| 4.0 | Invalid Operation | postprocessingModuleError | 0x40001182 | Post-processing module of cloud analytic service error. |
| 4.0 | Invalid Operation | frequentlyAppearedPersonAlarmIsAlreadyConfiguredForListLibrary | 0x40001183 | High frequency alarm is already armed for blacklist library. |
| 4.0 | Invalid Operation | creatingListLibraryFailed | 0x40001184 | Creating list library failed. |
| 4.0 | Invalid Operation | invalidIdentiryKeyOfListLibrary | 0x40001185 | Invalid identity key of list library. |
| 4.0 | Invalid Operation | noMoreDevicesCanBeArmed | 0x40001186 | No more camera can be added. |
| 4.0 | Invalid Operation | settingAlgorithmTypeForDeviceFailed | 0x40001187 | Allocating task resource failed. |
| 4.0 | Invalid Operation | gettingHighFrequencyPersonDetectionAlarmInformationFailed | 0x40001188 | Setting frequently appeared person alarm failed. |
| 4.0 | Invalid Operation | invalidSearchConfition | 0x40001189 | Invalid result. |
| 4.0 | Invalid Operation | noMoreTasksCanBeAdded | 0x4000118A | No more tasks can be added. |
| 4.0 | Invalid Operation | theTaskIsNotCompleted | 0x4000118B | The task is not completed. |
| 4.0 | Invalid Operation | resourceOverRemainLimit | 0x4000118C | No more resource can be pre-allocated. |
| 4.0 | Invalid Operation | frequentlyAppearedPersonAlarmIs AlreadyConfiguredForTheCameraDisarmFirstAndTryAgain | 0x4000118D | The frequently appeared person alarm of this camera is configured. Delete the arming information and try again. |
| 4.0 | Invalid Operation | noRecongnizeUSB | 0x4000118e | No USB found. Please insert USB or insert it again. |
| 4.0 | Invalid Operation | noSetSecurityEmail | 0x4000118f | Security E-mail address is not set. |
| 4.0 | Invalid Operation | unopenedHighResolutionMode | 0x40001190 | Ultra high resolution is not enabled. |
| 4.0 | Invalid Operation | accessFroDeviceParamFailure | 0x40001191 | Getting front-end device parameter failed. |
| 4.0 | Invalid Operation | accessFroDeviceStreamFailure | 0x40001192 | Getting front-end streaming failed. |
| 4.0 | Invalid Operation | restoringToDefaultSettingsIsNotAllowedInClusterMode | 0x40001193 | Restoring defaults is not allowed in cluster mode. |
| 4.0 | Invalid Operation | noPermissionToSetTheConfiguredFrequentlyAppearedPersonDetectionRuleOnlyTheAdminUserIsAllowed | 0x40001194 | Non admin user has no permission to set the frequently appeared person detection rules created by other users. |
| 4.0 | Invalid Operation | thisDeviceModelDoesNotSupportAddingCamera | 0x40001195 | The device model does not support to add camera. |
| 4.0 | Invalid Operation | editingDataAnalysisServerTypeIsNotAllowedInClusterMode | 0x40001196 | Editing data analytics server type is not allowed in cluster mode. |
| 4.0 | Invalid Operation | editingDataAnalysisServerTypeFailedTheServerIsAlreadyAdded | 0x40001197 | Data analytics server added, and its type cannot be edited. |
| 4.0 | Invalid Operation | dns1dns2CanNotSame | 0x40001198 | Top priority and alternative DNS cannot be same. |
| 4.0 | Invalid Operation | chanelIsUploadingCloudFile | 0x40001199 | Deleting or editing is not allowed. Channel is uploading file to external storage. |
| 4.0 | Invalid Operation | opsconnectfailcheckip | 0x4000119a | Connecting to operation and management platform failed. Please check IP. |
| 4.0 | Invalid Operation | userNameMismatched | 0x4000119b | The user name does not match with that of added device. |
| 4.0 | Invalid Operation | editingDeviceInformationFailed | 0x4000119c | Editing device information failed. |
| 4.0 | Invalid Operation | addingCameraInformationFailed | 0x4000119d | Creating camera information failed. |
| 4.0 | Invalid Operation | addingFailedTheGPUCardTypesOfDevicesAreDifferent | 0x4000119e | Adding failed. Inconsistent GPU card type. |
| 4.0 | Invalid Operation | Clusterstatecannotintmodifyelligentpatterns | 0x4000119f | Modifying smart mode is not allowed in cluster mode. |
| 4.0 | Invalid Operation | algorithmformaterror | 0x400011a0 | Invalid algorithm package format. |
| 4.0 | Invalid Operation | clustermodenotallowedRecovery | 0x400011a1 | Restoring defaults is not allowed in cluster mode. |
| 4.0 | Invalid Operation | Defaultalgorithmnotsupportdeleting | 0x400011a2 | Deleting default algorithm is not supported. |
| 4.0 | Invalid Operation | ipcNumReachesLimit | 0x400011a3 | No more IP cameras are allowed. |
| 4.0 | Invalid Operation | iotNumReachesLimit | 0x400011a4 | No more IoT channels are allowed. |
| 4.0 | Invalid Operation | iotChannelDeviceExist | 0x400011a5 | Device(s) has already been added in current IoT channel. |
| 4.0 | Invalid Operation | iotChannelDeviceNotExist | 0x400011a6 | No device exists in the IoT channel. |
| 4.0 | Invalid Operation | diskOccupation | 0x400011a7 | Disc is occupied by other service. |
| 4.0 | Invalid Operation | needResetRAID | 0x400011a8 | Restore RAID. |
| 4.0 | Invalid Operation | notSupportRaidSwitch | 0x400011a9 | Changing RAID is not supported. |
| 4.0 | Invalid Operation | needRapidConfigIraid | 0x400011aa | Quick configuration of IRAID is required. |
| 4.0 | Invalid Operation | smartNotSupportPic | 0x400011ab | Changing application mode is not supported under smart record mode. |
| 4.0 | Invalid Operation | duplicateIotDevice | 0x400011ac | Duplicate IoT device. |
| 4.0 | Invalid Operation | sadpModifyFailure | 0x400011ad | Modifying SADP failed. |
| 4.0 | Invalid Operation | ipcNetworkAbnormal | 0x400011ae | Network exception of the network camera. |
| 4.0 | Invalid Operation | ipcPasswordError | 0x400011af | Incorrect user name or password of the network camera. |
| 4.0 | Invalid Operation | ipcListNotEmpty | 0x400011b0 | One-Touch configuration is not supported. Added network camera list is not empty. |
| 4.0 | Invalid Operation | ipcListNotMatchPairing | 0x400011b1 | Network camera list does not match with the pairing list. |
| 4.0 | Invalid Operation | ipcIsLocking | 0x400011b2 | Network camera is locked. |
| 4.0 | Invalid Operation | ipcNotActivated | 0x400011b3 | Network camera is inactivated. |
| 4.0 | Invalid Operation | h323NotSupportH265 | 0x400011b4 | H.323 video conference does not support H.265 stream. |
| 4.0 | Invalid Operation | frameRateNotSupported | 0x400011b5 | Video frame rate is not supported. |
| 4.0 | Invalid Operation | channelOffline | 0x400011b6 | Channel is offline. |
| 4.0 | Invalid Operation | emptyIPCListForOneKey | 0x400011b7 | One-Touch configuration is not supported. Network camera configuration form is empty. |
| 4.0 | Invalid Operation | NVRNotSupportResetPassword | 0x400011b8 | NVR does not support resetting password. |
| 4.0 | Invalid Operation | ipcNeedOnLan | 0x400011b9 | Network camera should be connected to LAN. |
| 4.0 | Invalid Operation | resetPasswordTypeException | 0x400011ba | Exception occurred when getting reset password type of network camera. |
| 4.0 | Invalid Operation | IPCNotSupportResetPassword | 0x400011bb | Network camera does not support resetting password. |
| 4.0 | Invalid Operation | IPCIPNotUnique | 0x400011bc | Duplicate IP address of network camera. |
| 4.0 | Invalid Operation | analysisunitshouldconsistentwithnative | 0x400011c0 | Analysis unit added should be the same with device smart mode. |
| 4.0 | Invalid Operation | analysisunitacquireFailure | 0x400011c1 | Getting analysis unit smart mode failed. |
| 4.0 | Invalid Operation | modenotmodifybyanalysisadd | 0x400011c2 | Analysis unit added, and smart mode cannot be edited. |
| 4.0 | Invalid Operation | modenotmodifybyanalysisbeenadd | 0x400011c3 | Analysis unit added by non-self node, and smart mode cannot be edited. |
| 4.0 | Invalid Operation | schedulingdatabaseisfull | 0x400011c4 | Database disk is full. |
| 4.0 | Invalid Operation | algorithmtypeidnotvalid | 0x400011c5 | Invalid algorithm ID. |
| 4.0 | Invalid Operation | destinationaddressinvalid | 0x400011c6 | Invalid third-party address. |
| 4.0 | Invalid Operation | picdataurlisnotvalid | 0x400011c7 | Invalid picture URL. |
| 4.0 | Invalid Operation | failedtogetdataanalysis | 0x400011c8 | Streaming failed. |
| 4.0 | Invalid Operation | centralnewnodefailure | 0x400011c9 | Adding central control nodes failed. |
| 4.0 | Invalid Operation | centralclusterinstallationfailure | 0x400011ca | Installing central control cluster failed. |
| 4.0 | Invalid Operation | controlofdissolutionoftheclustertofail | 0x400011cb | Disbanding central control cluster failed. |
| 4.0 | Invalid Operation | accesscontrolclusterstatusfailed | 0x400011cc | Obtaining status of central control cluster failed. |
| 4.0 | Invalid Operation | gainschedulingclusterstatusfailed | 0x400011cd | Obtaining status of dispatching cluster failed. |
| 4.0 | Invalid Operation | basiccomponentsinstalledclustertofail | 0x400011ce | Installing basic component cluster failed. |
| 4.0 | Invalid Operation | basiccomponentsfailedtodissolutionofthecluster | 0x400011cf | Disbanding basic component cluster failed. |
| 4.0 | Invalid Operation | accesstobasiccomponentsclusterstatusfailed | 0x400011d0 | Obtaining status of basic component cluster failed. |
| 4.0 | Invalid Operation | accesscontroldynamiclibrarystatusfailed | 0x400011d1 | Obtaining status of central control dynamic library failed. |
| 4.0 | Invalid Operation | accesscontrolstaticlibrarystatusfailed | 0x400011d2 | Obtaining status of central control static library failed. |
| 4.0 | Invalid Operation | basiccomponentconfigurationfilewrittentofail | 0x400011d3 | Writing to basic component configuration file failed. |
| 4.0 | Invalid Operation | failedtogetthenodecontrol | 0x400011d4 | Central control acquiring nodes failed. |
| 4.0 | Invalid Operation | algorithmpacketsupperlimit | 0x400011d5 | Number of algorithm packages reached limit. |
| 4.0 | Invalid Operation | algorithmuploading | 0x400011d6 | Uploading algorithm package... |
| 4.0 | Invalid Operation | uploadalgorithmPackageLarge | 0x400011d7 | Algorithm package is too large. |
| 4.0 | Invalid Operation | algorithmconfignotexist | 0x400011d8 | Configuration file of algorithm package does not exist. |
| 4.0 | Invalid Operation | uploadalgorithmPackagesmall | 0x400011d9 | Algorithm package is too small. |
| 4.0 | Invalid Operation | algorithmexist | 0x400011da | Algorithm package already exists. |
| 4.0 | Invalid Operation | clustermodenotallowedmultimode | 0x400011db | Restoring to defaults is not allowed in multi-smart mode. |
| 4.0 | Invalid Operation | deploylibrarylistnumberhasreacheditslimit | 0x400011dc | Number of arm libraries reached limit. |
| 4.0 | Invalid Operation | fdlibrarymorethanupperlimit | 0x400011dd | Number of name lists exceeded limit. |
| 4.0 | Invalid Operation | nosoftwarepermissiondogwasinserted | 0x400011de | Software dongle is not inserted. |
| 4.0 | Invalid Operation | softwarepermissiondogexceptio | 0x400011df | Software dongle exception. |
| 4.0 | Invalid Operation | theTaskTypeIsNotSupported | 0x400011e0 | Task type is not supported. |
| 4.0 | Invalid Operation | allNodesNeedToBeInTheSameNetworkSegment | 0x400011e1 | All the nodes should be in the same network segment. |
| 4.0 | Invalid Operation | passersbyLibCannotBeDeleted | 0x400011e2 | Pedestrian library cannot be deleted. |
| 4.0 | Invalid Operation | cannotModifyTheNameOfPasserbyLib | 0x400011e3 | Pedestrian library name cannot be edited. |
| 4.0 | Invalid Operation | theanalysisunitneedstobeactivated | 0x400011e4 | Activate analysis unit first. |
| 4.0 | Invalid Operation | calcPoolConnectFailPleaseCheckIpPort | 0x400011e5 | Connecting to resource pool failed. Check IP address and port. |
| 4.0 | Invalid Operation | edgeManageConnectFailPleaseCheckIpPort | 0x400011e6 | Connecting to operation and management platform failed. Check IP address and port. |
| 4.0 | Invalid Operation | calcPoolSetFail | 0x400011e7 | Setting resource pool failed. |
| 4.0 | Invalid Operation | edgeManageSetFail | 0x400011e8 | Setting operation and management platform failed. |
| 4.0 | Invalid Operation | checkTheImageServerConfiguration | 0x400011e9 | Please check picture server configuration. |
| 4.0 | Invalid Operation | micinChannelOccupied | 0x400011ea | MICIN channel is occupied. |
| 4.0 | Invalid Operation | invalidDatasetType | 0x400011eb | Invalid data set type. |
| 4.0 | Invalid Operation | theDatasetCannotBeDeleted | 0x400011ec | This data set is contained in the operation task and cannot be deleted. |
| 4.0 | Invalid Operation | deleteOptionNeedToBeConfirmed | 0x400011ed | Confirmation is needed before deleting. This data set is contained in the untransformed task. |
| 4.0 | Invalid Operation | updateAttributeDuplicationOfName | 0x400011ee | Editing failed. Duplicate edited attribute name. |
| 4.0 | Invalid Operation | updateLabelDuplicationOfName | 0x400011ef | Editing failed. Duplicate edited tag name. |
| 4.0 | Invalid Operation | invalidRechargeCard | 0x400011f0 | Invalid top-up card. |
| 4.0 | Invalid Operation | cloudPlatformServerException | 0x400011f1 | Cloud platform server exception. |
| 4.0 | Invalid Operation | operationFailureWithoutLogin | 0x400011f2 | Operation failed. Login first. |
| 4.0 | Invalid Operation | invalidAssociatedSerialNumber | 0x400011f3 | Invalid linked serial number. |
| 4.0 | Invalid Operation | cloudPlatformAccountNotExist | 0x400011f4 | Cloud platform account does not exist. |
| 4.0 | Invalid Operation | deviceSerialNumberRegistered | 0x400011f5 | Serial number of the device is registered. |
| 4.0 | Invalid Operation | conferenceRoomNotExist | 0x400011f6 | Conference room does not exist. |
| 4.0 | Invalid Operation | needDisabledAnalogChannel | 0x400011f7 | Analog channel should be disabled. |
| 4.0 | Invalid Operation | studentRollCallFailure | 0x400011f8 | Checking student attendance failed. |
| 4.0 | Invalid Operation | subdeviceNotEnableIndividualBehavior | 0x400011f9 | Child device disabled individual behavior mode. |
| 4.0 | Invalid Operation | subdeviceChannelControlFailed | 0x400011fa | Controlling child device channel failed. |
| 4.0 | Invalid Operation | deviceNotInConference | 0x400011fb | Device is not in a meeting. |
| 4.0 | Invalid Operation | alreadyExistConference | 0x400011fc | Meeting already exists. |
| 4.0 | Invalid Operation | noSupportWithVideoConference | 0x400011fd | This function is not supported in current video conference. |
| 4.0 | Invalid Operation | startInteractionFailure | 0x400011fe | Starting interaction failed. |
| 4.0 | Invalid Operation | askQuestionStarted | 0x400011ff | Asking question is started. |
| 4.0 | Invalid Operation | askQuestionClosed | 0x40001200 | Asking question is finished. |
| 4.0 | Invalid Operation | unableOperateByHost | 0x40001201 | Operation is not allowed. The host has already disabled it. |
| 4.0 | Invalid Operation | repeatedAskQuestion | 0x40001202 | Duplicate question. |
| 4.0 | Invalid Operation | ipcChannelIsInPip | 0x40001203 | Operation failed. |
| 4.0 | Invalid Operation | updateattrvalueduplicationofname | 0x40001204 | Editing failed. Duplicate edited attribute value name. |
| 4.0 | Invalid Operation | addattributeduplicatioofname | 0x40001205 | Adding failed. Duplicate added attribute name. |
| 4.0 | Invalid Operation | addattrvalueduplicationofname | 0x40001206 | Adding failed. Duplicate added attribute value name. |
| 4.0 | Invalid Operation | addlabelduplicationofname | 0x40001207 | Adding failed. Duplicate added tag name. |
| 4.0 | Invalid Operation | attrhasbeenmarked | 0x40001208 | The attribute has been marked and cannot be deleted. |
| 4.0 | Invalid Operation | attrvaluehasbeenmarked | 0x40001209 | The attribute value has been marked and cannot be deleted. |
| 4.0 | Invalid Operation | podCreateFailed | 0x4000120a | Creating task scheduling unit failed. |
| 4.0 | Invalid Operation | podDeleteFailed | 0x4000120b | Deleting task scheduling unit failed. |
| 4.0 | Invalid Operation | podQueryFailed | 0x4000120c | Searching task scheduling unit failed. |
| 4.0 | Invalid Operation | podStopFailed | 0x4000120d | Stopping task scheduling unit failed. |
| 4.0 | Invalid Operation | trainGetEnvironmentVaribleFailed | 0x4000120e | Getting environment variables failed. |
| 4.0 | Invalid Operation | subTaskSyncUpdateFailed | 0x4000120f | Updating task simultaneously failed. |
| 4.0 | Invalid Operation | waitingTaskNumIsMaxLimit | 0x40001210 | Waiting queue exceeded limit. |
| 4.0 | Invalid Operation | trainingTaskFailed | 0x40001211 | Training model failed. |
| 4.0 | Invalid Operation | covertingTaskFailed | 0x40001212 | Transforming model failed. |
| 4.0 | Invalid Operation | initFailed | 0x40001213 | Initializing task failed. |
| 4.0 | Invalid Operation | haeParameterInvalid | 0x40001214 | Incorrect HAE parameter. |
| 4.0 | Invalid Operation | taskNotExitOrFailed | 0x40001215 | The task does not exist or has failed. |
| 4.0 | Invalid Operation | trainDataPrasingError | 0x40001216 | Parsing the data failed. |
| 4.0 | Invalid Operation | dataTxtGenerateFailed | 0x40001217 | Generating the data file failed. |
| 4.0 | Invalid Operation | taskMkdirFailed | 0x40001218 | Generating the file path failed. |
| 4.0 | Invalid Operation | taskDeleteFileFailed | 0x40001219 | Deleting the file(s) failed. |
| 4.0 | Invalid Operation | taskRollbackFailed | 0x4000121a | Task error. Rolling back failed. |
| 4.0 | Invalid Operation | switchtimedifflesslimit | 0x4000121b | The time difference between powering on and powering off should be larger than or equal to 10 minutes. |
| 4.0 | Invalid Operation | channelDeviceExist | 0x4000121c | Device(s) have already been added to the current channel. |
| 4.0 | Invalid Operation | channelDeviceNotExist | 0x4000121d | No device exists in the current channel. |
| 4.0 | Invalid Operation | notEnoughStorageAvailable | 0x4000121e | Not enough available storage space. XXX MB space is required. |
| 4.0 | Invalid Operation | pleaseWaitForClusterDisbandment | 0x4000121f | Disbanding the cluster...Please wait. |
| 4.0 | Invalid Operation | labelhasbeenmarked | 0x40001220 | Deleting is not allowed. The tag(s) to be deleted have been marked. |
| 4.0 | Invalid Operation | transformingtaskcontainsthedataset | 0x40001221 | Deleting is not allowed. The data set is contained in the conversion task. |
| 4.0 | Invalid Operation | trainingtaskcontainsthepicture | 0x40001222 | Deleting is not allowed. This picture is contained in the training task. |
| 4.0 | Invalid Operation | unconvertedtaskcontainsthepicture | 0x40001223 | Deleting the picture needs to be confirmed. This picture is contained in the unconverted trained task. |
| 4.0 | Invalid Operation | transformingtaskcontainsthepicture | 0x40001224 | Deleting is not allowed. This picture is contained in the conversion task. |
| 4.0 | Invalid Operation | binDownloadTypeNotSupport | 0x40001225 | The downloading type of the bin file is not supported. |
| 4.0 | Invalid Operation | binDecryptTypeNotSupport | 0x40001226 | The encryption type of the bin file is not supported. |
| 4.0 | Invalid Operation | theNumberOfLabelsReachesTheUpperLimit | 0x40001227 | No more labels are allowed. |
| 4.0 | Invalid Operation | theNumberOfAttributesReachesTheUpperLimit | 0x40001228 | No more attributes are allowed. |
| 4.0 | Invalid Operation | theNumberOfAttributeValuesReachesTheUpperLimit | 0x40001229 | No more attribute values are allowed. |
| 4.0 | Invalid Operation | getTokenFailed | 0x4000122a | Getting token failed. |
| 4.0 | Invalid Operation | databaseLackPicture | 0x4000122b | Not enough picture in the data set. |
| 4.0 | Invalid Operation | Video/picturePre-allocationMustBeAMultipleOf10/20 | 0x4000122c | The number of pre-allocated video/picture resources must be a multiple of 10/20. |
| 4.0 | Invalid Operation | transferTypeAlreadyApply | 0x4000122d | The conversion type already exists. |
| 4.0 | Invalid Operation | algorithmImportFailed | 0x4000122e | Importing the algorithm to the library failed. |
| 4.0 | Invalid Operation | faceModelVerionError | 0x4000122f | Face model versions mismatch. |
| 4.0 | Invalid Operation | resourceAllocationRoutesShouldNotBeLessThan TheAllocatedRoutesDeleteTasksAndThenOperate | 0x40001230 | The number of channels configured for the resource should be greater than or equal to that of the allocated channels. Delete the task and try again. |
| 4.0 | Invalid Operation | dataSetIdIsInvalid | 0x40001231 | Data set ID does not exist. |
| 4.0 | Invalid Operation | labelIdIsInvalid | 0x40001232 | Tag ID does not exist. |
| 4.0 | Invalid Operation | attrIdIsInvalid | 0x40001233 | Attribute ID does not exist |
| 4.0 | Invalid Operation | attrvalueIdIsInvalid | 0x40001234 | Attribute value ID does not exist |
| 4.0 | Invalid Operation | pictureIdIsInvalid | 0x40001235 | Picture ID does not exist. |
| 4.0 | Invalid Operation | runningTaskContainsTheLabel | 0x40001236 | Deleting the tag is not allowed. This tag is contained in the running task. |
| 4.0 | Invalid Operation | convertingTaskContainsTheLabel | 0x40001237 | Deleting the tag is not allowed. The tag is contained in the conversion task. |
| 4.0 | Invalid Operation | deleteTaskFirst | 0x40001238 | Delete the model task first and then delete the model. |
| 4.0 | Invalid Operation | deleteApplyFirst | 0x40001239 | Delete the conversion task first and then delete the model version training task. |
| 4.0 | Invalid Operation | taskModelNumLimit | 0x4000123a | No more model version training tasks are allowed. |
| 4.0 | Invalid Operation | noData | 0x4000124b | No data exported. |
| 4.0 | Invalid Operation | ssModelError | 0x4000124c | Scheduling module error. |
| 4.0 | Invalid Operation | esModelError | 0x4000124d | Engine module error. |
| 4.0 | Invalid Operation | tmsModelError | 0x4000124e | Stream component module error. |
| 4.0 | Invalid Operation | daModelError | 0x4000124f | Face picture analysis module error. |
| 4.0 | Invalid Operation | vaModelError | 0x40001250 | Vehicle picture analysis module error. |
| 4.0 | Invalid Operation | vsModelError | 0x40001251 | Video structuralization module error. |
| 4.0 | Invalid Operation | ndModelError | 0x40001252 | Post-processing component module error. |
| 4.0 | Invalid Operation | acModelError | 0x40001253 | Analyzing public module error. |
| 4.0 | Invalid Operation | tsModelError | 0x40001254 | Forwarding service module error. |
| 4.0 | Invalid Operation | anModelError | 0x40001255 | Computing node error. |
| 4.0 | Invalid Operation | getFingerInfoFail | 0x40001256 | Getting the hardware fingerprint failed. |
| 4.0 | Invalid Operation | setUpLicenseFail | 0x40001257 | Installing the certificate failed. |
| 4.0 | Invalid Operation | setUpLicenseAlready | 0x40001258 | The certificate has been installed. |
| 4.0 | Invalid Operation | deleteAlgorithmFailed | 0x40001259 | Deleting the algorithm package failed. |
| 4.0 | Invalid Operation | taskIdNotMatchTaskType | 0x4000125a | Task ID and type mismatch. |
| 4.0 | Invalid Operation | channelIpAddrConflictWithDev | 0x4000125b | The IP address of the current channel conflicts with that of the device. |
| 4.0 | Invalid Operation | channelIsConnecting | 0x4000125c | The current channel is connecting... |
| 4.0 | Invalid Operation | channelStreamTypeNotSupport | 0x4000125d | The stream type of the current channel is not supported. |
| 4.0 | Invalid Operation | channelBadLanguage | 0x4000125e | The language of the current channel mismatches. |
| 4.0 | Invalid Operation | channelUsernameNotExist | 0x4000125f | The user does not exist in the current channel. |
| 4.0 | Invalid Operation | channelAccessParamFailure | 0x40001260 | Getting parameters of the current channel failed. |
| 4.0 | Invalid Operation | channelGetStreamFailure | 0x40001261 | Getting the stream of the current channel failed. |
| 4.0 | Invalid Operation | channelRiskPassword | 0x40001262 | The default password of the current channel is risky. |
| 4.0 | Invalid Operation | taskModelNameConflict | 0x40001263 | Duplicate model name. |
| 4.0 | Invalid Operation | ModelConfirmTimeOut | 0x40001264 | Loading the algorithm... Please wait for 1 to 2 minutes and try again. |
| 4.0 | Invalid Operation | algorithmIsPacking | 0x40001265 | Importing the algorithm package to the library... Please wait for 1 to 2 minutes and try again. |
| 4.0 | Invalid Operation | cropPictureFailed | 0x40001266 | Matting picture(s) failed. |
| 4.0 | Invalid Operation | addDatasetRepeat | 0x40001267 | Adding the data set failed. Duplicate data set name. |
| 4.0 | Invalid Operation | updateDatasetRepeat | 0x40001268 | Editing the data set failed. Duplicate data set name. |
| 4.0 | Invalid Operation | outOfResource | 0x40001269 | The model cannot be verified now. Not enough GPU resource. |
| 4.0 | Invalid Operation | forbidOperSendChanCfgInConf | 0x40001270 | Editing encoding parameters of the stream sending channel is not allowed during the interactive meeting. |
| 4.0 | Invalid Operation | noSupportWithDiffSendChanCfg | 0x40001271 | Initiating interaction failed. The encoding parameters of the channel sending the interactive meeting stream are inconsistent. |
| 4.0 | Invalid Operation | modelUrlIsEmpty | 0x40001272 | Importing the model to the library failed. The model URL is empty. |
| 4.0 | Invalid Operation | mergeNotSupportVehicleSearch | 0x40001273 | Fusion Big Data V1.0.0 does not support searching the vehicle report type. |
| 4.0 | Invalid Operation | exceedMergeVehicleTimeRange | 0x40001274 | The time range for searching vehicles in Fusion Big Data cannot exceed three months. |
| 4.0 | Invalid Operation | storageSpaceNotEnough | 0x40001275 | Uploading picture(s) failed. HDD is full. |
| 4.0 | Invalid Operation | faceListTooMuchCan'tSlcingData | 0x40001276 | Benchmarking manually is not allowed. Too many lists. |
| 4.0 | Invalid Operation | insufficientTranscodingResources | 0x40001277 | Not enough transcoding resource. |
| 4.0 | Invalid Operation | diskDataReconstruction | 0x40001278 | Rebuilding the HDD data… |
| 4.0 | Invalid Operation | associatedFaceLibNumOverLimit | 0x40001279 | No more linked face picture libraries are allowed. |
| 4.0 | Invalid Operation | taskNameAlreadyExists | 0x4000127a | The task name already exists. |
| 4.0 | Invalid Operation | personnelDensityEventsCannotRunInOneTaskWithOtherEvents | 0x4000127b | The people density event cannot be run in the same task together with other events. |
| 4.0 | Invalid Operation | can'tSetUpSingleRunningAndMultipleRunningInOneTaskAtTheSameTime | 0x4000127c | The single-person running and multi-person running cannot be set in a task at the same time. |
| 4.0 | Invalid Operation | soundIntensityCatastropheEventsCanOnlyBeAssignedToOneRule | 0x4000127d | Only one rule can be configured for sudden change of sound intensity detection. |
| 4.0 | Invalid Operation | intelligentModeIsSameWithBefore | 0x4000127e | The smart mode remains unchanged and is the same as that before setting. |
| 4.0 | Invalid Operation | theTaskHasBeenCompleted | 0x4000127f | Task completed. |
| 4.0 | Invalid Operation | TasksNumOverRemainLimit | 0x40001280 | The number of created tasks exceeded that of remained tasks allowed to be configured. |
| 4.0 | Invalid Operation | algorithmpackagefileerror | 0x40001281 | The algorithm package file is damaged. |
| 4.0 | Invalid Operation | algorithmmodelversionsneedtobeconsistent | 0x40001282 | The algorithm model version should be consistent. |
| 4.0 | Invalid Operation | analyticalalgrequireassociationandalignmentalg | 0x40001283 | The analysis algorithm should be linked to the comparison algorithm. |
| 4.0 | Invalid Operation | errorinalgorithmipackageconfigfile | 0x40001284 | The configuration file of the algorithm package error. |
| 4.0 | Invalid Operation | modelcheckcannotbeopened | 0x40001285 | Enabling model verification failed. The algorithm model version is inconsistent. |
| 4.0 | Invalid Operation | algorithmoutputrulefiledoesnotexist | 0x40001286 | The output rule file of the algorithm package does not exist. |
| 4.0 | Invalid Operation | algorithmpacketunzipfailed | 0x40001287 | Extracting the algorithm package failed. |
| 4.0 | Invalid Operation | noMoreGetUpRulesAdded | 0x40001288 | No more out of bed detection rules are allowed. |
| 4.0 | Invalid Operation | noMoreStandUpRulesAdded | 0x40001289 | No more people standing up detection rules are allowed. |
| 4.0 | Invalid Operation | noMorePeopleNumChangeRulesAdded | 0x4000128A | No more people number change detection rules are allowed. |
| 4.0 | Invalid Operation | noMoreToiletTarryRulesAdded | 0x4000128B | No more in-toilet overtime detection rules are allowed. |
| 4.0 | Invalid Operation | noMoreAdvReachHeightRulesAdded | 0x4000128C | No more climbing rules are allowed. |
| 4.0 | Invalid Operation | noMoreViolentMotionRulesAdded | 0x4000128D | No more violent motion detection rules are allowed. |
| 4.0 | Invalid Operation | noMoreLeavePositionRulesAdded | 0x4000128E | No more absence rules are allowed. |
| 4.0 | Invalid Operation | insufficientAnalyticalAbilityofSmartBoar | 0x4000128F | Not enough VCA board analysis capability. |
| 4.0 | Invalid Operation | intelligentChannelNumOverLimit | 0x40001290 | No more channels for VCA rules are allowed. |
| 4.0 | Invalid Operation | SMRDiskNotSupportRaid | 0x40001291 | SMR disk does not support RAID due to performance limitations. |
| 4.0 | Invalid Operation | faceContratAlgorithmNotFound | 0x40001292 | Face picture comparison algorithm does not exist. |
| 4.0 | Invalid Operation | faceContratAlgorithmLoading | 0x40001293 | The face picture comparison algorithm is being loaded. |
| 4.0 | Invalid Operation | faceContratAlgorithmUnloading | 0x40001294 | The face picture comparison algorithm is being uninstalled. |
| 4.0 | Invalid Operation | getCalclatePoolFail | 0x40001295 | Getting the computing resource pool failed. |
| 4.0 | Invalid Operation | OpenModellingModeMustPreallocationFacePictureAlgorithms | 0x40001296 | Enabling the function of specifying the chip automatically for synchronous face picture analysis requires the pre-allocation of face picture resources. |
| 4.0 | Invalid Operation | algorithmPackTypeNotSupport | 0x40001297 | The packet type of the algorithm is not supported. |
| 4.0 | Invalid Operation | selfRelationNotSupported | 0x40001298 | The algorithm does not support linking to itself. |
| 4.0 | Invalid Operation | duplicateRelationNotSupported | 0x40001299 | The algorithm does not support repeated linkage. |
| 4.0 | Invalid Operation | sameTypeAlgorithmCannotRelation | 0x4000129a | The algorithm does not support linkage of the same type. |
| 4.0 | Invalid Operation | algorithmDoNotSupportTheTargetRelation | 0x4000129b | The algorithm does not support this target linkage. |
| 4.0 | Invalid Operation | algorithmNotSupportModifyingDescription | 0x4000129c | The algorithm does not support editing the description. |
| 4.0 | Invalid Operation | relationNeedSameVendorAlgs | 0x4000129d | The manufacturer should be the same for algorithm linkage. |
| 4.0 | Invalid Operation | needDeleteDigitalChannel | 0x4000129e | The digital channel(s) need to be deleted. |
| 4.0 | Invalid Operation | vehicleAnalysisNull | 0x4000129f | The vehicle picture analysis result is empty. |
| 4.0 | Invalid Operation | enabledIntelligentChannelFirst | 0x400012A0 | Enable the smart channel first. |
| 4.0 | Invalid Operation | videoMissionCompletedOrFailedCanNotBeReissued | 0x400012a1 | The recording task has finished or failed and cannot be applied again. Delete it first and then apply it again. |
| 4.0 | Invalid Operation | faceInitFail | 0x400012a2 | Initializing the maintenance of the face picture list library failed. |
| 4.0 | Invalid Operation | OnlySupportHikAndCustomProtocol | 0x400012a3 | Currently only adding IPv6 cameras via Hikvision protocol and custom protocol is supported. |
| 4.0 | Invalid Operation | LicenseDogIsNotDetectedClusteringIsNotAllowed | 0x400012a4 | No dongle detected. Creating the analysis cluster is not allowed. |
| 4.0 | Invalid Operation | getLogUrlFail | 0x400012a5 | Getting the URL for exporting logs failed. |
| 4.0 | Invalid Operation | vehicleEnginesNoResource | 0x400012a6 | Not enough vehicle engine resource. |
| 4.0 | Invalid Operation | NotEnoughSeatsClusteringIsNotAllowed | 0x400012a7 | Not enough licenses currently. Creating a cluster is not allowed. |
| 4.0 | Invalid Operation | MultipleCentreAuthenticationDogAreNotAllowedInTheCluster | 0x400012a8 | Multiple central authorization devices are not allowed in the cluster. |
| 4.0 | Invalid Operation | noMoreRunningRulesAdded | 0x400012a9 | No more people running rules are allowed. |
| 4.0 | Invalid Operation | noMoreGroupRulesAdded | 0x400012aa | No more people gathering rules are allowed. |
| 4.0 | Invalid Operation | noMoreFailDownRulesAdded | 0x400012ab | No more rules of people falling down are allowed. |
| 4.0 | Invalid Operation | noMorePlayCellphoneRulesAdded | 0x400012ac | No more rules of using mobile phone are allowed. |
| 4.0 | Invalid Operation | supAnalyTimeMin2 | 0x400012ad | When no channel of the device is enabled for intelligent analysis, the minimum analysis interval is 2 seconds. |
| 4.0 | Invalid Operation | supAnalyTimeMin5 | 0x400012ae | When one channel of the device is enabled for intelligent analysis, the minimum analysis interval is 5 seconds. |
| 4.0 | Invalid Operation | supAnalyTimeMin7 | 0x400012af | When two channels of the device are enabled for intelligent analysis, the minimum analysis interval is 7 seconds. |
| 4.0 | Invalid Operation | supOneWay | 0x400012b0 | Not enough engine performance. The device only supports enabling one channel for character recognition. |
| 4.0 | Invalid Operation | openOcrFailedByCourseDetNotOpen | 0x400012b1 | Enabling OCR character recognition failed. Courseware detection is not enabled. |
| 4.0 | Invalid Operation | curOcrOpeningByCourseDetForbidClose | 0x400012b2 | Courseware detection cannot be stopped. The OCR character recognition is running. |
| 4.0 | Invalid Operation | fireEscapeDetectionDurationNotLessThanAnalysisEnginesAutoSwitchTime | 0x400012b3 | The overstay time of the object in the fire escape is longer than or equal to the engine's polling time linked with it. |
| 4.0 | Invalid Operation | analysisEnginesAutoSwitchTimeNotGreaterThanfireEscapeDetectionDuration | 0x400012b4 | The polling time of the engine is shorter than or equal to the overstay time of the object in the fire escape of its linked channel. |
| 4.0 | Invalid Operation | leavePositionDelayNotLessThanAnalysisEnginesAutoSwitchTime | 0x400012b5 | The absence or sleep on duty time is longer than or equal to the engine's polling time linked with it. |
| 4.0 | Invalid Operation | analysisEnginesAutoSwitchTimeNotGreaterThanLeavePositionDelay | 0x400012b6 | The polling time of the engine is shorter than or equal to the absence or sleep on duty time of its linked channel. |
| 4.0 | Invalid Operation | cityManagementAlarmIntervalTimeNotLessThanAnalysisEnginesAutoSwitchTime | 0x400012b7 | The time interval of the city management alarm is longer than or equal to the engine's polling time linked with it. |
| 4.0 | Invalid Operation | analysisEnginesAutoSwitchTimeNotGreaterThanCityManagementAlarmIntervalTime | 0x400012b8 | The polling time of the engine is shorter than or equal to the time interval of the city management alarm of the linked channel. |
| 4.0 | Invalid Operation | taskBusy | 0x400012b9 | The task is executing another operation and cannot respond to this operation. (For example, the task is being paused and you cannot search for the task progress or resume the task.) |
| 4.0 | Invalid Operation | filePathIsEmpty | 0x400012ba | The path is empty. |
| 4.0 | Invalid Operation | filePathLengthIsTooLong | 0x400012bb | The path is too long. |
| 4.0 | Invalid Operation | filePathIsNotExist | 0x400012bc | The path does not exist. |
| 4.0 | Invalid Operation | noMoreUnregisteredStreetVendorRulesAdded | 0x400012bd | No more rules of unregistered street vendor are allowed. |
| 4.0 | Invalid Operation | noMoreStallOutsideShopRulesAdded | 0x400012be | No more rules of business outside store are allowed. |
| 4.0 | Invalid Operation | noMoreStallOccupyingRoadRulesAdded | 0x400012bf | No more rules of business on sidewalk are allowed. |
| 4.0 | Invalid Operation | noMoreIllegalHeapRulesAdded | 0x400012c0 | No more rules of piling goods or materials in chaos are allowed. |
| 4.0 | Invalid Operation | noMoreIllegalParkingofNon-MotorVehicleRulesAdded | 0x400012c1 | No more rules of non-motor vehicles parking in chaos are allowed. |
| 4.0 | Invalid Operation | noMoreIllegalOutdoorAdvertisementRulesAdded | 0x400012c2 | No more outdoor advertisement rules are allowed. |
| 4.0 | Invalid Operation | noMorePackGarbageRulesAdded | 0x400012c3 | No more packaged garbage rules are allowed. |
| 4.0 | Invalid Operation | noMoreStallUnderUmbrellaRulesAdded | 0x400012c4 | No more illegal umbrella rules are allowed. |
| 4.0 | Invalid Operation | noMoreDustbinOverflowRulesAdded | 0x400012c5 | No more overflowing dustbin rules are allowed. |
| 4.0 | Invalid Operation | noMoreExposeGarbageRulesAdded | 0x400012c6 | No more exposed garbage rules are allowed. |
| 4.0 | Invalid Operation | noMoreHangClothingAlongStreetRulesAdded | 0x400012c7 | No more rules of hanging stuff along the street are allowed. |
| 4.0 | Invalid Operation | ruleEventTypeDuplicate | 0x400012c8 | Duplicate event type of rules. |
| 4.0 | Invalid Operation | getChannelListError | 0x400012c9 | Getting the channel list failed. |
| 4.0 | Invalid Operation | existSameLicensePlate | 0x400012ca | The license plate number already exists |
| 4.0 | Invalid Operation | licensePlateNumOverflow | 0x400012cb | No more license plates are allowed. |
| 4.0 | Invalid Operation | noCDsInCakeBoxwithEmptyCDs | 0x400012cc | No disks are in the CD cake box. |
| 4.0 | Invalid Operation | deviceIsPrinting | 0x400012cd | The device is printing. |
| 4.0 | Invalid Operation | CDWarehouseDoorIsOpen | 0x400012ce | The front panel is open. |
| 4.0 | Invalid Operation | analyzingCannotFormatDisk | 0x400012cf | Task analysis is in progress. Stop it first. |
| 4.0 | Invalid Operation | plateListIsBindingChannel | 0x400012d0 | The license plate library is linked to a channel. Unlink and try again. |
| 4.0 | Invalid Operation | licensePlateNumWillOverflow | 0x400012d1 | The number of license plates is going to reach the limit. |
| 4.0 | Invalid Operation | plateListIsOperating | 0x400012d2 | Processing the license plate data. No operation is allowed. |
| 4.0 | Invalid Operation | channelNotReady | 0x400012d3 | The smart channel is not enabled or initialized. Configure rules later. |
| 4.0 | Invalid Operation | frequentFormatDisk | 0x400012d4 | Formatting operation is too frequent. Try again later. |
| 4.0 | Invalid Operation | getFileTimeError | 0x400012d5 | Getting the video file time failed. |
| 4.0 | Invalid Operation | noMoreRetentionRulesAdded | 0x400015ad | No more people overstay rules are allowed. |
| 4.0 | Invalid Operation | noMoreSleepOnDutyRulesAdded | 0x400015ae | No more sleeping on duty rules are allowed. |
| 4.0 | Invalid Operation | plsCloseVideoConfTry | 0x400015af | Operation failed. Please end the video meeting and try again. |
| 4.0 | Invalid Operation | plsAfterLogoutRetry | 0x400015B0 | Please log out and try again. |
| 4.0 | Invalid Operation | conferenceRoomError | 0x400015B1 | Incorrect meeting ID. |
| 4.0 | Invalid Operation | forbidOperateChanEnable | 0x400015B2 | Enabling or disabling channel is not allowed during meeting. |
| 4.0 | Invalid Operation | singleStreamRecvOver1080P | 0x400015B3 | Single-Channel receiving stream exceeded 1080p. |
| 4.0 | Invalid Operation | allStreamRecvOver7\*1080P | 0x400015B4 | Total receiving stream exceeded 7\*1080p. |
| 4.0 | Invalid Operation | needOpenVideoStream | 0x400015B5 | Audio cannot be enabled without video. |
| 4.0 | Invalid Operation | inQuestMediaOperisForbid | 0x400015B6 | Controlling audio and video is not allowed when asking question. |
| 4.0 | Invalid Operation | inConferenceForbidOper | 0x400015B7 | Setting parameters is not allowed in interactive meeting. |
| 4.0 | Invalid Operation | curAccountNotservicePleaseRecharge | 0x400015B8 | Current account has expired and cannot enter meeting room. Please top up first. |
| 4.0 | Invalid Operation | noSupportWithCloudConference | 0x400015B9 | The video encoding format of the current channel is H.265. Interactive meeting is not supported. |
| 4.0 | Invalid Operation | registerAccountConnectErr | 0x400015BA | Connecting to the address of the register platform failed. |
| 4.0 | Invalid Operation | PlateListIDNotExist | 0x400015BB | ID of license plate library does not exist. |
| 4.0 | Invalid Operation | onlyForHikProtocolAccess | 0x400015BC | Non-Hikvision protocol does not support motion detection. |
| 4.0 | Invalid Operation | onlyH264AndH265 | 0x400015BD | Incorrect encoding format. Only H264 and H265 are supported. |
| 4.0 | Invalid Operation | overResolutionLimited | 0x400015BE | Resolution exceeded limit. |
| 4.0 | Invalid Operation | PlateIDNotExist | 0x400015BF | License plate ID does not exist. |
| 4.0 | Invalid Operation | noMoreVMDHumanVehicle | 0x400015C0 | Number of motion detection channels exceeded limit. |
| 4.0 | Invalid Operation | taskIDArrayOverflow | 0x400015C1 | Number of task arrays overflow. |
| 4.0 | Invalid Operation | polygonNotAllowCrossing | 0x400015C2 | Polygons are not allowed to overlap. |
| 4.0 | Invalid Operation | setHcsInfoFailed | 0x400015C3 | Configuring cloud storage failed. |
| 4.0 | Invalid Operation | ?urlCheckAkFailed | 0x400015C4 | Verifying AK information in the URL failed. |
| 4.0 | Invalid Operation | LxcDeviceNotSupportSettingIp | 0x400015C5 | LXC device does not support editing IP address. |
| 4.0 | Invalid Operation | cannotSupportDoubleRoomPreemptiveBurn | 0x400015C6 | Configuring burning for two rooms is not supported. |
| 4.0 | Invalid Operation | noFaceInPicture | 0x400015C7 | No face in the picture. |
| 4.0 | Invalid Operation | NoPodiumArea | 0x400015C8 | Network camera has not configured the podium area. |
| 4.0 | Invalid Operation | recording | 0x400015C9 | Configuring encoding parameters failed. Device is recording. |
| 4.0 | Invalid Operation | repeatedURL | 0x400015CA | Duplicate URL. |
| 4.0 | Invalid Operation | duplicateAudioName | 0x400015CB | Duplicate audio file name. |
| 4.0 | Invalid Operation | InvalidAudioFileFormat | 0x400015CC | Incorrect audio format. |
| 4.0 | Invalid Operation | insufficientAudioSpace | 0x400015CD | Not enough audio space. Total size of imported audio file is larger than that of reserved space. |
| 4.0 | Invalid Operation | deviceAudio | 0x400015CE | Local audio cannot be deleted. |
| 4.0 | Invalid Operation | insufficientStreetBehaviorEngine | 0x400015CF | Not enough engine resources for street behavior analytics. |
| 4.0 | Invalid Operation | insufficientWorkBehaviorEngine | 0x400015D0 | Not enough engine resources for work behavior analytics. |
| 4.0 | Invalid Operation | ExistLowFreqTask | 0x400015D1 | Configuring personnel archive is not allowed. Low frequency task is running. |
| 4.0 | Invalid Operation | autoUpdateLibNumsExceedLimiti | 0x400015D2 | Number of face picture libraries for self-learning exceeded limit. |
| 4.0 | Invalid Operation | coverTemplateBinded | 0x400015D3 | The template is linked. Link another template. |
| 4.0 | Invalid Operation | audioChannelInProgress | 0x400015D4 | Audio channel is busy. |
| 4.0 | Invalid Operation | badSectorsTesting | 0x400015D5 | Device is running bad sector detection. |
| 4.0 | Invalid Operation | IPCNotExist | 0x400015D6 | Network camera does not exist. |
| 4.0 | Invalid Operation | serialNumberMismatched | 0x400015D7 | Inconsistent serial No. |
| 4.0 | Invalid Operation | maxPeopleFallingDownRuleReached | 0x400015D8 | No more people falling down rules are allowed. |
| 4.0 | Invalid Operation | maxViolentMotionRuleReached | 0x400015D9 | No more violent motion detection rules are allowed. |
| 4.0 | Invalid Operation | devIndexNotExisted | 0x400015DA | Proxy device ID does not exist. |
| 4.0 | Invalid Operation | agentDeviceNotOnline | 0x400015DB | Proxy device is offline. |
| 4.0 | 操作错误 | belowRequiredNASCapacity | 0x400015DC | Network disc capacity is lower than needed. |
| 4.0 | 操作错误 | noRegionEntranceRegion | 0x400015DD | Configuring personnel entrance region is required. |
| 4.0 | 操作错误 | ruleNotMatchAnalysisMode | 0x400015DF | Rule conflicts with the configuration information of the current mode. |
| 4.0 | Invalid Operation | emptyEventName | 0x400015E0 | Event description is required. |
| 4.0 | Invalid Operation | sameEventName | 0x400015E1 | Duplicate event description. |
| 4.0 | Invalid Operation | emptyEventType | 0x400015E2 | Event type is required. |
| 4.0 | Invalid Operation | sameEventType | 0x400015E3 | Duplicate event type. |
| 4.0 | Invalid Operation | maxEventNameReached | 0x400015E4 | No more event descriptions are allowed. |
| 4.0 | Invalid Operation | SVCEnhanceMutexWith4KOutPut | 0x400015E5 | Enhanced SVC mode and 4K resolution output are mutually exclusive. |
| 4.0 | Invalid Operation | eventNameConflict | 0x400015E6 | Duplicate descriptions in configuration and table. |
| 4.0 | Invalid Operation | smartAnalysisUnitError | 0x400015E7 | VCA board exception. |
| 4.0 | Invalid Operation | noEncodedResource | 0x400015E8 | Not enough encoding resources. |
| 4.0 | Invalid Operation | noAudioData | 0x400015E9 | No audio data collected. |
| 4.0 | Invalid Operation | curConferenceMemberisFull | 0x400016BB | Joining meeting failed. No more people are allowed for current meeting. |
| 4.0 | Invalid Operation | curConferenceServerConnectFaild | 0x400017BC | Connecting to the meeting server failed. |
| 4.0 | Invalid Operation | registerAccountRecvErr | 0x400018BD | Receiving data from the register platform failed. |
| 4.0 | Invalid Operation | sendChanCodecErrAddConfFaild | 0x400019BE | Joining meeting failed. Please adjust channel parameters in Video Settings and try again. |
| 4.0 | Invalid Operation | NotSupportAudioSourceConfig | 0x400019BF | Configuring audio source is not supported. |
| 4.0 | Invalid Operation | LxcForbidSetdefAll | 0x400019C0 | Restoring all operations is not supported by LXC device. |
| 4.0 | Invalid Operation | UpdateFileRSAError | 0x400019C1 | Incorrect upgrading package signature. |
| 4.0 | Invalid Operation | EnablePersonalTaskFirst | 0x400019C2 | Configure personnel archive before creating low frequency task. |
| 4.0 | Invalid Operation | PicSyncSearchTimeRangeLimit | 0x400019C3 | Time range for picture sync search cannot exceed 15 days. |
| 4.0 | Invalid Operation | AlgSearchFailed | 0x400019E0 | No specified algorithm package found. |
| 4.0 | Invalid Operation | ImageSearchFailed | 0x400019E1 | Searching algorithm training images failed. |
| 4.0 | Invalid Operation | ScheduUnsupport | 0x400019E2 | Task pausing and restoring are only supported by self-learning training. |
| 4.0 | Invalid Operation | HasRunningTask | 0x400019E3 | Switching to inferring mode is not allowed. Task in progress is contained. |
| 4.0 | Invalid Operation | UpdateSendInterrupt | 0x400019E4 | Sending upgrade package to node is interrupted. |
| 4.0 | Invalid Operation | RequestUrlIsNull | 0x400019F3 | Request path is required. |
| 4.0 | Invalid Operation | RequestUrlNotFound | 0x400019F4 | The request path does not exist. |
| 4.0 | Invalid Operation | NoToken | 0x400019F5 | Token is required in the request. |
| 4.0 | Invalid Operation | ClusterC360ServiceException | 0x400019F6 | Requesting cluster c360 service exception. |
| 4.0 | Invalid Operation | ClusterCloudStorageServiceException | 0x400019F7 | Requesting cluster cloud storage service exception. |
| 4.0 | Invalid Operation | StroageTypeNotSupport | 0x400019F8 | Storage type is not supported. |
| 4.0 | Invalid Operation | nodeTypeNotSupport | 0x400019F9 | Node type is not supported. |
| 4.0 | Invalid Operation | nodeStatusNotSupport | 0x400019FA | Node status is not supported. |
| 4.0 | Invalid Operation | softlockVersionIsNotRight | 0x400019FB | Incorrect soft lock version. |
| 4.0 | Invalid Operation | softlockDataTypeIsNotRight | 0x400019FC | Incorrect soft lock data type. |
| 4.0 | Invalid Operation | softlockAlgorithmTypeIsNotRight | 0x400019FD | Incorrect soft lock algorithm type. |
| 4.0 | Invalid Operation | softlockUnitIsNotRight | 0x400019FE | Incorrect soft lock unit. |
| 4.0 | Invalid Operation | softlockNumberIsNotRight | 0x400019FF | Incorrect soft lock amount. |
| 4.0 | Invalid Operation | GetingNodeNetInfo | 0x40001A00 | Obtaining network information of analysis node...Please wait. |
| 4.0 | Invalid Operation | SetNodeNtpError | 0x40001A01 | Setting NTP server information of analysis node failed. |
| 4.0 | Invalid Operation | theSubClassIsFull | 0x40001A02 | Number of sub-categories reached limit. |
| 4.0 | Invalid Operation | theSubClassIsExited | 0x40001A03 | Sub-Category already exists. |
| 4.0 | Invalid Operation | theSubClassIsNotExited | 0x40001A04 | Sub-Category does not exist. |
| 4.0 | Invalid Operation | theSubClassHasRecord | 0x40001A05 | Deleting the sub-category is not allowed. It contains algorithm records. |
| 4.0 | Invalid Operation | theTestDatasetCannotBeDeleted | 0x40001A06 | Deleting the test set is not allowed. It is contained in the running task. |
| 4.0 | Invalid Operation | maxFaceContrastRoutes | 0x40001A07 | Face picture comparison channels exceeded limit. |
| 4.0 | Invalid Operation | maxVideoTaskNumber | 0x40001A08 | Video structuralization channels exceeded limit. |
| 4.0 | Invalid Operation | maxPerimeterRoutes | 0x40001A09 | Perimeter protection channels exceeded limit. |
| 4.0 | Invalid Operation | maxFaceDecetionNumber | 0x40001A0A | Facial detection channels exceeded limit. |
| 4.0 | 操作错误 | theDeviceNumLimit | 0x40001A0B | No more devices can be added. |
| 4.0 | 操作错误 | theDeviceConflict | 0x40001A0C | Device conflict. |
| 4.0 | 操作错误 | theDeviceCannotBeDeleted | 0x40001A0D | Deleting the device is not allowed. It has been linked. |
| 4.0 | 操作错误 | theCollectTaskNumLimit | 0x40001A0E | No more material collection tasks can be added. |
| 4.0 | 操作错误 | theCollectTaskNameConflict | 0x40001A0F | Duplicate material collection task name. |
| 4.0 | 操作错误 | theHddErr | 0x40001A10 | Creating material collection task failed. HDD error. |
| 4.0 | 操作错误 | theTrainTaskNumLimit | 0x40001A11 | No more algorithm training tasks can be added. |
| 4.0 | 操作错误 | theRelatedDatasetUncompleted | 0x40001A12 | Creating task failed. Linked data set collection has not completed. |
| 4.0 | 操作错误 | theRelatedTestsetUntaged | 0x40001A13 | Creating task failed. Linked test set has not been marked. |
| 4.0 | 操作错误 | associatDatasetCanotBeDeleted | 0x40001A14 | Deleting the data set is not allowed. It has been linked. |
| 4.0 | 操作错误 | associatTestsetCanotBeDeleted | 0x40001A15 | Deleting the test set is not allowed. It has been linked. |
| 4.0 | 操作错误 | faceRecognitionNotSupportOver1080POutput | 0x40001A16 | In facial recognition mode, the maximum supported HDMI output resolution is 1080p. |
| 4.0 | 操作错误 | needCloseLocalPlayback | 0x40001A17 | No more than 8 channels for local synchronous playback are allowed. Close and try again. |
| 4.0 | 操作错误 | noBaytrailMatchesTheModel | 0x40001A18 | Node that matches with the model does not exist. |
| 4.0 | 操作错误 | userNameLocked | 0x40001A19 | The user name is locked. |
| 4.0 | Invalid Operation | ptzOccupiedPriority | 0x40002000 | A user with higher level of permission is operating the PTZ. |
| 4.0 | Invalid Operation | entityNotFound | 0x40002001 | NaN |
| 4.0 | Invalid Operation | entityAlreadyExist | 0x40002002 | NaN |
| 4.0 | Invalid Operation | SMDNoiseReduceWDROrCorridorMutexHighFrame1080P | 0x40002003 | NaN |
| 4.0 | Invalid Operation | highFrame1080PMutexSMDNoiseReduceWDROrCorridor | 0x40002004 | NaN |
| 4.0 | Invalid Operation | WDROrCorridorMutexHighFrame720 | 0x40002005 | NaN |
| 4.0 | Invalid Operation | highFrame720PMutexWDROrCorridor | 0x40002006 | NaN |
| 4.0 | Invalid Operation | WDROrDehazeMutexHLC | 0x40002007 | NaN |
| 4.0 | Invalid Operation | HLCMutexWDROrDehaze | 0x40002008 | NaN |
| 4.0 | Invalid Operation | DDSOrdehazeMutexWDR | 0x40002009 | NaN |
| 4.0 | Invalid Operation | WDRMutexDDSOrDehaze | 0x4000200A | NaN |
| 4.0 | Invalid Operation | highFrame1080PMutexWDROrCorridor | 0x4000200B | NaN |
| 4.0 | Invalid Operation | WDROrCorridorMutexHighFrame1080P | 0x4000200C | NaN |
| 4.0 | Invalid Operation | TransparentMutexPTZ485 | 0x4000200D | NaN |
| 4.0 | Invalid Operation | imageFlipMutexHighFrame1080P | 0x4000200E | NaN |
| 4.0 | Invalid Operation | highFrame1080PMutexImageFlip | 0x4000200F | NaN |
| 4.0 | Invalid Operation | MutexWithWDR | 0x40002010 | NaN |
| 4.0 | Invalid Operation | MutexWithSMD | 0x40002011 | NaN |
| 4.0 | Invalid Operation | MutexWithNoiseReduce | 0x40002012 | NaN |
| 4.0 | Invalid Operation | MutexWithHighFrame1080P | 0x40002013 | NaN |
| 4.0 | Invalid Operation | MutexWithHighFrame720P | 0x40002014 | NaN |
| 4.0 | Invalid Operation | MutexWithDehaze | 0x40002015 | NaN |
| 4.0 | Invalid Operation | MutexWithDSS | 0x40002016 | NaN |
| 4.0 | Invalid Operation | MutexWithHLC | 0x40002017 | NaN |
| 4.0 | Invalid Operation | MutexWithCoord | 0x40002018 | NaN |
| 4.0 | Invalid Operation | MutexWithFlip | 0x40002019 | NaN |
| 4.0 | Invalid Operation | MutexWithPDC | 0x4000201A | NaN |
| 4.0 | Invalid Operation | MutexWithFaceDetection | 0x4000201B | NaN |
| 4.0 | Invalid Operation | MutexWithVehicleDetection | 0x4000201C | NaN |
| 4.0 | Invalid Operation | MutexWithHVTVehicleDetection | 0x4000201D | NaN |
| 4.0 | Invalid Operation | MutexWithStream3 | 0x4000201E | NaN |
| 4.0 | Invalid Operation | MutexWithLensDistortionCorrection | 0x4000201F | NaN |
| 4.0 | Invalid Operation | MutexWithDualVCA | 0x40002020 | NaN |
| 4.0 | Invalid Operation | SMDMutexWithRecordSchedule | 0x40002021 | NaN |
| 4.0 | Invalid Operation | RecordScheduleMutexWithSMD | 0x40002022 | NaN |
| 4.0 | Invalid Operation | MutexWithDualVCAAndSMD | 0x40002023 | NaN |
| 4.0 | Invalid Operation | invalidDisplayParameterSwitch | 0x40002024 | NaN |
| 4.0 | Invalid Operation | MutexWithEIS | 0x40002025 | NaN |
| 4.0 | Invalid Operation | alreadyRunning | 0x40002026 | The application program is running. |
| 4.0 | Invalid Operation | notRunning | 0x40002027 | The application program has stopped. |
| 4.0 | Invalid Operation | packNotFound | 0x40002028 | The software package does not exist. |
| 4.0 | Invalid Operation | alreadyExist | 0x40002029 | The application program already exists. |
| 4.0 | Invalid Operation | noMemory | 0x4000202A | Not enough memory. |
| 4.0 | Invalid Operation | invalLicense | 0x4000202B | Invalid license. |
| 4.0 | Invalid Operation | invalidDayNightScheduledSwitch | 0x4000202C | NaN |
| 4.0 | Invalid Operation | domePTTranslateToDomeXYError | 0x4000202D | Converting the pan and tilt value of the PTZ channel to the X and Y coordinates of PTZ channel failed. |
| 4.0 | Invalid Operation | domePTTranslateToPanoramaXYError | 0x4000202E | Converting the pan and tilt value of the PTZ channel to the X and Y coordinates of the panoramic channel failed. |
| 4.0 | Invalid Operation | panoramaXYTranslateToDomePTError | 0x4000202F | Converting the X and Y coordinates of panoramic channel to the pan and tilt value of the PTZ channel failed. |
| 4.0 | Invalid Operation | multi-target-typeError | 0x40002030 | Set multi-target-type capture mode of the box camera channel to Face + Human Body + Vehicle. |
| 4.0 | Invalid Operation | deletingFailedTurnOffHTTPSEnhancedSDKWebsocketsFirst | 0x40002031 | Deleting failed. Turn off HTTPS, Enhanced SDK Service and Websockets on Network Service page first. |
| 4.0 | Invalid Operation | deletingFailedTurnOffHTTPSEnhancedSDKFirst | 0x40002032 | Deleting failed. Turn off HTTPS and Enhanced SDK Service on Network Service page first. |
| 4.0 | Invalid Operation | exposureTimeTooBigInModeP | 0x40002033 | In P standard, the exposure time must be less than 1/25 sec and defog function should be disabled. |
| 4.0 | Invalid Operation | exposureTimeTooBigInModeN | 0x40002034 | In N standard, the exposure time must be less than 1/30 sec and defog function should be disabled. |
| 4.0 | Invalid Operation | traceLinkageFail | 0x40002035 | Track linkage failed. Calibrate screen first. |
| 4.0 | Invalid Operation | noClientCertificate | 0x40002036 | Client certificate should be installed. |
| 4.0 | Invalid Operation | noCACertificate | 0x40002037 | CA certificate should be installed. |
| 4.0 | Invalid Operation | authenticationFailed | 0x40002038 | Authenticating certificate failed. Check the certificate. |
| 4.0 | Invalid Operation | clientCertificateExpired | 0x40002039 | Client certificate has expired. |
| 4.0 | Invalid Operation | clientCertificateRevocation | 0x4000203A | Client certificate is revoked. |
| 4.0 | Invalid Operation | CACertificateExpired | 0x4000203B | CA certificate has expired. |
| 4.0 | Invalid Operation | CACertificateRevocation | 0x4000203C | CA certificate is revoked. |
| 4.0 | Invalid Operation | connectFail | 0x4000203D | Connection failed. |
| 4.0 | Invalid Operation | contrastFailed | 0x4000203E | Face picture comparison failed. |
| 4.0 | Invalid Operation | loginNumExceedLimit | 0x4000203F | No more user can log in. |
| 4.0 | Invalid Operation | HDMIResolutionIllegal | 0x40002040 | HDMI video resolution cannot be larger than that of main and sub stream. |
| 4.0 | Invalid Operation | platformParametersInvalid | 0x40002041 | Please configure the platform parameters. |
| 4.0 | Invalid Operation | openFailedCheckHTTPSCertificate | 0x40002042 | Enabling failed. If there is no available certificate, create a certificate on the HTTPS page before enabling the function. If there exists a certificate, delete it on the HTTPS page, create a certificate and then enable the function. |
| 4.0 | Invalid Operation | repeatCroppingError | 0x40002043 | Cropping is enabled. Duplicate cropping is not allowed. |
| 4.0 | Invalid Operation | mainStreamCroppingError | 0x40002044 | Cropping is not supported under the current resolution. Adjust the main stream resolution and try again. |
| 4.0 | Invalid Operation | adjustingResolutionError | 0x40002045 | Disable cropping before adjusting the resolution. |
| 4.0 | Invalid Operation | regionCliped | 0x40002046 | This area is cropped. |
| 4.0 | Invalid Operation | functionInUse | 0x40002047 | The function is in use. Do not disable. |
| 4.0 | Invalid Operation | create2048Certificate | 0x40002048 | The 1024-bit certificate is detected. Please create a 2048-bit certificate and try again. |
| 4.0 | Invalid Operation | hdFormatFail | 0x40002049 | Formatting HDD failed. |
| 4.0 | Invalid Operation | parseCertificateFailed | 0x40002050 | The current certificate cannot be parsed. Create a new certificate and try again. |
| 4.0 | Invalid Operation | unableTwoAutomaticFDLibSameTime | 0x40002051 | Failed to enable two automatic face picture libraries simultaneously. One of them has already been enabled. |
| 4.0 | Invalid Operation | TCPorUDPRequired | 0x40002052 | Enable TCP or UDP to activate the settings. |
| 4.0 | Invalid Operation | TLS1.1orTLS1.2Required | 0x40002053 | Enable TLS 1.1 or TLS 1.2. |
| 4.0 | Invalid Operation | faceSnapMutualExclusionBehavior | 0x40002054 | The functions of face capture and abnormal event detection cannot be used simultaneously. |
| 4.0 | Invalid Operation | modlingMutualExclusionBehavior | 0x40002055 | The abnormal event detection effect will be affected when the device is modeling. |
| 4.0 | Invalid Operation | formattingFailed | 0x40002056 | Formatting failed. Please try again. |
| 4.0 | Invalid Operation | encryptedFormattingFailed | 0x40002057 | Formatting encrypted HDD failed. Please try again. |
| 4.0 | Invalid Operation | wrongPassword | 0x40002058 | Wrong password. Please try again. |
| 4.0 | Invalid Operation | exposureSynchronized | 0x40002059 | Sensors' exposure synchronization is enabled and configuring manual RGB is not allowed. |
| 4.0 | Invalid Operation | certificateNotExist | 0x40002060 | The certificate does not exist. |
| 4.0 | Invalid Operation | certificateIsUsing | 0x40002061 | The certificate is in use. |
| 4.0 | Invalid Operation | NOPriviteKey | 0x40002062 | Private key and certificate mismatched. |
| 4.0 | Invalid Operation | certificatesManagementNotSupport | 0x40002063 | Certificate management is not supported. |
| 4.0 | Invalid Operation | certificateExceptional | 0x40002065 | The selected certificate is abnormal. |
| 4.0 | Invalid Operation | enableVehicleArmingFirst | 0x40002066 | Enable arming first. |
| 4.0 | Invalid Operation | audioIsPlayingPleaseWait | 0x40002067 | Audio is playing...Please wait. |
| 4.0 | Invalid Operation | twoWayAudioInProgressPleaseWait | 0x40002068 | Two-way audio in progress...Please wait. |
| 4.0 | Invalid Operation | calibrationPointNumFull | 0x40002069 | The number of calibration points reached the limit. |
| 4.0 | Invalid Operation | completeTheLevelCalibrationFirst | 0x4000206A | Set level calibration first. |
| 4.0 | Invalid Operation | completeTheRadarCameraCalibrationFirst | 0x4000206B | Set radar-camera calibration first. |
| 4.0 | Invalid Operation | WifiWithoutLink | 0x4000207C | Wi-Fi is not connected. |
| 4.0 | Invalid Operation | mutexWifiCascade | 0x4000208D | It cannot be enabled simultaneously with Wi-Fi cascading function. |
| 4.0 | Invalid Operation | illegalFeatureDetectionAera | 0x4000208E | Drawing failed. Make sure the feature detection area is within the target detection area. |
| 4.0 | Invalid Operation | noFeatureOrTargetDetectionAera | 0x4000208F | Saving failed. Please draw the feature detection area and the target detection area first. |
| 4.0 | Invalid Operation | MaxPassword attempts | 0x40002090 | Attempts exceeded limit. Try again 30 minutes later. |
| 4.0 | Invalid Operation | noDetectionLine | 0x40002091 | Configuration failed. No detection line. |
| 4.0 | Invalid Operation | HBDLibNumOverLimit | 0x40002092 | The number of human body picture libraries reaches the upper limit. |
| 4.0 | Invalid Operation | theShieldRegionError | 0x40002093 | Saving failed. The shielded area should be the ground area where the shielded object is located. |
| 4.0 | Invalid Operation | theDetectionAreaError | 0x40002094 | Saving failed. The detection area should only cover the ground area. |
| 4.0 | Invalid Operation | drawingAreaFailed | 0x40002095 | Drawing area failed. No more areas can be added. |
| 4.0 | Invalid Operation | invalidLaneLine | 0x40002096 | Saving failed. Invalid lane line. |
| 4.0 | Invalid Operation | deviceSleep | 0x40002097 | The device is sleeping. |
| 4.0 | Invalid Operation | configureTheSecurityModeOfWiFiFailed | 0x40002098 | Configuration failed. Please set the security mode of Wi-Fi as WPA2-personal. |
| 4.0 | Invalid Operation | accessDeviceResolutionError | 0x40002099 | Connecting failed. The resolution of device must be 1080p. |
| 4.0 | Invalid Operation | allocatingComputingPowerFailed | 0x4000209A | Allocating GPU failed. Not enough GPU. Please allocate the smart mode of the device again. |
| 4.0 | Invalid Operation | VCAChanResourceMutualExclusive | 0x4000209B | VCA resources of the channel conflict. |
| 4.0 | Invalid Operation | pointsOnStraightLine | 0x4000209C | Calibrating failed. The calibration points cannot be on the same line. |
| 4.0 | Invalid Operation | TValueLessThanOrEqualZero | 0x4000209D | Calibrating failed. The T value of the calibration points should be larger than 0. |
| 4.0 | Invalid Operation | channel1CfgError | 0x4000209E | Configuring failed. Configure channel 1 as face, vehicle, or neither of them before configuring channel 2. |
| 4.0 | Invalid Operation | notSupportVehiclesAlone | 0x4000209F | Configuring failed. The device does not support selecting vehicle separately. |
| 4.0 | Invalid Operation | paramCfgTimeOut | 0x400020A0 | Configuring parameters timed out. Refresh and try again. |
| 4.0 | Invalid Operation | accessDeviceError | 0x400020A1 | Connecting to device failed. Make sure the device meets the following requirements: the resolution is 1080p; the encoding type is H264 or H265; the frame rate is larger than 12.5 fps. |
| 4.0 | Invalid Operation | enableITSFunctionOfThisChannelFirst | 0x400020A2 | Enable ITS function of this channel first. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalUp | 0x400020A3 | Calibration completed. The device deviates xx° up from the horizontal plane. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalDown | 0x400020A4 | Calibration completed. The device deviates xx° down from the horizontal plane. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalUpSuggestAdjustInstallation | 0x400020A5 | Calibration completed. The device deviates xx° up from the horizontal plane. The deviation is a bit large. It is recommended to adjust the installation angle. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalDownSuggestAdjustInstallation | 0x400020A6 | Calibration completed. The device deviates xx° down from the horizontal plane. The deviation is a bit large. It is recommended to adjust the installation angle. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalUpMustAdjustInstallation | 0x400020A7 | Calibration completed. The device deviates xx° up from the horizontal plane. The deviation is large and will seriously affect the distance and area of the radar detection. Please adjust the installation angle. |
| 4.0 | Invalid Operation | radarCalibrationHorizontalDownMustAdjustInstallation | 0x400020A8 | Calibration completed. The device deviates xx° down from the horizontal plane. The deviation is large and will seriously affect the distance and area of the radar detection. Please adjust the installation. |
| 4.0 | Invalid Operation | faceRadarCenterArea | 0x400020A9 | Camera should face at the center of the radar detection area. |
| 4.0 | Invalid Operation | calibrationPointsError | 0x400020B0 | Calibration failed. Calibration points with the same serial number should be at the same reference position and ensure the calibration parameters of rule configuration is accurate. |
| 4.0 | Invalid Operation | verifyingCalibrationFailed | 0x400020B1 | Calibration verification failed. Calibrate first. |
| 4.0 | Invalid Operation | startAppFail | 0x400020B2 | Running the application failed. |
| 4.0 | Invalid Operation | yuvconflict | 0x400020B3 | The raw video stream conflicts. |
| 4.0 | Invalid Operation | overMaxAppNum | 0x400020B4 | The number of applications exceeded the limit. |
| 4.0 | Invalid Operation | noFlash | 0x400020B5 | Not enough flash. |
| 4.0 | Invalid Operation | platMismatch | 0x400020B6 | Platform mismatch. |
| 4.0 | Invalid Operation | sendChanCodecErrStartConfFaild | 0x400020BF | Initiating meeting failed. Please adjust sending channel parameters on Video Settings page, and try again. |
| 4.0 | Invalid Operation | allIndividualsSupportOne | 0x400020C0 | Only supports 2-ch Group Behavior or 1-ch Individual Behavior. 1-ch Group Behavior and 1-ch Individual Behavior are not supported. |
| 4.0 | Invalid Operation | confCodeParamOnlySupportSub | 0x400020C1 | Main stream parameters for the sending channel are display on this page. If you need to adjust sub-stream and third stream parameters, go to the Video Settings page. |
| 4.0 | Invalid Operation | confCodeEncodeEerr | 0x400020C2 | Verifying interactive encoding parameters failed. |
| 4.0 | Invalid Operation | confCodeParamOnlySupportMain | 0x400020C3 | Configuration failed. When Sending Channel Encoding Settings is enabled, only main stream can be selected for the sending channel. |
| 4.0 | Invalid Operation | plsConfimClassroomIsConf | 0x400020C4 | Operation failed. Please check whether the classroom is under interaction. |
| 4.0 | Invalid Operation | noCloudStorageServer | 0x400020C5 | Cloud storage server is not configured. |
| 4.0 | Invalid Operation | AlgorithmIDIsNotMatchT4 | 0x400020C6 | NaN |
| 4.0 | Invalid Operation | NotHaveDFRAlgorithmMatchT4 | 0x400020C7 | NaN |
| 4.0 | Invalid Operation | noDisk | 0x400020C8 | No HDD. |
| 4.0 | Invalid Operation | diskError | 0x400020C9 | HDD error. |
| 4.0 | Invalid Operation | duplicateTaskID | 0x400020CA | Duplicate task ID. |
| 4.0 | Invalid Operation | PIDNumLimitedError | 0x400020CB | Number of picture ID exceeded limit. |
| 4.0 | Invalid Operation | NotHaveFDAlgorithmMatchT4 | 0x400020CC | No related FD algorithm of the T4 card. |
| 4.0 | Invalid Operation | NotHaveDFRAndFDAlgorithmMatchT4 | 0x400020CD | No related DFR and FD algorithm of the T4 card. |
| 4.0 | Invalid Operation | TaskStatusSearchFail | 0x400020CE | Searching task status failed. |
| 4.0 | Invalid Operation | DFRAndFDPreAllocatedExceptT4 | 0x400020CF | Other cards have been pre-allocated with DFR and FD algorithm when enabling 300 W. |
| 4.0 | Invalid Operation | OpenChipModeNotAllowClearDFRResource | 0x400020D0 | Clearing DFR resource is not allowed when enabling the specified chip function. |
| 4.0 | Invalid Operation | getFingerInfoFail | 0x400020D1 | Getting fingerprint failed. |
| 4.0 | Invalid Operation | setUpLicenseFail | 0x400020D2 | Setting license failed. |
| 4.0 | Invalid Operation | setUpLicenseAlready | 0x400020D3 | License imported. |
| 4.0 | Invalid Operation | productIdNotMatched | 0x400020D4 | Product ID mismatch. |
| 4.0 | Invalid Operation | haveTrailLicense | 0x400020D5 | Trial license imported. |
| 4.0 | Invalid Operation | AIRuleConfigurationNotValid | 0x400020F0 | AI rule configuration does not take effect. |
| 4.0 | Invalid Operation | ManualCountStarted | 0x400020F1 | Manual counting has started. |
| 4.0 | Invalid Operation | ManualCountNotStarted | 0x400020F2 | Manual counting has not started. |
| 4.0 | Invalid Operation | NotSupportWithVideoTask | 0x400020F3 | SMD is not supported. Video structuralization has already been enabled in the channel. |
| 4.0 | Invalid Operation | faceLibDiskFull | 0x400020F4 | Face picture library storage media is full. |
| 4.0 | Invalid Operation | gaitRuleIlleage | 0x400020F5 | Supports up to 1 detection frame and 8  shielded frames. |
| 4.0 | Invalid Operation | vehicleOrHumanPicDetectFailed | 0x400020F6 | Human body or vehicle picture detection failed. |
| 4.0 | Invalid Operation | vedioPreviewFailed | 0x400020F7 | Live view failed. |
| 4.0 | Invalid Operation | needSameDeviceAsStandby | 0x400020F8 | The same main and spare node is required to create main and spare cluster. |
| 4.0 | Invalid Operation | cannotModifiedToSmallFDlibConfig | 0x400020F9 | Editing to small capacity configuration failed. Large capacity is in use. |
| 4.0 | Invalid Operation | hostnameError | 0x400020FA | Node host name exception. |
| 4.0 | Invalid Operation | IPandGatewayNotInTheSameNetworkSegment | 0x400020FB | The IP address and the gateway should be in the same network segment. |
| 4.0 | Invalid Operation | ModifiedIpCannotBeDuplicate | 0x400020FC | Duplicate IP address. |
| 4.0 | Invalid Operation | faceLibraryIDNotExis | 0x400020FD | Face picture library does not exist. |
| 4.0 | Invalid Operation | notFindFaceAnalysisAlgorithm | 0x400020FE | No face picture analysis algorithm is found. |
| 4.0 | Invalid Operation | notSupportSmallerRatios | 0x400020FF | Function configuration is not supported when the ratio is less than 1. Please increase the ratio. |
| 4.0 | Invalid Operation | currentRatiosSettingInvalid | 0x40002100 | The iris and shutter related parameters you have set will only take effect when the ratio is no less than 1. |
| 4.0 | Invalid Operation | NeedTurnDownWatchList | 0x40002101 | Library capacity should be lowered. |
| 4.0 | Invalid Operation | HasAllocateHMS | 0x40002102 | Clear the pre-allocated structural algorithm of persons and vehicles. |
| 4.0 | Invalid Operation | DownloadLogFileFail | 0x40002103 | Downloading failed. Log file is too large. Please download in the back end. |
| 4.0 | Invalid Operation | ruleAreaExceedLimit | 0x40002104 | Out of the rule region. Please draw in the largest detection area. |
| 4.0 | Invalid Operation | dehazeMutexWDR | 0x40002105 | Please disable the defog function  in Day/Night Switch mode. |
| 4.0 | Invalid Operation | incorrectConsolePassword | 0x40002106 | Saving failed. Incorrect console password. |
| 4.0 | Invalid Operation | targetMutexesBetweenChannels | 0x40002107 | Saving failed. Targets selected from the channel 1 and channel 2 conflict. Please select again. |
| 4.0 | Invalid Operation | invalidPTZControl | 0x40002108 | Calibrating... The calibration will not affect PTZ control of panoramic channels. |
| 4.0 | Invalid Operation | abnormalInternalParameterList | 0x40002109 | Updating internal parameters list failed. Exception occurred when checking the existing internal parameters list. |
| 4.0 | Invalid Operation | MutexWithInternalParameterCorrection | 0x40002110 | Enabling internal parameters correction failed. Disable abnormal event detection first. |
| 4.0 | Invalid Operation | resetRulesOrExternalParameters | 0x40002111 | Smart event cannot be enabled. Configure the device rule and external parameters again. |
| 4.0 | Invalid Operation | completerulesAndExternalParametersFirst | 0x40002112 | Smart event cannot be enabled. Configure the device rule and external parameters first. |
| 4.0 | Invalid Operation | invalidMultiLensCalibration | 0x40002113 | Enabling multi-lens dewarping failed. Make sure all the channels of the device has enabled VCA. |
| 4.0 | Invalid Operation | invalidScheduleRecordAndCapture | 0x40002114 | This function cannot be enabled simultaneously with recording schedules, timed capture, and event capture. Go to Storage-Schedule Settings to disable  recording schedules, timed capture, and event capture. |
| 4.0 | Invalid Operation | invalidProRecordAndCapture | 0x40002115 | This function cannot be enabled simultaneously with Pro Record & Capture. Go to System → System Settings to disable Pro Record & Capture first. |
| 4.0 | Invalid Operation | invalidMemoryCardOrNAS | 0x40002116 | Searching failed. Please insert the memory card or load NAS. |
| 4.0 | Invalid Operation | invalidMemoryStatusOrCaptureSchedule | 0x40002117 | Searching failed. Check if the memory status is normal and the capture schedule is configured. |
| 4.0 | Invalid Operation | invalidMemoryStatusOrRecordSchedule | 0x40002118 | Searching failed. Check if the memory status is normal and the recording schedule is configured. |
| 4.0 | Invalid Operation | invalidMemoryCard | 0x40002119 | Formatting failed. Try again or change the memory card. |
| 4.0 | Invalid Operation | replaceMemoryCard | 0x4000211A | Change memory card in time for normal use. |
| 4.0 | Invalid Operation | invalidMaxMinSize | 0x4000211B | Saving failed. Check if the largest size is larger than the smallest size. |
| 4.0 | Invalid Operation | notCoverLaneLine | 0x4000211C | It is recommended that the lane line and the actual lane line should overlap. |
| 4.0 | Invalid Operation | errorUpgradeVersion | 0x4000211D | Upgrading failed. The version of the upgrade file is too low. |
| 4.0 | Invalid Operation | limitPreviewNumber | 0x4000211E | Live view failed. Number of live view exceeded limit. |
| 4.0 | Invalid Operation | invalidImageFormat | 0x4000211F | Importing failed. The picture format should be JPG or JPEG. |
| 4.0 | Invalid Operation | imageGreaterThan300KB | 0x40002120 | Importing failed. The picture size should be less than 300 KB. |
| 4.0 | Invalid Operation | wrongAlarmInputID | 0x40002121 | Incorrect alarm input encoding ID. |
| 4.0 | Invalid Operation | wrongVideoChannelID | 0x40002122 | Incorrect video channel encoding ID. |
| 4.0 | Invalid Operation | wrongAudioOutputChannelID | 0x40002123 | Incorrect audio output channel encoding ID. |
| 4.0 | Invalid Operation | failRegisterCheckNetwork | 0x40002124 | Registering failed, error code: s%. Please check network configuration or contact Hikvision technical support. |
| 4.0 | Invalid Operation | failRegisterCheckDNS | 0x40002125 | Registering failed, error code: s%. Please check network configuration such as DNS or contact  Hikvision technical support. |
| 4.0 | Invalid Operation | intelligenceWithInternalParameterCorrection | 0x40002126 | Correcting internal parameters failed. Disable smart function first. |
| 4.0 | Invalid Operation | trackingIntervalError | 0x40002127 | Setting failed. Waiting to lower tracking speed if low validity should be shorter than waiting to stop tracking if low validity. |
| 4.0 | Invalid Operation | audioNameExisted | 0x40002129 | Uploading failed. Duplicate audio name. |
| 4.0 | Invalid Operation | wrongDetectionLine | 0x40002130 | Draw detection line again. Make sure detection line is within target detection area. |
| 4.0 | Invalid Operation | FRPPortMappingFailed | 0x40002131 | Enable the function of related port before using FRP port mapping. |
| 4.0 | Invalid Operation | noDetectionScenes | 0x40002132 | Set detection scene first. |
| 4.0 | Invalid Operation | noArmingSchedule | 0x40002133 | Set arming schedule first. |
| NaN | NaN | NaN | NaN | NaN |
| 4.0 | Invalid Operation | loginNumLimit | 0x40002135 | Number of users attempting to log in exceeded limit. |
| 4.0 | Invalid Operation | faceLibInitializing | 0x40002136 | Initializing face picture library… Please wait. |
| 4.0 | Invalid Operation | 4GCollectionModuleUpgrading | 0x40002137 | 4G information collection module is upgrading... |
| 4.0 | Invalid Operation | 4GCollectionModuleRestarting | 0x40002138 | 4G information collection module is rebooting... |
| 4.0 | Invalid Operation | 4GCollectionModuleException | 0x40002139 | 4G information collection module exception. |
| 4.0 | Invalid Operation | cannotModifyIPSegment | 0x4000213A | Configuration is not allowed in this network segment. Try again. |
| 4.0 | Invalid Operation | noPreviousLevel | 0x4000213B | Configure the lower level first. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithTheVCA | 0x40004000 | Forklift filtering and smart analysis cannot be enabled simultaneously. Disable smart analysis and try again. |
| 4.0 | Invalid Operation | VCAConflictsWithTheForkliftFilter | 0x40004001 | Smart analysis and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithTheFireSourceDetection | 0x40004002 | Forklift detection and fire and smoke detection cannot be enabled simultaneously. Disable fire and smoke detection and try again. |
| 4.0 | Invalid Operation | fireSourceDetectionConflictsWiththeForkliftFilter | 0x40004003 | Fire and smoke detection and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithTheAIOP | 0x40004004 | Forklift filtering and AI platform cannot be enabled simultaneously. Disable AI platform and try again. |
| 4.0 | Invalid Operation | AIOPConflictsWithTheForkliftFilter | 0x40004005 | AI platform and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithShipDetection | 0x40004006 | Forklift detection and ship detection cannot be enabled simultaneously. Disable ship detection and try again. |
| 4.0 | Invalid Operation | shipDetectionConflictsWithForkliftFilter | 0x40004007 | Ship detection and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithWasteGasDetection | 0x40004008 | Forklift detection and waste gas detection cannot be enabled simultaneously. Disable fire and smoke detection and try again. |
| 4.0 | Invalid Operation | wasteGasDetectionConflictsWithForkliftFilter | 0x40004009 | Waste gas detection and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | forkliftFilterConflictsWithVehicleDetection | 0x4000400A | Forklift detection and vehicle detection cannot be enabled simultaneously. Disable vehicle detection and try again. |
| 4.0 | Invalid Operation | vehicleDetectionConflictsWithForkliftFilter | 0x4000400B | Vehicle detection and forklift filtering under the temperature screening function cannot be enabled simultaneously. Disable forklift filtering and try again. |
| 4.0 | Invalid Operation | sunReflectionBlurFailedWithFusionCalibration | 0x4000400C | Enabling sunshine reflection filtering failed. Contact technical personnel to conduct visual and thermal image fusion calibration. |
| 4.0 | Invalid Operation | sameNameMaterialUploading | 0x40005001 | Uploading materials with duplicate name... |
| 4.0 | Invalid Operation | deleteMaterialDatabaseError | 0x40005002 | Deleting material database records failed. |
| 4.0 | Invalid Operation | scheduleReleaseNoOperate | 0x40005003 | Applying schedule... The schedule cannot be edited or deleted. |
| 4.0 | Invalid Operation | scheduleReleaseNoOperateProgram | 0x40005004 | Applying schedule... Programs in the schedule cannot be edited or deleted. |
| 4.0 | Invalid Operation | scheduleReleaseNoOperateMaterial | 0x40005005 | Applying schedule... Materials in the schedule cannot be edited or deleted. |
| 4.0 | Invalid Operation | writeDiskScheduleDataFail | 0x40005006 | Writing schedule data to HDD failed. |
| 4.0 | Invalid Operation | readScheduleProgramFail | 0x40005007 | Reading programs in schedule failed. |
| 4.0 | Invalid Operation | readScheduleMaaterialFail | 0x40005008 | Reading materials in schedule failed. |
| 4.0 | Invalid Operation | someScheduleNoPermission | 0x40005009 | Not all schedules can be deleted or edited. |
| 4.0 | Invalid Operation | orgNoScheduleTerminal | 0x4000500A | No terminal in the organization is available for applying schedule. |
| 4.0 | Invalid Operation | scheduleMaxProgram | 0x4000500B | No more programs can be added in schedule. |
| 4.0 | Invalid Operation | scheduleNotApproveProgram | 0x4000500C | Programs in schedule are not approved. |
| 4.0 | Invalid Operation | maxAudioNum | 0x4000500D | No more audios can be opened in window. |
| 4.0 | Invalid Operation | programIsInsertRelease | 0x4000500E | Editing failed. Program cutting in or releasing... |
| 4.0 | Invalid Operation | orgWriteDatabaseFail | 0x4000500F | Organization writing to database failed. |
| 4.0 | Invalid Operation | orgReadDatabaseFail | 0x40005010 | Organization reading from database failed. |
| 4.0 | Invalid Operation | dataBackuping | 0x40005011 | Device is backing up data... |
| 4.0 | Invalid Operation | dataTransfering | 0x40005012 | Device is migrating data... |
| 4.0 | Invalid Operation | dataBackRestoring | 0x40005013 | Device is recovering data... |
| 4.0 | Invalid Operation | hdNotFormat | 0x40005014 | HDD not formatted. |
| 4.0 | Invalid Operation | hdFormatting | 0x40005015 | Formatting HDD... |
| 4.0 | Invalid Operation | backHdNotExist | 0x40005016 | Backup disk does not exist. |
| 4.0 | Invalid Operation | dataTransferRestoring | 0x40005017 | Device is migrating and recovering data. |
| 4.0 | Invalid Operation | dataBackError | 0x40005018 | Backing up data failed. |
| 4.0 | Invalid Operation | dataBaseBackError | 0x40005019 | Backing up database failed. |
| 4.0 | Invalid Operation | dataTransferError | 0x4000501A | Mitigating data failed. |
| 4.0 | Invalid Operation | dataBaseTransferError | 0x4000501B | Mitigating database failed. |
| 4.0 | Invalid Operation | maxProgramRepMaterialNum | 0x4000501C | Number of duplicate materials in program exceeded limit. |
| 4.0 | Invalid Operation | maxProgramMaterialNum | 0x4000501D | Number of unduplicate materials in program exceeded limit. |
| 4.0 | Invalid Operation | mainBordNotBackup | 0x4000501F | Conventional disk (main disk) in the first slot cannot be set as backup disk. |
| 4.0 | Invalid Operation | oneNormalHdOnly | 0x40005020 | At least one conventional disk exists when setting backup disk. |
| 4.0 | Invalid Operation | hdIsFull | 0x40005022 | HDD is full. |
| 4.0 | Invalid Operation | noApprovedNotExport | 0x40005023 | Exporting is not allowed without review. |
| 4.0 | Invalid Operation | ZeroDecodeChannel | 0x40005024 | No free decoding channel. |
| 4.0 | Invalid Operation | TX1AnalyzingNotChangeType | 0x40005025 | Changing analysis type is not allowed. TX1 channel is analyzing. |
| 4.0 | Invalid Operation | IPCSmartRuleNoDetectionFrame | 0x40005026 | No detection bezel is configured to the smart rule of current network camera channel. |
| 4.0 | Invalid Operation | maxDiffMaterialNumInProgram | 0x40005027 | Number of different materials in a program exceeded limit. |
| 4.0 | Invalid Operation | IPCStreamFormatError | 0x40005028 | Incorrect stream format of network camera. |
| 4.0 | Invalid Operation | IPCOverResolution | 0x40005029 | Resolution of network camera too high. |
| 4.0 | Invalid Operation | IPCNotOnline | 0x4000502A | Network camera offline. |
| 4.0 | Invalid Operation | IPCOverFrame | 0x4000502B | Frame rate of network camera stream too high. |
| 4.0 | Invalid Operation | streamLinkFull | 0x4000502C | Device stream link is full. |
| 4.0 | Invalid Operation | engineError | 0x4000502D | Engine exception. |
| 4.0 | Invalid Operation | noResource | 0x4000502E | Resource is empty. |
| 4.0 | Invalid Operation | TX1Error | 0x4000502F | TX1 exception. |
| 4.0 | Invalid Operation | packetCapturing | 0x40005030 | Device capturing packet... |
| 4.0 | Invalid Operation | soundAudioUsing | 0x40005031 | Voice activated and audio mixing cannot be enabled simultaneously. |
| 4.0 | Invalid Operation | inConferenceNotModeTime | 0x40005032 | Editing time is not allowed. Appointment or meeting in progress. |
| 4.0 | Invalid Operation | noCaptureFile | 0x40005033 | No captured packet file. |
| 4.0 | Invalid Operation | loopLayoutError | 0x40005034 | Switching layout is not supported by single channel polling. |
| 4.0 | Invalid Operation | userNotModInConference | 0x40005035 | Editing or deleting is not allowed. Appointment or meeting in progress. |
| 4.0 | Invalid Operation | recvCardNotOnline | 0x40005036 | Receiving card is offline. |
| 4.0 | Invalid Operation | noSelfDefineBmp | 0x40005037 | No customized background picture. |
| 4.0 | Invalid Operation | lampSaveError | 0x40005038 | Saving lightboard parameters failed. |
| 4.0 | Invalid Operation | lampReadError | 0x40005039 | Reading lightboard information failed. |
| 4.0 | Invalid Operation | 3dNotOsdError | 0x4000503A | Enabling OSD failed. 3D function has been enabled. |
| 4.0 | Invalid Operation | positionHintOn | 0x4000503B | Screen position prompt is enabled. |
| 4.0 | Invalid Operation | invalidSceneID | 0x4000503C | Invalid scene ID. |
| 4.0 | Invalid Operation | sceneNumFull | 0x4000503D | Number of scenes exceeded limit. |
| 4.0 | Invalid Operation | sceneNameRepeated | 0x4000503E | Duplicate scene name. |
| 4.0 | Invalid Operation | differRecvCardTypeNotSwitchScreen | 0x4000503F | Screens of different boards are not allowed to switch. |
| 4.0 | Invalid Operation | VideoPlayingCannot3D | 0x40005040 | 3D is not allowed when video window is open. |
| 4.0 | Invalid Operation | inputTextEmpty | 0x40005041 | Text is empty. |
| 4.0 | Invalid Operation | devNotSupportSave | 0x40005042 | Device does not support storage. |
| 4.0 | Invalid Operation | notInitColorStandard | 0x40005043 | Color gamut is not initialized. |
| 4.0 | Invalid Operation | colorStandardNotEnabled | 0x40005044 | Color gamut switch is not enabled. |
| 4.0 | Invalid Operation | screenPosHintCannotOpenWindow | 0x40005045 | Opening video window is not supported when screen position prompt is opened. |
| 4.0 | Invalid Operation | 3DModeCannotOpenWindow | 0x40005046 | Opening video window is not supported in 3D mode. |
| 4.0 | Invalid Operation | imageRevolveCannotOpenWindow | 0x40005047 | Opening video window is not supported in image rotation mode. |
| 4.0 | Invalid Operation | dynamicTitleCannotOpenWindow | 0x40005048 | Opening video window is not supported when dynamic message opened. |
| 4.0 | Invalid Operation | maxWallResolution | 0x40005049 | Video wall resolution exceeded limit. |
| 4.0 | Invalid Operation | tooSmallMiddleSignalArea | 0x4000504A | The middle signal source area is too small. |
| 4.0 | Invalid Operation | initDivideImageFailed | 0x4000504B | Initializing divided window image failed. |
| 4.0 | Invalid Operation | max3DDisplayWidth | 0x4000504C | 3D display width exceeded limit. |
| 4.0 | Invalid Operation | intelligentAnalysisIPCCannotOperate | 0x4000504D | Operation failed. Network camera is conducting smart analysis. |
| 4.0 | Invalid Operation | loopGroupAnalyzingCannotOperate | 0x4000504E | Operation failed. Current polling group is executing analysis task. |
| 4.0 | Invalid Operation | notPTZControlBySIP | 0x4000504F | Controlling peer port speed dome is not allowed in SIP protocol. |
| 4.0 | Invalid Operation | cannotAddSelfTerminal | 0x40005050 | Adding the terminal itself is not allowed. |
| 4.0 | Invalid Operation | requestTerminalIsSpeaking | 0x40005051 | The request terminal is in speaking status. |
| 4.0 | Invalid Operation | meetingCannotModifyChairmanByBasicInfo | 0x40005052 | Editing host in basic information is not allowed when in meeting. |
| 4.0 | Invalid Operation | noChairmanNoCheckroll | 0x40005053 | Roll call is not supported by non-host terminals. |
| 4.0 | Invalid Operation | rtspNotSupportMediaLoop | 0x40005054 | Audio and video loop are not supported by RTSP terminal. |
| 4.0 | Invalid Operation | defineViewNotSupportRTSP | 0x40005055 | Watching is not supported by RTSP terminal. |
| 4.0 | Invalid Operation | displayOnlyBroadcastMT | 0x40005056 | Enabling presentation by non-speakers is not allowed when in speaker mode. |
| 4.0 | Invalid Operation | forbiddenBySoundIntensity | 0x40005057 | Enabling voice activated... The operation is not allowed. |
| 4.0 | Invalid Operation | beSelectedNotSupportRTSPIn | 0x40005058 | Watching is not allowed when RTSP terminal is calling MCU. |
| 4.0 | Invalid Operation | repeatTerminalInfo | 0x40005059 | Duplicate terminal information. |
| 4.0 | Invalid Operation | addonlydeletemtfinished | 0x4000505A | Invitation is not allowed. Removing terminal is uncompleted. |
| 4.0 | Invalid Operation | forbiddenByForceBroadcast | 0x4000505B | Force broadcast activated... The operation is not allowed. |
| 4.0 | Invalid Operation | maxLoopChanWinNum | 0x4000505C | Number of single channel polling windows exceeded limit. |
| 4.0 | Invalid Operation | tooManyMixAudioNumtoAuto | 0x4000505D | Number of mixing audio parties reached limit. Enabling smart audio mixing failed. |
| 4.0 | Invalid Operation | terminalResourceFull | 0x4000505E | Not enough meeting terminal resource. |
| 4.0 | Invalid Operation | resourceExceptionToWait | 0x4000505F | Resource exception. Please wait… |
| 4.0 | Invalid Operation | forbiddenByChairMode | 0x40005060 | Current operation is not allowed in host meeting. |
| 4.0 | Invalid Operation | forbiddenedByPollRollSelect | 0x40005061 | Applying for hosting is not allowed when watching conference polling calling. |
| 4.0 | Invalid Operation | thitherNotMatchLocalVideo | 0x40005062 | Peer video type and local supported video type mismatch. |
| 4.0 | Invalid Operation | thitherNotMatchLocalAudio | 0x40005063 | Peer audio type and local supported audio type mismatch. |
| 4.0 | Invalid Operation | broadcastNotDefineSelfView | 0x40005064 | Configuring terminal image composition is not allowed in force broadcast. |
| 4.0 | Invalid Operation | videoLoopNotDefineSelfView | 0x40005065 | Configuring terminal image composition is not allowed in video loop. |
| 4.0 | Invalid Operation | sameVideoSrc | 0x40005066 | The same video source cannot be set. |
| 4.0 | Invalid Operation | maxMcuNum | 0x40005067 | Number of MCU reached limit. |
| 4.0 | Invalid Operation | sameMcuName | 0x40005068 | MCU name already exists. |
| 4.0 | Invalid Operation | mcuAlreadyExist | 0x40005069 | MCU already exists. |
| 4.0 | Invalid Operation | dualStreamLocked | 0x4000506A | Presentation is locked. |
| 4.0 | Invalid Operation | sipTerminalNodualStream | 0x4000506B | Dual stream cannot be enabled in SIP terminal. |
| 4.0 | Invalid Operation | broadcastSoundNotSame | 0x4000506C | Broadcast and voice activated cannot be enabled at the same time. |
| 4.0 | Invalid Operation | meetingInProgress | 0x4000506D | Meeting in progress. |
| 4.0 | Invalid Operation | notIPCallWhenGKLink | 0x4000506E | Calling IP address is not supported when connecting to GK server (only domain name calling allowed: point to point, join meeting, and create meeting). |
| 4.0 | Invalid Operation | oneSignalToMaxOutput | 0x4000506F | No more single input sources can be exported to output interface. |
| 4.0 | Invalid Operation | noTerminalInDemoMode | 0x40005070 | No terminal in presentation status. |
| 4.0 | Invalid Operation | noChairmanNoSelectView | 0x40005071 | Only host endpoint can watch other endpoints. |
| 4.0 | Invalid Operation | notAllowClearOrCutChairman | 0x40005072 | Removing or hanging up host terminal is not allowed. |
| 4.0 | Invalid Operation | noLayoutNoSoundIntensityPriority | 0x40005073 | Enabling voice activated failed. Composing meeting is not enabled. |
| 4.0 | Invalid Operation | layoutAutoNotSoundIntensityPriority | 0x40005074 | Enabling voice activated failed. Composing meeting is not customized. |
| 4.0 | Invalid Operation | conferenceTimeCannotOver24Hour | 0x40005075 | Duration cannot be greater than 24 hours. |
| 4.0 | Invalid Operation | createAudioMatrixFailed | 0x40005076 | Creating audio matrix failed. |
| 4.0 | Invalid Operation | oneVirtualLEDAreaBindOneAudioArea | 0x40005077 | A virtual LED area can be linked to an audio area only. |
| 4.0 | Invalid Operation | batchLoopNoSoundIntensityPriority | 0x40005078 | Voice activated is not supported when batch polling is enabled. |
| 4.0 | Invalid Operation | forceBroadcastFirst | 0x40005079 | Enabling speaker is required to enable force broadcast. |
| 4.0 | Invalid Operation | broadcastNotDefineView | 0x4000507A | Watching is not allowed when force broadcast is enabled. |
| 4.0 | Invalid Operation | broadcastNotAVLoop | 0x4000507B | Audio and video loop is not allowed when force broadcast is enabled. |
| 4.0 | Invalid Operation | maxPublicTemplateNum | 0x4000507C | Number of public conference templates exceeded limit. |
| 4.0 | Invalid Operation | layoutErrorInSoundIntensity | 0x4000507D | Changing layout is not allowed when voice activated is enabled. |
| 4.0 | Invalid Operation | audioVideoLoopNotSupport | 0x4000507E | Current operation is not allowed in audio and video loop. |
| 4.0 | Invalid Operation | rtspNotSupportSelfViewCompose | 0x4000507F | Auto image composition is not supported by RTSP terminal. |
| 4.0 | Invalid Operation | layoutCannotAutoInSoundIntensity | 0x40005080 | Changing layout to auto composition is not allowed when voice activated is enabled. |
| 4.0 | Invalid Operation | noViewComposeNotSupportPreMonitor | 0x40005081 | Displaying capture on client is not supported without image composition. |
| 4.0 | Invalid Operation | viewShieldNotSupportPreMonitor | 0x40005082 | Displaying capture on client is not supported by hiding image. |
| 4.0 | Invalid Operation | noConferenceNotSupportPreMonitor | 0x40005083 | Cannot display capture on client when terminal is not in the conference. |
| 4.0 | Invalid Operation | layoutCannotLoopInSoundIntensity | 0x40005084 | Batch polling is not allowed when voice activated is enabled. |
| 4.0 | Invalid Operation | notRegisterGKServerUseHostnameCall | 0x40005085 | Calling domain name is applied when GK is not registered. |
| 4.0 | Invalid Operation | startTimeCannotSetPassTime | 0x40005086 | Start time cannot be past time. |
| 4.0 | Invalid Operation | conferenceTimeCannotUnder10Minute | 0x40005087 | Meeting duration should be at least 10 minutes. |
| 4.0 | Invalid Operation | timeConflictInOrderConference | 0x40005088 | Reserved meeting time conflict. |
| 4.0 | Invalid Operation | orderConferenceTimeConflictToCurrent | 0x40005089 | Reserved meeting time and current meeting time conflict. |
| 4.0 | Invalid Operation | autoComposeForbiddenSoundIntensity | 0x4000508A | When image composition mode is auto, enabling voice activated is not allowed. |
| 4.0 | Invalid Operation | notAllowJoinConferenceByHostname | 0x4000508B | Joining meeting by domain name is not allowed. |
| 4.0 | Invalid Operation | mucConferenceNotSptSipTerminal | 0x4000508C | SIP protocol terminal is not supported in MCU meeting. |
| 4.0 | Invalid Operation | unRegGKCannotAddHostnameTerminal | 0x4000508D | Adding terminal with domain name as address type is not allowed when GK is not registered. |
| 4.0 | Invalid Operation | notSupportSynIPCByUrladdition | 0x4000508E | Network camera added by syncing URL method is not supported. |
| 4.0 | Invalid Operation | portConferenceMaxPreview | 0x4000508F | Number of port conference live view exceeded limit. |
| 4.0 | Invalid Operation | failedToOperateNoDisturbingConference | 0x40005090 | Operation failed. Conference is in Do Not Disturb mode. |
| 4.0 | Invalid Operation | sipRegisteredNeedMCUHostName | 0x40005091 | Device has been registered to SIP server, and needs to be linked to meeting creation server with domain name format. |
| 4.0 | Invalid Operation | sipNotRegisteredNeedMCUIP | 0x40005092 | Device has not been registered to SIP server, and needs to be linked to meeting creation server with IP format server. |
| 4.0 | Invalid Operation | maxVirtualLedNum | 0x40005093 | Number of virtual LEDs supported by device is limited. |
| 4.0 | Invalid Operation | maxVirtualLedNumInWall | 0x40005094 | Number of virtual LEDs supported by a single video wall is limited. |
| 4.0 | Invalid Operation | alarmLinkageNumLimited | 0x40005095 | Number of alarm linkage parameter structure is limited. |
| 4.0 | Invalid Operation | notSupportSynIPCByUrladdition | 0x40005096 | Network camera added by syncing URL method is not supported. |
| 4.0 | Invalid Operation | bandTestErrorByWirelessLinkLoss | 0x40005097 | Bandwidth test failed. Wireless network disconnected. |
| 4.0 | Invalid Operation | bandTestErrorByWirelessLinkAbnormal | 0x40005098 | Bandwidth test failed. Wireless network connection exception. |
| 4.0 | Invalid Operation | loopCannotOpenCheckroll | 0x40005099 | Roll call polling is not allowed when conference polling is enabled. |
| 4.0 | Invalid Operation | loopCannotOpenBeforeCancelSpokensman | 0x4000509a | Cancel speaker before enabling roll call polling. |
| 4.0 | Invalid Operation | createConferenceServerLoss | 0x4000509b | Connecting to meeting creation server failed. |
| 4.0 | Invalid Operation | createConferenceSeverNotConfig | 0x4000509c | Meeting creation server is not configured. |
| 4.0 | Invalid Operation | createConferenceServerRejectTerminal | 0x4000509d | Terminal is rejected to join meeting by meeting creation server. |
| 4.0 | Invalid Operation | cannotCheckTimeWhenTerminalOnline | 0x4000509e | Time syncing is not allowed when terminal is online. |
| 4.0 | Invalid Operation | invalidAggrgroup | 0x4000509f | Invalid aggregation group. |
| 4.0 | Invalid Operation | invalidAggrgroupPort | 0x400050a0 | Invalid port was added to aggregation group. |
| 4.0 | Invalid Operation | invalidAggrgroupMode | 0x400050a1 | Invalid load balancing mode. |
| 4.0 | Invalid Operation | limitAggrgroupMember | 0x400050a2 | Number of members in aggregation group exceeded limit. |
| 4.0 | Invalid Operation | limitAggrgroupNum | 0x400050a3 | Aggregation group exceeded limit. |
| 4.0 | Invalid Operation | setAggrgroupModeFailed | 0x400050a4 | Setting load balancing mode failed. |
| 4.0 | Invalid Operation | delAggrgroupFailed | 0x400050a5 | Deleting aggregation group failed. |
| 4.0 | Invalid Operation | addAggrgroupFailed | 0x400050a6 | Creating aggregation group failed. |
| 4.0 | Invalid Operation | hasAggrgroupCreated | 0x400050a7 | Aggregation group already exists. |
| 4.0 | Invalid Operation | hasAggrgroupPortAdded | 0x400050a8 | The port has been added to another aggregation group. |
| 4.0 | Invalid Operation | hasVlanCreated | 0x400050a9 | VLAN created. |
| 4.0 | Invalid Operation | addVlanIdFailed | 0x400050aa | Creating VLANID failed. |
| 4.0 | Invalid Operation | delVlanIdFailed | 0x400050ab | Deleting VLANID failed. |
| 4.0 | Invalid Operation | limitVlanNumber | 0x400050ac | Number of VLAN exceeded limit. |
| 4.0 | Invalid Operation | delDefaultVlanNotAllowed | 0x400050ad | Default VLAN cannot be deleted. |
| 4.0 | Invalid Operation | limitPortPermitVlanNum | 0x400050ae | Number of VLAN allowed by port exceeded limit. |
| 4.0 | Invalid Operation | setAccessPortFailed | 0x400050af | Configuring access port failed. |
| 4.0 | Invalid Operation | setTrunkPortFailed | 0x400050b0 | Configuring trunk port failed. |
| 4.0 | Invalid Operation | keepVlanOneEqualDefault | 0x400050b1 | At least one port has a VLANID 1> |
| 4.0 | Invalid Operation | setFiberPortNotAllowed | 0x400050b2 | Fiber optic port does not support editing. |
| 4.0 | Invalid Operation | setPortAllLinkDownNotAllowed | 0x400050b3 | Closing all ports is not allowed. |
| 4.0 | Invalid Operation | setPortDuplexNotAllowed | 0x400050b4 | Duplex mode does not support editing. |
| 4.0 | Invalid Operation | setPortDistanceNotAllowed | 0x400050b5 | Long range port configuration is not supported. |
| 4.0 | Invalid Operation | setPortPoeNotAllowed | 0x400050b6 | PoE port configuration is not supported. |
| 4.0 | Invalid Operation | setPortPriNotAllowed | 0x400050b7 | Priority configuration is not supported. |
| 4.0 | Invalid Operation | setAggregationNotAllowed | 0x400050b8 | Link aggregation is not supported. |
| 4.0 | Invalid Operation | hasPortDistanceOpened | 0x400050b9 | Long range port has been enabled. Editing rate failed. |
| 4.0 | Invalid Operation | setPortEnableFalied | 0x400050ba | Setting port switch failed. |
| 4.0 | Invalid Operation | setPortSpeedFalied | 0x400050bb | Setting port rate failed. |
| 4.0 | Invalid Operation | setPortDuplexFalied | 0x400050bc | Setting duplex mode failed. |
| 4.0 | Invalid Operation | setPortPauseFalied | 0x400050bd | Setting port flow control failed. |
| 4.0 | Invalid Operation | setPortDistanceFalied | 0x400050be | Setting port long range failed. |
| 4.0 | Invalid Operation | setPortPriFalied | 0x400050bf | Setting port priority failed. |
| 4.0 | Invalid Operation | setPortPoeFalied | 0x400050c0 | Setting port POE failed. |
| 4.0 | Invalid Operation | exportCfgFileError | 0x400050c1 | Exporting configuration file failed. |
| 4.0 | Invalid Operation | passwordCheckFailed | 0x400050c2 | Verifying password failed. |
| 4.0 | Invalid Operation | noSupportSetSpecialPreset | 0x400050c3 | Setting specific preset is not supported. |
| 4.0 | Invalid Operation | frequentOperation | 0x400050c4 | Too many operations. |
| 4.0 | Invalid Operation | ledResolutionMisMatched | 0x400050c5 | The LED resolution of the output port mismatch. The height of the output port in the same row should be the same. The width of theoutput port in the same column should be the same. |
| 4.0 | Invalid Operation | oddPortNotSptRes | 0x400050c6 | Odd port does not support this resolution. |
| 4.0 | Invalid Operation | eventPortNotSptRes | 0x400050c7 | Even port does not support this resolution. |
| 4.0 | Invalid Operation | 485CheckBitSetError | 0x400050c8 | 485 parity bit setting error. |
| 4.0 | Invalid Operation | externalDeviceAddress | 0x400050c9 | 485 peripheral address setting error. |
| 4.0 | Invalid Operation | virtualLedNotSupport4KOutput | 0x400050ca | Virtual LED does not support 4K output display. |
| 4.0 | Invalid Operation | baseMapNotSupport4KOutput | 0x400050cb | Background picture does not support 4K output display. |
| 4.0 | Invalid Operation | minBlockInVirtualLEDAndOutput | 0x400050cc | Virtual LED and output overlaps and causes a small block. |
| 4.0 | Invalid Operation | 485protoFileVersionInvalid | 0x400050cd | Invalid version of 485 protocol file. |
| 4.0 | Invalid Operation | 485protoFileCheckError | 0x400050ce | 485 protocol file verification error. |
| 4.0 | Invalid Operation | 485protoFileSizeAbnormal | 0x400050cf | 485 protocol file size exception. |
| 4.0 | Invalid Operation | pleaseCheckInputAndOutput | 0x400050d0 | Please check input and output device. |
| 4.0 | Invalid Operation | NotSpeakerForbidShowInSpeakeMode | 0x400050d1 | Enabling presentation by non-speakers is not allowed when in speaker mode. |
| 4.0 | Invalid Operation | sipTransAndEncryptProtocolConflict | 0x400050d2 | SIP transport protocol and encryption type conflict. |
| 4.0 | Invalid Operation | sipUserPasswordError | 0x400050d3 | Incorrect SIP authentication password. |
| 4.0 | Invalid Operation | sipConferenceNeedAdminAndPassword | 0x400050d4 | Registering user name and password on SIP server is required for meetings held via SIP server. |
| 4.0 | Invalid Operation | clusterLinked | 0x400050d5 | Editing this configuration is not supported. Cluster is connected. |
| 4.0 | Invalid Operation | setPoeWatchDogFailed????????????? | 0x400050d6 | Configuring PoE watchdog failed. |
| 4.0 | Invalid Operation | setPortBandControlFailed?????????? | 0x400050d7 | Configuring port speed limit failed. |
| 4.0 | Invalid Operation | setPortStormControlFailed????????? | 0x400050d8 | Configuring port storm failed. |
| 4.0 | Invalid Operation | setPortMirrorFailed??????????????????? | 0x400050d9 | Configuring port mirror failed. |
| 4.0 | Invalid Operation | delAggrgroupVlanFailed??????????? | 0x400050da | Configuring VLAN under the same aggregation group failed. |
| 4.0 | Invalid Operation | fastAddChannelFull | 0x400050db | Number of cameras in quick add channel exceeded limit. |
| 4.0 | Invalid Operation | addDuplicateIPC | 0x400050dc | Duplicate network camera added. |
| 4.0 | Invalid Operation | analyzingCannotModifyChannelInfo | 0x400050dd | Cannot edit channel information of channel which is conducting analysis. |
| 4.0 | Invalid Operation | loginfFroDeviceFailed | 0x400050de | Logging into encoding device failed. |
| 4.0 | Invalid Operation | noDetectionArea | 0x400050df | Configuration failed. Detection area is not configured. |
| 4.0 | Invalid Operation | subSystemConfigFailed | 0x400050e0 | Sub-system configuration parameter error. |
| 4.0 | Invalid Operation | subSystemTaskStatusFailed | 0x400050e1 | Binding task status of sub-system error. |
| 4.0 | Invalid Operation | longDisNeedConsistentInAggr | 0x400050e2 | Long range under the same aggregation group should be consistent. |
| 4.0 | Invalid Operation | monitorPortInAgg | 0x400050e3 | Live view port cannot be in the aggregation group. |
| 4.0 | Invalid Operation | mirrorPortNeedConsistentInAggr | 0x400050e4 | Port mirror configuration in the aggregation group should be consistent. |
| 4.0 | Invalid Operation | stpPortNeedConsistentInAggr | 0x400050e5 | STP port configuration in the aggregation group should be consistent. |
| 4.0 | Invalid Operation | stpAggrPortNotSupportConfig | 0x400050e6 | Configuring STP port in the aggregation group failed. Remove the port from the aggregation group first. |
| 4.0 | Invalid Operation | notificationStartStreamingFailure | 0x400050e7 | Notifying start streaming failed. |
| 4.0 | Invalid Operation | taskNotMatchEngine | 0x400050e8 | Task and engine mismatch. |
| 4.0 | Invalid Operation | subColonyNoSupport | 0x400050e9 | Cluster peripheral does not support this configuration. |
| 4.0 | Invalid Operation | colonyNeedControlAndCentralPort | 0x400050ea | Cluster control port and repeater service port must be enabled in cluster mode. |
| 4.0 | Invalid Operation | widthLargerThan2560AndHeightLargerThan1440FrameRateCanBeSet25/30 | 0x400050eb | Frame rate can only be set as 25/30 when width>2560 and height>1440. |
| 4.0 | Invalid Operation | notIPCallWhenGKOrSipLink | 0x400050ed | Calling IP address is not supported when registering GK/SIP server (only domain name calling allowed: point to point, join meeting, and create meeting). |
| 4.0 | Invalid Operation | loopConferenceCannotSetSpeaker | 0x400050ee | Setting speaker is not allowed in conference polling. |
| 4.0 | Invalid Operation | speakerModeCannotLoopConference | 0x400050ef | Conference polling is not allowed in speaker mode. |
| 4.0 | Invalid Operation | cannotModifyInConference | 0x400050f0 | Editing is not allowed in meeting. |
| 4.0 | Invalid Operation | cannotStrengthEncryptConfByTLSClosed | 0x400050f1 | Force encryption meeting registration is not supported. TLS registration is not enabled. |
| 4.0 | Invalid Operation | updatePackageNameOrSizeNotMatch | 0x400050f2 | Upgrade package size or name mismatch. |
| 4.0 | Invalid Operation | terminalEncryptedCannotOneKeyConference | 0x400050f3 | Quick create meeting is not supported when terminal configuration is encrypted. |
| 4.0 | Invalid Operation | notSupportColonySIPConference | 0x400050f4 | Cascading SIP conference is not supported. |
| 4.0 | Invalid Operation | notSupportAutoColonySIPConference | 0x400050f5 | Automatic cascading SIP conference is not supported. |
| 4.0 | Invalid Operation | sipStrongEncryptedNotUDPOrTCP | 0x400050f6 | UDP or TCP transmission protocol is not supported by SIP force encryption. |
| 4.0 | Invalid Operation | sipDependUDPOrTCPNotStrongEncrypted | 0x400050f7 | Force encryption is not supported. SIP transfer in accordance with UDP or TCP protocol. |
| 4.0 | Invalid Operation | terminalNotStartMediaOutput | 0x400050f8 | Audio and video output is not enabled by terminal. |
| 4.0 | Invalid Operation | checkRollAlreadyOver | 0x400050f9 | The roll call ended. |
| 4.0 | Invalid Operation | conferenceCodeExist | 0x400050fa | Conference code already exists. |
| 4.0 | Invalid Operation | bottomPicLoadParamFail | 0x400050fb | Loading parameter from bottom layer failed. No data written in bottom layer. |
| 4.0 | Invalid Operation | topBlackBiggerThanMax | 0x400050fc | The height of top blackness exceeds limit. |
| 4.0 | Invalid Operation | fontSizeBiggerThanLimit | 0x400050fd | Font size exceeds limit. |
| 4.0 | Invalid Operation | splitScreenNotsptInJointMode | 0x400050fe | Window division is not supported in collaged signal source display mode. |
| 4.0 | Invalid Operation | jointNotsptInSplitScreenMode | 0x400050ff | The collaged signal source is not supported in the window division mode. |
| 4.0 | Invalid Operation | upgradeProgramErr | 0x40005100 | Error occurred when executing upgrade program. |
| 4.0 | Invalid Operation | upgradeNoDevice | 0x40005101 | No upgradeable device. LED controller has not been connected with receiving card or multi-functional card, or other reasons. |
| 4.0 | Invalid Operation | imageZoomExceedLimit | 0x40005102 | Image zooming in/out exceeded limit. |
| 4.0 | Invalid Operation | resolutionOverLimit | 0x40005103 | Input resolution exceeded limit. |
| 4.0 | Invalid Operation | noCustomBase | 0x40005104 | No customized background picture. |
| 4.0 | Invalid Operation | priorityLower | 0x40005105 | Priority is lower than current mode. |
| 4.0 | Invalid Operation | sendMessageExcept | 0x40005106 | Exception occurred when sending message. |
| 4.0 | Invalid Operation | sendCardUpgrading | 0x40005107 | Upgrading sending card... |
| 4.0 | Invalid Operation | noWirelessNetCard | 0x40005108 | Wireless NIC is required. |
| 4.0 | Invalid Operation | loadFromScreenFail | 0x40005109 | Loading from screen failed. |
| 4.0 | Invalid Operation | flashUnstoreRecCard | 0x4000510a | No receiving card parameter stored in Flash. |
| 4.0 | Invalid Operation | faceURLIsEmpty | 0x4000510b | Face picture URL is required. |
| 4.0 | Invalid Operation | fileServerInfoIsEmpty | 0x4000510c | Picture storage server information is required. |
| 4.0 | Invalid Operation | fileDownloadFailed | 0x4000510d | Downloading file failed. |
| 4.0 | Invalid Operation | cameraOffline | 0x4000510e | Camera is offline. |
| 4.0 | Invalid Operation | faceFilePathIsEmpty | 0x4000510f | Face picture path is empty. |
| 4.0 | Invalid Operation | faceFileIsNotExist | 0x40005110 | Face picture file does not exist. |
| 4.0 | Invalid Operation | faceDataIsEmpty | 0x40005111 | Face picture information is required. |
| 4.0 | Invalid Operation | cardInfoIsNull | 0x40005112 | Card information is required. |
| 4.0 | Invalid Operation | cardInfoIsNotExist | 0x40005113 | Card information does not exist. |
| 4.0 | Invalid Operation | userInfoIsEmpty | 0x40005114 | User data is required. |
| 4.0 | Invalid Operation | terminalInternalError | 0x40005115 | Terminal internal error. |
| 4.0 | Invalid Operation | infopublishAPPNotRun | 0x40005116 | Information release application is not working. |
| 4.0 | Invalid Operation | faceEattendanceAPPNotRun | 0x40005117 | Attendance application is not working. |
| 4.0 | Invalid Operation | notDeployCamere | 0x40005118 | No camera added to terminal. |
| 4.0 | Invalid Operation | deepEyeInterErr | 0x40005119 | DeepinView camera internal error. |
| 4.0 | Invalid Operation | selfDevelopedInterErr | 0x4000511a | Self-Developed camera internal error. |
| 4.0 | Invalid Operation | forbiddenedCancelChairModeByPollRollSelect | 0x4000511b | Canceling host is not allowed when watching conference polling calling. |
| 4.0 | Invalid Operation | errorConferenceExtensionTime | 0x4000511c | Incorrect prolonged conference time (prolonged meeting time should be longer than 10 minutes and shorter than 24 hours. |
| 4.0 | Invalid Operation | forbiddenedCallYourselfByPTOP | 0x4000511d | Calling yourself is not allowed in point-to-point conference. |
| 4.0 | Invalid Operation | displayResolutionIsLessThanSmallestResolution | 0x4000511e | Display resolution is lower than minimum resolution. |
| 4.0 | Invalid Operation | notSupportLocalSourcesDragMore | 0x4000511f | A local signal resource can be displayed in only one window on the wall simultaneously. |
| 4.0 | Invalid Operation | materialIsLockedByProgram | 0x40005120 | Material is locked by program. |
| 4.0 | Invalid Operation | programIsLockedBySchedule | 0x40005121 | Program is locked by schedule. |
| 4.0 | Invalid Operation | networkSourceIPAlreadyExists | 0x40005122 | Network source IP address already exists. |
| 4.0 | Invalid Operation | BNCOutputNotSupportRoam | 0x40005123 | Roaming does not support decoding for BNC. |
| 4.0 | Invalid Operation | cancelTheCurrentLedAreaFirst | 0x40005124 | Output is in the LED area. Cancel it first. |
| 4.0 | Invalid Operation | terminalBusy | 0x40005125 | Terminal is busy, or no response. |
| 4.0 | Invalid Operation | terminalPasswordError | 0x40005126 | Incorrect terminal user name or password. |
| 4.0 | Invalid Operation | terminalIsLocking | 0x40005127 | Terminal is locked. |
| 4.0 | Invalid Operation | terminalNotActivated | 0x40005128 | Terminal is not activated. |
| 4.0 | Invalid Operation | terminalHasActivated | 0x40005129 | Terminal is activated. |
| 4.0 | Invalid Operation | syncSignalSourceOnTheWallCannotBeDeleted | 0x4000512a | Deleting is not allowed. Sync signal source has been displayed on screen. |
| 4.0 | Invalid Operation | currentModeNnotSupportImageRotation | 0x4000512b | Current mode does not support image rotation. |
| 4.0 | Invalid Operation | fileFormatConversionTimeout | 0x4000512c | Format conversion timed out. |
| 4.0 | Invalid Operation | onlineTerminalCannotModify | 0x4000512d | Do not edit online terminal. |
| 4.0 | Invalid Operation | customProtocolNameDuplicate | 0x4000512e | Duplicate self-defining protocol name. |
| 4.0 | Invalid Operation | customProtocolIsUsingNotAllowModifify | 0x4000512f | Editing is not allowed. Self-defining protocol in use. |
| 4.0 | Invalid Operation | libreOfficeNotInstall | 0x40005130 | Third-Party libreOffice is not installed. |
| 4.0 | Invalid Operation | onlyPublicCloudSupportsHotWordFunction | 0x40005131 | Only publica cloud supports hot word function. |
| 4.0 | Invalid Operation | fileExpired | 0x40005132 | File expired. |
| 4.0 | Invalid Operation | switchCameraManualModeThenControlGimbal | 0x40005133 | Switch mode of camera to manual mode before using PTZ control. |
| 4.0 | Invalid Operation | LEDNotInAssociatedArea | 0x40005134 | LED is not in linked area. |
| 4.0 | Invalid Operation | sceneConfigFileNameTooLong | 0x40005135 | Scene configuration file name is too long. |
| 4.0 | Invalid Operation | theSignalNotSupportDivision | 0x40005136 | Signal source does not support window division. |
| 4.0 | Invalid Operation | virtualLEDPictureSizeExceedLimit | 0x40005137 | Size of virtual LED picture exceeded limit. |
| 4.0 | Invalid Operation | noErrorReport | 0x40005138 | No error report. |
| 4.0 | Invalid Operation | voiceServerConnectionNotAllowedModifyIP | 0x40005139 | Editing IP address is not allowed. Connecting to voice server... |
| 4.0 | Invalid Operation | platformIPConflict | 0x4000513a | Platform IP address conflict. |
| 4.0 | Invalid Operation | variableCodeDuplication | 0x4000513b | Duplicate variable code. |
| 4.0 | Invalid Operation | addressNumberDuplicate | 0x4000513c | Duplicate address No. |
| 4.0 | Invalid Operation | addressCodeDuplication | 0x4000513d | Duplicate address code. |
| 4.0 | Invalid Operation | slaveAddressNumberCanOnlyBe1 | 0x4000513e | Sub node No. can only be 1. |
| 4.0 | Invalid Operation | variableNameDuplication | 0x4000513f | Duplicate variable name. |
| 4.0 | Invalid Operation | registerDddressDuplication | 0x40005140 | Duplicate register address. |
| 4.0 | Invalid Operation | registerGKServiceNotSupportCallingH323ProtocolIP | 0x40005141 | Calling H323 protocol IP address is not supported when registering to GK service. |
| 4.0 | Invalid Operation | registerSIPServiceNotSupportCallingSIPProtocolIP | 0x40005142 | Calling SIP protocol IP address is not supported when registering to SIP service. |
| 4.0 | Invalid Operation | usernameOrPasswordErrorOfTheFoundingServer | 0x40005143 | Incorrect user name or password of creating meeting server. |
| 4.0 | Invalid Operation | incorrectConferencePassword | 0x40005144 | Incorrect conference password. |
| 4.0 | Invalid Operation | dspParsesThePictureIncorrectly | 0x40005145 | Error occurred when DSP is parsing picture. |
| 4.0 | Invalid Operation | siteVariableNnotExisted | 0x40005146 | The site variable does not exist. |
| 4.0 | Invalid Operation | subBoardNumberOrSiteNumberNotMatchTheSiteType | 0x40005147 | Sub-Board No. or site No. and site type mismatch. |
| 4.0 | Invalid Operation | useDomainToCallWhenSIPServiceNotRegistered | 0x40005149 | Calling domain name is applied when SIP service is not registered. |
| 4.0 | Invalid Operation | confTemplateNameConflict | 0x40005150 | Meeting template name conflict. |
| 4.0 | Invalid Operation | hotStandbyNotAllowedModifyHotStandbyTypeAndRole | 0x40005151 | Editing hot spare type and role is not allowed. Hot spare device is started. |
| 4.0 | Invalid Operation | hotStandbyNotAllowedModifySiteAndVariable | 0x40005152 | Editing station and variable is not allowed. Hot spare device is started. |
| 4.0 | Invalid Operation | hotStandbyPeerAabnormalCannotBeSwitched | 0x40005153 | Switching failed. Peer end of hot spare device exception. |
| 4.0 | Invalid Operation | configureThePreviousRulesFirst | 0x40005154 | Configure previous rule first. |
| 4.0 | Invalid Operation | IPChannelLinkedToTheAssociatedVideoCannotBeDeleted | 0x40005155 | Deleting IP channel linked to video linkage is not allowed. |
| 4.0 | Invalid Operation | notSupportSimultaneousConfigurationSingleAndMultiplayerRunningModes | 0x40005156 | Single person mode and multiple persons mode cannot be configured in a task simultaneously. |
| 4.0 | Invalid Operation | deviceCtrledByRemoter | 0x40005157 | Device is currently controlled by a remote control. |
| 4.0 | Invalid Operation | engineBindingInProgressPleaseWait | 0x40005158 | Binding engine...Please wait. |
| 4.0 | Invalid Operation | carouselBasemapsHaveBeenPostedOnTheWallCannotBeDeleted | 0x40005159 | Loop base map displayed on the video wall cannot be deleted. |
| 4.0 | Invalid Operation | inputBoardUsedForSignalSourceSplicingCannotModifyTheNetworkArea | 0x4000515A | Cannot edit network area of input board used for signal resource splicing. |
| 4.0 | Invalid Operation | thePictureIsInUseAndCannotBeDeleted | 0x4000515B | Picture in use can not be deleted. |
| 4.0 | Invalid Operation | duplicateImageName | 0x4000515C | Duplicate picture name. |
| 4.0 | Invalid Operation | importOrAddFailed | 0x4000515D | Importing/Adding failed. |
| 4.0 | Invalid Operation | networkDetectionServerIsNotTurnedOn | 0x4000515E | Network detection server is disabled. |
| 4.0 | Invalid Operation | modelFileParsingFailed | 0x4000515F | Parsing model file failed. |
| 4.0 | Invalid Operation | modelLabelFileParsingFailed | 0x40005160 | Parsing model label file failed. |
| 4.0 | Invalid Operation | storSerDownloadFileFailed | 0x40006000 | Downloading file from storage service failed. |
| 4.0 | Invalid Operation | storSerDownloadFileSizeZero | 0x40006001 | Size of file downloaded from storage service is 0. |
| 4.0 | Invalid Operation | illegalTaskID | 0x40006002 | Invalid task ID. |
| 4.0 | Invalid Operation | storSerNotConfig | 0x40006003 | Storage service is not configured. |
| 4.0 | Invalid Operation | storSerUnavailable | 0x40006004 | Storage service is unavailable. |
| 4.0 | Invalid Operation | noUpgradePakage | 0x40006005 | No upgrade package information. |
| 4.0 | Invalid Operation | QRCodeGenFailure | 0x40006006 | Converting QR code picture failed. |
| 4.0 | Invalid Operation | decryptFailed | 0x40006008 | Decryption failed. |
| 4.0 | Invalid Operation | invalidIURL | 0x40006009 | Content after question mark (?) in URL is invalid. |
| 4.0 | Invalid Operation | fileUploadFailed | 0x4000600A | Uploading files (including pictures) failed. |
| 4.0 | Invalid Operation | codingFormatNotMatch | 0x4000600B | Encoding format of two communication sides mismatch. Negotiation failed. |
| 4.0 | Invalid Operation | destinationLongNumberError | 0x4000600C | Incorrect requested target long number. |
| 4.0 | Invalid Operation | multiAuthenticationFailed | 0x4000600D | Operating multi-factor authentication status failed. |
| 4.0 | Invalid Operation | materialDownloadFailed | 0x4000600E | Downloading materials failed. |
| 4.0 | Invalid Operation | fingerPrintNotExist | 0x4000600F | Fingerprint does not exist. The exception may occur when obtaining fingerprint from card reader or host machine by card No. or employee No. |
| 4.0 | Invalid Operation | faceLowQulity | 0x40006010 | Poor face picture quality. The exception may occur when applying face pictures. |
| 4.0 | Invalid Operation | faceResolutionOrRatioError | 0x40006011 | Face picture resolution or aspect ratio exception. The exception may occur when applying face pictures. |
| 4.0 | Invalid Operation | faceDataNotExist | 0x40006012 | User facial data does not exist. The exception may occur when searching person by face picture. |
| 4.0 | Invalid Operation | videoDownloadFailed | 0x40006013 | Downloading video failed. |
| 4.0 | Invalid Operation | deviceExisted | 0x40007000 | Intelligent device already exists. |
| 4.0 | Invalid Operation | nameExisted | 0x40007001 | Name already exists (device, scene, room). |
| 4.0 | Invalid Operation | numOverLimit | 0x40007002 | Number reached limit (device, scene, room). |
| 4.0 | Invalid Operation | sceneWorking | 0x40007003 | Deleting is not allowed. Scene is in use. |
| 4.0 | Invalid Operation | devicesNotExist | 0x40007004 | Intelligent device does not exist. |
| 4.0 | Invalid Operation | sceneIdNotExist | 0x40007005 | Scene does not exist. |
| 4.0 | Invalid Operation | sceneDelReject | 0x40007006 | Deleting scene is not allowed (at least 4 scenes should be reserved). |
| 4.0 | Invalid Operation | detectorNotExist | 0x40007007 | Detector does not exist. |
| 4.0 | Invalid Operation | roomNotExist | 0x40007008 | Room does not exist. |
| 4.0 | Invalid Operation | noSetAlarmPassword | 0x40007009 | No set arming/disarming password. |
| 4.0 | Invalid Operation | noRequest | 0x4000700a | No calling request (intercom call service). |
| 4.0 | Invalid Operation | dialedIsBusy | 0x4000700b | The device is busy now (intercom call service). |
| 4.0 | Invalid Operation | armingFailed | 0x40008000 | Arming failed. |
| 4.0 | Invalid Operation | disarmingFailed | 0x40008001 | Disarming failed. |
| 4.0 | Invalid Operation | clearAlarmFailed | 0x40008002 | Alarm clearing failed. |
| 4.0 | Invalid Operation | bypassFailed | 0x40008003 | Bypass failed. |
| 4.0 | Invalid Operation | bypassRecoverFailed | 0x40008004 | Bypass restoring failed. |
| 4.0 | Invalid Operation | outputsOpenFailed | 0x40008005 | Opening relay failed. |
| 4.0 | Invalid Operation | outputsCloseFailed | 0x40008006 | Closing relay failed. |
| 4.0 | Invalid Operation | registerTimeOut | 0x40008007 | Registering timed out. |
| 4.0 | Invalid Operation | registerFailed | 0x40008008 | Registering failed. |
| 4.0 | Invalid Operation | addedByOtherHost | 0x40008009 | The peripheral is already added by otherl control  panel. |
| 4.0 | Invalid Operation | alreadyAdded | 0x4000800A | The peripheral is already added by the current control panel. |
| 4.0 | Invalid Operation | armedStatus | 0x4000800B | The partition is armed. |
| 4.0 | Invalid Operation | bypassStatus | 0x4000800C | Bypass status. |
| 4.0 | Invalid Operation | zoneNotSupport | 0x4000800D | The zone does not support the operation. |
| 4.0 | Invalid Operation | zoneFault | 0x4000800E | The zone is in fault status. |
| 4.0 | Invalid Operation | pwdConflict | 0x4000800F | Password conflicted. |
| 4.0 | Invalid Operation | audioTestEntryFailed | 0x40008010 | Enabling audio test mode failed. |
| 4.0 | Invalid Operation | audioTestRecoveryFailed | 0x40008011 | Disabling audio test mode failed. |
| 4.0 | Invalid Operation | addCardMode | 0x40008012 | Adding card mode. |
| 4.0 | Invalid Operation | searchMode | 0x40008013 | Search mode. |
| 4.0 | Invalid Operation | addRemoterMode | 0x40008014 | Adding keyfob mode. |
| 4.0 | Invalid Operation | registerMode | 0x40008015 | Registration mode. |
| 4.0 | Invalid Operation | exDevNotExist | 0x40008016 | The peripheral does not exist. |
| 4.0 | Invalid Operation | theNumberOfExDevLimited | 0x40008017 | No peripheral can be added. |
| 4.0 | Invalid Operation | sirenConfigFailed | 0x40008018 | Setting siren failed. |
| 4.0 | Invalid Operation | chanCannotRepeatedBinded | 0x40008019 | This channel is already linked by the zone. |
| 4.0 | Invalid Operation | illegalPointParameter | 0x4000801A | Invalid calibration point parameter. |
| 4.0 | Invalid Operation | inProgramMode | 0x4000801B | The keypad is in programming mode. |
| 4.0 | Invalid Operation | remoterAlreadyRegistered | 0x4000801C | The remote control has been added to another control panel. |
| 4.0 | Invalid Operation | remoterSerialNumberError | 0x4000801D | Incorrect serial number of remote control. |
| 4.0 | Invalid Operation | repeaterSerialNumberError | 0x4000801E | Incorrect serial number of repeater. |
| 4.0 | Invalid Operation | outputModuleSerialNumberError | 0x4000801F | Incorrect serial number of wireless output module. |
| 4.0 | Invalid Operation | slaveRadarOffline | 0x40008020 | Slave radar is offline. |
| 4.0 | Invalid Operation | slavePasswordError | 0x40008021 | Incorrect slave radar password. |
| 4.0 | Invalid Operation | addedByOtherRadar | 0x40008022 | The device has been added to other radar. |
| 4.0 | Invalid Operation | devIsMasterRadar | 0x40008023 | The device is the master radar. |
| 4.0 | Invalid Operation | alarmRuleNotMatch | 0x40008024 | Trigger line rule mismatch. |
| 4.0 | Invalid Operation | cfgRadarTimeOut | 0x40008025 | Configuring radar parameter timed out. |
| 4.0 | Invalid Operation | subSystemNotEnabled | 0x40008026 | Sub-system is not enabled. |
| 4.0 | Invalid Operation | sameCenterParam | 0x40008027 | Duplicate central parameter. |
| 4.0 | Invalid Operation | sameKeypadPassword | 0x40008028 | Duplicate keyboard password. |
| 4.0 | Invalid Operation | extensionDeviceConfigFailed | 0x40008029 | Peripherals configuration failed. |
| 4.0 | Invalid Operation | recvModuleNoSpaceAdd | 0x4000802b | No more peripherals of receiver can be added. |
| 4.0 | Invalid Operation | masterSlaveIsEnable | 0x4000802c | The master-slave relationship has taken effect, the slave radar does not support this operation. |
| 4.0 | Invalid Operation | forceTrackNotEnabled | 0x4000802d | Mandatory tracking is disabled. |
| 4.0 | Invalid Operation | isNotSupportZoneConfigByLocalArea | 0x4000802e | This area does not support the zone type. |
| 4.0 | Invalid Operation | alarmLineCross | 0x4000802f | Trigger lines are overlapped. |
| 4.0 | Invalid Operation | zoneDrawingOutOfRange | 0x40008030 | The drawn zone is out of detection range. |
| 4.0 | Invalid Operation | alarmLineDrawingOutOfRange | 0x40008031 | The drawn alarm trigger line is out of detection range. |
| 4.0 | Invalid Operation | hasTargetInWarningArea | 0x40008032 | The warning zone already contains targets. Whether to enable mandatory arming? |
| 4.0 | Invalid Operation | radarMoudleConnectFail | 0x40008033 | Radar module communication failed. |
| 4.0 | Invalid Operation | importCfgFilePasswordErr | 0x40008034 | Incorrect password for importing configuration files. |
| 4.0 | Invalid Operation | cameraIsNotCalibrated | 0x40008035 | Camera is not calibrated. |
| 4.0 | Invalid Operation | cameraIsNotTrackEnable | 0x40008036 | Tracking is not enabled. |
| 4.0 | Invalid Operation | drawedAlarmLineIsOnPreAlarmline | 0x40008037 | New trigger line overlaps with original trigger line. |
| 4.0 | Invalid Operation | overAudioFileNumLimit | 0x40008038 | The number of audio files exceeded limit. |
| 4.0 | Invalid Operation | audioFileNameIsLong | 0x40008039 | The audio file name is too long. |
| 4.0 | Invalid Operation | audioFormatIsWrong | 0x4000803a | The audio file format is invalid. |
| 4.0 | Invalid Operation | audioFileIsLarge | 0x4000803b | The size of the audio file exceeded limit. |
| 4.0 | Invalid Operation | pircamCapTimeOut | 0x4000803c | Capturing of pircam timed out. |
| 4.0 | Invalid Operation | pircamCapFail | 0x4000803d | Capturing of pircam failed. |
| 4.0 | Invalid Operation | pircamIsCaping | 0x4000803e | The pircam is capturing. |
| 4.0 | Invalid Operation | audioFileHasExisted | 0x4000803f | The audio file already exists. |
| 4.0 | Invalid Operation | MCUUpgradeFail | 0x40008040 | Upgrading MCU failed. |
| 4.0 | Invalid Operation | speakerIsSetUpInTheMeetingDiscussionModeNotAllowed | 0x40008041 | Enabling discussion mode is not allowed when speaker is set in conference. |
| 4.0 | Invalid Operation | voiceStimulusTurnedOnDiscussionModeNotAllowed | 0x40008042 | Enabling discussion mode is not allowed when voice activated is enabled in conference. |
| 4.0 | Invalid Operation | rollCallEnabledDiscussionModeNotAllowed | 0x40008043 | Enabling discussion mode is not allowed when roll call is enabled in conference. |
| 4.0 | Invalid Operation | meetingRotationTrainingStartedDiscussionModeNotAllowed | 0x40008044 | Enabling discussion mode is not allowed when polling is enabled in conference. |
| 4.0 | Invalid Operation | insufficientTextConversionResources | 0x40008045 | Not enough resource to convert text. |
| 4.0 | Invalid Operation | insufficientTranslationResources | 0x40008046 | Not enough translation resource. |
| 4.0 | Invalid Operation | insufficientSemanticResources | 0x40008047 | Not enough semantic resource. |
| 4.0 | Invalid Operation | textConversionFail | 0x40008048 | Converting to text failed. |
| 4.0 | Invalid Operation | semanticFailure | 0x40008049 | Incorrect name. |
| 4.0 | Invalid Operation | translationFailure | 0x4000804a | Translation failed. |
| 4.0 | Invalid Operation | voiceServerRegistrationFailed | 0x4000804b | Registering audio server failed. |
| 4.0 | Invalid Operation | inZoneDetectionMode | 0x4000804c | Zone detection mode. |
| 4.0 | Invalid Operation | inZoneSignalDetectionMode | 0x4000804d | Zone signal strength detection mode. |
| 4.0 | Invalid Operation | radarAndMonitorGPSIsSame | 0x4000804e | The GPS position of radar and camera are the same. |
| 4.0 | Invalid Operation | alarmingCannotBeArmed | 0x4000804f | Arming failed. Device is uploading alarm. |
| 4.0 | Invalid Operation | oneKeyLock | 0x40008050 | One-Touch lock. |
| 4.0 | Invalid Operation | healthDetectProcess | 0x40008051 | Detecting health status... |
| 4.0 | Invalid Operation | findMeProcess | 0x40008052 | Detecting findme... |
| 4.0 | Invalid Operation | discussionModeIsOpenedInTheMeetingSpeakerNotAllowed | 0x40008053 | Setting speaker is not allowed when discussion mode is enabled in conference. |
| 4.0 | Invalid Operation | discussionModeIsOpenedInTheMeetingVoiceStimulusNotAllowed | 0x40008054 | Voice activated is not allowed when discussion mode is enabled in conference. |
| 4.0 | Invalid Operation | virtualAlarmMarkOutOfRange | 0x40008055 | False track mark is out of the detection range. |
| 4.0 | Invalid Operation | environmentAutoLearning | 0x40008056 | Device is in automatic environment learning status. |
| 4.0 | Invalid Operation | radarDirectionNotInDetectionRange | 0x40008057 | Radar direction is out of the detection range. |
| 4.0 | Invalid Operation | currentCodingChannelNotCalibrate | 0x40008058 | Current code channel is not calibrated. |
| 4.0 | Invalid Operation | startEnvironmentLearning | 0x40008059 | Enable environment learning. |
| 4.0 | Invalid Operation | stopEnvironmentLearning | 0x4000805a | Exit environment learning. |
| 4.0 | Invalid Operation | forbiddenedConfigureVoiceTransferInPointToPointConference | 0x4000805b | Configuring voice converting function is not allowed in point-to-point conference. |
| 4.0 | Invalid Operation | hotStandbySerialPortNotAssociated | 0x4000805c | Hot spare serial port is not linked. |
| 4.0 | Invalid Operation | hotStandbySerialPortAssociatedRepeated | 0x4000805d | Duplicate hot spare serial port linkage. |
| 4.0 | Invalid Operation | numberOfLinkagePointsExceedsLimit | 0x4000805e | Number of cameras exceeded limit. |
| 4.0 | Invalid Operation | masterAndSubBoardHotStandbyConflicted | 0x4000805f | The hot spare of main control board and sub-board conflict. |
| 4.0 | Invalid Operation | siteNumberAlreadyExists | 0x40008060 | The site No. already exists. |
| 4.0 | Invalid Operation | variableNumberAlreadyExistsUnderTheSite | 0x40008061 | The site variable No. already exists. |
| 4.0 | Invalid Operation | floatTypeOnlySupportsTwoRegisters | 0x40008062 | Only two registers are allowed in float type. |
| 4.0 | Invalid Operation | ariableExceedsMaximumLimit | 0x40008063 | Number of variables exceeded limit. |
| 4.0 | Invalid Operation | siteExceedsMaximumLimit | 0x40008064 | Number of sites exceeded limit. |
| 4.0 | Invalid Operation | scriptsAssociatedVariablesNotAllowedBeDeleted | 0x40008065 | Deleting is not allowed. Script is linked to variable. |
| 4.0 | Invalid Operation | insufficientVoiceAssistantResources | 0x40008066 | Not enough voice assistant resource. |
| 4.0 | Invalid Operation | voiceFunctionIsEnabledNotAllowModifyServer Configuration | 0x40008067 | Editing server configuration is not allowed when voice function is enabled. |
| 4.0 | Invalid Operation | repeatersMatchProcess | 0x40008068 | Repeater is matching... |
| 4.0 | Invalid Operation | MCUUpgrading | 0x40008069 | Upgrading MCU... |
| 4.0 | Invalid Operation | upgradePackageTransferFailed | 0x4000806A | Transferring upgrade package failed. |
| 4.0 | Invalid Operation | noDeviceDetected | 0x4000806B | No peripherals detected. |
| 4.0 | Invalid Operation | notSupportFixedPointPreview | 0x4000806C | Manual live view is not supported at current location. |
| 4.0 | Invalid Operation | illegalAreaDraw | 0x4000a001 | Invalid area drawing. |
| 4.0 | Invalid Operation | calculationPowerNoResource | 0x4000a002 | Not enough computing power resource. |
| 4.0 | Invalid Operation | algorithmRebooting | 0x4000a003 | Rebooting algorithm... |
| 4.0 | Invalid Operation | notMatchFacelib | 0x4000a004 | Face picture library is not matched. |
| 4.0 | Invalid Operation | illegalRecognizeMode | 0x4000a005 | Invalid recognition mode. |
| 4.0 | Invalid Operation | configFailed | 0x4000a006 | Configuration failed. |
| 4.0 | Invalid Operation | poorFaceQuality | 0x4000a007 | Low face picture quality. |
| 4.0 | Invalid Operation | alreadyExistThisFace | 0x4000a008 | The face picture already exists. |
| 4.0 | Invalid Operation | errorUserInfo | 0x4000a009 | Incorrect person information. |
| 4.0 | Invalid Operation | existSameNameFacelib | 0x4000a00a | Face picture library with duplicate name exists. |
| 4.0 | Invalid Operation | delFacelibFailed | 0x4000a00b | Deleting face picture library failed. |
| 4.0 | Invalid Operation | modifyFacelibFailed | 0x4000a00c | Modifying face picture library failed. |
| 4.0 | Invalid Operation | createFacelibFailed | 0x4000a00d | Creating face picture library failed. |
| 4.0 | Invalid Operation | pictureDecodingFailed | 0x4000a00e | Decoding picture failed. |
| 4.0 | Invalid Operation | alreadyExistCertificateNumber | 0x4000a00f | ID No. already exists. |
| 4.0 | Invalid Operation | facelibAlreadyUsed | 0x4000a010 | The face picture library has been used. |
| 4.0 | Invalid Operation | cancelFacelibAlgorithmFirst | 0x4000a011 | Delete after cancelling  the matched face picture library algorithm. |
| 4.0 | Invalid Operation | beyondNumberLimit | 0x4000a012 | Number exceeded limit. |
| 4.0 | Invalid Operation | pollingGroupIsOperating | 0x4000a013 | Polling group is running. |
| 4.0 | Invalid Operation | performTheOperationWhenAlarmOccurs | 0x4000a014 | Operate again when device alarms. |
| 4.0 | Invalid Operation | existSameNamePollingGroup | 0x4000a015 | Duplicate polling group name. |
| 4.0 | Invalid Operation | subscribeTypeErr | 0x4000a016 | The subscription of metadata type is not supported by device. |
| 4.0 | Invalid Operation | subscribeIDErr | 0x4000a017 | Subscribe again. Subscription link ID does not exist. |
| 4.0 | Invalid Operation | channelOccupiedByAIOpenPlatform | 0x4000a018 | Current channel is occupied by AI open platform. |
| 4.0 | Invalid Operation | channelOccupiedByRealtimeAlgorithm | 0x4000a019 | Current channel is occupied by real-time/poll algorithm. |
| 4.0 | Invalid Operation | motorPreheatingError | 0x4000a01a | Enabling deicing failed. Warming up motor. |
| 4.0 | Invalid Operation | ptDeicingError | 0x4000a01b | Enabling deicing failed. PTZ is deicing. |
| 4.0 | Invalid Operation | EISError | 0x4000A01C | Electronic image stabilization failed. VCA is starting. |
| 4.0 | Invalid Operation | jpegPicWithAppendDataError | 0x4000A01D | Capturing thermal graphic failed. Thermography configuration parameter exception. |
| 4.0 | Invalid Operation | invalidShutterLimit | 0x4000A01E | Setting failed. The min. shutter limit shall be less than the max. shutter limit. |
| 4.0 | Invalid Operation | 4GCollectionModuleSweeping | 0x4000A01F | 4G information collection module is sweeping... |
| 4.0 | Invalid Operation | 4GCollectionModuleStarting | 0x4000A020 | 4G information collection module is starting... |
| 4.0 | Invalid Operation | IPNotAllowed | 0x4000A021 | The client IP address you are accessing is xx.xx.xx.xx and is not in the list. Accessing device will not be allowed if operation continues. |
| 4.0 | Invalid Operation | noNeedUpgrade | 0x4000A022 | Latest version already. No need to upgrade. |
| 4.0 | Invalid Operation | invalidIrisLimit | 0x4000A023 | Setting failed. The min. iris limit shall be less than the max. iris limit. |
| 4.0 | Invalid Operation | detectionUndersSize | 0x4000A024 | The facial detection frame area is too small. |
| 5.0 | Invalid  Format | badXmlFormat | 0x50000001 | XML format error. |
| 5.0 | Invalid  Format | badJsonFormat | 0x50000002 | JSON format error. |
| 5.0 | Invalid  Format | badURLFormat | 0x50000003 | URL format error. |
| 6.0 | Invalid Content | badParameters | 0x60000001 | Parameter error. |
| 6.0 | Invalid Content | badHostAddress | 0x60000002 | Invalid host IP address. |
| 6.0 | Invalid Content | badXmlContent | 0x60000003 | Invalid XML content. |
| 6.0 | Invalid Content | badIPv4Address | 0x60000004 | Invalid IPv4 address. |
| 6.0 | Invalid Content | badIPv6Address | 0x60000005 | Invalid IPv6. |
| 6.0 | Invalid Content | conflictIPv4Address | 0x60000006 | IPv4 address conflict. |
| 6.0 | Invalid Content | conflictIPv6Address | 0x60000007 | IPv6 address conflict. |
| 6.0 | Invalid Content | badDomainName | 0x60000008 | Incorrect domain name. |
| 6.0 | Invalid Content | connectSreverFail | 0x60000009 | Connecting to server failed. |
| 6.0 | Invalid Content | conflictDomainName | 0x6000000A | Domain name conflict. |
| 6.0 | Invalid Content | badPort | 0x6000000B | Port conflict. |
| 6.0 | Invalid Content | portError | 0x6000000C | Port error. |
| 6.0 | Invalid Content | exportErrorData | 0x6000000D | Failed to export data. |
| 6.0 | Invalid Content | badNetMask | 0x6000000E | Invalid sub-net mask. |
| 6.0 | Invalid Content | badVersion | 0x6000000F | Version mismatch. |
| 6.0 | Invalid Content | badDevType | 0x60000010 | Device type mismatch. |
| 6.0 | Invalid Content | badLanguage | 0x60000011 | Language mismatch. |
| 6.0 | Invalid Content | incorrentUserNameOrPassword | 0x60000012 | Incorrect user name or password. |
| 6.0 | Invalid Content | invalidStoragePoolOfCloudServer | 0x60000013 | Invalid storage pool for cloud storage. Storage pool is not configured or is with an incorrect ID. |
| 6.0 | Invalid Content | noFreeSpaceOfStoragePool | 0x60000014 | Insufficient space in storage pool. |
| 6.0 | Invalid Content | riskPassword | 0x60000015 | Risky password. |
| 6.0 | Invalid Content | UnSupportCapture | 0x60000016 | Capturing pictures is not supported. |
| 6.0 | Invalid Content | badJsonContent | 0x60000017 | Incorrect JSON message. |
| 6.0 | Invalid Content | tokenEmpty | 0x60000018 | Token is required. |
| 6.0 | Invalid Content | MessageParametersLack | 0x60000019 | No message parameter. |
| 6.0 | Invalid Content | invalidSearchConditions | 0x6000001A | Search condition expires. Set and search again. |
| 6.0 | Invalid Content | incorrectFileFormat | 0x6000001B | Invalid file format. |
| 6.0 | Invalid Content | nameContainsInvalidCharcters | 0x6000001C | Invalid characters. |
| 6.0 | Invalid Content | nameIsOverlong | 0x6000001D | Name is too long. |
| 6.0 | Invalid Content | upgratePackageSizeLargerThan10M | 0x6000001E | File size should be within 10M. |
| 6.0 | Invalid Content | upgrateParameterWrong | 0x6000001F | Device upgrade parameter error. |
| 6.0 | Invalid Content | upgrateDataEmpty | 0x60000020 | Device upgrade data is null. |
| 6.0 | Invalid Content | passwordMustContainMorethan8Characters | 0x60000021 | A password should contain at least 8 characters. |
| 6.0 | Invalid Content | userPwdLenUnder8 | 0x60000022 | A password should contain two types of characters, including digits, upper-case letters, lower-case letters, and specical characters. |
| 6.0 | Invalid Content | userPwdNameSame | 0x60000023 | The user name and password cannot be the same. |
| 6.0 | Invalid Content | userPwdNameMirror | 0x60000024 | Password cannot be the mirror writing of the user name. |
| 6.0 | Invalid Content | beyondARGSRangeLimit | 0x60000025 | Parameter value exceeded the limit. |
| 6.0 | Invalid Content | unableCalibrate | 0x60000026 | Unable to calibrate. |
| 6.0 | Invalid Content | pleaseCalibrate | 0x60000027 | Calibrate first. |
| 6.0 | Invalid Content | SNMPv3NameDifferent | 0x60000028 | Security name of SNMPv3 reading and writing cannot be same. |
| 6.0 | Invalid Content | SNMPv3PasswordNone | 0x60000029 | SNMPv3 password is empty. Set one first. |
| 6.0 | Invalid Content | CalibFailedPleaseAgain | 0x6000002A | Calibration failed. Try again. |
| 6.0 | Invalid Content | DetectionLineError | 0x6000002B | Rule line error. Try again. Rule line must be in the red area. |
| 6.0 | Invalid Content | currentEnginesConfigurationUnSupport | 0x6000002C | Configured linkage action is not supported by the current engine configuration. |
| 6.0 | Invalid Content | faceLibraryNumError | 0x6000002D | No more face picture libraries can be added. |
| 6.0 | Invalid Content | faceImagesNumError | 0x6000002E | No more face pictures can be added. |
| 6.0 | Invalid Content | faceDataAnalysisError | 0x6000002F | Recognizing picture data failed. |
| 6.0 | Invalid Content | faceDataPIDError | 0x60000030 | Invalid face data PID. |
| 6.0 | Invalid Content | faceLibraryIDError | 0x60000031 | Invalid face picture library ID. |
| 6.0 | Invalid Content | faceLibraryDatabaseError | 0x60000032 | Database version of face picture library mismatch. |
| 6.0 | Invalid Content | checkCodeError | 0x60000033 | Verification code error. |
| 6.0 | Invalid Content | faceLibraryError | 0x60000034 | Face picture library error. |
| 6.0 | Invalid Content | multipleFaceObjectError | 0x60000035 | Multiple faces are recognized in the pictures to be imported into the face picture library. |
| 6.0 | Invalid Content | PicAnalysisNoTargetError | 0x60000036 | No target recognized in picture. |
| 6.0 | Invalid Content | SubpicAnalysisModelingError | 0x60000037 | Modeling sub-picture failed. |
| 6.0 | Invalid Content | nameError | 0x60000038 | Incorrect name. |
| 6.0 | Invalid Content | nameExistError | 0x60000039 | Duplicate name. |
| 6.0 | Invalid Content | faceLibPicImportingError | 0x6000003A | Importing picture into library… |
| 6.0 | Invalid Content | picFormatError | 0x6000003B | Incorrect picture format. |
| 6.0 | Invalid Content | picResolutionInvalidError | 0x6000003C | Incorrect picture resolution. |
| 6.0 | Invalid Content | picSizeExceedError | 0x6000003D | Picture size is too big. |
| 6.0 | Invalid Content | picSizeSmallError | 0x6000003E | Picture size  is too small. |
| 6.0 | Invalid Content | requestMemoryNULL | 0x6000003F | Request memory is null. |
| 6.0 | Invalid Content | tokenTimeout | 0x60000040 | Token timed out. |
| 6.0 | Invalid Content | timeFormatError | 0x60000041 | Incorrect time format. |
| 6.0 | Invalid Content | administratorPasswordError | 0x60000042 | Incorrect administrator password. |
| 6.0 | Invalid Content | thermometryRegionOverstep | 0x60000043 | Thermography region crossed the line. |
| 6.0 | Invalid Content | noEnvTempSensor | 0x60000044 | No temperature sensor. |
| 6.0 | Invalid Content | oversizePupilDistance | 0x60000045 | Interpupilary distance is too great. |
| 6.0 | Invalid Content | badDns | 0x6000004C | Incorrect DNS. |
| 6.0 | Invalid Content | badMTU | 0x6000004D | Incorrect MTU. |
| 6.0 | Invalid Content | badGateway | 0x6000004E | Incorrect gateway. |
| 6.0 | Invalid Content | invalidChannel | 0x6000004F | Analog channel is disabled. |
| 6.0 | Invalid Content | noAudioStream | 0x60000050 | No audio stream. |
| 6.0 | Invalid Content | noRecAudio | 0x60000051 | Audio and video are not enabled. |
| 6.0 | Invalid Content | noAudio | 0x60000052 | Audio is not enabled. |
| 6.0 | Invalid Content | WANNotSupport | 0x60000053 | This function only supports LAN. |
| 6.0 | Invalid Content | importErrorData | 0x60000054 | Incorrect imported message. |
| 6.0 | Invalid Content | SEQConfigNumError | 0x60000055 | Incorrect number of security questions. |
| 6.0 | Invalid Content | ResetErrorNoSEQ | 0x60000056 | Resetting password is not allowed. No security questions are configured for the device. |
| 6.0 | Invalid Content | ResetPasswordIllegal | 0x60000057 | Invalid reset password. |
| 6.0 | Invalid Content | SEQCertificateUnmatch | 0x60000058 | Incorrect answer. |
| 6.0 | Invalid Content | GUIDFileDataUnmatch | 0x60000059 | GUID file mismatch. |
| 6.0 | Invalid Content | illegalVerificationCode | 0x6000005A | Invalid verification code. |
| 6.0 | Invalid Content | lackVerificationCode | 0x6000005B | Verification code in required. |
| 6.0 | Invalid Content | mutexFunction | 0x6000005C | Exclusive error code of smart function. |
| 6.0 | Invalid Content | passwordLenNoMoreThan16 | 0x6000005F | The password length cannot exceed 16. |
| 6.0 | Invalid Content | mismatchedPassword | 0x60000060 | Password mismatch. |
| 6.0 | Invalid Content | loginPasswordError | 0x60000061 | Incorrect login password. |
| 6.0 | Invalid Content | calibPositionError | 0x60000062 | The current calibration position is out of the area monitored by the camera. |
| 6.0 | Invalid Content | deleteError | 0x60000063 | Deleting failed. |
| 6.0 | Invalid Content | sceneIDError | 0x60000064 | NaN |
| 6.0 | Invalid Content | WDRNotDisable | 0x60000065 | Please disable WDR in all channels. |
| 6.0 | Invalid Content | HLCNotDisable | 0x60000066 | Please disable highlight compensation in all channels. |
| 6.0 | Invalid Content | countAreaError | 0x60000067 | NaN |
| 6.0 | Invalid Content | faceContrastNoData | 0x60000068 | No face picture comparison data. |
| 6.0 | Invalid Content | faceLibraryNoData | 0x60000069 | No data found in face picture library. |
| 6.0 | Invalid Content | faceDataModeling | 0x6000006A | Concurrent operation is not supported. The device is modeling pictures. |
| 6.0 | Invalid Content | NoDataForModelingError | 0x6000006B | No modeling data in face picture library. |
| 6.0 | Invalid Content | customFaceLibIDRepeat | 0x6000006C | Duplicate ID of custom face picture library. |
| 6.0 | Invalid Content | customHumanIDRepeat | 0x6000006D | Duplicate ID of custom person. |
| 6.0 | Invalid Content | urlDownloadFail | 0x6000006E | Downloading URL failed. |
| 6.0 | Invalid Content | urlDownloadNotStart | 0x6000006F | URL downloading has not started. |
| 6.0 | Invalid Content | forbiddenIP | 0x60000070 | The IP address is forbidden. |
| 6.0 | Invalid Content | deviceInternalModelingError | 0x60000071 | NaN |
| 6.0 | Invalid Content | faceModelingError | 0x60000072 | NaN |
| 6.0 | Invalid Content | faceGradingModelingError | 0x60000073 | NaN |
| 6.0 | Invalid Content | faceFeatureModelingError | 0x60000074 | NaN |
| 6.0 | Invalid Content | faceAnalyzingModelingError | 0x60000075 | NaN |
| 6.0 | Invalid Content | cfgFileSecretKeyError | 0x60000076 | NaN |
| 6.0 | Invalid Content | CaliberatingError | 0x60000077 | Calibrating... |
| 6.0 | Invalid Content | fileFormatError | 0x60000078 | NaN |
| 6.0 | Invalid Content | fileContentError | 0x60000079 | NaN |
| 6.0 | Invalid Content | alarmInputOccupied | 0x6000007A | NaN |
| 6.0 | Invalid Content | unlockPTZError | 0x6000007B | Invalid operation. Lock the PTZ before saving settings. |
| 6.0 | Invalid Content | streamLimit | 0x6000007C | NaN |
| 6.0 | Invalid Content | streamDescriptionLack | 0x6000007D | NaN |
| 6.0 | Invalid Content | streamDeleteFail | 0x6000007E | NaN |
| 6.0 | Invalid Content | streamNameError | 0x60000080 | NaN |
| 6.0 | Invalid Content | streamNotExisted | 0x60000081 | NaN |
| 6.0 | Invalid Content | PupilDistanceParamError | 0x60000082 | Incorrect interpupilary distance parameter (the shortest interpupilary distance is  greater than the longest). |
| 6.0 | Invalid Content | sameNameOfAlarmLinkage | 0x60000083 | Duplicate alarm linkage name. |
| 6.0 | Invalid Content | sameDefenceAreaNo | 0x60000084 | Duplicate zone No. |
| 6.0 | Invalid Content | DetectionLineOutofDetectionRegion | 0x60000085 | Rule line is out of region. Make sure the rule line is in the blue area. |
| 6.0 | Invalid Content | DetectionRegionError | 0x60000086 | Rule region error. Make sure the rule region is a convex polygon. |
| 6.0 | Invalid Content | DetectionRegionOutOfCountingRegion | 0x60000087 | The rule frame should be in the red counting frame. |
| 6.0 | Invalid Content | PedalAreaError | 0x60000088 | Please place the pedal area in the rule frame. |
| 6.0 | Invalid Content | DetectionAreaABError | 0x60000089 | Please place detection area A and B in the rule frame. |
| 6.0 | Invalid Content | ABRegionCannotIntersect | 0x6000008a | Area A and B cannot overlap. |
| 6.0 | Invalid Content | customHBPIDError | 0x6000008b | Incorrect ID of custom human body picture library. |
| 6.0 | Invalid Content | customHBPIDRepeat | 0x6000008c | Duplicate ID of custom human body picture library. |
| 6.0 | Invalid Content | dataVersionsInHBDLibMismatches | 0x6000008d | Human body picture library database versions mismatch. |
| 6.0 | Invalid Content | invalidHBPID | 0x6000008e | Invalid human body picture PID. |
| 6.0 | Invalid Content | invalidHBDID | 0x6000008f | Invalid human body picture library ID. |
| 6.0 | Invalid Content | humanLibraryError | 0x60000090 | Incorrect human body picture library data. |
| 6.0 | Invalid Content | humanLibraryNumError | 0x60000091 | No more human body picture libraries can be added. |
| 6.0 | Invalid Content | humanImagesNumError | 0x60000092 | No more human body pictures can be added. |
| 6.0 | Invalid Content | noHumanInThePicture | 0x60000093 | Modeling failed. No human body recognized in picture. |
| 6.0 | Invalid Content | incorrectTime Interval | 0x60000094 | Incorrect time interval. |
| 6.0 | Invalid Content | densityLevelCustomNameExist | 0x60000095 | NaN |
| 6.0 | Invalid Content | analysisEnginesNoResourceError | 0x60001000 | No analysis engine. |
| 6.0 | Invalid Content | analysisEnginesUsageExcced | 0x60001001 | Engine is overloaded. |
| 6.0 | Invalid Content | PicAnalysisNoResourceError | 0x60001002 | No analysis engine for secondary picture recognition. |
| 6.0 | Invalid Content | analysisEnginesLoadingError | 0x60001003 | Initializing analysis engine... |
| 6.0 | Invalid Content | analysisEnginesAbnormaError | 0x60001004 | Analysis engine exception. |
| 6.0 | Invalid Content | analysisEnginesFacelibImporting | 0x60001005 | Analysis engine is importing face picture library. |
| 6.0 | Invalid Content | analysisEnginesAssociatedChannel | 0x60001006 | Analysis engines is linked to a channel. |
| 6.0 | Invalid Content | smdEncodingNoResource | 0x60001007 | Not enough SMD encoding resource. |
| 6.0 | Invalid Content | smdDecodingNoResource | 0x60001008 | Not enough SMD decoding resource. |
| 6.0 | Invalid Content | diskError | 0x60001009 | HDD error. |
| 6.0 | Invalid Content | diskFull | 0x6000100a | HDD is full. |
| 6.0 | Invalid Content | facelibDataProcessing | 0x6000100b | Processing face picture library data. |
| 6.0 | Invalid Content | capturePackageFailed | 0x6000100c | Capturing packet failed. |
| 6.0 | Invalid Content | capturePackageProcessing | 0x6000100d | Capturing packet... |
| 6.0 | Invalid Content | noSupportWithPlaybackAbstract | 0x6000100e | This function is not supported. Video synopsis is enabled. |
| 6.0 | Invalid Content | insufficientNetworkBandwidth | 0x6000100f | Not enough network bandwidth. |
| 6.0 | Invalid Content | tapeLibNeedStopArchive | 0x60001010 | Stop filing the tape library first. |
| 6.0 | Invalid Content | identityKeyError | 0x60001011 | Incorrect interaction command. |
| 6.0 | Invalid Content | identityKeyMissing | 0x60001012 | Interaction command is lost. |
| 6.0 | Invalid Content | noSupportWithPersonDensityDetect | 0x60001013 | The function is not supported. People density detection is enabled. |
| 6.0 | Invalid Content | ipcResolutionOverflow | 0x60001014 | IP camera resolution exceeded limit. |
| 6.0 | Invalid Content | ipcBitrateOverflow | 0x60001015 | IP camera bitrate exceeded limit. |
| 6.0 | Invalid Content | tooGreatTimeDifference | 0x60001016 | Time difference between device and server is too big. |
| 6.0 | Invalid Content | noSupportWithPlayback | 0x60001017 | The function is not supported. Playback is enabled. |
| 6.0 | Invalid Content | channelNoSupportWithSMD | 0x60001018 | The function is not supported. Motion detection is enabled. |
| 6.0 | Invalid Content | channelNoSupportWithFD | 0x60001019 | The function is not supported. Face capture is enabled. |
| 6.0 | Invalid Content | illegalPhoneNumber | 0x6000101a | Invalid mobile phone number |
| 6.0 | Invalid Content | illegalCertificateNumber | 0x6000101b | Invalid ID No. |
| 6.0 | Invalid Content | linkedCameraOutLimit | 0x6000101c | Connecting to camera timed out. |
| 6.0 | Invalid Content | achieveMaxChannelLimit | 0x6000101e | No more channels are allowed. |
| 6.0 | Invalid Content | humanMisInfoFilterEnabledChanNumError | 0x6000101f | No more channels can be turned on with the function for discarding the false alarms. |
| 6.0 | Invalid Content | humanEnginesNoResource | 0x60001020 | Not enough resource for human body analysis engine. |
| 6.0 | Invalid Content | taskNumberOverflow | 0x60001021 | No more tasks can be added. |
| 6.0 | Invalid Content | collisionTimeOverflow | 0x60001022 | No more comparison duration can be configured. |
| 6.0 | Invalid Content | invalidTaskID | 0x60001023 | Invalid task ID. |
| 6.0 | Invalid Content | eventNotSupport | 0x60001024 | Event subscription is not supported. |
| 6.0 | Invalid Content | passwordInvalid | 0x60001025 | Invalid password format. |
| 6.0 | Invalid Content | UserNameInvalid | 0x60001026 | Invalid user name format. |
| 6.0 | Invalid Content | tooSmallQuota | 0x60001027 | Not enough quota. |
| 6.0 | Invalid Content | emailFormatError | 0x60001028 | Incorrect email format. |
| 6.0 | Invalid Content | securityCodeFormatError | 0x60001029 | Incorrect verification code format. |
| 6.0 | Invalid Content | pdSpaceTooSmall | 0x6000102a | Not enough HDD space in the array. |
| 6.0 | Invalid Content | pdNumTooBig | 0x6000102b | The number of HDDs in the array cannot exceed half of the total number of HDDs. |
| 6.0 | Invalid Content | usbIsFull | 0x6000102c | USB flash drive is full. |
| 6.0 | Invalid Content | detectRangeInvalid | 0x6000102d | Invalid detection area. |
| 6.0 | Invalid Content | channelCapturePictureFailure | 0x6000102e | Channel capturing failed. |
| 6.0 | Invalid Content | onlySupportByIVMS | 0x6000102f | Support platform operation only. |
| 6.0 | Invalid Content | uploadTooLargeFile | 0x60001030 | The size of file is too big. |
| 6.0 | Invalid Content | uploadTooSmallFile | 0x60001031 | The size of file is too small. |
| 6.0 | Invalid Content | certificatesNotCreate | 0x60001032 | Enabling the function failed. Create a certificate on HTTP page and try again. |
| 6.0 | Invalid Content | invalidIotProtocolType | 0x60001033 | Invalid IoT protocol type. |
| 6.0 | Invalid Content | invalidEZVIZSecretKey | 0x60001034 | Invalid EZVIZ verification code. |
| 6.0 | Invalid Content | tapeNotInDevice | 0x60001035 | The tape with the file is not in the current tape library. Please insert tape. |
| 6.0 | Invalid Content | noRestoreSpace | 0x60001036 | No unfreeze space in the device. Please create archive volume first. |
| 6.0 | Invalid Content | surroundModeNumOverLimit | 0x60001037 | No more channels are allowed in environment mode. |
| 6.0 | Invalid Content | panelModeNotConfig | 0x60001038 | No intelligent panels configured. |
| 6.0 | Invalid Content | vcachannoresource | 0x60001039 | No more smart channel resources. |
| 6.0 | Invalid Content | noEnoughDecodeResource | 0x6000103a | Not enough decoding devices. |
| 6.0 | Invalid Content | fieldCodingNotSupport | 0x6000103b | Field encoding is not supported. |
| 6.0 | Invalid Content | channelResolutionNoSupport | 0x6000103c | Resolution is not supported for the channel. |
| 6.0 | Invalid Content | channelCompressionNoSupport | 0x6000103d | Encoding format is not supported. |
| 6.0 | Invalid Content | illegalRuleID | 0x6000103e | Invalid rule ID. |
| 6.0 | Invalid Content | polygonError | 0x6000103f | Polygon does not meet requirement. |
| 6.0 | Invalid Content | ruleParamError | 0x60001040 | Invalid rule parameters. |
| 6.0 | Invalid Content | safetyHelmetNoResource | 0x60001041 | Not enough hard hat detection resource. |
| 6.0 | Invalid Content | needDoubleVerification | 0x60001042 | Double authentication required. |
| 6.0 | Invalid Content | noDoubleVerificationUser | 0x60001043 | No user for double authentication. |
| 6.0 | Invalid Content | timeSpanNumOverLimit | 0x60001044 | Number of time ranges exceeded limit. |
| 6.0 | Invalid Content | channelNumOverLimit | 0x60001045 | Number of channels exceeded limit. |
| 6.0 | Invalid Content | noSearchIDResource | 0x60001046 | Not enough searchID resource of searching by page. |
| 6.0 | Invalid Content | oneKeyExport | 0x60001047 | Exporting... Please try again later. |
| 6.0 | Invalid Content | cityManagementEnginesNoResource | 0x60001048 | Not enough algorithm engine resource for urban management. |
| 6.0 | Invalid Content | situationAnalysisEnginesNoResource | 0x60001049 | Not enough  engine resource for trend analysis. |
| 6.0 | Invalid Content | channelNoSupportWithSafetyHelmet | 0x6000104a | The function is not supported. Hard hat detection is enabled. |
| 6.0 | Invalid Content | noSupportWithSMDOrSCD | 0x6000104b | The function is not supported. SMD/SCD detection is enabled. |
| 6.0 | Invalid Content | noSupportWithFD | 0x6000104c | The function is not supported. Face capture is enabled. |
| 6.0 | Invalid Content | FDEnginesNoResource | 0x6000104d | Not enough engine resource for face capture. |
| 6.0 | Invalid Content | oneKeyRemove | 0x6000104e | Deleting… Please try again later. |
| 6.0 | Invalid Content | facePipBackgroundChannelOverflow | 0x6000104f | Number of face picture picture-in-picture background channel exceeded limit. |
| 6.0 | Invalid Content | channelNoSupportWithFaceContrast | 0x60001050 | The function is not supported. Face picture comparison is enabled. |
| 6.0 | Invalid Content | noSupportDeleteStrangerLib | 0x60001051 | Deleting stranger library is not allowed. |
| 6.0 | Invalid Content | noSupportCreateStrangerLib | 0x60001052 | Creating stranger library is not allowed. |
| 6.0 | Invalid Content | behaviorAnalysisRuleInfoError | 0x60001053 | Invalid parameters for abnormal event detection rule. |
| 6.0 | Invalid Content | safetyHelmetParamError | 0x60001054 | Invalid parameters for not wearing hard hat detection. |
| 6.0 | Invalid Content | IllegalDatasetName | 0x60001055 | Invalid data set name. |
| 6.0 | Invalid Content | IllegalDatasetNameLength | 0x60001056 | Invalid data set name length. |
| 6.0 | Invalid Content | IllegalDatasetDescriptionLength | 0x60001057 | Invalid length for data set description. |
| 6.0 | Invalid Content | AbnormalDatasetPackageSize | 0x60001058 | Data set package size exception. |
| 6.0 | Invalid Content | IllegalFileOrFolderNameFormat | 0x60001059 | Invalid file or folder name format. |
| 6.0 | Invalid Content | IllegalFileOrFolderLength | 0x6000105a | Invalid file or folder name length. |
| 6.0 | Invalid Content | IllegalFileOrFolderPathLength | 0x6000105b | Invalid file or folder path length. |
| 6.0 | Invalid Content | IllegalModelName | 0x6000105c | Invalid model name format. |
| 6.0 | Invalid Content | IllegalModelNameLength | 0x6000105d | Invalid model name length. |
| 6.0 | Invalid Content | ModelAlreadyExists | 0x6000105e | Model already exists. |
| 6.0 | Invalid Content | IllegalPageNumber | 0x6000105f | Invalid page number. |
| 6.0 | Invalid Content | IllegalPageSize | 0x60001060 | Invalid searching quantity on a single page. |
| 6.0 | Invalid Content | IllegalModelDescriptionInfoLength | 0x60001061 | Invalid model description information length. |
| 6.0 | Invalid Content | UserUUidEmpty | 0x60001062 | UserUuid is required. |
| 6.0 | Invalid Content | IllegalModelVersionNameFormat | 0x60001063 | Invalid model version name format. |
| 6.0 | Invalid Content | IllegalModelVersionNameLength | 0x60001064 | Invalid length for model version name. |
| 6.0 | Invalid Content | ModelVersionAlreadyExists | 0x60001065 | Model version already exists. |
| 6.0 | Invalid Content | IllegalModelVersionDescriptionInfo | 0x60001066 | Invalid model version description. |
| 6.0 | Invalid Content | ModelNoExist | 0x60001067 | Model does not exist. |
| 6.0 | Invalid Content | ModelVersionNoExist | 0x60001068 | Model version does not exist. |
| 6.0 | Invalid Content | TaskNoExit | 0x60001069 | Task does not exist. |
| 6.0 | Invalid Content | IllegalTaskOperation | 0x6000106a | Invalid task operation. |
| 6.0 | Invalid Content | TaskNameAlreadyExist | 0x6000106b | Duplicate task name. |
| 6.0 | Invalid Content | TaskCreateFail | 0x6000106c | Creating task failed. |
| 6.0 | Invalid Content | TaskRestartFail | 0x6000106d | Restarting task failed. |
| 6.0 | Invalid Content | TaskStopFail | 0x6000106e | Stopping task failed. |
| 6.0 | Invalid Content | TaskDeleteFail | 0x6000106f | Deleting task failed. |
| 6.0 | Invalid Content | ImageNotExist | 0x60001070 | Mirror does not exist. |
| 6.0 | Invalid Content | ImageAlreadyExist | 0x60001071 | Mirror already exists. |
| 6.0 | Invalid Content | IllegalImageTagWith: | 0x60001072 | Invalid mirror tag. Use colon(:) to separate warehouse name and tag. |
| 6.0 | Invalid Content | IllegalImageTagWith/ | 0x60001073 | Invalid mirror tag. Use slash(/) to separate user name space and actual mirror name. |
| 6.0 | Invalid Content | ImageTagNotExist | 0x60001074 | Mirror tag does not exist. |
| 6.0 | Invalid Content | ImageTagAlreadyExist | 0x60001075 | The tag of the same user already exists. |
| 6.0 | Invalid Content | IllegalTagNameParameter | 0x60001076 | Invalid tag name parameter. |
| 6.0 | Invalid Content | OneChannelOnlyCanBindOneEngine | 0x60001077 | Binding failed. Only one engine can be bound. |
| 6.0 | Invalid Content | AreaConfigurationError | 0x60001078 | Incorrect area configuration. Disable the person/vehicle motion detection and try again. |
| 6.0 | Invalid Content | engineTypeMismatch | 0x60001079 | Engine type mismatched. |
| 6.0 | Invalid Content | badUpgradePackage | 0x6000107A | Invalid upgrade package. |
| 6.0 | Invalid Content | imagePositionError | 0x6000107B | Incorrect picture location. |
| 6.0 | Invalid Content | textPositionError | 0x6000107C | Incorrect text location. |
| 6.0 | Invalid Content | certDismatchCertReq | 0x6000107D | Certificate mismatch. Requested certificate and imported certificate mismatch. |
| 6.0 | Invalid Content | timeRangeOverlap | 0x6000107F | Time periods overlapped. |
| 6.0 | Invalid Content | IllegalDatasetName | 0x60001110 | Network camera capture is offline or does not exist. |
| 6.0 | Invalid Content | CloudServiceNotEnabledOrAbnotmal | 0x60001111 | Cloud service is disabled or abnormal. |
| 6.0 | Invalid Content | TaskIDDuplication | 0x60001112 | Duplicate task ID. |
| 6.0 | Invalid Content | InsufficientResourcesOfAIRetrievalEquipment | 0x60001113 | Not enough AI search device resource. |
| 6.0 | Invalid Content | AppAlreadyExists | 0x60001120 | Application already exists. |
| 6.0 | Invalid Content | AppDownloadFailed | 0x60001121 | Downloading application failed. |
| 6.0 | Invalid Content | AppDecryptionFailed | 0x60001122 | Decryption and unpacking application failed. |
| 6.0 | Invalid Content | DevicParsingAppAlgorithmConfigurationFailed | 0x60001123 | Parsing application package algorithm configuration failed. |
| 6.0 | Invalid Content | DifferentialUUIDMismatch | 0x60001124 | UUID of differential package mismatch. |
| 6.0 | Invalid Content | ScreenModeAndSplitScreensNotMatch | 0x60001130 | Viewing mode and window division number mismatch. |
| 6.0 | Invalid Content | TransitionUseEmmc | 0x60002000 | Starting device failed. The EMMC is overused. |
| 6.0 | Invalid Content | AdaptiveStreamNotEnabled | 0x60002001 | The stream self-adaptive function is not enabled. |
| 6.0 | Invalid Content | AdaptiveStreamAndVariableBitrateEnabled | 0x60002002 | Stream self-adaptive and variable bitrate function cannot be enabled at the same time. |
| 6.0 | Invalid Content | unclosedFaceSnapError | 0x60002003 | Operation failed. Disable face capture first. |
| 6.0 | Invalid Content | undesirableFaceSnapError | 0x60002004 | Operation failed. The scene is not suitable for face capture. |
| 6.0 | Invalid Content | unopenedFaceSnapError | 0x60002005 | Operation failed. Enable face capture first. |
| 6.0 | Invalid Content | sceneDurationTimeLessThanIntervalTime | 0x60002006 | Dwell time should be longer than detection cycle. |
| 6.0 | Invalid Content | localSIPPortConflictError | 0x60002007 | Local SIP port numbers of  two camera channels can not be the same. |
| 6.0 | Invalid Content | vodeoCodingIDConflictError | 0x60002008 | For one platform, Video Encoding IDs of two camera channels can not be the same. |
| 6.0 | Invalid Content | SIPUserNameConflictError | 0x60002009 | For one platform, SIP user names of two camera channels can not be the same. |
| 6.0 | Invalid Content | SIPAuthIDConflictError | 0x6000200A | For one platform, SIP authentication IDs of two camera channels can not be the same. |
| 6.0 | Invalid Content | labelDExceedError | 0x6000200B | Number of tag ID exceeded limit. |
| 6.0 | Invalid Content | labelTypeError | 0x6000200C | Incorrect tag type. |
| 6.0 | Invalid Content | labelFullError | 0x6000200D | No more tag can be added. |
| 6.0 | Invalid Content | labelDisabledError | 0x6000200E | Tag is not enabled. |
| 6.0 | Invalid Content | similarityLessSetValue | 0x6000201F | Inbound similarity threshold should be smaller than the threshold of succeeded face picture comparison. |
| 6.0 | Invalid Content | illegalPassword | 0x60002020 | Invalid password. Password cannot contain user name. |
| 6.0 | Invalid Content | incorrectVideoORAudioID | 0x60002021 | Incorrect video channel ID or audio output channel ID. |
| 6.0 | Invalid Content | repetitionTimeOverMaximum | 0x60002022 | Deduplication time should not exceed the maximum value. |
| 6.0 | Invalid Content | noSafetyHelmetRegion | 0x60002023 | Hard hat detection area is not configured (if users save their settings without configuring the arming area, they should be prompted to configure one). |
| 6.0 | Invalid Content | unclosedSafetyHelmet | 0x60002024 | Hard hat detection is enabled (If users save their settings after deleting the arming area, they should be prompted to disable hard hat detection first and then delete the arming area). |
| 6.0 | Invalid Content | startTimeShouldBeEarlierThanEndTime | 0x60002025 | Start time must be earlier than end time. |
| 6.0 | Invalid Content | customIDIllegal | 0x60002026 | Certificate ID includes invalid characters. It only supports letters and digits. |
| 6.0 | Invalid Content | customIDTooLong | 0x60002027 | Certificate ID is too long. It only supports 1 to 64 characters. |
| 6.0 | Invalid Content | certificateExceedMaxNum | 0x60002028 | Number of certificates exceeded limit. Up to 16 certificates are allowed. |
| 6.0 | Invalid Content | certificateFormatIllegal | 0x60002029 | Certificate format is not supported. Only formats in PEM, DER, and PKCS#12 are supported. |
| 6.0 | Invalid Content | InvalidCertificate | 0x6000202A | Invalid certificate. |
| 6.0 | Invalid Content | certificateExisted | 0x6000202B | A same certificate already exists. |
| 6.0 | Invalid Content | width/heightRatioOfPictureError | 0x6000202C | The width/height ratio of the uploaded picture should be in the range from 1:2 to 2:1. |
| 6.0 | Invalid Content | detectionAreaOutsideTheLimitedArea | 0x6000202D | Detection area is out of the limited area. |
| 6.0 | Invalid Content | PTZNotInitialized | 0x6000202E | PTZ is not initialized. |
| 6.0 | Invalid Content | PTZMoving | 0x6000202F | PTZ is on. |
| 6.0 | Invalid Content | PTZLocked | 0x60002030 | PTZ is locked. |
| 6.0 | Invalid Content | advancedParametersError | 0x60002031 | Auto-switch interval in advanced parameters cannot be shorter than parking tolerance for illegal parking detection in speed dome rule settings. |
| 6.0 | Invalid Content | intelligentMutexWithHighFrames | 0x60002032 | Disable multi-target-type detection, face capture, smart event, road traffic, manual tracking and smart tracking to enable high frame rate (50 fps or 60 fps). Otherwise the function will not take effect. |
| 6.0 | Invalid Content | theFunctionMutexWithHighFrames | 0x60002033 | Adjust the frame rate to 25 fps (PAL) or 30 fps (NTSC) and below to enable the function. Otherwise the function will not take effect. |
| 6.0 | Invalid Content | LicenseKeyNotMatchModel | 0x60002040 | License Key and model package mismatch. |
| 6.0 | Invalid Content | confAudioStreamNull | 0x60005000 | Conference audio encoding compression parameter is required. |
| 6.0 | Invalid Content | confVideoStreamNull | 0x60005001 | Conference video encoding compression parameter is required. |
| 6.0 | Invalid Content | audioMixMaxNum | 0x60005002 | Number of audio mixing terminals exceeded limit. |
| 6.0 | Invalid Content | resolutionError | 0x60005003 | Invalid resolution. |
| 6.0 | Invalid Content | crcError | 0x60005004 | CRC verification error. |
| 6.0 | Invalid Content | screenTypeError | 0x60005005 | Incorrect screen type. |
| 6.0 | Invalid Content | invalidVlanId | 0x60005006 | Invalid VLANID. |
| 6.0 | Invalid Content | invalidVlanPortType | 0x60005007 | Invalid port VLAN type. |
| 6.0 | Invalid Content | invalidVlanPvid | 0x60005008 | Invalid PVID. |
| 6.0 | Invalid Content | diffAggrgroupPortSpeed | 0x60005009 | Port speed of aggregation groups mismatch. |
| 6.0 | Invalid Content | diffAggrgroupPortDuplex | 0x6000500a | Port duplex of aggregation groups mismatch. |
| 6.0 | Invalid Content | diffAggrgroupPortPause | 0x6000500b | Port flow control of aggregation groups mismatch. |
| 6.0 | Invalid Content | diffAggrgroupPortPri | 0x6000500c | Port priority of aggregation groups mismatch. |
| 6.0 | Invalid Content | diffAggrgroupPortVlan | 0x6000500d | Port VLAN of aggregation groups mismatch. |
| 6.0 | Invalid Content | invalidDistancePortId | 0x6000500e | Invalid long range port No. |
| 6.0 | Invalid Content | invalidPortPri | 0x6000500f | Invalid port priority. |
| 6.0 | Invalid Content | invalidPoePortId | 0x60005010 | Invalid POE port ID. |
| 6.0 | Invalid Content | invalidPortSpeed | 0x60005011 | Invalid speed configuration parameter. |
| 6.0 | Invalid Content | invalidPortId | 0x60005012 | Invalid port ID. |
| 6.0 | Invalid Content | importEmptyFile | 0x60005013 | Imported file is empty. |
| 6.0 | Invalid Content | tooLargeImportFile | 0x60005014 | Imported file is too large. |
| 6.0 | Invalid Content | netGateInvalid | 0x60005015 | Invalid gateway address. |
| 6.0 | Invalid Content | pVidNotExistList | 0x60005016 | PVID is not in the list. |
| 6.0 | Invalid Content | wirelessSSIDError | 0x60005017 | Wireless SSID parameter error. |
| 6.0 | Invalid Content | wirelessCountryCodeError | 0x60005018 | Wireless county code parameter error. |
| 6.0 | Invalid Content | wirelessModeError | 0x60005019 | Wireless pattern parameter error. |
| 6.0 | Invalid Content | wirelessBandWidthError | 0x6000501a | Wireless bandwidth parameter error. |
| 6.0 | Invalid Content | wirelessChannelError | 0x6000501b | Wireless communication channel parameter error. |
| 6.0 | Invalid Content | wirelessSendPowerError | 0x6000501c | Wireless transmitting power parameter error. |
| 6.0 | Invalid Content | wirelessSecurityModeError | 0x6000501d | Wireless security mode parameter error. |
| 6.0 | Invalid Content | wirelessAuthKeyError | 0x6000501e | Wireless authentication key parameter error. |
| 6.0 | Invalid Content | wirelessWorkModeError | 0x6000501f | Wireless working scene parameter error. |
| 6.0 | Invalid Content | wirelessDeviceModeError | 0x60005020 | Wireless device mode parameter error. |
| 6.0 | Invalid Content | releaseNameillegal | 0x60005021 | Invalid publishing name. |
| 6.0 | Invalid Content | rePublishingPleaseWait | 0x60005022 | Publishing again, please wait… |
| 6.0 | Invalid Content | containerScheduleNoEffectiveTime | 0x60005023 | No effective time for default video schedule. |
| 6.0 | Invalid Content | unPublishingPleaseWait | 0x60005024 | Canceling publishing, please wait... |
| 6.0 | Invalid Content | publishingUnableToDeleteRealeaseRecord | 0x60005025 | Publish record cannot be deleted. Publishing... |
| 6.0 | Invalid Content | built-inMaterialIsUsed | 0x60005026 | Internal material has been used. |
| 6.0 | Invalid Content | DuplicateNameWithBuilt-inMaterial | 0x60005027 | Duplicate name with internal material. |
| 6.0 | Invalid Content | UsernameCannotContainChinese | 0x60005028 | User name is Chinese. |
| 6.0 | Invalid Content | repetitiveMaterialsExceedsLimitInTemplate | 0x60005029 | Number of duplicate material in template exceeded limit. |
| 6.0 | Invalid Content | nonRepetitiveMaterialsExceedsLimitInTemplate | 0x6000502a | Number of unduplicated materials in template program exceeded limit. |
| 6.0 | Invalid Content | templateNameError | 0x6000502b | Invalid template name. |
| 6.0 | Invalid Content | templateNameLenError | 0x6000502c | Invalid template name length. |
| 6.0 | Invalid Content | illegalTemplatePageName | 0x6000502d | Invalid template page name. |
| 6.0 | Invalid Content | illegalTemplatePageNameLength | 0x6000502e | Invalid template page name length. |
| 6.0 | Invalid Content | templatePageSwitchingEffectIsNotSupported | 0x6000502f | Switching effect of template page is not supported. |
| 6.0 | Invalid Content | windowsExceedsLimitInTemplatePage | 0x60005030 | Number of windows in template program page exceeded limit. |
| 6.0 | Invalid Content | windowLayerNumberInTemplatePage | 0x60005031 | Invalid window layer number in template page. |
| 6.0 | Invalid Content | duplicateWindowLayerNumberInTemplatePage | 0x60005032 | Duplicate window layer number in template page. |
| 6.0 | Invalid Content | wrongWindowPositionOrSizeInTemplatePage | 0x60005033 | Incorrect window position or size on the template page. |
| 6.0 | Invalid Content | windowMaterialTypeIsInconsistentInTemplatePage | 0x60005034 | The window material type on the template page mismatch. |
| 6.0 | Invalid Content | windowMaterialsExceedsLimitInTemplatePage | 0x60005035 | The window material number of the template page exceeded limit. |
| 6.0 | Invalid Content | windowMaterialNotExistInTemplatePage | 0x60005036 | The window material of the template page does not exist. |
| 6.0 | Invalid Content | windowMaterialNoAccessIInTemplatePage | 0x60005037 | No window material access permission on the template page. |
| 6.0 | Invalid Content | wndowMaterialPlaybackEffectNotSupportedInTemplatePage | 0x60005038 | The play effect of the window material on the template page is not supported. |
| 6.0 | Invalid Content | materialPlaybackTimeNotInValidRangeInTemplatePage | 0x60005039 | Invalid play time of the material on the template page. |
| 6.0 | Invalid Content | templatePageTimeIllegalInTemplatePage | 0x6000503a | Invalid template page time. |
| 6.0 | Invalid Content | inputBoardsInDifferentNetworkAreasCannotBeSpliced | 0x6000503b | Input boards of different network areas cannot be spliced. |
| 6.0 | Invalid Content | SplicingSourceOfDifferentNetworkAreasCannotBeOnTheWall | 0x6000503c | Splicing sources of different network areas cannot be displayed on the video wall. |
| 6.0 | Invalid Content | OutputBoardsThatAreBoundToTheTVWallCannot ModifyTheNetworkArea | 0x6000503d | The network area of the output board linked to the video wall cannot be edited. |
| 6.0 | Invalid Content | defaultNetworkZonecannotBeDeleted | 0x6000503e | Deleting failed. The default network area cannot be deleted. |
| 6.0 | Invalid Content | userNameRepetitive | 0x6000503f | Duplicate user name. |
| 6.0 | Invalid Content | Non-emptyAreaCannotBeDeleted | 0x60005040 | Deleting failed. The area is occupied. |
| 6.0 | Invalid Content | LEDAreaCannotAllowBaseMapRoaming | 0x60005041 | Background picture roaming is not allowed in the LED area. |
| 6.0 | Invalid Content | snmpCommunityHasCreated | 0x60005042 | The community name already exists. |
| 6.0 | Invalid Content | snmpCommunityReachLimit | 0x60005043 | Maximum number of community names reached. |
| 6.0 | Invalid Content | trapHostHasReachLimit | 0x60005044 | Maximum number of target trap hosts reached. |
| 6.0 | Invalid Content | trapHostHasCreated | 0x60005045 | The target trap host already exists. |
| 6.0 | Invalid Content | stpSmallBridgePriority | 0x60005046 | The STP bridge priority is too low. |
| 6.0 | Invalid Content | stpLargeBridgePriority | 0x60005047 | The STP bridge priority is too high. |
| 6.0 | Invalid Content | stpBridgePriorityNotMultipleOf4096 | 0x60005048 | The stepping of the STP bridge priority is not 4096. |
| 6.0 | Invalid Content | stpSmallMaxAge | 0x60005049 | Maximum generating time of STP message is less than the min. |
| 6.0 | Invalid Content | stpLargeMaxAge | 0x6000505a | Maximum generating time of STP message is larger than the max. |
| 6.0 | Invalid Content | stpSmallForwardDealy | 0x6000505b | The forwarding delay time is less than the minimum value. |
| 6.0 | Invalid Content | stpLargeForwardDealy | 0x6000505c | The forwarding delay time is more than the maximum value. |
| 6.0 | Invalid Content | stpForwardDelayAndMaxAgeAreInconsistent | 0x6000505d | The forwarding delay time and maximum session idle time conflict. |
| 6.0 | Invalid Content | stpHelloTimeAndMaxAgeAreInconsistent | 0x6000505e | The session time and maximum session idle time conflict. |
| 6.0 | Invalid Content | stpSmallPortPriority | 0x6000505f | The STP port priority is too low. |
| 6.0 | Invalid Content | stpLargePortPriority | 0x60005060 | The STP port priority is too high. |
| 6.0 | Invalid Content | stpPortPriorityNotMultpleOf16 | 0x60005061 | The stepping of the STP port priority is not 16. |
| 6.0 | Invalid Content | mainNodeAndSubNodeIPConflict | 0x60005062 | IP addresses of master and sub nodes conflict. |
| 6.0 | Invalid Content | limitSIPLineNumberBelowUsed | 0x60005063 | Maximum number of channels is less than the number of channels where the SIP service is enabled. |
| 6.0 | Invalid Content | conferenceRegisterSIPPasswordNull | 0x60005064 | Conference registration SIP password is required. |
| 6.0 | Invalid Content | cannotModSingleAudioInRelateOutputChanOrEnabled | 0x60005065 | Editing only the linked output channel No. of audio input or linking settings is not allowed. |
| 6.0 | Invalid Content | cannotCfgDifferentAudioInRelateOutputChanOrEnabled | 0x60005066 | Configuring different linked output channel No. of audio input or linking settings is not allowed. |
| 6.0 | Invalid Content | fileNameIncorrect | 0x60005067 | Incorrect file name. |
| 6.0 | Invalid Content | ipAddrConflictWithDev | 0x60005068 | The set IP address and device IP conflict. |
| 6.0 | Invalid Content | onlineMembersIsFullCallFails | 0x60005069 | Calling failed. Maximum number of online users reached. |
| 6.0 | Invalid Content | fileFormatConversionFailure | 0x6000506a | Converting the file format failed. |
| 6.0 | Invalid Content | checkMaterialIsWrong | 0x6000506b | Incorrect verification material. |
| 6.0 | Invalid Content | illegalPortMapping | 0x6000506c | Invalid port mapping. |
| 6.0 | Invalid Content | outputNotSupportVideoWallResolution | 0x6000506d | The output does not support the resolution of the video wall. |
| 6.0 | Invalid Content | videoWallOutputNotSupportThisResolution | 0x6000506e | The video wall has the output(s) which do not support the resolution. |
| 6.0 | Invalid Content | timeOverlap | 0x60006000 | Time periods overlap. |
| 6.0 | Invalid Content | holidayPlanOverlap | 0x60006001 | Holiday schedules overlap. |
| 6.0 | Invalid Content | cardNoNotSort | 0x60006002 | Card No. is not sorted. |
| 6.0 | Invalid Content | cardNoNotExist | 0x60006003 | Card No. is not found |
| 6.0 | Invalid Content | illegalCardNo | 0x60006004 | Card No. error. |
| 6.0 | Invalid Content | zoneAlarm | 0x60006005 | The zone is armed (the parameters cannot be edited). |
| 6.0 | Invalid Content | zoneOperationNotSupport | 0x60006006 | The zone does not support the operation. |
| 6.0 | Invalid Content | interlockAntiConflict | 0x60006007 | Multi-door interlocking and anti-passback cannot be configured at the same time. |
| 6.0 | Invalid Content | deviceCardFull | 0x60006008 | No more cards are allowed. |
| 6.0 | Invalid Content | holidayGroupDownload | 0x60006009 | Applying the holiday group failed. |
| 6.0 | Invalid Content | localControlOff | 0x6000600a | The distributed controller is offline. |
| 6.0 | Invalid Content | localControlNotAdd | 0x6000600b | The distributed controller is not added. |
| 6.0 | Invalid Content | localControlHasAdd | 0x6000600c | The distributed controller is added. |
| 6.0 | Invalid Content | localControlDoorNoConflict | 0x6000600d | Added distributed controller's door No. conflict. |
| 6.0 | Invalid Content | localControlCommunicationFail | 0x6000600e | Communicating with the distributed controller failed. |
| 6.0 | Invalid Content | operObjectNotExist | 0x6000600f | The object does not exist. |
| 6.0 | Invalid Content | localControlOverLimit | 0x60006010 | No more distributed controllers are allowed for the device. |
| 6.0 | Invalid Content | doorOverLimit | 0x60006011 | No more access control points are allowed for the device. |
| 6.0 | Invalid Content | alarmOverLimit | 0x60006012 | No more alarm inputs/outputs are allowed for the device. |
| 6.0 | Invalid Content | localControlAddressAndTypeNotConform | 0x60006013 | The IP address of the distributed controller does not match with its type. |
| 6.0 | Invalid Content | supportOneMoreCard | 0x60006014 | One person can only have one card. |
| 6.0 | Invalid Content | deleteNoExistFace | 0x60006015 | The face picture has already been deleted. |
| 6.0 | Invalid Content | doorSpecialPasswordRepeat | 0x60006016 | It cannot be the same as the door duress code, the super password, or the dismiss code. |
| 6.0 | Invalid Content | authCodeRepeat | 0x60006017 | It cannot be the same as the device authentication code. |
| 6.0 | Invalid Content | deployExceedMax | 0x60006018 | The number of arming connections exceeded limit. |
| 6.0 | Invalid Content | errorFingerID | 0x60006019 | Incorrect finger ID. |
| 6.0 | Invalid Content | errorFingerPrintType | 0x6000601a | Incorrect fingerprint type. |
| 6.0 | Invalid Content | fingerPrintNotLinkEmployeeNoOrCardNo | 0x6000601b | The fingerprint is not linked to any employee No. or card No. |
| 6.0 | Invalid Content | fingerPrintAlreadyExist | 0x6000601c | The fingerprint exits. |
| 6.0 | Invalid Content | fingerPrintModuleNoNeedConfigure | 0x6000601d | Configuring the fingerprint module is not required. |
| 6.0 | Invalid Content | notSupportDelFPByID | 0x6000601e | Deleting fingerprints by finger IDs is not supported by the card reader. |
| 6.0 | Invalid Content | employeeNoNotExist | 0x6000601f | The employee No. does not exist. |
| 6.0 | Invalid Content | employeeNoAlreadyExist | 0x60006020 | The employee No. already exists. |
| 6.0 | Invalid Content | temporaryPasswordError | 0x60006021 | No temporary passwords can be added. |
| 6.0 | Invalid Content | lateWarningError | 0x60006022 | No more late-return notifications can be added. |
| 6.0 | Invalid Content | deleteLastSmartLock | 0x60006023 | The last smart lock has been deleted. |
| 6.0 | Invalid Content | deleteLastSmartLockError | 0x60006024 | Deleting the last smart lock failed. Format the network. |
| 6.0 | Invalid Content | detectorAlreadyRegistered | 0x60006025 | The detector is already registered. |
| 6.0 | Invalid Content | detectorRelateFull | 0x60006026 | No more detectors can be linked to the smart lock. |
| 6.0 | Invalid Content | detectorOffline | 0x60006027 | Detector disconnected. |
| 6.0 | Invalid Content | detectorRegisterFull | 0x60006028 | No more detectors can be registered to the device. |
| 6.0 | Invalid Content | notSupportCharacter | 0x60006029 | Invalid characters. |
| 6.0 | Invalid Content | remoteDoorPasswordError | 0x6000602a | Incorrect password for remotely door opening. |
| 6.0 | Invalid Content | smartLockReturnError | 0x6000602b | No response is returned by the smart lcok. |
| 6.0 | Invalid Content | smartLockNoResponse | 0x6000602c | No data returned from the smart lock. |
| 6.0 | Invalid Content | smartLockNotExist | 0x6000602d | The smart lock does not exist. |
| 6.0 | Invalid Content | smartLockRegisterFull | 0x6000602e | No more smart locks can be registered. |
| 6.0 | Invalid Content | remoteDoorFunctionDisable | 0x6000602f | Local function of remotely door opening is not enabled. |
| 6.0 | Invalid Content | remoteDoorTimeStampError | 0x60006030 | Error occurred when comparing remotely door opening timestamps. |
| 6.0 | Invalid Content | needFormatNetParams | 0x60006031 | Please format the network parameters. |
| 6.0 | Invalid Content | smartLockAlreadyResgistered | 0x60006032 | The smart lock is already registered. |
| 6.0 | Invalid Content | cardNoAlreadyExist | 0x60006033 | Card No. already exists. |
| 6.0 | Invalid Content | fingerPrintDataLenZero | 0x60006034 | Data length of the fingerprint is 0. |
| 6.0 | Invalid Content | illegalCardReaderNo | 0x60006035 | Incorrect card reader No. |
| 6.0 | Invalid Content | illegalEmployeeNo | 0x60006036 | Incorrect employee No. |
| 6.0 | Invalid Content | illegalLeaderCardValue | 0x60006037 | Invalid first authentication value. |
| 6.0 | Invalid Content | cardReaderOffline | 0x60006038 | Configuration failed. The card reader is offline. |
| 6.0 | Invalid Content | adminPasswordNotConfig | 0x60006039 | No admin password configured. |
| 6.0 | Invalid Content | pictureNotExist | 0x6000603a | No pictures. |
| 6.0 | Invalid Content | pupilDistanceTooSmall | 0x6000603b | Pupillary distance too short. |
| 6.0 | Invalid Content | faceDataLenShort | 0x6000603c | Data length of the face picture is smaller than 1 K. |
| 6.0 | Invalid Content | pictureInfoCheckFailure | 0x6000603d | Verifying picture information failed. |
| 6.0 | Invalid Content | faceScoreFailure | 0x6000603e | Rating the face picture failed. |
| 6.0 | Invalid Content | QRCodeGenFailure | 0x6000603f | Converting to the QR code picture failed. |
| 6.0 | Invalid Content | fingerprintFull | 0x60006040 | No more fingerprints can be added. |
| 6.0 | Invalid Content | attendanceTimeInvalid | 0x60006041 | Attendance check period conflict. |
| 6.0 | Invalid Content | bondMacAddressNotMatch | 0x60006042 | The MAC address does not match with the user. |
| 6.0 | Invalid Content | bondIpAddressNotMatch | 0x60006043 | The IP address does not match with the user. |
| 6.0 | Invalid Content | adminUserNotAllowedModify | 0x60006044 | Editing admin information is not allowed. |
| 6.0 | Invalid Content | confirmPasswordError | 0x60006045 | Incorrect password when editing user information. |
| 6.0 | Invalid Content | passwordMustContainMorethan2Types | 0x60006046 | The password must contain two types of characters, including digits, upper-case letters, lower-case letters, and special characters. |
| 6.0 | Invalid Content | beyondTimeRangeLimit | 0x60006047 | The time for time sync is not within the time range supported by the device. |
| 6.0 | Invalid Content | endtimeEarlierThanBegintime | 0x60006048 | The start time should be earlier than the end time. |
| 6.0 | Invalid Content | materialNumberIsOver | 0x60006049 | Program list materials exceeded limit. Up to 5 materials are allowed for a program list. Exception may occur when applying materials. |
| 6.0 | Invalid Content | planNumberOverlap | 0x6000604A | Plan No. conflict. Invalid week, holiday, holiday group or plan template No. |
| 6.0 | Invalid Content | fingerPrintIDAlreadyExist | 0x6000604B | Fingerprint ID already exists in host computer. |
| 6.0 | Invalid Content | pictureFaceDetectZero | 0x6000604C | No face found in the picture. Exception may occur when applying face pictures. |
| 6.0 | Invalid Content | faceTypeError | 0x6000604D | Face picture error. Exception may occur when applying face pictures. |
| 6.0 | Invalid Content | devicePlatformMismatch | 0x6000604E | Upgrade package and device platform type mismatch. |
| 6.0 | Invalid Content | verificationFailed | 0x6000604F | Verifying upgrade package signature failed. |
| 6.0 | Invalid Content | upgradeParameterWrong | 0x60006050 | Upgrade package parameter error. |
| 6.0 | Invalid Content | OEMCodeMismatch | 0x60006051 | Upgrade package error. The OEM code mismatch. |
| 6.0 | Invalid Content | versionMismatch | 0x60006052 | Upgrade version mismatch. |
| 6.0 | Invalid Content | deviceUserFull | 0x60007000 | No more people are allowed. |
| 6.0 | Invalid Content | deviceFaceFull | 0x60007001 | No more face pictures are allowed. |
| 6.0 | Invalid Content | deviceUserAlreadyExist | 0x60007002 | The person already exists. |
| 6.0 | Invalid Content | deviceUserNotExist | 0x60007003 | The person does not exists. |
| 6.0 | Invalid Content | deviceUserAlreadyExistFace | 0x60007004 | The person ID already has a face picture. |
| 6.0 | Invalid Content | cardFullPerUser | 0x60007005 | Maximum number of cards per person reached. |
| 6.0 | Invalid Content | fingerprintFullPerUser | 0x60007006 | Maximum number of fingerprints per person reached. |
| 6.0 | Invalid Content | roomNoInvalid | 0x60007007 | Invalid room No. |
| 6.0 | Invalid Content | phoneNumberInvalid | 0x60007008 | Invalid No. |
| 6.0 | Invalid Content | roomNoExisted | 0x60007009 | Room No. conflict (already exists). |
| 6.0 | Invalid Content | serialNumberConflict | 0x6000700a | Serial No. conflict. |
| 6.0 | Invalid Content | includeOldDevice | 0x6000700b | Devices of older versions exist. |
| 6.0 | Invalid Content | deviceIdxConflict | 0x6000700c | Device No. conflict. |
| 6.0 | Invalid Content | roomNoStorageFull | 0x60007010 | Storage space for numbers is full. |
| 6.0 | Invalid Content | roomNoNotExist | 0x60007011 | Room No. does not exist. |
| 6.0 | Invalid Content | invalidFaceRegion | 0x60007012 | Invalid face picture area. |
| 6.0 | Invalid Content | detectorTypeMismatch | 0x60008000 | Detector type mismatch. |
| 6.0 | Invalid Content | nameExist | 0x60008001 | Duplicate name. |
| 6.0 | Invalid Content | detectorTypeNotSupport | 0x60008002 | Detector type is not supported. |
| 6.0 | Invalid Content | notSupportDeicing | 0x60008003 | NaN |
| 6.0 | Invalid Content | notMeetDeicing | 0x60008004 | NaN |
| 6.0 | Invalid Content | notSupportWithAPMode | 0x60008005 | NaN |
| 6.0 | Invalid Content | thermEnableClose | 0x60008006 | NaN |
| 6.0 | Invalid Content | panoramicLimitOperated | 0x60008007 | NaN |
| 6.0 | Invalid Content | RuleNumLimit | 0x60008008 | NaN |
| 6.0 | Invalid Content | LaserDeicingOperated | 0x60008009 | NaN |
| 6.0 | Invalid Content | smartH264RoiOperated | 0x60008010 | NaN |
| 6.0 | Invalid Content | OffDigitalZoom\_Or\_MinZoomLimit | 0x60008011 | NaN |
| 6.0 | Invalid Content | drawLaneLineError | 0x60008012 | NaN |
| 6.0 | Invalid Content | laneAndRegionOverlap | 0x60008013 | The lanes are overlapped. Adjust the position of the lane area. |
| 6.0 | Invalid Content | intelligentTrafficMutexWithHighFrames | 0x60008014 | To use 50 fps or higher frame rate, all functions in Traffic Event, Enforcement, and Traffic Data Collection should be disabled first. |
| 6.0 | Invalid Content | uploadImageTypeError | 0x60008015 | Invalid uploaded picture format. |
| 6.0 | Invalid Content | uploadImageSizeError | 0x60008016 | Size of the uploaded picture is larger than 5 MB. |
| 6.0 | Invalid Content | uploadImageResolutionError | 0x60008017 | Invalid picture resolution. |
| 6.0 | Invalid Content | intelligentTrafficMutexWithHighFramesEx | 0x60008018 | To use 50 fps or higher frame rate, all functions in Traffic Event, Enforcement, Traffic Data Collection and Vehicle Detection should be disabled first. |
| 6.0 | Invalid Content | TriggerLineError | 0x60008019 | Adjust the trigger line to cover all configured lanes. |
| 6.0 | Invalid Content | trafficSceneSheduleMutexWithHighFrames | 0x6000801A | To use 50 fps or higher frame rate, Scene Auto-switch should be disabled first. |
| 6.0 | Invalid Content | UKLocalCertificationError | 0x6000801B | Ensure the security control panel has enabled the local authentication function. |
| 6.0 | Invalid Content | callInstaller | 0x6000801C | Contact the installer to restore tamper or acknowledged alarm. |
| 7.0 | Reboot Required | rebootRequired | 0x70000001 | The operation will take effect after rebooting. |
| 7.0 | Reboot Required | autoReboot | 0x70000002 | NaN |
| 8.0 | Batch Operation | notAllSuccess | 0x80000001 | Batch operation partially succeeded. |
| 8.0 | Batch Operation | allSuccess | 0x80000002 | Batch operation succeeded. |
| 8.0 | Batch Operation | allFailed | 0x80000003 | Batch operation failed. |