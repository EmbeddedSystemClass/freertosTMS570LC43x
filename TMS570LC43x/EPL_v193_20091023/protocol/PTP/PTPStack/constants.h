/* constants.h */
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


#ifndef CONSTANTS_H
#define CONSTANTS_H

// NSC Specific constants
#define POW_2_32                0x100000000L

/* implementation specific constants */
#define MANUFACTURER_ID \
    "National Semiconductor:EPL v1.90\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"

#define DEFAULT_SYNC_INTERVAL        0
#define DEFAULT_UTC_OFFSET           0
#define DEFAULT_CLOCK_VARIANCE       (-4000)
#define DEFAULT_CLOCK_STRATUM        4
#define DEFAULT_INBOUND_LATENCY      215       /* in nsec */
#define DEFAULT_INBOUND_LATENCY_10MB 300       /* in nsec */
#define DEFAULT_OUTBOUND_LATENCY     0         /* in nsec */
#define DEFAULT_OUTBOUND_LATENCY_10MB 95       /* in nsec */
#define DEFAULT_NO_RESET_CLOCK       FALSE
#define DEFAULT_AP                   10
//#define DEFAULT_AI                   1000
#define DEFAULT_AI                   100
#define DEFAULT_DELAY_S              6
#define DEFUALT_MAX_FOREIGN_RECORDS  5

/* features, only change to reflect changes in implementation */
#define CLOCK_FOLLOWUP    TRUE
#define INITIALIZABLE     TRUE
#define BURST_ENABLED     FALSE
#define EXTERNAL_TIMING   FALSE
#define BOUNDARY_CLOCK    FALSE
#define NUMBER_PORTS      1
#define VERSION_PTP       1
#define VERSION_NETWORK   1

/* spec defined constants  */
#define DEFAULT_PTP_DOMAIN_NAME      "_DFLT\0\0\0\0\0\0\0\0\0\0\0"
#define ALTERNATE_PTP_DOMAIN1_NAME   "_ALT1\0\0\0\0\0\0\0\0\0\0\0"
#define ALTERNATE_PTP_DOMAIN2_NAME   "_ALT2\0\0\0\0\0\0\0\0\0\0\0"
#define ALTERNATE_PTP_DOMAIN3_NAME   "_ALT3\0\0\0\0\0\0\0\0\0\0\0"

#define IDENTIFIER_ATOM   "ATOM"
#define IDENTIFIER_GPS    "GPS\0"
#define IDENTIFIER_NTP    "NTP\0"
#define IDENTIFIER_HAND   "HAND"
#define IDENTIFIER_INIT   "INIT"
#define IDENTIFIER_DFLT   "DFLT"

/* ptp constants */
#define PTP_UUID_LENGTH                     6
#define PTP_CODE_STRING_LENGTH              4
#define PTP_SUBDOMAIN_NAME_LENGTH           16
#define PTP_MAX_MANAGEMENT_PAYLOAD_SIZE     90
/* no support for intervals less than one */
//#define PTP_SYNC_INTERVAL_TIMEOUT(x)        (1<<((x)<0?1:(x))) 
#define PTP_SYNC_INTERVAL_TIMEOUT(x)        (x)

//#define PTP_SYNC_RECEIPT_TIMEOUT(x)         (10*(1<<((x)<0?0:(x))))
#define PTP_SYNC_RECEIPT_TIMEOUT(x)         (10*(x))

#define PTP_DELAY_REQ_INTERVAL              30
#define PTP_FOREIGN_MASTER_THRESHOLD        2
#define PTP_FOREIGN_MASTER_TIME_WINDOW(x)   (4*(1<<((x)<0?0:(x))))
#define PTP_RANDOMIZING_SLOTS               18
#define PTP_LOG_VARIANCE_THRESHOLD          256
#define PTP_LOG_VARIANCE_HYSTERESIS         128
/* used in spec but not named */
#define MANUFACTURER_ID_LENGTH              48

/* ptp data enums */
enum {
  PTP_CLOSED=0,  PTP_ETHER,  PTP_FFBUS=4,
  PTP_PROFIBUS,  PTP_LON,  PTP_DNET,
  PTP_SDS,  PTP_CONTROLNET,  PTP_CANOPEN,
  PTP_IEEE1394=243,  PTP_IEEE802_11A,  PTP_IEEE_WIRELESS,
  PTP_INFINIBAND,  PTP_BLUETOOTH,  PTP_IEEE802_15_1,
  PTP_IEEE1451_2,  PTP_IEEE1451_5,  PTP_USB,
  PTP_ISA,  PTP_PCI,  PTP_VXI,  PTP_DEFAULT
};

enum {
  PTP_INITIALIZING=0,  PTP_FAULTY,  PTP_DISABLED,
  PTP_LISTENING,  PTP_PRE_MASTER,  PTP_MASTER,
  PTP_PASSIVE,  PTP_UNCALIBRATED,  PTP_SLAVE
};

enum {
  PTP_SYNC_MESSAGE=0,  PTP_DELAY_REQ_MESSAGE,  PTP_FOLLOWUP_MESSAGE,
  PTP_DELAY_RESP_MESSAGE,  PTP_MANAGEMENT_MESSAGE,
  PTP_SYNC_MESSAGE_BURST, PTP_DELAY_REQ_MESSAGE_BURST
};

enum {
  PTP_LI_61=0, PTP_LI_59, PTP_BOUNDARY_CLOCK,
  PTP_ASSIST, PTP_EXT_SYNC, PARENT_STATS, PTP_SYNC_BURST
};

enum {
  PTP_MM_NULL=0,  PTP_MM_OBTAIN_IDENTITY,  PTP_MM_CLOCK_IDENTITY,
  PTP_MM_INITIALIZE_CLOCK,  PTP_MM_SET_SUBDOMAIN,
  PTP_MM_CLEAR_DESIGNATED_PREFERRED_MASTER,
  PTP_MM_SET_DESIGNATED_PREFERRED_MASTER,
  PTP_MM_GET_DEFAULT_DATA_SET,  PTP_MM_DEFAULT_DATA_SET,
  PTP_MM_UPDATE_DEFAULT_DATA_SET,  PTP_MM_GET_CURRENT_DATA_SET,
  PTP_MM_CURRENT_DATA_SET,  PTP_MM_GET_PARENT_DATA_SET,
  PTP_MM_PARENT_DATA_SET,  PTP_MM_GET_PORT_DATA_SET,
  PTP_MM_PORT_DATA_SET,  PTP_MM_GET_GLOBAL_TIME_DATA_SET,
  PTP_MM_GLOBAL_TIME_DATA_SET,  PTP_MM_UPDATE_GLOBAL_TIME_PROPERTIES,
  PTP_MM_GOTO_FAULTY_STATE,  PTP_MM_GET_FOREIGN_DATA_SET,
  PTP_MM_FOREIGN_DATA_SET,  PTP_MM_SET_SYNC_INTERVAL,
  PTP_MM_DISABLE_PORT,  PTP_MM_ENABLE_PORT,
  PTP_MM_DISABLE_BURST,  PTP_MM_ENABLE_BURST,  PTP_MM_SET_TIME
};

/* enum used by this implementation */
enum {
  SYNC_RECEIPT_TIMER=0, SYNC_INTERVAL_TIMER, QUALIFICATION_TIMER,
  TIMER_ARRAY_SIZE  /* these two are non-spec */
};

#endif

