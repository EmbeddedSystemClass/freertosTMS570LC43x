//****************************************************************************
// epl_bist.c
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// Contains sources for Built In Self Test (BIST) related functions.
//
// It implements the following functions:
//      EPLBistStartTxTest
//      EPLBistStopTxTest
//      EPLBistGetStatus
//****************************************************************************

#include "epl.h"

//****************************************************************************
EXPORT void
    EPLBistStartTxTest(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL psr15Flag)
        
//  Starts Transmit Built-in Self Test (BIST).
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  psr15Flag
//      Set to TRUE to use 15-bit pseudo random data, FALSE to use 9-bit 
//      pseudo random data.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT phyctrl;

    phyctrl = EPLReadReg( portHandle, PHY_PHYCTRL);
    if ( psr15Flag)
        phyctrl |= P848_PHYCTRL_PSR_15;
    else
        phyctrl &= ~P848_PHYCTRL_PSR_15;
    phyctrl |= P848_PHYCTRL_BIST_START;
    EPLWriteReg( portHandle, PHY_PHYCTRL, phyctrl);
    return;
}

 
//****************************************************************************
EXPORT void
    EPLBistStopTxTest(
        IN PEPL_PORT_HANDLE portHandle)
        
//  Halts a previously started BIST test.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT phyctrl;

    phyctrl = EPLReadReg( portHandle, PHY_PHYCTRL);
    phyctrl &= ~P848_PHYCTRL_BIST_START;
    EPLWriteReg( portHandle, PHY_PHYCTRL, phyctrl);
}
 
 
//****************************************************************************
EXPORT void
    EPLBistGetStatus(
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_BOOL *bistActiveFlag,
        IN OUT NS_UINT *errDataNibbleCount)
        
//  Returns BIST status information.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  bistActiveFlag
//      Pointer to a Boolean variable that will be set on return to TRUE if 
//      transmit BIST is currently enabled, FALSE otherwise.
//  errDataNibbleCount
//      Pointer to a NS_UINT variable that will be set on return to the 
//      number of errored data nibbles dectected so far.
//
//  Returns:
//      bistActiveFlag and errDataNibbleCount are set on return.
//****************************************************************************
{
    *bistActiveFlag = FALSE;
    if ( EPLReadReg( portHandle, PHY_PHYCTRL) & P848_PHYCTRL_BIST_START)
        *bistActiveFlag = TRUE;
        
    *errDataNibbleCount = (EPLReadReg( portHandle, PHY_CDCTRL1) & P848_CDCTRL1_BIST_EC_MSK) >> 8;
    return;
}  