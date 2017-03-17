/** ***************************************************************************************************
 * @file main.c
 * @author Lovas Szilard <lovas.szilard@gmail.com>
 * @date 2016.02.22
 * @version 0.1
 * @copyright Lovas Szilard
 * GNU GENERAL PUBLIC LICENSE Version 2, June 1991
 *
 * Homepage: http://loszi.hu/works/ti_launchpad_freertos_demo/
 *
 * @brief FreeRTOS Demo project for Hercules LAUNCHXL2-570LC43 launchpad devboard.
 *
 * @details
 * Packages:
 * FreeRTOS+IO
 * FreeRTOS+CLI
 * FreeRTOS+TCP
 * FreeRTOS+FAT
 */

/* Include Files */
#include "HL_sys_common.h"

/* FreeRTOS headers */
#include "FreeRTOS.h"
#include "FreeRTOS_IO.h"
#include "os_task.h"
#include "os_queue.h"
#include "os_semphr.h"

#include "math.h"
#include "stdio.h"
#include "stdlib.h"

/* HALCoGen generated headers has moved to sys_main.h*/
#include "sys_main.h"

/* Time related functions */
#include "rti_runtimestats.h"

/* CLI related headers */
#include "FreeRTOS_CLI.h"
#include "UARTCommandConsole.h"		/* FreeRTOS-Plus-UART-Console includes. */
#include "UDPCommandConsole.h"		/* FreeRTOS-Plus-UDP-Console includes. */
#include "CLI_commands.h"			/* CLI commands */

/* TCPIP related headers */
#include "FreeRTOSIPConfig.h"
#include "FreeRTOS_IP.h"
#include "FreeRTOS_IP_Private.h"
#include "NetworkBufferManagement.h"
#include "FreeRTOS_TCP_server.h"

/* FreeRTOS+FAT includes. */
#include "ff_headers.h"
#include "ff_stdio.h"
#include "ff_ramdisk.h"

#include "udp_echo.h"

uint8 emacAddress[6U] =	{0x00U, 0x08U, 0xEEU, ECHO_PORT, 0xA6U, 0x6CU};
uint32 emacPhyAddress =	1U;
static const uint8_t ucIPAddress[4] = {configIP_ADDR0, configIP_ADDR1, configIP_ADDR2, configIP_ADDR3};
static const uint8_t ucNetMask[4] = {configNET_MASK0, configNET_MASK1, configNET_MASK2, configNET_MASK3};
static const uint8_t ucGatewayAddress[4] = {configGATEWAY_ADDR0, configGATEWAY_ADDR1, configGATEWAY_ADDR2, configGATEWAY_ADDR3};
static const uint8_t ucDNSServerAddress[4] = {configDNS_SERVER_ADDR0, configDNS_SERVER_ADDR1, configDNS_SERVER_ADDR2, configDNS_SERVER_ADDR3};

/* Task handlers */
xTaskHandle xTask1Handle, xTask2Handle, xServerWorkTaskHandle;
extern xTaskHandle xIPTaskHandle;

/* Tasks */
void vStartNTPTask( uint16_t usTaskStackSize, UBaseType_t uxTaskPriority );

extern hdkif_t hdkif_data[MAX_EMAC_INSTANCE];
extern void vRegisterFileSystemCLICommands( void );
extern void vCreateAndVerifyExampleFiles( const char *pcMountPath );
extern void vStdioWithCWDTest( const char *pcMountPath );
float xConvertAdcValueToNtcTemperature(uint16_t xAdcValue, uint16_t xAdcMaxValue, float xR1, float xA, float xB, float xD);

/* Hook functions */
BaseType_t xApplicationDNSQueryHook( const char *pcName );
const char *pcApplicationHostnameHook( void );
void vApplicationTickHook(void);
void vApplicationIdleHook(void);
void vApplicationStackOverflowHook(TaskHandle_t xTask, signed char *pcTaskName);

/* FTP and HTTP servers execute in the TCP server work task. */
#define mainTCP_SERVER_TASK_PRIORITY	( tskIDLE_PRIORITY + 2 )
#define	mainTCP_SERVER_STACK_SIZE		( configMINIMAL_STACK_SIZE * 12 )

/** ***************************************************************************************************
 * @fn		void main(void)
 * @brief	main function.
 */
void main(void)
{
	/* Initialize HALCoGen driver. */
	gioInit();
	gioSetDirection(hetPORT1, 0xAA07C821);
	gioSetDirection(hetPORT2, 0x00000000);
	sciInit();

	_enable_IRQ();

	/* Register some commands to CLI */
#if ( configGENERATE_RUN_TIME_STATS == 1 )
	FreeRTOS_CLIRegisterCommand( &xTaskStats );
	FreeRTOS_CLIRegisterCommand( &xRunTimeStats );
#endif
	// FreeRTOS_CLIRegisterCommand( &xMemTest ); /* Tests onboard 8M external memory on TMDX570LC43HDK devboard (and also ruins the ram disk) */
	FreeRTOS_CLIRegisterCommand( &xEmacStat );
	FreeRTOS_CLIRegisterCommand( &xPing );
	FreeRTOS_CLIRegisterCommand( &xNetStat );
	FreeRTOS_CLIRegisterCommand( &xReset );

	FreeRTOS_IPInit(ucIPAddress, ucNetMask, ucGatewayAddress, ucDNSServerAddress, emacAddress);

	/* Start the command interpreter */
	vStartUARTCommandInterpreterTask();

	vTaskStartScheduler();
	while(1);
}

