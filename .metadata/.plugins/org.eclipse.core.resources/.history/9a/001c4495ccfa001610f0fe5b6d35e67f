//****************************************************************************
// epl_bist.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains all of the BIST related definitions and prototypes
//
//****************************************************************************

#ifndef _EPL_BIST_INCLUDE
#define _EPL_BIST_INCLUDE

#include "epl.h"

// EPL Function Prototypes
#ifdef __cplusplus
extern "C" {
#endif

EXPORT void
    EPLBistStartTxTest (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL psr15Flag);

EXPORT void
    EPLBistStopTxTest (
        IN PEPL_PORT_HANDLE portHandle);

EXPORT void
    EPLBistGetStatus (
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_BOOL *bistActiveFlag, 
        IN OUT NS_UINT *errDataNibbleCount );

#ifdef __cplusplus
}
#endif


#endif // _EPL_BIST_INCLUDE
