//****************************************************************************
// epl_tdr.c
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// Contains sources for TDR related functions.
//
// It implements the following functions:
//      EPLTdrGetPulseShape
//      EPLTdrGetCableInfo
//****************************************************************************

#include "epl.h"

// Local prototypes
static NS_UINT
    GetOpenOrShortLength( 
        IN PTDR_RUN_RESULTS posResults, 
        IN PTDR_RUN_RESULTS negResults, 
        IN NS_BOOL nonInverted);


//****************************************************************************
EXPORT NS_STATUS
    EPLGetTDRPulseShape(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL use50nsPulse,
        IN OUT NS_SINT8 *positivePulseResults,
        IN OUT NS_SINT8 *negativePulseResults)
        
//  Uses the TDR feature to obtain an oscilloscope trace of the TDR pulse on 
//  the wire. The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      If TRUE a trace will be obtained for the Tx cable pair, if FALSE the 
//      trace will be for the Rx cable pair.
//  use50nsPulse
//      If TRUE a 50ns electrical pulse will be used to obtain the trace. 
//      If FALSE an 8ns pulse will be used. The negativePulseResults buffer 
//      can be NULL when using the 50ns option because the device does NOT 
//      support sending a negative 50ns pulse.
//  positivePulseResults
//      This must be at least a 256 byte array that will have its contents 
//      set with the sample data that describes the TDR pulse trace that was 
//      obtained by sending positive TDR pulses. The values can range from 
//      -32 to +32 and represent the relative power level measured at each 
//      sampling point. The value at index 0 in the array represents time 0, 
//      index 1 at time 8ns, up to index 255 that represents 2.040us. 
//  negativePulseResults
//      This must be at least a 256 byte array that will have its contents 
//      set with the sample data that describes the TDR pulse trace that was 
//      obtained by sending negative TDR pulses. The values can range from 
//      -32 to +32 and represent the relative power level measured at each 
//      sampling point. The value at index 0 in the array represents time 0, 
//      index 1 at time 8ns, up to index 255 that represents 2.040us. 
//      This array will NOT be set if use50nsPulse is TRUE.
//
//  Returns:
//      Results array data set as described above.
//****************************************************************************
{
TDR_RUN_REQUEST tdrRequest;
TDR_RUN_RESULTS tdrResults;
NS_UINT posPeakValue, windowTime, savedInfo;

    savedInfo = EPLInitTDR( portHandle);
    
    tdrRequest.sendPairTx = tdrRequest.reflectPairTx = useTxChannel;
    tdrRequest.txPulseTime = 1;
    tdrRequest.rxThreshold = 0x20;
    
    if ( use50nsPulse)
    {
        tdrRequest.use100MbTx = FALSE;
        tdrRequest.detectPosThreshold = TRUE;
    }
    else
        tdrRequest.use100MbTx = TRUE;
    
    for ( windowTime = 0; windowTime < 256; windowTime++)
    {
        tdrRequest.rxDiscrimStartTime = tdrRequest.rxDiscrimStopTime = windowTime;
    
        if ( use50nsPulse)
        {
            EPLRunTDR( portHandle, &tdrRequest, &tdrResults);
            if ( windowTime <= (50/8)+1)
                positivePulseResults[windowTime] = 0;
            else
                positivePulseResults[windowTime] = tdrResults.peakValue - 0x20;
        }
        else
        {
            tdrRequest.detectPosThreshold = TRUE;
            EPLRunTDR( portHandle, &tdrRequest, &tdrResults);
            posPeakValue = tdrResults.peakValue;
            
            tdrRequest.detectPosThreshold = FALSE;
            EPLRunTDR( portHandle, &tdrRequest, &tdrResults);
            
            if ( windowTime <= 1)
                positivePulseResults[windowTime] = negativePulseResults[windowTime] = 0;
            else
            {
                positivePulseResults[windowTime] = posPeakValue - 0x20;
                negativePulseResults[windowTime] = tdrResults.peakValue - 0x20;
            }
        }
    }

    EPLDeinitTDR( portHandle, savedInfo);
    return NS_STATUS_SUCCESS;
}

 
//****************************************************************************
EXPORT NS_STATUS
    EPLGetTDRCableInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN OUT EPL_CABLE_STS_ENUM *cableStatus,
        IN OUT NS_UINT *rawCableLength)

