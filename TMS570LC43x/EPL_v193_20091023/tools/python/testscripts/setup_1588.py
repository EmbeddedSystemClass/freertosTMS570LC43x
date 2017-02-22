# -------------------------------------------------------------------
# IEEE 1588 setup and basic routines
#
# $Id: setup_1588.py,v 1.2 2008/09/22 23:25:23 robertst Exp $
#
# $Log: setup_1588.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.31  2008/09/18 17:13:14  dave
# Updates to use modified ALP that includes PSF fixes.
# Major cleanup of unused code.
#
# Revision 1.30  2008/08/26 14:48:31  dave
# replace master_SA and slave_SA with mac_SA.
#
# Revision 1.29  2008/06/26 15:13:27  dave
# add management support.
# update with PTP spec names for dataset variables
#
# Revision 1.28  2008/05/20 15:17:49  dave
# add IP checksum verification for PSF.
# Add temporary fixes to allow use of EPL PSF configuration routine.
# fix a couple of xem vs port naming errors.
#
# Revision 1.27  2008/05/14 15:28:56  dave
# Major updates to add subroutines, BMC algorithm.
#
# Revision 1.26  2008/04/14 17:39:31  dave
# Significant changes to support Phy Status Frames.
#
# Revision 1.25  2008/04/10 17:58:26  dave
# fix mac dest address for pdelay messages.
#
# Revision 1.24  2008/04/02 15:31:09  dave
# update to CheckPktready.
# Add BC/TC 1588 clock alignment routines.
#
# Revision 1.23  2008/04/01 17:01:05  dave
# fix MDIO checksum validation (0 vs 0xffff)
#
# Revision 1.22  2008/03/18 17:00:10  dave
# minor cleanup of DelayReqRcvd.
#
# Revision 1.21  2008/03/13 13:39:36  benb
# Added Packet_Statistics class
#
# Revision 1.20  2008/03/13 12:37:01  dave
# add subroutines for most packet handling.
#
# Revision 1.19  2008/02/08 09:42:10  dave
# change default settings for rate adjustment.
#
# Revision 1.18  2008/01/23 16:16:47  dave
# modify UDP checksum modification bytes for IPv4.
# make GetMacStats backwards compatible to Integrity platform.
#
# Revision 1.17  2008/01/15 13:22:37  dave
# add TX, RX config routines
# add GetMacStats routing
# move more config options to config class.
#
# Revision 1.16  2008/01/04 16:34:21  dave
# add option to restart slave from current state.
# change rx_ts_dly default from 210 to 205.
#
# Revision 1.14  2008/01/03 10:15:33  dave
# fix V2 PTP message for negative values of logInterval.
#
# Revision 1.13  2007/12/20 14:19:39  benb
# Added dr_extra option (default 0) to ConfigOptions
#
# Revision 1.12  2007/12/19 14:00:30  benb
# Added check_msg_len (default 1) to ConfigOptions class.
# Modified v2_Parse_Pkt to not clear v2_ok if
#   cfg.check_msg_len = 0.
#
# Revision 1.11  2007/12/19 13:32:29  benb
# Added versionPTP_en to the ConfigOptions class (default 1)
#   to control programming of PTP version in TX and RX config
#   registers.
# Modified v2_Parse_Pkt to accept PTP packets with any
#   version if cfg.versionPTP_en = 0.  In this case,
#   base v1_ok/v2_ok on cfg.v2_enable.
#
# Revision 1.10  2007/12/19 11:26:47  dave
# use ip_dest_addr for IPv4 ip_hdr instead of cfg.ipv4_dest_addr
# in Build_v2_Pkt
#
# Revision 1.9  2007/12/18 13:06:45  benb
# Warn if invalid PTP version detected.
# Provide more detail for incorrect message length
#   in v2_Parse_Pkt.
# Declare and initialize useful low-level
#   Opal Kelly functions.
#
# Revision 1.8  2007/12/12 17:07:05  benb
# Added low-level Opal-Kelly functions, and call OkFunctionInit()
#   in master and slave.
# This is useful for setting the MAC duplex mode.
#
# Revision 1.7  2007/12/11 12:26:51  benb
# Added ConfigureClkOut function, which returns ptp_clkout_period
# Changed clkout_sel_pgm to 1
#
# Revision 1.6  2007/12/11 11:07:49  benb
# Added ptp_sync_suffix to ConfigOptions class.  Added code to ensure
#   that the ptpSuffix is at least two bytes (pad with 0's if nothing
#   else) for IPv4 1-Step Sync packets.  This allows the UDP checksum
#   fix to work correctly by letting it stuff the fix into the two
#   unused bytes.
#
# Revision 1.5  2007/12/07 11:52:34  dave
# improvements to support A2.
#
# Revision 1.4  2007/11/05 15:51:17  dave
# Add VLAN tag option for PTP messages.
# fix standard deviation script if sample_list is empty.
#
# Revision 1.3  2007/10/18 16:16:49  dave
# updates for management and signalling messages.
#
# Revision 1.2  2007/09/28 13:24:38  dave
# add identity detail to v1 messages.
#
# Revision 1.1  2007/09/26 10:46:50  dave
# Initial revision
#
# Revision 1.15  2007/09/06 10:42:06  dave
# Add configuration options.
# Add L2 appendend TS.
#
# Revision 1.14  2007/08/08 15:26:30  dave
# add trigger testing support, clkout phase alignment
#
# Revision 1.13  2007/07/25 12:27:04  dave
# additional default values for register configuration.
#
# Revision 1.12  2007/07/23 16:37:52  dave
# add peer delay mechanism.
#
# Revision 1.11  2007/07/19 16:22:54  dave
# Add PCF support to MdioWrite command to allow basic scripts
# to use Phy Control Frames.
#
# Revision 1.10  2007/07/18 15:19:13  dave
# fix DisableTrigger function (use trig_csel).
#
# Revision 1.9  2007/07/18 11:29:35  dave
# add temp_rate_en, s_ts_insert, poll_link_status variables.
#
# Revision 1.8  2007/07/18 09:58:04  benb
# Added parameter "print_time_error_list", default 0, to enable printing
#   the entire Time Error List upon slave script exit.  As this task can
#   keep ALP busy for a long time, turn off the display of the list by
#   default.
#
# Revision 1.7  2007/07/17 18:14:35  dave
# add v2 specific code.
#
# Revision 1.6  2007/07/13 15:44:41  benb
# Added defaults for clock output configuration.
#
# Revision 1.5  2007/07/13 14:39:34  benb
# Added PTP page 4 write checksum checking to SetTRate1588 and
#   EnableTrigger.
#
# Revision 1.4  2007/07/13 11:31:54  benb
# Update with new ALP enumeration
# Add support for "Stop" button
#
# Revision 1.3  2007/07/12 17:17:31  dave
# add support for event checking and sync enet.
#
# Revision 1.2  2007/07/05 11:14:22  dave
# updates as of 7/5/07
#
#
#

from alp1588 import *

# -------------------------------------------------------------------
# RX Timestamp Class
class RX_Timestamp:
    ok = 0
    ts = 0
    seqID = 0
    mtype = 0
    sourceHash = 0
    checksum = 0
    missed = 0

# -------------------------------------------------------------------
# TX Timestamp Class
class TX_Timestamp:
    ok = 0
    ts = 0
    checksum = 0
    missed = 0

# -------------------------------------------------------------------
# Phy Status Frames Configuration Class
class PSF_Configuration:
    dp83640_mdl_rev = 0
    psf_hdr_data = 0x02ff
    psf_mac_sa_sel = 0
    psf_ipv4 = 1
    psf_ip_src_addr = [0x11, 0x22, 0x33, 0x44]
    psf_preamble_len = 7
    psf_endian = 0
    psf_txts_en = 0
    psf_rxts_en = 0
    psf_trig_en = 0
    psf_evnt_en = 0


# -------------------------------------------------------------------
# Trigger Configuration Class
#    contains all fields for configuring a trigger
class Trigger_Configuration:
    def __init__(self, trig_num):
        self.trig_csel = trig_num
        self.trig_pulse = 0
        self.trig_per = 0
        self.trig_if_late = 0
        self.trig_notify = 0
        self.trig_gpio = 0
        self.trig_toggle = 0

# -------------------------------------------------------------------
# Trigger Control Class
#    contains all fields for control of a trigger
class Trigger_Control:
    def __init__(self, trig_num):
        self.trig_csel = trig_num
        self.trig_time = 0L
        self.trig_init_val = 0
        self.trig_wait4rollover = 0
        self.trig_pw1 = 0
        self.trig_pw2 = 0


# -------------------------------------------------------------------
# Event Status Class - as returned by EPL
class PSF_Event_Status:
    def __init__(self):
        self.ptp_ests = 0
        self.ext_event_status_valid = 0
        self.ext_event_status = 0
        self.event_ts_sec = 0
        self.event_ts_ns = 0

# -------------------------------------------------------------------
# Event Status Class
class Event_Status:
    event_detect = 0x00
    event_num = 0x00
    event_mult = 0x00
    event_rf = 0x00
    event_ts_len = 0x00
    events_missed = 0x00
    event_count = 0x00
    ext_status = 0x00
    ts = 0


# -------------------------------------------------------------------
# Transmit Timestamp Lists
class TXTS_Lists:
    TS_list = []
    sent_list = []

# -------------------------------------------------------------------
# Receive Timestamp Lists
class RXTS_Lists:
    TS_list = []

# -------------------------------------------------------------------
# Phy Status Frames Status Lists
class PSF_Lists:
    txts = TXTS_Lists()
    rxts = RXTS_Lists()
    trig_list = []
    event_list = []
    psf_err_list = []
    pcf_read_list = []

# -------------------------------------------------------------------
# IEEE 1588 V2 constants
#
# Event mtype
mtype_sync = 0x00
mtype_delay_req = 0x01
mtype_pdelay_req = 0x02
mtype_pdelay_resp = 0x03
# General mtype
mtype_follow_up = 0x08
mtype_delay_resp = 0x09
mtype_pdelay_follow = 0x0A
mtype_announce = 0x0B
mtype_signaling = 0x0C
mtype_management = 0x0D

# Port State constants
PORT_INITIALIZING = 1
PORT_FAULTY = 2
PORT_DISABLED = 3
PORT_LISTENING = 4
PORT_PRE_MASTER = 5
PORT_MASTER = 6
PORT_PASSIVE = 7
PORT_UNCALIBRATED = 8
PORT_SLAVE = 9

# Port State names
PORT_STATE_STRING = ["", "PORT_INITIALIZING", "PORT_FAULTY", "PORT_DISABLED", "PORT_LISTENING", "PORT_PRE_MASTER", "PORT_MASTER", "PORT_PASSIVE", "PORT_UNCALIBRATED", "PORT_SLAVE"]

# delay_mechanism constants
DELAY_E2E = 1
DELAY_P2P = 2
DELAY_DISABLED = 0xFE

# Management Actions
mgnt_action = ["GET", "SET", "RESPONSE", "COMMAND", "ACKNOWLEDGE"]

class MANAGEMENT_ACTION_FIELD:
    GET = 0
    SET = 1
    RESPONSE = 2
    COMMAND = 3
    ACKNOWLEDGE = 4

# TLV Types (constants)
class TLV_TYPE:
    MANAGEMENT = 1
    MANAGEMENT_ERROR_STATUS = 2

# Management Error IDs (constants)
class MANAGEMENT_ERROR_ID:
    RESPONSE_TOO_BIG = 1
    NO_SUCH_ID = 2
    WRONG_LENGTH = 3
    WRONG_VALUE = 4
    NOT_SETABLE = 5
    NOT_SUPPORTED = 6
    GENERAL_ERROR = 0XFE

# Management Error ID strings
def mgntErrorID_str(managementErrorId):
    if (managementErrorId == 1) : return("RESPONSE_TOO_BIG")
    if (managementErrorId == 2) : return("NO_SUCH_ID")
    if (managementErrorId == 3) : return("WRONG_LENGTH")
    if (managementErrorId == 4) : return("WRONG_VALUE")
    if (managementErrorId == 5) : return("NOT_SETABLE")
    if (managementErrorId == 6) : return("NOT_SUPPORTED")
    if (managementErrorId == 0XFE) : return("GENERAL_ERROR")

# Management IDs (constants)
class MANAGEMENT_ID:
    #
    # Applicable to All nodes
    NULL = 0
    CLOCK_DESCRIPTION = 1
    USER_DESCRIPTION = 2
    SAVE_IN_NON_VOLATILE_STORAGE = 3
    RESET_NON_VOLATILE_STORAGE = 4
    INITIALIZE = 5
    FAULT_LOG = 6
    FAULT_LOG_RESET = 7
    #
    # Applicable to Ordinary/Boundary Clocks
    DEFAULT_DATA_SET = 0x2000
    CURRENT_DATA_SET = 0x2001
    PARENT_DATA_SET = 0x2002
    TIME_PROPERTIES_DATA_SET = 0x2003
    PORT_DATA_SET = 0x2004
    PRIORITY1 = 0x2005
    PRIORITY2 = 0x2006
    DOMAIN = 0x2007
    SLAVE_ONLY = 0x2008
    LOG_ANNOUNCE_INTERVAL = 0x2009
    ANNOUNCE_RECEIPT_TIMEOUT = 0x200A
    LOG_SYNC_INTERVAL = 0x200B
    VERSION_NUMBER = 0x200C
    ENABLE_PORT = 0x200D
    DISABLE_PORT = 0x200E
    TIME = 0x200F
    CLOCK_ACCURACY = 0x2010
    UTC_PROPERTIES = 0x2011
    TRACEABILITY_PROPERTIES = 0x2012
    TIMESCALE_PROPERTIES = 0x2013
    UNICAST_NEGOTIATION_ENABLE = 0x2014
    PATH_TRACE_LIST = 0x2015
    PATH_TRACE_ENABLE = 0x2016
    GRANDMASTER_CLUSER_TABLE = 0x2017
    UNICAST_MASTER_TABLE = 0x2018
    UNICAST_MASTER_MAX_TABLE_SIZE = 0x2019
    ACCEPTABLE_MASTER_TABLE = 0x201A
    ACCEPTABLE_MASTER_TABLE_ENABLED = 0x201B
    ACCEPTABLE_MASTER_TABLE_SIZE = 0x201C
    ALTERNATE_MASTER = 0x201D
    ALTERNATE_TIME_OFFSET_ENABLE = 0x201E
    ALTERNATE_TIME_OFFSET_NAME = 0x201F
    ALTERNATE_TIME_OFFSET_MAX_KEY = 0x2020
    ALTERNATE_TIME_OFFSET_PROPERTIES = 0x2021
    #
    # Applicable to Transparent Clocks
    TRANSPARENT_CLOCK_DEFAULT_DATA_SET = 0x4000
    TRANSPARENT_CLOCK_PORT_DATA_SET = 0x4001
    PRIMARY_DOMAIN = 0x4002
    #
    # Applicable to Ordinary, Boundary, and Transparent Clocks
    DELAY_MECHANISM = 0x6000
    LOG_MIN_PDELAY_REQ_INTERVAL = 0x6001

# Management ID strings (managementID)
def mgntID_str(managementId):
    if (managementId == 0) : return("NULL_MANAGEMENT")
    if (managementId == 1) : return("CLOCK_DESCRIPTION")
    if (managementId == 2) : return("USER_DESCRIPTION")
    if (managementId == 3) : return("SAVE_IN_NONVOLATILE_STORAGE")
    if (managementId == 4) : return("RESET_NON_VOLATILE_STORAGE")
    if (managementId == 5) : return("INITIALIZE")
    if (managementId == 6) : return("FAULT_LOG")
    if (managementId == 7) : return("FAULT_LOG_RESET")
    # OC and BC
    if (managementId == 0x2000) : return("DEFAULT_DATA_SET")
    if (managementId == 0X2001) : return("CURRENT_DATA_SET")
    if (managementId == 0X2002) : return("PARENT_DATA_SET")
    if (managementId == 0X2003) : return("TIME_PROPERTIES_DATA_SET")
    if (managementId == 0X2004) : return("PORT_DATA_SET")
    if (managementId == 0X2005) : return("PRIORITY1")
    if (managementId == 0X2006) : return("PRIORITY2")
    if (managementId == 0X2007) : return("DOMAIN")
    if (managementId == 0X2008) : return("SLAVE_ONLY")
    if (managementId == 0X2009) : return("LOG_ANNOUNCE_INTERVAL")
    if (managementId == 0X200A) : return("ANNOUNCE_RECEIPT_TIMEOUT")
    if (managementId == 0X200B) : return("LOG_SYNC_INTERVAL")
    if (managementId == 0X200C) : return("VERSION_NUMBER")
    if (managementId == 0X200D) : return("ENABLE_PORT")
    if (managementId == 0X200E) : return("DISABLE_PORT")
    if (managementId == 0X200F) : return("TIME")
    if (managementId == 0X2010) : return("CLOCK_ACCURACY")
    if (managementId == 0X2011) : return("UTC_PROPERTIES")
    if (managementId == 0X2012) : return("TRACEABILITY_PROPERTIES")
    if (managementId == 0X2013) : return("TIMESCALE_PROPERTIES")
    if (managementId == 0X2014) : return("UNICAST_NEGOTIATION_ENABLE")
    if (managementId == 0X2015) : return("PATH_TRACE_LIST")
    if (managementId == 0X2016) : return("PATH_TRACE_ENABLE")
    if (managementId == 0X2017) : return("GRANDMASTER_CLUSTER_TABLE")
    if (managementId == 0X2018) : return("UNICAST_MASTER_TABLE")
    if (managementId == 0X2019) : return("UNICAST_MASTER_MAX_TABLE_SIZE")
    if (managementId == 0X201A) : return("ACCEPTABLE_MASTER_TABLE")
    if (managementId == 0X201B) : return("ACCEPTABLE_MASTER_TABLE_ENABLED")
    if (managementId == 0X201C) : return("ACCEPTABLE_MASTER_MAX_TABLE_SIZE")
    if (managementId == 0X201D) : return("ALTERNATE_MASTER")
    if (managementId == 0X201E) : return("ALTERNATE_TIME_OFFSET_ENABLE")
    if (managementId == 0X201F) : return("ALTERNATE_TIME_OFFSET_NAME")
    if (managementId == 0X2020) : return("ALTERNATE_TIME_OFFSET_MAX_KEY")
    if (managementId == 0X2021) : return("ALTERNATE_TIME_OFFSET_PROPERTIES")
    # TC
    if (managementId == 0X4000) : return("TRANSPARENT_CLOCK_DEFAULT_DATA_SET")
    if (managementId == 0X4001) : return("TRANSPARENT_CLOCK_PORT_DATA_SET")
    if (managementId == 0X4002) : return("PRIMARY_DOMAIN")
    # OC, BC, TC
    if (managementId == 0X6000) : return("DELAY_MECHANISM")
    if (managementId == 0X6001) : return("LOG_MIN_PDELAY_REQ_INTERVAL")
    #
    return("")


# -------------------------------------------------------------------
# IEEE 1588 ClockQuality
#
class clockQuality:
    clockClass = 255
    clockAccuracy = 254
    offsetScaledLogVariance = 0

# -------------------------------------------------------------------
# IEEE 1588 Default Data Set
#
class default_Data_Set:
    twoStepFlag = 0
    clockIdentity = [0, 0, 0, 0, 0, 0, 0, 0]
    numberPorts = 1
    clockQuality = clockQuality()
    priority1 = 128
    priority2 = 128
    domainNumber = 0
    slaveOnly = 0


# -------------------------------------------------------------------
# IEEE 1588 Current Data Set
#
class current_Data_Set:
    stepsRemoved = 1
    offsetFromMaster = 0
    meanPathDelay = 0

# -------------------------------------------------------------------
# IEEE 1588 Parent Data Set
#
class parent_Data_Set:
    parentPortIdentity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    parentStats = 0
    observed_poslv = 0xFFFF
    observed_pcpcr = 0x7FFFFFFF
    grandmasterIdentity = [0, 0, 0, 0, 0, 0, 0, 0]
    grandmasterClockQuality = clockQuality()
    grandmasterPriority1 = 255
    grandmasterPriority2 = 255


# -------------------------------------------------------------------
# IEEE 1588 Time Properties Data Set
#
class time_properties_Data_Set:
    currentUtcOffset = 0
    currentUtcOffsetValid = 0
    leap59 = 0
    leap61 = 0
    timeTraceable = 0
    frequencyTraceable = 0
    ptpTimescale = 0
    timeSource = 0xA0

# -------------------------------------------------------------------
# IEEE 1588 Port Data Set
#
class port_Data_Set:
    portIdentity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    portState = PORT_INITIALIZING
    logMinDelayReqInterval = 0
    peerMeanPathDelay = 0
    logAnnounceInterval = 1
    announceReceiptTimeout = 3
    logSyncInterval = 0
    delayMechanism = DELAY_E2E
    logMinPdelayReqInterval = 0
    versionNumber = 2


# -------------------------------------------------------------------
# IEEE 1588 Foreign Master Data Set Entry
#
class foreign_Master_Data_Set:
    def __init__(self):
        self.sourcePortIdentity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.grandmasterPriority1 = 0
        self.grandmasterClockQuality = clockQuality()
        self.grandmasterPriority2 = 0
        self.grandmasterIdentity = [0, 0, 0, 0, 0, 0, 0, 0]
        self.stepsRemoved = 0
        self.timeSource = 0
        self.currentUtcOffset = 0
        self.flagField = 0
        self.receivePortIdentity = 0
        self.AnnounceMessages = [1, 0, 0, 0]


# -------------------------------------------------------------------
# Port Pdelay_Req state info
# -- tracks state of Pdelay_Req mechanism for initiator
#
class Pdelay_Req_state:
    sent = 0
    seqID = 0
    resp_rcvd = 0
    resp_2step = 0
    resp_corr = 0
    follow_corr = 0
    wait4TS = 0
    next_pdelay_req = 0
    mean_pdly_req_pd = 0
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0

# -------------------------------------------------------------------
# Port Pdelay_Resp state info
# -- tracks state of Pdelay_Req mechanism for responder
#
class Pdelay_Resp_state:
    sent = 0
    seqID = 0
    sent_time = 0
    req_rcvd = 0
    wait4TS = 0
    t2 = 0
    t3 = 0

# -------------------------------------------------------------------
# Slave Status variables
class slave_Status:
    sync_complete = 0
    sync_rcvd = 0
    sync_rcvd_time = 0
    sync_rcvd_cf = 0
    delay_req_wait4TS = 0
    two_step = 0
    sync_sent_time = 0
    delay_sent_time = 0
    prev_sync_sent = 0
    prev_sync_rcvd = 0
    next_delay_req = 0
    mean_dly_req_pd = 0
    follow_cf = 0
    follow_rcvd = 0
    sync_seqID = 0
    log_mean_sync_interval = 0
    syntonized = 0

# -------------------------------------------------------------------
# Clock Status
# -- tracks state of PTP clock.  This is shared across multiple ports
#
class clock_Status:
    def __init__(self):
        self.rate_1588 = 0
        self.num_syncs = 0

# -------------------------------------------------------------------
# Master Status variables
class master_Status:
    sync_sent_time = 0
    next_sync_time = 0
    sync_wait4TS = 0

# -------------------------------------------------------------------
# Configuration/Mode options
#
class ConfigOptions:
    def __init__(self):
        self.defaultDS = default_Data_Set()
        self.currentDS = current_Data_Set()
        self.parentDS = parent_Data_Set()
        self.timePropertiesDS = time_properties_Data_Set()
        self.portDS = port_Data_Set()
        self.foreignMasterDS = []
        self.GM_timePropertiesDS = time_properties_Data_Set()
        self.port_name = ""
    dp83640_mdl_rev = 0
    v2_enable = 1
    versionPTP_en = 1
    check_msg_len = 1
    sync_1step = 1
    dr_insert = 0
    dr_insert_enabled = 0
    tx_chk_1step = 1
    one_step = 1
    ipv4_en = 0
    ipv6_en = 0
    l2_enet = 1
    alt_mast_dis = 0
    byte0_mask = 0xf8
    byte0_data = 0x00
    rx_byte0_mask = 0xf8
    rx_byte0_data = 0x00
    domain_en = 0
    user_ip_en = 0
    user_ip_addr = 0
    ip1588_en0 = 1
    ip1588_en1 = 1
    ip1588_en2 = 1
    acc_udp = 0
    acc_crc = 0
    ts_min_ifg = 0x0C
    ts_insert = 1
    ts_append = 0
    ts_ins_sec_en = 1
    ts_ins_sec_len = 0
    ts_ins_ns_off = 36
    ts_ins_sec_off = 33  
    ptp_etype = 0xF788
    rx_hash_en = 0
    ptp_rxhash = 0
    announce_seqID = 0
    sync_seqID = 0
    gen_seqID = 0
    delayreq_seqID = 0
    management_seqID = 0
    dr_extra = 0
    pdelayreq_seqID = 0
    all_flags = 0x00
    sync_flags = 0x00
    followup_flags = 0x00
    sync_corr_fld = 0
    epoch = 0
    mac_DA = [0x01, 0x1B, 0x19, 0x00, 0x00, 0x00]
    pdelay_DA = [0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E]
    mac_SA = [0x08, 0x00, 0x17, 0x00, 0x00, 0x01]
    l2_etype = 0x88F7
    ipv4_src_addr = [100, 100, 100, 1]
    ipv4_dest_addr = [224, 0, 1, 129]
    ipv4_pdelay_dest_addr = [224, 0, 0, 107]
    ipv4_mac_DA = [0x01, 0x00, 0x5E, 0x00, 0x01, 0x81]
    ipv4_pdelay_mac_DA = [0x01, 0x00, 0x5E, 0x00, 0x00, 0x6B]
    ipv4_ID = 0
    ipv4_ttl = 1
    ipv4_udp_chksum_en = 0
    ipv6_src_addr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 100, 100, 100, 1]
    ipv6_dest_addr = [0xFF, 0x0E, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x01, 0x81]
    ipv6_pdelay_dest_addr = [0xFF, 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x00, 0x6B]
    udp_src_port = 0
    v1_srcPortID = [0x00, 0x01]
    v1_grandmaster_stats = []
    vlan_en = 0
    vlan_pri = 0
    vlan_vid = 0
    mdio_cksum_en = 1
    # Management node support
    startingBoundaryHops = 255
    # Clock Description
    user_description = ""
    
# -------------------------------------------------------------------
# Options for IEEE 1588 v2 PTP Header generation
#
class ptpHeader_Class:
    transportSpecific = 0
    domainNumber = 0
    sourcePortIdentity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    logInterval = 0
    correctionField = [0, 0, 0, 0, 0, 0, 0, 0]


# -------------------------------------------------------------------
# IEEE 1588 v2 Packet Status
#
class v2_Packet_Status:
    v2_1588_ok = 0
    ipv4_ok = 0
    ipv6_ok = 0
    l2_enet_ok = 0
    delay_req_ok = 0
    sync_ok = 0
    delay_resp_ok = 0
    follow_ok = 0
    pdelay_req_ok = 0
    pdelay_resp_ok = 0
    pdelay_follow_ok = 0
    announce_ok = 0
    signaling_ok = 0
    management_ok = 0
    packet_timestamp = 0
    messageType = 0
    trans_specific = 0
    versionPTP = 0
    messageLength = 0
    domain = 0
    src_hash = 0
    seqID = 0
    two_step = 0
    corr_field = 0
    logInterval = 0
    ptp_offset = 0
    sync_originTS = []
    rcvdTS = []
    header = []
    body = []
    suffix = []
    vlan_tag = 0
    vlan_tci = 0


# -------------------------------------------------------------------
# Packet Statistics
#
class Packet_Statistics:
    # MAC header
    DA              = [0XFF, 0XFF, 0XFF, 0XFF, 0XFF, 0XFF]
    SA              = [0x08, 0x00, 0x17, 0x0B, 0x6B, 0x0F]
    # [Data start, data end, data]
    txByteCnt       = [14, 18, 0]
    txPktCnt        = [18, 20, 0]
    rxByteCnt       = [26, 30, 0]
    rxPktCnt        = [30, 32, 0]
    rxCrcErrCnt     = [32, 34, 0]
    rxRuntPkt       = [34, 36, 0]
    rxErrorPkt      = [36, 38, 0]


# -------------------------------------------------------------------
# Int8
# Convert Uint8 to Int8
def Int8(input_uint8):
    if (input_uint8 >= 128):
        input_uint8 -= 256
    return(input_uint8)
#
# End of Int8 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# UInt8
# Convert int8 to UInt8
def UInt8(input_int8):
    return(input_int8 & 0xff)
#
# End of Int8 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# List_to_Uint16
# Convert 2 octet list to Uint16
def List_to_Uint16(input_list):
    return((input_list[0] << 8) | input_list[1])
#
# End of List_to_Uint16 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Uint16_to_List
# Convert Uint16 to 2 octet list
def Uint16_to_List(input_uint16):
    return([(input_uint16 >> 8), (input_uint16 & 0xff)])
#
# End of Uint16_to_List routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# List_to_Uint32
# Convert 4 octet list to Uint32
def List_to_Uint32(input_list):
    return((input_list[0] << 24) | (input_list[1] << 16) | (input_list[2] << 8) | input_list[3])
#
# End of List_to_Uint32 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Uint32_to_List
# Convert Uint32 to 4 octet list
def Uint32_to_List(input_uint32):
    return([((input_uint32 >> 24) & 0xff), ((input_uint32 >> 16) & 0xff), ((input_uint32 >> 8) & 0xff), (input_uint32 & 0xff)])
#
# End of Uint32_to_List routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Time_Interval
# Convert signed integer to TimeInterval list (48-bit ns, 16 bit subns)
#
def Time_Interval(time_subns):
    #if (time_subns < 0):
    #    time_subns = time_subns + (2**64)
    time_list = [time_subns & 0xff]
    for cnt in range(7):
        time_subns = time_subns >> 8
        time_list = [time_subns & 0xff] + time_list
    return(time_list)
