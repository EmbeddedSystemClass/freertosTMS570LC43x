#===============================================================================
# This is kind of a monolithic script that runs through all of the EPL functions to 
# show how they are used from Python.
#===============================================================================

#===============================================================================
# Import Section - Get what we need from other places
import epl

from time import sleep

#===============================================================================
# Misc Tests
#===============================================================================
def CapabilitiesTest():
    print "\n  Capability Tests\n"

    # Check to see if device is capable of running TDR Tests
    capTDR = device.EPL_CAPA_TDR
    TDRTests = device.EPLIsDeviceCapable( capTDR )
    if( TDRTests ):
        print "    EPL_CAPA_TDR - Device is TDR Capable"
    else:
        print "    EPL_CAPA_TDR - Device is NOT TDR Capable "

    # Check to see if device is capable of running Link Quality Tests
    capQuality = device.EPL_CAPA_LINK_QUALITY
    QualityTests = device.EPLIsDeviceCapable( capQuality )
    if( QualityTests ):
        print "    EPL_CAPA_LINK_QUALITY - Device is Quality Capable"
    else:
        print "    EPL_CAPA_LINK_QUALITY - Device is NOT Quality Capable"

    capMIIPC = device.EPL_CAPA_MII_PORT_CFG
    MIIPCTests = device.EPLIsDeviceCapable( capMIIPC )
    if( MIIPCTests ):
        print "    EPL_CAPA_MII_PORT_CFG - Device does support MII port config"
    else:
        print "    EPL_CAPA_MII_PORT_CFG - Device does NOT support MII port config"

    capMIIRA = device.EPL_CAPA_MII_REG_ACCESS
    MIIRATests = device.EPLIsDeviceCapable( capMIIRA )
    if( MIIRATests ):
        print "    EPL_CAPA_MII_REG_ACCESS - Device does support MII reg access"
    else:
        print "    EPL_CAPA_MII_REG_ACCESS - Device does NOT support MII reg access"
        
    return
#---------------------------------------------------------------------------
def GetDisplayDeviceInfo():
    print "\n  EPLGetDeviceInfo() "
    deviceInfo = device.EPLGetDeviceInfo()
    if(   deviceInfo.deviceType == device.DEV_DP83848 ):
        print "    deviceType:          DEV_DP83848  "
    elif( deviceInfo.deviceType == device.DEV_DP83849 ):
        print "    deviceType:          DEV_DP83849  "
    elif( deviceInfo.deviceType == device.DEV_DP83640 ):
        print "    deviceType:          DEV_DP83640  "
    else:
        print "    deviceType:          DEV_UNKOWN"

    print "    numOfPorts:          %d " % (deviceInfo.numOfPorts)
    print "    deviceModelNum:      %d " % (deviceInfo.deviceModelNum)
    print "    deviceRevision:      %d " % (deviceInfo.deviceRevision)
    print "    numExtRegisterPages: %d " % (deviceInfo.numExtRegisterPages)
    
    return
#---------------------------------------------------------------------------
def GetSetMIICfg():
    print "\n  EPLGetMiiConfig() "
    capMIIPC = device.EPL_CAPA_MII_PORT_CFG
    MIIPCTests = device.EPLIsDeviceCapable( capMIIPC )
    if( MIIPCTests ):
        print "    EPL_CAPA_MII_PORT_CFG - Device does support MII port config"
        miiPCFG = device.EPLGetMiiConfig()
        if( miiPCFG==epl.MIIPCFG_NORMAL ):
            print "      MIIPCFG_NORMAL "
        elif( miiPCFG==epl.MIIPCFG_PORT_SWAP ):
            print "      MIIPCFG_PORT_SWAP "
        elif( miiPCFG==epl.MIIPCFG_EXT_MEDIA_CONVERTER ):
            print "      MIIPCFG_EXT_MEDIA_CONVERTER "
        elif( miiPCFG==epl.MIIPCFG_BROADCAST_TX_PORT_A ):
            print "      MIIPCFG_BROADCAST_TX_PORT_A "
        elif( miiPCFG==epl.MIIPCFG_BROADCAST_TX_PORT_B ):
            print "      MIIPCFG_BROADCAST_TX_PORT_B "
        elif( miiPCFG==epl.MIIPCFG_MIRROR_RX_CHANNEL_A ):
            print "      MIIPCFG_MIRROR_RX_CHANNEL_A "
        elif( miiPCFG==epl.MIIPCFG_MIRROR_RX_CHANNEL_B ):
            print "      MIIPCFG_MIRROR_RX_CHANNEL_B "
        elif( miiPCFG==epl.MIIPCFG_DISABLE_PORT_A ):
            print "      MIIPCFG_DISABLE_PORT_A "
        elif( miiPCFG==epl.MIIPCFG_DISABLE_PORT_B ):
            print "      MIIPCFG_DISABLE_PORT_B "
        else:
            print "      MIIPCFG_UNKNOWN "
            
        print "\n  EPLSetMiiConfig() "            
        miiPCFG = epl.MIIPCFG_NORMAL
        device.EPLSetMiiConfig( miiPCFG )

    else:
        print "    EPL_CAPA_MII_PORT_CFG - Device does NOT support MII port config"

        
    return
