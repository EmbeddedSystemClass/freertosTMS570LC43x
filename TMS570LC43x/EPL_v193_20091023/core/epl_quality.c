//****************************************************************************
// epl_quality.c
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// Contains sources for DSP Cable Quality related functions.
//
// It implements the following functions:
//      EPLGetCableStatus
//      EPLDspGetLinkQuality
//      EPLSetDspLinkQualityThresholds
//****************************************************************************

#include "epl.h"


//****************************************************************************
EXPORT NS_STATUS
    EPLGetCableStatus(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT sampleTime,
        IN OUT NS_UINT *cableLength,
        IN OUT NS_SINT *freqOffsetValue,
        IN OUT NS_SINT *freqControlValue,
        IN OUT NS_UINT *varianceValue)
        
//  Returns various cable status values. This function is only supported on 
//  devices that have the EPL_CAPA_LINK_QUALITY capability. A valid 100 Mbps 
//  link must be established before calling this function.
//
//  The freqOffsetValue and freqControlValue values can be used to calculate 
//  jitter in ppm. To do this you must first multiply the returned frequency 
//  offset and control values by 5.1562, then take the abs function of the 
//  difference between frequency control and frequency offset 
//      (e.g. abs( freqControl - freqOffset)).
//
//  The SNR can be calculated from the returned varianceValue using the 
//  following formula:
//      varData = (288.0 * ((1024 * 1024 * sampleTime) / 8.0)) 
//                  / float( varianceValue)
//      rxSNR = 10.0 * math.log10( varData) 
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  sampleTime
//      Defines the length of time in milliseconds that the hardware will 
//      sample SNR / variance data. Valid values are: 2, 4, 6 or 8.
//  cableLength
//      Pointer to a NS_UINT variable that will be set on return to the 
//      estimated length of the cable in meters.
//  freqOffsetValue
//      Frequency offset value (see data sheet for details). To obtain 
//      frequency offset in ppm you must multiply this value by 5.1562.
//      (Signed value).
//  freqControlValue
//      Frequency control value (see data sheet for details). To obtain 
//      frequency control in ppm you must multiply this value by 5.1562.
//      (Signed value).
//  varianceValue
//      This is the raw variance value obtained from the hardware after 
//      sampling for the indicated length of time (sampleTime). It can be 
//      used to calculate an SNR value that indicates the quality of the 
//      link (See formula above).
//
//  Returns:
//      NS_STATUS_SUCCESS
//          Function was successfully executed.
//      NS_STATUS_FAILURE
//          Link NOT established or link is NOT at 100 Mbps.
//****************************************************************************
{
EPL_LINK_STS linksts;
NS_UINT count, reg;

    EPLGetLinkStatus( portHandle, &linksts);
    if ( !linksts.linkup || linksts.speed != 100)
        return NS_STATUS_FAILURE;

    *cableLength = EPLReadReg( portHandle, PHY_PG2_LEN100_DET) & P849_CABLE_LEN_MASK;

    EPLWriteReg( portHandle, PHY_PG2_FREQ100, P849_SAMPLE_FREQ);
    *freqOffsetValue = EPLReadReg( portHandle, PHY_PG2_FREQ100) & P849_FREQ_OFFSET_MASK;
    EPLWriteReg( portHandle, PHY_PG2_FREQ100, P849_SAMPLE_FREQ | P849_SEL_FC);
    *freqControlValue = EPLReadReg( portHandle, PHY_PG2_FREQ100) & P849_FREQ_OFFSET_MASK;

    // If negative, convert to negative signed integer.
    if ( *freqOffsetValue & 0x80)
        *freqOffsetValue = -1 * (0xFF - *freqOffsetValue + 1);
    if ( *freqControlValue & 0x80)
        *freqControlValue = -1 * (0xFF - *freqControlValue + 1);
    
    // Execute the SNR measurement for the specified time period
    reg = EPLReadReg( portHandle, PHY_PG2_VAR_CTRL) | P849_VAR_ENABLE;
    EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, reg | (sampleTime-2));

    // Wait for it to finish.
    count = 10;
    while ( !(EPLReadReg( portHandle, PHY_PG2_VAR_CTRL) & P849_VAR_RDY)) {
        if ( count == 0) 
            return NS_STATUS_FAILURE;
        count -= 1;
    }

    EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, reg | (sampleTime-2) | P849_VAR_FREEZE | P849_VAR_ENABLE);
    *varianceValue = EPLReadReg( portHandle, PHY_PG2_VAR_DATA);
    *varianceValue |= EPLReadReg( portHandle, PHY_PG2_VAR_DATA) << 16;
    // Don't let a 0 value through, clamp to 1 to keep from having the formula fault.
    if ( *varianceValue == 0)
        *varianceValue = 1;
        
    // Disable variance feature before leaving
    EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, reg & ~P849_VAR_ENABLE);
    return NS_STATUS_SUCCESS;
}

 
//****************************************************************************
EXPORT void
    EPLDspGetLinkQualityInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT PDSP_LINK_QUALITY_GET linkQualityStruct)
        
