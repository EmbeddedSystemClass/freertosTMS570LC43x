/* ptpd_dep.h */
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


#ifndef PTPD_DEP_H
#define PTPD_DEP_H

#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<signal.h>
//#include<fcntl.h>
//#include<sys/stat.h>
#include<time.h>

//#ifndef _WIN32
//#include<unistd.h>
//#include<sys/time.h>
//#include<sys/timex.h>
//#include<sys/socket.h>
//#include<sys/select.h>
//#include<sys/ioctl.h>
//#include<arpa/inet.h>
//#endif //WIN32

#include "ptpControl.h"

/* system messages */
#ifdef ERROR
#undef ERROR
#endif


#define ERROR(...) PTPPrintf( 2, "ptpd!: " __VA_ARGS__)
#define PERROR(...) PTPPrintf( 2, "ptpd!: " __VA_ARGS__)
#define NOTIFY(...) PTPPrintf( 2, "ptpd!: " __VA_ARGS__)

/* debug messages */
#ifdef PTPD_DBGV
#define PTPD_DBG
#define DBGV(...) PTPPrintf( 0, "" __VA_ARGS__)
#else
#define DBGV(...)
#endif

#ifdef PTPD_DBG
#define DBG(...) PTPPrintf( 1, "" __VA_ARGS__)
#define DBGFLUSH()
#else
#define DBG(...)
#define DBGFLUSH()
#endif

/* endian corrections */
#if defined(PTPD_MSBF)
#define shift8(x,y)       ( (x) << ((3-y)<<3) )
#define shift16(x,y)      ( (x) << ((1-y)<<4) )
#elif defined(PTPD_LSBF)
#define shift8(x,y)       ( (x) << ((y)<<3) )
#define shift16(x,y)      ( (x) << ((y)<<4) )
#endif

#define flip16(x)         htons(x)
#define flip32(x)         htonl(x)

/* i don't know any target platforms that do not have htons and htonl,
   but here are generic funtions just in case */
/*
#if defined(PTPD_MSBF)
#define flip16(x)         (x)
#define flip32(x)         (x)
#elif defined(PTPD_LSBF)
static inline Integer16 flip16(Integer16 x)
{
   return (((x) >> 8) & 0x00ff) | (((x) << 8) & 0xff00);
}

static inline Integer32 flip32(x)
{
  return (((x) >> 24) & 0x000000ff) | (((x) >> 8 ) & 0x0000ff00) |
         (((x) << 8 ) & 0x00ff0000) | (((x) << 24) & 0xff000000);
}
#endif
*/

/* bit array manipulation */
#define getFlag(x,y)      !!(*(UInteger8*)((x)+((y)<8?1:0)) & ( 1<<((y)<8?(y):(y)-8) ))
#define setFlag(x,y)      (*(UInteger8*)((x)+((y)<8?1:0)) |= 1<<((y)<8?(y):(y)-8) )
#define clearFlag(x,y)    (*(UInteger8*)((x)+((y)<8?1:0)) &= ~(1<<((y)<8?(y):(y)-8)) )


/* msg.c */
Boolean msgPeek(void*);
void msgUnpackHeader(void*,MsgHeader*);
void msgUnpackSync(void*,MsgSync*);
void msgUnpackDelayReq(void*,MsgDelayReq*);
void msgUnpackFollowUp(void*,MsgFollowUp*);
void msgUnpackDelayResp(void*,MsgDelayResp*);
void msgUnpackManagement(void*,MsgManagement*);
UInteger8 msgUnloadManagement(void*,MsgManagement*,PtpClock*,RunTimeOpts*);
void msgUnpackManagementPayload(void *buf, MsgManagement *manage);
void msgPackHeader(void*,PtpClock*);
void msgPackSync(void*,Boolean,TimeRepresentation*,PtpClock*);
void msgPackDelayReq(void*,Boolean,TimeRepresentation*,PtpClock*);
void msgPackFollowUp(void*,UInteger16,TimeRepresentation*,PtpClock*);
void msgPackDelayResp(void*,MsgHeader*,TimeRepresentation*,PtpClock*);
UInteger16 msgPackManagement(void*,MsgManagement*,PtpClock*);
UInteger16 msgPackManagementResponse(void*,MsgHeader*,MsgManagement*,PtpClock*);

/* net.c */
/* linux API dependent */
Boolean netInit(NetPath*,RunTimeOpts*,PtpClock*);
Boolean netShutdown(NetPath*);
Boolean netSelect(TimeInternal*,NetPath*);
Boolean netRecvEvent(Octet*,Octet*,TimeInternal*,NetPath*);
Boolean netRecvGeneral(Octet*,Octet*,NetPath*);
Boolean netSendEvent(Octet*,Octet*,UInteger16,NetPath*);
Boolean netSendGeneral(Octet*,Octet*,UInteger16,NetPath*);

/* servo.c */
void initClock(RunTimeOpts*,PtpClock*);
void updateDelay(TimeInternal*,TimeInternal*,
  one_way_delay_filter*,RunTimeOpts*,PtpClock*);
Boolean updateOffset(TimeInternal*,TimeInternal*,
  offset_from_master_filter*,RunTimeOpts*,PtpClock*);
void updateClock(RunTimeOpts*,PtpClock*);

/* startup.c */
/* unix API dependent */
PtpClock * ptpdStartup(int,char**,Integer16*,RunTimeOpts*);
void ptpdShutdown(PtpClock *ptpClock);

/* sys.c */
/* unix API dependent */
void displayStats(RunTimeOpts*,PtpClock*);
Boolean nanoSleep(TimeInternal*);
void getTime(RunTimeOpts *rtOpts, TimeInternal*);
void setTime(RunTimeOpts *rtOpts, TimeInternal*);
UInteger16 getRand(UInteger32*);
Boolean adjFreq(Integer32);

/* timer.c */
void initTimer(void);
void timerUpdate(IntervalTimer*);
void timerStop(UInteger16,IntervalTimer*);
void timerStart(UInteger16,UInteger16,IntervalTimer*);
Boolean timerExpired(UInteger16,IntervalTimer*);


#endif