#---------------------------------------------------------------------------
def PortPower():
    print "\n  EPLSetPortPowerMode( FALSE )"
    xem.EPLSetPortPowerMode( FALSE )
    sleep(2)
    print "    Port Power Off "
    print "\n  EPLSetPortPowerMode( TRUE )"
    xem.EPLSetPortPowerMode( TRUE )
    print "    Port Power On  "
    sleep(2)
    return
#---------------------------------------------------------------------------
def GetMDIOAddress():
    print "\n  EPLGetPortMdioAddress()"
    mAdd = xem.EPLGetPortMdioAddress()
    print "    MDIO Port Address: %d " % mAdd
    return
#---------------------------------------------------------------------------
def ReadWrite():
    print "\n  EPLReadReg( epl.PHY_PHYSTS )"
    
    # Read the PHY Status Register
    value = xem.EPLReadReg( epl.PHY_PHYSTS )
    print "    PHYSTS Reg: %08X " % value
    
    print "\n  EPLWriteReg( epl.PHY_BMCR, epl.BMCR_RESTART_AUTONEG )"    
    print "    Restarting AutoNeg "
    # Restart AutoNeg
    xem.EPLWriteReg( epl.PHY_BMCR, epl.BMCR_RESTART_AUTONEG )
    
    return
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#===============================================================================
# Individual Link Tests
#---------------------------------------------------------------------------
def LinkUpTest():
    print "\n  EPLIsLinkUp() "
    result = xem.EPLIsLinkUp()
    if( result ):
        print "    Link is UP "
    else:
        print "    Link is NOT UP "
        
    return
#---------------------------------------------------------------------------
def GetLinkStatusTest():
    print "\n  EPLGetLinkStatus()"
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.linkup ):
        print "    Link is UP"
    else:
        print "    Link is DOWN"

    if( linkSts.autoNegEnabled ):
        print "    Auto-neg is ENABLED"
    else:
        print "    Auto-neg is DISABLED"

    if( linkSts.autoNegCompleted ):
        print "    Auto-neg has COMPLETED"
    else:
        print "    Auto-neg has NOT completed"

    if( linkSts.speed==100 ):
        print "    Link speed is 100Mbps"
    elif( linkSts.speed==10 ):
        print "    Link speed is 10Mbps"
    else:
        print "    Link speed is INVALID"

    if( linkSts.duplex ):
        print "    Link duplex is FULL"
    else: 
        print "    Link duplex is HALF"

    if( linkSts.mdixStatus ):
        print "    Wire pairs are swapped (crossed)"
    else:
        print "    Wire pairs are NOT swapped (crossed)"

    if( linkSts.autoMdixEnabled ):
        print "    Auto-MDIX is ENABLED"
    else:
        print "    Auto-MDIX is NOT enabled"

    if( linkSts.polarity ):
        print "    Inverted pair polarity WAS DETECTED"
    else:
        print "    Inverted pair polarity NOT detected"

    if( linkSts.energyDetectPower ):
        print "    Energy detect power is ON"
    else:
        print "    Energy detect power is OFF"
        
    return