#
# End of Time_Interval routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Convert_Time_Interval
# Convert TimeInterval list to signed 64-bit value (units of 2-16 ns)
#
def Convert_Time_Interval(time_int_list):
    time_subns = (long(time_int_list[0]) << 56) + (long(time_int_list[1]) << 48) + (long(time_int_list[2]) << 40) + (long(time_int_list[3]) << 32) + (long(time_int_list[4]) << 24) + (time_int_list[5] << 16) + (time_int_list[6] << 8) + (time_int_list[7])
    if (time_subns >= (2**63)):
        time_subns = time_subns - (2**64)
    return(time_subns)
#
# End of Convert_Time_Interval routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# StdDev script
#
def StdDev(sample_list, verbose):
    from math import sqrt
    #
    list_len = len(sample_list)
    if (list_len == 0):
        mean_error = 0
        sync_std_dev = 0
    else:
        sum_error = 0.0
        for cnt in range(list_len):
            sum_error = sum_error + (sample_list[cnt])
        mean_error = sum_error / list_len
        sum_error_sq = 0.0
        for cnt in range(list_len):
            sum_error_sq = sum_error_sq + ((sample_list[cnt] - mean_error)**2)
        sync_std_dev = sqrt(sum_error_sq/list_len)
    if verbose:
        print "Mean: %f" % (mean_error)
        print "Standard Deviation: %f" % (sync_std_dev)
    return [mean_error, sync_std_dev]

#
#
# End of StdDev routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# AvgList script
#
def AvgList(sample_list, max_length, verbose):
    #
    # Returns average of the last max_length values in a list
    # If list is less than max_length, averages all values in the list
    list_len = len(sample_list)
    list_avg = 0
    if (list_len != 0):
        if (list_len <= max_length):
            for cnt in range(list_len):
                list_avg = list_avg + sample_list[cnt]
            list_avg = list_avg/list_len
        else:
            for cnt in range(max_length):
                list_avg = list_avg + sample_list[list_len - cnt - 1]
            list_avg = list_avg/max_length
    if (verbose):
        print "AvgList: ", list_avg
    return (list_avg)

#
#
# End of AvgList routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# Incr_Word16 script
#
def Incr_Word16(word16_val):
    #
    # Increments 16-bit value, with rollover to 0
    return_val = (word16_val + 1) & 0xffff
    return (return_val)

#
#
# End of Incr_Word16 routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# 1588 Reset_PTP script
#
def Reset_PTP(xem, phyAddr, verbose):
    #
    if (verbose):
        print "Issuing PTP Reset"
    phy_model_rev = MdioRead(xem, phyAddr, PHYID2, 0)
    if (phy_model_rev == 0x5ce0):
        MdioWrite(xem, phyAddr, CGCR, DIS_CLK125_GATE, 0)
        MdioWrite(xem, phyAddr, PTP_CTL, PTP_RESET, 0)
        MdioWrite(xem, phyAddr, PTP_CTL, 0, 0)
        MdioWrite(xem, phyAddr, CGCR, 0, 0)
    else:
        MdioWrite(xem, phyAddr, PTP_CTL, PTP_RESET, 0)
        MdioWrite(xem, phyAddr, PTP_CTL, 0, 0)
    #
#
#
# End of 1588 Reset_PTP routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 GetEventTS script
#
def GetEventTS(xem, phyAddr, verbose):
    #
    mdio_read_val = MdioRead(xem, phyAddr, PTP_EDATA, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    mdio_read_val = MdioRead(xem, phyAddr, PTP_EDATA, 0)
    timestamp = [((mdio_read_val >> 8) & 0x3f), (mdio_read_val & 0xff)] + timestamp
    mdio_read_val = MdioRead(xem, phyAddr, PTP_EDATA, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + timestamp
    mdio_read_val = MdioRead(xem, phyAddr, PTP_EDATA, 0)
    timestamp = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + timestamp
    if(verbose):
        print "   Event Timestamp = ", timestamp[0:8]
    #
    return (timestamp)

#
#
# End of 1588 GetEventTS routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 GetEventTS_PSF script
#
def GetEventTS_PSF(current_event, event_list, verbose):
    #
    current_event.event_detect = event_list.ptp_ests & 0x01
    current_event.event_num = (event_list.ptp_ests >> 2) & 0x7
    current_event.event_mult = (event_list.ptp_ests >> 1) & 0x1
    current_event.event_rf = (event_list.ptp_ests >> 5) & 0x1
    current_event.event_ts_len = ((event_list.ptp_ests >> 6) & 0x3) + 1
    current_event.events_missed = (event_list.ptp_ests >> 8) & 0x7
    current_event.event_count = 0
    if (current_event.event_mult):
        current_event.ext_status = event_list.ext_event_status
        bit_num = 0 
        while (bit_num < 16):
            current_event.event_count += ((current_event.ext_status >> bit_num) & 1)
            bit_num = bit_num + 2
    else:
        current_event.ext_status = 0
        current_event.event_count = 1
    if (current_event.event_ts_len == 4):
        current_event.ts = 0
    if (current_event.event_ts_len == 3):
        current_event.ts = current_event.ts & 0xffff000000000000
    if (current_event.event_ts_len == 2):
        current_event.ts = current_event.ts & 0xffffffff00000000
    if (current_event.event_ts_len == 1):
        current_event.ts = current_event.ts & 0xffffffffffff0000
    current_event.ts |= (event_list.event_ts_sec * 10**9) + event_list.event_ts_ns
    if(debug_event):
        print "   Event #%d Timestamp = %s"% (current_event.event_num, Print_TS(current_event.ts))
    #
    return (current_event.event_detect)

#
#
# End of 1588 GetEventTS_PSF routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 SaveErrorList script
#
def SaveErrorList(Time_Error_list, fname):
    f=open(fname, 'w')
    for i in range(len(Time_Error_list)):
        value = str(Time_Error_list[i]) + '\n'
        f.write(value)
    f.close()

#
#
# End of SaveErrorList routine
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
# 1588 SetTRate1588 script
#
def SetTRate1588(xem, phyAddr, rate_1588, verbose):
    # Clear the write checksum register
    if (not xem.pcf_en):
        MdioRead(xem,phyAddr,PTP_WRCKSUM,0)
    #
    # Read MDIO register
    rate = abs(rate_1588)
    write_data = 0x4000 | (int(rate >> 16) & 0x7fff)
    if (rate_1588 < 0):
        write_data = write_data | 0x8000
    oc_list = [write_data]
    MdioWrite(xem, phyAddr, PTP_RATEH, write_data, 0)
    write_data = int(rate & 0xffff)
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_RATEL, write_data, 0)
    if(verbose):
        print "Set Temporary 1588 Rate = ", rate_1588
    # Read/Validate checksum
    if (not xem.pcf_en):
        wrcksum = MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [wrcksum])):
            print "FAILED: SetTRate1588 write checksum failure"
            print "  checksum data:", oc_list
            print "  write checksum value: %x" % (wrcksum)
            return 1
        else:
            return 0
    else:
        return 0
    #

#
#
# End of 1588 SetTRate1588 routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 GetRxTimestamp script
#
#class RX_Timestamp:
#    ts = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
#    seqID = [0, 0]
#    mtype = 0
#    sourceHash = 0
#    checksum = [0]
#    missed = 0
def GetRxTimestamp_cksum(xem, phyAddr, rx_timestamp, verbose):
    #
    # Clear checksum register
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RDCKSUM, 0)
    #
    # Read Timestamp
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = [mdio_read_val]
    rx_timestamp.ts = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = oc_list + [mdio_read_val]
    rx_timestamp.missed = mdio_read_val >> 14
    mdio_read_val = mdio_read_val & 0x3fff
    rx_timestamp.ts = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + rx_timestamp.ts
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = oc_list + [mdio_read_val]
    rx_timestamp.ts = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + rx_timestamp.ts
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = oc_list + [mdio_read_val]
    rx_timestamp.ts = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + rx_timestamp.ts
    #
    # Get Sequence ID
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = oc_list + [mdio_read_val]
    rx_timestamp.seqID = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    #
    # Get mType and sourceHash
    mdio_read_val = MdioRead(xem, phyAddr, PTP_RXTS, 0)
    oc_list = oc_list + [mdio_read_val]
    rx_timestamp.mtype = (mdio_read_val >> 12)
    rx_timestamp.sourceHash = (mdio_read_val & 0xfff)
    #
    if(verbose):
        print "Receive Timestamp = ", rx_timestamp.ts
        print "Receive Sequence ID     = ", rx_timestamp.seqID
        print "Receive mType           = ", rx_timestamp.mtype
        print "Receive sourceHash      = ", rx_timestamp.sourceHash
    # Read/Validate checksum
    rx_timestamp.checksum = MdioRead(xem, phyAddr, PTP_RDCKSUM, 0)
    if (not ValidateMdioCksum(oc_list + [rx_timestamp.checksum])):
        print "FAILED:  RX Timestamp read checksum failure"
        print "  checksum data:", oc_list
        print "  read checksum value: ", rx_timestamp.checksum
        timestamp_ok = 0
    else:
        timestamp_ok = 1
    #
    return (timestamp_ok)

#
#
# End of 1588 GetRxTimestamp routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 GetRxTimestamp script
#
def GetRxTimestamp(xem, phyAddr, chksum_en, verbose):
    #
    # Clear checksum register
    if (chksum_en):
        mdio_read_val = MdioRead(xem, phyAddr, PTP_RDCKSUM, 0)
    #
    # Read Timestamp
    oc_list = []
    for cnt in range(7):
        oc_list += [MdioRead(xem, phyAddr, PTP_RXTS, 0)]
    # initialize receive timestamp class
    rx_timestamp = RX_Timestamp()
    #
    # Get Timestamp
    timestamp = [(oc_list[0] >> 8), (oc_list[0] & 0xff)]
    timestamp = [((oc_list[1] & 0x3fff) >> 8), (oc_list[1] & 0xff)] + timestamp
    timestamp = [(oc_list[2] >> 8), (oc_list[2] & 0xff)] + timestamp
    timestamp = [(oc_list[3] >> 8), (oc_list[3] & 0xff)] + timestamp
    rx_timestamp.ts = TStoNS(timestamp)
    #
    # Get timestamp Missed value
    rx_timestamp.missed = oc_list[1] >> 14
    #
    # Get Sequence ID
    rx_timestamp.seqID = oc_list[4]
    #
    # Get mType and sourceHash
    rx_timestamp.mtype = (oc_list[5] >> 12)
    rx_timestamp.sourceHash = (oc_list[5] & 0xfff)
    #
    if(verbose):
        print "Receive Timestamp = ", Print_TS(rx_timestamp.ts)
        print "Receive Sequence ID     = ", rx_timestamp.seqID
        print "Receive mType           = ", rx_timestamp.mtype
        print "Receive sourceHash      = ", rx_timestamp.sourceHash
    # Read/Validate checksum
    rx_timestamp.ok = 1
    if (chksum_en):
        rx_timestamp.checksum = MdioRead(xem, phyAddr, PTP_RDCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [rx_timestamp.checksum])):
            print "FAILED:  RX Timestamp read checksum failure"
            print "  checksum data:", oc_list
            print "  read checksum value: ", rx_timestamp.checksum
            rx_timestamp.ok = 0
    #
    return (rx_timestamp)

#
#
# End of 1588 GetRxTimestamp routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 ConfigureClkOut routine
#
#
def ConfigureClkOut(xem, cfg, phyAddr, verbose):
    #
    # Make sure CLK_OUT is not disabled in PHYCR2
    phycr2_read = MdioRead(xem, phyAddr, PHYCR2, verbose)    
    MdioWrite(xem, phyAddr, PHYCR2, (phycr2_read & (~CLK2MAC_DISABLE)), verbose)
    ptp_clk_ctl_val = cfg.clkout_div_by_n
    if (not cfg.clkout_en):
        if (verbose):
            print "Disabling PTP Clock output"
        ptp_clk_ctl_val &= ~PTP_CLKOUT_EN
    else:
        if (verbose):
            print "Enabling PTP Clock output:"
        ptp_clk_ctl_val |= PTP_CLKOUT_EN
        if (cfg.clkout_sel_pgm):
            if (verbose):
                print "   Source: PGM"
            ptp_clk_ctl_val |= PTP_CLKOUT_SEL
        else:
            if (verbose):
                print "   Source: FCO"
            ptp_clk_ctl_val &= ~PTP_CLKOUT_SEL
        if (cfg.clkout_spd):
            if (verbose):
                print "   I/O speed: Turbo"
            ptp_clk_ctl_val |= PTP_CLKOUT_SPD
        else:
            if (verbose):
                print "   I/O speed: Normal"
            ptp_clk_ctl_val &= ~PTP_CLKOUT_SPD
        if (verbose):
            print "   Divide-by: ", cfg.clkout_div_by_n
    MdioWrite(xem, phyAddr, PTP_CLK_CTL, ptp_clk_ctl_val, verbose)
    ptp_clkout_period = cfg.clkout_div_by_n * 4
    return(ptp_clkout_period)
    

#
# End of ConfigureClkOut routine
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 ConfigureTrigger routine
#
def ConfigureTrigger(xem, phyAddr, trig_pulse, trig_per, trig_if_late, trig_notify, trig_gpio, trig_csel, verbose):
    #
    if(verbose):
        print ""
        print "Configuring Trigger: ", trig_csel
    trig_cfg_data = (trig_pulse << 15) | (trig_per << 14) | (trig_if_late << 13) | (trig_notify << 12)
    
    trig_cfg_data = trig_cfg_data | (trig_gpio << 8) | (trig_csel << 1) | 0x1
    MdioWrite(xem, phyAddr, PTP_TRIG, trig_cfg_data, 0)
    return (trig_cfg_data)
#
#
# End of 1588 ConfigureTrigger routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 ConfigTrig routine
#
def ConfigTrig(xem, phyAddr, trig_config, verbose):
    #
    if(verbose):
        print "Configuring Trigger: ", trig_config.trig_csel
    trig_cfg_data = (trig_config.trig_pulse << 15) | (trig_config.trig_per << 14) | (trig_config.trig_if_late << 13) | (trig_config.trig_notify << 12)
    
    trig_cfg_data = trig_cfg_data | (trig_config.trig_gpio << 8) | (trig_config.trig_toggle << 7) | (trig_config.trig_csel << 1) | 0x1
    MdioWrite(xem, phyAddr, PTP_TRIG, trig_cfg_data, 0)
    return (trig_cfg_data)

#
#
# End of 1588 ConfigTrig routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 EnableTrigger routine
#
def EnableTrigger(xem, phyAddr, trig_csel, time_1588, trig_pw1, trig_pw2, verbose):
    # Clear the write checksum
    if (not xem.pcf_en):
        MdioRead(xem,phyAddr,PTP_WRCKSUM,verbose)
    if(verbose):
        print "Enabling Trigger: ", trig_csel
    write_data = (0x0040 | (trig_csel << 10))
    oc_list = [write_data]
    MdioWrite(xem, phyAddr, PTP_CTL, write_data, 0)
    write_data = (time_1588[6]<<8) + time_1588[7]
    oc_list += [write_data]
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
    # write pulsewidth1
    write_data = (trig_pw1 & 0xffff)
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (trig_pw1 >> 16) & 0xffff
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    # write pulsewidth2
    if (trig_csel < 2):
        write_data = (trig_pw2 & 0xffff)
        oc_list += [write_data]
        MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
        write_data = (trig_pw2 >> 16) & 0xffff
        oc_list += [write_data]
        MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    # Read/Validate checksum
    if (not xem.pcf_en):
        wrcksum = MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [wrcksum])):
            print "FAILED:  EnableTrigger write checksum failure"
            print "  checksum data:", oc_list
            print "  write checksum value: %x" % wrcksum
            return 1
        else:
            return 0
    else:
        return 0


#
#
# End of 1588 EnableTrigger routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 EnableTrig routine
#
def EnableTrig(xem, phyAddr, trig_control, verbose):
    # Clear the write checksum
    if (not xem.pcf_en):
        MdioRead(xem,phyAddr,PTP_WRCKSUM,verbose)
    if(verbose):
        print "Enabling Trigger: ", trig_control.trig_csel
    trig_time = NStoTS(trig_control.trig_time)
    write_data = (0x0040 | (trig_control.trig_csel << 10))
    oc_list = [write_data]
    MdioWrite(xem, phyAddr, PTP_CTL, write_data, 0)
    write_data = (trig_time[6]<<8) + trig_time[7]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    # Upper ns value includes initial value and wait4rollover control
    write_data = (trig_control.trig_init_val << 15) + (trig_control.trig_wait4rollover << 14)
    write_data += (trig_time[4]<<8) + trig_time[5]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (trig_time[2]<<8) + trig_time[3]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (trig_time[0]<<8) + trig_time[1]
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    # write pulsewidth1
    write_data = (trig_control.trig_pw1 & 0xffff)
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    write_data = (trig_control.trig_pw1 >> 16) & 0xffff
    oc_list += [write_data]
    MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    if (trig_control.trig_csel < 2):
        # write pulsewidth2
        write_data = (trig_control.trig_pw2 & 0xffff)
        oc_list += [write_data]
        MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
        write_data = (trig_control.trig_pw2 >> 16) & 0xffff
        oc_list += [write_data]
        MdioWrite(xem, phyAddr, PTP_TDR, write_data, 0)
    # Read/Validate checksum
    if (not xem.pcf_en):
        wrcksum = MdioRead(xem, phyAddr, PTP_WRCKSUM, 0)
        if (not ValidateMdioCksum(oc_list + [wrcksum])):
            print "FAILED:  EnableTrigger write checksum failure"
            print "  checksum data:", oc_list
            print "  write checksum value: %x" % wrcksum
            return 1
        else:
            return 0
    else:
        return 0


#
#
# End of 1588 EnableTrig routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 EnableTriggerNow routine
#
def EnableTriggerNow(xem, phyAddr, trig_control, trig_offset, verbose):
    # Enable Trigger at least 1sec from current time.
    # trig_offset value provides offset from the next second value
    curr_time = TStoNS(GetTime1588(xem, phyAddr, verbose))
    trig_time_sec = (curr_time / (10**9)) + 2
    trig_control.trig_time = (trig_time_sec * (10**9)) + trig_offset
    EnableTrig(xem, phyAddr, trig_control, verbose)

#
# End of 1588 EnableTriggerNow routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 ReadTrigger routine
#
def ReadTrigger(xem, phyAddr, trig_csel, verbose):
    #
    if(verbose):
        print "Reading Trigger: ", trig_csel
    MdioWrite(xem, phyAddr, PTP_CTL, (0x0080 | (trig_csel << 10)), 0)
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)]
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    mdio_read_val = MdioRead(xem, phyAddr, PTP_TDR, 0)
    time_1588 = [(mdio_read_val >> 8), (mdio_read_val & 0xff)] + time_1588
    # read pulsewidth1
    trig_pw1 = MdioRead(xem, phyAddr, PTP_TDR, 0)
    trig_pw1 = trig_pw1 | (MdioRead(xem, phyAddr, PTP_TDR, 0) << 16)
    # read pulsewidth2
    if (trig_csel < 2):
        trig_pw2 = MdioRead(xem, phyAddr, PTP_TDR, 0)
        trig_pw2 = trig_pw2 | (MdioRead(xem, phyAddr, PTP_TDR, 0) << 16)
    else:
        trig_pw2 = 0
    if (verbose):
        print "Trig time = ", time_1588
        print "Trig_pw1  = ", trig_pw1
        print "Trig_pw2  = ", trig_pw2
    return (time_1588 + [trig_pw1, trig_pw2])

#
#
# End of 1588 ReadTrigger routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 DisableTrigger routine
#
def DisableTrigger(xem, phyAddr, trig_csel, verbose):
    #
    if(verbose):
        print "Disabling Trigger: ", trig_csel
    MdioWrite(xem, phyAddr, PTP_CTL, ((trig_csel << 10) | TRIG_DIS), 0)

#
#
# End of 1588 DisbleTrigger routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 DebugEnable routine
#
def DebugEnable(xem, phyAddr, ptp_testsel, verbose):
    #
    if(verbose):
        print ""
        print "Setting PTP Debug Test select: ", ptp_testsel
    #MdioWrite(xem, phyAddr, PAGESEL, 1, 0)
    MdioWrite(xem, phyAddr, TST_CTRL, (ptp_testsel << 6), 0)
    #MdioWrite(xem, phyAddr, PAGESEL, 4, 0)

#
#
# End of 1588 DebugEnable routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 DebugTrigger routine
#
def DebugTrigger(xem, phyAddr, verbose):
    #
    if(verbose):
        print ""
        print "Enabling Trigger Debug outputs"
    DebugEnable(xem, phyAddr, 7, verbose)

#
#
# End of 1588 DebugTrigger routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Gen_Src_Hash script
#
def Gen_Src_Hash(src_hash_data, verbose):
    #    
    # Generate Source Hash value using CRC on the byte data
    # in src_hash_data
    #
    pres_crc_lo = 0xffff
    pres_crc_hi = 0xffff
    for i in range(len(src_hash_data)):
        crc_byte_data = src_hash_data[i]
        crc_bit = 0
        for crc_bit in range(8):
            pres_crc_31 = ((pres_crc_hi >> 15) & 1)
            pres_crc_15 = ((pres_crc_lo >> 15) & 1)
            pres_crc_hi = (((pres_crc_hi << 1) | pres_crc_15) & 0xffff)
            pres_crc_lo = ((pres_crc_lo << 1) & 0xffff)
            crc_bit_data = ((crc_byte_data & 1) ^ pres_crc_31)
            if (crc_bit_data):
                pres_crc_lo = (pres_crc_lo ^ 0x1DB7)
                pres_crc_hi = (pres_crc_hi ^ 0x04C1)
            crc_byte_data = (crc_byte_data >> 1)
    src_hash_val = (pres_crc_hi >> 4) & 0x0fff
    if (verbose):
        print "Computed Source Hash Value = ", src_hash_val
    return (src_hash_val)

#
#
# End of Gen_Src_Hash routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 MDIO Write through PCF script
#
def AlpMdioWrite_PCF(phyAddr, regAddr, writeData, verbose):
    #
    pageSel = regAddr >> 8
    address = regAddr & 0xff
    #
    pcf_list = [0x40 | (phyAddr << 1) | (pageSel >> 3)]
    pcf_list = pcf_list + [((pageSel & 0x7) << 5) | address] 
    pcf_list = pcf_list + [(writeData >> 8), (writeData & 0xff)]
    #
    if(verbose):
        print "PCF register write: [%x %x %x %x]" % (pcf_list[0], pcf_list[1], pcf_list[2], pcf_list[3])
    return (pcf_list)

#
#
# End of 1588 MDIO Write through PCF routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Loop_Calibrate script
#
def Loop_Calibrate(xem, phyAddr, pkt_addr, pkt_len):
    # Calibrate Transmit to Receive Delay with loopback plug
    # Should be run after Tx and Rx initialized properly to send a packet
    rxcfg0_val = (IP1588_EN2 | IP1588_EN1 | IP1588_EN0 | RX_IPV4_EN | RX_PTP_VER1 | RX_TS_EN)
    #MdioWrite(xem, phyAddr, PAGESEL, 0x0005, 0)
    
    MdioWrite(xem, phyAddr, PTP_RXCFG0, rxcfg0_val, 0)
    SendTxPkt(xem, pkt_addr, pkt_len, 0)
    #MdioWrite(xem, phyAddr, PAGESEL, 0x0004, 0)
    ptp_sts_val = MdioRead(xem, phyAddr, PTP_STS, 0)
    if (ptp_sts_val & PTP_TXTS_RDY):
        tx_ts = GetTxTimestamp(xem, phyAddr, 0)
        txts_ok = 1
    else:
        print "FAILED:  Transmit TS not ready"
        txts_ok = 0
    if (ptp_sts_val & PTP_RXTS_RDY):
        rx_timestamp = RX_Timestamp()
        rxts_ok = GetRxTimestamp_cksum(xem, phyAddr, rx_timestamp, 0)
        rx_ts = rx_timestamp.ts
    else:
        print "FAILED:  Receive TS not ready"
        rxts_ok = 0
    if (rxts_ok & txts_ok):
        ts_diff = TStoNS(rx_ts) - TStoNS(tx_ts)
        print "Timestamp Difference = ", ts_diff
    #
    return (ts_diff)

#
#
# End of 1588 Loop_Calibrate routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 PSF_packet script
#
def PSF_packet(psf_config, rxpkt_buf, psf_list):
    # Evaluate packet to determine if PSF packet
    # Updates psf_list with PSF commands from packet
    psf_ok = rxpkt_buf[0:14] == psf_config.psf_exp_mac_hdr
    if (psf_ok & psf_config.psf_ipv4):
            # verify IP checksum (warning only at this point)
            ip_hdr = rxpkt_buf[14:34]
            if (ones_comp_chksum(ip_hdr)):
                print "WARNING:  PSF Packet has IP checksum error"
            # check IP Header
            exp_ip_length = len(rxpkt_buf) - 18
            ip_id = rxpkt_buf[18:20]
            #print "... Checking for PSF packet"
            ip_chksum = rxpkt_buf[24:26]
            exp_ip_hdr = [0x45, 0, 0, exp_ip_length] + ip_id + [0, 0, 1, 0x11] + ip_chksum + psf_config.psf_ip_src_addr + [0xE0, 0x00, 0x01, 0x81]
            if (exp_ip_hdr != ip_hdr):
                print "ERROR:  Phy Status Frame: IP Header does not match"
                psf_ok = 0
            if (psf_ok):
                # check UDP Header
                exp_udp_len = exp_ip_length - 20
                if (psf_config.dp83640_mdl_rev == 0):
                    exp_udp_hdr = [0x3f, 0x01, 0x3f, 0x01, 0x00, exp_udp_len, 0x00, 0x00]
                else:
                    exp_udp_hdr = [0x01, 0x3f, 0x01, 0x3f, 0x00, exp_udp_len, 0x00, 0x00]
                if (exp_udp_hdr != rxpkt_buf[34:42]):
                    print "ERROR in Phy Status Frame: UDP header does not match"
                    psf_ok = 0
            ptp_offset = 42
    else:
            ptp_offset = 14
    if (psf_ok):
            # check PTP header 1st two bytes
            if (rxpkt_buf[ptp_offset:ptp_offset+2] != psf_config.psf_ptp_hdr):
                print "ERROR:  Phy Status Frame: PTP header does not match"
                psf_ok = 0
    if (psf_ok):
        if (verbose):
            print "PSF Packet detected"
        # Parse packet for commands
        list_done = 0
        sts_ptr = ptp_offset + 2
        while (not list_done):
            if (not psf_config.psf_endian):
                sts_tmp = ((rxpkt_buf[sts_ptr] << 8) | rxpkt_buf[sts_ptr+1])
            else:
                sts_tmp = (rxpkt_buf[sts_ptr] | (rxpkt_buf[sts_ptr+1] << 8))
            sts_type = (sts_tmp >> 12)
            sts_type_ext = (sts_tmp & 0xfff)
            if ((sts_type == 0) | (sts_type > 6)):
                list_done = 1
            else:
                sts_len = 2    # type 3 or 6
                if (sts_type == 1):
                    sts_len = 5
                if (sts_type == 2):
                    sts_len = 7
                if (sts_type == 4):
                    sts_len = (((sts_type_ext & EVNT_TS_LEN_MASK) >> EVNT_TS_LEN_SHIFT) + 2)
                    if (sts_type_ext & 2):
                          sts_len = (sts_len + 1)
                if (sts_type == 5):
                    sts_len = 1
                psf_cmd = []
                for cnt in range(sts_len):
                    sts_ptr2 = sts_ptr + (2*cnt)
                    if (not psf_config.psf_endian):
                        sts_tmp = ((rxpkt_buf[sts_ptr2] << 8) | rxpkt_buf[sts_ptr2+1])
                    else:
                        sts_tmp = (rxpkt_buf[sts_ptr2] | (rxpkt_buf[sts_ptr2+1] << 8))
                    psf_cmd = psf_cmd + [sts_tmp]
                #print "PSF Command: ", psf_cmd
                if (sts_type == 1):
                    psf_list.txts.TS_list += [(((psf_cmd[4] << 16) + psf_cmd[3]) * 10**9) + ((psf_cmd[2] & 0x3fff) << 16) + psf_cmd[1]]
                if (sts_type == 2):
                    rx_timestamp = RX_Timestamp()
                    rx_timestamp.ts = (((psf_cmd[4] << 16) + psf_cmd[3]) * 10**9) + ((psf_cmd[2] & 0x3fff) << 16) + psf_cmd[1]
                    rx_timestamp.seqID = psf_cmd[5]
                    rx_timestamp.mtype = psf_cmd[6] >> 12
                    rx_timestamp.sourceHash = psf_cmd[6] & 0xfff
                    rx_timestamp.missed = psf_cmd[2] >> 14
                    rx_timestamp.ok = 1
                    psf_list.rxts.TS_list += [rx_timestamp]
                if (sts_type == 3):
                    psf_list.trig_list = psf_list.trig_list + [psf_cmd[1]]
                if (sts_type == 4):
                    psf_list.event_list = psf_list.event_list + [psf_cmd]
                if (sts_type == 5):
                    psf_list.psf_err_list = psf_list.psf_err_list + psf_cmd
                if (sts_type == 6):
                    psf_list.pcf_read_list = psf_list.pcf_read_list + [psf_cmd[1]]
                sts_ptr = sts_ptr + (sts_len * 2)
    return (psf_ok)

