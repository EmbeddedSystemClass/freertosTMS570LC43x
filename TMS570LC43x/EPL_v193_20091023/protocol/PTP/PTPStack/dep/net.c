/* net.c */
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


#include "epl.h"

NS_UINT8 *
    intGetNextPhyMessage (
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT NS_UINT8 *msgLocation,
        IN OUT PHYMSG_MESSAGE_TYPE_ENUM *messageType,
        IN OUT PHYMSG_MESSAGE *phyMessageOut,
        IN NS_BOOL usePSFList);


Boolean lookupSubdomainAddress(Octet *subdomainName, Octet *subdomainAddress)
{
  UInteger32 h;
  
  /* set multicast group address based on subdomainName */
  if (!memcmp(subdomainName, DEFAULT_PTP_DOMAIN_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, DEFAULT_PTP_DOMAIN_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN1_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN1_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN2_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN2_ADDRESS, NET_ADDRESS_LENGTH);
  else if(!memcmp(subdomainName, ALTERNATE_PTP_DOMAIN3_NAME, PTP_SUBDOMAIN_NAME_LENGTH))
    memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN3_ADDRESS, NET_ADDRESS_LENGTH);
  else
  {
    h = crc_algorithm(subdomainName, PTP_SUBDOMAIN_NAME_LENGTH) % 3;
    switch(h)
    {
    case 0:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN1_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    case 1:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN2_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    case 2:
      memcpy(subdomainAddress, ALTERNATE_PTP_DOMAIN3_ADDRESS, NET_ADDRESS_LENGTH);
      break;
    default:
      ERROR("handle out of range for '%s'!\n", subdomainName);
      return FALSE;
    }
  }
  
  return TRUE;
}

UInteger8 lookupCommunicationTechnology(UInteger8 communicationTechnology)
{
#if defined(linux)
  
  switch(communicationTechnology)
  {
  case ARPHRD_ETHER:
  case ARPHRD_EETHER:
  case ARPHRD_IEEE802:
    return PTP_ETHER;
    
  default:
    break;
  }
  
#elif defined(BSD_INTERFACE_FUNCTIONS)
  
#endif

#ifdef _WIN32
    return PTP_ETHER;
#endif // _WIN32
  
  return PTP_DEFAULT;
}

