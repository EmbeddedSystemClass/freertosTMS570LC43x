/* protocol.c */
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


#include "ptpd.h"

Boolean doInit(RunTimeOpts*,PtpClock*);
void doState(RunTimeOpts*,PtpClock*);
void toState(UInteger8,RunTimeOpts*,PtpClock*);

void handle(RunTimeOpts*,PtpClock*);
void handleSync(MsgHeader*,Octet*,TimeInternal*,Boolean,RunTimeOpts*,PtpClock*);
void handleFollowUp(MsgHeader*,Octet*,Boolean,RunTimeOpts*,PtpClock*);
void handleDelayReq(MsgHeader*,TimeInternal*,Boolean,RunTimeOpts*,PtpClock*);
void handleDelayResp(MsgHeader*,Octet*,Boolean,RunTimeOpts*,PtpClock*);
void handleManagement(MsgHeader*,Octet*,Boolean,RunTimeOpts*,PtpClock*);

void issueSync(RunTimeOpts*,PtpClock*);
void issueFollowup(TimeInternal*,RunTimeOpts*,PtpClock*);
void issueDelayReq(RunTimeOpts*,PtpClock*);
void issueDelayResp(TimeInternal*,MsgHeader*,RunTimeOpts*,PtpClock*);
void issueManagement(MsgHeader*,MsgManagement*,RunTimeOpts*,PtpClock*);

MsgSync * addForeign(Octet*,MsgHeader*,PtpClock*);

void PTPUpdateStatus(
    NS_UINT8 stsType,
    RunTimeOpts *rtOpts,
    PtpClock *ptpClock);


/* loop forever. doState() has a switch for the actions and events to be
   checked for 'port_state'. the actions and events may or may not change
   'port_state' by calling toState(), but once they are done we loop around
   again and perform the actions required for the new 'port_state'. */
void protocol(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  DBG("event POWERUP\n");
  
  toState(PTP_INITIALIZING, rtOpts, ptpClock);
  
  for(;;)
  {
    if(ptpClock->port_state != PTP_INITIALIZING)
      doState(rtOpts, ptpClock);
    else if(!doInit(rtOpts, ptpClock))
      return;
    
    if(ptpClock->message_activity)
      DBGV("activity\n");
    else
    {
      Sleep(0);
      //DBGV("no activity\n")
    }
      
    if ( rtOpts->oaiHandle->killThread)
        break;

    Sleep(0);
  }
}

Boolean doInit(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  DBG("manufacturerIdentity: %s\n", MANUFACTURER_ID);
  
  /* initialize networking */
  netShutdown(&ptpClock->netPath);
  if(!netInit(&ptpClock->netPath, rtOpts, ptpClock))
  {
    ERROR("failed to initialize network\n");
    toState(PTP_FAULTY, rtOpts, ptpClock);
    return FALSE;
  }
  
  /* initialize other stuff */
  initData(rtOpts, ptpClock);
  initTimer();
  initClock(rtOpts, ptpClock);
  m1(ptpClock);
  msgPackHeader(ptpClock->msgObuf, ptpClock);
  
  DBG("sync message interval: %d\n", PTP_SYNC_INTERVAL_TIMEOUT(ptpClock->sync_interval));
  DBG("clock identifier: %4.4s\n", ptpClock->clock_identifier);
  DBG("256*log2(clock variance): %d\n", ptpClock->clock_variance);
  DBG("clock stratum: %d\n", ptpClock->clock_stratum);
  DBG("clock preferred?: %s\n", ptpClock->preferred?"yes":"no");
  DBG("bound interface name: %s\n", rtOpts->ifaceName);
  DBG("communication technology: %d\n", ptpClock->port_communication_technology);
  DBG("uuid: %02hhX:%02hhX:%02hhX:%02hhX:%02hhX:%02hhX\n",
    ptpClock->port_uuid_field[0]&0xFF, ptpClock->port_uuid_field[1]&0xFF, ptpClock->port_uuid_field[2]&0xFF,
    ptpClock->port_uuid_field[3]&0xFF, ptpClock->port_uuid_field[4]&0xFF, ptpClock->port_uuid_field[5]&0xFF);
  DBG("PTP subdomain name: %s\n", ptpClock->subdomain_name);
  DBG("subdomain address: %02hhX.%02hhX.%02hhX.%02hhX\n",
    ptpClock->subdomain_address[0]&0xFF, ptpClock->subdomain_address[1]&0xFF,
    ptpClock->subdomain_address[2]&0xFF, ptpClock->subdomain_address[3]&0xFF);
  DBG("event port address: %02hhX %02hhX\n",
    ptpClock->event_port_address[0]&0xFF, ptpClock->event_port_address[1]&0xFF);
  DBG("general port address: %02hhX %02hhX\n",
    ptpClock->general_port_address[0]&0xFF, ptpClock->general_port_address[1]&0xFF);

  if ( !rtOpts->slaveOnly)
  {
      if ( rtOpts->forceBMCFlag)
      {
          toState(PTP_MASTER, rtOpts, ptpClock);
          DBG( "Assuming local clock is Best Master Clock. Skipping BMC wait.\n");
      }
      else
      {
          DBG( "Running BMC algorithm, waiting to hear from other masters.\n");
          toState(PTP_LISTENING, rtOpts, ptpClock);
      }
  }
  else
  {
      toState(PTP_LISTENING, rtOpts, ptpClock);
  }
  
  return TRUE;
}