//  Attempts to determine the length and status of the specified channel on 
//  this port. The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  To calculate the length of the cable or distance to a fault use the 
//  following formula:
//      length = rawCableLength / TDR_CABLE_VELOCITY / 2
//  where TDR_CABLE_VELOCITY is defined as 4.64. The length value will be in 
//  meters.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      If TRUE information will be obtained for the Tx cable pair, if FALSE 
//      the information will be for the Rx cable pair.
//  cableStatus
//      Set on return to a value that indicates the status of the selected 
//      wire pair (see enum definitions in epl.h).
//  rawCableLength
//      Set on return to a raw value indicating the approximate length of the 
//      cable or distance to fault. If the cableStatus indicates that the 
//      cable is properly terminated then this value is NOT valid. This value 
//      must be post processed to obtain the length in meters (see Comments 
//      above for formula).
//
//  Returns:
//      Passed in return parameters set as described above.
//      NS_STATUS_SUCCESS if determination was successful.
//      NS_STATUS_RESOURCES if memory allocation failed.
//****************************************************************************
{
PTDR_RUN_RESULTS posNoInvert, negNoInvert, posInvert, negInvert;
NS_BOOL reflectTxChannel, success;
NS_UINT length, threshAdjConst;

    *rawCableLength = 0;
    
    // Attempt to obtain a reflection that meets a threshold.
    if ( EPLIsLinkUp( portHandle))
    {
        *cableStatus = CABLE_STS_TERMINATED;
        return NS_STATUS_SUCCESS;
    }

    // Allocate the results arrays
    posNoInvert = (PTDR_RUN_RESULTS)OAIAlloc( (sizeof( TDR_RUN_RESULTS) * 10 * 1) + \
                                              (sizeof( TDR_RUN_RESULTS) * 8 * 3));
    if ( !posNoInvert)
        return NS_STATUS_RESOURCES;
        
    negNoInvert = &posNoInvert[10];
    posInvert = &negNoInvert[8];
    negInvert = &posInvert[8];

    for ( threshAdjConst = 10; threshAdjConst > 0; threshAdjConst--)
    {
        success = EPLGatherTDRInfo( portHandle, useTxChannel, useTxChannel, threshAdjConst,
                                    TRUE, NULL, posNoInvert, negNoInvert, posInvert, negInvert);
        if ( success)
            break;
    }
    
    if ( !success)
    {
        *cableStatus = CABLE_STS_UNKNOWN;
        OAIFree( posNoInvert);
        return NS_STATUS_FAILURE;
    }

    // Determine if there's an open pair. We determine this by checking 
    // for TDR pulses that successfully reflect with the same polarity
    // as the initiated TDR pulse.
    length = GetOpenOrShortLength( posNoInvert, negNoInvert, TRUE);
    if ( length != -1)
    {
        *cableStatus = CABLE_STS_OPEN;
        *rawCableLength = length;
        
        // If open, check for tx/rx shorted together 
        if ( useTxChannel) reflectTxChannel = FALSE;
        else reflectTxChannel = TRUE;

        success = EPLGatherTDRInfo( portHandle, useTxChannel, reflectTxChannel, 3, TRUE, NULL,
                                    posNoInvert, negNoInvert, posInvert, negInvert);
        if ( success)
            *cableStatus = CABLE_STS_CROSS_SHORTED;
    }
    else
    {
        // Determine if there's a shorted pair. We determine this by checking
        // for TDR pulses that succcessfully reflect with an opposite 
        // polarity as the TDR pulse itself.
        length = GetOpenOrShortLength( posInvert, negInvert, FALSE);
        if ( length != -1)
        {
            *cableStatus = CABLE_STS_SHORT;
            *rawCableLength = length;
        }
        else
            *cableStatus = CABLE_STS_UNKNOWN;
    }
        
    OAIFree( posNoInvert);
    return NS_STATUS_SUCCESS;
}