#
#
# End of 1588 PSF_packet routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 PSF_packet script
#
# Uses EPL routines to check and parse packet
def PSF_packet_EPL(psf_config, rxpkt_buf, psf_list):
    # Evaluate packet to determine if PSF packet
    lenPkt = len(xem.rxpkt_buf)	
    from epl import charArray
    pktBuf = charArray( lenPkt)
    for b in range( lenPkt):
        pktBuf[b] = xem.rxpkt_buf[b]
    nextMsg = xem.IsPhyStatusFrame( pktBuf, lenPkt )
    psf_ok = 0
    # Updates psf_list with PSF commands from packet
    while( nextMsg ):
        # Use exception handler here to avoid a quirk of SWIG when nextMsg is 0, ResultObj isn't properly returned
        try: nextMsg, msgType, psfBuf = xem.GetNextPhyMessage( nextMsg )
        except: 
            nextMsg = 0
        if (nextMsg):
            psf_ok = 1
            if (verbose):
                print "PSF Packet detected"
            if( msgType == xem.PHYMSG_STATUS_TX ):
                psf_list.txts.TS_list += [(psfBuf.TxStatus.txTimestampSecs * 10**9) + psfBuf.TxStatus.txTimestampNanoSecs]
            elif( msgType == xem.PHYMSG_STATUS_RX ):
                rx_timestamp = RX_Timestamp()
                rx_timestamp.ts = (psfBuf.RxStatus.rxTimestampSecs * 10**9) + psfBuf.RxStatus.rxTimestampNanoSecs
                rx_timestamp.seqID = psfBuf.RxStatus.sequenceId
                rx_timestamp.mtype = psfBuf.RxStatus.messageType
                rx_timestamp.sourceHash = psfBuf.RxStatus.sourceHash
                rx_timestamp.missed = psfBuf.RxStatus.rxOverflowCount
                rx_timestamp.ok = 1
                psf_list.rxts.TS_list += [rx_timestamp]
            elif( msgType == xem.PHYMSG_STATUS_TRIGGER ):
                psf_list.trig_list = psf_list.trig_list + [psfBuf.TriggerStatus.triggerStatus]
            elif( msgType == xem.PHYMSG_STATUS_EVENT ):
                event_entry = PSF_Event_Status()
                event_entry.ptp_ests = psfBuf.EventStatus.ptpEstsRegBits
                event_entry.ext_event_status_valid = psfBuf.EventStatus.extendedEventStatusFlag
                event_entry.ext_event_status = psfBuf.EventStatus.extendedEventInfo
                event_entry.event_ts_sec = psfBuf.EventStatus.evtTimestampSecs
                event_entry.event_ts_ns = psfBuf.EventStatus.evtTimestampNanoSecs
                psf_list.event_list = psf_list.event_list + [event_entry]
            elif( msgType == xem.PHYMSG_STATUS_ERROR ):
                psf_list.psf_err_list = psf_list.psf_err_list + [((psfBuf.ErrorStatus.frameBufOverflowFlag << 1) | psfBuf.ErrorStatus.frameCounterOverflowFlag)]
            elif( msgType == xem.PHYMSG_STATUS_REG_READ ):
                psf_list.pcf_read_list = psf_list.pcf_read_list + [psfBuf.RegReadStatus.readRegisterValue]
            del psfBuf

    return (psf_ok)

#
#
# End of 1588 PSF_packet routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588v2 PTP Header
#
def v2_Parse_Pkt(rxpkt_buf, cfg):
    #
    # Check Mac Header
    #
    pkt_status = v2_Packet_Status()
    pkt_ok = 0
    v2_ok = 0
    v1_ok = 0
    pkt_etype = (rxpkt_buf[12] << 8) | rxpkt_buf[13]
    pkt_offset = 14
    ptp_offset = 0
    udp_offset = 0
    if (pkt_etype == 0x8100):
        #VLAN TAG
        pkt_status.vlan_tag = 1
        pkt_status.vlan_tci = (rxpkt_buf[pkt_offset] << 8) | rxpkt_buf[pkt_offset + 1]
        pkt_etype = (rxpkt_buf[pkt_offset + 2] << 8) | rxpkt_buf[pkt_offset + 3]
        pkt_offset = pkt_offset + 4
    if (cfg.l2_enet & (pkt_etype == cfg.l2_etype)):
        pkt_status.l2_enet_ok = 1
        ptp_offset = pkt_offset
        pkt_ok = 1
    if (cfg.ipv4_en & (pkt_etype == 0x0800)):
        pkt_status.ipv4_ok = 1
        udp_offset = pkt_offset + ((rxpkt_buf[pkt_offset] & 0xf) << 2)
        pkt_ok = 1
    if (cfg.ipv6_en & (pkt_etype == 0x86DD)):
        pkt_status.ipv6_ok = 1
        udp_offset = pkt_offset + 40
        pkt_ok = 1
    if (pkt_status.ipv6_ok == 1):
        pkt_status.ip_src_addr = rxpkt_buf[pkt_offset+8 : pkt_offset+24]
        pkt_status.ip_dest_addr = rxpkt_buf[pkt_offset+24 : pkt_offset+40]
        pkt_status.udp_length = (rxpkt_buf[pkt_offset+4] << 8) & rxpkt_buf[pkt_offset+5]
        # check protocol for UDP
        if (rxpkt_buf[pkt_offset + 6] != 0x11):
            print "WARNING:  IP packet with non-UDP protocol"
            pkt_ok = 0
        else:
            # check UDP destination port number
            udp_dest_port = (rxpkt_buf[udp_offset + 2] << 8) + rxpkt_buf[udp_offset + 3]
            if ((udp_dest_port == 319) | (udp_dest_port == 320)):
                ptp_offset = udp_offset + 8
            else:
                print "WARNING:  UDP packet with non-1588 port number"
                pkt_ok = 0
    if (pkt_status.ipv4_ok == 1):
        pkt_status.ip_src_addr = rxpkt_buf[pkt_offset+12 : pkt_offset+16]
        pkt_status.ip_dest_addr = rxpkt_buf[pkt_offset+16 : pkt_offset+20]
        pkt_status.udp_length = (rxpkt_buf[pkt_offset+4] << 8) & rxpkt_buf[pkt_offset+5]
        # check protocol for UDP
        if (rxpkt_buf[pkt_offset + 9] != 0x11):
            print "WARNING:  IP packet with non-UDP protocol"
            print "pkt_offset = ", pkt_offset
            print "rxpkt_buf", rxpkt_buf
            pkt_ok = 0
        else:
            # check UDP destination port number
            udp_dest_port = (rxpkt_buf[udp_offset + 2] << 8) + rxpkt_buf[udp_offset + 3]
            if ((udp_dest_port == 319) | (udp_dest_port == 320)):
                ptp_offset = udp_offset + 8
            else:
                print "WARNING:  UDP packet with non-1588 port number"
                pkt_ok = 0
    if (pkt_ok):
        # check PTP Version
        ptp_message = rxpkt_buf[ptp_offset:(len(rxpkt_buf) - 4)]
        pkt_status.versionPTP = ptp_message[1] & 0xf
        if ((pkt_status.versionPTP == 2) | (cfg.versionPTP_en == 0)):
            v2_ok = cfg.v2_enable
        if ((pkt_status.versionPTP == 1) | (cfg.versionPTP_en == 0)):
            v1_ok = not cfg.v2_enable
        if not v1_ok and not v2_ok:
            print "WARNING: Invalid PTP version detected: ", pkt_status.versionPTP
    if (v2_ok):
        # check PTP message length
        pkt_status.messageLength = (ptp_message[2] << 8) | ptp_message[3]
        if (len(ptp_message) < (pkt_status.messageLength)):
            if (cfg.check_msg_len):
                v2_ok = 0
            print "PTP: Incorrect message length: expect %d  actual %d" % (pkt_status.messageLength, len(ptp_message))
    if (v2_ok):
        # Check sourcePortIdentity is not local portId
        pkt_status.sourcePortIdentity = ptp_message[20:30]
        if (pkt_status.sourcePortIdentity == cfg.portDS.portIdentity):
            v2_ok = 0
            print "PTP: sourcePortIdentity matches local port_identity", pkt_status.sourcePortIdentity
    if (v2_ok):
        # Check message type vs length
        pkt_status.messageType = ptp_message[0] & 0xf
        pkt_status.trans_specific = ptp_message[0] >> 4
        pkt_status.domain = ptp_message[4]
        pkt_status.header = ptp_message[0:34]
        pkt_status.two_step = (ptp_message[6] >> 1) & 0x1
        pkt_status.src_hash = Gen_Src_Hash(ptp_message[20:30], 0)
        pkt_status.seqID = (ptp_message[30] << 8) + ptp_message[31]
        pkt_status.corr_field = convertCorrField(ptp_message[8:16])
        pkt_status.extra_bytes = ptp_message[pkt_status.messageLength:len(ptp_message)]
        pkt_status.logInterval = Int8(ptp_message[33]) 
        v2_ok = 0
        if (pkt_status.messageType == mtype_sync):
            if (len(ptp_message) >= 44):
                pkt_status.body = ptp_message[34:44]
                pkt_status.sync_originTS = pkt_status.body[2:10]
                pkt_status.suffix = ptp_message[44:pkt_status.messageLength]
                pkt_status.sync_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_delay_req):
            if (len(ptp_message) >= 44):
                pkt_status.body = ptp_message[34:44]
                pkt_status.suffix = ptp_message[44:pkt_status.messageLength]
                pkt_status.delay_req_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_follow_up):
            if (len(ptp_message) >= 44):
                pkt_status.body = ptp_message[34:44]
                pkt_status.sync_originTS = pkt_status.body[2:10]
                pkt_status.fu_assocSeqId = pkt_status.seqID
                pkt_status.suffix = ptp_message[44:pkt_status.messageLength]
                pkt_status.follow_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_delay_resp):
            if (len(ptp_message) >= 54):
                pkt_status.body = ptp_message[34:54]
                pkt_status.rcvdTS = pkt_status.body[2:10]
                pkt_status.reqSourceSeqID = pkt_status.seqID
                pkt_status.suffix = ptp_message[54:pkt_status.messageLength]
                pkt_status.delay_resp_ok = 1
                pkt_status.reqPortId = pkt_status.body[10:20]
                v2_ok = 1
        if (pkt_status.messageType == mtype_pdelay_req):
            if (len(ptp_message) >= 54):
                pkt_status.body = ptp_message[34:54]
                pkt_status.suffix = ptp_message[54:pkt_status.messageLength]
                pkt_status.pdelay_req_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_pdelay_resp):
            if (len(ptp_message) >= 54):
                pkt_status.body = ptp_message[34:54]
                pkt_status.rcvdTS = pkt_status.body[2:10]
                pkt_status.reqSourceSeqID = pkt_status.seqID
                pkt_status.suffix = ptp_message[54:pkt_status.messageLength]
                pkt_status.pdelay_resp_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_pdelay_follow):
            if (len(ptp_message) >= 54):
                pkt_status.body = ptp_message[34:54]
                pkt_status.rcvdTS = pkt_status.body[2:10]
                pkt_status.reqSourceSeqID = pkt_status.seqID
                pkt_status.suffix = ptp_message[54:pkt_status.messageLength]
                pkt_status.pdelay_follow_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_announce):
            if (len(ptp_message) >= 64):
                pkt_status.body = ptp_message[34:64]
                pkt_status.suffix = ptp_message[64:pkt_status.messageLength]
                pkt_status.announce_ok = 1
                pkt_status.FM_entry = foreign_Master_Data_Set()
                pkt_status.FM_entry.sourcePortIdentity = pkt_status.sourcePortIdentity
                pkt_status.FM_entry.grandmasterPriority1 = ptp_message[47]
                pkt_status.FM_entry.grandmasterClockQuality.clockClass = ptp_message[48]
                pkt_status.FM_entry.grandmasterClockQuality.clockAccuracy = ptp_message[49]
                pkt_status.FM_entry.grandmasterClockQuality.offsetScaledLogVariance = (ptp_message[50] << 8) | ptp_message[51]
                pkt_status.FM_entry.grandmasterPriority2 = ptp_message[52]
                pkt_status.FM_entry.grandmasterIdentity = ptp_message[53:61]
                pkt_status.FM_entry.stepsRemoved = (ptp_message[61] << 8) | ptp_message[62]
                pkt_status.FM_entry.timeSource = ptp_message[63]
                pkt_status.FM_entry.flagField = ptp_message[7]
                pkt_status.FM_entry.currentUtcOffset = (ptp_message[44] << 8) | ptp_message[45]
                pkt_status.FM_entry.receivePortIdentity = cfg.portDS.portIdentity
                v2_ok = 1
        if (pkt_status.messageType == mtype_signaling):
            if (len(ptp_message) >= 44):
                pkt_status.body = ptp_message[34:44]
                pkt_status.suffix = ptp_message[44:pkt_status.messageLength]
                pkt_status.signaling_ok = 1
                v2_ok = 1
        if (pkt_status.messageType == mtype_management):
            if (len(ptp_message) >= 48):
                pkt_status.body = ptp_message[34:48]
                pkt_status.mgnt_action = ptp_message[46]
                pkt_status.suffix = ptp_message[48:pkt_status.messageLength]
                pkt_status.management_ok = 1
                v2_ok = 1
    if (v1_ok):
        # Check message type vs length
        pkt_status.messageType = ptp_message[20]
        pkt_status.domain = ptp_message[4:20]
        pkt_status.header = ptp_message[0:40]
        pkt_status.control = ptp_message[32]
        pkt_status.two_step = (ptp_message[35] >> 3) & 0x1
        pkt_status.src_hash = Gen_Src_Hash(ptp_message[20:30], 0)
        pkt_status.seqID = (ptp_message[30] << 8) + ptp_message[31]
        v1_ok = 0
        if (pkt_status.messageType == 0x01):
            if (pkt_status.control == 0):
                if ((len(ptp_message) >= 124) & (pkt_status.messageType == 0x01)):
                    pkt_status.body = ptp_message[40:124]
                    pkt_status.sync_originTS = pkt_status.body[0:8]
                    pkt_status.suffix = ptp_message[124:pkt_status.messageLength]
                    pkt_status.sync_ok = 1
                    v1_ok = 1
            if (pkt_status.control == 1):
                if ((len(ptp_message) >= 124) & (pkt_status.messageType == 0x01)):
                    pkt_status.body = ptp_message[40:124]
                    pkt_status.suffix = ptp_message[124:pkt_status.messageLength]
                    pkt_status.delay_req_ok = 1
                    v1_ok = 1
        if (pkt_status.messageType == 0x02):
            if (pkt_status.control == 2):
                if (len(ptp_message) >= 52):
                    pkt_status.body = ptp_message[40:52]
                    pkt_status.sync_originTS = pkt_status.body[4:12]
                    pkt_status.fu_assocSeqId = (pkt_status.body[2]<< 8) + pkt_status.body[3]
                    pkt_status.suffix = ptp_message[52:pkt_status.messageLength]
                    pkt_status.follow_ok = 1
                    v1_ok = 1
            if (pkt_status.control == 3):
                if (len(ptp_message) >= 60):
                    pkt_status.body = ptp_message[40:60]
                    pkt_status.rcvdTS = pkt_status.body[0:8]
                    pkt_status.reqPortId = pkt_status.body[10:18]
                    pkt_status.reqSourceSeqID = (pkt_status.body[18]<< 8) + pkt_status.body[19]
                    pkt_status.suffix = ptp_message[60:pkt_status.messageLength]
                    pkt_status.delay_resp_ok = 1
                    v1_ok = 1
    pkt_status.v2_1588_ok = ((v1_ok == 1) | (v2_ok == 1))
    pkt_status.ptp_offset = ptp_offset
    pkt_status.udp_offset = udp_offset
    return(pkt_status)

#
#
# End of 1588 v2_Parse_Pkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588v2 PTP Build Packet
#
def Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr):
    #
    if (cfg.l2_enet):
        v2_packet = mac_hdr + ptp_message
    if (cfg.ipv6_en):
        # Extend PTP message by 2 octets for UDP checksum correctin
        ptp_message = ptp_message + [0, 0]
        # UDP Header
        udp_length = len(ptp_message) + 8
        udp_hdr = [cfg.udp_src_port >> 8, cfg.udp_src_port & 0xff, udp_dest_port >> 8, udp_dest_port & 0xff, udp_length >> 8, udp_length & 0xff, 0x00, 0x00]
        pseudo_hdr = cfg.ipv6_src_addr + ip_dest_addr + [0x00, 0x11] + [udp_length >> 8, udp_length & 0xff]
        udp_chksum_buf = pseudo_hdr + udp_hdr + ptp_message
        udp_chksum = ones_comp_chksum(udp_chksum_buf)
        udp_hdr = udp_hdr[0:6] + [udp_chksum >> 8, udp_chksum & 0xff]
        #
        # IP Header
        ip_length = udp_length + 40
        ip_hdr = [0x60, 0x00, 0x00, 0x00, (ip_length >> 8), (ip_length & 0xff), 0x11, 0x00] + cfg.ipv6_src_addr + ip_dest_addr
        # Build packet
        v2_packet = mac_hdr + ip_hdr + udp_hdr + ptp_message
    if (cfg.ipv4_en):
        # UDP Header
        udp_src_port = 0
        udp_length = len(ptp_message) + 8
        udp_hdr = [cfg.udp_src_port >> 8, cfg.udp_src_port & 0xff, udp_dest_port >> 8, udp_dest_port & 0xff, udp_length >> 8, udp_length & 0xff, 0x00, 0x00]
        if (cfg.ipv4_udp_chksum_en):
            pseudo_hdr = cfg.ipv4_src_addr + ip_dest_addr + [0x00, 0x11] + [udp_length >> 8, udp_length & 0xff]
            udp_chksum_buf = pseudo_hdr + udp_hdr + ptp_message
            udp_chksum = ones_comp_chksum(udp_chksum_buf)
            udp_hdr = udp_hdr[0:6] + [udp_chksum >> 8, udp_chksum & 0xff]
        #
        # IP Header
        ip_length = udp_length + 20
        cfg.ipv4_ID = Incr_Word16(cfg.ipv4_ID)
        ip_hdr = [0x45, 0x00, (ip_length >> 8), (ip_length & 0xff), (cfg.ipv4_ID >> 8), (cfg.ipv4_ID & 0xff), 0x00, 0x00, cfg.ipv4_ttl, 0x11, 0x00, 0x00] + cfg.ipv4_src_addr + ip_dest_addr
        # compute IP checksum
        chksum = ones_comp_chksum(ip_hdr)
        ip_hdr = ip_hdr[0:10] + [chksum >> 8, chksum & 0xff] + cfg.ipv4_src_addr + ip_dest_addr
        # Build packet
        v2_packet = mac_hdr + ip_hdr + udp_hdr + ptp_message
    #
    while (len(v2_packet) < 60):
        v2_packet = v2_packet + [0]
    if (cfg.vlan_en):
        vlan_etype = [0x81, 0x00]
        vlan_tci = [((cfg.vlan_pri << 5) | (cfg.vlan_vid >> 8)), (cfg.vlan_vid & 0xff)]    
        v2_packet = v2_packet[0:12] + vlan_etype + vlan_tci + v2_packet[12:len(v2_packet)]    
    return(v2_packet)

#
#
# End of 1588 Build_v2_Pkt routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP Announce Packet
#
def v2AnnouncePkt(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
    ptpHeader.logInterval = cfg.portDS.logAnnounceInterval
    ptp_message = v2_Announce_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    announce_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(announce_pkt)

#
#
# End of 1588 v2AnnouncePkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 Announce Message
#
def v2_Announce_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.announce_seqID = Incr_Word16(cfg.announce_seqID) 
    #
    # set message type
    messageType = mtype_announce
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + curr_time
    ptpBody += [(cfg.timePropertiesDS.currentUtcOffset >> 8), (cfg.timePropertiesDS.currentUtcOffset & 0xff)]
    ptpBody += [0, cfg.parentDS.grandmasterPriority1]
    ptpBody += [cfg.parentDS.grandmasterClockQuality.clockClass, cfg.parentDS.grandmasterClockQuality.clockAccuracy] + [(cfg.parentDS.grandmasterClockQuality.offsetScaledLogVariance >> 8), (cfg.parentDS.grandmasterClockQuality.offsetScaledLogVariance & 0xff)]
    ptpBody += [cfg.parentDS.grandmasterPriority2]
    ptpBody += cfg.parentDS.grandmasterIdentity
    ptpBody += [(cfg.currentDS.stepsRemoved >> 8), (cfg.currentDS.stepsRemoved & 0xff)]
    ptpBody += [cfg.timePropertiesDS.timeSource]
    #
    # PTP Flags
    #
    announce_flags = cfg.timePropertiesDS.leap61
    announce_flags |= (cfg.timePropertiesDS.leap59 << 1)
    announce_flags |= (cfg.timePropertiesDS.currentUtcOffsetValid << 2)
    announce_flags |= (cfg.timePropertiesDS.ptpTimescale << 3)
    announce_flags |= (cfg.timePropertiesDS.timeTraceable << 4)
    announce_flags |= (cfg.timePropertiesDS.frequencyTraceable << 5)
    ptpFlags = [cfg.all_flags, announce_flags]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, cfg.announce_seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_Announce_Message routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588v2 PTP Sync Packet
#
def v2SyncPkt(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    if (cfg.v2_enable):
        ptpHeader.logInterval = cfg.portDS.logSyncInterval
        ptp_message = v2_Sync_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    else:
        ptp_message = v1_Sync_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
        if (cfg.one_step & cfg.tx_chk_1step):
            # Add 2 bytes to allow for checksum correction
            ptp_message += [0, 0]
    if (cfg.ipv6_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    sync_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(sync_pkt)

#
#
# End of 1588 v2SyncPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 v1_Sync_Message script
#
def v1_Sync_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #    
    #
    # Increment Sequence ID
    cfg.sync_seqID = Incr_Word16(cfg.sync_seqID) 
    # PTP Sync data
    #
    version_ptp = [0x00, 0x01]
    version_network = [0x00, 0x00]
    subDomain = [95, 68, 70, 76, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    messageType = [0x01]
    commTech = [0x01]
    #sequenceID = 0
    ptpControl = [0x00]
    if (cfg.one_step):
        ptp_flags = [0x00, 0x00]
        origin_TS = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        ptp_flags = [0x00, 0x08]
        origin_TS = curr_time
    ptp_buf = version_ptp + version_network + subDomain + messageType + commTech + cfg.mac_SA + cfg.v1_srcPortID + [(cfg.sync_seqID >> 8), (cfg.sync_seqID & 0xff)] + ptpControl + [0x00] + ptp_flags + [0, 0, 0, 0] + origin_TS + [(cfg.epoch >> 8), (cfg.epoch & 0xff)]
    #
    for i in range(74):
        ptp_buf = ptp_buf + [0]
        
    ptp_buf = ptp_buf + ptpSuffix
    return ptp_buf

#
#
# End of 1588 v1_Sync_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 Sync Message
#
def v2_Sync_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.sync_seqID = Incr_Word16(cfg.sync_seqID) 
    #
    # Correction field (for one-step)
    ptpHeader.correctionField = [0, 0, 0, 0, (cfg.sync_corr_fld >> 8), (cfg.sync_corr_fld & 0xff), 0, 0]
    #
    # set message type
    messageType = mtype_sync
    #
    # Store PTP suffix
    #
    ptpSuffix_save = ptpSuffix
    # Build PTP Body, Flags
    #
    if (cfg.one_step == 1):
        ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff), 0, 0, 0, 0, 0, 0, 0, 0]

    else:
        ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + curr_time
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags | cfg.sync_flags | ((~cfg.one_step & 1) << 1)), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, cfg.sync_seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)
    #
    # Restore ptpSuffix
    #
    ptpSuffix = ptpSuffix_save
    return(ptp_message)