//  Returns the current status of the device's DSP link quality parameters 
//  and settings. The device must have the EPL_CAPA_LINK_QUALITY capability 
//  to use this function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  linkQualityStruct
//      Pointer to a link quality get structure that will be filled out on 
//      return.
//
//  Returns:
//      linkQualityStruct filled out on return.
//****************************************************************************
{
NS_UINT x, msk, select, lqmr;
NS_UINT *intPtr;
NS_BOOL *boolPtr;
NS_UINT savedVAR_CTRL;
NS_UINT rVal;

    linkQualityStruct->linkQualityEnabled = FALSE;
    lqmr = EPLReadReg( portHandle, PHY_PG2_LQMR);
    if ( lqmr & P849_LQM_ENABLE)
        linkQualityStruct->linkQualityEnabled = TRUE;
    
    msk = 0x0200;
    boolPtr = &linkQualityStruct->freqCtrlHighWarn;
    for ( x = 0; x < 10; x++)
    {
        *boolPtr = FALSE;
        if ( lqmr & msk)
            *boolPtr = TRUE;
        boolPtr++;
        msk >>= 1;
    }

    select = 0x0000;
    intPtr = &linkQualityStruct->c1LowThresh;
    for ( x = 0; x < 10; x++)
    {
        EPLWriteReg( portHandle, PHY_PG2_LQDR, select);
        *intPtr = (NS_SINT)EPLReadReg( portHandle, PHY_PG2_LQDR) & P849_LQ_THR_DATA_MASK;
        if ( (x != 2 && x != 3) && *intPtr > 0x7F)
            *intPtr = -1 * (0x100 - *intPtr);
        select += 0x0100;
        intPtr--;
    }
    
    select = 0x0000;
    intPtr = &linkQualityStruct->c1CtrlSample;
    for ( x = 0; x < 5; x++)
    {
        EPLWriteReg( portHandle, PHY_PG2_LQDR, select | P849_SAMPLE_PARAM);
        *intPtr = EPLReadReg( portHandle, PHY_PG2_LQDR) & P849_LQ_THR_DATA_MASK;
        if ( x != 1 && *intPtr & 0x80)
            *intPtr = -1 * (0x100 - *intPtr);
        select += 0x0200;
        intPtr--;
    }

    // Get the restart on flags - Do all but Var since it is in another register
    boolPtr = &linkQualityStruct->restartOnC1;
    rVal = EPLReadReg( portHandle, PHY_PG2_LQMR)>>10;
    for ( x = 0; x < 5; x++ ) {
        *boolPtr = ( rVal & 1 );
        rVal >>= 1;
        boolPtr++;
    }

    // Get dropLinkStatus
    linkQualityStruct->dropLinkStatus = ((EPLReadReg( portHandle, PHY_PCSR ) & P848_PCSR_SD_OPTION ) ? TRUE : FALSE);
 
    // Fill in the variance data for DP83640
    // Note, this assumes that the part is already configured and
    // Enabled as desired.  This means that a call to EPLDspSetLinkQualityThresholds
    // is required prior to making this call.
    linkQualityStruct->varianceSampleTime = 0;
    linkQualityStruct->varianceWarn = 0;
    linkQualityStruct->varianceHighThresh = 0;
    linkQualityStruct->varianceSample = 0;

    savedVAR_CTRL = EPLReadReg( portHandle, PHY_PG2_VAR_CTRL);

    linkQualityStruct->varianceEnable = (savedVAR_CTRL & P849_VAR_ENABLE);
    if( linkQualityStruct->varianceEnable  ) {

        // Read sample time out of register
        linkQualityStruct->varianceSampleTime = (savedVAR_CTRL & P849_VAR_TIMER_MASK)+2;

        // Read warn state
        linkQualityStruct->varianceWarn = (EPLReadReg( portHandle, PHY_PG2_LQMR2) & P640_VAR_HIGH_WARN);
        
        linkQualityStruct->restartOnVar = ((EPLReadReg( portHandle, PHY_PG2_LQMR2) & P640_RESTART_ON_VAR) ? TRUE : FALSE );

        // Read threshold low then high
        EPLWriteReg( portHandle, PHY_PG2_LQDR, 0xA00 );
        linkQualityStruct->varianceHighThresh  = ((NS_SINT)EPLReadReg( portHandle, PHY_PG2_LQDR) & P849_LQ_THR_DATA_MASK);
        EPLWriteReg( portHandle, PHY_PG2_LQDR, 0xB00 );
        linkQualityStruct->varianceHighThresh |= ((NS_SINT)EPLReadReg( portHandle, PHY_PG2_LQDR) & P849_LQ_THR_DATA_MASK)<<8;

        // Get actual variance data
        EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, savedVAR_CTRL | P849_VAR_FREEZE );
        linkQualityStruct->varianceSample =  EPLReadReg( portHandle, PHY_PG2_VAR_DATA);
        linkQualityStruct->varianceSample |= EPLReadReg( portHandle, PHY_PG2_VAR_DATA) << 16;
        // Don't let a 0 value through, clamp to 1 to avoid divide/0 fault.
        if ( linkQualityStruct->varianceSample == 0)
            linkQualityStruct->varianceSample = 1;
            
        // Restore feature before leaving
        EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, savedVAR_CTRL );
    }

    return;
}

 
//****************************************************************************
EXPORT void
    EPLDspSetLinkQualityConfig(
        IN PEPL_PORT_HANDLE portHandle,
        IN PDSP_LINK_QUALITY_SET linkQualityStruct)