//****************************************************************************
static NS_UINT
    GetOpenOrShortLength( 
        IN PTDR_RUN_RESULTS posResults, 
        IN PTDR_RUN_RESULTS negResults, 
        IN NS_BOOL nonInverted)
    
//  Attempts to find successful threshold met test case and returns the
//  the adjusted peak length value. Positive and negative lengths are
//  averaged together, except in the case of the 100ns pulse.
//
//  Returns:
//      -1 if no threshold met test case could be found.
//      Adjusted peak length
//****************************************************************************
{
NS_UINT x;

    for ( x = 0; x < 8; x++)
    {
        if ( posResults[x].thresholdMet && negResults[x].thresholdMet)
        {
            return ( posResults[x].adjustedPeakLengthRaw + 
                     negResults[x].adjustedPeakLengthRaw) / 2;
        }
    }
    
    // Check the 50 & 100ns tests from the 10Mbps transmit engine (if this is noninverted)
    if ( nonInverted)
    {
        if ( posResults[8].thresholdMet)
            return posResults[8].adjustedPeakLengthRaw;
        if ( posResults[9].thresholdMet)
            return posResults[9].adjustedPeakLengthRaw;
    }
    
    return -1;
}


//****************************************************************************
EXPORT NS_BOOL
    EPLGatherTDRInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT thresholdAdjustConstant,
        IN NS_BOOL stopAfterSuccess,
        IN OUT NS_UINT *baseline,
        IN OUT PTDR_RUN_RESULTS posResultsArrayNoInvert,
        IN OUT PTDR_RUN_RESULTS negResultsArrayNoInvert,
        IN OUT PTDR_RUN_RESULTS posResultsArrayInvert,
        IN OUT PTDR_RUN_RESULTS negResultsArrayInvert)
            
