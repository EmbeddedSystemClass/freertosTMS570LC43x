//****************************************************************************
// okMAC.c
// 
// Copyright (c) 2007-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ALP based FPGA MAC Functions for the DP83640
//****************************************************************************

#include <winsock2.h>	// needed for htons(...) and ntohs(...)
#include "epl.h"
//#include "okMAC.h"

// Local prototypes
NS_UINT8 *
    intGetNextPhyMessage (
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_UINT8 *msgLocation,
        IN OUT PHYMSG_MESSAGE_TYPE_ENUM *messageType,
        IN OUT PHYMSG_MESSAGE *phyMessageOut,
        IN NS_BOOL usePSFList);

NS_UINT
    intMACReceivePacket(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *rxBuf,
        OUT NS_UINT *length,
        IN NS_BOOL  usePktList );


#define ALP_MAX_BOARD   2   // ALP board # max
#define ALP_MAX_CONN    4   // ALP board max # connectors 
#define ALP_MAX_ID      8   // ALP board max # devices (I2C addresses)

typedef struct OK_LOCAL_DATA_STRUCT {
    NS_BOOL bInitialized;
    okUSBFRONTPANEL_HANDLE okHandle[ALP_MAX_BOARD];
    NS_UINT connRegValue;
    HANDLE regularMutex;
} OK_LOCAL_DATA_STRUCT;

OK_LOCAL_DATA_STRUCT okLocalDataStruct;
OK_LOCAL_DATA_STRUCT *okLocalData;

#ifdef __cplusplus
extern "C" {
#endif

extern LPVOID lpvMem;

#ifdef __cplusplus
}
#endif

// ALP FPGA MAC Endpoints to our Netlist
ALP_ENDPOINTS_STRUCT conn1EndPoints =
    { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x20, 0x22,
      0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x48, 
      0x41, 0x42, 0x43, 0x68, 0x61, 0x62, 0x88, 0x81, 
      0xA1, 0xA2 };

ALP_ENDPOINTS_STRUCT conn3EndPoints =
    { 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x30, 0x32,
      0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x50,
      0x51, 0x52, 0x53, 0x70, 0x71, 0x72, 0x90, 0x91,
      0xB1, 0xB2 };

NS_UINT8 pcfDA0[6]   = {0x08, 0x00, 0x17, 0x0B, 0x6B, 0x0F};
NS_UINT8 pcfDA1[6]   = {0x08, 0x00, 0x17, 0x00, 0x00, 0x00};
NS_UINT8 pcfStart[6] = {0x5F, 0x50, 0x48, 0x59, 0x43, 0x46};

//****************************************************************************
NS_UINT 
    okReadEEPROM( 
        HANDLE okH, 
        NS_UINT conn, 
        NS_UINT iAddr, 
        NS_UINT mAddr, 
        NS_UINT nLen, 
        NS_UINT8 *outBuf )
//  Internal procedure called to initialize the Opal Kelly/ALP board
//
//  okH     - Handle to Opal Kelly interface to use
//  conn    - connector (0-3) to use
//  iAddr   - i2C address (0-7) to use
//  mAddr   - memory location/offset to read
//  nLen    - number of bytes to read
//  outBuf  - array of bytes to be filled in by this call
//  
//  Returns:
//      NS_UINT - Number of bytes read (0 on error)
//****************************************************************************
{
NS_UINT  offset;
NS_UINT8 cmdPacket[10];
NS_UINT8 cmdResponse[32];
NS_UINT8 length[2];
NS_UINT  nTimeOut;

    for( offset=0; offset < nLen; offset++ ) {

        *(NS_UINT16 *)&cmdPacket[0] = 0x0003;   // 16-bit length of cmd packet (0x0003)
        *(NS_UINT16 *)&cmdPacket[2] = 0x8000;   // Register read eeprom code (0x8000)
        *(NS_UINT16 *)&cmdPacket[4] = (NS_UINT16)(conn<<11) | (NS_UINT16)(iAddr<<8) | (NS_UINT16)((mAddr+offset) & 0x00FF);

        okUsbFrontPanel_ActivateTriggerIn( okH, 0x40, 0x0001 );
        okUsbFrontPanel_WriteToPipeIn( okH, 0x80, 6, cmdPacket );
        
        nTimeOut = 100;
        okUsbFrontPanel_UpdateTriggerOuts( okH );
        while ( !okUsbFrontPanel_IsTriggered( okH, 0x60, 0x01 ) && nTimeOut ) {
            okUsbFrontPanel_UpdateTriggerOuts( okH );
            nTimeOut--;
        }
            
        if( !nTimeOut ) {
            break;
        }

        okUsbFrontPanel_ReadFromPipeOut( okH, 0xA0, 2L, length );
        okUsbFrontPanel_ReadFromPipeOut( okH, 0xA0, (long)(length[0]*2), cmdResponse );

        if( *(NS_UINT16 *)&cmdResponse[0]==0x8000 ){ // CMD_EEPROM_READ_DONE - 0x8000
            if( cmdResponse[3]==0x00 ) {
                *(outBuf+offset) = cmdResponse[2];
            } // if( ACK )
            else
                break;
        } // if( CMD_EEPROM_READ_DONE )
        else
            break;

    } // for( offset... )

    return( offset );
}

