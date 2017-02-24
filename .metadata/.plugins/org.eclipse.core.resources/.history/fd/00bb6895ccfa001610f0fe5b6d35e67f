"""
  alp1588.py - ALP 1588 Library

  Copyright (c) 2006 National Semiconductor Corporation.
  All Rights Reserved.

  Implements the basic functions for 1588 ALP platfrom.
"""

# -------------------------------------------------------------------
# Revision History
#
# $Log: alp1588.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.6  2008/09/18 17:13:14  dave
# Updates to use modified ALP that includes PSF fixes.
# Major cleanup of unused code.
#
# Revision 1.5  2008/04/01 17:01:45  dave
# fix MDIO checksum validation.
#
# Revision 1.4  2008/03/13 12:29:57  dave
# rename GetRxTimestamp to GetRxTimestamp_old
#
# Revision 1.3  2008/01/23 16:13:14  dave
# make backwards compatible with integrity platform.
#
# Revision 1.2  2007/12/07 11:50:43  dave
# replace tabs with spaces.
# implement broadcast write capability.
#
# Revision 1.1  2007/09/26 10:46:50  dave
# Initial revision
#
# Revision 1.8  2007/07/19 16:22:54  dave
# Add PCF support to MdioWrite command to allow basic scripts
# to use Phy Control Frames.
#
# Revision 1.7  2007/07/19 10:45:40  dave
# check for completion on MDIO Read and Write
#
# Revision 1.6  2007/07/13 14:47:42  benb
# Oops, need to read and calculate the write checksum in SubTime1588
#
# Revision 1.5  2007/07/13 14:39:34  benb
# Added PTP page 4 write checksum checking to AddTime1588 and
#   SubTime1588.
#
# Revision 1.4  2007/07/13 11:31:54  benb
# Update with new ALP enumeration
# Add support for "Stop" button
#
# Revision 1.3  2007/07/05 17:09:26  benb
# Updated to detect either the Opal Kelly board or
#   the ALP board.
#
# Revision 1.2  2007/07/05 11:14:22  dave
# updates as of 7/5/07
#
#
#

from NSLibrary import *
from array import *
import sys
import ok
import time
one_ms = 0.001
one_us = 0.000001

from NS_1588_constants import *


# -------------------------------------------------------------------
# 1588 Initialization script
#
# Enumerate the devices:
# Look first for an Opal Kelly board.  If that is not found, look for an ALP
# board.
def find_ok_device( device=None, port=None):
    if device == None:
        devices = NSEnumDevices( virtualPorts=False, okUSB3010 = True)
        if len( devices) == 0:
            print "No MDIO devices were detected - exiting"
            return None
        else:
            for dev in devices:
                devInfo = dev.GetDeviceInfo()
                if devInfo['type'] == DEV_UNKNOWN:
                    print "FOUND Opal Kelly Device"
                    pldDeviceObj = dev   # Save it
                    device = dev
                    port = device.EnumPorts()[0]
                    xem = device.deviceHandle[0]
                    break
            else:
                print "Did not find Opal Kelly PLD device - exiting"
                return None
    else:
        # In ALP device & port objects have already been setup
        print "Found PHY device on ALP platform"
        pldDeviceObj = device
        xem = port  # Don't go direct to OK interface, use EPL's interfaces instead
    
    print "Read from port 0, register 0x0002 : %X" % (port.ReadReg( 0x0002))
    print "Read from port 0, register 0x0003 : %X\n\n" % (port.ReadReg( 0x0003))
    
    # Return the device
    return xem

# -------------------------------------------------------------------
# 1588 MDIO Read script
#
def AlpMdioRead(xem, phyAddr, regAddr, verbose):
    #
    # Read MDIO register
    mdio_read_val = xem.ReadReg( (regAddr & 0x1F) | ((regAddr & 0xF00) >> 3))
    #
    if(verbose):
        print "MDIO Read. Address: %x, Data: %x" % (phyAddr, mdio_read_val)
    return (mdio_read_val)

