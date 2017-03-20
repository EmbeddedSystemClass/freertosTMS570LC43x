//****************************************************************************
// oai.c (Windows Version)
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// OS Abstraction Interface (OAI) implementation for Windows.
//****************************************************************************

// Prevent inclusion of winsock.h in windows.h will be added as part 
// epl.h by way of ptp stack includes.
#include <stdlib.h>
#include "FreeRTOS.h"
#include "os_semphr.h"


#include "epl_platform.h"

//****************************************************************************
void 
	OAIInitialize( 
		OAI_DEV_HANDLE oaiDevHandle)

//  Called by EPL to initialize the OAI layer.
//
//  oaiDevHandle
//      Handle that represents the device. The definition of this is 
//      completely up to higher layer software.
//
//  Returns:
//      Nothing
//****************************************************************************
{
    if (!oaiDevHandle->multiOpMutex) {
        oaiDevHandle->multiOpMutex = xSemaphoreCreateMutex();
    }
    if (!oaiDevHandle->regularMutex) {
        oaiDevHandle->regularMutex = xSemaphoreCreateMutex();
    }
    
}

//****************************************************************************
void
	OAIBeginCriticalSection( 
		xSemaphoreHandle hMutex )

//  Begins a critical section given an arbitrary mutex handle.
//  This provides a more flexible method of managing
//
//  Returns:
//      Nothing
//****************************************************************************
{
    if(!xSemaphoreTake(hMutex, 1000)) {
    	//TODO: implement
//        PLATFORM_ASSERT("EPL_OAI", "xSemaphoreTake timeout");
    }
    return;
}

//****************************************************************************
void
	OAIEndCriticalSection( 
		xSemaphoreHandle hMutex )

//  Ends a critical section given an arbitrary mutex handle.
//  This provides a more flexible method of managing
//
//  Returns:
//      Nothing
//****************************************************************************
{
    xSemaphoreGive(hMutex);
    return;
}

//****************************************************************************
void 
    OAIBeginRegCriticalSection(
        OAI_DEV_HANDLE oaiDevHandle)
//****************************************************************************
{
    OAIBeginCriticalSection( oaiDevHandle->regularMutex);
    return;
}


//****************************************************************************
void 
    OAIEndRegCriticalSection(
        OAI_DEV_HANDLE oaiDevHandle)
//****************************************************************************
{
    OAIEndCriticalSection( oaiDevHandle->regularMutex);
    return;
}


//****************************************************************************
void 
    OAIBeginMultiCriticalSection(
        OAI_DEV_HANDLE oaiDevHandle)
//****************************************************************************
{
    OAIBeginCriticalSection( oaiDevHandle->multiOpMutex);
    return;
}


//****************************************************************************
void 
    OAIEndMultiCriticalSection(
        OAI_DEV_HANDLE oaiDevHandle)
//****************************************************************************
{
    OAIEndCriticalSection( oaiDevHandle->multiOpMutex );
    return;
}