#---------------------------------------------------------------------------
def SetLinkConfigTest():
    print "\n  EPLSetLinkConfig():"
    
    print "\n    Before Set: "
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.speed==100 ):
        print "    Link speed is 100Mbps"
    elif( linkSts.speed==10 ):
        print "    Link speed is 10Mbps"
    else:
        print "    Link speed is INVALID"

    # Get a config structure and fill it in from current status
    linkCfg = epl.EPL_LINK_CFG()
    linkCfg.autoNegEnable = linkSts.autoNegEnabled
    linkCfg.speed = linkSts.speed
    linkCfg.duplex = linkSts.duplex
    linkCfg.pause = TRUE
    linkCfg.autoMdix = linkSts.autoMdixEnabled
    linkCfg.energyDetect = linkSts.energyDetectPower
    
    # Make changes
    savedSpeed = linkSts.speed
    linkCfg.speed = 10
    
    # Set new config
    xem.EPLSetLinkConfig( linkCfg )
    sleep(3)
   
    print "\n    After Set: "
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.speed==100 ):
        print "    Link speed is 100Mbps"
    elif( linkSts.speed==10 ):
        print "    Link speed is 10Mbps"
    else:
        print "    Link speed is INVALID"
    
    linkCfg.speed = savedSpeed
    # Set new config
    xem.EPLSetLinkConfig( linkCfg )

    print "\n    After Restore: "
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.speed==100 ):
        print "    Link speed is 100Mbps"
    elif( linkSts.speed==10 ):
        print "    Link speed is 10Mbps"
    else:
        print "    Link speed is INVALID"

    return
#---------------------------------------------------------------------------
def RestartAutoNegTest():
    print "\n  EPLRestartAutoNeg():"
    print "\n    Before Restart: "
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.autoNegEnabled ):
        print "    Auto-neg is ENABLED"
    else:
        print "    Auto-neg is DISABLED"
    if( linkSts.autoNegCompleted ):
        print "    Auto-neg has COMPLETED"
    else:
        print "    Auto-neg has NOT completed"
    
    xem.EPLRestartAutoNeg()
    
    print "\n    After Restart: "    
    linkSts = xem.EPLGetLinkStatus()
    if( linkSts.autoNegEnabled ):
        print "    Auto-neg is ENABLED"
    else:
        print "    Auto-neg is DISABLED"
    if( linkSts.autoNegCompleted ):
        print "    Auto-neg has COMPLETED"
    else:
        print "    Auto-neg has NOT completed"
        
    return
#---------------------------------------------------------------------------
    
#---------------------------------------------------------------------------
#===============================================================================
# Individual BIST Tests
#---------------------------------------------------------------------------
def BISTTest():
    print "\n  BIST Tests:"
    print "    EPLSetLoopbackMode( TRUE )"
    xem.EPLSetLoopbackMode( TRUE )

    print "\n    EPLBistGetStatus()"
    bistActiveFlag, errNibbles = xem.EPLBistGetStatus()
    if ( bistActiveFlag ):
        print "      BIST is ACTIVE, Error Nibbles Count %d" % errNibbles
    else:
        print "      BIST is NOT ACTIVE, Error Nibbles Count %d" % errNibbles

    print "\n    EPLBistStartTxTest( TRUE )"
    xem.EPLBistStartTxTest( TRUE )

    print "\n    EPLBistGetStatus()"
    bistActiveFlag, errNibbles = xem.EPLBistGetStatus()
    if ( bistActiveFlag ):
        print "      BIST is ACTIVE, Error Nibbles Count %d" % errNibbles
    else:
        print "      BIST is NOT ACTIVE, Error Nibbles Count %d" % errNibbles

    print "\n    EPLBistStopTxTest"
    xem.EPLBistStopTxTest()

    print "\n    EPLBistGetStatus()"    
    bistActiveFlag, errNibbles = xem.EPLBistGetStatus()
    if ( bistActiveFlag ):
        print "      BIST is ACTIVE, Error Nibbles Count %d" % errNibbles
    else:
        print "      BIST is NOT ACTIVE, Error Nibbles Count %d" % errNibbles
    
    print "\n    EPLSetLoopbackMode( FALSE )"
    xem.EPLSetLoopbackMode( FALSE )
    
    return
