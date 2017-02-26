/* datatypes.h */
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
distribution of COMPANY’s Products, and only subject to the following 
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


#ifndef DATATYPES_H
#define DATATYPES_H

#include "HL_emac.h"

typedef struct {
  UInteger32 seconds;
  Integer32 nanoseconds;  
} TimeRepresentation;

typedef struct {
  Integer32 seconds;
  Integer32 nanoseconds;  
} TimeInternal;

typedef struct {
  Integer32  interval;
  Integer32  left;
  Boolean expire;
  Integer32  lastTime;
} IntervalTimer;

/* Message header */
typedef struct {
  UInteger16  versionPTP;
  UInteger16  versionNetwork;
  Octet subdomain[PTP_SUBDOMAIN_NAME_LENGTH];
  UInteger8  messageType;
  UInteger8  sourceCommunicationTechnology;
  Octet  sourceUuid[PTP_UUID_LENGTH];
  UInteger16  sourcePortId;
  UInteger16  sequenceId;
  UInteger8  control;
  Octet  flags[2];
  
} MsgHeader;

/* Sync or Delay_Req message */
typedef struct {
  TimeRepresentation  originTimestamp;
  UInteger16  epochNumber;
  Integer16  currentUTCOffset;
  UInteger8  grandmasterCommunicationTechnology;
  Octet  grandmasterClockUuid[PTP_UUID_LENGTH];
  UInteger16  grandmasterPortId;
  UInteger16  grandmasterSequenceId;
  UInteger8  grandmasterClockStratum;
  Octet  grandmasterClockIdentifier[PTP_CODE_STRING_LENGTH];
  Integer16  grandmasterClockVariance;
  Boolean  grandmasterPreferred;
  Boolean  grandmasterIsBoundaryClock;
  Integer16  syncInterval;
  Integer16  localClockVariance;
  UInteger16  localStepsRemoved;
  UInteger8  localClockStratum;
  Octet  localClockIdentifer[PTP_CODE_STRING_LENGTH];
  UInteger8  parentCommunicationTechnology;
  Octet  parentUuid[PTP_UUID_LENGTH];
  UInteger16  parentPortField;
  Integer16  estimatedMasterVariance;
  Integer32  estimatedMasterDrift;
  Boolean  utcReasonable;
  
} MsgSync;

typedef MsgSync MsgDelayReq;

/* Follow_Up message */
typedef struct {
  UInteger16  associatedSequenceId;
  TimeRepresentation  preciseOriginTimestamp;
  
} MsgFollowUp;

/* Delay_Resp message */
typedef struct {
  TimeRepresentation  delayReceiptTimestamp;
  UInteger8  requestingSourceCommunicationTechnology;
  Octet  requestingSourceUuid[PTP_UUID_LENGTH];
  UInteger16  requestingSourcePortId;
  UInteger16  requestingSourceSequenceId;
  
} MsgDelayResp;

/* Management message */
typedef union
{
  struct ClockIdentity
  {
    UInteger8  clockCommunicationTechnology;
    Octet  clockUuidField[PTP_UUID_LENGTH];
    UInteger16  clockPortField;
    Octet  manufacturerIdentity[MANUFACTURER_ID_LENGTH];
  } clockIdentity;
  
  struct DefaultData
  {
    UInteger8  clockCommunicationTechnology;
    Octet  clockUuidField[PTP_UUID_LENGTH];
    UInteger16  clockPortField;
    UInteger8  clockStratum;
    Octet  clockIdentifier[PTP_CODE_STRING_LENGTH];
    Integer16  clockVariance;
    Boolean  clockFollowupCapable;
    Boolean  preferred;
    Boolean  initializable;
    Boolean  externalTiming;
    Boolean  isBoundaryClock;
    Integer16  syncInterval;
    Octet  subdomainName[PTP_SUBDOMAIN_NAME_LENGTH];
    UInteger16  numberPorts;
    UInteger16  numberForeignRecords;
  } defaultData;
  
  struct Current
  {
    UInteger16  stepsRemoved;
    TimeRepresentation  offsetFromMaster;
    TimeRepresentation  oneWayDelay;
  } current;
  
  struct Parent
  {
    UInteger8  parentCommunicationTechnology;
    Octet  parentUuid[PTP_UUID_LENGTH];
    UInteger16  parentPortId;
    UInteger16  parentLastSyncSequenceNumber;
    Boolean  parentFollowupCapable;
    Boolean  parentExternalTiming;
    Integer16  parentVariance;
    Boolean  parentStats;
    Integer16  observedVariance;
    Integer32  observedDrift;
    Boolean  utcReasonable;
    UInteger8  grandmasterCommunicationTechnology;
    Octet  grandmasterUuidField[PTP_UUID_LENGTH];
    UInteger16  grandmasterPortIdField;
    UInteger8  grandmasterStratum;
    Octet  grandmasterIdentifier[PTP_CODE_STRING_LENGTH];
    Integer16  grandmasterVariance;
    Boolean  grandmasterPreferred;
    Boolean  grandmasterIsBoundaryClock;
    UInteger16  grandmasterSequenceNumber;
  } parent;
  
  struct Port
  {
    UInteger16  returnedPortNumber;
    UInteger8  portState;
    UInteger16  lastSyncEventSequenceNumber;
    UInteger16  lastGeneralEventSequenceNumber;
    UInteger8  portCommunicationTechnology;
    Octet  portUuidField[PTP_UUID_LENGTH];
    UInteger16  portIdField;
    Boolean  burstEnabled;
    UInteger8  subdomainAddressOctets;
    UInteger8  eventPortAddressOctets;
    UInteger8  generalPortAddressOctets;
    Octet  subdomainAddress[SUBDOMAIN_ADDRESS_LENGTH];
    Octet  eventPortAddress[PORT_ADDRESS_LENGTH];
    Octet  generalPortAddress[PORT_ADDRESS_LENGTH];
  } port;
  
  struct GlobalTime
  {
    TimeRepresentation  localTime;
    Integer16  currentUtcOffset;
    Boolean  leap59;
    Boolean  leap61;
    UInteger16  epochNumber;
  } globalTime;
  
  struct Foreign
  {
    UInteger16  returnedPortNumber;
    UInteger16  returnedRecordNumber;
    UInteger8  foreignMasterCommunicationTechnology;
    Octet  foreignMasterUuid[PTP_UUID_LENGTH];
    UInteger16  foreignMasterPortId;
    UInteger16  foreignMasterSyncs;
  } foreign;
  
} MsgManagementPayload;