//****************************************************************************
okUSBFRONTPANEL_HANDLE 
    okInitialize(
	    IN OAI_DEV_HANDLE oaiDevHandle)
//  Internal procedure called to initialize the Opal Kelly/ALP board
//  This code shows how to iterate through the ok interface and find ALP boards
//  and what is attached to the connector(s).  In this case we wouldn't really
//  need to do that since we simply want to find the first board and get the
//  FPGA properly setup.  We could just as easily assume where the device is
//
//  Nothing in
//
//  Returns:
//      okUSBFRONTPANEL_HANDLE to newly initialized Opal Kelly interface
//****************************************************************************
{
okUSBFRONTPANEL_HANDLE okH;
NS_UINT   numALPBoards;

NS_SINT8  tBuf[256];
NS_SINT8  *pBuf = &tBuf[0];
NS_UINT   tInt;

NS_UINT   nALPBoard;
NS_UINT   nDevAddr;

    // Load the library, if it is already loaded (which it should be)
    // this will simply return - no harm done.
    okFrontPanelDLL_LoadLib( NULL );

    // Create the OK Object
    okH = okUsbFrontPanel_Construct();

    if( okH ) {

        // Find out how many boards there are
        numALPBoards = okUsbFrontPanel_GetDeviceCount( okH );

        if( oaiDevHandle->board >= numALPBoards ) {
            return NULL;
        }
        nALPBoard = oaiDevHandle->board;

        tInt = sizeof( tBuf );
        okUsbFrontPanel_GetDeviceListSerial( okH, nALPBoard, pBuf, tInt );

        if( okUsbFrontPanel_OpenBySerial( okH, pBuf ) != ok_NoError ) {
            return NULL;
        }

        if( okUsbFrontPanel_LoadDefaultPLLConfiguration( okH ) != ok_NoError ) {
            return NULL;
        }

        // Load basic alp netlist
        if( okUsbFrontPanel_ConfigureFPGA( okH, "alp.bit" ) != ok_NoError ) {
            return NULL;
        }

        // Perform a reset on the FPGA to load new netlist
        okUsbFrontPanel_ActivateTriggerIn( okH, 0x40, 0x0000 );

        for( nDevAddr=0; nDevAddr< ALP_MAX_ID; nDevAddr++ ) {   // For each ID on connector

            // Attempt to read data from the EEPROM so we can verify the type of device
            // we are talking to.
            tInt = okReadEEPROM( okH, oaiDevHandle->connector, nDevAddr, 0x0000, 128, (NS_UINT8 *)tBuf );
            if( tInt != 0 ){

                // We can examine the EEPROM data here to determine which board we have
                // and various parameters about it.  For now we will assume a DP83640
                // board since that is what this code is written for.
                if( tBuf[0]!='A' || tBuf[1]!='L' || tBuf[2]!='P' || tBuf[3]!=0x00 ){
                    // We don't have a valid ALP board
                    continue;
                }

                // Now we know we have a board.
                if( okUsbFrontPanel_LoadDefaultPLLConfiguration( okH ) != ok_NoError ) {
                    continue;
                }

                // Load DP83640 netlist
                if( okUsbFrontPanel_ConfigureFPGA( okH, "dp83640.bit" ) != ok_NoError ) {
                    continue;
                }

                // Perform a reset on the FPGA to load new netlist
                okUsbFrontPanel_ActivateTriggerIn( okH, 0x40, 0x0000 );
        
                // Reset the extension board hardware
                okUsbFrontPanel_SetWireInValue( okH, 0x00, 0x02, 0xFFFF );
                okUsbFrontPanel_UpdateWireIns( okH );
                okUsbFrontPanel_SetWireInValue( okH, 0x00, 0x00, 0xFFFF );
                okUsbFrontPanel_UpdateWireIns( okH );

                // Reset RAM
                okUsbFrontPanel_ActivateTriggerIn( okH, 0x41, 0x0000 );
                return okH;
            }  // if( tInt != 0 )
        } // for( nDevAddr...)
    } // if( okH )

    // If we got here we didn't actually find anything.
    if( okH ) {
        // Destroy the oK object
        okUsbFrontPanel_Destruct( okH);
    }
    return NULL;    //okH;
}

NS_BOOL okCheck(
    OAI_DEV_HANDLE oaiDevHandle )
{
NS_UINT8  nI2CAddr;
NS_UINT8  tInt;
NS_SINT8  tBuf[256];

    for( nI2CAddr=0; nI2CAddr< ALP_MAX_ID; nI2CAddr++ ) {  // For each I2C Address on connector

        // Attempt to read data from the EEPROM so we can verify the type of device
        // we are talking to.
        tInt = okReadEEPROM( oaiDevHandle->ifHandle, oaiDevHandle->connector, nI2CAddr, 0x0000, 128, (NS_UINT8 *)tBuf );
        if( tInt != 0 ){
            // We can examine the EEPROM data here to determine which board we have
            // and various parameters about it.  For now we will assume a DP83640
            // board since that is what this code is written for.
            if( tBuf[0]!='A' || tBuf[1]!='L' || tBuf[2]!='P' || tBuf[3]!=0x00 ){
                // We don't have a valid ALP board
                continue;
            }
            else {
                return TRUE;
            }
        }
    } // for( nI2CAddr... )

    return FALSE;
}

