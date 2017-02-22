//****************************************************************************
// epl_quality.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains all of the quality related definitions and prototypes
//
//****************************************************************************

#ifndef _EPL_QUALITY_INCLUDE
#define _EPL_QUALITY_INCLUDE

#include "epl.h"

typedef struct DSP_LINK_QUALITY_GET {
    NS_BOOL   linkQualityEnabled;
    // The following NS_BOOL fields MUST be in this order.
    NS_BOOL   freqCtrlHighWarn;
    NS_BOOL   freqCtrlLowWarn;
    NS_BOOL   freqOffHighWarn;
    NS_BOOL   freqOffLowWarn;
    NS_BOOL   dblwHighWarn;
    NS_BOOL   dblwLowWarn;
    NS_BOOL   dagcHighWarn;
    NS_BOOL   dagcLowWarn;
    NS_BOOL   c1HighWarn;
    NS_BOOL   c1LowWarn;
    // The following NS_UINT fields MUST be in this order.
    NS_SINT   freqCtrlHighThresh;
    NS_SINT   freqCtrlLowThresh;
    NS_SINT   freqOffHighThresh;
    NS_SINT   freqOffLowThresh;
    NS_SINT   dblwHighThresh;
    NS_SINT   dblwLowThresh;
    NS_UINT   dagcHighThresh;
    NS_UINT   dagcLowThresh;
    NS_SINT   c1HighThresh;
    NS_SINT   c1LowThresh;
    NS_SINT   freqCtrlSample;
    NS_SINT   freqOffSample;
    NS_SINT   dblwCtrlSample;
    NS_UINT   dagcCtrlSample;
    NS_SINT   c1CtrlSample;

    NS_BOOL   restartOnC1;
    NS_BOOL   restartOnDAGC;
    NS_BOOL   restartOnDBLW;
    NS_BOOL   restartOnFreq;
    NS_BOOL   restartOnFC;
    NS_BOOL   restartOnVar;
    NS_BOOL   dropLinkStatus;

    // DP83640 only variance values
    NS_BOOL   varianceEnable;
    NS_UINT8  varianceSampleTime;
    NS_BOOL   varianceWarn;
    NS_UINT   varianceHighThresh;
    NS_UINT   varianceSample;

}DSP_LINK_QUALITY_GET,*PDSP_LINK_QUALITY_GET;

typedef struct DSP_LINK_QUALITY_SET {
    NS_BOOL   linkQualityEnabled;
    // The following NS_UINT fields MUST be in this order.
    NS_SINT   c1LowThresh;
    NS_SINT   c1HighThresh;
    NS_UINT   dagcLowThresh;
    NS_UINT   dagcHighThresh;
    NS_SINT   dblwLowThresh;
    NS_SINT   dblwHighThresh;
    NS_SINT   freqOffLowThresh;
    NS_SINT   freqOffHighThresh;
    NS_SINT   freqCtrlLowThresh;
    NS_SINT   freqCtrlHighThresh;

    NS_BOOL   restartOnC1;
    NS_BOOL   restartOnDAGC;
    NS_BOOL   restartOnDBLW;
    NS_BOOL   restartOnFreq;
    NS_BOOL   restartOnFC;
    NS_BOOL   restartOnVar;
    NS_BOOL   dropLinkStatus;

    // DP83640 only variance values
    NS_BOOL   varianceEnable;
    NS_UINT8  varianceSampleTime;
    NS_UINT   varianceHighThresh;
}DSP_LINK_QUALITY_SET,*PDSP_LINK_QUALITY_SET;

// EPL Function Prototypes
#ifdef __cplusplus
extern "C" {
#endif

EXPORT NS_STATUS
    EPLGetCableStatus (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT sampleTime,
        IN OUT NS_UINT *cableLength,
        IN OUT NS_SINT *freqOffsetValue,
        IN OUT NS_SINT *freqControlValue,
        IN OUT NS_UINT *varianceValue);

EXPORT void
    EPLDspGetLinkQualityInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT PDSP_LINK_QUALITY_GET linkQualityStruct);

EXPORT void
    EPLDspSetLinkQualityConfig(
        IN PEPL_PORT_HANDLE portHandle,
        IN PDSP_LINK_QUALITY_SET linkQualityStruct);

#ifdef __cplusplus
}
#endif

#endif // _EPL_QUALITY_INCLUDE