//  General purpose routine that runs all useful TDR test configurations
//  and returns the results. This can also be used to obtain a complete characteristic
//  dump of all TDR tests determine and troubleshoot TDR behaviour.
//
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//  
//  InitTDR() and DeinitTDR() should NOT be called when using this function.
//  
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      Specifies the send channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  useTxReflectChannel
//      Specifies the reflect channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  thresholdAdjustConstant
//      Defines the integer value that will be added to and substracted
//      from the baseline line levels to determine appropriate 
//      transmit and receive thresholds.
//  stopAfterSuccess
//      If set to TRUE all configurations are run until a successful reflection 
//      (both pos and neg) is obtained, or a pos reflection is obtained using
//      the 10Mbps block. Timings are increased from lowest to highest.
//      If set to FALSE all possible configurations are run with all 
//      possible timings. 
//  baseline
//      Set on return to the quiescent baseline measurement of the wire pair. 
//      If NULL this parameter will be ignored.
//  posResultsArrayNoInvert[10]
//  negResultsArrayNoInvert[8]
//  posResultsArrayInvert[8]
//  negResultsArrayInvert[8]
//      Arrays of TDR_RUN_RESULTS structures. These will be set 
//      on return with the results of running 8 TDR pulses from
//      8ns to 64ns (8ns step), followed by one 50ns and one 100ns pulse 
//      result (posResults only). If both pos and neg thresholds 
//      are met or the 50ns or 100ns threshold is reached and stopAfterSuccess 
//      is set to TRUE, any entries that were not run will be set 0.
//      Invert means that a inverse polarity reflection will be 
//      tested for. The 50ns and 100ns positive only pulse results
//      are not present in the negative polarity and inverted test results.
//      Entries that were not run will be NULL'ed out.
//
//  Returns:
//      TRUE if both a positive and negative pulse of the same length met 
//      their thresholds. TRUE is also returned if a positive 50ns or 100ns
//      pulse reaches its threshold. FALSE is returned if thresholds were
//      not met.
//****************************************************************************
{
NS_UINT posThresh, negThresh, base, x, c, length, savedInfo;
NS_BOOL thresholdMet = FALSE, success = FALSE, noninverted = TRUE;
PTDR_RUN_RESULTS results[4] = { posResultsArrayNoInvert, negResultsArrayNoInvert,\
                                posResultsArrayInvert, negResultsArrayInvert };
PTDR_RUN_RESULTS result;

    savedInfo = EPLInitTDR( portHandle);

    // Clear the results
    for ( x = 0; x < 4; x++)
    {
        if ( x == 0) length = 10;
        else length = 8;
        result = results[x];
        for ( c = 0; c < length; c++)
        {
            result->thresholdMet = FALSE;
            result->thresholdTime = result->thresholdLengthRaw = \
            result->peakValue = result->peakTime = \
            result->peakLengthRaw = result->adjustedPeakLengthRaw = 0;
            result++;
        }
    }
    
    // Determine reasonable thresholds based on the quiescent baseline measurements
    base = EPLMeasureTDRBaseline( portHandle, useTxChannel);
    posThresh = base + thresholdAdjustConstant;
    if ( posThresh > 0x3F) posThresh = 0x3F;
    negThresh = base - thresholdAdjustConstant;
    if ( negThresh < 0) negThresh = 0x00;
    if ( baseline) *baseline = base;

    for ( x = 0; x < 4; x += 2)
    {
        if ( x == 2) noninverted = FALSE;
    
        // Run each test using the 100Mb(short) and 10Mb (long) pulse generators
        success = EPLShortTDRPulseRun( portHandle, useTxChannel, useTxReflectChannel,
                                       posThresh, negThresh, noninverted, stopAfterSuccess,
                                       results[x], results[x+1]);

        if (!(stopAfterSuccess && success) && x == 0)
        {
            success = EPLLongTDRPulseRun( portHandle, useTxChannel, useTxReflectChannel,
                                          posThresh, stopAfterSuccess, &results[x][8]);
        }

        if ( success)
        {
            thresholdMet = TRUE;
            if ( stopAfterSuccess)
                break;
        }
    }
    
    EPLDeinitTDR( portHandle, savedInfo);
    return thresholdMet;
}


//****************************************************************************
EXPORT NS_UINT
    EPLInitTDR(
        IN PEPL_PORT_HANDLE portHandle)
  
//  Must be called prior to using the measurement TDR methods. This method
//  initializes the TDR engine for subsequent calls to the RunTDR(), TDRShortPulseRun(),
//  TDRLongPulseRun() or TDRMeasureBaseline() methods. DeinitTDR() must be called after 
//  all calls have been made to the TDR measurement methods.
//
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//
//  Returns:    
//      Saved link status (must be passed to DeinitTDR()).
//****************************************************************************
{
NS_UINT bmcr;

    // Force 100Mb FD
    bmcr = EPLReadReg( portHandle, PHY_BMCR);
    EPLWriteReg( portHandle, PHY_BMCR, BMCR_FORCE_SPEED_100 | BMCR_FORCE_FULL_DUP);
    
    // Stop TDR to ensure clean start
    EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, 0x0000);

    // Start TDR 100Mb circuitry
    EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, P849_TDR_100MB | P849_TDR_ENABLE);
    return bmcr;
}

   
//****************************************************************************
EXPORT void 
    EPLDeinitTDR(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT savedLinkStatus)

//  Must be called after all desired calls have been made to the
//  TDR measurement methods. This method restores the PHY to the previous
//  link settings.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  savedLinkStatus
//      Value that was returned by InitTDR() function.
//  
//  Returns:
//      Nothing
//****************************************************************************
{
    // Disable TDR
    EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, 0x0000);
    
    // Restart auto-neg if it was previously enabled
    if (savedLinkStatus & BMCR_AUTO_NEG_ENABLE)
        savedLinkStatus |= BMCR_RESTART_AUTONEG;
    EPLWriteReg( portHandle, PHY_BMCR, savedLinkStatus);
    return;
}


