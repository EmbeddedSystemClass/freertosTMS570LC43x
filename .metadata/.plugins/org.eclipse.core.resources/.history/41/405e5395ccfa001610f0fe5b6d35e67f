//****************************************************************************
// ifLPT.h
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ifLPT - Defines prototypes and defintions for MDIO interface on an LPT port
//****************************************************************************

#ifndef _LPT_INCLUDE
#define _LPT_INCLUDE

#include "epl.h"

// Define the interface to the MII bus through a LPT port.
// Bit 6 is Clock (active high), Bit 7 is data (active low)
#define MDC_PORT_OFFSET         0
#define PORT_MII_DATA_0         0xBF
#define PORT_MII_DATA_1         0x3F
#define PORT_MII_CLK_0          0x3F
#define PORT_MII_CLK_1          0x7F

// DATA bits are inverted when direct connection is used (no buffering)
#define PORT_MII_DIRECT_DATA_0  0x3F
#define PORT_MII_DIRECT_DATA_1  0xBF


// Version for FDI MDIO board
#define MDIO_OUT_PORT_OFFSET    0
#define MDIO_IN_PORT_OFFSET     1
#define MDC_FDI_PORT_OFFSET     2
#define MDIO_FDI_OUT_LOW        0xFF
#define MDIO_FDI_OUT_HIGH       0x7F
#define MDC_FDI_LOW             0x04
#define MDC_FDI_HIGH            0x0C

#define MDIO_IN_MASK            0x80

typedef enum {
    INT_NSC_MICRO_MDIO,
    INT_DIRECT_CONNECT,
    INT_FDI
}INTERFACE_TYPE;

NS_UINT
	ifLPTReadReg(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex);

void
	ifLPTWriteReg(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,
        IN NS_UINT value);

NS_BOOL	
    ifLPTMdioReadBit( 
        IN OAI_DEV_HANDLE oaiDevHandle);

void 
    ifLPTMdioWriteBit( 
        IN OAI_DEV_HANDLE oaiDevHandle, 
        IN NS_BOOL bit);

#endif // _LPT_INCLUDE