#---------------------------------------------------------------------------
#===============================================================================
# Individual Quality Tests
#---------------------------------------------------------------------------
def GetCableStatusTest():
    print "\n  EPLGetCableStatus():"
    for sampleTime in range( 2, 10, 2 ):
        result, cableLen, freqOff, freqCtl, varVal = xem.EPLGetCableStatus( sampleTime )
        if( result==NS_STATUS_SUCCESS ):
            print "\n    SampleTime:   %d ms " % sampleTime
            print "    NS_STATUS_SUCCESS "
            print "    Cable Length: %d " % cableLen
            print "    freqOffset    %d " % (freqOff * 5.1562)
            print "    freqCtl       %d " % (freqCtl * 5.1562)
            print "    varianceValue %d " % varVal
            
            print "    Jitter in PPM = %d " % abs(((freqCtl * 5.1562) - (freqOff * 5.1562)))
          
            varData = (288.0 * ((1024*1024*sampleTime) / 8.0)) / float(varVal)
            rxSNR = 10.0 * math.log10( varData )
            print "    SNR %.2f db" % ( rxSNR )
        else:
            print "    NS_STATUS_FAILURE "
            print "      Link NOT UP or NOT at 100Mbps "
            break
            
    return    
#---------------------------------------------------------------------------
def GetDisplayDspLinkQuality():
    print "\n  EPLDspGetLinkQuality()"
    dspLQ = xem.EPLDspGetLinkQualityInfo();
    print "\n    Link Quality Details:"

    if( dspLQ.linkQualityEnabled ):
        print "      Link Quality: ENABLED "
    else:
        print "      Link Quality: DISABLED "
    
    if( dspLQ.linkQualityEnabled ):
        print "\n              Current   Thresholds   Alarms / Triggers"
        print   "              Samples   Low   High   Low          High"

        if( dspLQ.c1LowWarn ):
            lWString = "TRIGGERED "
        else:
            lWString = "no trigger"
        if( dspLQ.c1HighWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"
            
        print "      DEQ C1     %4d  %4d   %4d   %s   %s" % (
                        dspLQ.c1CtrlSample, dspLQ.c1LowThresh, dspLQ.c1HighThresh, 
                        lWString, hWString )

        if( dspLQ.dagcLowWarn ):
            lWString = "TRIGGERED "
        else:
            lWString = "no trigger"
        if( dspLQ.dagcHighWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"
                        
        print "      DAGC       %4d  %4d   %4d   %s   %s" % (
                        dspLQ.dagcCtrlSample, dspLQ.dagcLowThresh, dspLQ.dagcHighThresh,
                        lWString, hWString )

        if( dspLQ.dblwLowWarn ):
            lWString = "TRIGGERED "
        else:
            lWString = "no trigger"
        if( dspLQ.dblwHighWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"
                        
        print "      DBLW       %4d  %4d   %4d   %s   %s" % (
                        dspLQ.dblwCtrlSample, dspLQ.dblwLowThresh, dspLQ.dblwHighThresh,
                        lWString, hWString )

        if( dspLQ.freqOffLowWarn ):
            lWString = "TRIGGERED "
        else:
            lWString = "no trigger"
        if( dspLQ.freqOffHighWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"

        print "      FREQ       %4d  %4d   %4d   %s   %s" % (
                        dspLQ.freqOffSample, dspLQ.freqOffLowThresh, dspLQ.freqOffHighThresh,
                        lWString, hWString )

        if( dspLQ.freqCtrlLowWarn ):
            lWString = "TRIGGERED "
        else:
            lWString = "no trigger"
        if( dspLQ.freqCtrlHighWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"

        print "      FC         %4d  %4d   %4d   %s   %s" % (
                        dspLQ.freqCtrlSample, 
                        dspLQ.freqCtrlLowThresh, 
                        dspLQ.freqCtrlHighThresh,
                        lWString, hWString )

    print "\n      Restart on flags: "
    if( dspLQ.restartOnC1 ):
        print "      Restart on DEQ C1: SET     "
    else:
        print "      Restart on DEQ C1: NOT SET "
    if( dspLQ.restartOnDAGC ):
        print "      Restart on DAGC:   SET     "
    else:
        print "      Restart on DAGC:   NOT SET "
    if( dspLQ.restartOnDBLW ):
        print "      Restart on DBLW:   SET     "
    else:
        print "      Restart on DBLW:   NOT SET "
    if( dspLQ.restartOnFreq ):
        print "      Restart on Freq:   SET     "
    else:
        print "      Restart on Freq:   NOT SET "
    if( dspLQ.restartOnFC ):
        print "      Restart on FC:     SET     "
    else:
        print "      Restart on FC:     NOT SET "
                        
    if( dspLQ.varianceEnable ):
        print "\n      Variance Monitoring: ENABLED "
        if( dspLQ.varianceWarn ):
            hWString = "TRIGGERED "
        else:
            hWString = "no trigger"

        print "                       Current   Threshold   Trigger"
        print "      Variance(%dms)  %9d   %9d   %s " % (
                        dspLQ.varianceSampleTime, 
                        dspLQ.varianceSample, 
                        dspLQ.varianceHighThresh, 
                        hWString )
        if( dspLQ.restartOnVar ):
            print "\n      Restart on Variance:  SET     "
        else:
            print "\n      Restart on Variance:  NOT SET "
    else:
        print "\n      Variance Monitoring: DISABLED "

    if( dspLQ.dropLinkStatus ):
        print "\n      Drop Link Status:    SET     "
    else:
        print "\n      Drop Link Status:    NOT SET "
        
    return

#---------------------------------------------------------------------------
def SetDspLinkQuality( enableLQM ):
    # Get the structure to fill in
    linkQSet = epl.DSP_LINK_QUALITY_SET()
    if( enableLQM ):
        # Enable monitoring
        # NOTE! these are bogus values that should be changed
        # for real world operation!
        print "\n  Enable Link Quality Monitoring: "
        linkQSet.linkQualityEnabled = TRUE
        linkQSet.c1LowThresh = 0
        linkQSet.c1HighThresh = 1
        linkQSet.dagcLowThresh = 2
        linkQSet.dagcHighThresh = 3
        linkQSet.dblwLowThresh = 4
        linkQSet.dblwHighThresh = 5
        linkQSet.freqOffLowThresh = 6
        linkQSet.freqOffHighThresh = 7
        linkQSet.freqCtrlLowThresh = 8
        linkQSet.freqCtrlHighThresh = 9
        
        linkQSet.restartOnC1 = 0
        linkQSet.restartOnDAGC = 0
        linkQSet.restartOnDBLW = 0
        linkQSet.restartOnFreq = 0
        linkQSet.restartOnFC = 0
        linkQSet.restartOnVar = 0
        linkQSet.dropLinkStatus = 0
        
        linkQSet.varianceEnable = TRUE
        linkQSet.varianceSampleTime = 2
        linkQSet.varianceHighThresh = 1234
    else:
        # Disable monitoring - Sets thresholds to default value
        # in case they were set to something else before
        print "\n  Disable Link Quality Monitoring: "
        linkQSet.linkQualityEnabled = FALSE
        linkQSet.c1LowThresh = -128
        linkQSet.c1HighThresh = 127
        linkQSet.dagcLowThresh = 0
        linkQSet.dagcHighThresh = 255
        linkQSet.dblwLowThresh = -128
        linkQSet.dblwHighThresh = 127
        linkQSet.freqOffLowThresh = -128
        linkQSet.freqOffHighThresh = 127
        linkQSet.freqCtrlLowThresh = -128
        linkQSet.freqCtrlHighThresh = 127

        linkQSet.restartOnC1 = 0
        linkQSet.restartOnDAGC = 0
        linkQSet.restartOnDBLW = 0
        linkQSet.restartOnFreq = 0
        linkQSet.restartOnFC = 0
        linkQSet.restartOnVar = 0
        linkQSet.dropLinkStatus = 0
        
        linkQSet.varianceEnable = FALSE
        linkQSet.varianceSampleTime = 0
        linkQSet.varianceHighThresh = 0x0000    
        
    # Make the actual call 
    xem.EPLDspSetLinkQualityConfig( linkQSet )
    
    return


#---------------------------------------------------------------------------
#===============================================================================
# Individual TDR Tests
#---------------------------------------------------------------------------
def InitDeinitTDRTest():
    # Init/Deinit procedures must be called for certain other procedures
    print "\n  EPLInitTDR: "
    SavedLinkStatus = xem.EPLInitTDR()
    print "    SavedLinkStatus = %08X " % SavedLinkStatus
    
    # Normally you would do work in here...
    
    # Must call deinit for each init
    print "\n  EPLDeinitTDR: "
    xem.EPLDeinitTDR( SavedLinkStatus )
    return
#---------------------------------------------------------------------------
def GetTDRPulseShapeTest():
    print "\n  EPLGetTDRPulseShape(...):"
    print "    Results for (TX 8ns): (non-zero entries only)"
    result, pPulseResults, nPulseResults = xem.EPLGetTDRPulseShape(TRUE, FALSE)
    for n in range( 256 ):
        if( pPulseResults[n]>0 or nPulseResults[n]>0 ):
            print "      [%03d] Time %4dns  pos = %4d  neg = %4d " % (n, n*8,
                            pPulseResults[n], nPulseResults[n])
    del pPulseResults, nPulseResults
    print "\n  EPLGetTDRPulseShape(...):"
    print "    Results for (RX 8ns): (non-zero entries only)"
    result, pPulseResults, nPulseResults = xem.EPLGetTDRPulseShape(FALSE, FALSE)
    for n in range( 256 ):
        if( pPulseResults[n]>0 or nPulseResults[n]>0 ):
            print "      [%03d] Time %4dns  pos = %4d  neg = %4d " % (n, n*8,
                            pPulseResults[n], nPulseResults[n])
    del pPulseResults, nPulseResults
    print "\n  EPLGetTDRPulseShape(...):"
    print "    Results for (TX 50ns): (non-zero entries only)"
    result, pPulseResults, nPulseResults = xem.EPLGetTDRPulseShape(TRUE, TRUE)
    for n in range( 256 ):
        if( pPulseResults[n]>0 or nPulseResults[n]>0 ):
            print "      [%03d] Time %4dns  pos = %4d  neg =  N/A " % (n, n*8,
                            pPulseResults[n])
    del pPulseResults, nPulseResults
    print "\n  EPLGetTDRPulseShape(...):"
    print "    Results for (RX 50ns): (non-zero entries only)"
    result, pPulseResults, nPulseResults = xem.EPLGetTDRPulseShape(FALSE, TRUE)
    for n in range( 256 ):
        if( pPulseResults[n]>0 or nPulseResults[n]>0 ):
            print "      [%03d] Time %4dns  pos = %4d  neg =  N/A " % (n, n*8,
                            pPulseResults[n])
    del pPulseResults, nPulseResults
    return
#---------------------------------------------------------------------------
def GetTDRCableInfoTest():
    print "\n  EPLGetTDRCableInfo(TRUE): TX Status"
    # First get the TX cable status
    result, CableStatus, CableLength = xem.EPLGetTDRCableInfo( TRUE )
    if( result==0 ):
        print "    NS_STATUS_SUCCESS"
        if( CableStatus==0 ):
            print "    Status: Terminated"
        elif( CableStatus==1 ):
            print "    Status: Open"
        elif( CableStatus==2 ):
            print "    Status: Short"
        elif( CableStatus==3 ):
            print "    Status: Cross Shorted"
        else:
            print "    UNKNOWN"
        print "    Length: %.4fm" % float(CableLength / 4.64 / 2 )
    else:
        print "    ERROR: %d " % (result)
        
    print "\n  EPLGetTDRCableInfo(FALSE): RX Status"
    result, CableStatus, CableLength = xem.EPLGetTDRCableInfo( FALSE )
    if( result==0 ):
        print "    NS_STATUS_SUCCESS"
        if( CableStatus==0 ):
            print "    Status: Terminated"
        elif( CableStatus==1 ):
            print "    Status: Open"
        elif( CableStatus==2 ):
            print "    Status: Short"
        elif( CableStatus==3 ):
            print "    Status: Cross Shorted"
        else:
            print "    UNKNOWN"
        print "    Length: %.4fm" % float(CableLength / 4.64 / 2 )
    else:
        print "    ERROR: %d " % (result)

    return
#---------------------------------------------------------------------------
def GatherTDRInfoTest():
    print "\n  EPLGatherTDRInfo:"
    result, baseLine, pNI, nNI, pI, nI = xem.EPLGatherTDRInfo(TRUE,TRUE,3,FALSE)

    # pNI[10], nNI[8], pI[8], nI[8] will be lists of TDR_RUN_RESULTS 
    # each list will contain 8 (from 8ns to 64ns in 8ns increments) TDR_RUN_RESULTS except pNI which will have 10 for 
    # 50ns and 100ns samples.  The list objects are created in the call and must be deleted when we are done with them.
    print "    result %d, baseLine %d" % (result, baseLine)
    print "\n    Positive NoInvert Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(10):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            pNI[n].thresholdMet,
            pNI[n].thresholdTime, 
            pNI[n].peakValue, 
            pNI[n].peakTime, 
            pNI[n].adjustedPeakLengthRaw)
        
    print "\n    Negative NoInvert Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(8):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            nNI[n].thresholdMet,
            nNI[n].thresholdTime, 
            nNI[n].peakValue, 
            nNI[n].peakTime, 
            nNI[n].adjustedPeakLengthRaw)

    print "\n    Positive Invert Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(8):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            pI[n].thresholdMet,
            pI[n].thresholdTime, 
            pI[n].peakValue, 
            pI[n].peakTime, 
            pI[n].adjustedPeakLengthRaw)
            
    print "\n    Negative Invert Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(8):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            nI[n].thresholdMet,
            nI[n].thresholdTime, 
            nI[n].peakValue, 
            nI[n].peakTime, 
            nI[n].adjustedPeakLengthRaw)

    # Delete the lists now that we are done with them
    del pNI, nNI, pI, nI
    return
#---------------------------------------------------------------------------
def MeasureTDRBaselineTest():
    # must call EPLInitTDR procedures to use this call
    SavedLinkStatus = xem.EPLInitTDR()
    
    print "\n  EPLShortTDRPulseRun(TRUE):"
    baseline = xem.EPLMeasureTDRBaseline( TRUE )
    print "    TX Baseline: %d " % ( baseline )

    print "\n  EPLShortTDRPulseRun(FALSE):"
    baseline = xem.EPLMeasureTDRBaseline( FALSE )
    print "    RX Baseline: %d " % ( baseline )
    
    # must call EPLDeinitTDR procedures to use wrap things up
    xem.EPLDeinitTDR( SavedLinkStatus )
    return
#---------------------------------------------------------------------------
def ShortTDRPulseRunTest():
    # must call EPLInitTDR procedures to use this call
    SavedLinkStatus = xem.EPLInitTDR()

    print "\n  EPLShortTDRPulseRun:"
    result, pResults, nResults = xem.EPLShortTDRPulseRun(TRUE,TRUE,0x30,0x10,TRUE,FALSE)

    # pResults[8], nResults[8] will be lists of TDR_RUN_RESULTS.  Each list will contain 8 TDR_RUN_RESULTS
    # The list objects are created in the call and must be deleted when we are done with them.
    print "    result %d" % (result)
    print "\n    Positive Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(8):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            pResults[n].thresholdMet,
            pResults[n].thresholdTime, 
            pResults[n].peakValue, 
            pResults[n].peakTime, 
            pResults[n].adjustedPeakLengthRaw)
        
    print "\n    Negative Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(8):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            nResults[n].thresholdMet,
            nResults[n].thresholdTime, 
            nResults[n].peakValue, 
            nResults[n].peakTime, 
            nResults[n].adjustedPeakLengthRaw)

    # Delete the lists now that we are done with them
    del pResults, nResults
    
    # must call EPLDeinitTDR procedures to use wrap things up
    xem.EPLDeinitTDR( SavedLinkStatus )
    return