//  Returns the current status of the device's DSP link quality parameters 
//  and settings. The device must have the EPL_CAPA_LINK_QUALITY capability 
//  to use this function.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  linkQualityStruct
//      Pointer to a link quality set structure holding the desired link 
//      quality settings.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT x, select;
NS_SINT *intPtr;
NS_UINT savedVAR_CTRL;
NS_BOOL *boolPtr;
NS_UINT rVal;

    intPtr = &linkQualityStruct->c1LowThresh;
    select = 0x0000;
    for ( x = 0; x < 10; x++)
    {
        EPLWriteReg( portHandle, PHY_PG2_LQDR, select | P849_WRITE_LQ_THR | (*intPtr & 0xFF));
        select += 0x0100;
        intPtr++;
    }

    // Create enable for restart on flags - Do all but Var since it is in another register
    boolPtr = &linkQualityStruct->restartOnC1;
    select = (1 << 10);
    rVal = 0;
    for ( x = 0; x < 5; x++ ) {
        if( *boolPtr )
            rVal |= select;
        select <<= 1;
        boolPtr++;
    }

    if ( linkQualityStruct->linkQualityEnabled)
        EPLWriteReg( portHandle, PHY_PG2_LQMR, (rVal | P849_LQM_ENABLE) );
    else
        EPLWriteReg( portHandle, PHY_PG2_LQMR, 0);

    // Set droplink status
    if( linkQualityStruct->dropLinkStatus )
        EPLWriteReg( portHandle, PHY_PCSR, (EPLReadReg( portHandle, PHY_PCSR) | P848_PCSR_SD_OPTION));
    else
        EPLWriteReg( portHandle, PHY_PCSR, (EPLReadReg( portHandle, PHY_PCSR) & !P848_PCSR_SD_OPTION));

    // Setup variance data for DP83640
    savedVAR_CTRL = EPLReadReg( portHandle, PHY_PG2_VAR_CTRL);
    EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, (savedVAR_CTRL & !P849_VAR_ENABLE));
    if( linkQualityStruct->varianceEnable  ) {

        // Set enable bit
        savedVAR_CTRL |= P849_VAR_ENABLE;

        // Read sample time out of register
        savedVAR_CTRL |= ((linkQualityStruct->varianceSampleTime-2) & P849_VAR_TIMER_MASK);

        // Write threshold low then high
        EPLWriteReg( portHandle, PHY_PG2_LQDR, 
            (0xA00 | P849_WRITE_LQ_THR | (linkQualityStruct->varianceHighThresh      & P849_LQ_THR_DATA_MASK )));
        EPLWriteReg( portHandle, PHY_PG2_LQDR, 
            (0xB00 | P849_WRITE_LQ_THR | ((linkQualityStruct->varianceHighThresh>>8) & P849_LQ_THR_DATA_MASK )));

        if( linkQualityStruct->restartOnVar )
            EPLWriteReg( portHandle, PHY_PG2_LQMR2, (EPLReadReg( portHandle, PHY_PG2_LQMR2) | P640_RESTART_ON_VAR ));

        // Now enable based on our parameters
        EPLWriteReg( portHandle, PHY_PG2_VAR_CTRL, savedVAR_CTRL );
    }

    return;
}