//****************************************************************************
EXPORT NS_STATUS
    MACInitialize( 
	    IN OAI_DEV_HANDLE oaiDevHandle)
//
//  Parameters
//    oaiDevHandle
//      Handle that represents the MDIO bus that the write operation should 
//      occur on. The definition of this is completely up to higher layer software.
//
//  Return Value
//      NS_STATUS_SUCCESS - Function was successfully executed.
//      NS_STATUS_FAILURE - Function was not able to initialize the interface.  
//                          This usually means that a device was not found.
//
//  Comments
//      This call is not usually called directly.  It is typically called from 
//      the EPLEnumDevice() function if it hasn’t already been initialized.
//      The input to this call is an OAI_DEV_HANDLE.  The connector member 
//      of that structure is used to define which connector on the ALP board 
//      to look for a PHY device.  NS_STATUS_FAILURE will be returned if a 
//      device isn’t found.  
//
//****************************************************************************
{
	// Use the value of the okHandle and ifHandle to determine if this is 
    // the 1st or 2nd MAC for each board
    // Based on the ALP connector, setup the FPGA endpoints we'll use.
    if( oaiDevHandle->board >= ALP_MAX_BOARD ) {
        // Unknown board number, default to 0;
        oaiDevHandle->board = 0;
    }

    //okLocalData = (OK_LOCAL_DATA_STRUCT *)lpvMem;
    okLocalData = (OK_LOCAL_DATA_STRUCT *)&okLocalDataStruct;

    if( !okLocalData->bInitialized ) {
        // Opportunity to initialize the DLL Global data
        okLocalData->bInitialized = TRUE;
    }

	if( !okLocalData->okHandle[oaiDevHandle->board] )
    {
        if( !oaiDevHandle->ifHandle ) {
			okLocalData->okHandle[oaiDevHandle->board] = oaiDevHandle->ifHandle = okInitialize( oaiDevHandle );
            if( !okLocalData->okHandle[oaiDevHandle->board] ) {
                return NS_STATUS_FAILURE;
            }
        }
        else {
			okLocalData->okHandle[oaiDevHandle->board] = oaiDevHandle->ifHandle;
        }

        okLocalData->connRegValue = 0;
        // Normal 1st board operation
        if( oaiDevHandle->connector == 0 ) okLocalData->connRegValue |= 0x00;
        if( oaiDevHandle->connector == 1 ) okLocalData->connRegValue |= 0x04;
        if( oaiDevHandle->connector == 2 ) okLocalData->connRegValue |= 0x08;
        if( oaiDevHandle->connector == 3 ) okLocalData->connRegValue |= 0x0C;
        FPGAWriteReg( okLocalData->okHandle[oaiDevHandle->board], 0x0007, okLocalData->connRegValue);
        memcpy( &oaiDevHandle->alpEP, &conn1EndPoints, sizeof( ALP_ENDPOINTS_STRUCT));
	    okLocalData->regularMutex = oaiDevHandle->regularMutex = OAICreateMutex();
    }
    else
    {
        // Normal 2nd connector processing
		if( !oaiDevHandle->ifHandle )
            oaiDevHandle->ifHandle = okLocalData->okHandle[oaiDevHandle->board];

        if( !okCheck( oaiDevHandle ) ) {
            oaiDevHandle->ifHandle = NULL;
            return NS_STATUS_FAILURE;
        }

        if( oaiDevHandle->connector == 0 ) okLocalData->connRegValue |= 0x00;
        if( oaiDevHandle->connector == 1 ) okLocalData->connRegValue |= 0x01;
        if( oaiDevHandle->connector == 2 ) okLocalData->connRegValue |= 0x02;
        if( oaiDevHandle->connector == 3 ) okLocalData->connRegValue |= 0x03;
        FPGAWriteReg( okLocalData->okHandle[oaiDevHandle->board], 0x0007, okLocalData->connRegValue);
        memcpy( &oaiDevHandle->alpEP, &conn3EndPoints, sizeof( ALP_ENDPOINTS_STRUCT));
        oaiDevHandle->regularMutex = okLocalData->regularMutex;
    }
        
    oaiDevHandle->multiOpMutex = OAICreateMutex();

    return NS_STATUS_SUCCESS;
}

//****************************************************************************
EXPORT void
    MACDeInitialize( 
	    IN OAI_DEV_HANDLE oaiDevHandle)
//
//  Parameters:
//      oaiDevHandle
//        Handle that represents the MDIO bus that the write operation should 
//        occur on. The definition of this is completely up to higher layer software.
//
//  Return Value
//      Nothing
//
//  Comments
//      This call is not usually called directly.  It is typically called 
//      from the EPLDeInitialize() function as part of the overall EPL 
//      shutdown process.
//****************************************************************************
{
	if( oaiDevHandle->ifHandle )
		okUsbFrontPanel_Destruct( oaiDevHandle->ifHandle);

	// Unload the okFrontPanel.dll if it is loaded.
	okFrontPanelDLL_FreeLib();

	okLocalData->okHandle[oaiDevHandle->board] = oaiDevHandle->ifHandle = NULL;
	return;
}