#
#
# End of 1588 v2_Sync_Message routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# 1588v2 PTP FollowUp Packet
#
def v2FollowUpPkt(tx_ts, cfg, ptpHeader, ptpSuffix):
    #
    if (cfg.v2_enable):
        ptpHeader.logInterval = cfg.portDS.logSyncInterval
        ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
        ptp_message = v2_FollowUp_Message(tx_ts, cfg, ptpHeader, ptpSuffix)
    else:
        ptp_message = v1_FollowUp_Message(tx_ts, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    followup_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(followup_pkt)

#
#
# End of 1588 v2FollowUpPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v1 Follow-Up Message
#
def v1_FollowUp_Message(tx_ts, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.gen_seqID = Incr_Word16(cfg.gen_seqID) 
    #
    # PTP Sync data
    #
    version_ptp = [0x00, 0x01]
    version_network = [0x00, 0x00]
    subDomain = [95, 68, 70, 76, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    messageType = [0x02]
    commTech = [0x01]
    #sequenceID = 0
    ptpControl = [0x02]
    ptp_flags = [0x08, 0x00]
    ptp_buf = version_ptp + version_network + subDomain + messageType + commTech + cfg.mac_SA + cfg.v1_srcPortID + [(cfg.gen_seqID >> 8), (cfg.gen_seqID & 0xff)] + ptpControl + [0x00] + ptp_flags + [0, 0, 0, 0, 0, 0] + [(cfg.sync_seqID >> 8), (cfg.sync_seqID & 0xff)] + tx_ts
    ptp_buf = ptp_buf + ptpSuffix
    return ptp_buf

#
#
# End of 1588 v1_FollowUp_Message routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 Follow-Up Message
#
def v2_FollowUp_Message(tx_ts, cfg, ptpHeader, ptpSuffix):
    #
    #
    # set message type
    messageType = mtype_follow_up
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + tx_ts
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags | cfg.followup_flags), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, cfg.sync_seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_FollowUp_Message routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588v2 PTP DelayReq Packet
#
def v2DelayReqPkt(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    if (cfg.v2_enable):
        ptpHeader.logInterval = 0x7f
        ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
        ptp_message = v2_DelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    else:
        ptp_message = v1_DelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    dreq_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(dreq_pkt)

#
#
# End of 1588 v2DelayReqPkt routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v1 DelayReq Message
#
def v1_DelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.delayreq_seqID = Incr_Word16(cfg.delayreq_seqID) 
    # PTP Sync data
    #
    version_ptp = [0x00, 0x01]
    version_network = [0x00, 0x01]
    subDomain = [95, 68, 70, 76, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    messageType = [0x01]
    commTech = [0x01]
    #sequenceID = 0
    ptpControl = [0x01]
    if (cfg.one_step):
        ptp_flags = [0x00, 0x00]
        origin_TS = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        ptp_flags = [0x00, 0x08]
        origin_TS = curr_time
    ptp_buf = version_ptp + version_network + subDomain + messageType + commTech + cfg.mac_SA + cfg.v1_srcPortID + [(cfg.delayreq_seqID >> 8), (cfg.delayreq_seqID & 0xff)] + ptpControl + [0x00] + ptp_flags + [0, 0, 0, 0] + origin_TS + [(cfg.epoch >> 8), (cfg.epoch & 0xff)]
    ptp_buf += [0, 0] + cfg.v1_grandmaster_stats
    ptp_buf += [0, 0, 0, cfg.v1_sync_interval]
    ptp_buf += [0, 0, 255, 255]
    ptp_buf += [0, 0, 0, cfg.v1_local_steps_removed]
    ptp_buf += [0, 0, 0, 4]
    ptp_buf += [68, 70, 76, 84]
    ptp_buf += cfg.v1_parent_stats
    ptp_buf += [0, 0, 0, 0]
    ptp_buf += [0, 0, 0, 0]
    ptp_buf += [0, 0, 0, 0]
    #
    #for i in range(74):
    #    ptp_buf = ptp_buf + [0]
    ptp_buf = ptp_buf + ptpSuffix
    return ptp_buf
    
#
#
# End of 1588 v1_DelayReq_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 DelayReq Message
#
def v2_DelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.delayreq_seqID = Incr_Word16(cfg.delayreq_seqID) 
    # set message type
    messageType = mtype_delay_req
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + curr_time
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, cfg.delayreq_seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_DelayReq_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP DelayResp Packet
#
def v2DelayRespPkt(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    if (cfg.v2_enable):
        cfg.portDS.logMinDelayReqInterval = cfg.master_log_min_delay_req_interval
        ptpHeader.logInterval = cfg.portDS.logMinDelayReqInterval
        ptpHeader.correctionField = pkt_status.header[8:16]
        ptp_message = v2_DelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix)
    else:
        ptp_message = v1_DelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    delayresp_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(delayresp_pkt)

#
#
# End of 1588 v2DelayRespPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v1 DelayResp Message
#
def v1_DelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    # Increment Sequence ID
    cfg.gen_seqID = Incr_Word16(cfg.gen_seqID) 
    #
    # Get ReqSrc values from DelayReq packet
    reqSrcCommTech = pkt_status.header[21]
    reqSrcUUID = pkt_status.header[22:28]
    reqSrcPortID = pkt_status.header[28:30]
    reqSrcSeqID = pkt_status.header[30:32]
    #
    # PTP DelayResp data
    #
    version_ptp = [0x00, 0x01]
    version_network = [0x00, 0x00]
    subDomain = [95, 68, 70, 76, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    messageType = [0x02]
    commTech = [0x01]
    #sequenceID = 0
    ptpControl = [0x03]
    ptp_flags = [0x08, 0x00]
    ptp_buf = version_ptp + version_network + subDomain + messageType + commTech + cfg.mac_SA + cfg.v1_srcPortID + [(cfg.gen_seqID >> 8), (cfg.gen_seqID & 0xff)] + ptpControl + [0x00] + ptp_flags + [0, 0, 0, 0] + rx_ts + [0x00] + [reqSrcCommTech] + reqSrcUUID + reqSrcPortID + reqSrcSeqID
    ptp_buf = ptp_buf + ptpSuffix
    return ptp_buf

#
#
# End of 1588 v1_DelayResp_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 DelayResp Message
#
def v2_DelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    #
    # set message type
    messageType = mtype_delay_resp
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + rx_ts + pkt_status.header[20:30]
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, pkt_status.seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_DelayResp_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 v2_PTP_Message script
#
def v2_PTP_Message(cfg, messageType, sequenceID, ptpHeader, ptpFlags, ptpBody, ptpSuffix):
    #
    # Determine PTP Control field from messageType
    #
    ptp_control = 5
    if (messageType == mtype_sync):
        ptp_control = 0
    if (messageType == mtype_delay_req):
        ptp_control = 1
    if (messageType == mtype_follow_up):
        ptp_control = 2
    if (messageType == mtype_delay_resp):
        ptp_control = 3
    if (messageType == mtype_management):
        ptp_control = 4
    #
    # Determine PTP Message Length
    #
    messageLength = 54
    if ((messageType == mtype_sync) | (messageType == mtype_follow_up) | (messageType == mtype_delay_req)):
        messageLength = 44
    if (messageType == mtype_announce):
        messageLength = 64
    if (messageType == mtype_management):
        messageLength = 34 + len(ptpBody)
    messageLength = messageLength + len(ptpSuffix)
    #
    # PTP Header
    #
    ptp_hdr = [(ptpHeader.transportSpecific << 4) | messageType]
    ptp_hdr = ptp_hdr + [cfg.portDS.versionNumber]
    ptp_hdr = ptp_hdr + [(messageLength >> 8), (messageLength & 0xff)]
    ptp_hdr = ptp_hdr + [cfg.defaultDS.domainNumber, 0x00] + ptpFlags
    ptp_hdr = ptp_hdr + ptpHeader.correctionField
    ptp_hdr = ptp_hdr + [0x00, 0x00, 0x00, 0x00]
    ptp_hdr = ptp_hdr + cfg.portDS.portIdentity
    ptp_hdr = ptp_hdr + [(sequenceID >> 8), (sequenceID & 0xff)]
    ptp_hdr = ptp_hdr + [ptp_control]
    # logInterval is signed
    ptp_hdr += [(0x100 + ptpHeader.logInterval) & 0xff]

    #
    # Add PTP Body and Suffix
    #
    ptp_message = ptp_hdr + ptpBody + ptpSuffix
    return (ptp_message)

#
#
# End of 1588 v2_PTP_Message routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588v2 PTP PDelayReq Packet
#
def v2PDelayReqPkt(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    ptpHeader.logInterval = 0x7f
    ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
    ptp_message = v2_PDelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.pdelay_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv4_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv6_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    pdelay_req_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(pdelay_req_pkt)

#
#
# End of 1588 v2PDelayReqPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 PDelayReq Message
#
def v2_PDelayReq_Message(curr_time, cfg, ptpHeader, ptpSuffix):
    #
    #
    # Increment Sequence ID
    cfg.pdelayreq_seqID = Incr_Word16(cfg.pdelayreq_seqID) 
    # set message type
    messageType = mtype_pdelay_req
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + curr_time + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, cfg.pdelayreq_seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_PDelayReq_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP PDelayResp Packet
#
def v2PDelayRespPkt(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    ptpHeader.logInterval = 0x7f
    ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
    ptp_message = v2_PDelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.pdelay_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv4_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 319
        ip_dest_addr = cfg.ipv6_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    delayresp_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(delayresp_pkt)

#
#
# End of 1588 v2PDelayRespPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 PDelayResp Message
#
def v2_PDelayResp_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    #
    # set message type
    messageType = mtype_pdelay_resp
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + rx_ts + pkt_status.header[20:30]
    #
    # PTP Flags
    # need to set TWO_STEP flag
    ptpFlags = [(cfg.all_flags | 2), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, pkt_status.seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_PDelayResp_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP PDelayRespFU Packet
#
def v2PDelayRespFUPkt(rx_ts, cfg, pdelay_follow_msg):
    #
    # modify timestamp of pre-built ptp message
    ptp_message = pdelay_follow_msg[0:36] + rx_ts + pdelay_follow_msg[44:len(pdelay_follow_msg)]
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.pdelay_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_pdelay_dest_addr
        mac_hdr = cfg.ipv4_pdelay_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    delayresp_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(delayresp_pkt)

#
#
# End of 1588 v2PDelayRespFUPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 PDelayRespFU Message
#
def v2_PDelayRespFU_Message(rx_ts, cfg, ptpHeader, pkt_status, ptpSuffix):
    #
    ptpHeader.logInterval = 0x7f
    ptpHeader.correctionField = pkt_status.header[8:16]
    #
    # set message type
    messageType = mtype_pdelay_follow
    #
    # Build PTP Body, Flags
    #
    ptpBody = [(cfg.epoch >> 8), (cfg.epoch & 0xff)] + rx_ts + pkt_status.header[20:30]
    #
    # PTP Flags
    #
    ptpFlags = [(cfg.all_flags), 0x0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, pkt_status.seqID, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_PDelayRespFU_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP Management Packet
#
def v2ManagementPkt(targetPortIdentity, actionField, managementTLV, cfg, ptpHeader, ptpSuffix):
    #
    ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
    ptpHeader.logInterval = 0x7f
    # Increment Sequence ID
    cfg.management_seqID = Incr_Word16(cfg.management_seqID)
    sequenceId = cfg.management_seqID
    #
    ptp_message = v2_Management_Message(targetPortIdentity, sequenceId, actionField, managementTLV, cfg, ptpHeader, ptpSuffix)
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    management_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(management_pkt)

#
#
# End of 1588 v2ManagementPkt routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Build 1588v2 Management Message
#
def v2_Management_Message(targetPortIdentity, sequenceId, actionField, managementTLV, cfg, ptpHeader, ptpSuffix):
    #
    #
    # set message type
    messageType = mtype_management
    #
    # Build PTP Body, Flags
    #
    ptpBody = targetPortIdentity + [cfg.startingBoundaryHops, cfg.startingBoundaryHops]
    ptpBody += [actionField, 0]
    ptpBody += managementTLV
    #
    # PTP Flags
    #
    ptpFlags = [cfg.all_flags, 0]
    # Build PTP Message
    #
    ptp_message = v2_PTP_Message(cfg, messageType, sequenceId, ptpHeader, ptpFlags, ptpBody, ptpSuffix)    
    return(ptp_message)

#
#
# End of 1588 v2_Management_Message routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 CreateManagementTLV Message
#
def CreateManagementTLV(managementId, dataField):
    tlv_type = TLV_TYPE.MANAGEMENT
    lengthField_val = 2 + len(dataField)
    managementTLV = Uint16_to_List(tlv_type)
    managementTLV += Uint16_to_List(lengthField_val)
    managementTLV += Uint16_to_List(managementId)
    managementTLV += dataField
    return(managementTLV)

#
#
# End of 1588 CreateManagementTLV routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 SendManagementResponse Message
#
def SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField):
    managementTLV = CreateManagementTLV(managementId, dataField)
    txpkt_buf = v2ManagementResponsePkt(targetPortIdentity, pkt_sts_1588, actionField, managementTLV, cfg, cfg.ptpHeader, cfg.ptpSuffix)
    txdone = SendPacket(port, txpkt_buf)
    return(txdone)
#
#
# End of 1588 SendManagementResponse routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 CreateManagementErrorTLV Message
#
def CreateManagementErrorTLV(managementErrorId, managementId, displayData):
    tlv_type = TLV_TYPE.MANAGEMENT_ERROR_STATUS
    if (len(displayData) & 1):
        #pad by 1 octet
        pad = [0]
    else:
        pad = []
    lengthField_val = 8 + len(displayData) + len(pad)
    lengthField = Uint16_to_List(lengthField_val)
    managementTLV = Uint16_to_List(tlv_type)
    managementTLV += Uint16_to_List(lengthField_val)
    managementTLV += Uint16_to_List(managementErrorId)
    managementTLV += Uint16_to_List(managementId)
    managementTLV += [0, 0, 0, 0] + displayData + pad
    return(managementTLV)

#
#
# End of 1588 CreateManagementErrorTLV routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# Build 1588v2 SendManagementErrorResponse Message
#
def SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, managementErrorId, displayData):
    managementTLV = CreateManagementErrorTLV(managementErrorId, managementId, displayData)
    txpkt_buf = v2ManagementResponsePkt(targetPortIdentity, pkt_sts_1588, actionField, managementTLV, cfg, cfg.ptpHeader, cfg.ptpSuffix)
    txdone = SendPacket(port, txpkt_buf)
    return(txdone)
#
#
# End of 1588 SendManagementErrorResponse routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# GetInsertedTS
#
def GetInsertedTS(rxpkt_buf, ptp_header, cfg, curr_time, local_time_offset):
    #
    approx_time = curr_time - local_time_offset
    approx_sec = approx_time / 1000000000
    sec_len = 0
    TS_list = []
    if (cfg.ts_ins_sec_en):
        sec_len = cfg.ts_ins_sec_len + 1
    # Determine seconds start location
    if (cfg.ts_append):
        pkt_buf = rxpkt_buf
        start_sec = len(rxpkt_buf) - 4 - sec_len  # adjust to remove CRC
        start_ns =  start_sec - 4
    else:
        pkt_buf = ptp_header
        start_sec = cfg.ts_ins_sec_off
        start_ns = cfg.ts_ins_ns_off
    # Get Seconds octets
    if (sec_len != 0):
        TS_list = pkt_buf[start_sec:(start_sec + sec_len)]
    # Get Nanoseconds octets (ignore upper 2 bits)
    TS_list += [pkt_buf[start_ns] & 0x3f] + pkt_buf[(start_ns + 1):(start_ns + 4)]    
    #print "TS_list: ", TS_list
    if (sec_len < 4):
        scale_factor = 2**(8*sec_len) * (10**9)
        while (len(TS_list) < 8): 
            TS_list = [0] + TS_list
        TS_ns = TStoNS(TS_list) + ((approx_time / scale_factor)  * scale_factor)
        CT_ns = (approx_time)
        ts_diff = TS_ns - CT_ns
        if (ts_diff > (scale_factor/2)):
            TS_ns = TS_ns - scale_factor
        if (ts_diff < (-scale_factor/2)):
            TS_ns = TS_ns + scale_factor
    else:
        TS_ns = TStoNS(TS_list)
    return(TS_ns)

#
#
# End of 1588 GetInsertedTS routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Correction field script
#    Convert correction field to integer nanoseconds
def convertCorrField(Corr_Field):
    #
    # Convert to ns
    if (len(Corr_Field) == 8):
        time_subns = (long(Corr_Field[0]) << 56) + (long(Corr_Field[1]) << 48) + (long(Corr_Field[2]) << 40) + (long(Corr_Field[3]) << 32) + (long(Corr_Field[4]) << 24) + (Corr_Field[5] << 16) + (Corr_Field[6] << 8) + (Corr_Field[7])
        if (time_subns >= (2**63)):
            time_subns = time_subns - (2**64)
        time_ns = long(round(time_subns / (2.0**16)))
    else:
        print "convertCorrField: ERROR in Corr_Field", Corr_Field
        time_ns = 0
    return (time_ns)

#
#
# End of convertCorrField routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 V1 configuration script
#    Set basic config parameters
def v1_config(cfg):
    #
    # Set configuration for V1
    cfg.v2_enable = 0
    cfg.l2_enet = 0
    cfg.ipv4_en = 1

#
#
# End of 1588V1 configuration routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 MISR Interrupt check
def check_MISR(xem, phyAddr, int_status, verbose):
    #
    # Check MISR for Interrupt Status
    misr_read_val = MdioRead(xem, phyAddr, MISR, 0)
    int_status = int_status | misr_read_val
    if (verbose):
        print "  MISR Read: %x" % misr_read_val
    return(int_status)

#
#
# End of check_MISR routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 ClearEventQueue
def ClearEventQueue(xem, phyAddr):
    event_sts = MdioRead(xem, phyAddr, PTP_ESTS, 0)
    event_detect = event_sts & 0x01
    while (event_detect):
        event_sts = MdioRead(xem, phyAddr, PTP_ESTS, 0)
        event_detect = event_sts & 0x01
#
# End of 1588 ClearEventQueue routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# 1588 Align1588ClkPhase
# Aligns CLKOUT phase to PPS boundary.
def Align1588ClkPhase(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor):
    # Align ClkOut phase
    phase_error = Avg1588ClkPhase(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor)
    if (phase_error != 0):
        phase_corr_list = NStoTS(phase_error + (2*ref_period))
        AddTime1588(xem, phyAddr, phase_corr_list, 0)
        if (xem.pcf_en):
            Send_PCF(xem)        
        print "Aligning 1588 Clk output:"
        print "   Phase correction = %d" % phase_error
    return (phase_error)
    
#
# End of 1588 Align1588ClkPhase routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Align1588ClkFine
# Aligns CLKOUT phase to PPS boundary.
def Align1588ClkFine(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor, num_samples):
    # Align ClkOut phase
    # Get num_samples measurements of phase_error
    pe_list = []
    low_val = False
    high_val = False
    for cnt in range(num_samples):
        pe_list += [Get1588ClkPhase(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor)]
        if (pe_list[cnt] < 10):
            low_val = True
        if (pe_list[cnt] > (clkout_period - 10)):
            high_val = True
    # Average Phase Error values
    pe_sum = 0
    for cnt in range(num_samples):
        if (low_val & high_val & (pe_list[cnt] < 10)):
            pe_list[cnt] += clkout_period
        pe_sum += pe_list[cnt]
    phase_error = int(round(pe_sum / num_samples))
    if (phase_error >= clkout_period):
        phase_error -= clkout_period
    if (phase_error != 0):
        phase_corr_list = NStoTS(phase_error + (2*ref_period))
        AddTime1588(xem, phyAddr, phase_corr_list, 0)
        if (xem.pcf_en):
            Send_PCF(xem)        
        print "Aligning 1588 Clk output:"
        print "   Phase correction = %d" % phase_error
    return (phase_error)
    
#
# End of 1588 Align1588ClkFine routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Get1588ClkPhase
# Get CLKOUT phase to PPS boundary.  Do not align
def Get1588ClkPhase(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor):
    # Align ClkOut phase
    phase_error = 0
    event_cfg_val = (EVNT_SINGLE | (12 << EVNT_GPIO) | (event_num << 1) | EVNT_WR)
    MdioWrite(xem, phyAddr, PTP_EVNT, event_cfg_val, 0)
    MdioWrite(xem, phyAddr, PTP_EVNT, (EVNT_RISE | event_cfg_val), 0)
    if (xem.pcf_en):
        Send_PCF(xem)
    event_sts = MdioRead(xem, phyAddr, PTP_ESTS, 0)
    event_detect = event_sts & 0x01
    if (event_detect == 0):
        print "Error - PTP_ESTS Read: Event not ready. event_sts = ", event_sts
    else:
        event_num = (event_sts >> 2) & 0x7
        event_mult = (event_sts >> 1) & 0x1
        event_rf = (event_sts >> 5) & 0x1
        event_ts_len = ((event_sts >> 6) & 0x3) + 1
        events_missed = (event_sts >> 8) & 0x7
        if (event_mult):
            event_ext_sts = MdioRead(xem, phyAdr, PTP_EDATA, 0)
        else:
            event_ext_sts = 0
        event_TS = TStoNS(GetEventTS(xem, phyAddr, 0)) - event_corr_factor
        phase_error = clkout_period - (event_TS % clkout_period)
        if (phase_error == clkout_period):
            phase_error = 0
        #print "Phase error for 1588 Clk output: %d" % phase_error
    # Disable Event and Clear Event Queue (only needed for rev A1)
    if (cfg.dp83640_mdl_rev == 0):
        event_cfg_val = ((event_num << 1) | EVNT_WR)
        MdioWrite(xem, phyAddr, PTP_EVNT, event_cfg_val, 0)
        if (xem.pcf_en):
            Send_PCF(xem)
        ClearEventQueue(xem, phyAddr)
    return (phase_error)
    
#
# End of 1588 Get1588ClkPhase routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588 Avg1588ClkPhase
# Get CLKOUT phase to PPS boundary.  Do not align
# Average of 8 sequential measurements
def Avg1588ClkPhase(xem, phyAddr, event_num, ref_period, clkout_period, event_corr_factor):
    # Align ClkOut phase
    phase_error = 0
    event_cfg_val = ((12 << EVNT_GPIO) | (event_num << 1) | EVNT_WR)
    MdioWrite(xem, phyAddr, PTP_EVNT, event_cfg_val, 0)
    MdioWrite(xem, phyAddr, PTP_EVNT, (EVNT_RISE | event_cfg_val), 0)
    if (xem.pcf_en):
        Send_PCF(xem)
    event_cnt = 0
    while (event_cnt < 8):
        event_sts = MdioRead(xem, phyAddr, PTP_ESTS, 0)
        event_detect = event_sts & 0x01
        if (event_detect):
            event_num = (event_sts >> 2) & 0x7
            event_mult = (event_sts >> 1) & 0x1
            event_rf = (event_sts >> 5) & 0x1
            event_ts_len = ((event_sts >> 6) & 0x3) + 1
            events_missed = (event_sts >> 8) & 0x7
            if (event_mult):
                event_ext_sts = MdioRead(xem, phyAdr, PTP_EDATA, 0)
            else:
                event_ext_sts = 0
            event_TS = TStoNS(GetEventTS(xem, phyAddr, 0)) - event_corr_factor
            if (event_cnt == 0):
                phase_error0 = clkout_period - (event_TS % clkout_period)
                delta_list = [0]
                TS0 = event_TS
            else:
                delta_list += [event_TS - TS0 - (event_cnt * clkout_period)]
            event_cnt += 1
    #print "phase_error0: ", phase_error0
    #print "delta_list: ", delta_list
    delta_sum = 0
    for event_cnt in range(8):
        delta_sum += delta_list[event_cnt]
    delta_avg = int(round(delta_sum/8.0))
    phase_error = phase_error0 - delta_avg
    if (phase_error > clkout_period):
        phase_error = phase_error - clkout_period
    print "Phase error for 1588 Clk output: %d" % phase_error
    # Disable Event and Clear Event Queue
    event_cfg_val = ((event_num << 1) | EVNT_WR)
    MdioWrite(xem, phyAddr, PTP_EVNT, event_cfg_val, 0)
    if (xem.pcf_en):
        Send_PCF(xem)
    ClearEventQueue(xem, phyAddr)
    return (phase_error)
    
#
# End of 1588 Avg1588ClkPhase routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# GetAdjustDoneFlag
# Returns 1 if the Adjust_Done flag is set in the inserted timestamp
# for a received 1588 event message
#
def GetAdjustDoneFlag(packet_sts, cfg, verbose):
    #
    # Get AdjustDoneFlag from Nanoseconds[31]
    if (cfg.ts_append):
        sec_len = 0
        if (cfg.ts_ins_sec_en):
            sec_len = cfg.ts_ins_sec_len + 1
        adjust_done_byte = packet_sts.extra_bytes[len(packet_sts.extra_bytes) - 4 - sec_len]
    else:
        adjust_done_byte = packet_sts.header[cfg.ts_ins_ns_off]
    adjust_done = (adjust_done_byte >> 7) == 1
    if (verbose & adjust_done):
        print "Info: Adjust_done flag set"
    return(adjust_done)

#
#
# End of 1588 GetAdjustDoneFlag routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# ConfigPTP_TX script
#
def ConfigPTP_TX(xem, phyAddr, enable_txts, cfg):
        # Enable Transmit Timestamp operation
        txcfg0_val = 0
        if (enable_txts):
            txcfg0_val |= epl.TXOPT_TS_EN
        if (cfg.sync_1step):
            txcfg0_val |= epl.TXOPT_SYNC_1STEP
        if (cfg.tx_chk_1step):
            txcfg0_val |= epl.TXOPT_CHK_1STEP
        if (cfg.dr_insert & (cfg.portDS.delayMechanism == DELAY_E2E) & (cfg.portDS.portState != PORT_MASTER)):
            txcfg0_val |= epl.TXOPT_DR_INSERT
            cfg.dr_insert_enabled = 1
        else:
            cfg.dr_insert_enabled = 0
        if (cfg.ipv4_en):
            txcfg0_val |= (epl.TXOPT_IP1588_EN | epl.TXOPT_IPV4_EN )
        if (cfg.l2_enet):
            txcfg0_val |= (epl.TXOPT_L2_EN)
        if (cfg.ipv6_en):
            txcfg0_val |= (epl.TXOPT_IP1588_EN | epl.TXOPT_IPV6_EN)
        xem.PTPSetTransmitConfig(txcfg0_val, cfg.portDS.versionNumber, cfg.byte0_mask, cfg.byte0_data)

#
# End of ConfigPTP_TX routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# ConfigPTP_RX script
#
def ConfigPTP_RX(xem, phyAddr, enable_rxts, cfg):
        # Enable Transmit Timestamp operation
        rxCfgOpts = 0
        if (cfg.defaultDS.slaveOnly):
            rxCfgOpts |= epl.RXOPT_RX_SLAVE
        if (enable_rxts):
            rxCfgOpts |= epl.RXOPT_RX_TS_EN
        if (cfg.ip1588_en0):
            rxCfgOpts |= epl.RXOPT_IP1588_EN0
        if (cfg.ip1588_en1):
            rxCfgOpts |= epl.RXOPT_IP1588_EN1
        if (cfg.ip1588_en2):
            rxCfgOpts |= epl.RXOPT_IP1588_EN2
        if (cfg.user_ip_en):
            rxCfgOpts |= epl.RXOPT_USER_IP_EN
        if (cfg.ipv4_en):
            rxCfgOpts |= epl.RXOPT_RX_IPV4_EN
        if (cfg.l2_enet):
            rxCfgOpts |= epl.RXOPT_RX_L2_EN
        if (cfg.ipv6_en):
            rxCfgOpts |= epl.RXOPT_RX_IPV6_EN
        if (cfg.rx_hash_en):
            rxCfgOpts |= epl.RXOPT_SRC_ID_HASH_EN
        if (cfg.acc_udp):
            rxCfgOpts |= epl.RXOPT_ACC_UDP
        if (cfg.acc_crc):
            rxCfgOpts |= epl.RXOPT_ACC_CRC
        if (cfg.ts_ins_sec_en):
            rxCfgOpts |= epl.RXOPT_TS_SEC_EN
        if (cfg.ts_insert):
            rxCfgOpts |= epl.RXOPT_TS_INSERT
            if (cfg.ts_append):
                rxCfgOpts |= epl.RXOPT_TS_APPEND
        
        rx_Cfg_Items = xem.RX_CFG_ITEMS()
        if (cfg.versionPTP_en):
            rx_Cfg_Items.ptpVersion = cfg.portDS.versionNumber
        else:
            rx_Cfg_Items.ptpVersion = 0
        rx_Cfg_Items.ptpDomain = cfg.defaultDS.domainNumber
        rx_Cfg_Items.ptpFirstByteData = cfg.rx_byte0_data
        rx_Cfg_Items.ptpFirstByteMask = cfg.rx_byte0_mask
        if (cfg.user_ip_en):
            rx_Cfg_Items.ipAddrData = cfg.user_ip_addr
        rx_Cfg_Items.rxTsNanoSecOffset = cfg.ts_ins_ns_off
        rx_Cfg_Items.rxTsSecondsOffset = cfg.ts_ins_sec_off
        rx_Cfg_Items.srcIdHash = cfg.ptp_rxhash
        rx_Cfg_Items.tsMinIFG = cfg.ts_min_ifg
        rx_Cfg_Items.tsSecLen = cfg.ts_ins_sec_len
        
        xem.PTPSetReceiveConfig(rxCfgOpts, rx_Cfg_Items)

#
# End of ConfigPTP_RX routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# GetMacStats
# Get Receive stats from MAC
#
def GetMacStats(xem, verbose):
    #
    # Get Address and Bytecount
    ok_functions.OkAlpIf.UpdateWireOuts()
    crc_err_cnt = (ok_functions.OkAlpIf.GetWireOutValue(0x26))
    rx_runt_cnt = (ok_functions.OkAlpIf.GetWireOutValue(0x27))
    rx_er_cnt = (ok_functions.OkAlpIf.GetWireOutValue(0x28))
    missed_pkt_cnt = (ok_functions.OkAlpIf.GetWireOutValue(0x29))
    rx_packets = (ok_functions.OkAlpIf.GetWireOutValue(0x2A))
    if(verbose):
        print "Packet Error Counts"
        print "   CRC Errors:   %d" % crc_err_cnt
        print "   Runt Errors:  %d" % rx_runt_cnt
        print "   RX_ER Errors: %d" % rx_er_cnt
        print "   RX Missed Pkts: %d" % missed_pkt_cnt
        print "   RX Pkts: %d" % rx_packets
    #
    Error_list = [crc_err_cnt, rx_runt_cnt, rx_er_cnt, missed_pkt_cnt, rx_packets]
    #
    return Error_list

#
# End of GetRxStats routine
# ------------------------------------------------------------------
    

# -------------------------------------------------------------------
# Print_TS
# Print timestamp in seconds, ns
#
def Print_TS(timestamp):
    if (timestamp < 0):
        sign = "-"
    else:
        sign = ""
    timestamp_abs = abs(timestamp)
    sec_val = timestamp_abs/(10**9)
    ns_val = timestamp_abs - (sec_val * (10**9))
    new_string = "%dsec, %9dns" % (sec_val, ns_val)
    return(new_string)

#
# End of GetRxStats routine
# ------------------------------------------------------------------
 
# -------------------------------------------------------------------
# CompareTS script
# verifies Timestamp matches packet (seqID, mtype, sourceHash)
#
def CompareTS(timestamp, pkt_sts_1588):
    #
    if (pkt_sts_1588.versionPTP == 1):
        mtype_match = (timestamp.mtype == pkt_sts_1588.control)
    else:
        mtype_match = (timestamp.mtype == pkt_sts_1588.messageType)
    sourceHash_match = (timestamp.sourceHash == pkt_sts_1588.src_hash)
    seqID_match = (timestamp.seqID == pkt_sts_1588.seqID)
    #
    return (mtype_match & sourceHash_match & seqID_match & timestamp.ok)

#
#
# End of CompareTS routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# FlushTimestamps script
#
def FlushTimestamps(port, phyAddr):
    return_val = 0
    ptp_sts_val = MdioRead(port, phyAddr, PTP_STS, 0)
    tmp_cnt = 0
    while (ptp_sts_val & (RXTS_RDY | PTP_TXTS_RDY)):
        if ((ptp_sts_val & RXTS_RDY) == RXTS_RDY):
            GetRxTimestamp_tmp(port, phyAddr, 0)
        if ((ptp_sts_val & PTP_TXTS_RDY) == PTP_TXTS_RDY):
            GetTxTimestamp(port, phyAddr, 0)
        tmp_cnt = tmp_cnt + 1
        if (tmp_cnt > 10):
            print "Unable to Clear Timestamps"
            return_val = 1
            break
        ptp_sts_val = MdioRead(port, phyAddr, PTP_STS, 0)    
    return(return_val)

#
#
# End of FlushTimestamps routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# FlushTxTimestamps script
#
def FlushTxTimestamps(port, phyAddr):
    return_val = 0
    ptp_sts_val = MdioRead(port, phyAddr, PTP_STS, 0)
    tmp_cnt = 0
    while (ptp_sts_val & (PTP_TXTS_RDY)):
        GetTxTimestamp(port, phyAddr, 0)
        tmp_cnt = tmp_cnt + 1
        if (tmp_cnt > 10):
            print "Unable to Clear Timestamps"
            return_val = 1
            break
        ptp_sts_val = MdioRead(port, phyAddr, PTP_STS, 0)    
    return(return_val)

#
#
# End of FlushTxTimestamps routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# CheckPktReady script
#
def CheckPktReady(port):
        rxpkt_buf = []
        rxpkt_buf = GetRXPkt(port, 0)
        if len( rxpkt_buf):
            rxpkt_rdy = True
        else:
            rxpkt_rdy = False
        return (rxpkt_rdy, rxpkt_buf)

#
#
# End of CheckPktReady routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# AnnounceRcvd script
#
def AnnounceRcvd(port, cfg, pkt_sts_1588, verbose):
    if (verbose):
        print "Announce Received: "
        print "   port_id = ", pkt_sts_1588.sourcePortIdentity
        print "   seq_id = ", pkt_sts_1588.seqID
        print "   grandmaster = %x %x %x %x %x %x %x %x" % (pkt_sts_1588.body[19], pkt_sts_1588.body[20], pkt_sts_1588.body[21], pkt_sts_1588.body[22], pkt_sts_1588.body[23], pkt_sts_1588.body[24], pkt_sts_1588.body[25], pkt_sts_1588.body[26])
    if ((cfg.portDS.portState != PORT_DISABLED) and (cfg.portDS.portState != PORT_INITIALIZING)):
        # If matches current master, update parentDS
        if ((cfg.portDS.portState == PORT_SLAVE) and (pkt_sts_1588.sourcePortIdentity == cfg.parentDS.parentPortIdentity)):
            RestartAnnounceReceiptTO(port, cfg)
            cfg.currentDS.stepsRemoved = pkt_sts_1588.FM_entry.stepsRemoved + 1
            cfg.parentDS.grandmasterIdentity = pkt_sts_1588.FM_entry.grandmasterIdentity
            cfg.parentDS.grandmasterPriority1 = pkt_sts_1588.FM_entry.grandmasterPriority1
            cfg.parentDS.grandmasterPriority2 = pkt_sts_1588.FM_entry. grandmasterPriority2
            cfg.parentDS.grandmasterClockQuality.clockClass = pkt_sts_1588.FM_entry.grandmasterClockQuality.clockClass
            cfg.parentDS.grandmasterClockQuality.clockAccuracy = pkt_sts_1588.FM_entry.grandmasterClockQuality.clockAccuracy
            cfg.parentDS.grandmasterClockQuality.offsetScaledLogVariance = pkt_sts_1588.FM_entry.grandmasterClockQuality.offsetScaledLogVariance
            cfg.parentDS.parentPortIdentity = pkt_sts_1588.FM_entry.sourcePortIdentity
            cfg.timePropertiesDS.currentUtcOffset = pkt_sts_1588.FM_entry.currentUtcOffset
            cfg.timePropertiesDS.currentUtcOffsetValid = (pkt_sts_1588.FM_entry.flagField & 0x04)           
            cfg.timePropertiesDS.leap59 = (pkt_sts_1588.FM_entry.flagField & 0x01)
            cfg.timePropertiesDS.leap61 = (pkt_sts_1588.FM_entry.flagField & 0x02)
            cfg.timePropertiesDS.timeTraceable = (pkt_sts_1588.FM_entry.flagField & 0x10)
            cfg.timePropertiesDS.frequencyTraceable = (pkt_sts_1588.FM_entry.flagField & 0x20)
            cfg.timePropertiesDS.ptpTimescale = (pkt_sts_1588.FM_entry.flagField & 0x08)
            cfg.timePropertiesDS.timeSource = pkt_sts_1588.FM_entry.timeSource
            UpdateFM_DS(port.E_rbest, pkt_sts_1588.FM_entry)
        else:
            fm_match, fm_num = IsKnownFM(cfg.foreignMasterDS, pkt_sts_1588.FM_entry)
            if (fm_match):
                UpdateFM_DS(cfg.foreignMasterDS[fm_num], pkt_sts_1588.FM_entry)
            else:
                # Add Foreign Master to data set
                cfg.foreignMasterDS += [pkt_sts_1588.FM_entry]
    return(0)

#
#
# End of AnnounceRcvd routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# SignalingRcvd script
#
def SignalingRcvd(pkt_sts_1588, sendPortId, verbose):
    if (verbose):
        if (pkt_sts_1588.body == sendPortId):
            print "   targetPortIdentity matches: ", pkt_sts_1588.body
            print "   TLVs : ", pkt_sts_1588.suffix
        else:
            print "   targetPortIdentity = ", pkt_sts_1588.body
    return(0)

#
#
# End of SignalingRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PdelayRespRcvd script
#
def PdelayRespRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if ((cfg.portDS.portState != PORT_DISABLED) and (cfg.portDS.portState != PORT_INITIALIZING)):
        port.pdelay_req.resp_rcvd = 0
        if (pkt_sts_1588.pdelay_resp_ok):
            if (cfg.portDS.delayMechanism != DELAY_P2P):
                print "WARNING: PDelay_Resp received: Peer Delay not enabled"
                pkt_sts_1588.pdelay_resp_ok = 0
            else:
                if (not port.pdelay_req.sent):
                    print "WARNING: PDelay_Resp: PDelay_Req not sent"
                    pkt_sts_1588.pdelay_resp_ok = 0
                else:
                    if (pkt_sts_1588.reqSourceSeqID != cfg.pdelayreq_seqID):
                        print "PDelay_Resp: SeqID does not match most recent PDelay_Req"
                        pkt_sts_1588.pdelay_resp_ok = 0
                        #break
        if (pkt_sts_1588.pdelay_resp_ok):
            port.pdelay_req.t2 = TStoNS(pkt_sts_1588.rcvdTS)
            port.pdelay_req.resp_2step = pkt_sts_1588.two_step
            port.pdelay_req.resp_corr = pkt_sts_1588.corr_field 
            port.pdelay_req.resp_rcvd = 1
            port.pdelay_req.t4 = pkt_sts_1588.packet_timestamp
            if (verbose & port.pdelay_req.resp_rcvd):
                print "PDelay_Resp received, seqId:", pkt_sts_1588.seqID
                print "... PDelay_Req sent:", Print_TS(port.pdelay_req.t1)
                print "... PDelay_Req rcvd:", Print_TS(port.pdelay_req.t2)
                print "... PDelay_Resp rcvd:", Print_TS(port.pdelay_req.t4)
                print "... PDelay_Resp corr:", port.pdelay_req.resp_corr
        return(0)
    else:
        return(0)
#
#
# End of PdelayRespRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PdelayRespFollowRcvd script
#
def PdelayRespFollowRcvd(port, cfg, pkt_sts_1588, verbose):
    if ((cfg.portDS.portState != PORT_DISABLED) and (cfg.portDS.portState != PORT_INITIALIZING)):
        if (pkt_sts_1588.pdelay_follow_ok):
            if (cfg.portDS.delayMechanism != DELAY_P2P):
                print "WARNING: PDelay_Resp_FollowUp received: Peer Delay not enabled"
                pkt_sts_1588.pdelay_follow_ok = 0
            else:
                if (not port.pdelay_req.resp_rcvd):
                    print "WARNING: PDelay_Resp_Followup: PDelay_Resp not received"
                    pkt_sts_1588.pdelay_follow_ok = 0
                else:
                    if (pkt_sts_1588.reqSourceSeqID != cfg.pdelayreq_seqID):
                        print "PDelay_Resp_Followup: SeqID does not match most recent PDelay_Req"
                        pkt_sts_1588.pdelay_follow_ok = 0
        if (pkt_sts_1588.pdelay_follow_ok):
            port.pdelay_req.t3 = TStoNS(pkt_sts_1588.rcvdTS)
            port.pdelay_req.follow_corr = pkt_sts_1588.corr_field 
            pdelay_follow_seqId = pkt_sts_1588.seqID
            if (verbose):
                print "PDelay_Resp_Followup Received:", pdelay_follow_seqId
                print "... PDelay_Resp_Followup seqId:", pdelay_follow_seqId
                print "... PDelay_Resp sent:", Print_TS(port.pdelay_req.t3)
        return(0)
    else:
        return(0)
#
#
# End of PdelayRespFollowRcvd routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# PdelayReqRcvd script
#
def PdelayReqRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if ((cfg.portDS.portState != PORT_DISABLED) and (cfg.portDS.portState != PORT_INITIALIZING)):
        if (cfg.portDS.delayMechanism != DELAY_P2P):
                pkt_sts_1588.pdelay_req_ok = 0
                print "WARNING:  PDelay_Req received, PDelay mechanism not enabled"
                return(0)
        if (pkt_sts_1588.pdelay_req_ok):
            port.pdelay_resp.req_rcvd_time = pkt_sts_1588.packet_timestamp
        if (pkt_sts_1588.pdelay_req_ok):
            if (verbose):
                print "PDelay_Req received at", Print_TS(port.pdelay_resp.req_rcvd_time)
        if (port.pdelay_resp.sent):
            print "WARNING:  PDelay_Req ignored, previous PDelay_Resp not complete"
            pkt_sts_1588.pdelay_req_ok = 0
        else:
            # Generate PDelay_Resp packet
            pdelay_resp_buf = v2PDelayRespPkt(NStoTS(port.pdelay_resp.req_rcvd_time), cfg, cfg.ptpHeader, pkt_sts_1588, cfg.ptpSuffix)
            txdone = SendPacket(port, pdelay_resp_buf)
            if (not txdone):
                print "FAILED: PDelay_Resp never completed"
            # Generate PDelay_Resp_FollowUp with TS of 0
            cfg.pdelay_follow_msg = v2_PDelayRespFU_Message(NStoTS(0), cfg, cfg.ptpHeader, pkt_sts_1588, cfg.ptpSuffix)
            #
            port.pdelay_resp.sent = 1
            port.pdelay_resp.wait4TS = 1
            port.txts.sent_list += [mtype_pdelay_resp]
            #
        return(0)
    else:
        return(0)
#
#
# End of PdelayReqRcvd routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# SyncRcvd script
#
def SyncRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if (cfg.portDS.portState != PORT_SLAVE) and (cfg.portDS.portState != PORT_UNCALIBRATED):
        if (verbose):
            print "Sync ignored, not in SLAVE/UNCALIBRATED state"
        pkt_sts_1588.sync_ok = 0
        if (port.time_adjust_pending):
            port.time_adjust_pending = not GetAdjustDoneFlag(pkt_sts_1588, cfg, verbose)
        return(0)
    else:
        if (cfg.v2_enable):
            if (pkt_sts_1588.domain != cfg.defaultDS.domainNumber):
                print "Sync : domain does not match"
                pkt_sts_1588.sync_ok = 0
                if (port.time_adjust_pending):
                    port.time_adjust_pending = not GetAdjustDoneFlag(pkt_sts_1588, cfg, verbose)
            if (pkt_sts_1588.sourcePortIdentity != cfg.parentDS.parentPortIdentity):
                print "Sync: sourcePortIdentity does not match parentPortIdentity"
                print "   reqPortId: ", pkt_sts_1588.sourcePortIdentity
                pkt_sts_1588.sync_ok = 0
        if (pkt_sts_1588.sync_ok):
            port.slave.sync_seqID = pkt_sts_1588.seqID
            if (verbose):
                print "Master IP:", rxpkt_buf[26:30]
                print "Domain:", pkt_sts_1588.domain
            if (not cfg.v2_enable):
                cfg.v1_parent_stats = [0] + pkt_sts_1588.header[21:28] +[0,0] + pkt_sts_1588.header[28:30]
                cfg.v1_grandmaster_stats = pkt_sts_1588.body[12:40]
                cfg.v1_sync_interval = pkt_sts_1588.body[43]
                cfg.v1_local_steps_removed = (pkt_sts_1588.body[50] << 8) + pkt_sts_1588.body[51] + 1
            port.slave.sync_rcvd = 1
            port.slave.sync_rcvd_time = pkt_sts_1588.packet_timestamp
            port.slave.sync_rcvd_cf = pkt_sts_1588.corr_field
            port.slave.follow_cf = 0
            if (verbose):
                print "... sync correct field : ", pkt_sts_1588.corr_field
            # Check PTP_ASSIST flag
            port.slave.two_step = pkt_sts_1588.two_step
            if ((port.slave.two_step == 0) & port.slave.sync_rcvd):
                port.slave.sync_sent_time = TStoNS(pkt_sts_1588.sync_originTS)
                port.slave.sync_complete = 1
                if (verbose):
                    print "Sync Sent: ", Print_TS(port.slave.sync_sent_time)
                if (port.slave.sync_sent_time == 0):
                    print "WARNING: Sync Origin TS (1-step) = 0"
                    return(1)
            if (port.slave.sync_rcvd):
                if (verbose):
                    print "Sync Received, seqID: %d,  Time: %s" %(port.slave.sync_seqID, Print_TS(port.slave.sync_rcvd_time))
                # get sync interval
                if (cfg.v2_enable & (port.slave.log_mean_sync_interval != pkt_sts_1588.logInterval)):
                    port.slave.log_mean_sync_interval = pkt_sts_1588.logInterval
                    print "New Sync Interval: %f seconds" % (2.0**port.slave.log_mean_sync_interval)
        return(0)
#
#
# End of SyncRcvd routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# FollowRcvd script
#
def FollowRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if (cfg.portDS.portState != PORT_SLAVE) and (cfg.portDS.portState != PORT_UNCALIBRATED):
        if (verbose):
            print "FollowUp ignored, not in SLAVE/UNCALIBRATED state"
        pkt_sts_1588.follow_ok = 0
        return(0)
    else:
        if (pkt_sts_1588.follow_ok & (not port.slave.sync_rcvd)):
            print "WARNING: Ignoring Follow-up, Sync not received yet"
            pkt_sts_1588.follow_ok = 0
        if (pkt_sts_1588.follow_ok & (not port.slave.two_step)):
            print "WARNING: Unexpected Follow-up, Sync was one-step"
            pkt_sts_1588.follow_ok = 0
        if (pkt_sts_1588.follow_ok & cfg.v2_enable):
            if (pkt_sts_1588.domain != cfg.defaultDS.domainNumber):
                print "FollowUp : domain does not match"
                pkt_sts_1588.follow_ok = 0
            if (pkt_sts_1588.sourcePortIdentity != cfg.parentDS.parentPortIdentity):
                print "FollowUp: sourcePortIdentity does not match parentPortIdentity"
                print "   reqPortId: ", pkt_sts_1588.sourcePortIdentity
                pkt_sts_1588.follow_ok = 0
        if (pkt_sts_1588.follow_ok):
            port.slave.sync_complete = 1
            port.slave.sync_sent_time = TStoNS(pkt_sts_1588.sync_originTS)
            port.slave.follow_cf = pkt_sts_1588.corr_field
            if (debug_TS):
                print "Follow_Up received: ", pkt_sts_1588.fu_assocSeqId
            if (debug_TS):
                print "... follow-up correct Field : ", port.slave.follow_cf
                print "... Sync Sent:", Print_TS(port.slave.sync_sent_time)
            if (pkt_sts_1588.fu_assocSeqId != port.slave.sync_seqID):
                print "  Assoc Seq ID:", pkt_sts_1588.fu_assocSeqId
                print "  ERROR: FollowUp does not match Sync"
                port.slave.sync_rcvd = 0
                port.slave.sync_complete = 0
        return(0)
#
#
# End of FollowRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# DelayReqRcvd script
#
def DelayReqRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if (cfg.portDS.portState != PORT_MASTER):
        if (verbose):
            print "Delay Request ignored, not in MASTER state"
        pkt_sts_1588.delay_req_ok = 0
        if (port.time_adjust_pending):
            port.time_adjust_pending = not GetAdjustDoneFlag(pkt_sts_1588, cfg, verbose)
        return(0)
    else:
        if (cfg.portDS.delayMechanism != DELAY_E2E):
            print "WARNING: Unexpected Delay_Req packet received"
            pkt_sts_1588.delay_req_ok = 0
        if (pkt_sts_1588.delay_req_ok):
            port.master.delay_req_time = pkt_sts_1588.packet_timestamp
        if (pkt_sts_1588.delay_req_ok):
            if (verbose):
                print "Delay_Req received at", Print_TS(port.master.delay_req_time)
            # Generate Delay_Resp packet
            delay_resp_buf = v2DelayRespPkt(NStoTS(port.master.delay_req_time), cfg, cfg.ptpHeader, pkt_sts_1588, cfg.ptpSuffix)
            txdone = SendPacket(port, delay_resp_buf)
            if (verbose):
                print "Delay_Resp sent"
            if (not txdone):
                print "FAILED: Delay_Resp never completed"
        return(0)
#
#
# End of DelayReqRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# DelayRespRcvd script
#
def DelayRespRcvd(port, phyAddr, cfg, rxpkt_buf, pkt_sts_1588, verbose):
    if (cfg.portDS.portState != PORT_SLAVE) and (cfg.portDS.portState != PORT_UNCALIBRATED):
        if (verbose):
            print "Delay Resp ignored, not in SLAVE/UNCALIBRATED state"
        pkt_sts_1588.delay_resp_ok = 0
        return(0)
    else:
        if (pkt_sts_1588.delay_resp_ok & (not port.slave.delay_req_sent)):
            if (verbose):
                print "WARNING: Unexpected Delay_Resp, Delay_Req not sent"
            pkt_sts_1588.delay_resp_ok = 0
        if (pkt_sts_1588.delay_resp_ok):
            if (pkt_sts_1588.reqSourceSeqID != cfg.delayreq_seqID):
                print "Delay_Resp: SeqID does not match most recent Delay_Req"
                pkt_sts_1588.delay_resp_ok = 0
            if (pkt_sts_1588.reqPortId != port.sendPortId):
                print "Delay_Resp: Req Port ID does not match"
                print "   reqPortId: ", pkt_sts_1588.reqPortId
                pkt_sts_1588.delay_resp_ok = 0
        if (pkt_sts_1588.delay_resp_ok & cfg.v2_enable):
            if (pkt_sts_1588.sourcePortIdentity != cfg.parentDS.parentPortIdentity):
                print "Delay_Resp: sourcePortIdentity does not match parentPortIdentity"
                print "   reqPortId: ", pkt_sts_1588.sourcePortIdentity
                pkt_sts_1588.delay_resp_ok = 0
        if (pkt_sts_1588.delay_resp_ok):
            cfg.portDS.logMinDelayReqInterval = pkt_sts_1588.logInterval
            port.slave.delay_rcvd_time = TStoNS(pkt_sts_1588.rcvdTS)
            delay_resp_seqId = pkt_sts_1588.seqID
            if (cfg.dr_insert):
                port.slave.delay_sent_time = pkt_sts_1588.packet_timestamp
            else:
                if (port.slave.delay_req_wait4TS):
                    print "ERROR: No Delay_Req Transmit TS received"
                    pkt_sts_1588.delay_resp_ok = 0
                    return(1)
                else:
                    pkt_sts_1588.packet_timestamp = port.slave.delay_sent_time
            if (verbose):
                print "Delay_Req sent:", Print_TS(port.slave.delay_sent_time)
                print "Delay_Req rcvd:", Print_TS(port.slave.delay_rcvd_time)
                print "Delay_Resp seqId:", delay_resp_seqId
            port.slave.delay_req_sent = 0
            port.slave.delay_resp_cf = pkt_sts_1588.corr_field
            if (verbose):
                print "... delay_resp correction : ", port.slave.delay_resp_cf
        return(0)
#
#
# End of DelayRespRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# ManagementRcvd script
#
def ManagementRcvd(port, cfg, pkt_sts_1588, sendPortId, verbose):
    if (verbose): print "Management Message Received: "
    # Parse message
    targetPortIdentity = pkt_sts_1588.body[0:10]
    startingBoundaryHops = pkt_sts_1588.body[10]
    boundaryHops = pkt_sts_1588.body[11]
    actionField = pkt_sts_1588.body[12] & 0xf
    mgntTLV = pkt_sts_1588.suffix

    # Validate Message
    all_ports = 0
    all_clocks = 0
    clock_match = 0
    selected_port = 0
    if (targetPortIdentity[0:8] == [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]):
        all_clocks = 1
        if (verbose): print "... all clocks selected"
    if (targetPortIdentity[0:8] == cfg.defaultDS.clockIdentity):
        clock_match = 1
        if (verbose): print "... local clock selected"
    if (all_clocks or clock_match):
        if (targetPortIdentity[8:10] == [0xff, 0xff]):
            all_ports = 1
            if (verbose): print "... all ports selected"
        else:
            if (verbose): print "targetPortIdentity", targetPortIdentity
            xem.targetPortIdentity = targetPortIdentity
            selected_port = (targetPortIdentity[8] << 8) | targetPortIdentity[9]
            if (verbose): print "... selected port number = %d" % selected_port
        if (verbose): print "   Action = ", mgnt_action[pkt_sts_1588.mgnt_action]
        tlv_type = (mgntTLV[0] << 8) + mgntTLV[1]
        tlv_len = (mgntTLV[2] << 8) + mgntTLV[3]
        tlv_managementId = (mgntTLV[4] << 8) + mgntTLV[5]
        tlv_dataField = []
        if (tlv_len != len(mgntTLV) - 4):
            print "ERROR - TLV length error"
            print "   lengthField = %d" % tlv_len
            print "   data length = %d" % len(mgntTLV)
            # Send Error Response
            managementErrorId = MANAGEMENT_ERROR_ID.WRONG_LENGTH
            # Set targetPortIdentity to respond to the source of the message
            targetPortIdentity = pkt_sts_1588.sourcePortIdentity
            # For reply to COMMAND, use ACKNOWLEDGE action, otherwise use RESPONSE
            if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND):
                actionField = MANAGEMENT_ACTION_FIELD.ACKNOWLEDGE
            else:
                actionField = MANAGEMENT_ACTION_FIELD.RESPONSE
            displayData = []
            txdone = SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, tlv_managementId, managementErrorId, displayData)
        if (tlv_len > 2):
            tlv_dataField = mgntTLV[6:(4 + tlv_len)]
        if (tlv_type == TLV_TYPE.MANAGEMENT):
            if (verbose):
                print "   TLV Length : ", tlv_len
                if (mgntID_str(tlv_managementId) == ''):
                    print "   managementId : 0x%x"% tlv_managementId
                else:
                    print "   managementId : %s"% mgntID_str(tlv_managementId)
                print "   TLV Data : ", tlv_dataField
            if ((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND)):
                ManagementResponse(port, cfg, pkt_sts_1588, tlv_managementId, tlv_dataField)
    else:
        if(verbose): print "... Local clock not selected"
    return(0)

#
#
# End of ManagementRcvd routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# 1588v2 PTP v2 Management Resonse Packet
#
def v2ManagementResponsePkt(targetPortIdentity, pkt_status, actionField, managementTLV, cfg, ptpHeader, ptpSuffix):
    #
    ptpHeader.correctionField = [0, 0, 0, 0, 0, 0, 0, 0]
    ptpHeader.logInterval = 0x7f
    # Use original sequence Id
    sequenceId = pkt_status.seqID
    #
    ptp_message = v2_Management_Message(targetPortIdentity, sequenceId, actionField, managementTLV, cfg, ptpHeader, ptpSuffix)
    if (verbose):
        print "v2ManagementResponsePkt:  targetPortidentity = ", targetPortIdentity    
        print ".. ptp_message = ", ptp_message
        print ".. managementTLV = ", managementTLV
    #
    if (cfg.l2_enet):
        mac_hdr = cfg.mac_DA + cfg.mac_SA + [(cfg.l2_etype >> 8), (cfg.l2_etype & 0xff)]
        udp_dest_port = 0
        ip_dest_addr = []
    if (cfg.ipv4_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv4_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x08, 0x00]
    if (cfg.ipv6_en):
        udp_dest_port = 320
        ip_dest_addr = cfg.ipv6_dest_addr
        mac_hdr = cfg.ipv4_mac_DA + cfg.mac_SA + [0x86, 0xDD]
    management_pkt = Build_v2_Pkt(cfg, ptp_message, udp_dest_port, ip_dest_addr, mac_hdr)
    #
    return(management_pkt)

#
#
# End of 1588 v2ManagementResponsePkt routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# ManagementResponse script
#
def ManagementResponse(port, cfg, pkt_sts_1588, managementId, dataField):
    from time import time
    # Set targetPortIdentity to respond to the source of the message
    targetPortIdentity = pkt_sts_1588.sourcePortIdentity
    #
    # For reply to COMMAND, use ACKNOWLEDGE action, otherwise use RESPONSE
    if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND):
        actionField = MANAGEMENT_ACTION_FIELD.ACKNOWLEDGE
    else:
        actionField = MANAGEMENT_ACTION_FIELD.RESPONSE
    #
    # Respond based on actionField TLV managementId
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND)) and (managementId == MANAGEMENT_ID.NULL)):
        # GET, SET, COMMAND NULL
        # Respond with no datafield
        dataField = []
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.CLOCK_DESCRIPTION)):
        # SET CLOCK_DESCRIPTION not supported
        if (verbose): print "Set CLOCK_DESCRIPTION not supported"
        managementErrorId = MANAGEMENT_ERROR_ID.NOT_SETABLE
        displayData = []
        #
        txdone = SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, managementErrorId, displayData)
        return(0)          
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.CLOCK_DESCRIPTION)):
        # GET CLOCK_DESCRIPTION
        # Respond with Clock Description
        #
        dataField = [0, 1]  # Ordinary clock
        dataField += CreatePTPText("IEEE 802.3")
        dataField += [0, 6]
        dataField += cfg.mac_SA
        if (cfg.l2_enet):
            networkProtocol = [0, 3] + [0, 6] + cfg.mac_SA
        if (cfg.ipv4_en):
            networkProtocol = [0, 1] + [0, 4] + cfg.ipv4_src_addr
        if (cfg.ipv6_en):
            networkProtocol = [0, 2] + [0, 16] + cfg.ipv6_src_addr
        dataField += networkProtocol
        # Manuf identity
        dataField += cfg.mac_SA[0:3]
        # Product Description
        prod_desc = "National Semiconductor;DP83640;%s" % printListHex(cfg.mac_SA)
        dataField += CreatePTPText(prod_desc)
        # Revision Data (only set HW value)
        rev_data = "%d;;" % (port.phyid2 & 0xf)
        dataField += CreatePTPText(rev_data)
        # User Description
        dataField += CreatePTPText(cfg.user_description)
        # profileIdentity
        if (cfg.portDS.delayMechanism == DELAY_P2P):
            dataField += [0x0, 0x1B, 0x19, 0x0, 0x2, 0]
        else:
            dataField += [0x0, 0x1B, 0x19, 0x0, 0x1, 0]
        # Pad to even # octets
        if (len(dataField) & 0x1):
            dataField += [0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.USER_DESCRIPTION)):
        # GET or SET USER_DESCRIPTION
        # If SET, then set cfg.user_description
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.user_description, pad = GetPTPText(dataField)
        # Response
        dataField = CreatePTPText(cfg.user_description)
        if (len(dataField) & 0x1):
            dataField += [0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if ((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND) and (managementId == MANAGEMENT_ID.INITIALIZE)):
        # COMMAND INITIALIZE
        # set port_state to INITIALIZING
        Set_BMC_State(port, cfg, PORT_INITIALIZING)
        # Response
        dataField = []
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.DEFAULT_DATA_SET)):
        # GET DEFAULT_DATA_SET
        # Flags
        dataField = [((cfg.defaultDS.slaveOnly << 1) | cfg.defaultDS.twoStepFlag), 0]
        # Number Ports
        dataField += [(cfg.defaultDS.numberPorts >> 8), (cfg.defaultDS.numberPorts & 0xff)]
        # Priority1
        dataField += [cfg.defaultDS.priority1]
        # Clock Quality
        dataField += [cfg.defaultDS.clockQuality.clockClass, cfg.defaultDS.clockQuality.clockAccuracy] + [(cfg.defaultDS.clockQuality.offsetScaledLogVariance >> 8), (cfg.defaultDS.clockQuality.offsetScaledLogVariance & 0xff)]
        # Priority2
        dataField += [cfg.defaultDS.priority2]
        # clockIdentity
        dataField += cfg.defaultDS.clockIdentity
        # Domain Number
        dataField += [cfg.defaultDS.domainNumber]
        dataField += [0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.CURRENT_DATA_SET)):
        # GET CURRENT_DATA_SET
        # Current Data Set Fields
        dataField = Uint16_to_List(cfg.currentDS.stepsRemoved)
        dataField += Time_Interval(cfg.currentDS.offsetFromMaster)
        dataField += Time_Interval(cfg.currentDS.meanPathDelay)
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.PARENT_DATA_SET)):
        # GET PARENT_DATA_SET
        # Parent Data Set Fields
        dataField = cfg.parentDS.parentPortIdentity
        dataField += [cfg.parentDS.parentStats, 0]
        dataField += Uint16_to_List(cfg.parentDS.observed_poslv)
        dataField += Uint32_to_List(cfg.parentDS.observed_pcpcr)
        dataField += [cfg.parentDS.grandmasterPriority1]
        dataField += [cfg.parentDS.grandmasterClockQuality.clockClass, cfg.parentDS.grandmasterClockQuality.clockAccuracy] + Uint16_to_List(cfg.parentDS.grandmasterClockQuality.offsetScaledLogVariance)
        dataField += [cfg.parentDS.grandmasterPriority2]
        dataField += cfg.parentDS.grandmasterIdentity
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.TIME_PROPERTIES_DATA_SET)):
        # GET TIME_PROPERTIES_DATA_SET
        # TimeProperties Data Set Fields
        tp_flags = 0
        if (cfg.timePropertiesDS.leap59): tp_flags |= 1
        if (cfg.timePropertiesDS.leap61): tp_flags |= 2
        if (cfg.timePropertiesDS.currentUtcOffsetValid): tp_flags |= 4
        if (cfg.timePropertiesDS.ptpTimescale): tp_flags |= 8
        if (cfg.timePropertiesDS.timeTraceable): tp_flags |= 0x10
        if (cfg.timePropertiesDS.frequencyTraceable): tp_flags |= 0x20
        #
        dataField = Uint16_to_List(cfg.timePropertiesDS.currentUtcOffset)
        dataField += [tp_flags]
        dataField += [cfg.timePropertiesDS.timeSource]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET)) and (managementId == MANAGEMENT_ID.PORT_DATA_SET)):
        # GET PORT_DATA_SET
        # Port Data Set Fields
        dataField = []
        dataField += cfg.portDS.portIdentity
        dataField += [cfg.portDS.portState]
        dataField += [UInt8(cfg.portDS.logMinDelayReqInterval)]
        dataField += Time_Interval(cfg.portDS.peerMeanPathDelay)
        dataField += [UInt8(cfg.portDS.logAnnounceInterval)]
        dataField += [cfg.portDS.announceReceiptTimeout]
        dataField += [UInt8(cfg.portDS.logSyncInterval)]
        dataField += [cfg.portDS.delayMechanism]
        dataField += [UInt8(cfg.portDS.logMinPdelayReqInterval)]
        dataField += [cfg.portDS.versionNumber]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.PRIORITY1)):
        # GET or SET PRIORITY1
        # If SET, then set cfg.defaultDS.priority1
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.defaultDS.priority1 = dataField[0]
        # Response
        dataField = [cfg.defaultDS.priority1, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.PRIORITY2)):
        # GET or SET PRIORITY2
        # If SET, then set cfg.defaultDS.priority2
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.defaultDS.priority2 = dataField[0]
        # Response
        dataField = [cfg.defaultDS.priority2, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.DOMAIN)):
        # GET or SET DOMAIN
        # If SET, then set cfg.defaultDS.domainNumber
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.defaultDS.domainNumber = dataField[0]
            # set port_state to INITIALIZING
            Set_BMC_State(port, cfg, PORT_INITIALIZING)
        # Response
        dataField = [cfg.defaultDS.domainNumber, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.SLAVE_ONLY)):
        # GET or SET SLAVE_ONLY
        # If SET, then set cfg.defaultDS.slaveOnly
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.defaultDS.slaveOnly = dataField[0] & 0x1
        # Response
        targetPortIdentity = pkt_sts_1588.sourcePortIdentity
        dataField = [cfg.defaultDS.slaveOnly, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.LOG_ANNOUNCE_INTERVAL)):
        # GET or SET LOG_ANNOUNCE_INTERVAL
        # If SET, then set cfg.portDS.logAnnounceInterval
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.portDS.logAnnounceInterval = Int8(dataField[0])
        # Response
        dataField = [cfg.portDS.logAnnounceInterval & 0xff, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.ANNOUNCE_RECEIPT_TIMEOUT)):
        # GET or SET ANNOUNCE_RECEIPT_TIMEOUT
        # If SET, then set cfg.portDS.announceReceiptTimeout
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.portDS.announceReceiptTimeout = dataField[0]
        # Response
        dataField = [cfg.portDS.announceReceiptTimeout, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.LOG_SYNC_INTERVAL)):
        # GET or SET LOG_SYNC_INTERVAL
        # If SET, then set cfg.portDS.logSyncInterval
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.portDS.logSyncInterval = Int8(dataField[0])
        # Response
        dataField = [cfg.portDS.logSyncInterval & 0xff, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.VERSION_NUMBER)):
        # GET or SET VERSION_NUMBER
        # If SET, then set cfg.portDS.versionNumber
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.portDS.versionNumber = dataField[0]
        # Response
        dataField = [cfg.portDS.versionNumber, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
    if ((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND) and (managementId == MANAGEMENT_ID.ENABLE_PORT)):
        # COMMAND ENABLE_PORT
        # if DISABLED, set port_state to INITIALIZING
        if (cfg.portDS.portState == PORT_DISABLED):
            Set_BMC_State(port, cfg, PORT_INITIALIZING)
        # Response
        dataField = []
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if ((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND) and (managementId == MANAGEMENT_ID.DISABLE_PORT)):
        # COMMAND DISABLE_PORT
        # Disable port
        Set_BMC_State(port, cfg, PORT_DISABLED)
        # Response
        dataField = []
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (managementId == MANAGEMENT_ID.TIME):
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.COMMAND):
            # Unsupported
            managementErrorId = MANAGEMENT_ERROR_ID.NOT_SUPPORTED
            displayData = []
            #
            txdone = SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, managementErrorId, displayData) 
            return(0)
        if ((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET) & (cfg.portDS.portState != PORT_MASTER)):
            # If not Grandmaster, report error
            managementErrorId = MANAGEMENT_ERROR_ID.NOT_SETABLE
            displayData = []
            #
            txdone = SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, managementErrorId, displayData) 
            return(0)
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            # Set Time
            PTP_SetNewTime(port, cfg, dataField)
            # Respond with time set
            txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
            return(0)                   
        # Response to GET TIME
        curr_time = GetTime1588(xem, phyAddr, verbose)
        dataField = [0, 0] + GetTime1588(port, port.phyAddr, 0)
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)       
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.CLOCK_ACCURACY)):
        # GET or SET CLOCK_ACCURACY
        # If SET, then set cfg.defaultDS.clockQuality.clockAccuracy
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.defaultDS.clockQuality.clockAccuracy = dataField[0]
        # Response
        dataField = [cfg.defaultDS.clockQuality.clockAccuracy, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.UTC_PROPERTIES)):
        # GET or SET UTC_PROPERTIES
        # If SET, then set cfg.defaultDS.clockQuality.clockAccuracy
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.timePropertiesDS.currentUtcOffset = List_to_Uint16(dataField[0:2])
            cfg.timePropertiesDS.leap59 = dataField[2] & 0x1
            cfg.timePropertiesDS.leap61 = dataField[2] & 0x2
            cfg.timePropertiesDS.currentUtcOffsetValid = dataField[2] & 0x4
        # Response
        tp_flags = 0
        if (cfg.timePropertiesDS.leap59): tp_flags |= 1
        if (cfg.timePropertiesDS.leap61): tp_flags |= 2
        if (cfg.timePropertiesDS.currentUtcOffsetValid): tp_flags |= 4
        #
        dataField = Uint16_to_List(cfg.timePropertiesDS.currentUtcOffset)
        dataField += [tp_flags, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.TRACEABILITY_PROPERTIES)):
        # GET or SET UTC_PROPERTIES
        # If SET, then set fields
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.timePropertiesDS.timeTraceable = (dataField[0] >> 4) & 0x1
            cfg.timePropertiesDS.frequencyTraceable = (dataField[0] >> 5) & 0x1
        # Response
        tp_flags = 0
        if (cfg.timePropertiesDS.timeTraceable): tp_flags |= 0x10
        if (cfg.timePropertiesDS.frequencyTraceable): tp_flags |= 0x20
        #
        dataField = [tp_flags, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.TIMESCALE_PROPERTIES)):
        # GET or SET TIMESCALE_PROPERTIES
        # If SET, then set fields
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.timePropertiesDS.ptpTimescale = (dataField[0] >> 3) & 0x1
            cfg.timePropertiesDS.timeSource = dataField[1]
        # Response
        tp_flags = 0
        if (cfg.timePropertiesDS.ptpTimescale): tp_flags |= 8
        #
        dataField = [tp_flags]
        dataField += [cfg.timePropertiesDS.timeSource]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.DELAY_MECHANISM)):
        # GET or SET DELAY_MECHANISM
        # If SET, then set fields
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            if (cfg.portDS.delayMechanism != dataField[0]):
                # Change delay_mechanism
                cfg.portDS.delayMechanism = dataField[0]
                if (cfg.portDS.delayMechanism == DELAY_P2P):
                    port.slave.send_delay_req = 0
                    port.slave.delay_req_sent = 0
                    port.slave.delay_req_timer = 0
                    port.slave.delay_req_wait4TS = 0
                    port.Prop_Dly_list = []
                    port.PropDelayAvg = 0
                    # Determine next PDelay_Req time
                    port.pdelay_req.mean_pdly_req_pd = (2**cfg.portDS.logMinPdelayReqInterval) * (10**9)
                    if (cfg.portDS.portState == PORT_MASTER):
                        port.pdelay_req.next_pdelay_req = port.master.next_sync_time + (cfg.sync_interval/2) + port.pdelay_req.mean_pdly_req_pd
                    else:
                        curr_time = long(time() * (10**9))
                        port.pdelay_req.next_pdelay_req = curr_time + port.pdelay_req.mean_pdly_req_pd
                    if (cfg.dr_insert_enabled):
                        Disable_DR_Insert(port, cfg)
                if (cfg.portDS.delayMechanism == DELAY_E2E):
                    port.pdelay_req.sent = 0
                    port.pdelay_req.resp_rcvd = 0
                    port.pdelay_req.wait4TS = 0
                    port.pdelay_resp.sent = 0
                    port.pdelay_resp.wait4TS = 0
                    port.pdelay_req.next_pdelay_req = 0
                    port.mean_path_delay = 0
                    port.Prop_Dly_list = []
                    port.PropDelayAvg = 0
                    cfg.portDS.peerMeanPathDelay = port.PropDelayAvg
                    if (cfg.dr_insert and (not cfg.dr_insert_enabled) and (cfg.portDS.portState == PORT_SLAVE)):
                        Enable_DR_Insert(port, cfg)
        # Response
        dataField = [cfg.portDS.delayMechanism, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    if (((pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.GET) or (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET)) and (managementId == MANAGEMENT_ID.LOG_MIN_PDELAY_REQ_INTERVAL)):
        # GET or SET LOG_MIN_PDELAY_REQ_INTERVAL
        # If SET, then set fields
        if (pkt_sts_1588.mgnt_action == MANAGEMENT_ACTION_FIELD.SET):
            cfg.portDS.logMinPdelayReqInterval = dataField[0]
            port.pdelay_req.mean_pdly_req_pd = (2**cfg.portDS.logMinPdelayReqInterval) * (10**9)
        # Response
        dataField = [cfg.portDS.logMinPdelayReqInterval, 0]
        #
        txdone = SendManagementResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, dataField)
        return(0)        
    # Unsupported Management Request
    # Respond with Management Error TLV
    print "Unsupported Management TLV"
    managementErrorId = MANAGEMENT_ERROR_ID.NO_SUCH_ID
    displayData = []
    #
    txdone = SendManagementErrorResponse(port, cfg, targetPortIdentity, pkt_sts_1588, actionField, managementId, managementErrorId, displayData) 
    return(0)  
    #
