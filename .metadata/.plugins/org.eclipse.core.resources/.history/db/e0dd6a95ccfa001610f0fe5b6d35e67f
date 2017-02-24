"""
  ok_fn.py - Sets up useful Opal Kelly functions.

  Copyright (c) 2007 National Semiconductor Corporation.
  All Rights Reserved.
"""
# -------------------------------------------------------------------
# Opal Kelly functions
#
# $Id: ok_fn.py,v 1.2 2008/09/22 23:25:23 robertst Exp $
#
# $Log: ok_fn.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.7  2008/04/22 15:48:40  benb
# Added OkCheckTxBlitzDone to check separate tx_done trigger for blitzing
#
# Revision 1.6  2008/04/18 16:45:17  benb
# Added OkPktType to OkFunctions class
# Strip txt in OkGetInput()
# Removed blitz from OkSetPktLen()
# Fixed OkSetBurstCount()
# Fixed OkSetPktType()
# Added OkStartBlitz() and OkStopBlitz()
#
# Revision 1.5  2008/03/13 11:53:00  benb
# Added OkFPGAWriteReg and OkFPGAReadReg
#
# Revision 1.4  2008/03/13 10:47:07  benb
# Added RX_STS_EN and FORCE_STS_PKT bits
#
# Revision 1.3  2007/12/19 13:29:41  benb
# Updated to work with multiple ALP boards
#
# Revision 1.2  2007/12/13 17:31:06  benb
# cleanup
#
# Revision 1.1  2007/12/12 17:06:28  benb
# Initial revision
#

