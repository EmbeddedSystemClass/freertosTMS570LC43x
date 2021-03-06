/* ptpd.c */

#include "ptpd.h"

#define __IO

#define PTPD_THREAD_PRIO    (tskIDLE_PRIORITY + 2)

//static sys_mbox_t ptp_alert_queue;

// Statically allocated run-time configuration data.
RunTimeOpts rtOpts;
PtpClock ptpClock;
ForeignMasterRecord ptpForeignRecords[DEFAULT_MAX_FOREIGN_RECORDS];

#include "NetworkInterface.h"
RX_CFG_ITEMS rxCfgItems;
uint32_t rxCfgOpts;
extern hdkif_t hdkif_data[];
extern uint8 emacAddress[6U];

void * protomalloc(void * allocator_data, size_t size){
	return malloc(size);
}

void protofree(void * allocator_data, void *pointer){
	return free(pointer);
}

ProtobufCAllocator protoallocator = {
		.alloc = protomalloc,
		.free = protofree,
		.allocator_data = NULL,
};


__IO uint32_t PTPTimer = 0;

void proto_practice(void){

//	AeroNetwork__TimingPacket timing_packet;
//	aero_network__timing_packet__init(&timing_packet);
//	timing_packet.mac_address = *(int64_t*)emacAddress;
//	timing_packet.offset_from_master_s = 1;
//	timing_packet.offset_from_master_ns = 2;
//	timing_packet.mean_path_delay_s = 3;
//	timing_packet.mean_path_delay_ns = 4;
//
//	size_t pack_size = aero_network__timing_packet__get_packed_size(&timing_packet);
//	uint8_t * packet_buffer = malloc(pack_size);
//	memset(packet_buffer, 0, pack_size);
//	aero_network__timing_packet__pack(&timing_packet, packet_buffer);
//
//	AeroNetwork__TimingPacket * unpacked = aero_network__timing_packet__unpack(&protoallocator, pack_size, packet_buffer);
//	free(unpacked);
//	free(packet_buffer);
}

//static void ptpd_thread(void *arg)
void ptpd_thread(void *arg)
{
	proto_practice();
    PEPL_PORT_HANDLE epl_port_handle = pvPortMalloc(sizeof(PORT_OBJ));
    epl_port_handle->oaiDevHandle = pvPortMalloc(sizeof(OAI_DEV_HANDLE_STRUCT));
    epl_port_handle->oaiDevHandle->regularMutex = xSemaphoreCreateMutex();
    epl_port_handle->oaiDevHandle->multiOpMutex = xSemaphoreCreateRecursiveMutex();

    rtOpts.epl_port_handle = epl_port_handle;

    epl_port_handle->psfConfigOptions |= STSOPT_IPV4;
    epl_port_handle->psfConfigOptions |= STSOPT_LITTLE_ENDIAN;
    epl_port_handle->psfConfigOptions |= STSOPT_TXTS_EN;
    epl_port_handle->psfConfigOptions |= STSOPT_RXTS_EN;

    memset(&(epl_port_handle->rxCfgItems), 0, sizeof(RX_CFG_ITEMS));
    rxCfgItems.ptpVersion = 0x02;
    rxCfgItems.ptpFirstByteMask = 0x00;
    rxCfgItems.ptpFirstByteData = 0x00;
    rxCfgItems.ipAddrData = 0;
    rxCfgItems.tsMinIFG = 0x0C;
    rxCfgItems.srcIdHash = 0;
    rxCfgItems.ptpDomain = 0;
    rxCfgItems.tsSecLen = 3;
    rxCfgItems.rxTsSecondsOffset = 8;
    rxCfgItems.rxTsNanoSecOffset = 12;

    rxCfgOpts = 0;
    rxCfgOpts = RXOPT_IP1588_EN0|RXOPT_IP1588_EN1|RXOPT_IP1588_EN2|
   					   RXOPT_RX_L2_EN|RXOPT_RX_IPV4_EN|RXOPT_ACC_UDP|RXOPT_ACC_CRC|
   					   RXOPT_TS_INSERT|RXOPT_RX_TS_EN|RXOPT_TS_SEC_EN;

    hdkif_t *hdkif;
    hdkif = &hdkif_data[0U];
    epl_port_handle->hdkif = *hdkif;
    epl_port_handle->rxCfgItems = rxCfgItems;
    epl_port_handle->rxCfgOpts = rxCfgOpts;
    EMACInstConfig(hdkif);
    init1588(epl_port_handle);

	// Initialize run-time options to default values.
	rtOpts.announceInterval = DEFAULT_ANNOUNCE_INTERVAL;
	rtOpts.syncInterval = DEFAULT_SYNC_INTERVAL;
	rtOpts.clockQuality.clockAccuracy = DEFAULT_CLOCK_ACCURACY;
	rtOpts.clockQuality.clockClass = DEFAULT_CLOCK_CLASS;
	rtOpts.clockQuality.offsetScaledLogVariance = DEFAULT_CLOCK_VARIANCE; /* 7.6.3.3 */
	rtOpts.priority1 = DEFAULT_PRIORITY1;
	rtOpts.priority2 = DEFAULT_PRIORITY2;
	rtOpts.domainNumber = DEFAULT_DOMAIN_NUMBER;
	rtOpts.slaveOnly = SLAVE_ONLY;
	rtOpts.currentUtcOffset = DEFAULT_UTC_OFFSET;
	rtOpts.servo.noResetClock = DEFAULT_NO_RESET_CLOCK;
	rtOpts.servo.noAdjust = NO_ADJUST;
	rtOpts.inboundLatency.nanoseconds = DEFAULT_INBOUND_LATENCY;
	rtOpts.outboundLatency.nanoseconds = DEFAULT_OUTBOUND_LATENCY;
	rtOpts.servo.sDelay = DEFAULT_DELAY_S;
	rtOpts.servo.sOffset = DEFAULT_OFFSET_S;
	rtOpts.servo.ap = DEFAULT_AP;
	rtOpts.servo.ai = DEFAULT_AI;
	rtOpts.maxForeignRecords = sizeof(ptpForeignRecords) / sizeof(ptpForeignRecords[0]);
	rtOpts.stats = PTP_TEXT_STATS;
	rtOpts.delayMechanism = DEFAULT_DELAY_MECHANISM;

	// Initialize run time options.
	if (ptpdStartup(&ptpClock, &rtOpts, ptpForeignRecords) != 0)
	{
		printf("PTPD: startup failed");
		return;
	}

	// Loop forever.
	for (;;)
	{
		void *msg;

		// Process the current state.
		do
		{
			// doState() has a switch for the actions and events to be
			// checked for 'port_state'. The actions and events may or may not change
			// 'port_state' by calling toState(), but once they are done we loop around
			// again and perform the actions required for the new 'port_state'.
			doState(&ptpClock);
		}
		while (netSelect(&ptpClock.netPath, 0) > 0);
		
		// Wait up to 100ms for something to do, then do something anyway.
//		sys_arch_mbox_fetch(&ptp_alert_queue, &msg, 100);
	}


//    epl_port_handle->oaiDevHandle->regularMutex = xSemaphoreCreateRecursiveMutex();
//    xSemaphore();
//
//    epl_port_handle->oaiDevHandle->regularMutex = xSemaphoreCreateMutex();
//    epl_port_handle->oaiDevHandle->regularMutex = xSemaphoreCreateMutex();
//
//    epl_port_handle->oaiDevHandle = pvPortMalloc(sizeof(OAI_DEV_HANDLE_STRUCT));
//    epl_port_handle->oaiDevHandle = pvPortMalloc(sizeof(OAI_DEV_HANDLE_STRUCT));
//
//    vPortFree(epl_port_handle);
}

