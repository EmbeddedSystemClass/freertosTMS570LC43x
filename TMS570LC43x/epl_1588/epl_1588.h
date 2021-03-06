//****************************************************************************
// epl_1588.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains all of the 1588/PTP related definitions and prototypes
//
//****************************************************************************

#ifndef _EPL_1588_INCLUDE
#define _EPL_1588_INCLUDE

#include "epl.h"

#define EXPORT
#define IN
#define OUT

// Adj for pin input delay and edge detection time (35ns = 8ns(refclk) * 4 + 3)
#define	PIN_INPUT_DELAY		35

// 1588 Related Definitions
#define TRGOPT_PULSE        0x00000001
#define TRGOPT_PERIODIC     0x00000002
#define TRGOPT_TRG_IF_LATE  0x00000004
#define TRGOPT_NOTIFY_EN    0x00000008
#define TRGOPT_TOGGLE_EN    0x00000010

#define TXOPT_DR_INSERT     0x00000001
#define TXOPT_IGNORE_2STEP  0x00000002
#define TXOPT_CRC_1STEP     0x00000004
#define TXOPT_CHK_1STEP     0x00000008
#define TXOPT_IP1588_EN     0x00000010
#define TXOPT_L2_EN         0x00000020
#define TXOPT_IPV6_EN       0x00000040
#define TXOPT_IPV4_EN       0x00000080
#define TXOPT_TS_EN         0x00000100
#define TXOPT_SYNC_1STEP    0x00000200
#define TXOPT_NTP_TS_EN     0x00001000

#define STSOPT_LITTLE_ENDIAN    0x00000001
#define STSOPT_IPV4             0x00000002
#define STSOPT_TXTS_EN          0x00000004
#define STSOPT_RXTS_EN          0x00000008
#define STSOPT_TRIG_EN          0x00000010
#define STSOPT_EVENT_EN         0x00000020
#define STSOPT_ERR_EN           0x00000040
#define STSOPT_PCFR_EN          0x00000080

#define RXOPT_DOMAIN_EN         0x00000001
#define RXOPT_ALT_MAST_DIS      0x00000002
#define RXOPT_USER_IP_EN        0x00000008
#define RXOPT_RX_SLAVE          0x00000010
#define RXOPT_IP1588_EN0        0x00000020
#define RXOPT_IP1588_EN1        0x00000040
#define RXOPT_IP1588_EN2        0x00000080
#define RXOPT_RX_L2_EN          0x00000100
#define RXOPT_RX_IPV6_EN        0x00000200
#define RXOPT_RX_IPV4_EN        0x00000400
#define RXOPT_SRC_ID_HASH_EN    0x00000800
#define RXOPT_RX_TS_EN          0x00001000
#define RXOPT_ACC_UDP           0x00002000
#define RXOPT_ACC_CRC           0x00004000
#define RXOPT_TS_APPEND         0x00008000
#define RXOPT_TS_INSERT         0x00010000
#define RXOPT_IPV4_UDP_MOD      0x00020000
#define RXOPT_TS_SEC_EN         0x00040000

typedef enum
{
    STS_SRC_ADDR_1 = 0x00000003,
    STS_SRC_ADDR_2 = 0x00000000,
    STS_SRC_ADDR_3 = 0x00000001,
    STS_SRC_ADDR_USE_MC = 0x00000002
} MAC_SRC_ADDRESS_ENUM;


#define CLKOPT_CLK_OUT_EN           0x00000001
#define CLKOPT_CLK_OUT_SEL          0x00000002
#define CLKOPT_CLK_OUT_SPEED_SEL    0x00000004

typedef enum PHYMSG_MESSAGE_TYPE_ENUM {
    PHYMSG_STATUS_TX,
    PHYMSG_STATUS_RX,
    PHYMSG_STATUS_TRIGGER,
    PHYMSG_STATUS_EVENT,
    PHYMSG_STATUS_ERROR,
    PHYMSG_STATUS_REG_READ
} PHYMSG_MESSAGE_TYPE_ENUM;

typedef union PHYMSG_MESSAGE {
    struct {
        uint32_t txTimestampSecs;
        uint32_t txTimestampNanoSecs;
        uint8_t  txOverflowCount;          // 2-bit value in 8-bit variable
    } TxStatus;

    struct {
        uint32_t rxTimestampSecs;
        uint32_t rxTimestampNanoSecs;
        uint8_t  rxOverflowCount;          // 2-bits data in 8-bit variable
        uint16_t sequenceId;               // 16-bits
        uint8_t  messageType;              // 4-bits data in 8 bit variable
        uint16_t sourceHash;               // 12-bit data in 16-bit variable
    } RxStatus;

    struct {
        uint16_t triggerStatus;            // Bits [11:0] indicating what triggers occurred (12 - 1 respectively).
    } TriggerStatus;

    struct {
        uint16_t ptpEstsRegBits;           // 12-bits - See PTP_ESTS register for bit definitions
        boolean   extendedEventStatusFlag;  // 8-bits  - Set to TRUE if ext. info available
        uint16_t extendedEventInfo;        // See register definition for more info
        uint32_t evtTimestampSecs;
        uint32_t evtTimestampNanoSecs;
    } EventStatus;

    struct {
        boolean frameBufOverflowFlag;       // 8-bits
        boolean frameCounterOverflowFlag;   // 8-bits
    } ErrorStatus;

    struct {
        uint8_t regIndex;                  // 5-bits data in 8-bit variable
        uint8_t regPage;                   // 3-bits data in 8-bit variable
        uint16_t readRegisterValue;        // 16-bits
    } RegReadStatus;
} PHYMSG_MESSAGE;