typedef struct {
  UInteger8  targetCommunicationTechnology;
  Octet  targetUuid[PTP_UUID_LENGTH];
  UInteger16  targetPortId;
  Integer16  startingBoundaryHops;
  Integer16  boundaryHops;
  UInteger8  managementMessageKey;
  UInteger16  parameterLength;
  UInteger16  recordKey;
  
  MsgManagementPayload payload;
} MsgManagement;

typedef struct
{
  UInteger8  foreign_master_communication_technology;
  Octet  foreign_master_uuid[PTP_UUID_LENGTH];
  UInteger16  foreign_master_port_id;
  UInteger16  foreign_master_syncs;
  
  MsgHeader  header;
  MsgSync  sync;
} ForeignMasterRecord;

/* program options set at run-time */
typedef struct RunTimeOpts {
  Boolean revA1SiliconFlag;
  Integer16  syncInterval;
  Octet  subdomainName[PTP_SUBDOMAIN_NAME_LENGTH];
  Octet  clockIdentifier[PTP_CODE_STRING_LENGTH];
  UInteger32  clockVariance;
  UInteger8  clockStratum;
  Boolean  clockPreferred;
  Integer16  currentUtcOffset;
  UInteger16  epochNumber;
  Octet  ifaceName[IFACE_NAME_LENGTH];
  Boolean  noResetClock;
  Boolean  noAdjust;
  Boolean  displayStats;
  Boolean  csvStats;
  Octet  directAddress[NET_ADDRESS_LENGTH];
  Integer16  ap, ai;
  Integer16  s;
  TimeInternal  inboundLatency, outboundLatency;
  Integer16  max_foreign_records;
  Boolean  slaveOnly;
  Boolean  probe;
  UInteger8  probe_management_key;
  UInteger16  probe_record_key;
  Boolean  halfEpoch;

  Octet destMACAddress[NET_ADDRESS_LENGTH];  
  Octet localMACAddress[NET_ADDRESS_LENGTH];  
  Boolean udpChksumEnable;
  
  Octet srcIPAddress[4];

  void *eplPortHandle;
  hdkif_t hdkif;

//  OAI_DEV_HANDLE_STRUCT *oaiHandle;
  
  Boolean forceBMCFlag;
  Boolean useOneStepFlag;
  Boolean useTempRateFlag;
  NS_UINT tempRateLength;
  
  Boolean limiterEnable;
  NS_UINT limiterThresh;
  NS_UINT limiterThreshMax;
  NS_UINT limiterGoodThresh;
  NS_UINT limiterLimitMultiplier;
  
  TimeInternal syncAdjustValue;
  TimeInternal delayReqAdjustValue;
  
  int numRateSamples;
  int numRateAvgs;
  int numOneWayAvgSamples;
  
  Boolean syncEthMode;
  Boolean phaseAlignClkoutFlag;
  Boolean clkOutEnableFlag;
  NS_UINT clkOutDivide;
  Boolean clkOutSpeed;
  Boolean clkOutSource;
  Boolean ppsEnableFlag;
  NS_UINT ppsStartTime;
  Boolean ppsRiseOrFallFlag;
  NS_UINT ppsGpio;

  NS_UINT clkOutPeriod;
  
  Boolean haveLoopbackedSend;
  NS_UINT lastSendLength;
  
  Octet txBuff[2048];
  Octet rxBuff[2048];
  
} RunTimeOpts;