//****************************************************************************
void 
    sendPacketNoUdpChecksum(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *txBuf,
        IN NS_UINT length,
        IN NS_BOOL genUdpChecksum)
//
//  This is an internal procedure that is used to send data.
//
//  Parameters
//      eplPortHandle
//          Handle to the port to send the data.
//      txBuf
//          Pointer to the packet of data to send.
//      length
//          Length of the data packet to be sent.
//      genUdpChecksum
//          Flag to determine whether or not to calculate/set the UDP checksum
//
//  Returns:
//      Nothing
//
//  Comments:
//      Sends a packet through the FPGA's MAC. This function calculates
//      and sets the IP & UDP checksum fields.
//****************************************************************************
{
PPORT_OBJ portHdl = (PPORT_OBJ)eplPortHandle;
OAI_DEV_HANDLE oaiDevHandle = portHdl->oaiDevHandle;
okUSBFRONTPANEL_HANDLE okHdl;
NS_UINT8 *ipHead, *udpHead;
NS_UINT chksum;
NS_UINT nTimeout;

    // If we have a PCF, bypass all processing
    if ( memcmp( txBuf, pcfDA0, 6 ) != 0 && memcmp( txBuf, pcfDA1, 6 ) != 0 ) {
        // Calc IP header checksum
        ipHead = &txBuf[14];
        
        // IP header?
        if ( length > 14 && txBuf[12] == 0x08 && txBuf[13] == 0x00 ) {
            *(NS_UINT16*)&ipHead[10] = 0x0000;
            *(NS_UINT16*)&ipHead[10] = htons( CalcChecksum( ipHead, 20, 0x0000 ) );
    
            // UDP header?
            if ( length > 34 && ipHead[9] == 17 ) {
                // Calc UDP header checksum
                udpHead = &ipHead[20];
                
                if ( genUdpChecksum ) {
                    *(NS_UINT16*)&udpHead[6] = 0x0000;  // 0 chksum

                    if ( oaiDevHandle->udpChksumEnable) {
                        chksum = 0x0000;
                        chksum += ntohs( *(NS_UINT16*)&ipHead[12] );  // Pseudo hdr
                        chksum += ntohs( *(NS_UINT16*)&ipHead[14] );
                        chksum += ntohs( *(NS_UINT16*)&ipHead[16] );
                        chksum += ntohs( *(NS_UINT16*)&ipHead[18] );
                        chksum += 0x0011;
                        chksum += ntohs( *(NS_UINT16*)&udpHead[4] );
                        *(NS_UINT16*)&udpHead[6] = htons( CalcChecksum( udpHead, length-14-20, chksum ) );
                    } // if( updChksumEnable )
                }  // if( genUpdChecksum )
            }  // if( upd header check )
        }  // if( IP header check )
    }  // if( not PCF )

    // Move the packet data into the FPGA tx buffer.
    okHdl = oaiDevHandle->ifHandle;
    
    OAIBeginRegCriticalSection( oaiDevHandle );
    
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.DATA_FIFO_LOAD, 0x0000, 0xFFFF );  // Tx buf addr
    okUsbFrontPanel_UpdateWireIns( okHdl );
    okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MAC_CTRL, 1 );
    okUsbFrontPanel_WriteToPipeIn( okHdl, oaiDevHandle->alpEP.TX_FIFO_WR_DATA, (length+1)&0xFFFE, txBuf );
    
    // Initiate the transmit
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_TX_FRAME_SIZE, length, 0xFFFF );  // Tx frame len
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.DATA_FIFO_LOAD, 0x0000, 0xFFFF );     // Tx buf addr
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.TX_BURST_COUNT, 0x0001, 0xFFFF );     // Num pckts = 1
    okUsbFrontPanel_UpdateWireIns( okHdl );

    okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MAC_CTRL, 2 );  // Load start addr
    okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.START_TX, 0 );  // Sends pckt
    
    // Wait for completion
    for( nTimeout=100; nTimeout; nTimeout-- ) {
        okUsbFrontPanel_UpdateTriggerOuts( okHdl );
        if( okUsbFrontPanel_IsTriggered( okHdl, oaiDevHandle->alpEP.TX_DONE, 1 ) )
            break;
    }
    
    OAIEndRegCriticalSection( oaiDevHandle );
    return;
}

//****************************************************************************
EXPORT void 
    MACSendPacket(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *txBuf,
        IN NS_UINT length)
//
//  Parameters
//      eplPortHandle
//          Handle to the port to send the data.
//      txBuf
//          Pointer to the packet of data to send.
//      length
//          Length of the data packet to be sent.
//
//  Returns:
//      Nothing
//
//  Comments:
//      Sends a packet through the FPGA's MAC. This function calculates
//      and sets the IP & UDP checksum fields.
//****************************************************************************
{
    sendPacketNoUdpChecksum( eplPortHandle, txBuf, length, TRUE);
    return;
}


//****************************************************************************
EXPORT void 
    MACSendPacketNoUdpChecksum(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *txBuf,
        IN NS_UINT length)