/* handle actions and events for 'port_state' */
void doState(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  UInteger8 state;
  
  ptpClock->message_activity = FALSE;
  
  switch(ptpClock->port_state)
  {
  case PTP_LISTENING:
  case PTP_PASSIVE:
  case PTP_SLAVE:
  case PTP_MASTER:
    if(ptpClock->record_update)
    {
      ptpClock->record_update = FALSE;
      state = bmc(ptpClock->foreign, rtOpts, ptpClock);
      if(state != ptpClock->port_state)
        toState(state, rtOpts, ptpClock);
    }
    break;
    
  default:
    break;
  }
  
  switch(ptpClock->port_state)
  {
  case PTP_FAULTY:
    /* imaginary troubleshooting */
    
    DBG("event FAULT_CLEARED\n");
    toState(PTP_INITIALIZING, rtOpts, ptpClock);
    return;
    
  case PTP_LISTENING:
  case PTP_PASSIVE:
  case PTP_UNCALIBRATED:
  case PTP_SLAVE:
    handle(rtOpts, ptpClock);
    
    if(timerExpired(SYNC_RECEIPT_TIMER, ptpClock->itimer))
    {
      DBG("event SYNC_RECEIPT_TIMEOUT_EXPIRES\n");
      ptpClock->number_foreign_records = 0;
      ptpClock->foreign_record_i = 0;
      if(!rtOpts->slaveOnly && ptpClock->clock_stratum != 255)
      {
        m1(ptpClock);
        toState(PTP_MASTER, rtOpts, ptpClock);
      }
      else if(ptpClock->port_state != PTP_LISTENING)
        toState(PTP_LISTENING, rtOpts, ptpClock);
    }
    
    break;
    
  case PTP_MASTER:
    if(timerExpired(SYNC_INTERVAL_TIMER, ptpClock->itimer))
    {
      DBGV("event SYNC_INTERVAL_TIMEOUT_EXPIRES\n");
      issueSync(rtOpts, ptpClock);
    }
    
    handle(rtOpts, ptpClock);
    
    break;
    
  case PTP_DISABLED:
    handle(rtOpts, ptpClock);
    break;
    
  default:
    DBG("do unrecognized state\n");
    break;
  }

  Sleep(5);
}