UInteger32 findIface(Octet *ifaceName, UInteger8 *communicationTechnology,
  Octet *uuid, Boolean multicast, NetPath *netPath)
{
#if defined(linux)

  /* depends on linux specific ioctls (see 'netdevice' man page) */
  int i, flags;
  struct ifconf data;
  struct ifreq device[IFCONF_LENGTH];
  
  data.ifc_len = sizeof(device);
  data.ifc_req = device;
  
  memset(data.ifc_buf,0,data.ifc_len);
  
  flags = IFF_UP|IFF_RUNNING|(multicast?IFF_MULTICAST:0);
  
  /* look for an interface if none specified */
  if(ifaceName[0] != '\0')
  {
    i = 0;
    memcpy(device[i].ifr_name, ifaceName, IFACE_NAME_LENGTH);
    
    if(ioctl(netPath->eventSock, SIOCGIFHWADDR, &device[i]) < 0)
      DBGV("failed to get hardware address\n");
    else if((*communicationTechnology = lookupCommunicationTechnology(device[i].ifr_hwaddr.sa_family)) == PTP_DEFAULT)
      DBGV("unsupported communication technology (%d)\n", *communicationTechnology);
    else
      memcpy(uuid, device[i].ifr_hwaddr.sa_data, PTP_UUID_LENGTH);
  }
  else
  {
    /* no iface specified */
    /* get list of network interfaces*/
    if(ioctl(netPath->eventSock, SIOCGIFCONF, &data) < 0)
    {
      PERROR("failed query network interfaces");
      return 0;
    }
    
    if(data.ifc_len >= sizeof(device))
      DBG("device list may exceed allocated space\n");
    
    /* search through interfaces */
    for(i=0; i < data.ifc_len/sizeof(device[0]); ++i)
    {
      DBGV("%d %s %s\n",i,device[i].ifr_name,inet_ntoa(((struct sockaddr_in *)&device[i].ifr_addr)->sin_addr));
      
      if(ioctl(netPath->eventSock, SIOCGIFFLAGS, &device[i]) < 0)
        DBGV("failed to get device flags\n");
      else if((device[i].ifr_flags&flags) != flags)
        DBGV("does not meet requirements (%08x, %08x)\n", device[i].ifr_flags, flags);
      else if(ioctl(netPath->eventSock, SIOCGIFHWADDR, &device[i]) < 0)
        DBGV("failed to get hardware address\n");
      else if((*communicationTechnology = lookupCommunicationTechnology(device[i].ifr_hwaddr.sa_family)) == PTP_DEFAULT)
        DBGV("unsupported communication technology (%d)\n", *communicationTechnology);
      else
      {
        DBGV("found interface (%s)\n", device[i].ifr_name);
        
        memcpy(uuid, device[i].ifr_hwaddr.sa_data, PTP_UUID_LENGTH);
        memcpy(ifaceName, device[i].ifr_name, IFACE_NAME_LENGTH);
        
        break;
      }
    }
  }
  
  if(ifaceName[0] == '\0')
  {
    ERROR("failed to find a usable interface\n");
    return 0;
  }
  
  if(ioctl(netPath->eventSock, SIOCGIFADDR, &device[i]) < 0)
  {
    PERROR("failed to get ip address");
    return 0;
  }
  
  return ((struct sockaddr_in *)&device[i].ifr_addr)->sin_addr.s_addr;

#elif defined(BSD_INTERFACE_FUNCTIONS)

  struct ifaddrs *if_list, *ifv4, *ifh;

  if (getifaddrs(&if_list) < 0)
  {
    PERROR("getifaddrs() failed");
    return FALSE;
  }

  /* find an IPv4, multicast, UP interface, right name(if supplied) */
  for (ifv4 = if_list; ifv4 != NULL; ifv4 = ifv4->ifa_next)
  {
    if ((ifv4->ifa_flags & IFF_UP) == 0)
      continue;
    if ((ifv4->ifa_flags & IFF_RUNNING) == 0)
      continue;
    if ((ifv4->ifa_flags & IFF_LOOPBACK))
      continue;
    if (multicast && (ifv4->ifa_flags & IFF_MULTICAST) == 0)
      continue;
    if (ifv4->ifa_addr->sa_family != AF_INET)  /* must have IPv4 address */
      continue;

    if (ifaceName[0] && strncmp(ifv4->ifa_name, ifaceName, IF_NAMESIZE) != 0)
      continue;

    break;
  }

  if (ifv4 == NULL)
  {
    if (ifaceName[0])
    {
      ERROR("interface \"%s\" does not exist, or is not appropriate\n", ifaceName);
      return FALSE;
    }
    ERROR("no suitable interfaces found!");
    return FALSE;
  }

  /* find the AF_LINK info associated with the chosen interface */
  for (ifh = if_list; ifh != NULL; ifh = ifh->ifa_next)
  {
    if (ifh->ifa_addr->sa_family != AF_LINK)
      continue;
    if (strncmp(ifv4->ifa_name, ifh->ifa_name, IF_NAMESIZE) == 0)
      break;
  }

  if (ifh == NULL)
  {
    ERROR("could not get hardware address for interface \"%s\"\n", ifv4->ifa_name);
    return FALSE;
  }

  /* check that the interface TYPE is OK */
  if ( ((struct sockaddr_dl *)ifh->ifa_addr)->sdl_type != IFT_ETHER )
  {
    ERROR("\"%s\" is not an ethernet interface!\n", ifh->ifa_name);
    return FALSE;
  }

  printf("==> %s %s %s\n", ifv4->ifa_name,
       inet_ntoa(((struct sockaddr_in *)ifv4->ifa_addr)->sin_addr),
        ether_ntoa((struct ether_addr *)LLADDR((struct sockaddr_dl *)ifh->ifa_addr))
        );

  *communicationTechnology = PTP_ETHER;
  memcpy(ifaceName, ifh->ifa_name, IFACE_NAME_LENGTH);
  memcpy(uuid, LLADDR((struct sockaddr_dl *)ifh->ifa_addr), PTP_UUID_LENGTH);

  return ((struct sockaddr_in *)ifv4->ifa_addr)->sin_addr.s_addr;
  
#elif defined(_WIN32)
  return FALSE;

#endif
}