/* main program data structure */
typedef struct {
  /* Default data set */
  UInteger8  clock_communication_technology;
  Octet  clock_uuid_field[PTP_UUID_LENGTH];
  UInteger16  clock_port_id_field;
  UInteger8  clock_stratum;
  Octet  clock_identifier[PTP_CODE_STRING_LENGTH];
  Integer16  clock_variance;
  Boolean  clock_followup_capable;
  Boolean  preferred;
  Boolean  initializable;
  Boolean  external_timing;
  Boolean  is_boundary_clock;
  Integer16  sync_interval;
  Octet  subdomain_name[PTP_SUBDOMAIN_NAME_LENGTH];
  UInteger16  number_ports;
  UInteger16  number_foreign_records;
  
  /* Current data set */
  UInteger16  steps_removed;
  TimeInternal  offset_from_master;
  TimeInternal  one_way_delay;
  
  /* Parent data set */
  UInteger8  parent_communication_technology;
  Octet  parent_uuid[PTP_UUID_LENGTH];
  UInteger16  parent_port_id;
  UInteger16  parent_last_sync_sequence_number;
  Boolean  parent_followup_capable;
  Boolean  parent_external_timing;
  Integer16  parent_variance;
  Boolean  parent_stats;
  Integer16  observed_variance;
  Integer32  observed_drift;
  Boolean  utc_reasonable;
  UInteger8  grandmaster_communication_technology;
  Octet  grandmaster_uuid_field[PTP_UUID_LENGTH];
  UInteger16  grandmaster_port_id_field;
  UInteger8  grandmaster_stratum;
  Octet  grandmaster_identifier[PTP_CODE_STRING_LENGTH];
  Integer16  grandmaster_variance;
  Boolean  grandmaster_preferred;
  Boolean  grandmaster_is_boundary_clock;
  UInteger16  grandmaster_sequence_number;
  
  /* Global time properties data set */
  Integer16  current_utc_offset;
  Boolean  leap_59;
  Boolean  leap_61;
  UInteger16  epoch_number;
  
  /* Port configuration data set */
  UInteger8  port_state;
  UInteger16  last_sync_event_sequence_number;
  UInteger16  last_general_event_sequence_number;
  Octet  subdomain_address[SUBDOMAIN_ADDRESS_LENGTH];
  Octet  event_port_address[PORT_ADDRESS_LENGTH];
  Octet  general_port_address[PORT_ADDRESS_LENGTH];
  UInteger8  port_communication_technology;
  Octet  port_uuid_field[PTP_UUID_LENGTH];
  UInteger16  port_id_field;
  Boolean  burst_enabled;
  
  /* Foreign master data set */
  ForeignMasterRecord *foreign;
  
  /* Other things we need for the protocol */
  Boolean halfEpoch;
  
  Integer16  max_foreign_records;
  Integer16  foreign_record_i;
  Integer16  foreign_record_best;
  Boolean  record_update;
  UInteger32 random_seed;
  
  MsgHeader msgTmpHeader;
  
  union {
    MsgSync  sync;
    MsgFollowUp  follow;
    MsgDelayReq  req;
    MsgDelayResp  resp;
    MsgManagement  manage;
  } msgTmp;
  
  Octet msgObuf[PACKET_SIZE];
  Octet msgIbuf[PACKET_SIZE];
  
  TimeInternal  master_to_slave_delay;
  TimeInternal  slave_to_master_delay;
  
  TimeInternal  delay_req_receive_time;
  TimeInternal  delay_req_send_time;
  TimeInternal  sync_receive_time;
  
  UInteger16  Q;
  UInteger16  R;
  
  Boolean  sentDelayReq;
  UInteger16  sentDelayReqSequenceId;
  Boolean  waitingForFollow;
  
  offset_from_master_filter  ofm_filt;
  one_way_delay_filter  owd_filt;
  
  Boolean message_activity;
  
  IntervalTimer  itimer[TIMER_ARRAY_SIZE];
  
  NetPath netPath;
  
  //struct RunTimeOpts *rtOpts;
  RunTimeOpts *rtOpts;

  int numSyncsSeen;
  int lastOffset;
  int currRateAdj;
  
  TimeInternal oneWayList[64];
  int oneWayWriteIdx;
  int numOneWayValues;
  TimeInternal oneWayAvg;
  
  Boolean ignoreNextRateFlag;
  
  double prevOffsetFromMaster;
  TimeInternal offsetDelta;

  Boolean didStepFlag;
  Boolean waitingForAdjFlag;
  
  NS_UINT ignoreSyncCount;
  NS_UINT numGoodOffsets;
                                            
  TimeInternal prevSyncRxTime;
  TimeInternal prevSyncTxTime;
  int currRate;
  int lastRateAdj;
  
  int rateHistory[64];
  int rateSampleRateIdx;
  int numRateHistValues;
  
  int avgRatesHistory[64];
  int avgRatesWriteIdx;
  int numAvgRatesHistValues;

} PtpClock;

#endif