#
# End of ManagementResponse routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# CreatePTPText script
#
def CreatePTPText(s):
    ptp_text = array('B', s).tolist()
    return([len(ptp_text)] + ptp_text)
    
#
# End of CreatePTPText routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# GetPTPText script
#
# Returns PTP Text in string form
# Strips PTP Text from original list
def GetPTPText(ptp_text):
    if (ptp_text == []):
        print "ERROR - PTP_TEXT decode", ptp_text
        return("", ptp_text)
    len_ptp_text = ptp_text[0]
    len_list = len(ptp_text) - 1
    if (len_ptp_text > len_list):
        print "ERROR - PTP_TEXT decode", ptp_text
        return("", ptp_text)
    s = array('B', ptp_text[1:(len_ptp_text+1)]).tostring()
    if (len_ptp_text == len_list):
        return_list = []
    else:
        return_list = ptp_text[(len_ptp_text+1) : (len_list+1)]
    return(s, return_list)
    
#
# End of GetPTPText routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# printListHex script
#
# Prints a list to screen in hex format
def printListHex(list_to_print):
    s = ""
    for i in range(len(list_to_print)):
        s += " %x" % list_to_print[i]
    return (s)
#
# End of printListHex routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTP_SetNewTime script
#
# Used to set a new time for a GrandMaster
# Should conserve the phase alignment
# Also, sets new local_time_offset value and other Master timeout values
def PTP_SetNewTime(xem, cfg, new_time):
    global local_time_offset
    curr_time = long(time.time() * (10**9))
    curr_1588_time = curr_time - local_time_offset
    new_time_1588 = TStoNS(new_time[2:10])
    Time_corrected = new_time_1588 - curr_1588_time
    if (cfg.align_clkout):
        Time_corrected = ((Time_corrected + (cfg.ptp_clkout_period/2))/ cfg.ptp_clkout_period) * cfg.ptp_clkout_period
    # correct for 2 cycle add time
    TimeCorr = (Time_corrected + (2 * cfg.ref_period))
    new_trig_time = ((new_time_1588 / 10**9) + 1) * (10**9)
    if (TimeCorr > 0):
        if (TimeCorr > 1000000000):
            #modify PPS
            cfg.trig0_control.trig_time = ((new_trig_time / (10**9)) + 2) * (10**9)
            EnableTrig(xem, xem.phyAddr, cfg.trig0_control, verbose)
        TimeCorr_list = NStoTS(TimeCorr)
        AddTime1588(xem, xem.phyAddr, TimeCorr_list, 1)
    else:
        if (TimeCorr < -1000000000):
            #disable PPS
            DisableTrigger(xem, xem.phyAddr, cfg.trig0_control.trig_csel, verbose)
        TimeCorr_list = NStoTS(-TimeCorr)
        SubTime1588(xem, xem.phyAddr, TimeCorr_list, 1)
        if (TimeCorr < -1000000000):
            #modify PPS
            cfg.trig0_control.trig_time = ((new_trig_time / (10**9)) + 2) * (10**9)
            EnableTrig(xem, xem.phyAddr, cfg.trig0_control, verbose)
    #
    # Set new local_time_offset
    local_time_offset -= Time_corrected
    #
    # Modify timeout values
    #xem.pdelay_req.next_pdelay_req += Time_corrected
    #xem.announce_receipt_timer += Time_corrected
    #xem.next_announce_time += Time_corrected
    #xem.master.next_sync_time += Time_corrected
    return(0)