/* start all of the UDP stuff */
/* must specify 'subdomainName', optionally 'ifaceName', if not then pass ifaceName == "" */
/* returns other args */
/* on socket options, see the 'socket(7)' and 'ip' man pages */
Boolean netInit(NetPath *netPath, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
#if defined(linux)
  int temp
  struct in_addr interfaceAddr, netAddr;
  struct sockaddr_in addr;
  struct ip_mreq imr;
#endif //linux

  int i;
  char *s;
  
  char addrStr[NET_ADDRESS_LENGTH];
  
  DBG("netInit\n");
  
#if defined(linux)
  /* open sockets */
  if( (netPath->eventSock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP) ) < 0
    || (netPath->generalSock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP) ) < 0 )
  {
    PERROR("failed to initalize sockets");
    return FALSE;
  }

  /* find a network interface */
  if( !(interfaceAddr.s_addr = findIface(rtOpts->ifaceName, &ptpClock->port_communication_technology,
    ptpClock->port_uuid_field, !rtOpts->directAddress, netPath)) )
    return FALSE;
  
  temp = 1;  /* allow address reuse */
  if( setsockopt(netPath->eventSock, SOL_SOCKET, SO_REUSEADDR, &temp, sizeof(int)) < 0
    || setsockopt(netPath->generalSock, SOL_SOCKET, SO_REUSEADDR, &temp, sizeof(int)) < 0 )
  {
    DBG("failed to set socket reuse\n");
  }

  /* bind sockets */
  /* need INADDR_ANY to allow receipt of multicast and unicast messages */
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = htonl(INADDR_ANY);
  addr.sin_port = htons(PTP_EVENT_PORT);
  if(bind(netPath->eventSock, (struct sockaddr*)&addr, sizeof(struct sockaddr_in)) < 0)
  {
    PERROR("failed to bind event socket");
    return FALSE;
  }
  
  addr.sin_port = htons(PTP_GENERAL_PORT);
  if(bind(netPath->generalSock, (struct sockaddr*)&addr, sizeof(struct sockaddr_in)) < 0)
  {
    PERROR("failed to bind general socket");
    return FALSE;
  }
  
  /* set general and port address */
  *(Integer16*)ptpClock->event_port_address = PTP_EVENT_PORT;
  *(Integer16*)ptpClock->general_port_address = PTP_GENERAL_PORT;
  
  netPath->rtOpts = rtOpts;
  netPath->ptpClock = ptpClock;
  
  /* set socket to a unicast address if specified (useful for testing) */
  if(rtOpts->directAddress[0])
  {
    if(!inet_aton(rtOpts->directAddress, &netAddr))
      return FALSE;
    
    netPath->bcastAddr = netAddr.s_addr;
    
    s = rtOpts->directAddress;
    for(i = 0; i < SUBDOMAIN_ADDRESS_LENGTH; ++i)
    {
      ptpClock->subdomain_address[i] = strtol(s, &s, 0);
      
      if(!s)
        break;
      
      ++s;
    }
    
    return TRUE;
  }
  
  /* resolve PTP subdomain */
  if(!lookupSubdomainAddress(rtOpts->subdomainName, addrStr))
    return FALSE;
  
  inet_aton(addrStr, &netAddr);
  netPath->bcastAddr = netAddr.s_addr;
  
  s = addrStr;
  for(i = 0; i < SUBDOMAIN_ADDRESS_LENGTH; ++i)
  {
    ptpClock->subdomain_address[i] = strtol(s, &s, 0);
    
    if(!s)
      break;
    
    ++s;
  }
  
  /* multicast send only on specified interface */
  imr.imr_multiaddr.s_addr = netAddr.s_addr;
  imr.imr_interface.s_addr = interfaceAddr.s_addr;
  if( setsockopt(netPath->eventSock, IPPROTO_IP, IP_MULTICAST_IF, &imr.imr_interface.s_addr, sizeof(struct in_addr)) < 0
    || setsockopt(netPath->generalSock, IPPROTO_IP, IP_MULTICAST_IF, &imr.imr_interface.s_addr, sizeof(struct in_addr)) < 0 )
  {
    PERROR("failed to set multicast send interface");
    return FALSE;
  }
  
  /* join multicast group (for receiving) on specified interface */
  if( setsockopt(netPath->eventSock, IPPROTO_IP, IP_ADD_MEMBERSHIP, &imr, sizeof(struct ip_mreq))  < 0
    || setsockopt(netPath->generalSock, IPPROTO_IP, IP_ADD_MEMBERSHIP, &imr, sizeof(struct ip_mreq)) < 0 )
  {
    PERROR("failed to join multicast group for receiving");
    return FALSE;
  }

  /*set socket time to life to 1 */
  temp = 1;
  setsockopt(netPath->eventSock, IPPROTO_IP, IP_MULTICAST_TTL, &temp, sizeof(int));
  setsockopt(netPath->generalSock, IPPROTO_IP, IP_MULTICAST_TTL, &temp, sizeof(int));
  
  temp = 1;  /* allow loopback */
  setsockopt(netPath->eventSock, IPPROTO_IP, IP_MULTICAST_LOOP, &temp, sizeof(int));
  setsockopt(netPath->generalSock, IPPROTO_IP, IP_MULTICAST_LOOP, &temp, sizeof(int));

  /* make timestamps available through recvmsg() */
  temp = 1;
  if (setsockopt(netPath->eventSock, SOL_SOCKET, SO_TIMESTAMP, &temp, sizeof(int)) == -1
    || setsockopt(netPath->generalSock, SOL_SOCKET, SO_TIMESTAMP, &temp, sizeof(int)) == -1)
  {
    PERROR("accurate timestamps not possible: setsockopt(SO_TIMESTAMP) failed");
    return FALSE;
  }


  return TRUE;
  