/* perform actions required when leaving 'port_state' and entering 'state' */
void toState(UInteger8 state, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  ptpClock->message_activity = TRUE;
  
  /* leaving state tasks */
  switch(ptpClock->port_state)
  {
  case PTP_MASTER:
    timerStop(SYNC_INTERVAL_TIMER, ptpClock->itimer);
    timerStart(SYNC_RECEIPT_TIMER, PTP_SYNC_RECEIPT_TIMEOUT(ptpClock->sync_interval), ptpClock->itimer);
    break;
    
  case PTP_SLAVE:
    initClock(rtOpts, ptpClock);
    break;
    
  default:
    break;
  }
  
  /* entering state tasks */
  switch(state)
  {
  case PTP_INITIALIZING:
    DBG("state PTP_INITIALIZING\n");
    timerStop(SYNC_RECEIPT_TIMER, ptpClock->itimer);
    
    ptpClock->port_state = PTP_INITIALIZING;
    break;
    
  case PTP_FAULTY:
    DBG("state PTP_FAULTY\n");
    timerStop(SYNC_RECEIPT_TIMER, ptpClock->itimer);
    
    ptpClock->port_state = PTP_FAULTY;
    break;
    
  case PTP_DISABLED:
    DBG("state change to PTP_DISABLED\n");
    timerStop(SYNC_RECEIPT_TIMER, ptpClock->itimer);
    
    ptpClock->port_state = PTP_DISABLED;
    break;
    
  case PTP_LISTENING:
    DBG("state PTP_LISTENING\n");
    
    timerStart(SYNC_RECEIPT_TIMER, PTP_SYNC_RECEIPT_TIMEOUT(ptpClock->sync_interval), ptpClock->itimer);
    
    ptpClock->port_state = PTP_LISTENING;
    break;
    
  case PTP_MASTER:
    DBG("state PTP_MASTER\n");
    
    if(ptpClock->port_state != PTP_PRE_MASTER)
      timerStart(SYNC_INTERVAL_TIMER, PTP_SYNC_INTERVAL_TIMEOUT(ptpClock->sync_interval), ptpClock->itimer);
    
    timerStop(SYNC_RECEIPT_TIMER, ptpClock->itimer);
    
    ptpClock->port_state = PTP_MASTER;
    break;
    
  case PTP_PASSIVE:
    DBG("state PTP_PASSIVE\n");
    ptpClock->port_state = PTP_PASSIVE;
    break;
    
  case PTP_UNCALIBRATED:
    DBG("state PTP_UNCALIBRATED\n");
    ptpClock->port_state = PTP_UNCALIBRATED;
    break;
    
  case PTP_SLAVE:
    DBG("state PTP_PTP_SLAVE\n");
    
    initClock(rtOpts, ptpClock);
    
    /* R is chosen to allow a few syncs before we first get a one-way delay estimate */
    /* this is to allow the offset filter to fill for an accurate initial clock reset */
    ptpClock->Q = 0;
//    ptpClock->R = getRand(&ptpClock->random_seed)%4 + 4;
    ptpClock->R = 3;
    DBG("Q = %d, R = %d\n", ptpClock->Q, ptpClock->R);
    
    ptpClock->waitingForFollow = FALSE;
    ptpClock->delay_req_send_time.seconds = ptpClock->delay_req_receive_time.seconds = 0;
    ptpClock->delay_req_send_time.nanoseconds = ptpClock->delay_req_receive_time.nanoseconds = 0;
    
    timerStart(SYNC_RECEIPT_TIMER, PTP_SYNC_RECEIPT_TIMEOUT(ptpClock->sync_interval), ptpClock->itimer);
    
    ptpClock->port_state = PTP_SLAVE;
    break;
    
  default:
    DBG("to unrecognized state\n");
    break;
  }
  
  if(rtOpts->displayStats)
    displayStats(rtOpts, ptpClock);
}

