# config_options script
# Queries user to set basic options
#
# $Id: config_options.py,v 1.2 2008/09/22 23:25:23 robertst Exp $
#
# $Log: config_options.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.12  2008/09/18 17:13:14  dave
# Updates to use modified ALP that includes PSF fixes.
# Major cleanup of unused code.
#
# Revision 1.11  2008/08/26 14:48:31  dave
# replace master_SA and slave_SA with mac_SA.
#
# Revision 1.10  2008/06/26 15:12:46  dave
# Update with PTP spec names for dataset variables.
#
# Revision 1.9  2008/05/14 15:38:20  dave
# major updates
#
# Revision 1.8  2008/03/21 13:17:38  dave
# if master, set slave_only to 0.
#
# Revision 1.7  2008/03/13 12:31:43  dave
# update pdelay_req to use log.
#
# Revision 1.6  2008/01/23 16:13:55  dave
# add option to include UDP checksum.
# create cfg local to allow use with Boundary Clock.
#
# Revision 1.5  2008/01/15 13:23:45  dave
# move more config options to config class.
#
# Revision 1.4  2007/12/13 17:33:33  benb
# Don't assign sync_interval to cfg.portDS.logMinDelayReqInterval
#
# Revision 1.3  2007/11/05 15:54:15  dave
# updates to select default values with Return
# configure v2 Delay_Req log interval and Sync log interval.
#
# Revision 1.2  2007/09/28 13:22:49  dave
# Updates for identity fields.
#
# Revision 1.1  2007/09/26 10:46:50  dave
# Initial revision
#
# Revision 1.5  2007/08/15 18:32:14  dave
# fix operation with ALP.
# Add cfg.rx_byte0_mask/data.
#
# Revision 1.4  2007/08/08 15:29:43  dave
# add clkout options.
#
# Revision 1.3  2007/07/25 12:27:04  dave
# fix v1 operation.
#
# Revision 1.2  2007/07/23 16:37:17  dave
# add peer delay options.
#
# Revision 1.1  2007/07/19 16:24:42  dave
# Initial revision
#


def ALP_check():
    Integrity = 0
    try:
        ALPScriptInput
    except:
        Integrity = 1
    return (Integrity)

def GetInput(prompt_string):
    try:
        use_integrity = Integrity
    except:
        use_integrity = 0
    if (use_integrity):
        txt = raw_input(prompt_string)
    else:
        txt = ALPScriptInput(prompt_string)
    return(txt)


#
import sys


#
Integrity = ALP_check()

# Set Mac and IP addresses
txt = GetInput( "Station Number (sets Mac/IP addresses): ")
txt = txt.strip()   # Remove leading & trailing white space
try:
        txtAsVal = int(txt)
except:
        print "Invalid value, Using default: %d" % 0
        txtAsVal = 0
station_num = txtAsVal