#elif defined(_WIN32)
    *(Integer16*)ptpClock->event_port_address = PTP_EVENT_PORT;
    *(Integer16*)ptpClock->general_port_address = PTP_GENERAL_PORT;
    
    ptpClock->port_communication_technology = PTP_ETHER;
    
    memcpy( ptpClock->port_uuid_field, rtOpts->localMACAddress, PTP_UUID_LENGTH);
    
    /* resolve PTP subdomain */
    if(!lookupSubdomainAddress(rtOpts->subdomainName, addrStr))
        return FALSE;
        
    s = addrStr;
    for(i = 0; i < SUBDOMAIN_ADDRESS_LENGTH; ++i)
    {
        ptpClock->subdomain_address[i] = (Octet)strtol(s, &s, 0);
        netPath->bcastAddr = (netPath->bcastAddr << 8) | (ptpClock->subdomain_address[i] & 0xFF);
        if( !s) break;
        ++s;
    }
    
    netPath->eventSock = 0xC000;
    netPath->generalSock = 0xC001;
    netPath->rtOpts = rtOpts;
    netPath->ptpClock = ptpClock;
    rtOpts->haveLoopbackedSend = FALSE;
    return TRUE;
#endif
}

/* shut down the UDP stuff */
Boolean netShutdown(NetPath *netPath)
{
#if defined(linux)
  struct ip_mreq imr;

  imr.imr_multiaddr.s_addr = netPath->bcastAddr;
  imr.imr_interface.s_addr = htonl(INADDR_ANY);

  setsockopt(netPath->eventSock, IPPROTO_IP, IP_DROP_MEMBERSHIP, &imr, sizeof(struct ip_mreq));
  setsockopt(netPath->generalSock, IPPROTO_IP, IP_DROP_MEMBERSHIP, &imr, sizeof(struct ip_mreq));
  
  if(netPath->eventSock > 0)
    close(netPath->eventSock);
  netPath->eventSock = -1;
  
  if(netPath->generalSock > 0)
    close(netPath->generalSock);
  netPath->generalSock = -1;
#endif
    
  return TRUE;
}

Boolean netSelect(TimeInternal *timeout, NetPath *netPath)
{
#if defined(linux)
  int nfds;
  fd_set readfds;
  struct timeval tv;
  
  if(timeout < 0)
    return FALSE;
  
  FD_ZERO(&readfds);
  FD_SET(netPath->eventSock, &readfds);
  FD_SET(netPath->generalSock, &readfds);
  
  tv.tv_sec = timeout->seconds;
  tv.tv_usec = timeout->nanoseconds/1000;
  
  if(netPath->eventSock > netPath->generalSock)
    nfds = netPath->eventSock;
  else
    nfds = netPath->generalSock;
  
  return select(nfds + 1, &readfds, 0, 0, &tv) > 0;
  
#elif defined(_WIN32)
  return FALSE;

#endif
}