//****************************************************************************
EXPORT NS_UINT
    EPLMeasureTDRBaseline(
        IN PEPL_PORT_HANDLE portHandle,
        NS_BOOL useTxChannel)

//  Measures the baseline signal level for the specified channel.
//  This can be used to determine appropriate threshold values by
//  using the baseline values as a mid point.
//  
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      Set to TRUE to measure the baseline for the Tx channel, set to FALSE
//      to measure the Rx channel.
//  
//  Returns:    
//      Baseline level
//****************************************************************************
{
TDR_RUN_REQUEST tdrParms = { useTxChannel, useTxChannel, TRUE, 0, TRUE, 0, 0xFF, 0x20 };
TDR_RUN_RESULTS tdrResults;

    EPLRunTDR( portHandle, &tdrParms, &tdrResults);
    return tdrResults.peakValue;
}


//****************************************************************************
EXPORT NS_BOOL
    EPLShortTDRPulseRun(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT posThreshold,
        IN NS_UINT negThreshold,
        IN NS_BOOL noninvertedThreshold,
        IN NS_BOOL stopAfterSuccess,
        IN OUT PTDR_RUN_RESULTS posResultsArray,
        IN OUT PTDR_RUN_RESULTS negResultsArray)
                      
//  Runs through all useful combinations of TDR operations
//  on the specified channel using the chip's 100Mb 8ns
//  pulse generator. The positive and negative threshold values 
//  can be specified.
//    
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      Specifies the send channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  useTxReflectChannel
//      Specifies the reflect channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  posThreshold : Integer (0x21 - 0x3F)
//      Specifies the positive threshold value used when listening
//      for a return TDR pulse.
//  negThreshold : Integer (0x00 - 0x20)
//      Specifies the negative threshold value used when listening
//      for a return TDR pulse.
//  noninvertedThreshold
//      Specifies whether or not an non-inverted polarity threshold and peak 
//      detection should be used. For example if set to FALSE, after sending
//      a positive(+) TDR pulse, the chip would be set to detect
//      a negative(-) return pulse. Set to FALSE to detect a channel that
//      is electrically shorted.
//  stopAfterSuccess
//      Specifies whether measurements should stop after a successful
//      threshold condition occurs. If FALSE, all possible timing
//      configurations are run.
//  posResultsArray
//      Array of 8 TDR_RUN_RESULTS structures. These will be set 
//      on return with the results of running 8 TDR pulses from
//      time 1 to time 8. These represent the results of positive
//      polarity pulses. If both pos and neg thresholds are met
//      and stopAfterSuccess is set to TRUE, any entries that 
//      were not run will be set 0. 
//  negResultsArray
//      Array of 8 TDR_RUN_RESULTS structures. These will be set 
//      on return with the results of running 8 TDR pulses from
//      time 1 to time 8. These represent the results of negative
//      polarity pulses.
//  
//  Returns:
//      TRUE if both positive and negative thresholds were met using
//      the same length of TDR pulse, FALSE otherwise. The positiveResultArray
//      and negativeResultsArray array structures will hold the
//      TDR pulse results.
//****************************************************************************
{
NS_UINT pthresh, nthresh, txPulseTime;
TDR_RUN_REQUEST tdrRequest;

    // Set thresholds according to whether we're looking for an
    // inverted reflection.
    if ( noninvertedThreshold)
    {
        pthresh = posThreshold;
        nthresh = negThreshold;
    }
    else
    {
        pthresh = negThreshold;
        nthresh = posThreshold;
    }

    tdrRequest.sendPairTx = useTxChannel;
    tdrRequest.reflectPairTx = useTxReflectChannel;
    tdrRequest.use100MbTx = TRUE;
    tdrRequest.rxDiscrimStopTime = 0xFF;

    for ( txPulseTime=0; txPulseTime < 8; txPulseTime++)
    {
        tdrRequest.txPulseTime = txPulseTime;
        tdrRequest.rxDiscrimStartTime = txPulseTime;
        tdrRequest.rxThreshold = pthresh;
        tdrRequest.detectPosThreshold = noninvertedThreshold;
        EPLRunTDR( portHandle, &tdrRequest, posResultsArray);

        tdrRequest.rxThreshold = nthresh;
        tdrRequest.detectPosThreshold = !noninvertedThreshold;
        EPLRunTDR( portHandle, &tdrRequest, negResultsArray);
        
        // Stop gathering if we have both pos and neg thresholds met and the caller wants this behavior
        if ( stopAfterSuccess && posResultsArray->thresholdMet && negResultsArray->thresholdMet)
            return TRUE;
        posResultsArray++;
        negResultsArray++;
    }
    
    return FALSE;
}