#
#
# End of 1588 MDIO Read routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 MDIO Write script
#
def AlpMdioWrite(xem, phyAddr, regAddr, writeData, verbose):
    #
    # Write MDIO register
    xem.WriteReg( (regAddr & 0x1F) | ((regAddr & 0xF00) >> 3), writeData)
    
    if(verbose):
        print "MDIO Write. Address: %x, Data: %x" % (regAddr, writeData)
    #

#
#
# End of 1588 MDIO Write routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 MDIO Read script
# 
def MdioRead(xem, phyAddr, regAddr, verbose):
    # Includes page change if necessary (NO LONGER INCLUDED)
    page = regAddr >> 8
    address = regAddr
    #
    # Read MDIO register
    mdio_read_val = AlpMdioRead(xem, phyAddr, address, 0)
    #
    if(verbose):
        print "MDIO Read. Page: %x, Address: %x, Data: %x" % (page, address, mdio_read_val)
    return (mdio_read_val)

#
#
# End of 1588 MDIO Read routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 MDIO Write script
# 
def MdioWrite(xem, phyAddr, regAddr, writeData, verbose):
    # Includes page change if necessary (NO LONGER INCLUDED)
    page = regAddr >> 8
    address = regAddr & 0xff
    #
    if (xem.pcf_en):
        pcf_list = [0x40 | (phyAddr << 1) | (page >> 3)]
        pcf_list = pcf_list + [((page & 0x7) << 5) | address] 
        pcf_list = pcf_list + [(writeData >> 8), (writeData & 0xff)]
        xem.pcf_list = xem.pcf_list + pcf_list
        if(verbose):
            print "PCF register write: [%x %x %x %x]" % (pcf_list[0], pcf_list[1], pcf_list[2], pcf_list[3])
        if (xem.send_pcf):
            Send_PCF(xem)
        if(verbose):
            print "PCF Write. Page: %x, Address: %x, Data: %x" % (page, address, writeData)
    else:
        # allow use of defined phyAddr rather than port phyAddr
        # provides for broadcast write function
        xem.curr_page = page
        address = regAddr
        save_phyAddr = xem.port.portMdioAddress
        xem.port.portMdioAddress = phyAddr
        AlpMdioWrite(xem, phyAddr, address, writeData, 0)
        xem.port.portMdioAddress = save_phyAddr
        if(verbose):
            print "MDIO Write. Page: %x, Address: %x, Data: %x" % (page, address, writeData)

#
#
# End of 1588 MDIO Write routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 ValidateMdioCksum script
#
def ValidateMdioCksum(buf_array):
    return(ones_comp_sum16(buf_array) == 0xffff)

#
#
# End of ValidateMdioCksum routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 SendTxPkt script
#
def SendTxPkt(xem, pktbuf, pktLen, verbose):
    #
    if(verbose):
        print ""
        print "Sending TX Pkt."
    #
    from epl import charArray
    inBufBytes = charArray( pktLen)
    for b in range( pktLen):
        inBufBytes[b] = pktbuf[b]
    xem.MACSendPacketNoUdpChecksum( inBufBytes, pktLen)

#
#
# End of 1588 SendTxPkt routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Send_PCF script
#    Send Phy Control Frame
#    options are contained in xem
def Send_PCF(xem):
    #
    if (xem.pcf_da_sel == 0):
        pkt_tmp = [0x08, 0x00, 0x17, 0x0B, 0x6B, 0x0F]
    else:
        pkt_tmp = [0x08, 0x00, 0x17, 0x00, 0x00, 0x00]
    pkt_tmp = pkt_tmp + xem.pcf_header + [95, 80, 72, 89, 67, 70]
    pkt_tmp = pkt_tmp + xem.pcf_list + [0, 0, 0, 0]
    if (len(pkt_tmp) < 60):
        for i in range(60 - len(pkt_tmp)):
            pkt_tmp = pkt_tmp + [0]
    pktbuf_len = len(pkt_tmp)
    SendTxPkt(xem, pkt_tmp, pktbuf_len, 0)
    txdone = True
    rxpkt_rdy = False
    xem.pcf_list = []
    return (rxpkt_rdy)
    #return (pktbuf)

