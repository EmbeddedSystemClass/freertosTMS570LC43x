/* net.c */
/*****************************************************************************
COPYRIGHT NOTICE

PTP Notice for PTPd Software

The following copyright notice applies to all files which compose the original
PTPd Software. This notice applies as if the text was explicitly included each
file.

Copyright (c) 2006 Aidan Williams
Copyright (c) 2005-2007 Kendall Correll

Permission is hereby granted to use, copy, modify, and distribute this software
for any purpose and without fee, provided that this notice appears in all
copies. The authors make no representations about the suitability of this
software for any purpose. This software is provided "as is" without express or
implied warranty.

National Semiconductor Notice for Modified Software

The following copyright notice applies Modifications of the PTPd Software 
developed by National Semiconductor Corporation, and distributed by 
National Semiconductor as a Modified Version of the PTPd Software.  

Copyright (c) 2008 National Semiconductor

The associated Modified Software is distributed by National Semiconductor under 
the above PTPd Notice and Permission, and under the following License, 
Restrictions, Disclaimers and Limitations:

LICENSE:  Permission is granted to copy, use, modify and/or distribute the 
Software in Source and/or Binary form, including as an FPGA or other hardware 
implementation of the Software, subject to the Restrictions, Disclaimers and 
Limitations.  NSC and/or its licensors retain ownership of all copyright, 
patent and other intellectual property rights in the Software, and COMPANY 
shall not remove or alter any copyright or other notices associated with the 
Software

RESTRICTIONS: The Software may be distributed only in connection the 
distribution of COMPANY�s Products, and only subject to the following 
additional Restrictions:  (a) NSC Components:  The Software may be used 
only in connection with Components that are incorporated into COMPANY's 
Products; (b) Sublicensing Source:  The Software may be sublicensed in 
Source form, without any right to grant further downstream sublicenses, 
solely in accordance with this Agreement including these Restrictions;  
(c) Confidentiality.  The Source form of the Software is confidential, 
and unauthorized use or disclosure is prohibited; and (d) Export Compliance.  
The Software is subject to United States export control laws and regulations, 
and any product, software or technical data acquired from NSC, or any direct 
product thereof, shall not be, directly or indirectly, exported, re-exported, 
or released to any destination without first obtaining any export license or 
other approval required by the U.S. government, or other applicable non-U.S. 
governments.  This provision shall survive any termination of this Agreement.

DISCLAIMERS:   The Software is provided "AS IS" without warranty of any kind, 
including any warranty as to the design or manufacture of COMPANY Products 
incorporating Components.  NSC and its licensors expressly disclaim all 
warranties, expressed, implied or otherwise, including without limitation, 
warranties of merchantability, fitness for a particular purpose and 
non-infringement of intellectual property rights.  
Any COMPANY Product incorporating any Software (or any FPGA or other hardware 
implementation) and associated Components should not be released to production 
without full test, verification, and qualification, including verification of 
the selection, configuration and performance of any Software (or any FPGA or 
other hardware implementation) and/or Components, and including verification 
that the product design meets functional, performance, reliability and any 
applicable export or other regulatory requirements.

LIMITATIONS ON LIABILITY.  NSC or its licensors shall not be liable for any 
direct or indirect or punitive damages of any kind, including but not limited 
to any special, consequential or incidental damages, including any costs of 
labor, delay, requalification, or replacement, and any lost business 
opportunity, profits, or goodwill, whether arising out of the use or 
inability to use the Software (or the use or inability to use any COMPANY 
Product incorporating the Software), even if NSC is advised of the 
possibility of such damages.  In no event shall NSC's aggregate liability from 
any obligation arising out of or in connection with the license or use of the 
Software, under any theory of liability including but not limited to contract, 
tort or promissory fraud, exceed the consideration received by NSC, if any, 
for the license to the Software.  The foregoing limitation shall not apply to 
damages resulting directly from NSC's willful and wanton conduct.  To the 
maximum extent permitted under law, the limitations in this paragraph shall 
apply even if this limited remedy is found to have failed of its essential 
purpose.

******************************************************************************/


