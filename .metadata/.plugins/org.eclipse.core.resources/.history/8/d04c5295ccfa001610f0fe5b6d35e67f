//****************************************************************************
// ifLPT.c
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ifLPT - Implements the MDIO interface on an LPT port
//****************************************************************************

#include "epl.h"

unsigned int LptPortBase;

// MDIO Register Access Op Code's
#define MDIO_READ_OPCODE    0x60000000
#define MDIO_WRITE_OPCODE   0x50020000

// 0 = microMDIO, 1 = directIO, 2 = FDI board
INTERFACE_TYPE PortIoType;


//****************************************************************************
static void
    writeMiiPreambleAndIdle( 
        IN OAI_DEV_HANDLE oaiDevHandle)
// This is an internal function that is used to setup the bus
//****************************************************************************
{
NS_UINT i;

    // Clock out 32 idle bits and one extra idle bit.
    for ( i = 0; i < 33; i++) {
        // Clock out 1 idle bit.
        ifLPTMdioWriteBit( oaiDevHandle, TRUE);
    }
}


//****************************************************************************
NS_UINT
    ifLPTReadReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex)

//  Issues a register read operation through the LPT interface
//
//  oaiDevHandle
//      Handle that represents the device that the read operation should 
//      occur on. The definition of this is completely up to higher layer 
//      software.
//  regIndex
//      Index of the register to read. Bits 7:5 select the 
//      register page (000-pg0, 001-pg1, 010-pg3, 011-pg4, etc.).
//
//  Returns:
//      The value read from the register.
//****************************************************************************
{
NS_UINT data, i;

    // Default operation bit bang on LPT port
    writeMiiPreambleAndIdle( portHandle->oaiDevHandle );
    
    data = MDIO_READ_OPCODE | (portHandle->portMdioAddress<<23) | (regIndex << 18) | 0x0003FFFF;
     
    // Tell the PHY the register we want to read.
    for ( i = 0; i < 14; i++, data <<= 1)
    {
        ifLPTMdioWriteBit( portHandle->oaiDevHandle, data & 0x80000000);
    }

    // Turn around cycle
    ifLPTMdioWriteBit( portHandle->oaiDevHandle, TRUE);

    for ( data = 0, i = 0; i < 16; i++)
    {
        data <<= 1;
        if ( ifLPTMdioReadBit( portHandle->oaiDevHandle))
            data |= 1;
    }
    
    // One MDC clock cycle (idle) to end things
    ifLPTMdioWriteBit( portHandle->oaiDevHandle, TRUE);

    return data;
}


//****************************************************************************
void
    ifLPTWriteReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,
        IN NS_UINT value)

//  Issues a write operation through the LPT interface
//
//  portHandle
//      Handle that represents the device that the write operation should 
//      occur on.
//  regIndex
//      Index of the register to write. Bits 7:5 select the 
//      register page (000-pg0, 001-pg1, 010-pg3, 011-pg4, etc.).
//  value
//      The value to write to the register (0x0000 - 0xFFFF).
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT i, data;

   	// Default path bit bang on LPT
    data = MDIO_WRITE_OPCODE | (portHandle->portMdioAddress<<23) | (regIndex << 18) | value;

    writeMiiPreambleAndIdle( portHandle->oaiDevHandle );
    
    for ( i = 0; i < 32; i++, data <<= 1 )
    {
        ifLPTMdioWriteBit( portHandle->oaiDevHandle, data & 0x80000000);
    }

    // Clock one idle bit
    ifLPTMdioWriteBit( portHandle->oaiDevHandle, TRUE);

    return;
}

//****************************************************************************
NS_BOOL 
    ifLPTMdioReadBit( 
        IN OAI_DEV_HANDLE oaiDevHandle)