#
#
# End of 1588 SendPhyControlFrame routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 GetRXPkt script
#
def GetRXPkt(xem, verbose):
        from epl import charArray
        inBufBytes = charArray( 4096)
        rxFlag, rx_byte_cnt = xem.MACReceivePacket( inBufBytes)
        if rxFlag:
            retBuf = []
            for n in range( rx_byte_cnt):
                retBuf.append( inBufBytes[n])
            return retBuf
        return []

#
#
# End of 1588 GetRXPkt routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 FlushRX script
#
# Flushes Receive packets by simply doing 4 read_pkt_done strobes.
# Clear out Triggers as well
#
def FlushRX(xem, verbose):
    #
    if(verbose):
        print ""
        print "Flushing RX Pkts."
        
    xem.MACFlushReceiveFifos()
    return

#
#
# End of 1588 FlushRX routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# ones_comp checksum script
#
def ones_comp_chksum(buf_array):
    #
    # compute ones complement checksum
    i=0
    sum=0
    while i < len(buf_array):
        tmp1 = (buf_array[i] << 8) + buf_array[i+1]
        sum = sum + tmp1
        i = i+2
    rollover = sum >> 16
    sum = (sum & 0xffff) + rollover
    rollover = sum >> 16
    sum = (sum & 0xffff) + rollover
    ones_comp_sum = ~sum & 0xffff
    #
    return ones_comp_sum

#
#
# End of ones_comp_chksum routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# ones_comp_sum16 script
#
def ones_comp_sum16(buf_array):
    #
    # compute ones complement sum of 16-bit values
    i=0
    sum=0
    while i < len(buf_array):
        sum = sum + buf_array[i]
        i = i+1
    while (sum > 0xffff):
        rollover = sum >> 16
        sum = (sum & 0xffff) + rollover
    #
    return sum

#
#
# End of ones_comp_sum16 routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 GetTxTimestamp script
#
def GetTxTimestamp(xem, phyAddr, verbose):
    #
    if(verbose):
        print ""
        print "Getting Transmit Timestamp."
    #
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TXTS, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TXTS, 0) & 0x3fff
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + timestamp
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TXTS, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + timestamp
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TXTS, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + timestamp
    if(verbose):
        print "Transmit Timestamp (sec) = ", timestamp[0:4]
        print "Transmit Timestamp (ns)  = ", timestamp[4:8]
    #
    return (timestamp)

#
#
# End of 1588 GetTxTimestamp routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 GetTime1588 script
#
def GetTime1588(xem, phyAddr, verbose):
    #
    if(verbose):
        print ""
        print "Getting 1588 Clock Time."
    #
    MdioWrite(xem, phyAddr, PTP_CTL, 0x0020, 0)
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    if(verbose):
        print "Clock 1588 Time (sec) = ", time_1588[0:4]
        print "Clock 1588 Time (ns)  = ", time_1588[4:8]
    #
    return (time_1588)

#
#
# End of 1588 GetTime1588 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 SetTime1588 script
#
def SetTime1588(xem, phyAddr, time_1588, verbose):
    #
    if(verbose):
        print ""
        print "Setting 1588 Clock Time."
    #
    write_data = (time_1588[6]<<8) + time_1588[7]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[4]<<8) + time_1588[5]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[2]<<8) + time_1588[3]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[0]<<8) + time_1588[1]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    MdioWrite(xem, phyAddr, PTP_CTL, 0x0010, 0)
    if(verbose):
        print "Set Clock 1588 Time (sec) = ", time_1588[0:4]
        print "Set Clock 1588 Time (ns)  = ", time_1588[4:8]
    #
    return (time_1588)