//#include "epl.h"
#include "ptpd.h"
/* FreeRTOS includes. */
#include "FreeRTOS.h"
#include "os_task.h"
#include "os_semphr.h"

/* FreeRTOS+CLI includes. */
#include "FreeRTOS_CLI.h"

/* FreeRTOS+TCP includes. */
#include "FreeRTOS_IP.h"
#include "FreeRTOS_Sockets.h"
#include "udp_echo.h"

UInteger32 crc_algorithm(Octet *buf, Integer16 length)
{
  Integer16 i;
  UInteger8 data;
  UInteger32 polynomial = 0xedb88320, crc = 0xffffffff;

  while(length-- > 0)
  {
    data = *(UInteger8 *)(buf++);

    for(i=0; i<8; i++)
    {
      if((crc^data)&1)
      {
        crc = (crc>>1);
        crc ^= polynomial;
      }
      else
      {
        crc = (crc>>1);
      }
      data >>= 1;
    }
  }

  return crc^0xffffffff;
}


#define socket FreeRTOS_socket
#define SOCK_DGRAM FREERTOS_SOCK_DGRAM
#define IPPROTO_UDP FREERTOS_IPPROTO_UDP
#define AF_INET 		FREERTOS_AF_INET
#define PF_INET 		FREERTOS_AF_INET
#define htons(x)		FreeRTOS_htons(x)
#define htonl(x)			FreeRTOS_htonl(x)
#define bind(x,y,z) 	FreeRTOS_bind(x,y,z)
uint32_t MACReceivePacket(NetPath * netPath, Octet * rxbuff, uint32_t *rxbuff_len);

/* Demo app includes. */
#include "udp_echo.h"
#include "NetworkInterface.h"

#define freertos		1

NS_UINT8 *
    intGetNextPhyMessage (
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_UINT8 *msgLocation,
        IN OUT PHYMSG_MESSAGE_TYPE_ENUM *messageType,
        IN OUT PHYMSG_MESSAGE *phyMessageOut,
        IN NS_BOOL usePSFList);