#
# End of PTP_SetNewTime routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTP_Initialize script
#
# In PORT_INITIALIZING state, initialize configuration and master/slave 
# parameters
# transition to PORT_LISTENING state
def PTP_Initialize(xem, cfg):
    import time
    global local_time_offset
    
    phyAddr = xem.phyAddr
    
    # Disable Transmit and Receive Timestamp
    MdioWrite(xem, phyAddr, PTP_TXCFG0, 0x0000, 0)
    MdioWrite(xem, phyAddr, PTP_RXCFG0, 0x0000, 0)
    MdioWrite(xem, phyAddr, PTP_RXCFG3, 0x0000, 0)

    # Initialize timestamp lists
    xem.psf_list = PSF_Lists()
    xem.psf_list.rxts.TS_list = []
    xem.psf_list.txts.TS_list = []
    xem.psf_list.txts.sent_list = []

    # Define Transmit and Receive timestamp lists (point to PSF lists)
    xem.txts = xem.psf_list.txts
    xem.rxts = xem.psf_list.rxts
    cfg.mdio_rxts_en = (not cfg.psf_config.psf_rxts_en) and (not cfg.ts_insert)

    # Flush Transmit and Receive Timestamps
    FlushTimestamps(xem, phyAddr)

    # Enable Transmit Timestamp operation
    ConfigPTP_TX(xem, phyAddr, 1, cfg)

    # Enable Receive Timestamp operation
    ConfigPTP_RX(xem, phyAddr, 1, cfg)

    # Send Phy Control Frame
    if (xem.pcf_en):
        Send_PCF(xem)

    # Get offset of PTP clock time vs local time
    curr_time = long(time.time() * (10**9))
    PTP_time = TStoNS(GetTime1588(xem, phyAddr, 0))
    local_time_offset = curr_time - PTP_time

    # Initial sync time
    if (cfg.v2_enable):
        cfg.sync_interval = int((2.0**cfg.portDS.logSyncInterval) * (10**9))
    curr_1588_time = curr_time - local_time_offset
    xem.master.next_sync_time = ((curr_1588_time / (10**9)) * 10**9) + (2*cfg.sync_interval) + (cfg.sync_interval/2)
    xem.master.next_sync_time += local_time_offset

    # Initial announce time
    if (cfg.v2_enable):
        cfg.announce_interval = (2**cfg.portDS.logAnnounceInterval)* (10**9)
        xem.next_announce_time = xem.master.next_sync_time - (cfg.sync_interval/2)

    # initialize Announce Receipt Timer
    xem.restart_Announce_Receipt_Timeout = 0
    if (cfg.v2_enable):
        xem.announce_receipt_timer_en = 1
        announce_receipt_timeout_interval = (cfg.portDS.announceReceiptTimeout * cfg.announce_interval)
        xem.announce_receipt_timer = curr_time + announce_receipt_timeout_interval
    else:
        xem.announce_receipt_timer_en = 0
        xem.announce_receipt_timer = 0

    # Determine next PDelay_Req time
    if (cfg.portDS.delayMechanism == DELAY_P2P):
        curr_time = long(time.time() * (10**9))
        xem.pdelay_req.mean_pdly_req_pd = (2**cfg.portDS.logMinPdelayReqInterval) * (10**9)
        xem.pdelay_req.next_pdelay_req = xem.master.next_sync_time + (cfg.sync_interval/2) + xem.pdelay_req.mean_pdly_req_pd
    else:
        xem.pdelay_req.next_pdelay_req = 0

    # clear state variables
    xem.clock.num_syncs = 0
    xem.rxpkt_rdy = 0
    xem.time_adjust_pending = 0

    xem.master.sync_sent = 0
    xem.master.sync_wait4TS = 0

    xem.slave.sync_rcvd = 0
    xem.slave.send_delay_req = 0
    xem.slave.delay_req_sent = 0
    xem.slave.two_step = 1
    xem.slave.delay_req_timer = 0
    xem.slave.delay_req_wait4TS = 0
    xem.slave.next_delay_req = 3
    xem.slave.Time_Error_list = []
    xem.slave.Time_Corr_list = []
    xem.slave.sync_rcvd_list = []
    xem.slave.sync_sent_list = []
    xem.slave.sync_cf_list = []
    xem.slave.ignore_cnt = 0
    xem.slave.sync_missed = 0
    xem.slave.sync_complete = 0
    xem.slave.rate_cnt = 0
    xem.slave.syntonized = 0

    #if (not restart_1588):
    xem.rate_list = []
    xem.rate_avg_list = []
    xem.Prop_Dly_list = []
    xem.PropDelayAvg = 0
    xem.slave.prev_sync_rcvd = 0
    xem.slave.last_sync_seqID = 0

    xem.pdelay_req.sent = 0
    xem.pdelay_req.resp_rcvd = 0
    xem.pdelay_req.wait4TS = 0
    xem.pdelay_resp.sent = 0
    xem.pdelay_resp.wait4TS = 0

    # Transition to the LISTENING state
    xem.E_rbest = 0
    Set_BMC_State(xem, cfg, PORT_LISTENING)

#
# End of PTP_Initialize routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# PTPHandleEvents script
#
def PTPHandleEvents(xem, cfg):
    if (not cfg.event_enable):
        return(0)
    if (cfg.psf_config.psf_evnt_en):
        event_ready = (xem.psf_list.event_list != [])
        while (event_ready):
            event_detect = GetEventTS_PSF(xem.current_event, xem.psf_list.event_list[0], 0)
            xem.psf_list.event_list.pop(0)
            event_ready = (xem.psf_list.event_list != [])
            if (event_detect):
                xem.event_list += [xem.current_event.ts]
    else:
        event_ready = ((MdioRead(xem, xem.phyAddr, PTP_STS, 0) >> 8) & 1)
        if (event_ready):
            event_sts = MdioRead(xem, xem.phyAddr, PTP_ESTS, 0)
            event_detect = event_sts & 0x01
            if (event_detect == 0):
                print "Error - PTP_ESTS Read: Event not ready"
            while (event_detect):
                event_num = (event_sts >> 2) & 0x7
                event_mult = (event_sts >> 1) & 0x1
                event_rf = (event_sts >> 5) & 0x1
                event_ts_len = ((event_sts >> 6) & 0x3) + 1
                events_missed = (event_sts >> 8) & 0x7
                if (event_mult):
                    event_ext_sts = MdioRead(xem, xem.phyAdr, PTP_EDATA, 0)
                else:
                    event_ext_sts = 0
                event_TS = GetEventTS(xem, xem.phyAddr, debug_event)
                event_sts = MdioRead(xem, xem.phyAddr, PTP_ESTS, 0)
                event_detect = event_sts & 0x01
                xem.event_list += [TStoNS(event_TS)]
    return(0)
#
#
# End of PTPHandleEvents routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTPHandlePackets script
#
def PTPHandlePackets(xem, cfg):
    ErrorFound = 0
    if (not xem.rxpkt_rdy):
        xem.rxpkt_rdy, xem.rxpkt_buf = CheckPktReady(xem)
    if (xem.rxpkt_rdy):
        # Check for Phy Status Frame
        psf_ok = PSF_packet_EPL(cfg.psf_config, xem.rxpkt_buf, xem.psf_list)
        #psf_ok = PSF_packet(cfg.psf_config, xem.rxpkt_buf, xem.psf_list)
        if (psf_ok):
            print "PSF received"
            #xem.nextMsg = xem.IsPhyStatusFrame( pktBuf, lenPkt )
            #print "stop", here
            xem.rxpkt_rdy = 0
    if (xem.rxpkt_rdy):
        # Place packet on packet fifo
        xem.pkt_fifo += [xem.rxpkt_buf]
        xem.rxpkt_rdy = 0
    if (len(xem.pkt_fifo) > 0):
        if (cfg.mdio_rxts_en):
            # Check for timestamps through Management Interface
            ptp_sts_val = MdioRead(xem, phyAddr, PTP_STS, 0)
            while ((ptp_sts_val & PTP_RXTS_RDY) == PTP_RXTS_RDY):
                xem.rxts.TS_list += [GetRxTimestamp(xem, phyAddr, cfg.mdio_cksum_en, 0)]
                ptp_sts_val = MdioRead(xem, phyAddr, PTP_STS, 0)
        xem.rxpkt_rdy, pkt_sts_1588, xem.rxpkt_buf, xem.pkt_fifo = Pkt_Timestamp(xem, cfg, xem.pkt_fifo, xem.psf_list)
    #
    # Check for TX Timestamps
    if (not cfg.psf_config.psf_txts_en and (len(xem.txts.sent_list) > 0)):
        ptp_sts_val = MdioRead(xem, phyAddr, PTP_STS, 0)
        while ((ptp_sts_val & PTP_TXTS_RDY) == PTP_TXTS_RDY):    
            tx_timestamp = TStoNS(GetTxTimestamp(xem, phyAddr, 0))
            tx_timestamp += xem.tx_ts_dly
            xem.txts.TS_list += [tx_timestamp]
            ptp_sts_val = MdioRead(xem, phyAddr, PTP_STS, 0)
    #
    # Parse Transmit Timestamp List
    if (xem.txts.TS_list != []):
        ParseTxTS_list(xem, xem.txts)
    #
    # Handle Received packet
    if (xem.rxpkt_rdy):
        xem.slave.send_delay_req = 0
        # Parse Receive Packet for 1588 frame
        xem.rxpkt_rdy = 0
        if (pkt_sts_1588.announce_ok):
            AnnounceRcvd(xem, cfg, pkt_sts_1588, debug_TS)
        if (pkt_sts_1588.signaling_ok):
            SignalingRcvd(pkt_sts_1588, xem.sendPortId, debug_TS)
        if (pkt_sts_1588.management_ok):
            ManagementRcvd(xem, cfg, pkt_sts_1588, xem.sendPortId, debug_TS)
        # Pdelay_Resp Received
        #
        if (pkt_sts_1588.pdelay_resp_ok):
            ErrorFound |= PdelayRespRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, debug_TS)
            if (xem.pdelay_req.resp_rcvd & (not xem.pdelay_req.resp_2step)):
                # Compute Link Delay
                xem.mean_path_delay = ((xem.pdelay_req.t4 - xem.pdelay_req.t1) - xem.pdelay_req.resp_corr)/2
                xem.Prop_Dly_list = xem.Prop_Dly_list + [xem.mean_path_delay]
                xem.PropDelayAvg = AvgList(xem.Prop_Dly_list, cfg.delay_avg_period, 0)
                cfg.portDS.peerMeanPathDelay = xem.PropDelayAvg
                xem.pdelay_req.sent = 0
                xem.pdelay_req.resp_rcvd = 0
                if (not debug_silent):
                    print "%s Path Delay measurement: %d ns " % (cfg.port_name, xem.mean_path_delay)
                if (debug_TS):
                    print "... Average path delay = ", xem.PropDelayAvg

        # Pdelay_Resp_Followup Received
        #
        if (pkt_sts_1588.pdelay_follow_ok):
            ErrorFound |= PdelayRespFollowRcvd(xem, cfg, pkt_sts_1588, debug_TS)
        if (pkt_sts_1588.pdelay_follow_ok):
            # Compute Link Delay
            xem.mean_path_delay = ((xem.pdelay_req.t4 - xem.pdelay_req.t1) - (xem.pdelay_req.t3 - xem.pdelay_req.t2) - xem.pdelay_req.resp_corr - xem.pdelay_req.follow_corr)/2
            xem.Prop_Dly_list = xem.Prop_Dly_list + [xem.mean_path_delay]
            xem.PropDelayAvg = AvgList(xem.Prop_Dly_list, cfg.delay_avg_period, 0)
            cfg.portDS.peerMeanPathDelay = xem.PropDelayAvg
            xem.pdelay_req.sent = 0
            xem.pdelay_req.resp_rcvd = 0
            if (not debug_silent):
                print "%s Path Delay measurement: %d ns " % (cfg.port_name, xem.mean_path_delay)
            if (debug_TS):
                print "... Average path delay = ", xem.PropDelayAvg

        # Pdelay_Req Received
        #
        if (pkt_sts_1588.pdelay_req_ok):
            ErrorFound |= PdelayReqRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, debug_TS)

        # DelayReq Received
        #
        if (pkt_sts_1588.delay_req_ok):
            ErrorFound |= DelayReqRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, debug_TS)

        # Sync Received
        #
        if (pkt_sts_1588.sync_ok):
            ErrorFound |= SyncRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, verbose)
            if (pkt_sts_1588.sync_ok and xem.slave.sync_rcvd):
                # Store sync time
                xem.slave.sync_rcvd_list += [xem.slave.sync_rcvd_time]

        # FollowUp Received
        #
        if (pkt_sts_1588.follow_ok):
            ErrorFound |= FollowRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, verbose)

        # Delay_Resp Received
        #
        if (pkt_sts_1588.delay_resp_ok):
            ErrorFound |= DelayRespRcvd(xem, phyAddr, cfg, xem.rxpkt_buf, pkt_sts_1588, verbose)
        if (pkt_sts_1588.delay_resp_ok):
            # compute SMdelay
            xem.slave.delay_sent_time += xem.slave.delay_resp_cf
            xem.slave.delay_rcvd_time -= xem.delay_rcvd_correct
            SMdelay = xem.slave.delay_rcvd_time - xem.slave.delay_sent_time
            # compute one_way_delay (meanPathDelay for v2)
            one_way_delay = (xem.slave.MSdelay + SMdelay) / 2
            xem.Prop_Dly_list += [one_way_delay]
            xem.PropDelayAvg = AvgList(xem.Prop_Dly_list, cfg.delay_avg_period, 0)
            # Save currentDS.meanPathDelay (this is in subns)
            cfg.currentDS.meanPathDelay = one_way_delay << 16
            if (not debug_silent):
                print "%s Delay_Resp received: Average one-way delay: %d"% (cfg.port_name, xem.PropDelayAvg)

    return(ErrorFound)
#
#
# End of PTPHandlePackets routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTPClockServo script
#
def PTPClockServo(xem, phyAddr, cfg):
        global local_time_offset
        # Sync Complete processing
        if (xem.slave.sync_complete):
            xem.slave.sync_sent_list += [xem.slave.sync_sent_time]
        if (xem.slave.sync_complete & xem.time_adjust_pending):
            if (xem.slave.sync_seqID != Incr_Word16(xem.slave.last_sync_seqID)):
                print "%s Warning:  Missed Sync message" % cfg.port_name
                print "    sync_seqID = ", xem.slave.sync_seqID
                print "    last_seqID = ", xem.slave.last_sync_seqID
                xem.slave.sync_missed = 1
            xem.slave.last_sync_seqID = xem.slave.sync_seqID
            if (xem.time_adjust_pending & (xem.slave.ignore_cnt < 16)):
                if (not debug_silent):
                    print "%s Time adjust pending, sync ignored" % cfg.port_name
                xem.slave.ignore_cnt += 1
                xem.slave.sync_complete = 0
            if ((xem.slave.ignore_cnt >= 16) & xem.slave.sync_missed):
                print "%s ERROR Adjust pending max reached" % cfg.port_name
                xem.time_adjust_pending = 0
                #return(1)
        if (xem.slave.sync_complete):
            xem.slave.sync_complete = 0
            xem.slave.sync_rcvd = 0
            # Decide if need to send Delay_Req
            if (xem.slave.delay_req_timer >= xem.slave.next_delay_req):
                xem.slave.send_delay_req = 1
            else:
                xem.slave.delay_req_timer += 1
                xem.slave.send_delay_req = 0
            #
            #compute MSDelay
            #
            xem.slave.sync_sent_time += xem.sync_sent_correct
            if (xem.slave.two_step == 0):
                xem.slave.sync_sent_time += xem.correct_1step
            total_sync_correct = xem.slave.sync_rcvd_cf + xem.slave.follow_cf
            xem.slave.sync_sent_time += total_sync_correct
            if (debug_TS):
                print "... total sync_sent correction:", (total_sync_correct)
            xem.slave.sync_cf_list += [total_sync_correct]
            xem.slave.MSdelay = xem.slave.sync_rcvd_time - xem.slave.sync_sent_time
            #
            # Determine Time Error (offset_from_master)
            #
            TimeError = xem.slave.MSdelay - xem.PropDelayAvg
            xem.slave.Time_Error_list += [TimeError]
            if (not debug_silent):
                print "%s Sync: %d    Time: %s    Error: %d" % (cfg.port_name, xem.slave.sync_seqID, Print_TS(xem.slave.sync_rcvd_time), TimeError)
            cfg.currentDS.offsetFromMaster = TimeError << 16
            #
            # Correct Time and Rate
            #
            # Determine time correction and method
            TimeError_mag = abs(TimeError)
            use_temp_rate = cfg.temp_rate_en & (TimeError_mag < cfg.min_step_adjust)
            if (TimeError_mag < cfg.min_time_correct):
                # No time correction, too small
                Time_corrected = 0
            else:
                if (use_temp_rate & (TimeError_mag > cfg.max_trate_correct)):
                    if (TimeError < 0):
                        Time_corrected = -cfg.max_trate_correct
                    else:
                        Time_corrected = cfg.max_trate_correct
                else:
                    Time_corrected = TimeError
            #
            if (use_temp_rate & (Time_corrected != 0)):
                # Adjust Temporary Rate to correct time
                delta_rate = long((float(Time_corrected)/cfg.trate_duration) * (2**32))
                temp_rate = xem.clock.rate_1588 - delta_rate
                if (debug_TS):
                    print "rate_1588 %d" % xem.clock.rate_1588
                    print "temp_rate %d" % temp_rate
                SetTRate1588(xem, phyAddr, temp_rate, verbose)
            if ((not use_temp_rate) & (Time_corrected != 0)):
                if (cfg.align_clkout):
                    Time_corrected = ((Time_corrected + (cfg.ptp_clkout_period/2))/ cfg.ptp_clkout_period) * cfg.ptp_clkout_period
                    if (not debug_silent):
                        print "Phase Alignment: Modifed TimeError = %d ns" % Time_corrected
                # correct for 2 cycle add time
                TimeError_adj = (Time_corrected - (2 * cfg.ref_period))
                TimeCorr = -TimeError_adj
                if (TimeCorr > 0):
                    if (TimeCorr > 1000000000):
                        #modify PPS
                        cfg.trig0_control.trig_time = (((xem.slave.sync_rcvd_time - TimeError) / (10**9)) + 2) * (10**9)
                        EnableTrig(xem, phyAddr, cfg.trig0_control, verbose)
                    TimeCorr_list = NStoTS(TimeCorr)
                    AddTime1588(xem, phyAddr, TimeCorr_list, 0)
                else:
                    if (TimeCorr < -1000000000):
                        #disable PPS
                        DisableTrigger(xem, phyAddr, cfg.trig0_control.trig_csel, verbose)
                    TimeCorr_list = NStoTS(TimeError_adj)
                    SubTime1588(xem, phyAddr, TimeCorr_list, 0)
                    if (TimeCorr < -1000000000):
                        #modify PPS
                        cfg.trig0_control.trig_time = (((xem.slave.sync_rcvd_time - TimeError) / (10**9)) + 2) * (10**9)
                        EnableTrig(xem, phyAddr, cfg.trig0_control, verbose)
            if (xem.slave.rate_cnt == 0):
                #Reset rate list (ignore rate after rate adjusment)
                xem.rate_list = []
                #Don't send delay_req following rate adjustment, will be inaccurate
                xem.slave.send_delay_req = 0
                xem.slave.rate_cnt += 1
            else:
                #compute rate and add to list
                # ignores 1st rate following rate correction
                s_diff = float(xem.slave.sync_rcvd_time - xem.slave.prev_sync_rcvd)
                m_diff = float(xem.slave.sync_sent_time - xem.slave.prev_sync_sent)
                if ( m_diff == 0 ):
                    rate_diff = 0
                else:
                    rate_diff = (m_diff - s_diff)/m_diff * cfg.ref_period
                rate_long = long(rate_diff * (2**32))
                xem.rate_list = xem.rate_list + [rate_long]
                if ((xem.slave.rate_cnt == 2) & (not cfg.sync_enet) & (not xem.slave.syntonized)):
                    #Adjust Rate
                    xem.clock.rate_1588 += rate_long
                    SetRate1588(xem, phyAddr, xem.clock.rate_1588, debug_TS)
                    xem.slave.syntonized = 1
                    xem.slave.rate_cnt = 0
                else:
                  if ((xem.slave.rate_cnt == cfg.rate_period) & (not cfg.sync_enet)):
                    #Adjust Rate
                    rate_avg = 0
                    for cnt in range(len(xem.rate_list)):
                        rate_avg = rate_avg + xem.rate_list[cnt]
                    rate_avg = rate_avg/len(xem.rate_list)
                    xem.rate_avg_list = [(rate_avg + xem.clock.rate_1588)] + xem.rate_avg_list
                    if (cfg.rate_avg_period == 0):
                        xem.clock.rate_1588 = xem.rate_list[len(xem.rate_list) - 1] + xem.clock.rate_1588
                    else:
                        avg_rate_avg = 0
                        len_avg = cfg.rate_avg_period
                        if (len(xem.rate_avg_list) < cfg.rate_avg_period):
                            len_avg = len(xem.rate_avg_list)
                        for cnt in range(len_avg):
                            avg_rate_avg = avg_rate_avg + xem.rate_avg_list[cnt]
                        xem.clock.rate_1588 = avg_rate_avg/len_avg
                    # Limit rate to +/- 100ppm
                    if (xem.clock.rate_1588 > 35000000):
                        xem.clock.rate_1588 = 35000000
                    if (xem.clock.rate_1588 < -35000000):
                        xem.clock.rate_1588 = -35000000
                    SetRate1588(xem, phyAddr, xem.clock.rate_1588, debug_TS)
                    xem.slave.rate_cnt = 0
                    xem.rate_list = []
                  else:
                    xem.slave.rate_cnt += 1
            # 
            # Send PCF Frame to correct Time, Rate, Enable Trigger
            #
            if (xem.pcf_en):
                xem.rxpkt_rdy |= Send_PCF(xem)
            #
            # Increment Sync count value (i) and set previous values for future rate corrections
            #
            xem.slave.Time_Corr_list = xem.slave.Time_Corr_list + [Time_corrected]
            xem.clock.num_syncs += 1
            if (xem.adjust_done_capable & cfg.ts_insert & (Time_corrected != 0)):
                xem.time_adjust_pending = 1
                xem.slave.last_sync_seqID = xem.slave.sync_seqID
                xem.slave.ignore_cnt = 0
                xem.slave.sync_missed = 0
            xem.slave.prev_sync_sent = xem.slave.sync_sent_time
            xem.slave.prev_sync_rcvd = xem.slave.sync_rcvd_time - Time_corrected
            xem.slave.MSdelay = xem.slave.MSdelay - Time_corrected
            # modify time offset
            curr_time = long(time.time() * (10**9))
            local_time_offset = (curr_time - xem.slave.prev_sync_rcvd)
            # wait for time correction to complete
            if (xem.slave.send_delay_req):
                time.sleep(one_us * cfg.trate_duration_us)
        return(0)