/** ***************************************************************************************************
 * @fn		const char *pcApplicationHostnameHook(void)
 * @brief	DHCP hostname register hook function.
 * @details
 * Assign the name defined with "mainDEVICE_NICK_NAME" to this network node during DHCP.
 */
BaseType_t xApplicationDNSQueryHook(const char *pcName)
{
BaseType_t xReturn;

	/* Determine if a name lookup is for this node.  Two names are given
	to this node: that returned by pcApplicationHostnameHook() and that set
	by mainDEVICE_NICK_NAME. */
	if( strcmp( pcName, pcApplicationHostnameHook() ) == 0 )
	{
		xReturn = pdPASS;
	}
	else if( strcmp( pcName, mainDEVICE_NICK_NAME ) == 0 )
	{
		xReturn = pdPASS;
	}
	else
	{
		xReturn = pdFAIL;
	}

	return xReturn;
}

void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )
{
static BaseType_t xTasksAlreadyCreated = pdFALSE;

if( eNetworkEvent == eNetworkUp )
    {
        if( xTasksAlreadyCreated == pdFALSE )
        {
        	/* Start the UDP command line on port 5001 */
//        	vStartUDPCommandInterpreterTask( mainUDP_CLI_TASK_STACK_SIZE, mainUDP_CLI_PORT_NUMBER, mainUDP_CLI_TASK_PRIORITY );


        	vStartPTP1588Task(mainPTP1588_TASK_STACK_SIZE, mainPTP1588_PORT_NUMBER, mainPTP1588_TASK_PRIORITY);

        	/* Start the UDP echo on port 5000 */
        	vStartUDPEchoTask(mainUDP_Echo_TASK_STACK_SIZE, mainUDP_Echo_PORT_NUMBER, mainUDP_Echo_TASK_PRIORITY);

        	xTasksAlreadyCreated = pdTRUE;
        }

    }
}

/** ***************************************************************************************************
 * @fn		const char *pcApplicationHostnameHook(void)
 * @brief	DHCP hostname register hook function.
 * @details
 * Assign the name defined with "mainDEVICE_NICK_NAME" to this network node during DHCP.
 */
const char *pcApplicationHostnameHook(void)
{
	return mainDEVICE_NICK_NAME;
}

/** ***************************************************************************************************
 * @fn		void vApplicationTickHook(void)
 * @brief	TICK hook function.
 */
void vApplicationTickHook(void)
{
}

/** ***************************************************************************************************
 * @fn		void vApplicationIdleHook(void)
 * @brief	IDLE hook function.
 */
void vApplicationIdleHook(void)
{
}

/** ***************************************************************************************************
 * @fn		void vApplicationMallocFailedHook(void)
 * @brief	Malloc() fail hook function.
 */
void vApplicationMallocFailedHook(void)
{
	volatile uint32_t ulMallocFailures = 0;
	ulMallocFailures++;
}

/** ***************************************************************************************************
 * @fn		void vApplicationStackOverflowHook(TaskHandle_t xTask, signed char *pcTaskName)
 * @brief	Stack overflow hook function.
 */
void vApplicationStackOverflowHook(TaskHandle_t xTask, signed char *pcTaskName)
{
	( void ) pcTaskName;
	configASSERT(0);
}

#if(ipconfigSUPPORT_OUTGOING_PINGS == 1)
/** ***************************************************************************************************
 * @fn		void vApplicationPingReplyHook(ePingReplyStatus_t eStatus, uint16_t usIdentifier)
 * @brief	Ping reply hook function.
 */
void vApplicationPingReplyHook(ePingReplyStatus_t eStatus, uint16_t usIdentifier)
{
static const char *pcSuccess = "Ping reply received - identifier %d\r\n";
static const char *pcInvalidChecksum = "Ping reply received with invalid checksum - identifier %d\r\n";
static const char *pcInvalidData = "Ping reply received with invalid data - identifier %d\r\n";

	switch(eStatus)
	{
		case eSuccess	:
			FreeRTOS_printf((pcSuccess, (int)usIdentifier));
			break;
		case eInvalidChecksum :
			FreeRTOS_printf((pcInvalidChecksum, (int)usIdentifier));
			break;
		case eInvalidData :
			FreeRTOS_printf((pcInvalidData, (int)usIdentifier));
			break;
		default :
			/* It is not possible to get here as all enums have their own case. */
			break;
	}
	/* Prevent compiler warnings in case FreeRTOS_debug_printf() is not defined. */
	(void) usIdentifier;
}
#endif