#---------------------------------------------------------------------------
def LongTDRPulseRunTest():
    # must call EPLInitTDR procedures to use this call
    SavedLinkStatus = xem.EPLInitTDR()

    print "\n  EPLLongTDRPulseRun:"
    result, pResults = xem.EPLLongTDRPulseRun( TRUE, TRUE, 0x30, FALSE)

    # pResults[2] will be lists of TDR_RUN_RESULTS.  The list will contain 2 TDR_RUN_RESULTS
    # The list objects are created in the call and must be deleted when we are done with them.
    print "    result %d" % (result)
    print "\n    Positive Results: "
    print "      [nn] thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(2):
        print "      [%02d] %4d, %4d, %4d, %4d, %4d" % (n, 
            pResults[n].thresholdMet,
            pResults[n].thresholdTime, 
            pResults[n].peakValue, 
            pResults[n].peakTime, 
            pResults[n].adjustedPeakLengthRaw)
        
    # Delete the lists now that we are done with them
    del pResults
    
    # must call EPLDeinitTDR procedures to use wrap things up
    xem.EPLDeinitTDR( SavedLinkStatus )
    return
#---------------------------------------------------------------------------
def RunTDRTest():
    # must call EPLInitTDR procedures to use this call
    SavedLinkStatus = xem.EPLInitTDR()

    print "\n  EPLRunTDR():"
    
    # First we must create a TDR Request object and fill it in
    Request = xem.TDR_RUN_REQUEST()
    Request.sendPairTx         = TRUE
    Request.reflectPairTx      = TRUE
    Request.use100MbTx         = TRUE
    Request.txPulseTime        = 1
    Request.detectPosThreshold = TRUE
    Request.rxDiscrimStartTime = 0
    Request.rxDiscrimStopTime  = 64
    Request.rxThreshold        = 0x30
    
    result, rResults = xem.EPLRunTDR( Request )

    # Results a TDR_RUN_RESULTS structure
    print "    Results: "
    print "      thresholdMet, thresholdTime, peakValue, peakTime, adjustedPeakLengthRaw"
    for n in range(2):
        print "      %3d, %3d, %3d, %3d, %3d" % ( 
            rResults.thresholdMet,
            rResults.thresholdTime, 
            rResults.peakValue, 
            rResults.peakTime, 
            rResults.adjustedPeakLengthRaw)
    
    # destroy the results structure since we don't need it anymore
    del rResults
    
    # must call EPLDeinitTDR procedures to use wrap things up
    xem.EPLDeinitTDR( SavedLinkStatus )
    return
