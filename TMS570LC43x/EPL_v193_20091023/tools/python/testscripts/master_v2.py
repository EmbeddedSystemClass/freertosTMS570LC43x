# -------------------------------------------------------------------
# Master IEEE 1588 v2
#
# $Log: master_v2.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.20  2008/09/18 17:13:14  dave
# Updates to use modified ALP that includes PSF fixes.
# Major cleanup of unused code.
#
# Revision 1.19  2008/06/26 15:14:01  dave
# add management support.
# update with PTP spec names for dataset variables
#
# Revision 1.18  2008/05/20 15:11:07  dave
# configure Phy Status Frames after PTP Reset, otherwise it clears the
# PSF configuration
#
# Revision 1.17  2008/05/14 15:28:56  dave
# Major updates to add subroutines, BMC algorithm.
#
# Revision 1.16  2008/04/14 17:39:31  dave
# Significant changes to support Phy Status Frames.
#
# Revision 1.15  2008/04/10 17:55:16  dave
# modify initial sync, pdelay, announce times.
#
# Revision 1.14  2008/04/02 15:32:01  dave
# Use new CheckPktReady routine
# Modify initial Sync time to be midpoint between sync periods
# of 1588 clock (more consistent alignment with PPS).
#
# Revision 1.13  2008/03/18 16:58:09  dave
# determine sync_interval from cfg.portDS.logSyncInterval for v2.
#
# Revision 1.12  2008/03/13 12:36:28  dave
# add subroutines for most packet handling.
# Updates to pdelay code.
#
# Revision 1.11  2008/01/23 16:15:36  dave
# fix timestamp insertion variable names.
#
# Revision 1.10  2008/01/15 13:23:18  dave
# use RX/TX config routines
# move more config options to config class.
#
# Revision 1.9  2007/12/19 14:02:01  benb
# If cfg.versionPTP_en = 0, don't include the PTP
#   version when configuring TXCFG0 and RXCFG0.  This
#   will cause the PHY to timestamp any version PTP
#   packets.
# Enable Fast Link Loss by default
#
# Revision 1.8  2007/12/13 14:23:37  benb
# Don't configure OK functions = now done in setup_1588
#
# Revision 1.7  2007/12/12 17:07:05  benb
# Added low-level Opal-Kelly functions, and call OkFunctionInit()
#   in master and slave.
# This is useful for setting the MAC duplex mode.
#
# Revision 1.6  2007/12/11 12:27:56  benb
# Call ConfigureClkOut function instead of explicit code.
#
# Revision 1.5  2007/12/07 11:51:50  dave
# improve get inserted timestamp for V2 (includes adjust_done fix).
#
# Revision 1.4  2007/11/28 13:22:22  dave
# separate cfg.one_step and one_step controls.
# cfg.one_step controls packet generation.  one_step controls device config
#
# Revision 1.3  2007/10/18 16:02:24  benb
# Don't use WriteTXRam for ALP version
#
# Revision 1.2  2007/09/28 13:23:47  dave
# add capability to send announce messages
#
# Revision 1.1  2007/09/26 10:46:50  dave
# Initial revision
#
# Revision 1.11  2007/09/06 10:42:06  dave
# Add configuration options.
# Add L2 appendend TS.
#
# Revision 1.10  2007/08/09 13:45:17  dave
# allow phase alignment of CLKOUT.
#
# Revision 1.9  2007/08/08 15:28:27  dave
# improved trigger controls.
#
# Revision 1.8  2007/07/25 12:27:04  dave
# fix v1 operation.
#
# Revision 1.7  2007/07/23 16:37:52  dave
# Add peer delay mechanism.
#
# Revision 1.6  2007/07/19 16:22:54  dave
# Add PCF support to MdioWrite command to allow basic scripts
# to use Phy Control Frames.
#
# Revision 1.5  2007/07/18 15:18:26  dave
# print config options.
#
# Revision 1.4  2007/07/18 11:51:58  dave
# Set PAGESEL register to ensure curr_page setting is correct.
#
# Revision 1.3  2007/07/18 11:29:37  benb
# Added option to turn off link status polling if poll_link_status = 0
# Added support for Stop button
#
# Revision 1.2  2007/07/17 18:14:35  dave
# add v1 support
#
# Revision 1.1  2007/07/12 13:42:10  dave
# Initial revision
#
#
#

# Input Options:  Basic options are usually set by running
#   config_options.py
#

# -------------------------------------------------------------------
# Routines required:
#from BMC_routines import *