class OkFunctions:
    OkAlpIf = None
    OkAlpBoardNum = 0
    OkPhyPort = 0
    OkSlave = 1
    OkPktLength = 1514
    OkPktBlitz = 0
    OkBurstCount = 65535
    OkPktType = 0
    OkRxFilterMode = 1
    
    # Endpoints
    SLAVE_MAC_CONTROL           = 0x00  # WireIn
    SLAVE_MAC_TX_FRAME_SIZE     = 0x01  # WireIn
    SLAVE_MAC_MDIO_ADDR         = 0x02  # WireIn
    SLAVE_MAC_MDIO_WRITE_DATA   = 0x03  # WireIn
    SLAVE_MAC_START_ADDR        = 0x04  # WireIn
    SLAVE_MAC_TX_BURST_COUNT    = 0x05  # WireIn
    MASTER_MAC_CONTROL          = 0x06  # WireIn
    MASTER_MAC_TX_FRAME_SIZE    = 0x07  # WireIn
    MASTER_MAC_MDIO_ADDR        = 0x08  # WireIn
    MASTER_MAC_MDIO_WRITE_DATA  = 0x09  # WireIn
    MASTER_MAC_START_ADDR       = 0x0A  # WireIn
    MASTER_MAC_TX_BURST_COUNT   = 0x0B  # WireIn
    SLAVE_MAC_CONTROL_RD        = 0x20  # WireOut
    SLAVE_MAC_TX_FRAME_SIZE_RD  = 0x21  # WireOut
    SLAVE_MAC_MDIO_ADDR_RD      = 0x22  # WireOut
    SLAVE_MAC_MDIO_READ_DATA    = 0x23  # WireOut
    SLAVE_MAC_RX_PKT_STS        = 0x24  # WireOut
    SLAVE_MAC_RX_BYTE_CNT       = 0x25  # WireOut
    SLAVE_MAC_RX_CRC_ERR_CNT    = 0x26  # WireOut
    SLAVE_MAC_RX_RUNT_PKT_CNT   = 0x27  # WireOut
    SLAVE_MAC_RX_ERROR_CNT      = 0x28  # WireOut
    SLAVE_MAC_RX_MISSED_PKT_CNT = 0x29  # WireOut
    MASTER_MAC_CONTROL_RD       = 0x30  # WireOut
    MASTER_MAC_TX_FRAME_SIZE_RD = 0x31  # WireOut
    MASTER_MAC_MDIO_ADDR_RD     = 0x32  # WireOut
    MASTER_MAC_MDIO_READ_DATA   = 0x33  # WireOut
    MASTER_MAC_RX_PKT_STS       = 0x34  # WireOut
    MASTER_MAC_RX_BYTE_CNT      = 0x35  # WireOut
    MASTER_MAC_RX_CRC_ERR_CNT   = 0x36  # WireOut
    MASTER_MAC_RX_RUNT_PKT_CNT  = 0x37  # WireOut
    MASTER_MAC_RX_ERROR_CNT     = 0x38  # WireOut
    MASTER_MAC_RX_MISSED_PKT_CNT= 0x39  # WireOut
    SLAVE_MAC_FIFO_TRIGGER      = 0x41  # TriggerIn
    SLAVE_MAC_TX_PKT_EN         = 0x42  # TriggerIn
    SLAVE_MAC_RX_PKT_RD_DONE    = 0x43  # TriggerIn
    SLAVE_MAC_MDIO_TRIGGER      = 0x48  # TriggerIn
    MASTER_MAC_MDIO_TRIGGER     = 0x50  # TriggerIn
    MASTER_MAC_FIFO_TRIGGER     = 0x51  # TriggerIn
    MASTER_MAC_TX_PKT_EN        = 0x52  # TriggerIn
    MASTER_MAC_RX_PKT_RD_DONE   = 0x53  # TriggerIn
    SLAVE_MAC_MDIO_DONE         = 0x61  # TriggerOut
    SLAVE_MAC_RX_READY          = 0x62  # TriggerOut
    SLAVE_MAC_TX_DONE           = 0x68  # TriggerOut
    MASTER_MAC_TX_DONE          = 0x70  # TriggerOut
    MASTER_MAC_MDIO_DONE        = 0x71  # TriggerOut
    MASTER_MAC_RX_READY         = 0x72  # TriggerOut
    SLAVE_MAC_RX_FIFO_WR_DATA   = 0x81  # PipeIn
    SLAVE_MAC_TX_FIFO_WR_DATA   = 0x88  # PipeIn
    MASTER_MAC_TX_FIFO_WR_DATA  = 0x90  # PipeIn
    MASTER_MAC_RX_FIFO_WR_DATA  = 0x91  # PipeIn
    SLAVE_MAC_TX_FIFO_RD_DATA   = 0xA1  # PipeOut
    SLAVE_MAC_RX_FIFO_RD_DATA   = 0xA2  # PipeOut
    MASTER_MAC_TX_FIFO_RD_DATA  = 0xB1  # PipeOut
    MASTER_MAC_RX_FIFO_RD_DATA  = 0xB2  # PipeOut

    # Bit positions
    MAC_HALF_DUPLEX             = 0x0008
    MAC_RX_FILTER_DIS           = 0x0010
    MAC_RX_IGNORE_CRC_ERR       = 0x0020
    MAC_RMII_MODE               = 0x0040
    MAC_SPEED_10                = 0x0100
    TX_BLITZ_EN                 = 0x8000
    RX_STS_EN                   = 0x0200
    FORCE_STS_PKT               = 1



def OkGetAlpBoard(ok_functions, alpBoards, board):
    num_alp_boards = len(alpBoards)
    board_alp_if = board.GetBaseboardObject()
    attempts = 1
    found_board = 0
    while (attempts <= num_alp_boards) :
        if (board_alp_if != alpBoards[ok_functions.OkAlpBoardNum]):
            ok_functions.OkAlpBoardNum += 1
            attempts += 1
        else:
            found_board = 1
            break
    if (not found_board):
        print "ERROR: Could not identify ALP board!"
        return 0
    else:
        print "Selected ALP board", ok_functions.OkAlpBoardNum+1
        OkBoard = alpBoards[ok_functions.OkAlpBoardNum]
        return(OkBoard)

def OkGetAlpIf(OkBoard):
    OkAlpIf = OkBoard.GetALPInterface()
    return(OkAlpIf)

def OkGetInput(prompt_string):
    txt = ALPScriptInput(prompt_string)
    txt = txt.strip()
    return(txt)