//
//  Parameters
//      eplPortHandle
//          Handle to the port to send the data.
//      txBuf
//          Pointer to the packet of data to send.
//      length
//          Length of the data packet to be sent.
//
//  Returns:
//      Nothing
//
//  Comments:
//      Sends a packet through the FPGA's MAC. This function calculates
//      and sets the IP checksum field ONLY!
//****************************************************************************
{
    sendPacketNoUdpChecksum( eplPortHandle, txBuf, length, FALSE);
    return;
}

NS_UINT8 dummyBuf[4096];

//****************************************************************************
EXPORT void MACFlushReceiveFifos(
    IN PEPL_PORT_HANDLE eplPortHandle)
//
//  Parameters
//      eplPortHandle
//          Handle to the port to send the data.
//  Returns
//      Nothing
//****************************************************************************
{
NS_UINT length;

    // Just pulsing the pckt rd done bit 4 times doesn't seem to always clear
    // out the rx FIFO - so actually receive the packets until no more are
    // indicated.
    while( MACReceivePacket( eplPortHandle, dummyBuf, &length ) );
    return;
}

//****************************************************************************
EXPORT NS_UINT
    MACReceivePacket(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *rxBuf,
        OUT NS_UINT *length)
//
//  Parameters
//      eplPortHandle
//          Handle to the port to send the data.
//      rxBuf
//          Pointer to a buffer that will be filled in if any data is available
//      length
//          Length of the data packet to be sent.
//
//  Return Value
//      TRUE if data is available
//      FALSE if no data is available
//****************************************************************************
{
    return( intMACReceivePacket( eplPortHandle, rxBuf, length, TRUE ) );
}

//****************************************************************************
NS_UINT
    intMACReceivePacket(
        IN PEPL_PORT_HANDLE eplPortHandle,
        IN NS_UINT8 *rxBuf,
        OUT NS_UINT *length,
        IN NS_BOOL  usePktList )
//****************************************************************************
{
PPORT_OBJ portHdl = (PPORT_OBJ)eplPortHandle;
OAI_DEV_HANDLE oaiDevHandle = portHdl->oaiDevHandle;
okUSBFRONTPANEL_HANDLE okHdl;
NS_UINT rxStartAddr, rxLength;
PKT_LIST *pktList;



    // Clear out the PKT List first
    if( usePktList && portHdl->pktList ) {
        while( portHdl->pktList ) {
            pktList = portHdl->pktList;
            if( pktList->pPacket ) {
                memcpy( rxBuf, pktList->pPacket, pktList->pSize );
                DBG( "MACReceive: Queued Packet =========================> %d \n", pktList->nPkt );
                OAIFree( pktList->pPacket );
                portHdl->pktList = pktList->nxtPkt;
                OAIFree( pktList );
                //return TRUE;
            }
            else {
                DBG( "MACReceive: Missing Packet\n" );
                portHdl->pktList = pktList->nxtPkt;
                OAIFree( pktList );
            }
        }  // while( pktList )
    } // if( portHdl->pktList )

    okHdl = oaiDevHandle->ifHandle;

    OAIBeginRegCriticalSection( oaiDevHandle );

    okUsbFrontPanel_UpdateWireOuts( okHdl );
    if( okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.RX_DATA_ADDR) & 0x4000 )
    {
        rxStartAddr = okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.RX_DATA_ADDR) & 0x03FF;
        rxLength = okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.RX_BYTE_COUNT);
        
        // Sanity check the receive length - sometimes we get really wrong values for a length
        if ( rxLength > 2048) {
            // Reset the RAM FIFO's
            okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MAC_CTRL, 0);
            OAIEndRegCriticalSection( oaiDevHandle);
            return FALSE;
        }
        
        okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.DATA_FIFO_LOAD, rxStartAddr, 0xFFFF);  // Rx buf addr
        okUsbFrontPanel_UpdateWireIns( okHdl);
        okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MAC_CTRL, 3);
        okUsbFrontPanel_ReadFromPipeOut( okHdl, oaiDevHandle->alpEP.RXFIFO_RD_DATA, ((rxLength+1) & 0xFFFE), rxBuf);
        
        // Pulse pkt_read_done to move to next packet
        okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.PKT_RD_DONE, 0);
    }
    else {
        OAIEndRegCriticalSection( oaiDevHandle);
        return FALSE;
    }
    
    *length = rxLength;    
    OAIEndRegCriticalSection( oaiDevHandle);

    return TRUE;
}

//****************************************************************************
NS_UINT
    MACReadReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex)

