/*
    FreeRTOS V8.2.2 - Copyright (C) 2015 Real Time Engineers Ltd.
    All rights reserved

    VISIT http://www.FreeRTOS.org TO ENSURE YOU ARE USING THE LATEST VERSION.

    This file is part of the FreeRTOS distribution.

    FreeRTOS is free software; you can redistribute it and/or modify it under
    the terms of the GNU General Public License (version 2) as published by the
    Free Software Foundation >>!AND MODIFIED BY!<< the FreeRTOS exception.

    ***************************************************************************
    >>!   NOTE: The modification to the GPL is included to allow you to     !<<
    >>!   distribute a combined work that includes FreeRTOS without being   !<<
    >>!   obliged to provide the source code for proprietary components     !<<
    >>!   outside of the FreeRTOS kernel.                                   !<<
    ***************************************************************************

    FreeRTOS is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  Full license text is available on the following
    link: http://www.freertos.org/a00114.html

    ***************************************************************************
     *                                                                       *
     *    FreeRTOS provides completely free yet professionally developed,    *
     *    robust, strictly quality controlled, supported, and cross          *
     *    platform software that is more than just the market leader, it     *
     *    is the industry's de facto standard.                               *
     *                                                                       *
     *    Help yourself get started quickly while simultaneously helping     *
     *    to support the FreeRTOS project by purchasing a FreeRTOS           *
     *    tutorial book, reference manual, or both:                          *
     *    http://www.FreeRTOS.org/Documentation                              *
     *                                                                       *
    ***************************************************************************

    http://www.FreeRTOS.org/FAQHelp.html - Having a problem?  Start by reading
    the FAQ page "My application does not run, what could be wrong?".  Have you
    defined configASSERT()?

    http://www.FreeRTOS.org/support - In return for receiving this top quality
    embedded software for free we request you assist our global community by
    participating in the support forum.

    http://www.FreeRTOS.org/training - Investing in training allows your team to
    be as productive as possible as early as possible.  Now you can receive
    FreeRTOS training directly from Richard Barry, CEO of Real Time Engineers
    Ltd, and the world's leading authority on the world's leading RTOS.

    http://www.FreeRTOS.org/plus - A selection of FreeRTOS ecosystem products,
    including FreeRTOS+Trace - an indispensable productivity tool, a DOS
    compatible FAT file system, and our tiny thread aware UDP/IP stack.

    http://www.FreeRTOS.org/labs - Where new FreeRTOS products go to incubate.
    Come and try FreeRTOS+TCP, our new open source TCP/IP stack for FreeRTOS.

    http://www.OpenRTOS.com - Real Time Engineers ltd. license FreeRTOS to High
    Integrity Systems ltd. to sell under the OpenRTOS brand.  Low cost OpenRTOS
    licenses offer ticketed support, indemnification and commercial middleware.

    http://www.SafeRTOS.com - High Integrity Systems also provide a safety
    engineered and independently SIL3 certified version for use in safety and
    mission critical applications that require provable dependability.

    1 tab == 4 spaces!
*/

/* Standard includes. */
#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>

/* FreeRTOS includes. */
#include "FreeRTOS.h"
#include "os_task.h"
#include "os_semphr.h"

/* FreeRTOS+CLI includes. */
#include "FreeRTOS_CLI.h"

/* FreeRTOS+TCP includes. */
#include "FreeRTOS_IP.h"
#include "FreeRTOS_Sockets.h"

/* Demo app includes. */
#include "udp_echo.h"
#include "NetworkInterface.h"
#include "ptpd.h"

extern RX_CFG_ITEMS rxCfgItems;
extern uint32_t rxCfgOpts;
extern hdkif_t hdkif_data[];

/* Dimensions the buffer into which input characters are placed. */
#define cmdMAX_INPUT_SIZE	1024

/* Dimensions the buffer into which string outputs can be placed. */
#define cmdMAX_OUTPUT_SIZE	1024

/* Dimensions the buffer passed to the recvfrom() call. */
#define cmdSOCKET_INPUT_BUFFER_SIZE 1024

/* The socket used by the CLI and debug print messages. */
static Socket_t xSocket = FREERTOS_INVALID_SOCKET;

/*
 * The task that runs FreeRTOS+CLI.
 */
static void prvUDPEchoTask( void *pvParameters );
void prv1588PTPTask( void *pvParameters );

/*
 * Open and configure the UDP socket.
 */

/* Stores the UDP port on which the CLI will be presented. */
static uint32_t ulCLIPort = 0;

/* This is required as a parameter to maintain the sendto() Berkeley sockets
API - but it is not actually used so can take any value. */
static socklen_t xClientAddressLength = 0;

/*-----------------------------------------------------------*/

void vStartUDPEchoTask( uint16_t usStackSize, uint32_t ulPort, UBaseType_t uxPriority )
{
	xTaskCreate( prvUDPEchoTask, "UdpEcho", usStackSize, ( void * ) ulPort, uxPriority, NULL );
	ulCLIPort = ulPort;
}

