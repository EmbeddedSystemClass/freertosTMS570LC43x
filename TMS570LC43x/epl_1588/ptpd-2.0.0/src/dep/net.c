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

#define socket FreeRTOS_socket
#define SOCK_DGRAM FREERTOS_SOCK_DGRAM
#define IPPROTO_UDP FREERTOS_IPPROTO_UDP
#define AF_INET 		FREERTOS_AF_INET
#define PF_INET 		FREERTOS_AF_INET
#define htons(x)		FreeRTOS_htons(x)
#define htonl(x)			FreeRTOS_htonl(x)
#define bind(x,y,z) 	FreeRTOS_bind(x,y,z)
uint32_t MACReceivePacket(NetPath * netPath, octet_t * rxbuff, uint32_t *rxbuff_len);
extern RunTimeOpts rtOpts;

/* Demo app includes. */
#include "udp_echo.h"
#include "NetworkInterface.h"
extern uint8 emacAddress[6U];

void send_to_analysis(PtpClock *ptpClock){

	AeroNetwork__Ptp1588TimingPacket timing_packet;
	aero_network__ptp1588_timing_packet__init(&timing_packet);
	timing_packet.mac_address = *(int64_t*)emacAddress;
	timing_packet.has_mac_address = true;

	timing_packet.offset_from_master_s = ptpClock->currentDS.offsetFromMaster.seconds;
	timing_packet.has_offset_from_master_s = true;

	timing_packet.offset_from_master_ns = ptpClock->currentDS.offsetFromMaster.nanoseconds;
	timing_packet.has_offset_from_master_ns = true;

	timing_packet.mean_path_delay_s = ptpClock->currentDS.meanPathDelay.seconds;
	timing_packet.has_mean_path_delay_s = true;

	timing_packet.mean_path_delay_ns = ptpClock->currentDS.meanPathDelay.nanoseconds;
	timing_packet.has_mean_path_delay_ns = true;

	timing_packet.slave_to_master_delay_s = ptpClock->Tsm.seconds;
	timing_packet.has_slave_to_master_delay_s = true;

	timing_packet.slave_to_master_delay_ns = ptpClock->Tsm.nanoseconds;
	timing_packet.has_slave_to_master_delay_ns = true;

	timing_packet.master_to_slave_delay_s = ptpClock->Tms.seconds;
	timing_packet.has_master_to_slave_delay_s = true;

	timing_packet.master_to_slave_delay_ns = ptpClock->Tms.nanoseconds;
	timing_packet.has_master_to_slave_delay_ns = true;

	timing_packet.sync_receive_s = ptpClock->timestamp_syncRecieve.seconds;
	timing_packet.has_sync_receive_s = true;

	timing_packet.sync_receive_ns = ptpClock->timestamp_syncRecieve.nanoseconds;
	timing_packet.has_sync_receive_ns = true;

	timing_packet.delay_request_send_s = ptpClock->timestamp_delayReqSend.seconds;
	timing_packet.has_delay_request_send_s = true;

	timing_packet.delay_request_send_ns = ptpClock->timestamp_delayReqSend.nanoseconds;
	timing_packet.has_delay_request_send_ns = true;

	timing_packet.delay_request_receive_s = ptpClock->timestamp_delayReqRecieve.seconds;
	timing_packet.has_delay_request_receive_s = true;

	timing_packet.delay_request_receive_ns = ptpClock->timestamp_delayReqRecieve.nanoseconds;
	timing_packet.has_delay_request_receive_ns = true;

	timing_packet.port_state = ptpClock->portDS.portState;
	timing_packet.has_port_state = true;

	size_t pack_size = aero_network__ptp1588_timing_packet__get_packed_size(&timing_packet);
	uint8_t * packet_buffer = malloc(pack_size);
	memset(packet_buffer, 0, pack_size);
	aero_network__ptp1588_timing_packet__pack(&timing_packet, packet_buffer);
	netSendAnalysis(&ptpClock->netPath, (const octet_t*) packet_buffer , pack_size);
	free(packet_buffer);
}


#define freertos		1

NS_UINT8 *
    intGetNextPhyMessage (
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_UINT8 *msgLocation,
        IN OUT PHYMSG_MESSAGE_TYPE_ENUM *messageType,
        IN OUT PHYMSG_MESSAGE *phyMessageOut,
        IN NS_BOOL usePSFList);


uint32_t findIface(octet_t *ifaceName, uint8_t *communicationTechnology,
  octet_t *uuid, boolean multicast, NetPath *netPath)
{
  return FALSE;
}

