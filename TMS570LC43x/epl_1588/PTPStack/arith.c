/* arith.c */
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

 
#include "ptpd.h"

/* from annex C of the spec */
UInteger32 crc_algorithm(Octet *buf, Integer16 length)
{
  Integer16 i;
  UInteger8 data;
  UInteger32 polynomial = 0xedb88320, crc = 0xffffffff;
  
  while(length-- > 0)
  {
    data = *(UInteger8 *)(buf++);
    
    for(i=0; i<8; i++)
    {
      if((crc^data)&1)
      {
        crc = (crc>>1);
        crc ^= polynomial;
      }
      else
      {
        crc = (crc>>1);
      }
      data >>= 1;
    }
  }
  
  return crc^0xffffffff;
}

UInteger32 sum(Octet *buf, Integer16 length)
{
  UInteger32 sum = 0;
  
  while(length-- > 0)
    sum += *(UInteger8 *)(buf++);
  
  return sum;
}

void fromInternalTime(TimeInternal *internal, TimeRepresentation *external, Boolean halfEpoch)
{
  external->seconds = labs(internal->seconds) + halfEpoch * INT_MAX;
  
  if(internal->seconds < 0 || internal->nanoseconds < 0)
  {
    external->nanoseconds = labs(internal->nanoseconds) | ~INT_MAX;
  }
  else
  {
    external->nanoseconds = labs(internal->nanoseconds);
  }
  
  DBGV("fromInternalTime: %10ds %11dns -> %10us %11dns\n",
    internal->seconds, internal->nanoseconds,
    external->seconds, external->nanoseconds);
}

void toInternalTime(TimeInternal *internal, TimeRepresentation *external, Boolean *halfEpoch)
{
  *halfEpoch = external->seconds / INT_MAX;
  
  if(external->nanoseconds & ~INT_MAX)
  {
    internal->seconds = -1 * (external->seconds % INT_MAX);
    internal->nanoseconds = -(external->nanoseconds & INT_MAX);
  }
  else
  {
    internal->seconds = external->seconds % INT_MAX;
    internal->nanoseconds = external->nanoseconds;
  }
  
  DBGV("toInternalTime: %10ds %11dns <- %10us %11dns\n",
    internal->seconds, internal->nanoseconds,
    external->seconds, external->nanoseconds);
}

void normalizeTime(TimeInternal *r)
{
  r->seconds += r->nanoseconds/1000000000;
  r->nanoseconds -= r->nanoseconds/1000000000*1000000000;
  
  if(r->seconds > 0 && r->nanoseconds < 0)
  {
    r->seconds -= 1;
    r->nanoseconds += 1000000000;
  }
  else if(r->seconds < 0 && r->nanoseconds > 0)
  {
    r->seconds += 1;
    r->nanoseconds -= 1000000000;
  }
}

void addTime(TimeInternal *r, TimeInternal *x, TimeInternal *y)
{
  r->seconds = x->seconds + y->seconds;
  r->nanoseconds = x->nanoseconds + y->nanoseconds;
  
  normalizeTime(r);
}

void subTime(TimeInternal *r, TimeInternal *x, TimeInternal *y)
{
  r->seconds = x->seconds - y->seconds;
  r->nanoseconds = x->nanoseconds - y->nanoseconds;
  
  normalizeTime(r);
}