//  Issues a direct register read operation. Host software must implement 
//  this function as a synchronous operation.
//
//  portHandle
//      Handle that represents the port to use for the transaction
//  regIndex
//      Index of the register to read. Bits 7:5 select the 
//      register page (000-pg0, 001-pg1, 010-pg3, 011-pg4, etc.).
//
//  Returns:
//      The value read from the register.
//****************************************************************************
{
okUSBFRONTPANEL_HANDLE okHdl;
NS_UINT readVal, val;
OAI_DEV_HANDLE  oaiDevHandle = portHandle->oaiDevHandle;
NS_UINT mdioAddr = portHandle->portMdioAddress;
NS_UINT nTimeout;

    okHdl = oaiDevHandle->ifHandle;
    
    if ( regIndex & 0x8000) {   // check for special broadcast bit
        mdioAddr = 0x1F;        // Broadcast address
        regIndex &= ~0x8000;
    }
    
    val = (mdioAddr << 5) | regIndex;
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_ADDR, val, 0xFFFF);
    okUsbFrontPanel_UpdateWireIns( okHdl);
    okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MDIO_TRIGGER_IN, 0);

    for( nTimeout=100; nTimeout; nTimeout-- ) {
        okUsbFrontPanel_UpdateWireOuts( okHdl);
        if ( okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_ADDR_RD) & 0x8000)
            break;
    }
    if( nTimeout ) {
        // We didn't timeout, get value    
        readVal = okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_DATA_RD);
    }
    else {
        // We timed out, return 0
        readVal = 0;
    }

    return readVal;
}

 
//****************************************************************************
void
    MACWriteReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,    // Take out when PCF are supported
        IN NS_UINT value)

//  Issues a write operation Phy control operation through the environment's 
//  MAC interface.
//
//  portHandle
//      Handle that represents the port to use for the transaction
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
okUSBFRONTPANEL_HANDLE okHdl;
NS_UINT val;
OAI_DEV_HANDLE  oaiDevHandle = portHandle->oaiDevHandle;
NS_UINT mdioAddr = portHandle->portMdioAddress;
NS_UINT nTimeout;

    okHdl = oaiDevHandle->ifHandle;
    
    if ( regIndex & 0x8000) {  // check for special broadcast bit
        mdioAddr = 0x1F;       // Broadcast address
        regIndex &= ~0x8000;
    }
     
    val = 0x0400 | (mdioAddr << 5) | regIndex;
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_ADDR, val, 0xFFFF);
    okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_DATA, value, 0xFFFF);
    okUsbFrontPanel_UpdateWireIns( okHdl);
    okUsbFrontPanel_ActivateTriggerIn( okHdl, oaiDevHandle->alpEP.MDIO_TRIGGER_IN, 0);
    
    for( nTimeout=100; nTimeout; nTimeout-- ) {
        okUsbFrontPanel_UpdateWireOuts( okHdl);
        if ( okUsbFrontPanel_GetWireOutValue( okHdl, oaiDevHandle->alpEP.REG_MDIO_ADDR_RD) & 0x8000) {
            break;
        }
    }
     
    return;
}

NS_UINT8 rBuf[4096];
NS_BOOL  pcfReadPending = FALSE;

//****************************************************************************
NS_UINT
    MACMIIReadReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT8 *readRegRequestPacket,
        IN NS_UINT length)