def OkWriteReg(ok_functions, Reg, Data):
    ok_functions.OkAlpIf.SetWireInValue(Reg, Data, 0xFFFF)
    ok_functions.OkAlpIf.UpdateWireIns()

def OkReadReg(ok_functions, Reg):
    ok_functions.OkAlpIf.UpdateWireOuts()
    Value = ok_functions.OkAlpIf.GetWireOutValue(Reg)
    return(Value)
    
def OkFPGAWriteReg(alpBoard, Reg, Value):
    alpBoard.FPGAWriteReg(Reg, Value)
    
def OkFPGAReadReg(alpBoard, Reg):
    return(alpBoard.FPGAReadReg(Reg))

def OkSetDuplex(ok_functions):
    phy_duplex = ok_functions.OkPhyPort.ReadReg(ok_functions.OkPhyPort.PHY_PHYSTS) & ok_functions.OkPhyPort.P848_STS_DUPLEX
    if phy_duplex:
        mac_half_duplex = 0
        print "Configuring the MAC for full duplex mode"
    else:
        mac_half_duplex = ok_functions.MAC_HALF_DUPLEX
        print "Configuring the MAC for half duplex mode"
    if (ok_functions.OkSlave):
        mac_control    = ok_functions.SLAVE_MAC_CONTROL
        mac_control_rd = ok_functions.SLAVE_MAC_CONTROL_RD
    else:
        mac_control    = ok_functions.MASTER_MAC_CONTROL
        mac_control_rd = ok_functions.MASTER_MAC_CONTROL_RD
    mac_control_reg = OkReadReg(ok_functions, mac_control)
    mac_control_reg &= ~ok_functions.MAC_HALF_DUPLEX
    mac_control_reg |= mac_half_duplex
    OkWriteReg(ok_functions, mac_control, mac_control_reg)
    return (phy_duplex)

def OkSetPktLen(ok_functions):
    if (ok_functions.OkSlave):
        frame_size = ok_functions.SLAVE_MAC_TX_FRAME_SIZE
    else:
        frame_size = ok_functions.MASTER_MAC_TX_FRAME_SIZE
    OkWriteReg(ok_functions, frame_size, ok_functions.OkPktLength)

def OkSetBurstCount(ok_functions):
    if (ok_functions.OkSlave):
        burst_count_reg = ok_functions.SLAVE_MAC_TX_BURST_COUNT
    else:
        burst_count_reg = ok_functions.MASTER_MAC_TX_BURST_COUNT
    OkWriteReg(ok_functions, burst_count_reg, ok_functions.OkBurstCount & 0xFFFF)

def OkSetPktType(ok_functions):
    if (ok_functions.OkSlave):
        pkt_type_reg = ok_functions.SLAVE_MAC_START_ADDR
    else:
        pkt_type_reg = ok_functions.MASTER_MAC_START_ADDR
    OkWriteReg(ok_functions, pkt_type_reg, (ok_functions.OkPktType << 12))

def OkStartBurst(ok_functions):
    if (ok_functions.OkSlave):
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.SLAVE_MAC_TX_PKT_EN, 0)
    else:
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.MASTER_MAC_TX_PKT_EN, 0)
        
def OkStartBlitz(ok_functions):
    if (ok_functions.OkSlave):
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.SLAVE_MAC_TX_PKT_EN, 1)
    else:
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.MASTER_MAC_TX_PKT_EN, 1)
        
def OkStopBlitz(ok_functions):
    if (ok_functions.OkSlave):
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.SLAVE_MAC_TX_PKT_EN, 2)
    else:
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.MASTER_MAC_TX_PKT_EN, 2)
        