# Print Mode of Operation
if (cfg.defaultDS.slaveOnly):
    print "Running Slave.  Options:"
else:
    print "Running Master.  Options:"
if (cfg.v2_enable):
    if (cfg.l2_enet):
        print "IEEE 1588 V2, Layer2 Ethernet"
    if (cfg.ipv4_en):
        print "IEEE 1588 V2, UDP/IPv4"
    if (cfg.ipv6_en):
        print "IEEE 1588 V2, UDP/IPv6"
else:
    print "IEEE 1588 V1, UDP/IPv4"
if (cfg.ts_insert):
    print "Timestamp Insertion Enabled"
if (cfg.pcf_en):
    print "Using Phy Control Frames"
if (cfg.portDS.delayMechanism == DELAY_P2P):
    print "Using Peer Delay Mechanism"
print ""

if (restart_1588):
    print "Restarting ..."

import time
one_ms = 0.001
one_us = 0.000001
from random import *


# Set up Script Dialog window
if (dialog_on):
    import wx
    from ScriptDialog import ScriptDialog
    scriptDlg = ScriptDialog( s.parent, 2, size=(300,150), xSpacing=20, ySpacing=5)
    # Create the rows and columns
    scriptDlg.AddRow( 0, "Sync Seq ID")
    scriptDlg.AddRow( 0, "Time")
    scriptDlg.AddRow( 1, "")
    scriptDlg.AddRow( 1, "")

    def UpdateDialog(time_value):
        time_sec = time_value / (10**9)
        time_ns = time_value % (10**9)
        scriptDlg.SetLabel( 1, 0, "%d" % (cfg.sync_seqID))
        scriptDlg.SetLabel( 1, 1, "%dsec %dns" % (time_sec, time_ns))

    UpdateDialog(start_time)

# initialize packet buffer fifo
xem.pkt_fifo = []

# Set PAGE_SEL register
xem.pcf_en = 0
MdioWrite(xem, phyAddr, PAGESEL, xem.curr_page, 0)

# Set Temp Rate duration in number of 8ns clock cycles
cfg.trate_duration = (cfg.trate_duration_us * 1000) >> 3

# Enable Phy Control Frames
if (cfg.pcf_en):
    pcfcr_val = ((cfg.pcf_da_sel << 8) | (cfg.pcf_buf_size << PCF_BUF) | PCF_EN)
    MdioWrite(xem, phyAddr, PCFCR, pcfcr_val, 0);
    xem.pcf_en = 1
    xem.pcf_list = []
    xem.send_pcf = 0
    xem.pcf_da_sel = cfg.pcf_da_sel
    xem.pcf_buf_size = cfg.pcf_buf_size
    xem.pcf_header = cfg.pcf_header
else:
    pcfcr_val = 0
    MdioWrite(xem, phyAddr, PCFCR, pcfcr_val, 0);


if (not restart_1588):
    # Enable Fast Link Loss by default
    sdcfg_val = MdioRead(xem, phyAddr, SD_CFG, verbose)
    sdcfg_val |= SIG_DET_TIME
    MdioWrite(xem, phyAddr, SD_CFG, sdcfg_val, verbose)

    # Set PTP_ETYPE
    if (cfg.l2_enet):
        MdioWrite(xem, phyAddr, PTP_ETR, cfg.ptp_etype, 0)

    # Disable 1588 clock
    MdioWrite(xem, phyAddr, PTP_CTL, (PTP_DISABLE | PTP_RESET), 0)
    MdioWrite(xem, phyAddr, PTP_CTL, PTP_DISABLE, 0)

    # inital state
    cfg.portDS.portState = PORT_INITIALIZING
    
    # Configure Clock Output
    cfg.ptp_clkout_period = ConfigureClkOut(xem, cfg, phyAddr, verbose)
    
    # Set Temporary Rate Duration.  Will be unchanged for entire test
    MdioWrite(xem, phyAddr, PTP_TRDH, (cfg.trate_duration >> 16), 0)
    MdioWrite(xem, phyAddr, PTP_TRDL, (cfg.trate_duration & 0xFFFF), 0)

    # Configure Triggers
    DisableTrigger(xem, phyAddr, cfg.trig0_config.trig_csel, verbose)
    ConfigTrig(xem, phyAddr, cfg.trig0_config, verbose)
    
    # Disable Transmit and Receive Timestamp
    MdioWrite(xem, phyAddr, PTP_TXCFG0, 0x0000, 0)
    MdioWrite(xem, phyAddr, PTP_RXCFG0, 0x0000, 0)
    MdioWrite(xem, phyAddr, PTP_RXCFG3, 0x0000, 0)

    # Enable 1588 clock, set start time, set rate to 0
    xem.clock.rate_1588 = 0
    SetRate1588(xem, phyAddr, xem.clock.rate_1588, 0)
    SetTime1588(xem, phyAddr, NStoTS(start_time), verbose)
    MdioWrite(xem, phyAddr, PTP_CTL, PTP_ENABLE, 0)

    # Enable Trigger 0
    cfg.trig0_control.trig_time = (((start_time / 10**9) + 1) * 10**9)
    EnableTrig(xem, phyAddr, cfg.trig0_control, verbose)

    # Send Phy Control Frame
    if (xem.pcf_en):
        Send_PCF(xem)
    curr_time = long(time.time() * (10**9))
    local_time_offset = curr_time - start_time

    # Align ClkOut phase
    if (cfg.align_clkout):
        ClearEventQueue(xem, phyAddr)
        event_num = 7
        event_corr_factor = (3 * cfg.ref_period) + 11
        phase_error = Align1588ClkPhase(xem, phyAddr, event_num, cfg.ref_period, cfg.ptp_clkout_period, event_corr_factor)
        local_time_offset = local_time_offset - phase_error