/* check and handle received messages */
void handle(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  PEPL_PORT_HANDLE pHdl;
  Boolean isFromSelf;
  TimeInternal wait, time = { 0, 0 };
  int ccode;
  
  wait.seconds = PTP_SYNC_INTERVAL_TIMEOUT(ptpClock->sync_interval);
  wait.nanoseconds = 0;
  if(!ptpClock->message_activity)
    netSelect(&wait, &ptpClock->netPath);
  
  ccode = netRecvEvent(0, ptpClock->msgIbuf, &time, &ptpClock->netPath);
  if ( ccode == 0)
    return;
    
  if ( ccode == 3)
  {
    // Adj for inbound latency on our received event packet timestamps
    subTime(&time, &time, &rtOpts->inboundLatency);
  }
  
  ptpClock->message_activity = TRUE;
  
  if(!msgPeek(ptpClock->msgIbuf))
    return;
  
  msgUnpackHeader(ptpClock->msgIbuf, &ptpClock->msgTmpHeader);
  
  DBGV("event Receipt of Message\n   type %d\n"
    "   uuid %02hhx:%02hhx:%02hhx:%02hhx:%02hhx:%02hhx\n"
    "   sequence %d\n   time %us %dns\n",
    ptpClock->msgTmpHeader.control,
    ptpClock->msgTmpHeader.sourceUuid[0], ptpClock->msgTmpHeader.sourceUuid[1], ptpClock->msgTmpHeader.sourceUuid[2],
    ptpClock->msgTmpHeader.sourceUuid[3], ptpClock->msgTmpHeader.sourceUuid[4], ptpClock->msgTmpHeader.sourceUuid[5],
    ptpClock->msgTmpHeader.sequenceId,
    time.seconds, time.nanoseconds);
  
  isFromSelf = ptpClock->msgTmpHeader.sourceCommunicationTechnology == ptpClock->port_communication_technology
                && ptpClock->msgTmpHeader.sourcePortId == ptpClock->port_id_field
                && !memcmp(ptpClock->msgTmpHeader.sourceUuid, ptpClock->port_uuid_field, PTP_UUID_LENGTH);

  switch(ptpClock->msgTmpHeader.control)
  {
  case PTP_SYNC_MESSAGE:
      DBG( "PTP_SYNC_MESSAGE %s\n", (isFromSelf ? "(self)" : "(ext)") );
    handleSync(&ptpClock->msgTmpHeader, ptpClock->msgIbuf, &time, isFromSelf, rtOpts, ptpClock);
    break;
    
  case PTP_FOLLOWUP_MESSAGE:
    DBG( "PTP_FOLLOWUP_MESSAGE %s\n", (isFromSelf ? "(self)" : "(ext)") );
    handleFollowUp(&ptpClock->msgTmpHeader, ptpClock->msgIbuf, isFromSelf, rtOpts, ptpClock);
    break;
    
  case PTP_DELAY_REQ_MESSAGE:
    DBG( "PTP_DELAY_REQ_MESSAGE %s\n", (isFromSelf ? "(self)" : "(ext)") );
    handleDelayReq(&ptpClock->msgTmpHeader, &time, isFromSelf, rtOpts, ptpClock);
    break;
    
  case PTP_DELAY_RESP_MESSAGE:
    DBG( "PTP_DELAY_RESP_MESSAGE %s\n", (isFromSelf ? "(self)" : "(ext)") );
    handleDelayResp(&ptpClock->msgTmpHeader, ptpClock->msgIbuf, isFromSelf, rtOpts, ptpClock);
    break;
    
  case PTP_MANAGEMENT_MESSAGE:
    DBG( "PTP_MANAGEMENT_MESSAGE %s\n", (isFromSelf ? "(self)" : "(ext)") );
    handleManagement(&ptpClock->msgTmpHeader, ptpClock->msgIbuf, isFromSelf, rtOpts, ptpClock);
    break;
    
   default:
    DBG("handleMessage: unrecognized message %s\n", (isFromSelf ? "(self)" : "(ext)") );
    break;
  }

#if 1
  // Check for PSF and forward if available
  pHdl = rtOpts->eplPortHandle;
  if( pHdl->psfList ) {
      PTPUpdateStatus( STS_PSF_DATA, rtOpts, ptpClock );
  }
#endif
}