typedef struct PHYMSG_LIST {
    PHYMSG_MESSAGE_TYPE_ENUM msgType;
    PHYMSG_MESSAGE      phyMsg;
    struct PHYMSG_LIST  *nxtMsg;
} PHYMSG_LIST;

#define PTPEVT_TRANSMIT_TIMESTAMP_BIT   0x00000001
#define PTPEVT_RECEIVE_TIMESTAMP_BIT    0x00000002
#define PTPEVT_EVENT_TIMESTAMP_BIT      0x00000004
#define PTPEVT_TRIGGER_DONE_BIT         0x00000008

#define PTP_EVENT_PACKET_LENGTH         93

// EPL Function Prototypes
#ifdef __cplusplus
extern "C" {
#endif

void EPLWriteReg(PEPL_PORT_HANDLE epl_port_handle, uint32_t reg, uint32_t data);
uint32_t EPLReadReg(PEPL_PORT_HANDLE epl_port_handle, uint32_t reg);

void PTPEnable(
    		PEPL_PORT_HANDLE epl_port_handle,
        boolean enableFlag);

void PTPSetTriggerConfig(
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t trigger,
        uint32_t triggerBehavior,
        uint32_t gpioConnection);

void PTPSetTriggerConfig(
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t trigger,
        uint32_t triggerBehavior,
        uint32_t gpioConnection);

void PTPSetEventConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t event,
        boolean eventRiseFlag,
        boolean eventFallFlag,
        boolean eventSingle,
        uint32_t gpioConnection);

void PTPSetTransmitConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t txConfigOptions,
        uint32_t ptpVersion,
        uint32_t ptpFirstByteMask,
        uint32_t ptpFirstByteData);

uint32_t PTPReadTransmitConfig (PEPL_PORT_HANDLE epl_port_handle);

void PTPSetPhyStatusFrameConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t statusConfigOptions,
        MAC_SRC_ADDRESS_ENUM srcAddrToUse,
        uint32_t minPreamble,
        uint32_t ptpReserved,
        uint32_t ptpVersion,
        uint32_t transportSpecific,
        uint8_t messageType,
        uint32_t sourceIpAddress);

void PTPSetReceiveConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t rxConfigOptions,
        RX_CFG_ITEMS *rxConfigItems);

uint32_t PTPReadReceiveConfig (PEPL_PORT_HANDLE epl_port_handle);

uint32_t PTPCalcSourceIdHash (
        uint8_t *tenBytesData);

void PTPSetTempRateDurationConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t duration);

void PTPSetClockConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t clockConfigOptions,
        uint32_t ptpClockDivideByValue,
        uint32_t ptpClockSource,
        uint32_t ptpClockSourcePeriod);

void PTPSetGpioInterruptConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t gpioInt);

void PTPSetMiscConfig (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t ptpEtherType,
        uint32_t ptpOffset,
        uint32_t txSfdGpio,
        uint32_t rxSfdGpio);

void PTPClockStepAdjustment (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t numberOfSeconds,
        uint32_t numberOfNanoSeconds,
        boolean negativeAdj);

void PTPClockSet (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t numberOfSeconds,
        uint32_t numberOfNanoSeconds);

void PTPClockSetRateAdjustment (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t rateAdjValue,
        boolean tempAdjFlag,
        boolean adjDirectionFlag);

uint32_t PTPCheckForEvents (
    		PEPL_PORT_HANDLE epl_port_handle);

void PTPArmTrigger (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t trigger,
        uint32_t expireTimeSeconds,
        uint32_t expireTimeNanoSeconds,
        boolean initialStateFlag,
        boolean waitForRolloverFlag,
        uint32_t pulseWidth,
        uint32_t pulseWidth2);

boolean PTPHasTriggerExpired (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t trigger);

void PTPCancelTrigger (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t trigger);

uint32_t MonitorGpioSignals (
    		PEPL_PORT_HANDLE epl_port_handle
		);

void PTPClockReadCurrent (
    		PEPL_PORT_HANDLE epl_port_handle,
        int32_t *retNumberOfSeconds,
        int32_t *retNumberOfNanoSeconds);

void PTPGetTransmitTimestamp (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t *retNumberOfSeconds,
        uint32_t *retNumberOfNanoSeconds,
        uint32_t   *overflowCount);

void PTPGetReceiveTimestamp (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t *retNumberOfSeconds,
        uint32_t *retNumberOfNanoSeconds,
        uint32_t *overflowCount,
        uint32_t *sequenceId,
        uint8_t *messageType,
        uint32_t *hashValue);

void PTPGetTimestampFromFrame (
        uint8_t *receiveFrameData,
        uint32_t *retNumberOfSeconds,
        uint32_t *retNumberOfNanoSeconds);

boolean PTPGetEvent (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint32_t   *eventBits,
        uint32_t   *riseFlags,
        uint32_t *eventTimeSeconds,
        uint32_t *eventTimeNanoSeconds,
        uint32_t   *eventsMissed);

uint8_t * IsPhyStatusFrame (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint8_t *frameBuffer,
        uint16_t frameLength);

uint8_t * GetNextPhyMessage (
    		PEPL_PORT_HANDLE epl_port_handle,
        uint8_t *msgLocation,
        PHYMSG_MESSAGE_TYPE_ENUM *messageType,
        PHYMSG_MESSAGE *message);

#ifdef __cplusplus
}
#endif


#endif // _EPL_1588_INCLUDE