# Configure Phy Status Frames
ConfigPSF(xem, phyAddr, cfg, cfg.psf_config)

# Initialize timestamp lists
xem.psf_list = PSF_Lists()
xem.psf_list.rxts.TS_list = []
xem.psf_list.txts.TS_list = []
xem.psf_list.txts.sent_list = []

# Define Transmit and Receive timestamp lists (point to PSF lists)
xem.txts = xem.psf_list.txts
xem.rxts = xem.psf_list.rxts
cfg.mdio_rxts_en = (not cfg.psf_config.psf_rxts_en) and (not cfg.ts_insert)

# Clear Event Queue
if (cfg.event_enable):
    ClearEventQueue(xem, phyAddr)

# Flush Receive,
FlushRX(xem, 0)

# Flush Transmit and Receive Timestamps
FlushTimestamps(xem, phyAddr)

# Enable Transmit Timestamp operation
ConfigPTP_TX(xem, phyAddr, 1, cfg)

# Enable Receive Timestamp operation
ConfigPTP_RX(xem, phyAddr, 1, cfg)

# Enable Event 0 detection, rise edge on GPIO1
event_cfg_val = (EVNT_RISE | (cfg.event_gpio << EVNT_GPIO) | EVNT_WR)
if (cfg.event_enable):
    MdioWrite(xem, phyAddr, PTP_EVNT, event_cfg_val, 0)
    xem.current_event = Event_Status()

# Send Phy Control Frame
if (xem.pcf_en):
    Send_PCF(xem)
    curr_time = long(time.time() * (10**9))

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

if (cfg.defaultDS.slaveOnly):
    RxStats_start = GetMacStats(xem, 0)

# clear state variables
xem.clock.num_syncs = 0
xem.rxpkt_rdy = 0
xem.time_adjust_pending = 0

xem.master.sync_sent = 0

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
if (not restart_1588):
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

xem.event_list = []

if (cfg.v2_enable):
    # Transition to the LISTENING state
    xem.E_rbest = 0
    Set_BMC_State(xem, cfg, PORT_LISTENING)
else:
    # force slave or master state
    if (cfg.defaultDS.slaveOnly):
        cfg.portDS.portState = PORT_SLAVE
    else:
        cfg.portDS.portState = PORT_MASTER
        if (cfg.dr_insert_enabled):
            Disable_DR_Insert(port, cfg)        