void handleSync(MsgHeader *header, Octet *msgIbuf, TimeInternal *time, Boolean isFromSelf, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  MsgSync *sync;
  TimeInternal originTimestamp;
  
  switch(ptpClock->port_state)
  {
  case PTP_FAULTY:
  case PTP_INITIALIZING:
  case PTP_DISABLED:
    DBGV("handleSync: disreguard\n");
    return;
    
  case PTP_UNCALIBRATED:
  case PTP_SLAVE:
    if(isFromSelf)
    {
      DBG("handleSync: ignore from self\n");
      return;
    }
    
    if(getFlag(header->flags, PTP_SYNC_BURST) && !ptpClock->burst_enabled)
      return;
    
    DBGV("handleSync: looking for uuid %02hhx:%02hhx:%02hhx:%02hhx:%02hhx:%02hhx\n",
      ptpClock->parent_uuid[0], ptpClock->parent_uuid[1], ptpClock->parent_uuid[2],
      ptpClock->parent_uuid[3], ptpClock->parent_uuid[4], ptpClock->parent_uuid[5]);
    
    if( header->sequenceId > ptpClock->parent_last_sync_sequence_number
      && header->sourceCommunicationTechnology == ptpClock->parent_communication_technology
      && header->sourcePortId == ptpClock->parent_port_id
      && !memcmp(header->sourceUuid, ptpClock->parent_uuid, PTP_UUID_LENGTH) )
    {
      /* addForeign() takes care of msgUnpackSync() */
      ptpClock->record_update = TRUE;
      sync = addForeign(ptpClock->msgIbuf, &ptpClock->msgTmpHeader, ptpClock);
      
      if(sync->syncInterval != ptpClock->sync_interval)
      {
        DBGV("message's sync interval is %d, but clock's is %d\n", sync->syncInterval, ptpClock->sync_interval);
        /* spec recommends handling a sync interval discrepancy as a fault */
      }

      ptpClock->sync_receive_time.seconds = time->seconds;
      ptpClock->sync_receive_time.nanoseconds = time->nanoseconds;
      if(!getFlag(header->flags, PTP_ASSIST))
      {
        ptpClock->waitingForFollow = FALSE;
        
        toInternalTime(&originTimestamp, &sync->originTimestamp, &ptpClock->halfEpoch);
        
        addTime( &originTimestamp, &originTimestamp, &rtOpts->syncAdjustValue);
        
        DBG( "Sync rxed, 1-step timestamp %ds %dns\n", originTimestamp.seconds, originTimestamp.nanoseconds);
        if ( updateOffset(&originTimestamp, &ptpClock->sync_receive_time,
                          &ptpClock->ofm_filt, rtOpts, ptpClock))
            updateClock(rtOpts, ptpClock);
      }
      else
      {
        ptpClock->waitingForFollow = TRUE;
      }
      
      s1(header, sync, ptpClock);
      
      if(!(--ptpClock->R))
      {
        issueDelayReq(rtOpts, ptpClock);
        
        ptpClock->Q = 0;
//        ptpClock->R = getRand(&ptpClock->random_seed)%(PTP_DELAY_REQ_INTERVAL - 2) + 2;
        ptpClock->R = 3;
        DBG("Q = %d, R = %d\n", ptpClock->Q, ptpClock->R);
      }
      
      DBGV("SYNC_RECEIPT_TIMER reset\n");
      timerStart(SYNC_RECEIPT_TIMER, PTP_SYNC_RECEIPT_TIMEOUT(ptpClock->sync_interval), ptpClock->itimer);
    }
    
  case PTP_MASTER:
  default:
    if( header->sourceCommunicationTechnology == ptpClock->clock_communication_technology
      || header->sourceCommunicationTechnology == PTP_DEFAULT
      || ptpClock->clock_communication_technology == PTP_DEFAULT )
    {
      if(!isFromSelf)
      {
        ptpClock->record_update = TRUE;
        addForeign(ptpClock->msgIbuf, &ptpClock->msgTmpHeader, ptpClock);
      }
      else if(ptpClock->port_state == PTP_MASTER && ptpClock->clock_followup_capable)
      {
        addTime(time, time, &rtOpts->outboundLatency);
        issueFollowup(time, rtOpts, ptpClock);
      }
    }
    break;
  }
}

void handleFollowUp(MsgHeader *header, Octet *msgIbuf, Boolean isFromSelf, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  MsgFollowUp *follow;
  TimeInternal preciseOriginTimestamp;
  
  switch(ptpClock->port_state)
  {
  case PTP_SLAVE:
    if(isFromSelf)
    {
      DBG("handleFollowUp: ignore from self\n");
      return;
    }
    
    if(getFlag(header->flags, PTP_SYNC_BURST) && !ptpClock->burst_enabled)
      return;
    
    DBGV("handleFollowUp: looking for uuid %02hhx:%02hhx:%02hhx:%02hhx:%02hhx:%02hhx\n",
      ptpClock->parent_uuid[0], ptpClock->parent_uuid[1], ptpClock->parent_uuid[2],
      ptpClock->parent_uuid[3], ptpClock->parent_uuid[4], ptpClock->parent_uuid[5]);
    
    follow = &ptpClock->msgTmp.follow;
    msgUnpackFollowUp(ptpClock->msgIbuf, follow);
    
    if( ptpClock->waitingForFollow
      && follow->associatedSequenceId == ptpClock->parent_last_sync_sequence_number
      && header->sourceCommunicationTechnology == ptpClock->parent_communication_technology
      && header->sourcePortId == ptpClock->parent_port_id
      && !memcmp(header->sourceUuid, ptpClock->parent_uuid, PTP_UUID_LENGTH) )
    {
      ptpClock->waitingForFollow = FALSE;
      toInternalTime(&preciseOriginTimestamp, &follow->preciseOriginTimestamp, &ptpClock->halfEpoch);
      
      addTime( &preciseOriginTimestamp, &preciseOriginTimestamp, &rtOpts->syncAdjustValue);
      
      DBG( "sync_receive_time %d s %d ns\n", ptpClock->sync_receive_time.seconds, ptpClock->sync_receive_time.nanoseconds);
      DBG( "preciseOriginTimestamp %d s %d ns\n", preciseOriginTimestamp.seconds, preciseOriginTimestamp.nanoseconds);
      if ( updateOffset(&preciseOriginTimestamp, &ptpClock->sync_receive_time,
                        &ptpClock->ofm_filt, rtOpts, ptpClock))
      {
          updateClock(rtOpts, ptpClock);
      }
    }
    else
    {
      DBG("handleFollowUp: unwanted\n");
    }
    break;
    
  default:
    DBGV("handleFollowUp: disreguard\n");
    return;
  }
}

