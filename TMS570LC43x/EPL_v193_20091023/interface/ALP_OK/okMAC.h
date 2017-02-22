//****************************************************************************
// okMAC.h
// 
// Copyright (c) 2007-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ALP based FPGA MAC Definitions
//****************************************************************************

#ifndef _MAC_INCLUDE
#define _MAC_INCLUDE

#include "epl.h"

typedef struct PKT_LIST {
    NS_UINT8 pType;
    NS_UINT  nPkt;
    NS_UINT  pSize;
    NS_UINT8 *pPacket;
    struct PKT_LIST  *nxtPkt;
} PKT_LIST;

#ifdef __cplusplus
extern "C" {
#endif

EXPORT NS_STATUS
	MACInitialize( 
	    IN OAI_DEV_HANDLE oaiDevHandle);

EXPORT void 
	MACDeInitialize( 
	    IN OAI_DEV_HANDLE oaiDevHandle);

EXPORT void 
	MACSendPacket(
	    IN PEPL_PORT_HANDLE eplPortHandle,
	    IN NS_UINT8 *txBuf,
	    IN NS_UINT length);

EXPORT void 
	MACSendPacketNoUdpChecksum(
	    IN PEPL_PORT_HANDLE eplPortHandle,
		IN NS_UINT8 *txBuf,
		IN NS_UINT length);

EXPORT void 
	MACFlushReceiveFifos(
		IN PEPL_PORT_HANDLE eplPortHandle);

EXPORT NS_UINT
    MACReceivePacket(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8  *rxBuf,
        OUT NS_UINT *length);

EXPORT void 
	PythonReload( 
		void);

NS_UINT
	MACReadReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex);

void
	MACWriteReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,
        IN NS_UINT value);

NS_UINT
	MACMIIReadReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT8 *readRegRequestPacket,
        IN NS_UINT length);

void
	MACMIIWriteReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT8 *writeRegRequestPacket,
		IN NS_UINT length);

EXPORT void 
	SetDuplex( 
	    IN PEPL_PORT_HANDLE portHandle,
	    IN NS_BOOL halfDuplex);

EXPORT NS_UINT16
    CalcChecksum( 
        IN NS_UINT8 *buf, 
        IN NS_UINT len, 
        IN NS_UINT chksum);

EXPORT void 
    FPGAWriteReg( 
        IN okUSBFRONTPANEL_HANDLE okHandle,
        IN NS_UINT regIndex, 
        IN NS_UINT regValue);

#ifdef __cplusplus
}
#endif

#endif // _MAC_INCLUDE