#
#
# End of 1588 SetTime1588 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 AddTime1588 script
#
def AddTime1588(xem, phyAddr, time_1588, verbose):
    #
    if(verbose):
        print ""
        print "Adding 1588 Clock Time."
    #
    if (not xem.pcf_en):
        # Clear the write checksum
        MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
    write_data = (time_1588[6]<<8) + time_1588[7]
    oc_list = [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[4]<<8) + time_1588[5]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[2]<<8) + time_1588[3]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588[0]<<8) + time_1588[1]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = 0x0008
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_CTL, write_data, 0)
    if(verbose):
        print "Add Clock 1588 Time (sec) = ", time_1588[0:4]
        print "Add Clock 1588 Time (ns)  = ", time_1588[4:8]
    #
    if (not xem.pcf_en):
        # Read/Validate checksum
        wrcksum = MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [wrcksum])):
            print "FAILED:  AddTime1588 write checksum failure"
            print "  checksum data:", oc_list
            print "  write checksum value: %x" % wrcksum
            return 0
        else:
            return (time_1588)
    else:
        return (time_1588)

#
#
# End of 1588 AddTime1588 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 SubTime1588 script
#
def SubTime1588(xem, phyAddr, time_1588, verbose):
    #
    if(verbose):
        print "Subtract 1588 Clock Time."
    #
    # Convert to 2's complement
    time_1588_sec = (time_1588[0] << 24) + (time_1588[1] << 16) + (time_1588[2] << 8) + (time_1588[3])
    time_1588_ns = (time_1588[4] << 24) + (time_1588[5] << 16) + (time_1588[6] << 8) + (time_1588[7])
    time_1588_sec = (0x100000000 - time_1588_sec) & 0xFFFFFFFF
    time_1588_ns = (0x100000000 - time_1588_ns) & 0xFFFFFFFF

    time_1588_comp = [time_1588_sec >> 24] + [(time_1588_sec >> 16) & 0xff] + [(time_1588_sec >> 8) & 0xff] + [time_1588_sec & 0xff]
    time_1588_comp = time_1588_comp + [time_1588_ns >> 24] + [(time_1588_ns >> 16) & 0xff] + [(time_1588_ns >> 8) & 0xff] + [time_1588_ns & 0xff]
    time_array = array( 'B', time_1588_comp)
    time_1588_comp = time_array.tolist()
    #
    if (not xem.pcf_en):
        # Clear the write checksum
        MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
    write_data = (time_1588_comp[6]<<8) + time_1588_comp[7]
    oc_list = [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588_comp[4]<<8) + time_1588_comp[5]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588_comp[2]<<8) + time_1588_comp[3]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (time_1588_comp[0]<<8) + time_1588_comp[1]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = 0x0008
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_CTL, write_data, 0)
    if(verbose):
        print "Add (2's comp) Clock 1588 Time (sec) = ", time_1588_comp[0:4]
        print "Add (2's comp) Clock 1588 Time (ns)  = ", time_1588_comp[4:8]
    #
    if (not xem.pcf_en):
        # Read/Validate checksum
        wrcksum = MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [wrcksum])):
            print "FAILED:  SubTime1588 write checksum failure"
            print "  checksum data:", oc_list
            print "  write checksum value: %x" % wrcksum
            return 0
        else:
            return (time_1588)
    else:
        return (time_1588)

#
#
# End of 1588 SubTime1588 routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 TStoNS script
#    Convert Timestamp list to nanoseconds
def TStoNS(TimeStamp):
    #
    # Convert to sec, ns fields
    #print "TStoNS Timestamp ", TimeStamp
    if (len(TimeStamp) == 8):
        time_sec = (TimeStamp[0] << 24) + (TimeStamp[1] << 16) + (TimeStamp[2] << 8) + (TimeStamp[3])
        time_ns = (TimeStamp[4] << 24) + (TimeStamp[5] << 16) + (TimeStamp[6] << 8) + (TimeStamp[7])
        time_ns = time_ns + (time_sec * 1000000000)
    else:
        print "TStoNS: ERROR in Timestamp", TimeStamp
        time_ns = 0
    return (time_ns)