void initEMAC(PEPL_PORT_HANDLE epl_port_handle){
    epl_port_handle->psfConfigOptions |= STSOPT_IPV4;
    epl_port_handle->psfConfigOptions |= STSOPT_LITTLE_ENDIAN;
    epl_port_handle->psfConfigOptions |= STSOPT_TXTS_EN;
    epl_port_handle->psfConfigOptions |= STSOPT_RXTS_EN;

    memset(&(epl_port_handle->rxCfgItems), 0, sizeof(RX_CFG_ITEMS));
    epl_port_handle->rxCfgItems.ptpVersion = 0x02;
    epl_port_handle->rxCfgItems.ptpFirstByteMask = 0x00;
    epl_port_handle->rxCfgItems.ptpFirstByteData = 0x00;
    epl_port_handle->rxCfgItems.ipAddrData = 0;
    epl_port_handle->rxCfgItems.tsMinIFG = 0x0C;
    epl_port_handle->rxCfgItems.srcIdHash = 0;
    epl_port_handle->rxCfgItems.ptpDomain = 0;
    epl_port_handle->rxCfgItems.tsSecLen = 3;
    epl_port_handle->rxCfgItems.rxTsSecondsOffset = 8;
    epl_port_handle->rxCfgItems.rxTsNanoSecOffset = 12;

    epl_port_handle->rxCfgOpts = 0;
    epl_port_handle->rxCfgOpts = RXOPT_IP1588_EN0|RXOPT_IP1588_EN1|RXOPT_IP1588_EN2|
  					   RXOPT_RX_L2_EN|RXOPT_RX_IPV4_EN|RXOPT_ACC_UDP|RXOPT_ACC_CRC|
  					   RXOPT_TS_INSERT|RXOPT_RX_TS_EN|RXOPT_TS_SEC_EN;

  init1588(epl_port_handle);
}

//// Notify the PTP thread of a pending operation.
//void ptpd_alert(void)
//{
//	// Send a message to the alert queue to wake up the PTP thread.
//	sys_mbox_trypost(&ptp_alert_queue, NULL);
//}
//
//void ptpd_init(void)
//{
//	// Create the alert queue mailbox.
//  if (sys_mbox_new(&ptp_alert_queue, 8) != ERR_OK)
//	{
//    printf("PTPD: failed to create ptp_alert_queue mbox");
//  }
//
//	// Create the PTP daemon thread.
//	sys_thread_new("PTPD", ptpd_thread, NULL, DEFAULT_THREAD_STACKSIZE * 2, osPriorityAboveNormal);
//}
//