#
#
# End of PTPClockServo routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTPSendPackets script
#
def PTPSendPackets(xem, cfg):
    #
    # Check if ready to send Delay_Req Pkt
    if (xem.slave.send_delay_req):
        xem.slave.send_delay_req = 0
        xem.slave.delay_req_timer = 0
        if (cfg.portDS.delayMechanism == DELAY_E2E):
            #
            # Build/Send Delay Request
            #
            curr_time = long(time.time() * (10**9))
            delay_req_buf = v2DelayReqPkt(NStoTS(curr_time), cfg, cfg.ptpHeader, cfg.ptpSuffix)
            txdone = SendPacket(xem, delay_req_buf)
            xem.slave.delay_req_sent = 1
            if (not cfg.dr_insert):
                xem.slave.delay_req_wait4TS = 1
                xem.txts.sent_list += [mtype_delay_req]
            else:
                xem.slave.delay_req_wait4TS = 0
            if (debug_TS):
                print "%s Delay_Req sent: %d" % (cfg.port_name, cfg.delayreq_seqID)
            if (not txdone):
                print "%s FAILED: Delay_Req never completed" % cfg.port_name
        # compute next_delay_req period
        if (cfg.v2_enable):
            if (cfg.delay_req_period != 0):
                xem.slave.next_delay_req += cfg.delay_req_period
            else:
                xem.slave.mean_dly_req_pd = (2**cfg.portDS.logMinDelayReqInterval)
                if (xem.slave.mean_dly_req_pd < 2):
                    xem.slave.mean_dly_req_pd = 2
                xem.slave.next_delay_req += (xem.slave.mean_dly_req_pd/2) + round(random() * xem.slave.mean_dly_req_pd)
        else:
            if (cfg.delay_req_period != 0):
                xem.slave.next_delay_req += cfg.delay_req_period
            else:
                xem.slave.next_delay_req = 2 + round(random() * 28)

    #
    # Check Time to see if ready to send Sync Pkt
    curr_time = long(time.time() * (10**9))
    if ((cfg.portDS.portState == PORT_MASTER) & (curr_time > xem.master.next_sync_time) & xem.master.sync_sent):
        # Check for long delay on sending sync
        if (curr_time > (xem.master.next_sync_time + (4 * cfg.sync_interval))):
            print "%s WARNING: No Sync sent TS available" % cfg.port_name
            return(1)
            xem.master.sync_sent = 0
    if ((cfg.portDS.portState == PORT_MASTER) & (curr_time > xem.master.next_sync_time) & (not xem.master.sync_sent)):
        #send sync packet
        approx_time = curr_time - local_time_offset
        sync_buf = v2SyncPkt(NStoTS(approx_time), cfg, cfg.ptpHeader, cfg.ptpSuffix)
        txdone = SendPacket(xem, sync_buf)
        if (not txdone):
            print "%s FAILED: Transmit Sync never completed" % cfg.port_name
            return(1)
        if (cfg.one_step):
            xem.master.sync_sent = 0
            xem.master.sync_wait4TS = 0
            xem.master.sync_sent_time = approx_time
            xem.clock.num_syncs += 1
            if(dialog_on):
                UpdateDialog(xem.master.sync_sent_time)
            else:
                if (not debug_silent):
                    print "%s Sync sent: %d    Time: %s" % (cfg.port_name, cfg.sync_seqID, Print_TS(xem.master.sync_sent_time))
        else:
            xem.master.sync_sent = 1
            xem.master.sync_wait4TS = 1
            xem.txts.sent_list += [mtype_sync]
        #
        # Update next Sync time
        xem.master.next_sync_time += int(cfg.sync_interval * cfg.sync_interval_factor)
        curr_time = long(time.time() * (10**9))
        if (curr_time > xem.master.next_sync_time):
            if (debug_TS):
                print "%s Warning: Next Sync time already passed" % cfg.port_name
                print "  curr_time: ", curr_time
                print "  xem.master.next_sync_time: ", xem.master.next_sync_time
            xem.master.next_sync_time = curr_time + int(cfg.sync_interval * cfg.sync_interval_factor)

    #
    # Check Time to see if ready to send PDelay_Req Pkt
    curr_time = long(time.time() * (10**9))
    if ((cfg.portDS.delayMechanism == DELAY_P2P) & (curr_time > xem.pdelay_req.next_pdelay_req) & (not xem.time_adjust_pending) & (not xem.pdelay_req.wait4TS)):
        #
        # Build/Send PDelay Request
        #
        pdelay_req_buf = v2PDelayReqPkt(NStoTS(curr_time), cfg, cfg.ptpHeader, cfg.ptpSuffix)
        txdone = SendPacket(xem, pdelay_req_buf)
        if (debug_TS):
            print "%s PDelay_Req sent" % cfg.port_name
        if (not txdone):
            print "%s FAILED: Transmit PDelay_Req never completed" % cfg.port_name
            return(1)
        #
        xem.pdelay_req.sent = 1
        xem.pdelay_req.wait4TS = 1
        xem.pdelay_req.t1 = 0
        xem.txts.sent_list += [mtype_pdelay_req]
        # compute next_pdelay_req
        xem.pdelay_req.next_pdelay_req += int(xem.pdelay_req.mean_pdly_req_pd * cfg.sync_interval_factor)
        curr_time = long(time.time() * (10**9))
        if (xem.pdelay_req.next_pdelay_req < (curr_time + (xem.pdelay_req.mean_pdly_req_pd/2))):
            xem.pdelay_req.next_pdelay_req = curr_time + int((xem.pdelay_req.mean_pdly_req_pd/2) * cfg.sync_interval_factor)

    # Get Sync Timestamp and send FollowUp
    if (xem.master.sync_sent & (not xem.master.sync_wait4TS)):
            xem.master.sync_sent = 0
            if (debug_TS):
                print "%s Sync Packet was sent at %s" % (cfg.port_name, Print_TS(xem.master.sync_sent_time))
            follow_buf = v2FollowUpPkt(NStoTS(xem.master.sync_sent_time), cfg, cfg.ptpHeader, cfg.ptpSuffix)
            txdone = SendPacket(xem, follow_buf)
            if (not txdone):
                print "%s FAILED: Transmit FollowUp never completed" % cfg.port_name
                return(1)
            # Sync Complete
            xem.clock.num_syncs += 1
            if(dialog_on):
                UpdateDialog(xem.master.sync_sent_time)
            else:
                if (not debug_silent):
                    print "%s Sync sent: %d    Time: %s" % (cfg.port_name, cfg.sync_seqID, Print_TS(xem.master.sync_sent_time))

    # Determine if ready to send PDelay_Resp_FollowUp Pkt
    if (xem.pdelay_resp.sent & (not xem.pdelay_resp.wait4TS)):
        xem.pdelay_resp.sent = 0
        pdelay_follow_buf = v2PDelayRespFUPkt(NStoTS(xem.pdelay_resp.sent_time), cfg, cfg.pdelay_follow_msg)
        txdone = SendPacket(xem, pdelay_follow_buf)
        if (verbose):
            print "%s PDelay_FollowUp sent" % cfg.port_name
        if (not txdone):
            print "%s FAILED: Transmit PDelay_FollowUp never completed" % cfg.port_name
            return(1)
    #
    return(0)
#
#
# End of PTPSendPackets routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTPAnnounceReceiptTimeout script
#
def PTPAnnounceReceiptTimeout(xem, cfg):
    curr_time = long(time.time() * (10**9))
    if (xem.announce_receipt_timer_en):
        if ((cfg.portDS.portState == PORT_INITIALIZING) or (cfg.portDS.portState == PORT_DISABLED) or (cfg.portDS.portState == PORT_FAULTY) or (cfg.portDS.portState == PORT_PRE_MASTER) or (cfg.portDS.portState == PORT_MASTER)):
            # Disable Announce Receipt Timer
            xem.announce_receipt_timer_en = 0
    if (xem.announce_receipt_timer_en and (curr_time > xem.announce_receipt_timer)):
        # postpone if waiting on Delay_Req transmit timestamp
        if not (xem.slave.delay_req_wait4TS):
            # Announce Receipt Timeout
            if (debug_TS):
                print "%s Announce Receipt Timeout" % cfg.port_name
            xem.E_rbest = 0
            if (cfg.defaultDS.slaveOnly):
                if ((cfg.portDS.portState != PORT_INITIALIZING) and (cfg.portDS.portState != PORT_DISABLED) and (cfg.portDS.portState != PORT_FAULTY)):
                    # Update data set parameters based on local clock
                    UpdateDataSet_M1_M2(cfg)
                    Set_BMC_State(xem, cfg, PORT_LISTENING)
            else:
                if ((cfg.portDS.portState == PORT_LISTENING) or (cfg.portDS.portState == PORT_UNCALIBRATED) or (cfg.portDS.portState == PORT_SLAVE) or (cfg.portDS.portState == PORT_PASSIVE)):
                    if ((cfg.portDS.portState == PORT_SLAVE) or (cfg.parentDS.grandmasterIdentity != cfg.defaultDS.clockIdentity)):
                        # Update data set parameters based on local clock
                        UpdateDataSet_M1_M2(cfg)
                    if (cfg.dr_insert_enabled):
                        Disable_DR_Insert(xem, cfg)
                    Set_BMC_State(xem, cfg, PORT_MASTER)
            # Restart timer if still enabled
            if (xem.announce_receipt_timer_en):
                RestartAnnounceReceiptTO(xem, cfg)
    return(0)
#
#
# End of PTPAnnounceReceiptTimeout routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# PTPAnnounceInterval script
#
def PTPAnnounceInterval(xem, cfg):
        xem.busy = 0
        xem.announce_interval_timeout = 0
        curr_time = long(time.time() * (10**9))
        if (curr_time > xem.next_announce_time):
            # postpone if waiting on transmit timestamp
            if (xem.master.sync_wait4TS or xem.slave.delay_req_wait4TS):
                xem.busy = 1
            else:
                if ((cfg.portDS.portState == PORT_LISTENING) or (cfg.portDS.portState == PORT_UNCALIBRATED) or (cfg.portDS.portState == PORT_SLAVE) or (cfg.portDS.portState == PORT_PRE_MASTER) or (cfg.portDS.portState == PORT_MASTER) or (cfg.portDS.portState == PORT_PASSIVE) ):
                    xem.announce_interval_timeout = 1
        return (xem.announce_interval_timeout, xem.busy)
#
#
# End of PTPAnnounceInterval routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# GetAlignError script
#
def GetAlignError(port_1, port_2, trig_control):
    EnableTriggerNow(port_1, port_1.phyAddr, trig_control, 500000000, verbose)
    event_detect = 0
    clk_error = 0
    evnt_cnt = 0
    while (event_detect == 0):
        event_sts = MdioRead(port_2, port_2.phyAddr, PTP_ESTS, 0)
        event_detect = event_sts & 0x01
        evnt_cnt += 1
        if (evnt_cnt == 1000):
            print "Error - PTP_ESTS Read: Event not ready"
            print "        If scope attached to SMA, use 1Mohm termination"
            break
            return(0, 0)
    if (event_detect):
        event1_TS = TStoNS(GetEventTS(port_2, port_2.phyAddr, 0))
        # Get Event TS from port_1
        event_sts = MdioRead(port_1, port_1.phyAddr, PTP_ESTS, 0)
        event_detect = event_sts & 0x01
        if (event_detect):
            event2_TS = TStoNS(GetEventTS(port_1, port_1.phyAddr, 0))
    if (event_detect):
        clk_error = long(event2_TS - event1_TS)
        #print "Clock Alignment Correction = ", clk_error
    return(event_detect, clk_error)
#
#
# End of GetAlignError routine
# ------------------------------------------------------------------

            
# -------------------------------------------------------------------
# Align_BC_Clocks script
#
def Align_BC_Clocks(port_1, port_2, trig_control, trig_config, ref_period):
    global ClockAlignCorrect
    #Align Slave and Master clocks
    #Enable GPIO9 on slave as single edge trigger
    #Enable GPIO9 to detect edge on both master and slave
    print "Aligning PTP Clocks between PHYs, please be patient..."
    ClearEventQueue(port_2, phyAddr)
    ClearEventQueue(port_1, phyAddr)
    port_2.PTPCancelTrigger(trig_config.trig_csel)
    port_1.PTPCancelTrigger(trig_config.trig_csel)
    event_num = 7
    event_cfg_val = ((9 << EVNT_GPIO) | (event_num << 1) | EVNT_WR)
    MdioWrite(port_2, phyAddr, PTP_EVNT, event_cfg_val, 0)
    MdioWrite(port_1, phyAddr, PTP_EVNT, event_cfg_val, 0)
    event_cfg_val |= EVNT_RISE
    MdioWrite(port_2, phyAddr, PTP_EVNT, event_cfg_val, 0)
    MdioWrite(port_1, phyAddr, PTP_EVNT, event_cfg_val, 0)
    trig_config.trig_per = 0
    trig_config.trig_gpio = 9
    trig_config.trig_notify = 0
    trig_config.trig_pulse = 1
    trig_control.trig_pw1 = 200
    ConfigTrig(port_1, phyAddr, trig_config, verbose)
    # Disable port_2 trigger
    trig_config.trig_gpio = 0
    ConfigTrig(port_2, phyAddr, trig_config, verbose)
    max_error = 0-(10**9)
    align_list = []
    for sample in range(10):
        event_detect, clk_error = GetAlignError(port_1, port_2, trig_control)
        if (event_detect):
            align_list += [clk_error]
            #print "clk_error: %d, max_error: %d" % (clk_error, max_error)
            if (clk_error > max_error):
                max_error = clk_error
        else:
            return(0)
        #print "max_error: ", max_error
    print "PTP Clock Alignment correction: %dns "% clk_error
    print "...ClockAlignCorrect = %dns "% ClockAlignCorrect
    clk_error = max_error + (2 * ref_period) + ClockAlignCorrect
    if (clk_error > 0):
        AddTime1588(port_2, phyAddr, NStoTS(clk_error), 0)
    else:
        SubTime1588(port_2, phyAddr, NStoTS(-clk_error), 0)
    # Disable Event
    #event_cfg_val = ((9 << EVNT_GPIO) | (event_num << 2) | EVNT_WR)
    #MdioWrite(port_2, phyAddr, PTP_EVNT, event_cfg_val, 0)
    #MdioWrite(port_1, phyAddr, PTP_EVNT, event_cfg_val, 0)
    #ClearEventQueue(port_2, phyAddr)
    #ClearEventQueue(port_1, phyAddr)
    return(event_detect)
#
#
# End of Align_BC_Clocks routine
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Pkt_Timestamp script
# Subroutine to buffer packets and align packets and timestamps
#
# Returns 4 variables:
#    packet_rdy
#    pkt_sts_1588
#    rxpkt
#    pkt_fifo
def Pkt_Timestamp(port, cfg, pkt_fifo, psf_list):
    #
    # Parse 1st packet on buffer
    pkt_sts_1588 = v2_Parse_Pkt(pkt_fifo[0], cfg)
    #
    # Return packet status if packet is a general packet (no timestamp)
    if (pkt_sts_1588.announce_ok or pkt_sts_1588.signaling_ok or pkt_sts_1588.management_ok or pkt_sts_1588.pdelay_follow_ok or pkt_sts_1588.follow_ok):
        rxpkt = pkt_fifo.pop(0)
        return(1, pkt_sts_1588, rxpkt, pkt_fifo)
    #
    # If Delay_Resp, if not inserting DR timestamp, return packet (no timestamp)
    if (pkt_sts_1588.delay_resp_ok & ((not cfg.ts_insert) or (not cfg.dr_insert))):
        rxpkt = pkt_fifo.pop(0)
        return(1, pkt_sts_1588, rxpkt, pkt_fifo)
    # Check for timestamp available
    if (pkt_sts_1588.sync_ok or pkt_sts_1588.delay_req_ok or pkt_sts_1588.pdelay_req_ok or pkt_sts_1588.pdelay_resp_ok or pkt_sts_1588.delay_resp_ok):
        if (cfg.ts_insert):
            curr_time = long(time.time() * (10**9))
            if (port.time_adjust_pending):
                port.time_adjust_pending = not GetAdjustDoneFlag(pkt_sts_1588, cfg, verbose)
            rxpkt = pkt_fifo.pop(0)
            pkt_sts_1588.packet_timestamp = GetInsertedTS(rxpkt, pkt_sts_1588.header, cfg, curr_time, local_time_offset)
            if (pkt_sts_1588.delay_resp_ok):
                pkt_sts_1588.packet_timestamp += port.tx_ts_dly
            else:
                pkt_sts_1588.packet_timestamp -= port.rx_ts_dly
            return(1, pkt_sts_1588, rxpkt, pkt_fifo)
        else:
            # Check timestamp list for appropriate timestamp
            ts_cnt = 0
            fifo_cnt = 0
            len_fifo = len(pkt_fifo)
            len_TS_list = len(psf_list.rxts.TS_list)
            while ((ts_cnt < len_TS_list) & (fifo_cnt < len_fifo)):
                timestamp = psf_list.rxts.TS_list[ts_cnt]
                pkt_sts_1588.packet_timestamp = timestamp.ts - port.rx_ts_dly
                if (CompareTS(timestamp, pkt_sts_1588)):
                    psf_list.rxts.TS_list = psf_list.rxts.TS_list[(ts_cnt+1) : len_TS_list]
                    pkt_fifo = pkt_fifo[fifo_cnt : len_fifo]
                    rxpkt = pkt_fifo.pop(0)
                    return(1, pkt_sts_1588, rxpkt, pkt_fifo)
                else:
                    ts_cnt += 1
                    if ((ts_cnt == len_TS_list) & (fifo_cnt < len_fifo)):
                        ts_cnt = 0
                        fifo_cnt += 1
            else:
                if (not cfg.psf_config.psf_rxts_en):
                    # No timestamp, discard packet
                    print "WARNING: Discarding packet, no timestamp available"
                    rxpkt = pkt_fifo.pop(0)
                    return(0, pkt_sts_1588, rxpkt, pkt_fifo)
                else:
                    # Not fatal, wait for PSF packet for timestamps
                    return(0, pkt_sts_1588, [], pkt_fifo)
    else:
        # Invalid packet.  Drop packet, return nothing
        rxpkt = pkt_fifo.pop(0)
        return(0, pkt_sts_1588, rxpkt, pkt_fifo)
#
#
# End of Pkt_Timestamp routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# ParseTxTS_list script
#
def ParseTxTS_list(port, txts):
    len_sent_list = len(txts.sent_list)
    len_ts_list = len(txts.TS_list)
    if (len_sent_list < len_ts_list):
        print "WARNING: too many transmit timestamps"
        # truncate timestamp list to only use most recent
        txts.TS_list = txts.TS_list[(len_ts_list - len_sent_list):len_ts_list]
        len_ts_list = len_sent_list
    while (len_ts_list > 0):
        if (txts.sent_list[0] == mtype_sync):
            port.master.sync_wait4TS = 0
            port.master.sync_sent_time = txts.TS_list.pop(0)
        if (txts.sent_list[0] == mtype_delay_req):
            port.slave.delay_req_wait4TS = 0
            port.slave.delay_sent_time = txts.TS_list.pop(0)
        if (txts.sent_list[0] == mtype_pdelay_req):
            port.pdelay_req.wait4TS = 0
            port.pdelay_req.t1 = txts.TS_list.pop(0)
        if (txts.sent_list[0] == mtype_pdelay_resp):
            port.pdelay_resp.wait4TS = 0
            port.pdelay_resp.sent_time = txts.TS_list.pop(0)
        if ((txts.sent_list[0] != mtype_sync) and (txts.sent_list[0] != mtype_delay_req) and (txts.sent_list[0] != mtype_pdelay_req) and (txts.sent_list[0] != mtype_pdelay_resp)):
            print "WARNING: unexpected Transmit mtype: ", txts.sent_list[0]
            txts.TS_list.pop(0)
        txts.sent_list.pop(0)
        len_ts_list = len(txts.TS_list)
    return(0)
#
#
# End of Pkt_Timestamp routine
# ------------------------------------------------------------------

    
# -------------------------------------------------------------------
# ConfigPSF script
#
def ConfigPSF(xem, phyAddr, cfg, psf_config):
    # Expected PSF fields based on configuration
    if (psf_config.psf_ipv4):
        psf_etype = [0x08, 0x00]
        psf_ipv4_val = PKT_IPV4
        psf_exp_mac_da = [0x01, 0x00, 0x5E, 0x00, 0x01, 0x81]
    else:
        psf_etype = [0x88, 0xF7]
        psf_ipv4_val = 0
        psf_exp_mac_da = [0x01, 0x1B, 0x19, 0x00, 0x00, 0x00]
    psf_exp_mac_sa = [0, 0, 0, 0, 0, 0]
    if (psf_config.psf_mac_sa_sel == 0):
        psf_exp_mac_sa = [0x08, 0x00, 0x17, 0x0B, 0x6B, 0x0F]
    if (psf_config.psf_mac_sa_sel == 1):
        psf_exp_mac_sa = [0x08, 0x00, 0x17, 0x00, 0x00, 0x00]
    if (psf_config.psf_mac_sa_sel == 2):
        psf_exp_mac_sa = psf_exp_mac_da

    psf_config.psf_exp_mac_hdr = psf_exp_mac_da + psf_exp_mac_sa + psf_etype
    psf_config.psf_ptp_hdr = [(psf_config.psf_hdr_data & 0xff), (psf_config.psf_hdr_data >> 8)]

    ones_comp_list = [0x4500, 0x0111, 0xE000, 0x0181, ((psf_config.psf_ip_src_addr[0] << 8) | psf_config.psf_ip_src_addr[1]), ((psf_config.psf_ip_src_addr[2] << 8) | psf_config.psf_ip_src_addr[3])]
    ones_comp_sum = ones_comp_sum16(ones_comp_list)
        
    if (0):
        # Define PKTSTS Data
        pktsts_data = (psf_config.psf_mac_sa_sel << MAC_ADD_SEL_SHFT)| psf_ipv4_val | (psf_config.psf_preamble_len << MIN_PRE_SHFT) | psf_config.psf_endian
        if (psf_config.psf_txts_en):
            pktsts_data |= PSF_TXTS_EN
        if (psf_config.psf_rxts_en):
            pktsts_data |= PSF_RXTS_EN
        if (psf_config.psf_trig_en):
            pktsts_data |= PSF_TRIG_EN
        if (psf_config.psf_evnt_en):
            pktsts_data |= PSF_EVNT_EN

        # Configure Phy Status Frames
        MdioWrite(xem, phyAddr, PTP_PKTSTS1, psf_config.psf_hdr_data, 0)
        MdioWrite(xem, phyAddr, PTP_PKTSTS2, ((psf_config.psf_ip_src_addr[1] << 8)| psf_config.psf_ip_src_addr[0]), 0)
        MdioWrite(xem, phyAddr, PTP_PKTSTS3, ((psf_config.psf_ip_src_addr[3] << 8)| psf_config.psf_ip_src_addr[2]), 0)

        MdioWrite(xem, phyAddr, PTP_PKTSTS4, ones_comp_sum, 0)

        # Enable/Disable Phy Status Frames
        MdioWrite(xem, phyAddr, PTP_PKTSTS, pktsts_data, 1)
    else:
        #EPL version
        statusConfigOptions = 0
        if (psf_config.psf_endian):
            statusConfigOptions |= xem.STSOPT_LITTLE_ENDIAN
        if (psf_config.psf_ipv4):
            statusConfigOptions |= xem.STSOPT_IPV4
        if (psf_config.psf_txts_en):
            statusConfigOptions |= xem.STSOPT_TXTS_EN
        if (psf_config.psf_rxts_en):
            statusConfigOptions |= xem.STSOPT_RXTS_EN
        if (psf_config.psf_trig_en):
            statusConfigOptions |= xem.STSOPT_TRIG_EN
        if (psf_config.psf_evnt_en):
            statusConfigOptions |= xem.STSOPT_EVENT_EN
        srcAddrToUse = xem.STS_SRC_ADDR_1
        if (psf_config.psf_mac_sa_sel == 0):
            srcAddrToUse = xem.STS_SRC_ADDR_2
        if (psf_config.psf_mac_sa_sel == 1):
            srcAddrToUse = xem.STS_SRC_ADDR_3
        if (psf_config.psf_mac_sa_sel == 2):
            srcAddrToUse = xem.STS_SRC_ADDR_USE_MC
        ptpReserved = (psf_config.psf_ptp_hdr[1] >> 4)
        ptpVersion = (psf_config.psf_ptp_hdr[1] & 0xf)
        transportSpecific = (psf_config.psf_ptp_hdr[0] >> 4)
        messageType = (psf_config.psf_ptp_hdr[0] & 0xf)
        sourceIpAddress = (psf_config.psf_ip_src_addr[3] << 24) | (psf_config.psf_ip_src_addr[2] << 16) | (psf_config.psf_ip_src_addr[1] << 8) | (psf_config.psf_ip_src_addr[0])
        #xem.PTPSetPhyStatusFrameConfig (statusConfigOptions, srcAddrToUse, psf_config.psf_preamble_len, ptpReserved, ptpVersion, transportSpecific, messageType, sourceIpAddress, ones_comp_sum)
        xem.PTPSetPhyStatusFrameConfig (statusConfigOptions, srcAddrToUse, psf_config.psf_preamble_len, ptpReserved, ptpVersion, transportSpecific, messageType, sourceIpAddress)
    return(0)
#
#
# End of ConfigPSF routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# SendPacket script
# Send packet through ALP or Integrity
def SendPacket(xem, packet_buf):
    packet_len = len(packet_buf)
    SendTxPkt(xem, packet_buf, packet_len, 0)
    txdone = True
    return(txdone)

#
#
# End of SendPacket routine
# ------------------------------------------------------------------

# ForeignMaster comparison Constants
A_BETTER = 1
B_BETTER = 2
A_BETTER_BY_TOPO = 3
B_BETTER_BY_TOPO = 4

# -------------------------------------------------------------------
# IsKnownFM script
#
# Determine if foreignMaster already exists in foreignMaster table
#
def IsKnownFM(foreignMasterDS, FM_entry):
    len_FM_DS = len(foreignMasterDS)
    if (len_FM_DS == 0):
        return (0, 0)
    for cnt in range(len_FM_DS):
        if (FM_entry.sourcePortIdentity == foreignMasterDS[cnt].sourcePortIdentity):
            break
    else:
        return(0, 0)
    return(1, cnt)