void handleDelayReq(MsgHeader *header, TimeInternal *time, Boolean isFromSelf, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  switch(ptpClock->port_state)
  {
  case PTP_MASTER:
    if(isFromSelf)
    {
      DBG("handleDelayReq: ignore from self\n");
      return;
    }
    
    if( header->sourceCommunicationTechnology == ptpClock->clock_communication_technology
      || header->sourceCommunicationTechnology == PTP_DEFAULT
      || ptpClock->clock_communication_technology == PTP_DEFAULT )
    {
      issueDelayResp(time, &ptpClock->msgTmpHeader, rtOpts, ptpClock);
    }
    
    break;
    
  case PTP_SLAVE:
    if(isFromSelf)
    {
	  DBG("handleDelayReq: self  %d %d\n", time->seconds, time->nanoseconds);

	  //if (time->seconds > 0 || time->nanoseconds > 0)
	  //{
	  //	DBG("handleDelayReq: time not set!\n");
	  //}
      ptpClock->delay_req_send_time.seconds = time->seconds;
      ptpClock->delay_req_send_time.nanoseconds = time->nanoseconds;
      
      addTime(&ptpClock->delay_req_send_time, &ptpClock->delay_req_send_time, &rtOpts->outboundLatency);
      
      if(ptpClock->delay_req_receive_time.seconds)
      {
        DBG( "updateDelay 1\n");
        updateDelay(&ptpClock->delay_req_send_time, &ptpClock->delay_req_receive_time,
          &ptpClock->owd_filt, rtOpts, ptpClock);
        DBG( "updateDelay 2\n");
        
        ptpClock->delay_req_receive_time.seconds = ptpClock->delay_req_receive_time.seconds = 0;
        ptpClock->delay_req_receive_time.nanoseconds = ptpClock->delay_req_receive_time.nanoseconds = 0;
      }
    }
    break;
    
  default:
    DBGV("handleDelayReq: disreguard\n");
    return;
  }
}

void handleDelayResp(MsgHeader *header, Octet *msgIbuf, Boolean isFromSelf, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  MsgDelayResp *resp;
  
  switch(ptpClock->port_state)
  {
  case PTP_SLAVE:
    if(isFromSelf)
    {
      DBG("handleDelayResp: ignore from self\n");
      return;
    }
    
    resp = &ptpClock->msgTmp.resp;
    msgUnpackDelayResp(ptpClock->msgIbuf, resp);
    
    if( ptpClock->sentDelayReq
      && resp->requestingSourceSequenceId == ptpClock->sentDelayReqSequenceId
      && resp->requestingSourceCommunicationTechnology == ptpClock->port_communication_technology
      && resp->requestingSourcePortId == ptpClock->port_id_field
      && !memcmp(resp->requestingSourceUuid, ptpClock->port_uuid_field, PTP_UUID_LENGTH)
      && header->sourceCommunicationTechnology == ptpClock->parent_communication_technology
      && header->sourcePortId == ptpClock->parent_port_id
      && !memcmp(header->sourceUuid, ptpClock->parent_uuid, PTP_UUID_LENGTH) )
    {
      ptpClock->sentDelayReq = FALSE;
      toInternalTime(&ptpClock->delay_req_receive_time, &resp->delayReceiptTimestamp, &ptpClock->halfEpoch);
      
      addTime( &ptpClock->delay_req_receive_time, &ptpClock->delay_req_receive_time, &rtOpts->delayReqAdjustValue);
      
      if(ptpClock->delay_req_send_time.seconds)
      {
        DBG( "updateDelay 3\n");
        updateDelay(&ptpClock->delay_req_send_time, &ptpClock->delay_req_receive_time,
          &ptpClock->owd_filt, rtOpts, ptpClock);
        DBG( "updateDelay 4\n");
        
        ptpClock->delay_req_receive_time.seconds = 0;
        ptpClock->delay_req_receive_time.nanoseconds = 0;
      }
    }
    else
    {
      DBGV("handleDelayResp: unwanted\n");
    }
    break;
    
  default:
    DBGV("handleDelayResp: disreguard\n");
    return;
  }
}