#---------------------------------------------------------------------------

#===============================================================================
# Execution Starts HERE!
#===============================================================================

print "\n\nPython EPL Test Script"
print     "----------------------"

TRUE = 1
FALSE = 0

# Set each of the variables to 1 to run that particular test section
MiscTests = 0
LinkTests = 0
BISTTests = 0
TDRTests = 0
QualityTests = 1

# Misc Tests
if( MiscTests ):
    print "\nRunning Misc Tests... "
    CapabilitiesTest()
    GetDisplayDeviceInfo()
    GetSetMIICfg()
    PortPower()
    GetMDIOAddress()
    ReadWrite()
    
# Link Tests
if( LinkTests ):
    print "\nRunning Link Tests... "
    LinkUpTest()
    GetLinkStatusTest()
    SetLinkConfigTest()
    RestartAutoNegTest()

#BIST Tests
if( BISTTests ):
    print "\nRunning BIST Tests... "
    BISTTest()
            
# TDR Tests
if( TDRTests ):
    # Check to see if device is capable of running TDR Tests
    print "\nChecking TDR Capabilities"
    capTDR = device.EPL_CAPA_TDR
    TDRTests = device.EPLIsDeviceCapable( capTDR )
    if( TDRTests ):
        print "  EPL_CAPA_TDR - Device is TDR Capable"
        print "\nRunning TDR Tests... "
        GetTDRPulseShapeTest()
        GetTDRCableInfoTest()
        GatherTDRInfoTest()
        MeasureTDRBaselineTest()
        ShortTDRPulseRunTest()
        LongTDRPulseRunTest()
        RunTDRTest()
    else:
        print "  EPL_CAPA_TDR - Device is NOT TDR Capable "
        print "\nSkipping TDR Tests... "        
    
    
# Quality Tests
if( QualityTests ):
    # Check to see if device is capable of running Link Quality Tests
    print "\nChecking Link Quality Capabilities"    
    capQuality = device.EPL_CAPA_LINK_QUALITY
    QualityTests = device.EPLIsDeviceCapable( capQuality )
    if( QualityTests ):
        print "  EPL_CAPA_LINK_QUALITY - Device is Quality Capable"
        print "\nRunning Quality Tests... "        
        GetCableStatusTest()

        # Link Quality Monitor Test Sequence
        SetDspLinkQuality( FALSE )
        GetDisplayDspLinkQuality()
        SetDspLinkQuality( TRUE )
        GetDisplayDspLinkQuality()  
        SetDspLinkQuality( FALSE )
        GetDisplayDspLinkQuality()
    else:
        print "  EPL_CAPA_LINK_QUALITY - Device is NOT Quality Capable"
        print "\nSkipping Quality Tests... "        



    