# Select IEEE Version
txt = GetInput( "IEEE 1588 Version (1 or 2): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
try:
    txtAsVal = int(txt)
except:
    print "Invalid value, choosing v1"
    txtAsVal = 1
cfg.v2_enable = (txtAsVal == 2)
#
# V1 Options
if (not cfg.v2_enable):
    cfg.l2_enet = 0
    cfg.ipv4_en = 1
    cfg.ipv6_en = 0
    cfg.portDS.versionNumber = 1
    cfg.byte0_mask = 0xff
    cfg.byte0_data = 0x00
    cfg.rx_byte0_mask = 0xff
    cfg.rx_byte0_data = 0x00
    cfg.portDS.delayMechanism = DELAY_E2E
#
# V2 Options
if (cfg.v2_enable):
    cfg.portDS.versionNumber = 2
    cfg.byte0_mask = 0xf8
    cfg.byte0_data = 0x00
    cfg.rx_byte0_mask = 0xf8
    cfg.rx_byte0_data = 0x00
    # Layer 2 ?
    txt = GetInput( "Layer2 (y/n): ")
    txt = txt.strip()   # Remove leading & trailing white space
    #    
    if (txt == 'y'):
        cfg.l2_enet = 1
        cfg.ipv4_en = 0
        cfg.ipv6_en = 0
    else:
        cfg.l2_enet = 0
        # IPv4 vs IPv6 ?
        txt = GetInput( "IPv4 (y/n): ")
        txt = txt.strip()   # Remove leading & trailing white space
        #    
        if (txt == 'y'):
            cfg.ipv4_en = 1
            cfg.ipv6_en = 0
        else:
            cfg.ipv4_en = 0
            cfg.ipv6_en = 1
            print "UDP/IPv6 selected"
    # Peer Delay Mechanism
    txt = GetInput( "Initiate Peer Delay mechanism?: ")
    txt = txt.strip()   # Remove leading & trailing white space
    #    
    if (txt == 'y'):
        cfg.portDS.delayMechanism = DELAY_P2P
        # Peer Delay period ?
        print "PDelay_Req Interval = 2**(log_min_mean_pdelay_req_interval)"
        print "   i.e., 0 => 1 second, 5 = 32 seconds"
        txt = GetInput( "   Input log_min_mean_pdelay_req_interval (default = 1):")
        if (txt == ''):
            txt = "1"
        cfg.portDS.logMinPdelayReqInterval = int(txt)
    else:
        cfg.portDS.delayMechanism = DELAY_E2E
#
# Phy Control Frames
txt = GetInput( "Use Phy Control Frames? (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
    cfg.pcf_en = 1
else:
    cfg.pcf_en = 0
#
# Master/Slave
txt = GetInput( "Slave Only (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
    slave_en = 1
    cfg.defaultDS.slaveOnly = 1
else:
    slave_en = 0
    cfg.defaultDS.slaveOnly = 0
    txt = GetInput( "Preferred Master (y/n): ")
    txt = txt.strip()   # Remove leading & trailing white space
    if (txt == 'y'):
        cfg.defaultDS.priority1 = 127
    else:
        cfg.defaultDS.priority1 = 128

cfg.mac_SA = cfg.mac_SA[0:5] + [station_num]
cfg.ipv4_src_addr = [192, 168, 1, station_num]
cfg.defaultDS.clockIdentity = cfg.mac_SA[0:3] + [0xFF, 0xFE] + cfg.mac_SA[3:6]
cfg.portDS.portIdentity = cfg.defaultDS.clockIdentity + [0, 1]
cfg.parentDS.parentPortIdentity = cfg.portDS.portIdentity
cfg.parentDS.grandmasterIdentity = cfg.defaultDS.clockIdentity
cfg.ivp6_src_addr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff] + cfg.ipv4_src_addr
#
# Timestamp Insertion
cfg.ts_insert = 0
cfg.dr_insert = 0
txt = GetInput( "Timestamp Insertion (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
    cfg.ts_insert = 1
    # Delay_Req Timestamp Insertion
    txt = GetInput( "Delay_Req Timestamp Insertion (y/n): ")
    txt = txt.strip()   # Remove leading & trailing white space
    #    
    if (txt == 'y'):
        cfg.dr_insert =1
#
print ""
print "Slave Options:"
# Slave Options
#
# Temporary Rate
txt = GetInput( "Time Correction: Temporary Rate (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
        cfg.temp_rate_en = 1
        txt = GetInput( "Temporary Rate Duration in us (default = 10000): ")
        txt = txt.strip()   # Remove leading & trailing white space
        if (txt == ''):
            txt = "10000"
        cfg.trate_duration_us = int(txt)
        # Set max trate correction to +/- 5ppm
        cfg.max_trate_correct = int(round((5.0/1000000) * cfg.trate_duration_us * 1000))
        cfg.min_step_adjust = 2 * cfg.max_trate_correct
else:
        cfg.temp_rate_en = 0
        cfg.max_trate_correct = 0
        cfg.min_step_adjust = cfg.min_time_correct
#

print ""
print "Master Options"
# Master options
#
# One-Step
txt = GetInput( "One-Step operation (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
        cfg.one_step = 1
        cfg.tx_chk_1step = 0
        cfg.ipv4_udp_chksum_en = 0
        if (cfg.ipv4_en):
            txt = GetInput( "Enable UDP checksum (y/n): ")
            txt = txt.strip()
            if (txt == 'y'):
                cfg.tx_chk_1step = 1
                cfg.ipv4_udp_chksum_en = 1
else:
        cfg.one_step = 0
#
# Sync Interval
if (not cfg.v2_enable):
        txt = GetInput( "Sync Interval (in seconds): ")
        txt = txt.strip()   # Remove leading & trailing white space
        #    
        cfg.sync_interval = int(float(txt) * (10**9))
else:
        print "Sync Interval = 2**(logMeanSyncInterval)"
        print "   i.e., 1 => 2sec, 0 => 1sec, -1 => 0.5sec"
        txt = GetInput( "   Input logMeanSyncInterval (default = 0):")
        if (txt == ''):
            txt = "0"
        cfg.portDS.logSyncInterval = int(txt)
        cfg.sync_interval = int((2.0**cfg.portDS.logSyncInterval) * (10**9))
if (cfg.v2_enable & (cfg.portDS.delayMechanism == DELAY_E2E)):
        print "Delay_Req Interval = 2**(log_min_delay_req_interval)"
        print "   i.e., 1 => 2 sync cycles, 5 => 32 sync cycles"
        txt = GetInput( "   Input log_min_delay_req_interval (default = 1):")
        if (txt == ''):
            txt = "1"
        cfg.portDS.logMinDelayReqInterval = int(txt) + cfg.portDS.logSyncInterval
        cfg.master_log_min_delay_req_interval = cfg.portDS.logMinDelayReqInterval

# Synchronous Ethernet
print ""
txt = GetInput( "Synchronous Ethernet (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
if (txt == 'y'):
        cfg.sync_enet = 1
        if (cfg.temp_rate_en):
            txt = GetInput( "Are you sure you want temp rate enabled (y/n): ")
            txt = txt.strip()   # Remove leading & trailing white space
            cfg.temp_rate_en = (txt == 'y')
else:
        cfg.sync_enet = 0
#

# CLKOUT configuration
txt = GetInput( "Enable CLKOUT (y/n): ")
txt = txt.strip()   # Remove leading & trailing white space
#    
cfg.clkout_en = (txt == 'y')
if (cfg.clkout_en):
    # CLKOUT Divisor
    cfg.clkout_div_by_n = 0
    while ((cfg.clkout_div_by_n < 2) | (cfg.clkout_div_by_n > 255)):
        txt = GetInput( "CLKOUT divide-by-N (2-255): ")
        txt = txt.strip()   # Remove leading & trailing white space
        #    
        cfg.clkout_div_by_n = int(txt)
    # Align CLKOUT?
    txt = GetInput( "Phase Align CLKOUT (y/n): ")
    txt = txt.strip()   # Remove leading & trailing white space
    #    
    cfg.align_clkout = (txt == 'y')
    if (cfg.align_clkout & cfg.temp_rate_en):
        cfg.min_step_adjust = ((cfg.clkout_div_by_n * 4)/2) + cfg.max_trate_correct
else:
    cfg.align_clkout = 0
    

# Enable synchronous ethernet mode if requested
# Also enable CLKOUT if requeseted
phycr2_read = MdioRead(xem, phyAddr, PHYCR2, 0)
phycr2_write = phycr2_read & (~SYNC_ENET_EN)
if (cfg.sync_enet == 1):
    phycr2_write = (phycr2_write | SYNC_ENET_EN)
if (cfg.clkout_en):
    phycr2_write = phycr2_write & (~CLK2MAC_DISABLE)
MdioWrite(xem, phyAddr, PHYCR2, (phycr2_write), 0)
#time.sleep(2)


# Initialize variables based on configuration
# Set Duplex mode of ALP
if isinstance( xem, PhyPort):
    phy_duplex = OkSetDuplex(ok_functions)
       
# Modified options
if (cfg.one_step):
    cfg.sync_corr_fld = xem.tx_ts_dly

if (cfg.v2_enable):
    xem.correct_1step = 0
    xem.sendPortId = cfg.portDS.portIdentity
else:
    xem.correct_1step = xem.one_step_correct
    xem.sendPortId = cfg.mac_SA + cfg.v1_srcPortID

# Timestamp Insertion points
if (cfg.v2_enable):
    cfg.ts_ins_ns_off = v2_ts_ins_ns_off
    cfg.ts_ins_sec_off = v2_ts_ins_sec_off
    cfg.ts_ins_sec_en = v2_ts_ins_sec_en
    cfg.ts_ins_sec_len = v2_ts_ins_sec_len
else:
    cfg.ts_ins_ns_off = rxts_ins_ns_off
    cfg.ts_ins_sec_off = rxts_ins_sec_off
    cfg.ts_ins_sec_en = rxts_ins_sec_en
    cfg.ts_ins_sec_len = rxts_ins_sec_len

# Set adjust_done_capable for revA2
xem.adjust_done_capable = (cfg.dp83640_mdl_rev == 1)

# Set Temp Rate duration in number of 8ns clock cycles
cfg.trate_duration = (cfg.trate_duration_us * 1000) >> 3

# Set PAGE_SEL register
xem.pcf_en = 0
MdioWrite(xem, phyAddr, PAGESEL, xem.curr_page, 0)

# Set PTP Clock period to ref_period
if (cfg.clksrc_div_pgm):
    MdioWrite(xem, phyAddr, PTP_CLKSRC, (PTP_CLKSRC_DIV | (cfg.ref_period & 0xf8)), 0)
else:
   if (cfg.clksrc_ext):
       MdioWrite(xem, phyAddr, PTP_CLKSRC, (PTP_CLKSRC_EXT | cfg.ref_period), 0)
   else:
       MdioWrite(xem, phyAddr, PTP_CLKSRC, cfg.ref_period, 0)
    