void handleManagement(MsgHeader *header, Octet *msgIbuf, Boolean isFromSelf, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  MsgManagement *manage;
  
  UInteger8 state;
  
  if(ptpClock->port_state == PTP_INITIALIZING)
    return;
  
  manage = &ptpClock->msgTmp.manage;
  msgUnpackManagement(ptpClock->msgIbuf, manage);
  
  if( (manage->targetCommunicationTechnology == ptpClock->clock_communication_technology
    && !memcmp(manage->targetUuid, ptpClock->clock_uuid_field, PTP_UUID_LENGTH))
    || ((manage->targetCommunicationTechnology == PTP_DEFAULT
    || manage->targetCommunicationTechnology == ptpClock->clock_communication_technology)
    && !sum(manage->targetUuid, PTP_UUID_LENGTH)) )
  {
    switch(manage->managementMessageKey)
    {
    case PTP_MM_OBTAIN_IDENTITY:
    case PTP_MM_GET_DEFAULT_DATA_SET:
    case PTP_MM_GET_CURRENT_DATA_SET:
    case PTP_MM_GET_PARENT_DATA_SET:
    case PTP_MM_GET_PORT_DATA_SET:
    case PTP_MM_GET_GLOBAL_TIME_DATA_SET:
    case PTP_MM_GET_FOREIGN_DATA_SET:
      issueManagement(header, manage, rtOpts, ptpClock);
      break;
      
    default:
      ptpClock->record_update = TRUE;
      state = msgUnloadManagement(ptpClock->msgIbuf, manage, ptpClock, rtOpts);
      if(state != ptpClock->port_state)
        toState(state, rtOpts, ptpClock);
      break;
    }
  }
}

/* pack and send various messages */
void issueSync(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
//  TimeInternal internalTime;
  TimeRepresentation originTimestamp;
  
  ++ptpClock->last_sync_event_sequence_number;
  ptpClock->grandmaster_sequence_number = ptpClock->last_sync_event_sequence_number;

  originTimestamp.seconds = originTimestamp.nanoseconds = 0;  // Let PHY timestamp  
  //getTime( rtOpts, &internalTime);
  //fromInternalTime(&internalTime, &originTimestamp, ptpClock->halfEpoch);
  msgPackSync(ptpClock->msgObuf, FALSE, &originTimestamp, ptpClock);
  
  if(!netSendEvent(0, ptpClock->msgObuf, SYNC_PACKET_LENGTH, &ptpClock->netPath))
    toState(PTP_FAULTY, rtOpts, ptpClock);
  else
    DBGV("sent sync message\n");
}

void issueFollowup(TimeInternal *time, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  TimeRepresentation preciseOriginTimestamp;
  
  ++ptpClock->last_general_event_sequence_number;
  
  fromInternalTime(time, &preciseOriginTimestamp, ptpClock->halfEpoch);
  msgPackFollowUp(ptpClock->msgObuf, ptpClock->last_sync_event_sequence_number, &preciseOriginTimestamp, ptpClock);
  
  if(!netSendGeneral(0, ptpClock->msgObuf, FOLLOW_UP_PACKET_LENGTH, &ptpClock->netPath))
    toState(PTP_FAULTY, rtOpts, ptpClock);
  else
    DBGV("sent followup message\n");
}

