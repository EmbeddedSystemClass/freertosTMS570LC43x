/* ptpd.h */
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


#ifndef PTPD_H
#define PTPD_H

#include "epl.h"

#include "constants.h"
#include "datatypes.h"
#include "dep/constants_dep.h"
#include "dep/datatypes_dep.h"
#include "dep/ptpd_dep.h"

#define PTPV2_FLAG_OFFSET							6
#define PTPV2_FLAG_LENGTH							2
#define PTPV2_SRC_PORT_ID_OFFSET				28
#define PTPV2_SEQUENCE_ID_OFFSET				30
#define PTPV2_CONTROL_OFFSET					32
#define PTPV2_ORIGIN_TS_SEC_OFFSET			36
#define PTPV2_ORIGIN_TS_NSEC_OFFSET 		40
#define PTPV2_CLOCK_ID_OFFSET 					20
#define PTPV2_CLOCK_ID_LENGTH					8
#define PTPV2_MESSAGE_TYPE_OFFSET			0
#define PTPV2_VERSION_OFFSET						1
#define PTPV2_SUBDOMAIN_OFFSET				4
#define PTPV2_SUBDOMAIN_LENGTH				1
#define PTPV2_MESSAGE_LENGTH_OFFSET		3

#define PTPV2_SYNC_TYPE								0
#define PTPV2_SYNC_CONTROL						0
#define PTPV2_SYNC_LENGTH							0x2C

#define PTPV2_DELAY_REQUEST_TYPE			1
#define PTPV2_DELAY_REQUEST_LENGTH		0x2C
#define PTPV2_DELAY_REQUEST_CONTROL		1

#define PTPV2_DELAY_RESPONSE_TYPE			9
#define PTPV2_DELAY_RESPONSE_CONTROL	3
#define PTPV2_DELAY_RESPONSE_LENGTH		0x36

#define PTPV2_FOLLOWUP_TYPE						8
#define PTPV2_FOLLOWUP_CONTROL				2
#define PTPV2_FOLLOWUP_LENGTH				0x2C


void init1588(PEPL_PORT_HANDLE epl_port_handle);
int runPtpd(void);

#define malloc(x)	pvPortMalloc(x)
void *pvPortCalloc(int value, size_t size);
#define calloc(x, y)		pvPortCalloc(x, y)

#define EXPORT

#define STS_PSF_DATA    1
#define STS_OFFSET_DATA 2

typedef struct STS_OFFSET_DATA_STRUCT {
    TimeInternal offset_from_master;
    TimeInternal master_to_slave_delay;
    TimeInternal slave_to_master_delay;
    TimeInternal oneWayAvg;
} STS_OFFSET_DATA_STRUCT;

#ifdef __cplusplus
extern "C" {
#endif

EXPORT void PTPThread(
    IN PEPL_PORT_HANDLE portHandle,
//    IN PyObject *guiObj,
//    IN PyObject *stdioCallback,
//    IN PyObject *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg);

EXPORT void PTPThreadC(
    IN PEPL_PORT_HANDLE portHandle,
    IN void *guiObj,
    IN void *stdioCallback,
    IN void *statusUpdateCallback,
    IN RunTimeOpts *ptpStackCfg);

EXPORT void PTPKillThread(
    IN PEPL_PORT_HANDLE portHandle);

void PTPPrintf(
    NS_UINT type,
    NS_UINT8 *baseStr,
    ...);

#ifdef __cplusplus
}
#endif


/* arith.c */
UInteger32 crc_algorithm(Octet*,Integer16);
UInteger32 sum(Octet*,Integer16);
void fromInternalTime(TimeInternal*,TimeRepresentation*,Boolean);
void toInternalTime(TimeInternal*,TimeRepresentation*,Boolean*);
void normalizeTime(TimeInternal*);
void addTime(TimeInternal*,TimeInternal*,TimeInternal*);
void subTime(TimeInternal*,TimeInternal*,TimeInternal*);

/* bmc.c */
UInteger8 bmc(ForeignMasterRecord*,RunTimeOpts*,PtpClock*);
void m1(PtpClock*);
void s1(MsgHeader*,MsgSync*,PtpClock*);
void initData(RunTimeOpts*,PtpClock*);

/* probe.c */
void probe(RunTimeOpts*,PtpClock*);

/* protocol.c */
void protocol(RunTimeOpts*,PtpClock*);


#endif