int netRecvEvent(Octet *address, Octet *buf, TimeInternal *time, NetPath *netPath)
{
#if defined(linux)
  struct msghdr msg;
  struct iovec vec[1];
  struct sockaddr_in from_addr;
  union {
      struct cmsghdr cm;
      char data[CMSG_SPACE(sizeof(struct timeval))];
  } cmsg_un;
  struct cmsghdr *cmsg;
  struct timeval *tv;
  
  vec[0].iov_base = buf;
  vec[0].iov_len = PACKET_SIZE;
  
  memset(&msg, 0, sizeof(msg));
  memset(&from_addr, 0, sizeof(from_addr));
  memset(buf, 0, PACKET_SIZE);
  memset(&cmsg_un, 0, sizeof(cmsg_un));
  
  msg.msg_name = (caddr_t)&from_addr;
  msg.msg_namelen = sizeof(from_addr);
  msg.msg_iov = vec;
  msg.msg_iovlen = 1;
  msg.msg_control = cmsg_un.data;
  msg.msg_controllen = sizeof(cmsg_un.data);
  msg.msg_flags = 0;
  
  if(recvmsg(netPath->eventSock, &msg, MSG_DONTWAIT) <= 0)
    return FALSE;
  
  /* get time stamp of packet */
  if(!time)
    return FALSE;
  
  if(msg.msg_controllen < sizeof(struct cmsghdr) || msg.msg_flags & MSG_CTRUNC)
  {
    PERROR("short or truncated cmsghdr!\n");
    return FALSE;
  }
  
  tv = 0;
  for (cmsg = CMSG_FIRSTHDR(&msg); cmsg != NULL; cmsg = CMSG_NXTHDR(&msg, cmsg))
  {
    if (cmsg->cmsg_level == SOL_SOCKET && cmsg->cmsg_type == SCM_TIMESTAMP)
      tv = (struct timeval *)CMSG_DATA(cmsg);
  }
  
  if(tv)
  {
    time->seconds = tv->tv_sec;
    time->nanoseconds = tv->tv_usec*1000;
    DBGV("kernel recv time stamp %us %dns\n", time->seconds, time->nanoseconds);
  }
  else
  {
    /* do not try to get by with recording the time here, better to fail
       because the time recorded could be well after the message receive,
       which would put a big spike in the offset signal sent to the clock servo */
    DBG("error getting recieve time\n");
    return FALSE;
  }

  /* save address */
  if(address)
    memcpy(address, inet_ntoa(from_addr.sin_addr), NET_ADDRESS_LENGTH);
  
  return TRUE;

#elif defined(_WIN32)
RunTimeOpts *rtOpts = (RunTimeOpts*)netPath->rtOpts;
PtpClock *ptpClock = (PtpClock*)netPath->ptpClock;
NS_UINT8 *ethHead, *ipHead, *udpHead, *ptpHead;
NS_UINT length, destPort;
NS_UINT overflowCount, sequenceId, hashValue;
NS_UINT8 messageType;
NS_UINT8 *psfStart;
PHYMSG_LIST *psfList;
PHYMSG_MESSAGE_TYPE_ENUM msgType;
PHYMSG_MESSAGE phyMsg;

    if ( rtOpts->haveLoopbackedSend ) {
        ethHead = &rtOpts->txBuff[0];
        ipHead  = &rtOpts->txBuff[0x0E];
        udpHead = &rtOpts->txBuff[0x22];
        ptpHead = &rtOpts->txBuff[0x2A];
        memcpy( buf, ptpHead, rtOpts->lastSendLength-0x2A);

        rtOpts->haveLoopbackedSend = FALSE;

        destPort = *(NS_UINT16*)&udpHead[0x02];
        if ( destPort == 0x3F01 && !rtOpts->useOneStepFlag) {
            if( !(((PEPL_PORT_HANDLE)rtOpts->eplPortHandle)->psfConfigOptions & STSOPT_TXTS_EN) ) {
                if ( PTPCheckForEvents( rtOpts->eplPortHandle) & PTPEVT_TRANSMIT_TIMESTAMP_BIT) {
                    PTPGetTransmitTimestamp( rtOpts->eplPortHandle, &time->seconds, &time->nanoseconds,
                                             &overflowCount);
                    DBG( "Got PTP looped back event message and timestamp - %d sec, %d nanosec\n", 
                          time->seconds, time->nanoseconds);
                }
                else {
                    ERROR( "NO TIMESTAMP AVAILABLE FOR LOOPED BACK TX EVENT PACKET!\n");
                }
                return 1;
            }
            else {
                // Reset flag to allow it to pick up the operation below
                rtOpts->haveLoopbackedSend = TRUE;
            }
        }
        else {
            return 2;
        }
    }

    if ( !MACReceivePacket( rtOpts->eplPortHandle, rtOpts->rxBuff, &length))
        return 0;
    DBG( "NR2\n" );    

    psfStart = IsPhyStatusFrame( rtOpts->eplPortHandle, rtOpts->rxBuff, length );
    while( psfStart ) {
        psfStart = intGetNextPhyMessage( rtOpts->eplPortHandle, psfStart, &msgType, &phyMsg, 0 );
        if( !psfStart ) {
            continue;
        }
#if 1
        // Debug help
        switch( msgType ) {
        case PHYMSG_STATUS_TX:
            DBG( "netRecv: PSF : PHYMSG_STATUS_TX:   %ds %dns  %d\n",
                        phyMsg.TxStatus.txTimestampSecs, 
                        phyMsg.TxStatus.txTimestampNanoSecs,
                        phyMsg.TxStatus.txOverflowCount );
            break;
        case PHYMSG_STATUS_RX:
            DBG( "netRecv: PSF : PHYMSG_STATUS_RX:   %ds %dns  %d   #%d   %d  %d\n", 
                        phyMsg.RxStatus.rxTimestampSecs, 
                        phyMsg.RxStatus.rxTimestampNanoSecs,
                        phyMsg.RxStatus.rxOverflowCount,
                        phyMsg.RxStatus.sequenceId,
                        phyMsg.RxStatus.messageType, 
                        phyMsg.RxStatus.sourceHash );
            break;
        case PHYMSG_STATUS_TRIGGER:
            DBG( "netRecv: PSF : PHYMSG_STATUS_TRIGGER:   %d\n", phyMsg.TriggerStatus.triggerStatus );
            break;
        case PHYMSG_STATUS_EVENT:
            DBG( "netRecv: PSF : PHYMSG_STATUS_EVENT: \n" );
            break;
        case PHYMSG_STATUS_ERROR:
            DBG( "netRecv: PSF : PHYMSG_STATUS_ERROR: \n" );
            break;
        case PHYMSG_STATUS_REG_READ:
            // Should never get this, but just in case!
            DBG( "netRecv: PSF : PHYMSG_STATUS_REG_READ: \n" );
            break;
        default:
            DBG( "netRecv: PSF : PSF %04X\n", msgType );                    
            break;
        }
#endif
        psfList = (PHYMSG_LIST *)((PEPL_PORT_HANDLE)rtOpts->eplPortHandle)->psfList;
        if( psfList ) {
            // Already have a list add to the end of it
            while( psfList->nxtMsg )
                psfList = psfList->nxtMsg;
            psfList = psfList->nxtMsg = OAIAlloc( sizeof(PHYMSG_LIST) );
        }
        else {
            // No list yet, start it.
            psfList = (PHYMSG_LIST *)((PEPL_PORT_HANDLE)rtOpts->eplPortHandle)->psfList = OAIAlloc( sizeof(PHYMSG_LIST) );
        }
        psfList->nxtMsg = NULL;
        psfList->msgType = msgType;
        memcpy( &psfList->phyMsg, &phyMsg, sizeof(PHYMSG_MESSAGE) );
    }  // while( psfStart )

    if( rtOpts->haveLoopbackedSend && (((PEPL_PORT_HANDLE)rtOpts->eplPortHandle)->psfConfigOptions & STSOPT_TXTS_EN) ) {
        // Look for TX Timestamp PSF
        psfList = (PHYMSG_LIST *)((PEPL_PORT_HANDLE)rtOpts->eplPortHandle)->psfList;
        if( psfList ) {
            do {
                if( psfList->msgType == PHYMSG_STATUS_TX ) {
                    time->seconds = psfList->phyMsg.TxStatus.txTimestampSecs;
                    time->nanoseconds = psfList->phyMsg.TxStatus.txTimestampNanoSecs;
                    DBG( "PSF timestamp - %d sec, %d nanosec\n", 
                          time->seconds, time->nanoseconds);
                }
                psfList = psfList->nxtMsg;
            } while( psfList );
			rtOpts->haveLoopbackedSend = FALSE;
			return 1;
		}
		DBG("[!psfList]");
		return 0;
    }

//    x;
//    DBGV( "DUMP RX PACKET - Length %d\n", length);
//    for ( x = 0; x < length; x++)
//    {
//        if ( (x % 16) == 0)
//        {
//            DBGV( "\n");
//        }
//        
//        DBGV( "%02X ", rtOpts->rxBuff[x] & 0xFF);
//    }
//    DBGV( "\n\n");
    
    ethHead = &rtOpts->rxBuff[0];
    ipHead  = &rtOpts->rxBuff[0x0E];
    udpHead = &rtOpts->rxBuff[0x22];
    ptpHead = &rtOpts->rxBuff[0x2A];

    if ( length < 48)
        return 0;
        
    if ( *(NS_UINT16*)&ethHead[0x0C] != 0x0008)     // IP packet?
        return 0;
    if ( ipHead[0x09] != 0x11)                      // UDP packet?
        return 0;
    destPort = *(NS_UINT16*)&udpHead[0x02];
    if ( destPort != 0x3F01 && destPort != 0x4001)  // PTP Event or general msg? 
        return 0;
    if ( *(NS_UINT16*)&ptpHead[0] != 0x0100)        // PTP Version
        return 0;

    memcpy( buf, ptpHead, length-0x2A);    
   
    if ( destPort == 0x3F01)
    {
        if ( !rtOpts->revA1SiliconFlag)
        {
            time->nanoseconds = flip32( *(NS_UINT32*)&ptpHead[126]);
            time->seconds = flip32( *(NS_UINT32*)&ptpHead[130]);
        
            // Discard sync msgs if we did a rate adj and are waiting for it to complete.
            
            DBG( "waitingForAdjAck %s, adjDoneAckRxed %s\n", ptpClock->waitingForAdjFlag ? "Yes":"No", 
                 time->nanoseconds & 0x80000000 ? "Yes":"No");
            
            if ( ptpClock->waitingForAdjFlag && !(time->nanoseconds & 0x80000000))
            {
                // We could lose the rate adj complete bit if the sync packet was
                // dropped, so use a counter to recover.
                if ( ptpClock->ignoreSyncCount != 0)
                {
                    ptpClock->ignoreSyncCount--;
                    DBG( "Ignoring Sync msg, previous time adj hasn't finished.\n");
                    return 0;
                }
            }
        
            ptpClock->ignoreSyncCount = 8;
            time->nanoseconds &= ~0x80000000;
            ptpClock->waitingForAdjFlag = FALSE;
        }
        else
        {
            time->seconds = 0;
            time->nanoseconds = 0;
        
            if ( PTPCheckForEvents( rtOpts->eplPortHandle) & PTPEVT_RECEIVE_TIMESTAMP_BIT)
            {
                PTPGetReceiveTimestamp( rtOpts->eplPortHandle, &time->seconds, &time->nanoseconds,
                                        &overflowCount, &sequenceId, &messageType, &hashValue);
                DBG( "Got PTP RX Timestamp event message and timestamp - %d sec, %d nanosec\n", 
                      time->seconds, time->nanoseconds);
            }
            else
            {
                ERROR( "TIMEOUT - NO TIMESTAMP AVAILABLE FOR RECEIVED EVENT PACKET!\n");
                return 0;
            }
        }
        return 3;
    }
    return 2;

#endif
  
}