//  Reads one bit from the MDIO bus. This function must assert MDC, read 
//  the MDIO state, then de-assert MDC. In general there is a maximum MDIO 
//  clocking frequency of 25 MHz (40ns clock). If the environment could 
//  possibly allow MDIO clocking faster then this, this function should 
//  include a delay of at least 40ns so that the max. clocking frequency 
//  is not violated.
//
//  oaiDevHandle
//      Handle that represents the device that the read operation should 
//      occur on. The definition of this is completely up to higher layer 
//      software.
//  memPtr
//      Pointer to the memory block to free.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT32 mdio;

    if ( PortIoType == INT_FDI)
    {
        // MDO must be high when reading MDI
        WritePort( LptPortBase+MDC_FDI_PORT_OFFSET, MDC_FDI_LOW);
        WritePort( LptPortBase+MDC_FDI_PORT_OFFSET, MDC_FDI_HIGH);
        mdio = ReadPort( (NS_UINT16)(LptPortBase+MDIO_IN_PORT_OFFSET));
    } 
    else if ( PortIoType == INT_DIRECT_CONNECT)
    {
        WritePort( LptPortBase+MDC_PORT_OFFSET, PORT_MII_DIRECT_DATA_1 | PORT_MII_CLK_0);
        WritePort( LptPortBase+MDC_PORT_OFFSET, PORT_MII_DIRECT_DATA_1 | PORT_MII_CLK_1);
        // Tristate I/O drivers so we can use Data line as input
        WritePort( LptPortBase+2, 0x6C);
        mdio = ReadPort( (NS_UINT16)(LptPortBase+0));
        // Reenable port I/O drivers
        WritePort( LptPortBase+2, 0x0C);
    }
    else
    {
        // MDO must be high when reading MDI
        WritePort( LptPortBase+MDC_PORT_OFFSET, PORT_MII_DATA_1 | PORT_MII_CLK_0);
        WritePort( LptPortBase+MDC_PORT_OFFSET, PORT_MII_DATA_1 | PORT_MII_CLK_1);
        mdio = ReadPort( (NS_UINT16)(LptPortBase+MDIO_IN_PORT_OFFSET));
    }

    if( mdio & MDIO_IN_MASK )
        return TRUE;
    else
        return FALSE;
}

//****************************************************************************
void 
    ifLPTMdioWriteBit( 
        IN OAI_DEV_HANDLE oaiDevHandle, 
        IN NS_BOOL bit)

//  Writes one bit on the MDIO bus. This function must assert MDC, drive 
//  the MDIO input line as specified, then de-assert MDC. In general there 
//  is a maximum MDIO clocking frequency of 25 MHz (40ns clock). If the 
//  environment could possibly allow MDIO clocking faster then this, this 
//  function should include a delay of at least 40ns so that the max. 
//  clocking frequency is not violated.
//
//  oaiDevHandle
//      Handle that represents the device that the write operation should 
//      occur on. The definition of this is completely up to higher layer 
//      software.
//  bit
//      TRUE if a 1 should be written on the MDIO line, FALSE if a 0 should 
//      be written.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT mdio;

    if ( PortIoType == INT_FDI)
    {
        mdio = bit ? MDIO_FDI_OUT_HIGH : MDIO_FDI_OUT_LOW;
        WritePort( LptPortBase+MDC_FDI_PORT_OFFSET, MDC_FDI_LOW);
        WritePort( LptPortBase+MDIO_OUT_PORT_OFFSET, mdio);
        WritePort( LptPortBase+MDC_FDI_PORT_OFFSET, MDC_FDI_HIGH);
    } 
    else if ( PortIoType == INT_DIRECT_CONNECT) 
    {
        mdio = bit ? PORT_MII_DIRECT_DATA_1 : PORT_MII_DIRECT_DATA_0;
        WritePort( LptPortBase+MDC_PORT_OFFSET, mdio | PORT_MII_CLK_0);
        WritePort( LptPortBase+MDC_PORT_OFFSET, mdio | PORT_MII_CLK_1);
    } 
    else
    {
        mdio = bit ? PORT_MII_DATA_1 : PORT_MII_DATA_0;
        WritePort( LptPortBase+MDC_PORT_OFFSET, mdio | PORT_MII_CLK_0);
        WritePort( LptPortBase+MDC_PORT_OFFSET, mdio | PORT_MII_CLK_1);
    }
}