break_loop = 0
while (not break_loop):
    #
    if (poll_link_status):
        LinkStatus = MdioRead(xem, phyAddr, PHYSTS, 0) & 0x01
        if (LinkStatus == 0):
            print "Phy has lost link, exiting"
            break
    # Check for Event
    PTPHandleEvents(xem, cfg)

    # Check for INITIALIZING state
    if (cfg.portDS.portState == PORT_INITIALIZING):
        PTP_Initialize(xem, cfg)
    
    #check for receive packet
    ErrorFound = PTPHandlePackets(xem, cfg)
    if (ErrorFound):
        break
    
    if (cfg.portDS.portState != PORT_DISABLED):
        ErrorFound = PTPClockServo(xem, xem.phyAddr, cfg)
        if (ErrorFound):
            break
        ErrorFound = PTPSendPackets(xem, cfg)
        if (ErrorFound):
            break

        #
        # Check for Announce Receipt timeout on each port
        if (cfg.v2_enable):
            PTPAnnounceReceiptTimeout(xem, cfg)

        #
        # Checkfor announceInterval timeout on each port
        if (cfg.v2_enable):
            PTPAnnounceInterval(xem, cfg)
            #
            if (xem.announce_interval_timeout & (not xem.busy)):
                #
                # compute E_rbest
                Compute_E_rbest(xem, cfg)
                #
                # Determine E_best
                E_best = xem.E_rbest
                #
                # For Each port, do State Decision Event
                recommended_state = StateDecisionEvent(xem, cfg, E_best)
                BMC_State_Event(xem, cfg, recommended_state, E_best)
                #
                # For each port with an announce interval timeout, update FM window
                if (xem.announce_interval_timeout):
                    AdjustForeignMasterWindow(cfg)
                    # If Master state, send Announce
                    if (cfg.portDS.portState == PORT_MASTER):
                        curr_time = long(time.time() * (10**9))
                        approx_time = curr_time - local_time_offset
                        #send announce packet
                        announce_buf = v2AnnouncePkt(NStoTS(approx_time), cfg, cfg.ptpHeader, cfg.ptpSuffix)
                        txdone = SendPacket(xem, announce_buf)
                        if (debug_TS):
                            print "%s Announce sent: %d"% (cfg.port_name, cfg.announce_seqID)
                    # Update next Announce time
                    xem.next_announce_time += int(cfg.announce_interval * cfg.sync_interval_factor)


    #
    #wait 1 ms
    #time.sleep(one_ms)
    #
    if 'ALPExiting' in locals():
        if ALPExiting():
            break_loop = 1
    # check for max sync cyles reached
    if (sync_cycles > 0):
        if (xem.clock.num_syncs == sync_cycles):
            break_loop = 1

if(dialog_on):
    scriptDlg.Deinit()

if (cfg.defaultDS.slaveOnly):
    print ""
    RxStats_end = GetMacStats(xem, 1)
    
    if (dis_trig_on_exit):
        DisableTrigger(xem, phyAddr, trig_csel, verbose)
    if (print_time_error_list):
        print "Time Error List:", xem.slave.Time_Error_list
    print ""
    print "Offset from Master Results:"
    StdDev(xem.slave.Time_Error_list[6:len(xem.slave.Time_Error_list)], 1)
    print "Number of Sync cycles", len(xem.slave.Time_Error_list)
    if (len(xem.slave.Time_Error_list) > 10):
        print "Max Time Error: %d" % max(xem.slave.Time_Error_list[10:len(xem.slave.Time_Error_list)])
        print "Min Time Error: %d" % min(xem.slave.Time_Error_list[10:len(xem.slave.Time_Error_list)])
    print ""
    print "One-way delay results:"
    StdDev(xem.Prop_Dly_list, 1)

    # Print event results
    if (cfg.event_enable):
        if (xem.event_list == []):
            print "Warning: No events detected"
        else:
            event_list_dly = []
            for cnt in range(len(xem.event_list)):
                event_list_dly += [xem.event_list[cnt] % (10**9)]
                if (event_list_dly[len(event_list_dly)-1] > (5*cfg.ref_period)):
                    print "Warning: unexpected event time: ", xem.event_list[cnt]
                    event_list_dly = event_list_dly[0:(len(event_list_dly)-1)]
            print "Event (PPS) stats:"
            StdDev(event_list_dly, 1)
    
    if (RxStats_start[0:4] != RxStats_end[0:4]):
        print "WARNING : Difference in receive MAC stats"
        print "               CRC, Runt, RX_ER, Missed, Rx pkts"
        print "  Start stats: ", RxStats_start
        print "  End stats: ", RxStats_end
    
    fname = 'C:\\Documents and Settings\\All Users\\Documents\\alp1588_sync.log'
    SaveErrorList(xem.slave.Time_Error_list, fname)
    fname = 'C:\\Documents and Settings\\All Users\\Documents\\alp1588_rate.log'
    SaveErrorList(xem.rate_avg_list, fname)
    fname = 'C:\\Documents and Settings\\All Users\\Documents\\alp1588_cf.log'
    SaveErrorList(xem.slave.sync_cf_list, fname)