Boolean netRecvGeneral(Octet *address, Octet *buf, NetPath *netPath)
{
#if defined(linux)
  struct sockaddr_in addr;
  socklen_t addr_len = sizeof(struct sockaddr_in);
  
  if(recvfrom(netPath->generalSock, buf, PACKET_SIZE, MSG_DONTWAIT, (struct sockaddr *)&addr, &addr_len) <= 0)
    return FALSE;
  
  /* save address */
  if(address)
    memcpy(address, inet_ntoa(addr.sin_addr), NET_ADDRESS_LENGTH);
    
  return TRUE;
  
#elif defined(_WIN32)
  
  return FALSE;
#endif
}


#ifdef _WIN32

void SendAPacket( Octet *buf, UInteger16 length, NetPath *netPath, UInteger16 srcPort, UInteger16 destPort)
{
RunTimeOpts *rtOpts = (RunTimeOpts*)netPath->rtOpts;
Octet *txBuf = rtOpts->txBuff;
Octet *txBufPtr = txBuf;
int x;

    // Build the Ethernet header
    memcpy( txBufPtr, rtOpts->destMACAddress, 6);
    memcpy( txBufPtr+6, rtOpts->localMACAddress, 6);
    *(NS_UINT16*)&txBufPtr[12] = 0x0008;
    txBufPtr += 14;
    
    // Build the IP header
    txBufPtr[0] = (0x04 << 4) | 0x05;                       // Version & header length
    txBufPtr[1] = 0x00;                                     // Type of Service
    *(NS_UINT16*)&txBufPtr[2] = htons( 20 + 8 + length);    // Total datagram length
    *(NS_UINT16*)&txBufPtr[4] = 0x0000;                     // Frag id
    *(NS_UINT16*)&txBufPtr[6] = 0x0000;                     // Frag offset & flags
    txBufPtr[8] = 8;                                        // Time to live hops
    txBufPtr[9] = 17;                                       // Protocol - UDP
    memcpy( &txBufPtr[12], rtOpts->srcIPAddress, 4);
    *(NS_UINT32*)&txBufPtr[16] = htonl( netPath->bcastAddr);
    txBufPtr += 20;
    
    // Build the UDP header
    *(NS_UINT16*)&txBufPtr[0] = htons( srcPort);
    *(NS_UINT16*)&txBufPtr[2] = htons( destPort);
    *(NS_UINT16*)&txBufPtr[4] = htons( 8 + length);
    txBufPtr += 8;
    
    // Copy over the PTP packet data
    memcpy( txBufPtr, buf, length);
    
    x;
//    DBGV( "DUMP PACKET\n");
//    for ( x = 0; x < length; x++)
//    {
//        if ( (x % 16) == 0)
//        {
//            DBGV( "\n");
//        }
//        
//        DBGV( "%02X ", txBuf[x] & 0xFF);
//    }
//    DBGV( "\n\n");
    
    // Send the packet
    MACSendPacket( rtOpts->eplPortHandle, txBuf, (NS_UINT)(txBufPtr-txBuf) + length);

    // Need to loop the packet back into the receive engine
    rtOpts->lastSendLength = (NS_UINT)(txBufPtr-txBuf) + length;
    rtOpts->haveLoopbackedSend = TRUE;
    return;
}