#
#
# End of IsKnownFM routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# UpdateFM_DS script
#
# Update foreignMaster entry in foreignMaster table
#
def UpdateFM_DS(foreignMaster, FM_entry):
    foreignMaster.sourcePortIdentity = FM_entry.sourcePortIdentity
    foreignMaster.grandmasterPriority1 = FM_entry.grandmasterPriority1
    foreignMaster.grandmasterClockQuality.clockClass = FM_entry.grandmasterClockQuality.clockClass
    foreignMaster.grandmasterClockQuality.clockAccuracy = FM_entry.grandmasterClockQuality.clockAccuracy
    foreignMaster.grandmasterClockQuality.offsetScaledLogVariance = FM_entry.grandmasterClockQuality.offsetScaledLogVariance
    foreignMaster.grandmasterPriority2 = FM_entry.grandmasterPriority2
    foreignMaster.grandmasterIdentity = FM_entry.grandmasterIdentity
    foreignMaster.stepsRemoved = FM_entry.stepsRemoved
    foreignMaster.timeSource = FM_entry.timeSource
    foreignMaster.flagField = FM_entry.flagField
    foreignMaster.currentUtcOffset = FM_entry.currentUtcOffset
    foreignMaster.receivePortIdentity = FM_entry.receivePortIdentity
    #
    foreignMaster.AnnounceMessages[0] += 1
    #
    return(foreignMaster)
#
#
# End of UpdateFM_DS routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# SumAnnounceMessages script
#
# Sum of announce messages over 4 announce periods
#
def SumAnnounceMessages(foreignMaster):
    return(foreignMaster.AnnounceMessages[0] + foreignMaster.AnnounceMessages[1] + foreignMaster.AnnounceMessages[2] + foreignMaster.AnnounceMessages[3])
#
#
# End of SumAnnounceMessages routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# AdjustForeignMasterWindow script
#
# shift announce message counts for each foreignMaster entry
# to adjust window to next announce interval
# 
def AdjustForeignMasterWindow(cfg):
    for FM_entry in (cfg.foreignMasterDS):
        FM_entry.AnnounceMessages[3] = FM_entry.AnnounceMessages[2]
        FM_entry.AnnounceMessages[2] = FM_entry.AnnounceMessages[1]
        FM_entry.AnnounceMessages[1] = FM_entry.AnnounceMessages[0]
        FM_entry.AnnounceMessages[0] = 0
    return(0)
#
#
# End of AdjustForeignMasterWindow routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Compute_E_rbest script
#
# Compute best master for port r
# 
def Compute_E_rbest(port, cfg):
    # Determine E_rbest
    len_FM = len(cfg.foreignMasterDS)
    if (len_FM > 0):
        # Compare Foreign Masters to find best
        for FM_entry in cfg.foreignMasterDS:
            if (SumAnnounceMessages(FM_entry) > 1):
                compare_result = CompareDS(port.E_rbest, FM_entry)
                if ((compare_result == B_BETTER) or (compare_result == B_BETTER_BY_TOPO)):
                    port.E_rbest = FM_entry
        # Delete unused qualified Foreign Masters
        cnt = 0
        for FM_entry in cfg.foreignMasterDS:
            if (SumAnnounceMessages(FM_entry) > 1):
                if (FM_entry != port.E_rbest):
                    del FM_entry
    return (0)
#
#
# End of Compute_E_rbest routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# StateDecisionEvent script
#
# Determine recommended state for Ordinary clock based on foreignMaster
# data set and local clock
# 
def StateDecisionEvent(port, cfg, E_best):
    #
    # Comparing to D0 (local clock)
    D0_data_set = foreign_Master_Data_Set()
    D0_data_set.sourcePortIdentity = cfg.defaultDS.clockIdentity + [0, 0]
    D0_data_set.grandmasterPriority1 = cfg.defaultDS.priority1
    D0_data_set.grandmasterClockQuality = cfg.defaultDS.clockQuality
    D0_data_set.grandmasterPriority2 = cfg.defaultDS.priority2
    D0_data_set.grandmasterIdentity = cfg.defaultDS.clockIdentity
    D0_data_set.receivePortIdentity = cfg.defaultDS.clockIdentity + [0, 0]
    D0_data_set.stepsRemoved = 0
    D0_compare = CompareDS(E_best, D0_data_set)
    #
    # Figure 26, state decision diagram
    if ((cfg.portDS.portState == PORT_LISTENING) and (port.E_rbest == 0)):
        recommended_state = PORT_LISTENING
    else:
        if ((D0_data_set.grandmasterClockQuality.clockClass > 0) and (D0_data_set.grandmasterClockQuality.clockClass < 128)):
            if ((D0_compare == B_BETTER) or (D0_compare == B_BETTER_BY_TOPO)):
                # M1 state transition
                recommended_state = PORT_MASTER
            else:
                # P1 state transition
                recommended_state = PORT_PASSIVE
        else:
            if ((D0_compare == B_BETTER) or (D0_compare == B_BETTER_BY_TOPO)):
                # M2 state transition
                recommended_state = PORT_MASTER
            else:
                if (E_best.receivePortIdentity == cfg.portDS.portIdentity):
                    # S1 state transition
                    recommended_state = PORT_SLAVE
                else:
                    Ebest_compare = CompareDS(E_best, port.E_rbest)
                    if (Ebest_compare == A_BETTER_BY_TOPO):
                        # P2 state transition
                        recommended_state = PORT_PASSIVE
                    else:
                        # M3 state transition
                        recommended_state = PORT_PRE_MASTER
    #
    return(recommended_state)
#
#
# End of StateDecisionEvent routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# UpdateDataSet_M1_M2 script
#
# Update datasets based on state decision code M1 or M2
# From Table 13 of v2 1588 specification 
# 
def UpdateDataSet_M1_M2(cfg):
    # currentDS
    cfg.currentDS.stepsRemoved = 0
    cfg.currentDS.offsetFromMaster = 0
    cfg.currentDS.meanPathDelay = 0
    # parentDS
    cfg.parentDS.parentPortIdentity = cfg.defaultDS.clockIdentity + [0, 0]
    cfg.parentDS.grandmasterIdentity = cfg.defaultDS.clockIdentity
    cfg.parentDS.grandmasterClockQuality = cfg.defaultDS.clockQuality
    cfg.parentDS.grandmasterPriority1 = cfg.defaultDS.priority1
    cfg.parentDS.grandmasterPriority2 = cfg.defaultDS.priority2
    # timePropertiesDS
    cfg.timePropertiesDS.currentUtcOffset = cfg.GM_timePropertiesDS.currentUtcOffset
    cfg.timePropertiesDS.currentUtcOffsetValid = cfg.GM_timePropertiesDS.currentUtcOffsetValid
    cfg.timePropertiesDS.leap59 = cfg.GM_timePropertiesDS.leap59
    cfg.timePropertiesDS.leap61 = cfg.GM_timePropertiesDS.leap61
    cfg.timePropertiesDS.timeTraceable = cfg.GM_timePropertiesDS.timeTraceable
    cfg.timePropertiesDS.frequencyTraceable = cfg.GM_timePropertiesDS.frequencyTraceable
    cfg.timePropertiesDS.ptpTimescale = cfg.GM_timePropertiesDS.ptpTimescale
    cfg.timePropertiesDS.timeSource = cfg.GM_timePropertiesDS.timeSource
    # portDS
    # cfg.portDS.portState assigned elsewhere
    return(0)
#
#
# End of UpdateDataSet_M1_M2 routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# UpdateDataSet_S1 script
#
# Update datasets based on state decision code S1
# From Table 16 of v2 1588 specification 
# 
def UpdateDataSet_S1(cfg, E_best):
    # currentDS
    cfg.currentDS.stepsRemoved = E_best.stepsRemoved + 1
    # parentDS
    cfg.parentDS.parentPortIdentity = E_best.sourcePortIdentity
    cfg.parentDS.grandmasterIdentity = E_best.grandmasterIdentity
    cfg.parentDS.grandmasterClockQuality = E_best.grandmasterClockQuality
    cfg.parentDS.grandmasterPriority1 = E_best.grandmasterPriority1
    cfg.parentDS.grandmasterPriority2 = E_best.grandmasterPriority2
    # timePropertiesDS
    cfg.timePropertiesDS.currentUtcOffset = E_best.currentUtcOffset
    cfg.timePropertiesDS.currentUtcOffsetValid = (E_best.flagField & 0x04)           
    cfg.timePropertiesDS.leap59 = (E_best.flagField & 0x01)
    cfg.timePropertiesDS.leap61 = (E_best.flagField & 0x02)
    cfg.timePropertiesDS.timeTraceable = (E_best.flagField & 0x10)
    cfg.timePropertiesDS.frequencyTraceable = (E_best.flagField & 0x20)
    cfg.timePropertiesDS.ptpTimescale = (E_best.flagField & 0x08)
    cfg.timePropertiesDS.timeSource = E_best.timeSource
    # portDS
    # cfg.portDS.portState assigned elsewhere
    return(0)
#
#
# End of UpdateDataSet_S1 routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# RestartAnnounceReceiptTO script
#
# Restart Announce Receipt timer 
# 
def RestartAnnounceReceiptTO(port, cfg):
    from time import time
    curr_time = long(time() * (10**9))
    port.announce_receipt_timer_en = 1
    announce_receipt_timeout_interval = (cfg.portDS.announceReceiptTimeout * cfg.announce_interval)
    port.announce_receipt_timer = curr_time + announce_receipt_timeout_interval
#
#
# End of RestartAnnounceReceiptTO routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Set_BMC_State script
#
# Set port state based on BMC algorithm results 
# 
def Set_BMC_State(port, cfg, new_state):
    if (cfg.portDS.portState == new_state):
        # No state change
        if ((new_state == PORT_INITIALIZING) or (new_state == PORT_DISABLED) or (new_state == PORT_FAULTY) or (new_state == PORT_PRE_MASTER) or (new_state == PORT_MASTER)):
            # Disable Announce Receipt Timer
            port.announce_receipt_timer_en = 0
    else:
        if ((new_state == PORT_LISTENING) or (new_state == PORT_UNCALIBRATED) or (new_state == PORT_SLAVE) or (new_state == PORT_PASSIVE)):
            # Restart Announce Receipt Timeout
            RestartAnnounceReceiptTO(port, cfg) 
        #
        if ((new_state == PORT_INITIALIZING) or (new_state == PORT_DISABLED) or (new_state == PORT_FAULTY) or (new_state == PORT_PRE_MASTER) or (new_state == PORT_MASTER)):
            # Disable Announce Receipt Timer
            port.announce_receipt_timer_en = 0
        #
        cfg.portDS.portState = new_state
        if (not debug_silent):
            print "%s State Change -> %s" % (cfg.port_name, PORT_STATE_STRING[new_state])
#
#
# End of Set_BMC_State routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# Enable_DR_Insert script
#
# In changing from Master to Slave, may need to enable the DR_insert
# mode of operation.  This is necessary as the DR_Insert option is not
# compatible with normal Transmit Timestamp operation.
#
def Enable_DR_Insert(port, cfg):
        txcfg0_val = TX_TS_EN
        if (cfg.sync_1step):
            txcfg0_val |= SYNC_1STEP
        if (cfg.tx_chk_1step):
            txcfg0_val |= TX_FIX_CHK
        if (cfg.dr_insert & (cfg.portDS.delayMechanism == DELAY_E2E)):
            txcfg0_val |= PTP_DR_INSERT
        txcfg0_val |= (cfg.portDS.versionNumber << 1)
        if (cfg.ipv4_en):
            txcfg0_val |= (IP1588_EN | TX_IPV4_EN )
        if (cfg.l2_enet):
            txcfg0_val |= (TX_L2_EN)
        if (cfg.ipv6_en):
            txcfg0_val |= (IP1588_EN | TX_IPV6_EN)
        MdioWrite(port, phyAddr, PTP_TXCFG0, txcfg0_val, 0)
        if (xem.pcf_en):
            Send_PCF(xem)        
        #
        cfg.dr_insert_enabled = 1
        #
        return (0)
#
# End of Enable_DR_Insert routine
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# Disable_DR_Insert script
#
# In changing from Slave to Master, may need to disable the DR_insert
# mode of operation.  This is necessary as the DR_Insert option is not
# compatible with Timestamp reads through MDIO
#
# Disabling the DR_INSERT control may result in a timestamp available.
# This should be cleared by reading the Transmit Timestamp Register
#
def Disable_DR_Insert(port, cfg):
        txcfg0_val = TX_TS_EN
        if (cfg.sync_1step):
            txcfg0_val |= SYNC_1STEP
        if (cfg.tx_chk_1step):
            txcfg0_val |= TX_FIX_CHK
        txcfg0_val |= (cfg.portDS.versionNumber << 1)
        if (cfg.ipv4_en):
            txcfg0_val |= (IP1588_EN | TX_IPV4_EN )
        if (cfg.l2_enet):
            txcfg0_val |= (TX_L2_EN)
        if (cfg.ipv6_en):
            txcfg0_val |= (IP1588_EN | TX_IPV6_EN)
        MdioWrite(port, port.phyAddr, PTP_TXCFG0, txcfg0_val, 1)
        if (xem.pcf_en):
            Send_PCF(xem)
        #
        # Flush transmit timestamps if any exist.
        FlushTxTimestamps(port, port.phyAddr)
        #
        cfg.dr_insert_enabled = 0
        MdioRead(port, port.phyAddr, PTP_TXCFG0, 1)
        #
        return (0)

#
# End of Disable_DR_Insert routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# BMC_State_Event script
#
# Handle BMC state event and make appropriate state transition
#
def BMC_State_Event(port, cfg, recommended_state, E_best):
    if (recommended_state == PORT_SLAVE):
        new_master = (cfg.portDS.portState == PORT_SLAVE) and (cfg.parentDS.parentPortIdentity != E_best.sourcePortIdentity)
        if ((cfg.portDS.portState == PORT_LISTENING) or (cfg.portDS.portState == PORT_PRE_MASTER) or (cfg.portDS.portState == PORT_MASTER) or (cfg.portDS.portState == PORT_PASSIVE) or (new_master)):
            # UNCALIBRATED state is transitional
            Set_BMC_State(port, cfg, PORT_UNCALIBRATED)
            # Set Dataset parameters based on new Master
            UpdateDataSet_S1(cfg, E_best)
            #
            # re-initialize servo parameters
            reinit_slave(port, cfg)
            #
            # enable delay_req timestamp insert if needed
            if (cfg.dr_insert and (cfg.portDS.delayMechanism == DELAY_E2E) and (not cfg.dr_insert_enabled)):
                Enable_DR_Insert(port, cfg)
            #
            # set state to PORT_SLAVE
            Set_BMC_State(port, cfg, PORT_SLAVE)
    if (recommended_state == PORT_PASSIVE):
        if (cfg.defaultDS.slaveOnly):
            Set_BMC_State(port, cfg, PORT_LISTENING)
        else:
            Set_BMC_State(port, cfg, PORT_PASSIVE)
    if (recommended_state == PORT_MASTER):
        if (cfg.defaultDS.slaveOnly):
            if (cfg.portDS.portState != PORT_LISTENING):
                # Update data set paramenters based on local clock
                UpdateDataSet_M1_M2(cfg)
                Set_BMC_State(port, cfg, PORT_LISTENING)
        else:
            if (cfg.portDS.portState != PORT_MASTER):
                # Set data set parameters based on local clock
                UpdateDataSet_M1_M2(cfg)
                if (cfg.dr_insert_enabled):
                    Disable_DR_Insert(port, cfg)
                #
                Set_BMC_State(port, cfg, PORT_MASTER)
    if ((recommended_state == PORT_PRE_MASTER) and (cfg.portDS.portState != PORT_MASTER)):
        #
        # Need to add timeout check.  For now, just goto MASTER
        Set_BMC_State(port, cfg, PORT_PRE_MASTER)
        if (cfg.dr_insert_enabled):
            Disable_DR_Insert(port, cfg)
        Set_BMC_State(port, cfg, PORT_MASTER)
    return (0)
#
# End of BMC_State_Event routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# CompareDS script
#
# Compare two master data sets to determine best master
#
def CompareDS(data_setA, data_setB):
    if (data_setA == 0):
        return(B_BETTER)
    if (data_setB == 0):
        return(A_BETTER)
    if (data_setA.grandmasterIdentity != data_setB.grandmasterIdentity):
        # Different grandmaster
        if (data_setA.grandmasterPriority1 > data_setB.grandmasterPriority1):
            return(B_BETTER)
        if (data_setA.grandmasterPriority1 < data_setB.grandmasterPriority1):
            return(A_BETTER)
        if (data_setA.grandmasterClockQuality.clockClass > data_setB.grandmasterClockQuality.clockClass):
            return(B_BETTER)
        if (data_setA.grandmasterClockQuality.clockClass < data_setB.grandmasterClockQuality.clockClass):
            return(A_BETTER)
        if (data_setA.grandmasterClockQuality.clockAccuracy > data_setB.grandmasterClockQuality.clockAccuracy):
            return(B_BETTER)
        if (data_setA.grandmasterClockQuality.clockAccuracy < data_setB.grandmasterClockQuality.clockAccuracy):
            return(A_BETTER)
        if (data_setA.grandmasterClockQuality.offsetScaledLogVariance > data_setB.grandmasterClockQuality.offsetScaledLogVariance):
            return(B_BETTER)
        if (data_setA.grandmasterClockQuality.offsetScaledLogVariance < data_setB.grandmasterClockQuality.offsetScaledLogVariance):
            return(A_BETTER)
        if (data_setA.grandmasterPriority2 > data_setB.grandmasterPriority2):
            return(B_BETTER)
        if (data_setA.grandmasterPriority2 < data_setB.grandmasterPriority2):
            return(A_BETTER)
        if (data_setA.grandmasterIdentity > data_setB.grandmasterIdentity):
            return(B_BETTER)
        return(A_BETTER)
    else:
        # Same grandmaster
        if (data_setA.stepsRemoved > (data_setB.stepsRemoved + 1)):
            return(B_BETTER)
        if (data_setA.stepsRemoved < (data_setB.stepsRemoved + 1)):
            return(A_BETTER)
        if (data_setA.stepsRemoved > data_setB.stepsRemoved):
            if (data_setA.receivePortIdentity == data_setA.sourcePortIdentity):
                return(0)
            if List_A_LT_B(data_setA.receivePortIdentity, data_setA.sourcePortIdentity):
                return(B_BETTER)
            if List_A_GT_B(data_setA.receivePortIdentity, data_setA.sourcePortIdentity):
                return(B_BETTER_BY_TOPO)
        if (data_setA.stepsRemoved < data_setB.stepsRemoved):
            if (data_setB.receivePortIdentity == data_setB.sourcePortIdentity):
                return(0)
            if List_A_LT_B(data_setB.receivePortIdentity, data_setB.sourcePortIdentity):
                return(A_BETTER)
            if List_A_GT_B(data_setB.receivePortIdentity, data_setB.sourcePortIdentity):
                return(A_BETTER_BY_TOPO)
        if List_A_GT_B(data_setA.sourcePortIdentity, data_setB.sourcePortIdentity):
            return(B_BETTER_BY_TOPO)
        if List_A_LT_B(data_setA.sourcePortIdentity, data_setB.sourcePortIdentity):
            return(A_BETTER_BY_TOPO)
        if List_A_GT_B(data_setA.receivePortIdentity[8:10], data_setB.receivePortIdentity[8:10]):
            return(B_BETTER_BY_TOPO)
        if List_A_LT_B(data_setA.receivePortIdentity[8:10], data_setB.receivePortIdentity[8:10]):
            return(A_BETTER_BY_TOPO)
        return(0)
#
# End of CompareDS routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# List_A_GT_B script
#
# Compare two lists to determine if A greater than B
#
def List_A_GT_B(list_A, list_B):
    # Assumes lists are same length
    for cnt in range(len(list_A)):
        if (list_A[cnt] > list_B[cnt]):
            return(1)
        if (list_A[cnt] < list_B[cnt]):
            return(0)
    return(0)
#
# End of List_A_GT_B routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# List_A_LT_B script
#
# Compare two lists to determine if A less than B
#
def List_A_LT_B(list_A, list_B):
    # Assumes lists are same length
    for cnt in range(len(list_A)):
        if (list_A[cnt] < list_B[cnt]):
            return(1)
        if (list_A[cnt] > list_B[cnt]):
            return(0)
    return(0)
#
# End of List_A_LT_B routine
# ------------------------------------------------------------------


# -------------------------------------------------------------------
# reinit_slave script
#
# Reinitialize slave on transition to PORT_SLAVE state
# 
#
def reinit_slave(xem, cfg):
    #
    # set initial Delay_Req time
    xem.delay_req_timer = 0
    xem.slave.next_delay_req = 3
    #
    # clear servo and clock update parameters
    xem.time_adjust_pending = 0
    xem.slave.sync_complete = 0
    xem.slave.sync_rcvd = 0
    # if not P2P, clear delay history
    if (cfg.portDS.delayMechanism != DELAY_P2P):
        xem.Prop_Dly_list = []
        xem.rate_avg_list = []
    #
    # Clear mean path delay
    xem.mean_path_delay = 0
    # clear rate adjust parameters
    xem.slave.rate_cnt = 0
    xem.rate_list = []
    xem.slave.syntonized = 0
    #
    return (0)
#
# End of reinit_slave routine
# ------------------------------------------------------------------

# -------------------------------------------------------------------
# init_port script
#
def init_port(xem, PhyPort, cfg):
    xem.phyAddr = 0

    xem.phyAddr = AlpMdioRead(xem, 0, PHYCR, 0) & 0x01F
    xem.phyid2 = AlpMdioRead(xem, xem.phyAddr, PHYID2, 0)
    phyAddr = xem.phyAddr

    # Set current page
    xem.curr_page = AlpMdioRead(xem, phyAddr, PAGESEL, 0)

    # ------------------------------------------------------------------
    # Add port state variables to xem instance
    xem.pdelay_req = Pdelay_Req_state()
    xem.pdelay_resp = Pdelay_Resp_state()
    xem.slave = slave_Status()
    xem.master = master_Status()
    xem.clock = clock_Status()

    # ------------------------------------------------------------------
    # timestamp correction values, for delay from TS point to/from wire
    xem.tx_ts_dly = 0
    xem.rx_ts_dly = 215
    xem.one_step_correct = 0    #correction for transmitter in one-step mode

    # corrections for partner that does not do corrections accurately
    xem.sync_sent_correct = 0
    xem.delay_rcvd_correct = 0

    # ------------------------------------------------------------------
    # Phy Control Frame Options
    xem.pcf_en = 0

    ##### CONFIG options
    # Set Reference clock period
    cfg.ref_period = 8

    cfg.clksrc_div_pgm = 0
    cfg.clksrc_ext = 0

    # ------------------------------------------------------------------
    # Defaults for Slave scripts
    
    # Set rate period (number of sync cycles to adjust rate)
    cfg.rate_period = 5
    
    # Set rate average period (number of rate periods to average rate over)
    # total # of sync cycles for rate averaging is rate_period * rate_avg_period
    # 0 indicates no averaging - just use most recent computed rate
    cfg.rate_avg_period = 0

    # Set Delay_Req period in number of sync cycles
    cfg.delay_req_period = 0    #0 = use default random (v1), or master setting (v2)

    # Set number of Propagation Delay values to average
    cfg.delay_avg_period = 10

    # Set Temp Rate duration in microseconds (if making temp rate corrections)
    cfg.trate_duration_us = 10000

    # Enable time correction via temporary rate correction (not step add/sub)
    cfg.temp_rate_en = 1

    # Set correction values to determine trate vs step
    cfg.min_time_correct = 1
    cfg.max_trate_correct = int(round((5.0/1000000) * cfg.trate_duration_us * 1000))
    cfg.min_step_adjust = 2 * cfg.max_trate_correct
    
    # ------------------------------------------------------------------
    # Defaults for Master scripts

    # Set sync interval
    cfg.sync_interval = (1 * 10**9) + 0
    cfg.sync_interval_factor = 1.0

    # ------------------------------------------------------------------
    # Phy Control Frame Options
    cfg.pcf_en = 0
    cfg.pcf_da_sel = 1
    cfg.pcf_buf_size = 0xf
    cfg.pcf_header = []
    xem.pcf_en = 0
    
    # ------------------------------------------------------------------
    # Phy Status Frame Options
    cfg.psf_config = PSF_Configuration()
    cfg.psf_config.dp83640_mdl_rev = (xem.phyid2 & 0xf)
    cfg.psf_config.psf_hdr_data = 0x02ff
    cfg.psf_config.psf_mac_sa_sel = 0
    cfg.psf_config.psf_ipv4 = 1
    cfg.psf_config.psf_ip_src_addr = [0x11, 0x22, 0x33, 0x44]
    cfg.psf_config.psf_preamble_len = 7
    cfg.psf_config.psf_endian = 0
    
    # ------------------------------------------------------------------
    # Trigger Control options
    cfg.trig_pulse = 0
    cfg.trig_per = 1
    cfg.trig_gpio = 1
    cfg.trig_csel = 0
    cfg.trig_if_late = 0
    cfg.trig_notify = 1
    cfg.trig_pw1 = 500000000
    cfg.trig_pw2 = 0
    
    cfg.trig0_config = Trigger_Configuration(0)
    cfg.trig1_config = Trigger_Configuration(1)
    cfg.trig2_config = Trigger_Configuration(2)
    cfg.trig3_config = Trigger_Configuration(3)
    cfg.trig4_config = Trigger_Configuration(4)
    cfg.trig5_config = Trigger_Configuration(5)
    cfg.trig6_config = Trigger_Configuration(6)
    cfg.trig7_config = Trigger_Configuration(7)
    
    cfg.trig0_config.trig_per = 1
    cfg.trig0_config.trig_gpio = 1
    cfg.trig0_config.trig_notify = 1
    
    # Enable trigger mask (8-bit field for enabling triggers 0-7)
    cfg.trigger_en = 0x01
    
    # Trigger Control fields
    cfg.trig0_control = Trigger_Control(0)
    cfg.trig1_control = Trigger_Control(1)
    cfg.trig2_control = Trigger_Control(2)
    cfg.trig3_control = Trigger_Control(3)
    cfg.trig4_control = Trigger_Control(4)
    cfg.trig5_control = Trigger_Control(5)
    cfg.trig6_control = Trigger_Control(6)
    cfg.trig7_control = Trigger_Control(7)
    
    cfg.trig0_control.trig_pw1 = 500000000
    
    
    # ------------------------------------------------------------------
    # Event configuration
    cfg.event_enable = 0
    cfg.evnt_chk_rate = 1
    cfg.event_gpio = 1
    xem.current_event = Event_Status()

    # ------------------------------------------------------------------
    cfg.sync_enet = 0
    
    # ------------------------------------------------------------------
    # Clock output configuration:
    #    PGM source
    #    no turbo
    #    10MHz (250/25)
    cfg.clkout_sel_pgm = 1
    cfg.clkout_spd = 0
    cfg.clkout_div_by_n = 25
    cfg.clkout_en = 1
    cfg.align_clkout = 0    # Enables phase alignment of CLKOUT to PPS
    
    # ------------------------------------------------------------------
    # V2 Options
    cfg.ptpHeader = ptpHeader_Class()
    cfg.dp83640_mdl_rev = (xem.phyid2 & 0xf)
    cfg.defaultDS.twoStepFlag = (not cfg.one_step)
    cfg.defaultDS.clockIdentity = cfg.mac_SA[0:3] + [0xFF, 0xFE] + cfg.mac_SA[3:6]
    cfg.portDS.portIdentity = cfg.defaultDS.clockIdentity + [0, 1]
    cfg.parentDS.parentPortIdentity = cfg.portDS.portIdentity
    cfg.parentDS.grandmasterIdentity = cfg.defaultDS.clockIdentity
    cfg.parentDS.grandmasterClockQuality = cfg.defaultDS.clockQuality
    cfg.parentDS.grandmasterPriority1 = cfg.defaultDS.priority1
    cfg.parentDS.grandmasterPriority2 = cfg.defaultDS.priority2
    
    cfg.ptpSuffix = []
    
#
#
# End of init_port routine
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# Basic initialization

dev = None
if 'alpBoards' in globals():
    dev = device

xem = find_ok_device( dev, port)

cfg = ConfigOptions()

init_port(xem, PhyPort, cfg)
phyAddr = xem.phyAddr


# set verbosity
verbose = 0

# ------------------------------------------------------------------
# Defaults for Slave scripts

# Start time in nanoseconds
slave_start_time = (1 * 10**9) + 0

# Disable Trigger on exit from script (useful for scope capture)
dis_trig_on_exit = 0

# Print the time error list on exit from script
print_time_error_list = 0

# Poll for Link Status to exit
poll_link_status = 0

# Restart slave from current state
restart_1588 = 0

# ------------------------------------------------------------------
# Timestamp Insertion constants
rxts_ins_ns_off = 36
rxts_ins_sec_off = 33
rxts_ins_sec_en = 1
rxts_ins_sec_len = 0

v2_ts_ins_ns_off = 16
v2_ts_ins_sec_off = 5
v2_ts_ins_sec_en = 1
v2_ts_ins_sec_len = 0


# ------------------------------------------------------------------
# Defaults for Master scripts

# Start time in nanoseconds
start_time = (1 * 10**9) + 0


# ------------------------------------------------------------------
# Useful Opal Kelly-related functions

from ok_fn import *
ok_functions = OkFunctions()
OkFunctionInit(alpBoards, ok_functions, board, port, dev, verbose)


# ------------------------------------------------------------------
# Debug Control
debug_TS = 0        #Turn on most debug messages
debug_event = 0     #Turn on event debug messages
debug_silent = 0    #Disable all but error messages
dialog_on = 0   #enable dialog box status (turn off for better performance)
sync_cycles = 0     # Halt after number of cycles, disable if 0

# -----------------------------------------------------------------
# Boundary and Transparent Clock correction
# The ALP platform introduces skew between the reference clocks, 
# resulting in a Clock Alignment error
ClockAlignCorrect = -8