void prvUDPEchoTask( void *pvParameters )
{
	int32_t lBytes = 0;
	static char cLocalBuffer[ cmdSOCKET_INPUT_BUFFER_SIZE ];
	struct freertos_sockaddr xClient;

	/* Attempt to open the socket.  The port number is passed in the task
	parameter.  The strange casting is to remove compiler warnings on 32-bit
	machines. */
	xSocket = prvOpenUDPServerSocket( ( uint16_t ) ( ( uint32_t ) pvParameters ) & 0xffffUL );
	uint32_t bits_written = 0;

	configASSERT(xSocket != FREERTOS_INVALID_SOCKET )
	for( ;; )
	{
		/* Wait for incoming data on the opened socket. */
		lBytes = FreeRTOS_recvfrom(xSocket,
								   ( void * ) cLocalBuffer,
								   sizeof( cLocalBuffer ),
								   0,
								   &xClient,
								   &xClientAddressLength );

		if( lBytes > 0 )
		{
			xClient.sin_port = FreeRTOS_htons(ECHO_PORT_BASE + ECHO_PORT);
			bits_written = FreeRTOS_sendto(xSocket,
										   cLocalBuffer,
										   lBytes,
										   0,
										   &xClient,
										   xClientAddressLength );
		}
	}
}

void vStartPTP1588Task( uint16_t usStackSize, uint32_t ulPort, UBaseType_t uxPriority )
{
	xTaskCreate( prv1588PTPTask, "PTP1588", usStackSize, ( void * ) ulPort, uxPriority, NULL );
	ulCLIPort = ulPort;
}

void prv1588PTPTask( void *pvParameters )
{
	ptpd_thread();
	vTaskDelete( NULL );
}

boolean is_ptp1588_packet(uint8_t * packet){
	return 0;
}

Socket_t prvOpenUDPServerSocket( uint16_t usPort )
{
	struct freertos_sockaddr xServer;
	Socket_t xSocket = FREERTOS_INVALID_SOCKET;
	TickType_t xSendTimeOut = 100;
	TickType_t xRecvTimeOut = 100;

	xSocket = FreeRTOS_socket( FREERTOS_AF_INET, FREERTOS_SOCK_DGRAM, FREERTOS_IPPROTO_UDP );
	if( xSocket != FREERTOS_INVALID_SOCKET)
	{
		/* Set to non-blocking sends with a timeout of zero as the socket might
		also be used for debug prints which should not block. */
		FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_SNDTIMEO, &xSendTimeOut, sizeof( xSendTimeOut ) );
		FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_RCVTIMEO, &xRecvTimeOut, sizeof( xRecvTimeOut ) );

		/* Zero out the server structure. */
		memset( ( void * ) &xServer, 0x00, sizeof( xServer ) );

		/* Set family and port. */
		xServer.sin_port = FreeRTOS_htons( usPort );

		/* Bind the address to the socket. */
		if( FreeRTOS_bind( xSocket, &xServer, sizeof( xServer ) ) == -1 )
		{
			FreeRTOS_closesocket( xSocket );
			xSocket = FREERTOS_INVALID_SOCKET;
		}
	}

	return xSocket;
}


Socket_t prvOpenUDPClientSocket( uint16_t usPort )
{
	Socket_t xSocket = FREERTOS_INVALID_SOCKET;
	TickType_t xSendTimeOut = 100;
	TickType_t xRecvTimeOut = 100;

	xSocket = FreeRTOS_socket(FREERTOS_AF_INET,
							  FREERTOS_SOCK_DGRAM,
							  FREERTOS_IPPROTO_UDP);

	configASSERT(xSocket != FREERTOS_INVALID_SOCKET);

	/* Set to non-blocking sends with a timeout of zero as the socket might
	also be used for debug prints which should not block. */
	FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_SNDTIMEO, &xSendTimeOut, sizeof( xSendTimeOut ) );
	FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_RCVTIMEO, &xRecvTimeOut, sizeof( xRecvTimeOut ) );

	return xSocket;
}

Socket_t prvOpenTCPClientSocket(uint16_t usPort){
	struct freertos_sockaddr xBindAddress;
	Socket_t xClientSocket;
	socklen_t xSize = sizeof(xBindAddress);
	static const TickType_t xTimeOut = pdMS_TO_TICKS(2000);

	xClientSocket = FreeRTOS_socket(PF_INET,
									FREERTOS_SOCK_STREAM,
									FREERTOS_IPPROTO_TCP);
	configASSERT(xClientSocket != FREERTOS_INVALID_SOCKET);

	FreeRTOS_setsockopt(xClientSocket,
						0,
						FREERTOS_SO_RCVTIMEO,
						&xTimeOut,
						sizeof(xTimeOut));

	FreeRTOS_setsockopt(xClientSocket,
						0,
						FREERTOS_SO_SNDTIMEO,
						&xTimeOut,
						sizeof(xTimeOut));

	xBindAddress.sin_port = (uint16_t) usPort;
	xBindAddress.sin_port = FreeRTOS_htons(xBindAddress.sin_port);
	xBindAddress.sin_addr = FreeRTOS_inet_addr_quick(10, 10, 10, 12);
	FreeRTOS_connect(xClientSocket, &xBindAddress, xSize);

	return xClientSocket;
}