#endif // _WIN32

Boolean netSendEvent(Octet *address, Octet *buf, UInteger16 length, NetPath *netPath)
{
#if defined(linux)
  struct sockaddr_in addr;
  
  addr.sin_family = AF_INET;
  addr.sin_port = htons(PTP_EVENT_PORT);
  if(address)
    inet_aton(address, &addr.sin_addr);
  else
    addr.sin_addr.s_addr = netPath->bcastAddr;
  
  if(sendto(netPath->eventSock, buf, length, 0, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) < 0)
  {
    DBGV("error sending event message\n");
    return FALSE;
  }
  
  return TRUE;
  
#elif defined(_WIN32)
    DBG( "***Sending event message\n");
    SendAPacket( buf, length, netPath, netPath->eventSock, PTP_EVENT_PORT);
    return TRUE;
#endif
}

Boolean netSendGeneral(Octet *address, Octet *buf, UInteger16 length, NetPath *netPath)
{
#if defined(linux)
  struct sockaddr_in addr;
  
  addr.sin_family = AF_INET;
  addr.sin_port = htons(PTP_GENERAL_PORT);
  if(address)
    inet_aton(address, &addr.sin_addr);
  else
    addr.sin_addr.s_addr = netPath->bcastAddr;
  
  if(sendto(netPath->generalSock, buf, length, 0, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) < 0)
  {
    DBG("error sending general message\n");
    return FALSE;
  }
  
  return TRUE;
  
#elif defined(_WIN32)
    DBG( "***Sending general message\n");
    SendAPacket( buf, length, netPath, netPath->generalSock, PTP_GENERAL_PORT);
    return TRUE;
#endif
}