#
#
# End of 1588 TStoNS routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# 1588 NStoTS script
#    Convert nanoseconds value to Timestamp list
def NStoTS(time_ns):
    #
    # NS portion
    ns_only = time_ns % 1000000000
    ns_list = [ns_only >> 24] + [(ns_only >> 16) & 0xff] + [(ns_only >> 8) & 0xff] + [ns_only & 0xff]
    ns_array = array( 'B', ns_list)
    ns_list = ns_array.tolist()
    # Seconds portion
    sec_only = (time_ns - ns_only) / 1000000000
    sec_list = [sec_only >> 24] + [(sec_only >> 16) & 0xff] + [(sec_only >> 8) & 0xff] + [sec_only & 0xff]
    sec_array = array( 'B', sec_list)
    sec_list = sec_array.tolist()
    TimeStamp = sec_list + ns_list
    #
    return (TimeStamp)

#
#
# End of 1588 NStoTS routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 SetRate1588 script
#
def SetRate1588(xem, phyAddr, rate_1588, verbose):
    #
    if(verbose):
        print ""
        print "Setting 1588 Clock Rate."
    #
    # Read MDIO register
    rate = abs(rate_1588)
    write_data = (int(rate >> 16) & 0x7fff)
    if (rate_1588 < 0):
        write_data = write_data | 0x8000
    MdioWrite(xem, phyAddr, PTP_RATEH, write_data, 0)
    write_data = int(rate & 0xffff)
    MdioWrite(xem, phyAddr, PTP_RATEL, write_data, 0)
    if(verbose):
        print "Set Clock 1588 Rate = ", rate_1588
    #

#
#
# End of 1588 SetRate1588 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 GetRate1588 script
#
def GetRate1588(xem, phyAddr, verbose):
    #
    if(verbose):
        print ""
        print "Getting 1588 Clock Rate."
    #
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RATEL, 0)
    get_rate_1588 = long(mdio_read_val)
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RATEH, 0)
    get_rate_1588 = ((mdio_read_val & 0x3FFF) << 16) + get_rate_1588
    if (mdio_read_val & 0x8000):
        get_rate_1588 = -get_rate_1588
    #
    if(verbose):
        print "Get Clock 1588 Rate = ", get_rate_1588
    #
    return(get_rate_1588)

#
#
# End of 1588 GetRate1588 routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 GetRxStats script
#
def GetRxStats(xem, verbose):
    #
    # Get Address and Bytecount
    xem.UpdateWireOuts()
    crc_err_cnt = (xem.GetWireOutValue(0x26))
    rx_runt_cnt = (xem.GetWireOutValue(0x27))
    rx_er_cnt = (xem.GetWireOutValue(0x28))
    missed_pkt_cnt = (xem.GetWireOutValue(0x29))
    if(verbose):
        print "Packet Error Counts"
        print "   CRC Errors:   %d" % crc_err_cnt
        print "   Runt Errors:  %d" % rx_runt_cnt
        print "   RX_ER Errors: %d" % rx_er_cnt
        print "   RX Missed Pkts: %d" % missed_pkt_cnt
    #
    Error_list = [crc_err_cnt, rx_runt_cnt, rx_er_cnt, missed_pkt_cnt]
    #
    return Error_list

# -------------------------------------------------------------------
# checkCRC script
#
def checkCRC(pktbuf, verbose):
    #
    # Check CRC for packet buffer
    present_crc = 0x100000000 - 1
    for i in range(len(pktbuf)):
        for j in range(8):
            data_bit = ((pktbuf[i] >> j) & 0x01) ^ (present_crc >> 31)
            #print (pktbuf[i] >> j), data_bit
            if (data_bit):
                present_crc = ((present_crc << 1) ^ 0x04C11DB7) & (0x100000000 - 1)
            else:
                present_crc = (present_crc << 1) & (0x100000000 - 1)
            #hexprint(present_crc)
    crc_ok = (present_crc == (0x100000000 - 0x38FB2285))
    if (verbose):
        if (crc_ok):
            print "CRC Check OK: %x" % present_crc
        else:
            print "CRC Check FAIL: %x" % present_crc
    return (crc_ok)