Boolean lookupSubdomainAddress(Octet *subdomainName, Octet *subdomainAddress)
{
  UInteger32 h;
  
  /* set multicast group address based on subdomainName */
  if (!memcmp(subdomainName, DEFAULT_PTP_DOMAIN_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, DEFAULT_PTP_DOMAIN_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN1_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN1_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN2_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN2_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN3_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN3_ADDRESS, NET_ADDRESS_LENGTH);
  else
  {
    h = crc_algorithm(subdomainName, PTP_SUBDOMAIN_NAME_LENGTH) % 3;
    switch(h)
    {
    case 0:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN1_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    case 1:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN2_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    case 2:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN3_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    default:
      ERROR("handle out of range for '%s'!\n", subdomainName);
      return FALSE;
    }
  }
  
  return TRUE;
}

UInteger8 lookupCommunicationTechnology(UInteger8 communicationTechnology)
{
  return PTP_ETHER;
}

UInteger32 findIface(Octet *ifaceName, UInteger8 *communicationTechnology,
  Octet *uuid, Boolean multicast, NetPath *netPath)
{
  return FALSE;
}

/* start all of the UDP stuff */
/* must specify 'subdomainName', optionally 'ifaceName', if not then pass ifaceName == "" */
/* returns other args */
/* on socket options, see the 'socket(7)' and 'ip' man pages */
Boolean netInit(NetPath *netPath, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  int i;
  char *s;
  
  char addrStr[NET_ADDRESS_LENGTH];
  
  DBG("netInit\n");
  
  /* set general and port address */
  *(Integer16*)ptpClock->event_port_address = PTP_EVENT_PORT;
  *(Integer16*)ptpClock->general_port_address = PTP_GENERAL_PORT;

  netPath->rtOpts = rtOpts;
  netPath->ptpClock = ptpClock;

    *(Integer16*)ptpClock->event_port_address = PTP_EVENT_PORT;
    *(Integer16*)ptpClock->general_port_address = PTP_GENERAL_PORT;

    ptpClock->port_communication_technology = PTP_ETHER;

//    memcpy( ptpClock->port_uuid_field, rtOpts->localMACAddress, PTP_UUID_LENGTH);
  uint8_t clock_id[8] = {0x00, 0x1E, 0x06, 0x0FF, 0xFE, 0x32, 0x4D, 0x8E};
  memcpy(&(ptpClock->port_uuid_field),  clock_id, 8);

    /* resolve PTP subdomain */
    if(!lookupSubdomainAddress(rtOpts->subdomainName, addrStr))
        return FALSE;

    s = addrStr;
    for(i = 0; i < SUBDOMAIN_ADDRESS_LENGTH; ++i)
    {
        ptpClock->subdomain_address[i] = (Octet)strtol(s, &s, 0);
        netPath->bcastAddr.sin_addr = (netPath->bcastAddr.sin_addr << 8) | (ptpClock->subdomain_address[i] & 0xFF);
        if( !s) break;
        ++s;
    }

    netPath->eventSock = prvOpenUDPServerSocket(PTP_EVENT_PORT);
    netPath->generalSock = prvOpenUDPServerSocket(PTP_GENERAL_PORT);
    netPath->rtOpts = rtOpts;
    netPath->ptpClock = ptpClock;
    rtOpts->haveLoopbackedSend = FALSE;
    return TRUE;
}

/* shut down the UDP stuff */
Boolean netShutdown(NetPath *netPath)
{
  return TRUE;
}

Boolean netSelect(TimeInternal *timeout, NetPath *netPath)
{
  //TODO: implement select
  return TRUE;
}

int netRecvEvent(Octet *address, Octet *buf, TimeInternal *time, NetPath *netPath)
{
	RunTimeOpts *rtOpts = (RunTimeOpts*)netPath->rtOpts;
	PtpClock *ptpClock = (PtpClock*)netPath->ptpClock;
	NS_UINT length;
	NS_UINT overflowCount, sequenceId, hashValue;
	NS_UINT8 messageType;

    if ( !MACReceivePacket(netPath, buf, &length))
        return 0;
    DBG( "NR2\n" );

    if ( length < 44)
        return 0;

    if ( buf[1] != 0x02)        // PTP Version
        return 0;

        if ( !rtOpts->revA1SiliconFlag)
        {
            time->nanoseconds =  *(NS_UINT32*)&buf[PTPV2_ORIGIN_TS_NSEC_OFFSET];
            time->seconds =  *(NS_UINT32*)&buf[PTPV2_ORIGIN_TS_SEC_OFFSET];
//        	PTPGetTimestampFromFrame(ptpHead, &(time->seconds), &(time->nanoseconds));

            if ( ptpClock->waitingForAdjFlag && !(time->nanoseconds & 0x80000000))
            {
                // We could lose the rate adj complete bit if the sync packet was
                // dropped, so use a counter to recover.
                if ( ptpClock->ignoreSyncCount != 0)
                {
                    ptpClock->ignoreSyncCount--;
                    DBG( "Ignoring Sync msg, previous time adj hasn't finished.\n");
                    return 0;
                }
            }

            ptpClock->ignoreSyncCount = 8;
            time->nanoseconds &= ~0x80000000;
            ptpClock->waitingForAdjFlag = FALSE;
        }
        else
        {
            time->seconds = 0;
            time->nanoseconds = 0;

            if ( PTPCheckForEvents( rtOpts->eplPortHandle) & PTPEVT_RECEIVE_TIMESTAMP_BIT)
            {
                PTPGetReceiveTimestamp( rtOpts->eplPortHandle, &time->seconds, &time->nanoseconds,
                                        &overflowCount, &sequenceId, &messageType, &hashValue);
            }
            else
            {
                ERROR( "TIMEOUT - NO TIMESTAMP AVAILABLE FOR RECEIVED EVENT PACKET!\n");
                return 0;
            }
        }
	return length;
}

uint32_t MACReceivePacket(NetPath * net_path, Octet * rxbuff, uint32_t *rx_len){
	socklen_t xClientAddressLength = 0;
	int received_data_length =0;
	if( net_path->eventSock != FREERTOS_INVALID_SOCKET )
	{
		struct freertos_sockaddr client;
		received_data_length = FreeRTOS_recvfrom( net_path->eventSock, ( void * ) rxbuff,  2048, 0, &client, &xClientAddressLength );
		if(!(received_data_length >= 0)){
			received_data_length = 0;
		}
	}
	if(!received_data_length){
		if( net_path->generalSock!= FREERTOS_INVALID_SOCKET )
		{
			struct freertos_sockaddr client;
			received_data_length = FreeRTOS_recvfrom( net_path->generalSock, ( void * ) rxbuff,  2048, 0, &client, &xClientAddressLength );
			if(!(received_data_length >= 0)){
				received_data_length = 0;
			}
		}
	}
	*rx_len = received_data_length;
    return received_data_length;
}

uint32_t MACSendPacket(NetPath * net_path, Octet * txbuff, uint32_t txbuff_len){
	struct freertos_sockaddr destination;
	Socket_t send_socket;
	socklen_t destination_address_length = 0;
	uint32_t bits_written = 0;
	uint8_t message_type = txbuff[0];
	if(message_type == PTPV2_DELAY_RESPONSE_TYPE || message_type == PTPV2_FOLLOWUP_TYPE){
		destination.sin_port = FreeRTOS_htons(320);
		send_socket = net_path->generalSock;
	}else if(message_type == PTPV2_SYNC_TYPE || message_type == PTPV2_DELAY_REQUEST_TYPE ){
		send_socket = net_path->eventSock;
		destination.sin_port = FreeRTOS_htons(319);
	}
	destination.sin_addr = FreeRTOS_inet_addr_quick(224, 0, 1, 129);

	if( net_path->eventSock != FREERTOS_INVALID_SOCKET )
	{
		bits_written = FreeRTOS_sendto( send_socket, txbuff,  txbuff_len, 0, &destination, destination_address_length);
	}
	else
	{
		/* The socket could not be opened. */
		//TODO: something about this
//		vTaskDelete( NULL );
	}
	return bits_written;
}

Boolean netRecvGeneral(Octet *address, Octet *buf, NetPath *netPath)
{
  return FALSE;
}

void SendAPacket( Octet *buf, UInteger16 length, NetPath *netPath, UInteger16 srcPort, UInteger16 destPort)
{
	RunTimeOpts *rtOpts = (RunTimeOpts*)netPath->rtOpts;
	Octet *txBuf = rtOpts->txBuff;
	Octet *txBufPtr = txBuf;

    // Copy over the PTP packet data
    memcpy( txBufPtr, buf, length);

    // Send the packet
    MACSendPacket( netPath, txBuf, length);

    // Need to loop the packet back into the receive engine
    rtOpts->lastSendLength = length;
    rtOpts->haveLoopbackedSend = TRUE;
    return;
}

Boolean netSendEvent(Octet *address, Octet *buf, UInteger16 length, NetPath *netPath)
{
    DBG( "***Sending event message\n");
    UInteger16 null_src = 0;
//    SendAPacket( buf, length, netPath, netPath->eventSock, PTP_EVENT_PORT);
    SendAPacket( buf, length, netPath, null_src, PTP_EVENT_PORT);
    return TRUE;
}

Boolean netSendGeneral(Octet *address, Octet *buf, UInteger16 length, NetPath *netPath)
{
    DBG( "***Sending general message\n");
    UInteger16 null_src = 0;
//    SendAPacket( buf, length, netPath, netPath->generalSock, PTP_GENERAL_PORT);
    SendAPacket( buf, length, netPath, null_src, PTP_GENERAL_PORT);
    return TRUE;
}