def OkWriteTXRam(ok_functions, strtAddr, buf):
    buf_tmp = array( 'B', buf)
    buf_tmp = buf_tmp.tostring()
    # Write RAM starting at address strtAddr
    if (ok_functions.OkSlave):
        OkWriteReg(ok_functions, ok_functions.SLAVE_MAC_START_ADDR, strtAddr)
        ok_functions.OkAlpIf.ActivateTriggerIn(ok_functions.SLAVE_MAC_FIFO_TRIGGER,1)
        ok_functions.OkAlpIf.WriteToPipeIn(ok_functions.SLAVE_MAC_TX_FIFO_WR_DATA, buf_tmp)
    else:
        OkWriteReg(ok_functions, ok_functions.MASTER_MAC_START_ADDR, strtAddr)
        OkAlpIf.ActivateTriggerIn(ok_functions.MASTER_MAC_FIFO_TRIGGER,1)
        OkAlpIf.WriteToPipeIn(ok_functions.MASTER_MAC_TX_FIFO_WR_DATA, buf_tmp)

def OkCheckTxDone(ok_functions):
    ok_functions.OkAlpIf.UpdateTriggerOuts()
    if (ok_functions.OkSlave):
        txdone = ok_functions.OkAlpIf.IsTriggered(ok_functions.SLAVE_MAC_TX_DONE,0x0001)
    else:
        txdone = ok_functions.OkAlpIf.IsTriggered(ok_functions.MASTER_MAC_TX_DONE,0x0001)
    return txdone

def OkCheckTxBlitzDone(ok_functions):
    ok_functions.OkAlpIf.UpdateTriggerOuts()
    if (ok_functions.OkSlave):
        txdone = ok_functions.OkAlpIf.IsTriggered(ok_functions.SLAVE_MAC_TX_DONE,0x0002)
    else:
        txdone = ok_functions.OkAlpIf.IsTriggered(ok_functions.MASTER_MAC_TX_DONE,0x0002)
    return txdone

def OkSetRxFilterMode(ok_functions):
    if (ok_functions.OkSlave):
        mac_control    = ok_functions.SLAVE_MAC_CONTROL
        mac_control_rd = ok_functions.SLAVE_MAC_CONTROL_RD
    else:
        mac_control    = ok_functions.MASTER_MAC_CONTROL
        mac_control_rd = ok_functions.MASTER_MAC_CONTROL_RD
    if (ok_functions.OkRxFilterMode):
        filter_mode = 0
        print "RX Filter Enabled"
    else:
        filter_mode = ok_functions.MAC_RX_FILTER_DIS
        print "RX Filter Disabled"
    mac_control_reg = OkReadReg(ok_functions, mac_control_rd)
    mac_control_reg &= ~ok_functions.MAC_RX_FILTER_DIS
    mac_control_reg |= filter_mode
    OkWriteReg(ok_functions, mac_control, mac_control_reg)


def OkFunctionInit(alpBoards, ok_functions, board, port, device, verbose):
    # Configure
    OkBoard = OkGetAlpBoard(ok_functions, alpBoards, board)
    if not OkBoard:
        return 0
    ok_functions.OkAlpIf = OkGetAlpIf(OkBoard)
    ok_functions.OkPhyPort = port
    
    conn = device.connector
    creg7 = OkBoard.FPGAReadReg(7)
    slave_conn = creg7 & 0x000C
    slave_conn = slave_conn >> 2
    master_conn = creg7 & 0x0003
    ok_functions.OkSlave = (conn == slave_conn)
    if ok_functions.OkSlave:
        slave_txt = "MAC 1"
    else:
        slave_txt = "MAC 2"
    
    print ""
    phy_duplex = OkSetDuplex(ok_functions)
    print "Selected ALP %s on Connector %d" % (slave_txt, conn+1)
    print ""
    if (verbose):
        print "Available Functions:"
        print "    OkCheckTxBlitzDone"
        print "    OkCheckTxDone"
        print "    OkFPGAReadReg"
        print "    OkFPGAWriteReg"
        print "    OkGetAlpBoard"
        print "    OkGetAlpIf"
        print "    OkGetInput"
        print "    OkReadReg"
        print "    OkSetBurstCount"
        print "    OkSetDuplex"
        print "    OkSetPktLen"
        print "    OkSetRxFilterMode"
        print "    OkStartBurst"
        print "    OkWriteReg"
        print "    OkWriteTXRam"
        print ""