//  Issues a read request Phy control operation through the environment's 
//  MAC interface. Host software must implement this function as a synchronous 
//  operation.
//
//  portHandle
//      Handle that represents the port to use for the transaction
//  readRegRequestPacket
//      Fully formatted packet buffer containing a register read Phy Control 
//      Frame (PCF).
//  length
//      Specifies the length of the readReqRequestPacket buffer in bytes.
//
//  Returns:
//      The value read from the register.
//****************************************************************************
{
NS_UINT  nOffset=0;
NS_UINT8 *nxtMsg;
PHYMSG_MESSAGE_TYPE_ENUM msgType;
PHYMSG_MESSAGE phyMsg;
NS_UINT readData;
NS_UINT8 nTimeout;
NS_UINT8 nAttempts;
PHYMSG_LIST *psfList;
PKT_LIST *pktList;
NS_UINT nPkt;

    // Prepare full request PCF Request
    // Zero out buffer
    memset( rBuf, 0x00, sizeof( rBuf ) );

    // Target MAC address
    if( portHandle->pcfDA_SEL ) {
        memcpy( &rBuf[nOffset], pcfDA1, sizeof(pcfDA1) );
    }
    else {
        memcpy( &rBuf[nOffset], pcfDA0, sizeof(pcfDA0) );
    }
    nOffset += sizeof(pcfDA0);

    // Start of PCF
    memcpy( &rBuf[nOffset], pcfStart, sizeof(pcfStart) );
    nOffset += sizeof(pcfStart);

    // Actual PCF packet
    memcpy( &rBuf[nOffset], readRegRequestPacket, length );
    nOffset += length;

    // Termination Field
    nOffset +=4;    

    // Fill out to at least 60 bytes
    if( nOffset < 60 ) {
        nOffset = 60;
    }

    pcfReadPending = TRUE;

    // Send newly created packet
    sendPacketNoUdpChecksum( portHandle, rBuf, nOffset, FALSE);

    // Now that we sent the request, wait for response
    nAttempts = 10;
    readData = 0;
    while( pcfReadPending && nAttempts-- ) {

        // Zero out buffer, not really needed but helps debug
        memset( rBuf, 0x00, sizeof( rBuf ) );

        // Wait for packet to arrive
        nTimeout = 100; // Only allow 100 attempts to avoid a hang
        while( !intMACReceivePacket( portHandle, rBuf, &nOffset, FALSE ) && nTimeout ) {
            nTimeout--;
        }
        if( !nTimeout ) {
            // We timed out something must be wrong.  Bail out. 
            readData = 0x0000;
            pcfReadPending = FALSE;
            break;
        }

        // We have a packet, see if it is a PHYMSG_STATUS_REG_READ PSF 
        nxtMsg = IsPhyStatusFrame( portHandle, rBuf, nOffset );
        if( !nxtMsg ) {
#if 1
            // Oops, we got a non-PSF packet, store it for later
            // Not the message we are looking for, put it in the queue
            pktList = portHandle->pktList;
            if( pktList ) {
                nPkt = pktList->nPkt+1;
                // Already have a list add to the end of it
                while( pktList->nxtPkt ) {
                    pktList = pktList->nxtPkt;
                    nPkt = pktList->nPkt+1;
                }
                pktList = pktList->nxtPkt = OAIAlloc( sizeof(PKT_LIST) );
            }
            else {
                // No list yet, start it.
                pktList = portHandle->pktList = OAIAlloc( sizeof(PKT_LIST) );
                nPkt = 0;
            }
            if( pktList ) {
                pktList->nxtPkt = NULL;
                pktList->pType = 1;
                pktList->pSize = nOffset;
                pktList->nPkt = nPkt;
                pktList->pPacket = OAIAlloc( nOffset );
                if( pktList->pPacket ) {
                    memcpy( pktList->pPacket, rBuf, nOffset );
                }
            }
#else
            nPkt = 100;
#endif
            DBG( "MMRR ==============================================> %d\n", nPkt );
        }
        while( nxtMsg && pcfReadPending ) {
            nxtMsg = intGetNextPhyMessage( portHandle, nxtMsg, &msgType, &phyMsg, 0 );
            if( !nxtMsg ) {
                continue;
            }
            switch( msgType ){
            case PHYMSG_STATUS_REG_READ:
                DBG( "MACMIIReadReg:(%d) PSF %04X (READ) index: %02X  page: %02X  value: %04X\n", nAttempts,
                        msgType, phyMsg.RegReadStatus.regIndex, phyMsg.RegReadStatus.regPage, 
                        phyMsg.RegReadStatus.readRegisterValue );
                readData = phyMsg.RegReadStatus.readRegisterValue;
                pcfReadPending = FALSE;
                break;
            default:
                switch( msgType ) {
                case PHYMSG_STATUS_TX:
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_TX:   %ds %dns  %d\n", nAttempts,
                                phyMsg.TxStatus.txTimestampSecs, 
                                phyMsg.TxStatus.txTimestampNanoSecs,
                                phyMsg.TxStatus.txOverflowCount );
                    break;
                case PHYMSG_STATUS_RX:
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_RX:   %ds %dns  %d   #%d   %d  %d\n", nAttempts,
                                phyMsg.RxStatus.rxTimestampSecs, 
                                phyMsg.RxStatus.rxTimestampNanoSecs,
                                phyMsg.RxStatus.rxOverflowCount,
                                phyMsg.RxStatus.sequenceId,
                                phyMsg.RxStatus.messageType, 
                                phyMsg.RxStatus.sourceHash );
                    break;
                case PHYMSG_STATUS_TRIGGER:
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_TRIGGER:   %d\n", nAttempts, phyMsg.TriggerStatus.triggerStatus );
                    break;
                case PHYMSG_STATUS_EVENT:
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_EVENT: \n", nAttempts );
                    break;
                case PHYMSG_STATUS_ERROR:
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_ERROR: \n", nAttempts );
                    break;
                case PHYMSG_STATUS_REG_READ:
                    // Should never get this, but just in case!
                    DBG( "MACMIIReadReg:(%d) PHYMSG_STATUS_REG_READ: \n", nAttempts );
                    break;
                default:
                    DBG( "MACMIIReadReg:(%d) PSF %04X\n", nAttempts, msgType );                    
                    break;
                }
                // Not the message we are looking for, put it in the queue
                psfList = portHandle->psfList;
                if( psfList ) {
                    // Already have a list add to the end of it
                    while( psfList->nxtMsg )
                        psfList = psfList->nxtMsg;
                    psfList = psfList->nxtMsg = OAIAlloc( sizeof(PHYMSG_LIST) );
                }
                else {
                    // No list yet, start it.
                    psfList = portHandle->psfList = OAIAlloc( sizeof(PHYMSG_LIST) );
                }
                psfList->nxtMsg = NULL;
                psfList->msgType = msgType;
                memcpy( &psfList->phyMsg, &phyMsg, sizeof(PHYMSG_MESSAGE) );
                break;
            }  // switch( msgType )
        }  // while( nxtMsg )
    } // while( pcfReadPending )
    pcfReadPending = FALSE;

    return readData;
}

NS_UINT8 tBuf[4096];

//****************************************************************************
void
    MACMIIWriteReg (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT8 *writeRegRequestPacket,
        IN NS_UINT length)