/* start all of the UDP stuff */
/* must specify 'subdomainName', optionally 'ifaceName', if not then pass ifaceName == "" */
/* returns other args */
/* on socket options, see the 'socket(7)' and 'ip' man pages */
boolean netInit(NetPath *netPath, PtpClock *ptpClock)
{
  netPath->eventSock = prvOpenUDPServerSocket(PTP_EVENT_PORT);
  netPath->generalSock = prvOpenUDPServerSocket(PTP_GENERAL_PORT);
  netPath->anaysisSocket = prvOpenUDPServerSocket(PTP_ANALYSIS_PORT);
    return TRUE;
}

/* shut down the UDP stuff */
boolean netShutdown(NetPath *netPath)
{
  return TRUE;
}

int32_t netSelect(NetPath *netPath, const TimeInternal *timeout)
{
  //TODO: implement select
  return TRUE;
}

size_t netRecvEvent( NetPath *netPath, octet_t *buf, TimeInternal *time)
{
	uint32_t length;

    if ( !MACReceivePacket(netPath, buf, &length))
        return 0;
    DBG( "NR2\n" );

    if ( length < 44)
        return 0;

    if ( buf[1] != 0x02)        // PTP Version
        return 0;

//	time->nanoseconds =  *(NS_UINT32*)&buf[PTPV2_ORIGIN_TS_NSEC_OFFSET];
//	time->seconds =  *(NS_UINT32*)&buf[PTPV2_ORIGIN_TS_SEC_OFFSET];
//	PTPGetTimestampFromFrame(buf, &(time->seconds), &(time->nanoseconds));
    switch(buf[0]){
    case PTPV2_SYNC_TYPE:
    case PTPV2_FOLLOWUP_TYPE:
    case PTPV2_DELAY_REQUEST_TYPE:
	//The tx timestamp willl be coming in in the correction fields of this packet
    case PTPV2_DELAY_RESPONSE_TYPE:
		PTPGetTimestampFromFrame((uint8_t*)buf, (uint32_t*)&(time->seconds),(uint32_t*) &(time->nanoseconds));
		break;
    default:
		PTPClockReadCurrent(rtOpts.epl_port_handle, &(time->seconds), &(time->nanoseconds));
    }

    if(!(time->seconds)){
		PTPClockReadCurrent(rtOpts.epl_port_handle, &(time->seconds), &(time->nanoseconds));
    }
	return length;
}

uint32_t MACReceivePacket(NetPath * net_path, octet_t * rxbuff, uint32_t *rx_len){
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

uint32_t MACSendPacket(NetPath * net_path, octet_t * txbuff, uint32_t txbuff_len){
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

uint32_t MACSendAnalysisPacket(NetPath * net_path, octet_t * txbuff, uint32_t txbuff_len){
	struct freertos_sockaddr destination;
	Socket_t send_socket;
	socklen_t destination_address_length = 0;
	uint32_t bits_written = 0;
	send_socket = net_path->anaysisSocket;
	destination.sin_port = FreeRTOS_htons(5500);
	destination.sin_addr = FreeRTOS_inet_addr_quick(10, 10, 10, 12);

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

size_t netRecvGeneral(NetPath *netPath, octet_t *buf, TimeInternal * time)
{
  return FALSE;
}

void SendAPacket( octet_t *buf, uint16_t length, NetPath *netPath, uint16_t srcPort, uint16_t destPort)
{
    // Send the packet
    MACSendPacket( netPath, buf, length);
}

size_t netSendEvent( NetPath *netPath, const  octet_t *buf, int16_t length, TimeInternal * time)
{
    return MACSendPacket( netPath, buf, length);
}

size_t netSendGeneral(NetPath *netPath, const octet_t *buf, int16_t length )
{
    return MACSendPacket( netPath, buf, length);
}

size_t netSendAnalysis(NetPath *netPath, const octet_t *buf, int16_t length )
{
    return MACSendAnalysisPacket( netPath, buf, length);
}

size_t netSendPeerGeneral(NetPath *netPath, const octet_t *buf, int16_t  length)
{
//	return netSend(buf, length, NULL, &netPath->peerMulticastAddr, netPath->generalPcb);
	//TODO: implement
    return MACSendPacket( netPath, buf, length);
}

size_t netSendPeerEvent(NetPath *netPath, const octet_t *buf, int16_t  length, TimeInternal* time)
{
//	return netSend(buf, length, time, &netPath->peerMulticastAddr, netPath->eventPcb);
	//TODO: implement
    return MACSendPacket( netPath, buf, length);
}
