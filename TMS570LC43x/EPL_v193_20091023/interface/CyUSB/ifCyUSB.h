//****************************************************************************
// ifCyUSB.c
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ifCyUSB - Access routines for Cypress USB access to PHY
//****************************************************************************

#ifndef _CYUSB_INCLUDE
#define _CYUSB_INCLUDE

#include "epl.h"

#ifdef __cplusplus
extern "C" {
#endif

EXPORT NS_STATUS
    ifCyUSB_Init( 
	    IN OAI_DEV_HANDLE oaiDevHandle);

EXPORT void
    ifCyUSB_DeInit( 
	    IN OAI_DEV_HANDLE oaiDevHandle);

NS_UINT
	ifCyUSB_ReadMDIO(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex);

void
	ifCyUSB_WriteMDIO(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,
		IN NS_UINT value);

#ifdef __cplusplus
}
#endif

#endif // _CYUSB_INCLUDE
