/* ptpd.c */
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
#include "NetworkInterface.h"
#include "HL_emac.h"
extern hdkif_t hdkif_data[];

RunTimeOpts rtOpts;  /* statically allocated run-time configuration data */
RX_CFG_ITEMS rxCfgItems;
uint32_t rxCfgOpts;

void *pvPortCalloc(int value, size_t size){
	void *p_to_m = malloc(size);
	memset(p_to_m, value, size);
	return p_to_m;
}

int runPtpd(void)
{
  PtpClock *ptpClock;
  Integer16 ret;

  PEPL_PORT_HANDLE epl_port_handle = malloc(sizeof(struct PORT_OBJ));
  epl_port_handle->psfConfigOptions |= STSOPT_IPV4;
  epl_port_handle->psfConfigOptions |= STSOPT_LITTLE_ENDIAN;
  epl_port_handle->psfConfigOptions |= STSOPT_TXTS_EN;
  epl_port_handle->psfConfigOptions |= STSOPT_RXTS_EN;
  hdkif_t *hdkif;
  hdkif = &hdkif_data[0U];

  EMACInstConfig(hdkif);

  memset(&rxCfgItems, 0, sizeof(RX_CFG_ITEMS));
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

  epl_port_handle->hdkif = *hdkif;
  epl_port_handle->rxCfgItems = rxCfgItems;
  epl_port_handle->rxCfgOpts = rxCfgOpts;

  init1588(epl_port_handle);
  
  rtOpts.eplPortHandle = epl_port_handle;

  /* initialize run-time options to reasonable values */ 
  rtOpts.syncInterval = DEFAULT_SYNC_INTERVAL;
  memcpy(rtOpts.subdomainName, DEFAULT_PTP_DOMAIN_NAME, PTP_SUBDOMAIN_NAME_LENGTH);
  memcpy(rtOpts.clockIdentifier, IDENTIFIER_DFLT, PTP_CODE_STRING_LENGTH);
  rtOpts.clockVariance = DEFAULT_CLOCK_VARIANCE;
  rtOpts.clockStratum = DEFAULT_CLOCK_STRATUM;
  rtOpts.directAddress[0] = 0;
  rtOpts.inboundLatency.nanoseconds = DEFAULT_INBOUND_LATENCY;
  rtOpts.outboundLatency.nanoseconds = DEFAULT_OUTBOUND_LATENCY;
  rtOpts.noResetClock = DEFAULT_NO_RESET_CLOCK;
  rtOpts.s = DEFAULT_DELAY_S;
  rtOpts.ap = DEFAULT_AP;
  rtOpts.ai = DEFAULT_AI;
  rtOpts.max_foreign_records = DEFUALT_MAX_FOREIGN_RECORDS;
  rtOpts.currentUtcOffset = DEFAULT_UTC_OFFSET;
  rtOpts.slaveOnly = true;
  
  int argc = 0;
  char ** argv = {0};
  if( !(ptpClock = ptpdStartup(argc, argv, &ret, &rtOpts)) )
    return ret;
  
  ptpClock->external_timing = false;
  ptpClock->clock_followup_capable = false;
  ptpClock->is_boundary_clock = false;
  ptpClock->burst_enabled = false;
  ptpClock->parent_stats = false;

  if(rtOpts.probe)
  {
//    probe(&rtOpts, ptpClock);
  }
  else
  {
    /* do the protocol engine */
//    protocol(&rtOpts, ptpClock);
  }
  
  ptpdShutdown(ptpClock);
  
  NOTIFY("self shutdown, probably due to an error\n");
  return 1;
}