void issueDelayReq(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  TimeInternal internalTime;
  TimeRepresentation originTimestamp;
  
  ptpClock->sentDelayReq = TRUE;
  ptpClock->sentDelayReqSequenceId = ++ptpClock->last_sync_event_sequence_number;
  
  getTime( rtOpts, &internalTime);
  fromInternalTime(&internalTime, &originTimestamp, ptpClock->halfEpoch);
  msgPackDelayReq(ptpClock->msgObuf, FALSE, &originTimestamp, ptpClock);
  
  if(!netSendEvent(0, ptpClock->msgObuf, DELAY_REQ_PACKET_LENGTH, &ptpClock->netPath))
    toState(PTP_FAULTY, rtOpts, ptpClock);
  else
    DBGV("sent delay request message\n");
}

void issueDelayResp(TimeInternal *time, MsgHeader *header, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  TimeRepresentation delayReceiptTimestamp;
  
  ++ptpClock->last_general_event_sequence_number;
  
  fromInternalTime(time, &delayReceiptTimestamp, ptpClock->halfEpoch);
  msgPackDelayResp(ptpClock->msgObuf, header, &delayReceiptTimestamp, ptpClock);
  
  if(!netSendGeneral(0, ptpClock->msgObuf, DELAY_RESP_PACKET_LENGTH, &ptpClock->netPath))
    toState(PTP_FAULTY, rtOpts, ptpClock);
  else
    DBGV("sent delay response message\n");
}

void issueManagement(MsgHeader *header, MsgManagement *manage, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
  UInteger16 length;
  
  ++ptpClock->last_general_event_sequence_number;
  
  if(!(length = msgPackManagementResponse(ptpClock->msgObuf, header, manage, ptpClock)))
    return;
  
  if(!netSendGeneral(0, ptpClock->msgObuf, length, &ptpClock->netPath))
    toState(PTP_FAULTY, rtOpts, ptpClock);
  else
    DBGV("sent management message\n");
}

/* add or update an entry in the foreign master data set */
MsgSync * addForeign(Octet *buf, MsgHeader *header, PtpClock *ptpClock)
{
  Integer16 i, j;
  Boolean found = FALSE;
  
  DBGV("updateForeign\n");
  
  j = ptpClock->foreign_record_best;
  for(i = 0; i < ptpClock->number_foreign_records; ++i)
  {
    if(header->sourceCommunicationTechnology == ptpClock->foreign[j].foreign_master_communication_technology
      && header->sourcePortId == ptpClock->foreign[j].foreign_master_port_id
      && !memcmp(header->sourceUuid, ptpClock->foreign[j].foreign_master_uuid, PTP_UUID_LENGTH))
    {
      ++ptpClock->foreign[j].foreign_master_syncs;
      found = TRUE;
      DBGV("updateForeign: update record %d\n", j);
      break;
    }
    
    j = (j + 1)%ptpClock->number_foreign_records;
  }
  
  if(!found)
  {
    if(ptpClock->number_foreign_records < ptpClock->max_foreign_records)
      ++ptpClock->number_foreign_records;
    
    j = ptpClock->foreign_record_i;
    
    ptpClock->foreign[j].foreign_master_communication_technology =
      header->sourceCommunicationTechnology;
    ptpClock->foreign[j].foreign_master_port_id =
      header->sourcePortId;
    memcpy(ptpClock->foreign[j].foreign_master_uuid,
      header->sourceUuid, PTP_UUID_LENGTH);
    
    DBG("updateForeign: new record (%d,%d) %d %d %02hhx:%02hhx:%02hhx:%02hhx:%02hhx:%02hhx\n",
      ptpClock->foreign_record_i, ptpClock->number_foreign_records,
      ptpClock->foreign[j].foreign_master_communication_technology,
      ptpClock->foreign[j].foreign_master_port_id,
      ptpClock->foreign[j].foreign_master_uuid[0], ptpClock->foreign[j].foreign_master_uuid[1],
      ptpClock->foreign[j].foreign_master_uuid[2], ptpClock->foreign[j].foreign_master_uuid[3],
      ptpClock->foreign[j].foreign_master_uuid[4], ptpClock->foreign[j].foreign_master_uuid[5]);
    
    ptpClock->foreign_record_i = (ptpClock->foreign_record_i + 1)%ptpClock->max_foreign_records;
  }
  
  msgUnpackHeader(buf, &ptpClock->foreign[j].header);
  msgUnpackSync(buf, &ptpClock->foreign[j].sync);
  
  return &ptpClock->foreign[j].sync;
}