//****************************************************************************
EXPORT NS_BOOL
    EPLLongTDRPulseRun(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT threshold,
        IN NS_BOOL stopAfterSuccess,
        IN OUT PTDR_RUN_RESULTS resultsArray)
                      
//  Runs through all useful combinations of TDR operations
//  on the specified channel using the chip's 10Mb 50ns
//  pulse generator. The positive threshold value can be 
//  specified.
//    
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  useTxChannel
//      Specifies the send channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  useTxReflectChannel
//      Specifies the reflect channel. Set to TRUE to use Tx channel,
//      FALSE for the Rx channel.
//  threshold : Integer (0x21 - 0x3F)
//      Specifies the positive threshold value used when listening
//      for a return TDR pulse.
//  stopAfterSuccess
//      Specifies whether measurements should stop after a successful
//      threshold condition occurs. If FALSE, all possible timing
//      configurations are run.
//  resultsArray
//      Array of 2 TDR_RUN_RESULTS structures. These will be set 
//      on return with the results of running 2 TDR pulses, 50ns
//      and 100ns.
//  
//  Returns:
//      TRUE if the specified threshold was met.The resultsArray
//      structure will hold the TDR pulse results, the first structure
//      will have the results for the 50ns pulse, the second structure
//      will have the results for the 100ns pulse.
//****************************************************************************
{
NS_UINT txPulseTime;
TDR_RUN_REQUEST tdrRequest;

    tdrRequest.sendPairTx = useTxChannel;
    tdrRequest.reflectPairTx = useTxReflectChannel;
    tdrRequest.use100MbTx = FALSE;
    tdrRequest.rxDiscrimStopTime = 0xFF;
    tdrRequest.rxThreshold = threshold;
    tdrRequest.detectPosThreshold = TRUE;

    for ( txPulseTime = 1; txPulseTime < 3; txPulseTime++)
    {
        tdrRequest.rxDiscrimStartTime = ((txPulseTime * 50) / 8) + 1;
        tdrRequest.txPulseTime = txPulseTime;
        EPLRunTDR( portHandle, &tdrRequest, resultsArray);
        
        // Stop gathering if we have a met threshold and the caller wants this behavior
        if ( stopAfterSuccess && resultsArray->thresholdMet)
        {
            // Bug FIX: If you don't stop the TDR after being in 10Mb mode, then
            // you get erroneous results when trying to do 100Mb operations.
            EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, 0x0000);
            return TRUE;
        }
        
        resultsArray++;
    }
    
    // Bug FIX: If you don't stop the TDR after being in 10Mb mode, then
    // you get erroneous results when trying to do 100Mb operations.
    EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, 0x0000);
    return FALSE;
}


//****************************************************************************
EXPORT NS_STATUS
    EPLRunTDR(
        IN PEPL_PORT_HANDLE portHandle,
        IN PTDR_RUN_REQUEST tdrParms,
        IN OUT PTDR_RUN_RESULTS tdrResults)
   