//  Issues a write operation Phy control operation through the environment's 
//  MAC interface.
//
//  portHandle
//      Handle that represents the port to use for the transaction
//  writeRegRequestPacket
//      Fully formatted packet buffer containing a register write Phy Control 
//      Frame (PCF). This frame may contain more then one register write 
//      request.
//  length
//      Specifies the length of the writeReqRequestPacket buffer in bytes.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT  nOffset=0;

    // Zero out buffer
    memset( tBuf, 0x00, sizeof( tBuf ) );

    // Target MAC address
    if( portHandle->pcfDA_SEL ) {
        memcpy( &tBuf[nOffset], pcfDA1, sizeof(pcfDA1) );
    }
    else {
        memcpy( &tBuf[nOffset], pcfDA0, sizeof(pcfDA0) );
    }
    nOffset += sizeof(pcfDA0);

    // Start of PCF
    memcpy( &tBuf[nOffset], pcfStart, sizeof(pcfStart) );
    nOffset += sizeof(pcfStart);

    // Actual PCF packet
    memcpy( &tBuf[nOffset], writeRegRequestPacket, length );
    nOffset += length;

    // Termination Field
    nOffset +=4;    

    // Fill out to at least 60 bytes
    if( nOffset < 60 ) {
        nOffset = 60;
    }

    sendPacketNoUdpChecksum( portHandle, tBuf, nOffset, FALSE);

	return;
}

//****************************************************************************
EXPORT void SetDuplex( 
    IN PEPL_PORT_HANDLE portHandle,
    NS_BOOL halfDuplex)
//
//  Parameters
//      portHandle
//          Handle to the port to send the data.
//      halfDuplex
//          Flag saying we want half duplex
//  Returns
//      Nothing
//****************************************************************************
{
PPORT_OBJ portHdl = (PPORT_OBJ)portHandle;
OAI_DEV_HANDLE oaiDevHandle;
okUSBFRONTPANEL_HANDLE okHdl;

    oaiDevHandle = portHdl->oaiDevHandle;
    okHdl = oaiDevHandle->ifHandle;

    // Configures the FPGA MAC duplex operation
    if ( halfDuplex) {
        okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_CNTRL_WR, 0x0008, 0x0008);
    }
    else {
        okUsbFrontPanel_SetWireInValue( okHdl, oaiDevHandle->alpEP.REG_CNTRL_WR, 0x0000, 0x0008);
    }
    
    okUsbFrontPanel_UpdateWireIns( okHdl );
}

//****************************************************************************
EXPORT void PythonReload( void)
// This procedure should not be needed in a real system.
// Called by our python library to tell us that boards have been reenumerated.
// We need this hook to reset the connector mux assignment tracking variables.
//****************************************************************************
{
NS_UINT nBrd;

    // Zero out all board handles, no need to free them because Python is 
    // controlling them we just need to erase references that may not be
    // valid anymore.
    if( okLocalData ) {
        for( nBrd=0; nBrd < ALP_MAX_BOARD; nBrd++ ) {
            okLocalData->okHandle[nBrd] = NULL;
        }
        okLocalData->connRegValue = 0;
    }
}

//****************************************************************************
EXPORT NS_UINT16
    CalcChecksum( 
        NS_UINT8 *buf, 
        NS_UINT len, 
        NS_UINT chksum)
// Internal procedure used to calculate the checksum of a buffer.
//****************************************************************************
{
NS_UINT x;

    for ( x = 0; x < (len / 2); x += 1)
        chksum += (buf[x*2] << 8) + buf[x*2+1];
    
    if ( len & 0x01)
        chksum += (buf[len-1] << 8);
        
    chksum = (chksum & 0xFFFF) + (chksum >> 16);
    chksum = (chksum & 0xFFFF) + (chksum >> 16);
    return (~chksum) & 0xFFFF;
}

//****************************************************************************
void 
    FPGAWriteReg( 
        okUSBFRONTPANEL_HANDLE okHdl,
        NS_UINT regIndex, 
        NS_UINT regValue)
//  Internal procedure used to configure the FPGA interface
//****************************************************************************
{
NS_UINT8 cmdPacket[8];
NS_UINT8 cmdResponse[32];
NS_UINT8 length[2];
NS_UINT  nTimeout;

    cmdPacket[0] = 0x04;                // 16-bit length of cmd packet (0x0004)
    cmdPacket[1] = 0x00;
    cmdPacket[2] = 0x00;                // Register write cmd code (0x7000)
    cmdPacket[3] = 0x70;
    cmdPacket[4] = regIndex & 0x00FF;
    cmdPacket[5] = regIndex >> 8;
    cmdPacket[6] = regValue & 0x00FF;
    cmdPacket[7] = regValue >> 8;

    // Send down a FPGA reg write cmd to our HDL and wait for an ack
    okUsbFrontPanel_ActivateTriggerIn( okHdl, 0x40, 3);
    
    okUsbFrontPanel_WriteToPipeIn( okHdl, 0x80, 8, cmdPacket);
    
    okUsbFrontPanel_UpdateTriggerOuts( okHdl);
    nTimeout = 100;
    while( !okUsbFrontPanel_IsTriggered( okHdl, 0x60, 0x04) && nTimeout-- ) {
        okUsbFrontPanel_UpdateTriggerOuts( okHdl);
    }
    if( nTimeout ) {
        // We didn't timeout, get response
        okUsbFrontPanel_ReadFromPipeOut( okHdl, 0xA0, 2L, length);
        okUsbFrontPanel_ReadFromPipeOut( okHdl, 0xA0, (long)(length[0]*2), cmdResponse);
    }

    return;    
}

