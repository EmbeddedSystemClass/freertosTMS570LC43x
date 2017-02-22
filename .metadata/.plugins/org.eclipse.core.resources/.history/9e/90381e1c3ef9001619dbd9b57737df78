//****************************************************************************
// epl_tdr.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains all of the TDR related definitions and prototypes
//
//****************************************************************************

#ifndef _EPL_TDR_INCLUDE
#define _EPL_TDR_INCLUDE

#include "epl.h"

#define TDR_CABLE_VELOCITY  4.64	// Not used...

typedef enum {
    CABLE_STS_TERMINATED,
    CABLE_STS_OPEN,
    CABLE_STS_SHORT,
    CABLE_STS_CROSS_SHORTED,
    CABLE_STS_UNKNOWN
} EPL_CABLE_STS_ENUM;

typedef struct TDR_RUN_REQUEST {
    NS_BOOL sendPairTx;
    NS_BOOL reflectPairTx;
    NS_BOOL use100MbTx;
    NS_UINT txPulseTime;
    NS_BOOL detectPosThreshold;
    NS_UINT rxDiscrimStartTime;
    NS_UINT rxDiscrimStopTime;
    NS_UINT rxThreshold;
} TDR_RUN_REQUEST,*PTDR_RUN_REQUEST;

typedef struct TDR_RUN_RESULTS {
    NS_BOOL thresholdMet;
    NS_UINT thresholdTime;
    NS_UINT thresholdLengthRaw;
    NS_UINT peakValue;
    NS_UINT peakTime;
    NS_UINT peakLengthRaw;
    NS_UINT adjustedPeakLengthRaw;
} TDR_RUN_RESULTS,*PTDR_RUN_RESULTS;

// EPL Function Prototypes
#ifdef __cplusplus
extern "C" {
#endif

EXPORT NS_UINT
    EPLInitTDR(
        IN PEPL_PORT_HANDLE portHandle);

EXPORT void 
    EPLDeinitTDR(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT savedLinkStatus);

EXPORT NS_UINT
    EPLMeasureTDRBaseline(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel);

EXPORT NS_STATUS
    EPLGetTDRPulseShape(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL use50nsPulse,
        IN OUT NS_SINT8 *positivePulseResults,
        IN OUT NS_SINT8 *negativePulseResults);

EXPORT NS_STATUS
    EPLGetTDRCableInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN OUT EPL_CABLE_STS_ENUM *cableStatus,
        IN OUT NS_UINT *rawCableLength);

EXPORT NS_BOOL
    EPLGatherTDRInfo(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT thresholdAdjustConstant,
        IN NS_BOOL stopAfterSuccess,
        IN OUT NS_UINT *baseline,
        IN OUT PTDR_RUN_RESULTS  posResultsArrayNoInvert,
        IN OUT PTDR_RUN_RESULTS  negResultsArrayNoInvert,
        IN OUT PTDR_RUN_RESULTS  posResultsArrayInvert,
        IN OUT PTDR_RUN_RESULTS  negResultsArrayInvert);

EXPORT NS_BOOL
    EPLShortTDRPulseRun(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT posThreshold,
        IN NS_UINT negThreshold,
        IN NS_BOOL noninvertedThreshold,
        IN NS_BOOL stopAfterSuccess,
        IN OUT PTDR_RUN_RESULTS  posResultsArray,
        IN OUT PTDR_RUN_RESULTS  negResultsArray);

EXPORT NS_BOOL
    EPLLongTDRPulseRun(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL useTxChannel,
        IN NS_BOOL useTxReflectChannel,
        IN NS_UINT threshold,
        IN NS_BOOL stopAfterSuccess,
        IN OUT PTDR_RUN_RESULTS  resultsArray);

EXPORT NS_STATUS
    EPLRunTDR(
        IN PEPL_PORT_HANDLE portHandle,
        IN PTDR_RUN_REQUEST tdrParms,
        IN OUT PTDR_RUN_RESULTS  tdrResults);

#ifdef __cplusplus
}
#endif

#endif // _EPL_TDR_INCLUDE
