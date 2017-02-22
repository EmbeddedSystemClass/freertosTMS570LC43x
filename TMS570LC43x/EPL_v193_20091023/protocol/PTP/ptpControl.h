//****************************************************************************
// ptpControl.h
// 
// Copyright (c) 2007-2008 National Semiconductor Corporation.
// All Rights Reserved
//
//****************************************************************************

#ifndef _PTPCONTROL_INCLUDE
#define _PTPCONTROL_INCLUDE

#include "ptpd.h"
#include "epl.h"

#define STS_PSF_DATA    1
#define STS_OFFSET_DATA 2

typedef struct STS_OFFSET_DATA_STRUCT {
    TimeInternal offset_from_master;
    TimeInternal master_to_slave_delay;
    TimeInternal slave_to_master_delay;
    TimeInternal oneWayAvg;
} STS_OFFSET_DATA_STRUCT;

#ifdef __cplusplus
extern "C" {
#endif

EXPORT void PTPThread(
    IN PEPL_PORT_HANDLE portHandle,
    IN PyObject *guiObj,
    IN PyObject *stdioCallback,
    IN PyObject *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg);

EXPORT void PTPThreadC(
    IN PEPL_PORT_HANDLE portHandle,
    IN void *guiObj,
    IN void *stdioCallback,
    IN void *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg);

EXPORT void PTPKillThread(
    IN PEPL_PORT_HANDLE portHandle);

void PTPPrintf(
    NS_UINT type,
    NS_UINT8 *baseStr,
    ...);

#ifdef __cplusplus
}
#endif

#endif  // _PTPCONTROL_INCLUDE