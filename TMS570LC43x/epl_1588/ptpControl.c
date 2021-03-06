//****************************************************************************
// ptpControl.c
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This is the top most API used by our PTP Python code.
//****************************************************************************

#include "ptpd.h"
//#include "epl.h"
//#include "ptpControl.h"

DWORD ptpTLSSlot;
HANDLE appMutex = NULL;

// Local prototypes
void PTPInitHardware( 
    IN PEPL_PORT_HANDLE portHandle,
    IN RunTimeOpts *ptpStackCfg);

void PTPThreadAll(
    IN PEPL_PORT_HANDLE portHandle,
    IN void *guiObj,
    IN void *stdioCallback, 
    IN void *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg);

//****************************************************************************
EXPORT void PTPThread(
    IN PEPL_PORT_HANDLE portHandle,
//    IN PyObject *guiObj,
//    IN PyObject *stdioCallback,
//    IN PyObject *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg)
{
    // Simply pass on through after setting Python flag
//    portHandle->oaiDevHandle->Python = TRUE;
//    PTPThreadAll( portHandle, (void *)guiObj, (void *)stdioCallback,
//                    (void *)statusUpdateCallback, ptpStackCfg );
    return;
}

EXPORT void PTPThreadC(
    IN PEPL_PORT_HANDLE portHandle,
    IN void *guiObj,
    IN void *stdioCallback, 
    IN void *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg)
{
    // Simply pass through after setting flag for NOT Python
//    portHandle->oaiDevHandle->Python = FALSE;
    PTPThreadAll( portHandle, guiObj, stdioCallback, 
                    statusUpdateCallback, ptpStackCfg );
    return;
}

void PTPThreadAll(
    IN PEPL_PORT_HANDLE portHandle,
    IN void *guiObj,
    IN void *stdioCallback, 
    IN void *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg)
//  Returns:
//      Nothing
//****************************************************************************
{
//OAI_DEV_HANDLE_STRUCT *oaiDevHandle;
//PtpClock *ptpClock;
//Integer16 ret;
//
//    oaiDevHandle = portHandle->oaiDevHandle;
//    oaiDevHandle->guiObj = guiObj;
//    oaiDevHandle->stdioCallback = stdioCallback;
//    oaiDevHandle->statusUpdateCallback = statusUpdateCallback;
//    oaiDevHandle->killThread = FALSE;
//
//    if ( !appMutex)
//    	appMutex = OAICreateMutex();
//
//    if( oaiDevHandle->Python ) {
//        // Can's use the Py_BEGIN / END macros because they are meant for local
//        // unblock/block code sections - we want wider control. Calling this
//        // allows python to run concurrently with our thread. We must restore
//        // thread contents if we want to call back into python.
//        oaiDevHandle->pythonThrdSave = PyEval_SaveThread();
//    }
//
//    // Set our thread specific storage structure
//    TlsSetValue( ptpTLSSlot, oaiDevHandle);
//
//    NOTIFY( "From inside PTPThread\n" );
//
//    oaiDevHandle->udpChksumEnable = ptpStackCfg->udpChksumEnable;
//
//    // Setup the PHY
//    PTPInitHardware( portHandle, ptpStackCfg);
//
//    // Setup the PTP stack
//    if ( !(ptpClock = ptpdStartup( 0, NULL, &ret, ptpStackCfg)))
//    {
//        ERROR( "ptpdStartup returned FAILURE\n");
//        if( oaiDevHandle->Python ) {
//            PyEval_RestoreThread( oaiDevHandle->pythonThrdSave);
//        }
//        return;
//    }
//
//    protocol( ptpStackCfg, ptpClock);
//
//    PTPEnable( portHandle, FALSE);
//
//    // Disable CLKOUT if it was enabled
//    if ( ptpStackCfg->clkOutEnableFlag) {
//        PTPSetClockConfig( portHandle, 0, ptpStackCfg->clkOutDivide, 0x00, 8);
//    }
//
//    ptpdShutdown( ptpClock);
//
//    if( oaiDevHandle->Python ) {
//        PyEval_RestoreThread( oaiDevHandle->pythonThrdSave);
//    }

    return;
}


//****************************************************************************
EXPORT void PTPKillThread(
    IN PEPL_PORT_HANDLE portHandle)
//****************************************************************************
{
//OAI_DEV_HANDLE_STRUCT *oaiDevHandle;
//
//    oaiDevHandle = portHandle->oaiDevHandle;
//    oaiDevHandle->killThread = TRUE;
    return;
}


//****************************************************************************
void PTPInitHardware( 
    IN PEPL_PORT_HANDLE portHandle,
    IN RunTimeOpts *ptpStackCfg)
//****************************************************************************
{
RX_CFG_ITEMS rxCfgItems;
NS_UINT events, overflowCount, flags, x;
NS_UINT seqId, hashValue;
NS_UINT8 msgType;
NS_UINT eventNum, riseFlag, eventsMissed;
NS_UINT32 rxCfgOpts;
NS_UINT phaseError, clkOutPeriod;
NS_UINT8 nTimeout1, nTimeout2;
TimeInternal ts;

//    ptpStackCfg->revA1SiliconFlag = FALSE;
//    if ( (EPLReadReg( portHandle, 0x0003) & 0x000F) == 0)
//        ptpStackCfg->revA1SiliconFlag = TRUE;
    
    // Disable 1588 clock, set start time, set rate to 0
//    PTPEnable( portHandle, FALSE);
    
    // Disconnect event from GPIO 12
//    PTPSetEventConfig( portHandle, 7, FALSE, FALSE, FALSE, 0);
    
//    x = EPLReadReg( portHandle, 0x0004);
//    x |= 0x0060;   // Enable advertising 10Mbps support
//    EPLWriteReg( portHandle, 0x0004, x);
//
//    flags = 0;
//    if ( ptpStackCfg->clkOutEnableFlag)
//    {
//        flags |= CLKOPT_CLK_OUT_EN;
//        if ( ptpStackCfg->clkOutSpeed)
//            flags |= CLKOPT_CLK_OUT_SPEED_SEL;
//        if ( ptpStackCfg->clkOutSource == 2)
//            flags |= CLKOPT_CLK_OUT_SEL;
//        else if ( ptpStackCfg->clkOutSource == 1)
//        {
//            // Cfg for 100 Mbps autoneg mode if FCO is src clk and user doesn't
//            // want to lose phase alignment on link loss.
//            EPLWriteReg( portHandle, 0x1E, 0x803F);
//            EPLWriteReg( portHandle, 0x1E, 0x803F);
//            x = EPLReadReg( portHandle, 0x0004);
//            x &= ~0x0060;   // Disable advertising 10Mbps support
//            EPLWriteReg( portHandle, 0x0004, x);
//        }
//    }
//
//    PTPSetClockConfig( portHandle, flags, ptpStackCfg->clkOutDivide, 0x00, 8);
//
//    PTPEnable( portHandle, TRUE);
//
//    PTPClockSet( portHandle, 0, 0);
//
//    // Setup the PPS configuration
//    if ( ptpStackCfg->ppsEnableFlag)
//    {
//        PTPSetTriggerConfig( portHandle, 0, TRGOPT_PULSE|TRGOPT_PERIODIC|TRGOPT_NOTIFY_EN, ptpStackCfg->ppsGpio);
//        PTPArmTrigger( portHandle, 0, ptpStackCfg->ppsStartTime, 0,
//                       ptpStackCfg->ppsRiseOrFallFlag, FALSE, 500000000, 500000000);
//    }
//    else
//    {
//        PTPCancelTrigger( portHandle, 0);
//    }
//
//    // Disable Transmit and Receive Timestamp
//    PTPSetTransmitConfig( portHandle, 0, 0, 0, 0);
//    memset( &rxCfgItems, 0, sizeof( RX_CFG_ITEMS));
//    PTPSetReceiveConfig( portHandle, 0, &rxCfgItems);
//
//    // Flush Receive FIFO
//    MACFlushReceiveFifos( portHandle);
//
//    // Flush Transmit, Receive and Event Timestamps
//    while ( (events = PTPCheckForEvents( portHandle))) {
//        if ( events & PTPEVT_TRANSMIT_TIMESTAMP_BIT)
//            PTPGetTransmitTimestamp( portHandle, &ts.seconds, &ts.nanoseconds, &overflowCount);
//        if ( events & PTPEVT_RECEIVE_TIMESTAMP_BIT)
//            PTPGetReceiveTimestamp( portHandle, &ts.seconds, &ts.nanoseconds, &overflowCount, &seqId, &msgType, &hashValue);
//        if ( events & PTPEVT_EVENT_TIMESTAMP_BIT)
//            PTPGetEvent( portHandle, &eventNum, &riseFlag, &ts.seconds, &ts.nanoseconds, &eventsMissed);
//    }
//
//    // Enable Transmit Timestamp operation
//    flags = TXOPT_IP1588_EN | TXOPT_IPV4_EN | TXOPT_TS_EN;
//
//    if ( ptpStackCfg->useOneStepFlag)
//    {
//        flags |= TXOPT_CRC_1STEP | TXOPT_CHK_1STEP | TXOPT_SYNC_1STEP | TXOPT_IGNORE_2STEP;
//    }
//
//    PTPSetTransmitConfig( portHandle, flags, 1, 0xFF, 0x00);
//
//    // Enable Receive Timestamp operation
//    rxCfgItems.ptpVersion = 0x01;
//    rxCfgItems.ptpFirstByteMask = 0xFF;
//    rxCfgItems.ptpFirstByteData = 0x00;
//    rxCfgItems.ipAddrData = 0;
//    rxCfgItems.tsMinIFG = 0x0C;
//    rxCfgItems.srcIdHash = 0;
//    rxCfgItems.ptpDomain = 0;
//    rxCfgItems.tsSecLen = 3; //0; // DRs option
//    rxCfgItems.rxTsNanoSecOffset = 0; //0x24; // DRs option
//    rxCfgItems.rxTsSecondsOffset = 0; //0x21; // DRs option
//
//    rxCfgOpts = RXOPT_IP1588_EN0|RXOPT_IP1588_EN1|RXOPT_IP1588_EN2|
//                RXOPT_RX_IPV4_EN|RXOPT_RX_TS_EN|RXOPT_ACC_UDP;
//
//    if ( !ptpStackCfg->revA1SiliconFlag) {
//        rxCfgOpts |= RXOPT_TS_SEC_EN|RXOPT_TS_INSERT|RXOPT_TS_APPEND;
//    }
//
//    if ( ptpStackCfg->slaveOnly)
//        rxCfgOpts |= RXOPT_RX_SLAVE;
//
//    PTPSetReceiveConfig( portHandle, rxCfgOpts, &rxCfgItems);
//
//    // Make sure TX timestamp PSFs are off before we go through the Phase
//    // alignment process.  This will allow TIMESTAMP events to be presented
//    // properly.  This will be undone below.
//    PTPSetPhyStatusFrameConfig( portHandle,
//                                (portHandle->psfConfigOptions & ~STSOPT_TXTS_EN),
//                                STS_SRC_ADDR_2,
//                                7, 0x00, VERSION_PTP, 0x0F, 0x0F,
//                                (NS_UINT32)(ptpStackCfg->srcIPAddress[0] |
//                                            ptpStackCfg->srcIPAddress[1]<<8 |
//                                            ptpStackCfg->srcIPAddress[2]<<16 |
//                                            ptpStackCfg->srcIPAddress[1]<<24) );
//
//    // Phase align CLKOUT if requested
//    if ( ptpStackCfg->clkOutEnableFlag && ptpStackCfg->phaseAlignClkoutFlag)
//    {
//        // Cfg event 7 for rising signal on GPIO 12
//        PTPSetEventConfig( portHandle, 7, TRUE, FALSE, FALSE, 12);
//
//        // Wait for the event timestamp - ignore the 1st one because sometimes
//        // we have an old event timestamp that isn't correct.
//        x = 0;
//
//        for( nTimeout1 = 10; nTimeout1; nTimeout1-- ) {
//            nTimeout2 = 10;
//            while ( !(PTPCheckForEvents( portHandle) & PTPEVT_EVENT_TIMESTAMP_BIT) && nTimeout2-- ) ;
//            if( !PTPGetEvent( portHandle, &eventNum, &riseFlag, &ts.seconds, &ts.nanoseconds, &eventsMissed) ) {
//                continue;
//            }
//
//            if( eventNum & 0x80 ) {
//                x++;
//                if( x > 1 ) {
//                    break;
//                }
//            }
//        }
//
//        DBG( "CLKOUT Event Time Stamp = %d %d\n", ts.seconds, ts.nanoseconds);
//
//        // Disconnect event from GPIO 12
//        PTPSetEventConfig( portHandle, 7, FALSE, FALSE, FALSE, 0);
//
//        // Clear out event queue
//        while ( PTPGetEvent( portHandle, &eventNum, &riseFlag, &ts.seconds, &ts.nanoseconds, &eventsMissed)) ;
//
//        // Calc the step adj needed to correct the phase difference.
//        ptpStackCfg->clkOutPeriod = clkOutPeriod = ptpStackCfg->clkOutDivide * 4;
//        DBG( "CLKOUT Period Value %dns\n", ptpStackCfg->clkOutPeriod);
//
//        phaseError = clkOutPeriod - (ts.nanoseconds % clkOutPeriod) + 16;
//        DBG( "Phase Adjustement %dns\n", phaseError);
//        PTPClockStepAdjustment( ptpStackCfg->eplPortHandle, 0, abs(phaseError), FALSE);
//    }
//
//    // Setup to receive PHY Status Frames
//    // NOTE: if the library is setup to use PCF/PSFs for access to the PHY these
//    //       settings should be compatible with those options.  See EPLEnumDevice()
//    //       for Options we start with existing.  Set/Clear other bits as desired.
//    PTPSetPhyStatusFrameConfig( portHandle, ( portHandle->psfConfigOptions
//                                 //& ~STSOPT_PCFR_EN
//                                 //|  STSOPT_PCFR_EN
//                                 //& ~STSOPT_IPV4         // Clear
//                                 |  STSOPT_IPV4       // Set
//                                 //& ~STSOPT_TXTS_EN      // Clear
//                                 |  STSOPT_TXTS_EN    // Set
//                                 //& ~STSOPT_RXTS_EN      // Clear
//                                 |  STSOPT_RXTS_EN    // Set
//                                 & ~STSOPT_TRIG_EN    // Clear
//                                 //|  STSOPT_TRIG_EN    // Set
//                                 & ~STSOPT_EVENT_EN   // Clear
//                                 //|  STSOPT_EVENT_EN   // Set
//                                 & ~STSOPT_ERR_EN     // Clear
//                                 //|  STSOPT_ERR_EN     // Set
//                                 ),
//                                STS_SRC_ADDR_2,
//                                7, 0x00, VERSION_PTP, 0x0F, 0x0F,
//                                (uint32_t)(ptpStackCfg->srcIPAddress[0] |
//                                            ptpStackCfg->srcIPAddress[1]<<8 |
//                                            ptpStackCfg->srcIPAddress[2]<<16 |
//                                            ptpStackCfg->srcIPAddress[1]<<24) );

    return;
}


//****************************************************************************
void PTPUpdateStatus(
    NS_UINT8 stsType,
    RunTimeOpts *rtOpts,
    PtpClock *ptpClock)
    
//  Returns:
//      Nothing
//****************************************************************************
{
//OAI_DEV_HANDLE_STRUCT *oaiDevHandle;
//STS_OFFSET_DATA_STRUCT stsODS;
//NS_UINT32 dBuf = 0;
//
//void (*callback)( NS_UINT8, void * );
//
//    oaiDevHandle = (OAI_DEV_HANDLE_STRUCT*)TlsGetValue( ptpTLSSlot );
//    if ( !oaiDevHandle )
//        return;
//
//    // Make sure we have a good pointer
//    callback = oaiDevHandle->statusUpdateCallback;
//    if( callback ) {
//        OAIBeginCriticalSection( appMutex );
//
//        switch( stsType ) {
//        case STS_OFFSET_DATA:
//            if( oaiDevHandle->Python ) {
//                PyEval_RestoreThread( oaiDevHandle->pythonThrdSave );
//                PyObject_CallFunction( (PyObject *)callback, "iiiiiiii",
//                                       ptpClock->offset_from_master.seconds,
//                                       ptpClock->offset_from_master.nanoseconds,
//                                       ptpClock->master_to_slave_delay.seconds,
//                                       ptpClock->master_to_slave_delay.nanoseconds,
//                                       ptpClock->slave_to_master_delay.seconds,
//                                       ptpClock->slave_to_master_delay.nanoseconds,
//                                       ptpClock->oneWayAvg.seconds,
//                                       ptpClock->oneWayAvg.nanoseconds );
//
//                oaiDevHandle->pythonThrdSave = PyEval_SaveThread();
//            }
//            else {
//                stsODS.offset_from_master = ptpClock->offset_from_master;
//                stsODS.master_to_slave_delay = ptpClock->master_to_slave_delay;
//                stsODS.slave_to_master_delay = ptpClock->slave_to_master_delay;
//                stsODS.oneWayAvg = ptpClock->oneWayAvg;
//                (*callback)( STS_OFFSET_DATA, (void *)&stsODS );
//            }
//            break;
//        case STS_PSF_DATA:
//            if( oaiDevHandle->Python ) {
//                // Python isn't setup to deal with this so don't do anything.
//                // Flush the list so it doesn't build up
//                PHYMSG_MESSAGE_TYPE_ENUM msgType;
//                PHYMSG_MESSAGE phyMsg;
//                NS_UINT32 dBuf = 0;
//                while( GetNextPhyMessage( rtOpts->eplPortHandle, (NS_UINT8 *)&dBuf, &msgType, &phyMsg ) );
//            }
//            else {
//                // Send a pointer to 0, calls to GetNextPhyMessage() will sort
//                // it out and send back a proper packet based on psfList, the
//                // pointer to 0 will prevent it from trying to parse/return
//                // a non-existent packet.
//                (*callback)( STS_PSF_DATA, (void *)&dBuf );
//            }
//            break;
//        default:
//            break;
//        } // switch( stsType )
//
//        OAIEndCriticalSection( appMutex );
//    }  // if( callback )
//
    return;
}

//****************************************************************************
void PTPPrintf(
    NS_UINT type,
    NS_UINT8 *baseStr,
    ...)
    
//  type - type of message, can be one of the following:
//      0 - debug msg (verbose)
//      1 - debug msg (normal)
//      2 - error msg
//      3 - normal notify msg
//    
//  Returns:
//      Nothing
//****************************************************************************
{
va_list args;
int ccode;
//OAI_DEV_HANDLE_STRUCT *oaiDevHandle;
//void (*callback)( int, char * );
//
//    oaiDevHandle = (OAI_DEV_HANDLE_STRUCT*)TlsGetValue( ptpTLSSlot );
//    if ( !oaiDevHandle )
//        return;
//
//    callback = oaiDevHandle->stdioCallback;
//    if( callback ) {
//
//        va_start( args, baseStr );
//        ccode = vsprintf_s( oaiDevHandle->sprintfBuffer, sizeof( oaiDevHandle->sprintfBuffer), baseStr, args );
//
//        if ( ccode != -1) {
//            OAIBeginCriticalSection( appMutex );
//            if( oaiDevHandle->Python ) {
//                PyEval_RestoreThread( oaiDevHandle->pythonThrdSave );
//                PyObject_CallFunction( (PyObject *)callback, "is", type, oaiDevHandle->sprintfBuffer );
//                oaiDevHandle->pythonThrdSave = PyEval_SaveThread();
//            }
//            else {
//                (*callback)( type, oaiDevHandle->sprintfBuffer );
//            }
//            OAIEndCriticalSection( appMutex );
//        }
//        va_end( args );
//    }
    return;
}
