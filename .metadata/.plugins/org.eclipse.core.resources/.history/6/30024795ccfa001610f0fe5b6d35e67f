//****************************************************************************
// epl_miiconfig.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains all of the MII related definitions and prototypes
//
//****************************************************************************

#ifndef _EPL_MII_INCLUDE
#define _EPL_MII_INCLUDE

#include "epl.h"

typedef enum EPL_MIICFG_ENUM {
    MIIPCFG_UNKNOWN,
    MIIPCFG_NORMAL,
    MIIPCFG_PORT_SWAP,
    MIIPCFG_EXT_MEDIA_CONVERTER,
    MIIPCFG_BROADCAST_TX_PORT_A,
    MIIPCFG_BROADCAST_TX_PORT_B,
    MIIPCFG_MIRROR_RX_CHANNEL_A,
    MIIPCFG_MIRROR_RX_CHANNEL_B,
    MIIPCFG_DISABLE_PORT_A,
    MIIPCFG_DISABLE_PORT_B
}EPL_MIICFG_ENUM;

// EPL Function Prototypes
#ifdef __cplusplus
extern "C" {
#endif

EXPORT EPL_MIICFG_ENUM
    EPLGetMiiConfig(
        IN PEPL_DEV_HANDLE deviceHandle);

EXPORT void
    EPLSetMiiConfig(
        IN PEPL_DEV_HANDLE deviceHandle,
        IN EPL_MIICFG_ENUM miiPortConfig);

#ifdef __cplusplus
}
#endif

#endif // _EPL_MIIINCLUDE