//  Low-level function that initiates a TDR operation and gathers
//  the results of the operation.
//  
//  The hardware will alternate between sending a positive and negative
//  pulses when txUse100Mb is TRUE. If set to FALSE, only positive pulses
//  will be sent.
//  
//  The device must have the EPL_CAPA_TDR capability to use this 
//  function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  tdrParms
//      Pointer to a TDR_RUN_REQUEST structure that defines the parameters
//      that will be used for the TDR operation.
//  tdrResults
//      Pointer to a TDR_RUN_RESULTS structure that will be set on return
//      with the results of the TDR operation.
//    
//  Returns:
//      Nothing       
//****************************************************************************
{
NS_UINT tdrctl, tdrThresh, tdrPeak, pulseTime;

    // Setup TDR control reg
    tdrctl = tdrParms->rxThreshold;
    if ( !tdrParms->detectPosThreshold)
        tdrctl |= P849_TDR_MIN_MODE;
        
    tdrctl |= (tdrParms->txPulseTime << P849_TDR_WIDTH_SHIFT) & P849_TDR_WIDTH_MASK;
    
    if ( !tdrParms->reflectPairTx)
        tdrctl |= P849_RX_CHANNEL;
    if ( !tdrParms->sendPairTx)
        tdrctl |= P849_TX_CHANNEL;
    if ( tdrParms->use100MbTx)
        tdrctl |= P849_TDR_100MB;
    
    // Setup receive window times (8ns units)
    EPLWriteReg( portHandle, PHY_PG2_TDR_WIN, (tdrParms->rxDiscrimStartTime \
                 << P849_TDR_START_SHIFT) | tdrParms->rxDiscrimStopTime);
    
    // Initiate the actual TDR 
    tdrctl |= P849_TDR_ENABLE | P849_SEND_TDR;
    EPLWriteReg( portHandle, PHY_PG2_TDR_CTRL, tdrctl);

    // Wait for the TDR tx to finish ... should always be done
    for (;;)
    {
        tdrctl = EPLReadReg( portHandle, PHY_PG2_TDR_CTRL);
        if ( !(tdrctl & P849_SEND_TDR))
            break;
    }
    
    // Gather the results
    tdrThresh = EPLReadReg( portHandle, PHY_PG2_TDR_THR);
    tdrPeak = EPLReadReg( portHandle, PHY_PG2_TDR_PEAK);
    
    // Setup the return values
    tdrResults->peakValue = (tdrPeak & P849_TDR_PEAK_MASK) >> P849_TDR_PEAK_SHIFT;
    tdrResults->peakTime = ((tdrPeak & P849_TDR_PEAK_TIME_MASK) >> P849_TDR_PEAK_TIME_SHIFT) * 8;
    tdrResults->thresholdTime = ((tdrThresh & P849_TDR_THR_TIME_MASK) >> P849_TDR_THR_TIME_SHIFT) * 8;
    tdrResults->thresholdMet = FALSE;

    pulseTime = tdrParms->txPulseTime;
    if ( !tdrParms->use100MbTx)
    {
        if ( tdrParms->txPulseTime == 1) pulseTime = 48 / 8;
        else if ( tdrParms->txPulseTime == 2) pulseTime = 96 / 8;
    }
    
    tdrResults->peakLengthRaw = tdrResults->peakTime;
    
    // Adjust Peak lengths to subtract off TDR pulse length for 
    // proper length calculation.
    tdrResults->adjustedPeakLengthRaw = tdrResults->peakTime - (pulseTime-1) * 8;
    
    if ( tdrThresh & P849_TDR_THR_MET)
    {
        tdrResults->thresholdMet = TRUE;
        tdrResults->thresholdLengthRaw = tdrResults->thresholdTime;
    }
    else
        tdrResults->thresholdLengthRaw = 0;
        
    return NS_STATUS_SUCCESS;
}

 
