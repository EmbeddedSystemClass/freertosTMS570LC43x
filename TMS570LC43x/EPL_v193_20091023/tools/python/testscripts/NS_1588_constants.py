"""
 NS_1588_constants.py - ALP 1588 Library

 Copyright (c) 2006 National Semiconductor Corporation.
 All Rights Reserved.

 Implements constants used for 1588 ALP platfrom.
"""

# -------------------------------------------------------------------
# Constants:  Register definitions
#
# $Id: NS_1588_constants.py,v 1.2 2008/09/22 23:25:23 robertst Exp $
#
# $Log: NS_1588_constants.py,v $
# Revision 1.2  2008/09/22 23:25:23  robertst
# Updated test scripts from DaveR
# Updated EPLTest based on EPL update.
#
# Revision 1.4  2008/04/01 17:02:07  dave
# add correct PSF_CFG0 names.
#
# Revision 1.3  2008/03/13 12:11:15  benb
# Added Phyter FPGA registers/bits
#
# Revision 1.2  2007/11/30 15:47:16  dave
# replace EVNT_NOTIFY with EVNT_SINGLE
#
# Revision 1.1  2007/09/26 10:46:50  dave
# Initial revision
#
# Revision 1.4  2007/07/11 16:44:26  benb
# Added CNT_INT_EN to MISR
#
# Revision 1.3  2007/07/09 10:09:55  benb
# Imported lots of register definitions from defs.csi
#
# Revision 1.2  2007/07/05 11:08:01  dave
# add page to upper byte of each constant value.
#
#
#

# ---- Base Page register space offsets ----
BMCR	= 0x000		# basic mode control register
SW_RESET	= 0x8000	# s/w/ reset
GLB_LPBK	= 0x4000	# loopback (global ting)
SPD_SEL		= 0x2000	# speed selection
AN_EN 		= 0x1000	# auto-neg enable
PWR_DWN		= 0x0800	# power down
ISOLATE		= 0x0400	# isolate
AN_REST		= 0x0200	# auto-neg restart
DPLX 		= 0x0100	# duplex mode
COL_TEST	= 0x0080	# collision test
UNIDIR_EN	= 0x0020	# Unidirectional enable (TX without link)
BMSR	= 0x001		# basic mode status register
AUTONEG_DONE	= 0x0020	# autonegotiation complete
REM_FAULT 	= 0x0010	# remote fault
LINK_STATUS	= 0x0004	# link status
JABBER_DETECT	= 0x0002	# jabber detect
PHYID1	= 0x002		# PHY identification reg 1
PHYID2	= 0x003		# PHY identification reg 2
ANAR 	= 0x004		# auto-neg advertisement register
ADV_NP  	= 0x8000	# auto-neg advertise next page
ADV_RF  	= 0x2000	# auto-neg advertise remote fault
AN_TOGGLE_TX	= 0x0800	# auto-neg toggle tx bit for next page
ADV_ASM_DIR 	= 0x0800	# auto-neg advertise asymmetric pause
ADV_PAUSE 	= 0x0400	# auto-neg advertise symmetric pause
ADV_100F 	= 0x0100	# auto-neg advertise 100M full duplex
ADV_100H 	= 0x0080	# auto-neg advertise 100M half duplex
ADV_10F  	= 0x0040	# auto-neg advertise 10M full duplex
ADV_10H  	= 0x0020	# auto-neg advertise 10M half duplex
ADV_SEL  	= 0x0001	# auto-neg advertise protocol selector
ANLPAR	= 0x005		# auto-neg link partner abilities
ANER 	= 0x006		# auto-neg expansion register
ANNPTR	= 0x007		# nway next page transmit
PHYSTS	= 0x010		# Phy Status Register
MDIX_MODE	= 0x4000	# Nway MDIX mode indication
RCV_ERR_LATCH	= 0x2000	# receive error latch
POL_STAT 	= 0x1000	# polarity status
FCS_LATCH 	= 0x0800	# false carrier sense latch
SIG_DET  	= 0x0400	# 100Base-TX signal detect
DSCRM_LOCK 	= 0x0200	# 100Base-TX descrambler lock
PAGE_RCV 	= 0x0100	# page recieved
MII_INT  	= 0x0080	# MII interrupt Pending
REMOTE_FAULT	= 0x0040	# REmote fault
JAB_DET  	= 0x0020	# Jabber detected
ANEG_COMP 	= 0x0010	# Auto-neg complete
LPBK_STAT 	= 0x0008	# loopback enabled
DUP_STAT 	= 0x0004	# Duplex; 1= 0xFull duplex
SPD10  		= 0x0002	# Speed status; 1	= 0x10mb/s
LINK_STAT 	= 0x0001	# link status
MICR	= 0x011		# MII Interrupt Control Register
PTP_INT_SEL	= 0x0008	# Select PTP Interrupt for MISR[11]
TINT		= 0x0004	# Force test interrupt
INTEN		= 0x0002	# Master interrupt enable
UNMSK_INT	= 0x0002	# Unmask interrupts (old definition)
INT_OE		= 0x0001	# Interrupt Output Enable
INT_EN		= 0x0001	# Master interrupt enable (old definition)
MISR	= 0x012		# MII Interrupt Status Register
LQM_INT		= 0x8000	# Link Quality monitor event
ED_INT		= 0x4000	# change of energy detect event
LINK_INT	= 0x2000	# change of link status event
SPD_INT		= 0x1000	# speeed change event
JAB_INT		= 0x1000	# jabber event (revA1 only)
PTP_INT		= 0x0800	# duplex change event
DUP_INT		= 0x0800	# duplex change event
RF_INT		= 0x0800	# remote fault event (revA1 only)
ANC_INT		= 0x0400	# auto-neg complete event
FHF_INT		= 0x0200	# false carrier ctr reg 1/2 full event
CNT_INT		= 0x0200	# combined counter event (if PCF enabled)
RHF_INT		= 0x0100	# receive error ctr reg 1/2 full event
PCF_INT		= 0x0100	# Phy control frame event
LQM_INT_EN	= 0x0080	# enable interrupt on Link Quality Monitor event
ED_INT_EN	= 0x0040	# enable interrupt on energy detect event
UNMSK_ED	= 0x0040	# unmask change of energy detect event
LINK_INT_EN	= 0x0020	# enable interrupt on link status event
UNMSK_LINK	= 0x0020	# unmask change of link status event
SPD_INT_EN	= 0x0010	# enable interrupt on speed change
UNMSK_JAB	= 0x0010	# unmask jabber event
PTP_INT_EN	= 0x0008	# enable interrupt on duplex change
DUP_INT_EN	= 0x0008	# enable interrupt on duplex change
UNMSK_RF	= 0x0008	# unmask remote fault event
ANC_INT_EN	= 0x0004	# enable interrupt on auto-neg complete event
UNMSK_ANC	= 0x0004	# unmask auto-neg complete event
FHF_INT_EN	= 0x0002	# en int on false carrier ctr reg 1/2 full event
UNMSK_FHF	= 0x0002	# unmask false carrier ctr reg 1/2 full event
CNT_INT_EN	= 0x0002	# Counter interrupt enable
RHF_INT_EN	= 0x0001	# en int on receive error ctr reg 1/2 full event
UNMSK_RHF	= 0x0001
PCF_INT_EN	= 0x0001	# en int on phy control frame event
UNMSK_PCF	= 0x0001	# unmask phy control frame event
PAGESEL	= 0x013		# Page Select Register
PAGE_SEL 	= 0x0001	# page select bit
PAGE0_SEL 	= 0x0000	# page 0 select
PAGE1_SEL 	= 0x0001	# page 1 select
PAGE2_SEL 	= 0x0002	# page 2 select
PAGE3_SEL 	= 0x0003	# page 3 select
PAGE4_SEL 	= 0x0004	# page 4 select
PAGE5_SEL 	= 0x0005	# page 5 select
PAGE6_SEL 	= 0x0006	# page 6 select
PAGE7_SEL 	= 0x0007	# page 7 select
FCSCR	= 0x014		# False Carrier Sense Counter Register
RECR	= 0x015		# Receive Error Counter
PCSR	= 0x016		# PCS Configuration and Status Register
NON_AN_MDIX	= 0x8000	# Enable non-autoneg MDIX
RMII_PME_DIS	= 0x4000	# Disable RMII signaling of PME
EN_TXER		= 0x2000	# Enable TX_ER input
BP4B5B		= 0x1000	# bypass 4b5b - requires TX_ER input
FREECLK 	= 0x0800	# Receive clock free-running mode
FREE_CLK	= 0x0800	# Receive clock free-running mode
TRUE_QUIET	= 0x0400	# True Quiet mode enable
TQ_EN  		= 0x0400	# Enable true quiet
SD_FORCE_B	= 0x0200	# force signal detect B (datasheet name)
SD_FORCE	= 0x0200	# Force Signal Detect
SD_OPTION	= 0x0100	# SD option (AND lock with SD)
DESC_TIME	= 0x0080	# Descrambler Timeout
FX_EN		= 0x0040	# Fiber mode enable
F_LINK_100	= 0x0020	# Force Link 100 ok
FORCE_100_OK	= 0x0020	# Force Link 100 ok
F_100_OK	= 0x0020	# Force Link 100 ok
FEFI_TST 	= 0x0010	# enable FEFI test (datasheet name)
FEFI_TEST	= 0x0010	# Far-end-fault test enable
FEFI_EN		= 0x0008	# Far-end-fault enable
FEFI_ENABLE	= 0x0008	# Enable FEFI
BPNRZI 		= 0x0004	# Bypass NRZI
NRZI_BYPASS	= 0x0004	# bypass NRZI (datasheet name)
BPSCR 		= 0x0003	# bypass scrambler and descrambler
BPSCRonly	= 0x0002	# bypass scrambler only
SCRAM_BYPASS	= 0x0002	# bypass scrambler (datasheet name)
DESCRAM_BYPASS	= 0x0001	# bypass descrambler (datasheet name)
BPDESCR  	= 0x0001	# bypass descrambler only
BP_SCR		= DESCRAM_BYPASS|SCRAM_BYPASS
RBR	= 0x017		# RMII and Bypass Register
RMII	= RBR		# RMII and Bypass Register
SIM_WRITE 	= 0x8000	# simultaneous write
RMII_MASTER	= 0x4000	# RMII Master Mode
DIS_TX_OPT	= 0x2000	# Disable TX Optimization 
PMD_LOOP 	= 0x0100	# Internal Remote (PMD) Loopback
MII_RXSYNC 	= 0x0080	# MII Synchronous RX Mode Enable
MII_TXSYNC 	= 0x0040	# MII Synchronous TX Mode Enable
RMII_EN  	= 0x0020	# reduced MII mode Enable
RMII_1_0 	= 0x0010	# RMII Version 1.0 compatible
RX_OVF_STS 	= 0x0008	# RX FIFO overflow status
RX_UNF_STS 	= 0x0004	# RX FIFO underflow status
RX_RD_PTR_0 	= 0x0000	# RX FIFO threshold to 0
RX_RD_PTR_1 	= 0x0001	# RX FIFO threshold to 1
RX_RD_PTR_2 	= 0x0002	# RX FIFO threshold to 2
RX_RD_PTR_3 	= 0x0003	# RX FIFO threshold to 3
LEDCR	= 0x018		# LED Control Register
DIS_LEDSPD	= 0x0800	# Disable LED_SPD
DIS_LEDLNK	= 0x0400	# Disable LED_LNK
DIS_LEDACT	= 0x0200	# Disable LED_ACT
LEDACT_RX	= 0x0100	# Activity LED only on RX
DRV_LEDSPD	= 0x0020	# Enable driving LED_SPD
DRV_LEDLNK	= 0x0010	# Enable driving LED_LNK
DRV_LEDACT	= 0x0008	# Enable driving LED_ACTCOL
LEDSPD		= 0x0004	# Drive 1 on LED_SPD
LEDLNK		= 0x0002	# Drive 1 on LED_LNK
LEDACT		= 0x0001	# Drive 1 on LED_ACT
PHYCR	= 0x019		# Phy Control Register
PHYCTRL	= PHYCR		# Phy Control Register (data sheet name)
AN_MDIX_EN	= 0x8000	# Autoneg MDIX enable
AN_FORCE_MDIX	= 0x4000	# Autoneg force MDIX
PAUSE_RX_NEG	= 0x2000	# Pause receive enable negotiated
PAUSE_TX_NEG	= 0x1000	# Pause transmit enable negotiated
BIST_F_ERR	= 0x0800	# BIST Force Error
PSR_15		= 0x0400	# BIST sequence select
BIST_STATUS	= 0x0200	# BIST test status
BIST_START	= 0x0100	# BIST start
BP_STRETCH 	= 0x0080	# bypass LED stretching (datasheet name)
BPSTRETCH 	= 0x0080	# bypass LED stretching
LED_CNFG_3 	= 0x0060	# LED configuration 3
LED_CNFG_2 	= 0x0040	# LED configuration 2
LED_CNFG_1 	= 0x0020	# LED configuration 1
LED_CNFG_0 	= 0x0000	# LED configuration 0
TENBTSCR= 0x01A		# 10BaseT Status and Control Register
_10BTSCR= TENBTSCR	# 10BaseT Status and Control Register
SERIAL10	= 0x8000	# 10BT Serial Mode
REJECT_100BASET	= 0x4000	# Reject 100Base-TX signaling in the receiver
LOOPBACK_10_DIS	= 0x0100	# 10M loopback disable (datasheet name)
LPBK_DIS 	= 0x0100	# 10M loopback disable
LP_DIS  	= 0x0080	# 10M link pulse disable
FORCE_LINK_10	= 0x0040	# force 10M link (datasheet name)
F_10_LINK 	= 0x0040	# Force 10M link
FORCE_POL_COR	= 0x0020	# force 10M polarity correction (datasheet name)
F_POL_COR 	= 0x0020	# Force polarity correction
POLARITY 	= 0x0010	# Inverted polarity detected
AUTOPOL_DIS 	= 0x0008	# auto polarity det/corr disable (datsheet name)
POL_DIS  	= 0x0008	# Polarity detection/correction disable
LOW_SQUELCH 	= 0x0004	# Low Squelch
HEARTBEAT_DIS	= 0x0002	# heartbeat disable (datasheet name)
HB_DIS  	= 0x0002	# Heartbeat disable
JABBER_DIS 	= 0x0001	# jabber disable (datasheet name)
JAB_DIS  	= 0x0001	# Jabber disable
CDCTRL1	= 0x01B		# CD test register 1 (datasheet name)
CDTEST1	= CDCTRL1	# CD test register 1
CD_ENABLE 	= 0x8000	# CD enable
DCDCOMP  	= 0x4000	# duty cycle distortion compensation
FIL_TTL  	= 0x2000	# waveshaper current source test
RISETIME_43 	= 0x0000	# CD rise time	= 0x4.3ns (default)
RISETIME_36 	= 0x0800	# CD rise time	= 0x3.6ns
RISETIME_29 	= 0x1800	# CD rise time	= 0x2.9ns
FALLTIME_43 	= 0x0000	# CD fall time	= 0x4.3ns (default)
FALLTIME_36 	= 0x0200	# CD fall time	= 0x3.6ns
FALLTIME_29 	= 0x0600	# CD fall time	= 0x2.9ns
CDTESTEN 	= 0x0100	# CD test mode enable
BIST_PTP	= 0x0080	# Enable PTP BIST mode
MII_CLOCK_EN	= 0x0040	# Enable MII clock outputs in non-MII modes
BIST_CONT 	= 0x0020	# Continuous BIST mode control
CDPATTEN_10 	= 0x0010	# 10M CD test pattern enable
MDIO_PULL_EN	= 0x0008	# MDIO pullup enable
PATT_GAP_10M	= 0x0004	# IFG for 10M data or NLPs
CDPATTSEL_0 	= 0x0000	# CD pattern select
CDPATTSEL_1 	= 0x0001	# CD pattern select
CDPATTSEL_2 	= 0x0002	# CD pattern select
CDPATTSEL_3 	= 0x0003	# CD pattern select
PHYCR2	= 0x01C		# PHY Control Register 2
SYNC_ENET_EN	= 0x2000	# Synchronous Ethernet Enable
CLK2MAC_RXCLK	= 0x1000	# 100Mb RX_CLK mirrored on CLK2MAC
MGNT_BC_EN	= 0x0800	# MDIO Broadcast Enable
PHYTER_COMP	= 0x0400	# Phyter Compatibility Enable
MDIO_BC_EN	= 0x0800	# MDIO Broadcast Enable
CLK2MAC_DISABLE 	= 0x0002	# Disable CLK2MAC Output
FAST_ADAPT 	= 0x0001	# Enable Fast DSP Adaption
EDCR	= 0x01D		# Energy Detect control reg
ED_EN		= 0x8000	# Energy Detect enable
ED_AUTO_UP	= 0x4000	# Energy Detect Automatic Power Up 
ED_AUTO_DOWN	= 0x2000	# Energy Detect Automatic Power Down
ED_MAN		= 0x1000	# Energy Detect Manual Power Up/Down
ED_BURST_DIS	= 0x0800	# Energy Detect Data Pulse Burst Disable
ED_PWR_STATE	= 0x0400	# Energy Detect Power State
ED_ERR_MET	= 0x0200	# Energy Detect Error Threshold Met
ED_DATA_MET	= 0x0100	# Energy Detect Data Threshold Met
ED_ERR_COUNT	= 0x00f0	# Energy Detect Error Threshold
ED_DATA_COUNT	= 0x000f	# Energy Detect Data Threshold
AFECR 	= 0x01E		# Analog Front End Control Register
DIS_AUTO_AFE	= 0x8000	# Disable Auto AFE powerup
FAST_POWERUP	= 0x4000	# Use Fast powerup sequence
FCO_RST		= 0x2000	# FCO Reset
ADC_RST		= 0x1000	# ADC Reset
CD10_RST	= 0x0800	# CD10 Reset
CD100_RST	= 0x0400	# CD100 Reset
AFE_REG_RST	= 0x0200	# AFE Registers Reset
PMG_RST		= 0x0100	# PGM Reset
PGM_RST		= 0x0100	# PGM Reset
CGM_RST		= 0x0080	# CGM Reset
AFE_BLOCK_SEL	= 0x0040	# Select between FCO1/PGM1 and FCO2/PGM2
AAGC_AEQ_EN	= 0x0020	# AAGC/AEQ Enable
FCO_EN 		= 0x0010	# FCO Enable
ADC_EN 		= 0x0008	# ADC Enable
CD_EN 		= 0x0004	# CD Enable
PGM_EN 		= 0x0002	# PGM Enable
CGM_EN 		= 0x0001	# CGM Enable
PCFCR   = 0x01F		# PHY Control Frames Configuration Register
PCF_STS_ERR	= 0x8000	# Phy Control Frame Status - Error received
PCF_STS_OK	= 0x4000	# Phy Control Frame Status - Frame OK
PCF_DA_SEL	= 0x0100	# Phy Control Frame - Dest Addr select
PCF_INT_ERR	= 0x0080	# Phy Control Frame - Interrupt on Error
PCF_INT_OK	= 0x0040	# Phy Control Frame - Interrupt on Frame OK
PCF_BC_DIS	= 0x0020	# Phy Control Frame - Interrupt on Error
PCF_BUF		= 0x1		# Shift for PCF_BUF size
PCF_EN		= 0x0001	# Phy Control Frame Enable

# ---- Page 1 register space offsets ----
PMD_CNFG = 0x114		# PMD Configuration (Datasheet name)
PMDSCR		= PMD_CNFG	# PMD status and control
PMDCSR		= PMD_CNFG	# PMD Control/Status Register
AUTONEG_LPBK	= 0x8000	# auto-neg loopback
DISABLE_DCO_10	= 0x0400	# Disable 10Mb DCO correction
SOFT_RESET 	= 0x0200	# soft reset
LEN100_AEQ 	= 0x0100	# Enable AEQ value on LEN100_DET[9:8]
SIEMENS_MODE	= 0x0010	# Siemens mode, block RMII CRS_DV on RX_ER
FX_COMP_OBS	= 0x0003	# FX Comparator observe test mode
MDIX_OBS	= 0x0002	# MDIX Observe test mode
ED_OBS		= 0x0001	# Energy Detect Observe test mode
TMR	= 0x115		# Test Mode Register (datasheet name)
TMODE	= TMR		# test mode register
CLK_ADC_OEN 	= 0x8000	# Output enable for ADC_CLK pad, revB+
CLK_ADC_BYP	= 0x4000	# Select external ADC clock
SD_OBS		= 0x0200	# Signal Detect Observe
ATP_EN		= 0x0100	# Enable analog test points on LED's
ATP1_EN		= 0x0100	# Enable analog test points on LED's
ATP0_EN		= 0x0080	# Enable analog test points on LED's
STND_ALONE 	= 0x0000	# PHY standalone mode (NO LONGER USED)
DIS_IO_TURBO	= 0x0040	# Disable IO Turbo switch for ADC/RMII
BYP_ADC  	= 0x0020	# Bypass ADC
BYP_PLLS 	= 0x0010	# Bypass PLL
TESTSEL_NRZI	= 0x0008	# NRZI
TESTSEL_NLPLIT	= 0x0007	# auto-neg arbitration
TESTSEL_ANA 	= 0x0006	# auto-neg arbitration
TESTSEL_ANTX	= 0x0005	# auto-neg arbitration
TESTSEL_ANRX	= 0x0004	# auto-neg arbitration
PLLBIST_OBS	= 0x0003	# PLLBIST Observe Mode
TESTSEL_CDBP	= 0x0002	# CD bypass
TESTSEL_ADC 	= 0x0001	# ADC standalone
TMR2 	= 0x116		# Test Mode Register 2
DSP_INIT_OBS	= 0xc000	# DSP Init Sequence Observe Test mode
AAGC_AEQ_OBS	= 0xb000	# AAGC/AEQ Control Observe Test mode
TRL_LFO_OBS	= 0xa000	# TRL LoopFilter Output Observe Test mode
TRL_BETA_OBS	= 0x9000	# TRL Beta Acc Observe Test mode
TRL_PHASE_OBS	= 0x8000	# TRL Phase Observe Test mode
SLICER_OBS	= 0x7000	# Slicer Observe Test mode
BLW_OBS		= 0x6000	# BLW Observe Test mode
AGC_OBS		= 0x5000	# AGC Adaptation Observe Test mode
DP_SYMB_OBS	= 0x4000	# Datapath Symbol Observe Test mode
EQ_COEF3_OBS	= 0x3000	# Equalizer Coef3 Observe Test mode
EQ_COEF2_OBS	= 0x2000	# Equalizer Coef2 Observe Test mode
EQ_COEF1_OBS	= 0x1000	# Equalizer Coef1 Observe Test mode
DP_SYMB_CON 	= 0x0400	# DP_SYMB Control test mode
AD_SAMPLE_CON	= 0x0800	# AD_SAMPLE Control test mode
SIGN_X_CON	= 0x0c00	# SIGN_X Control test mode
CR_FCO_CON	= 0x0b00	# CR_FCO Control test mode
INT_DUMP_CON	= 0x0a00	# INT_DUMP Control test mode
LF_OUT_CON	= 0x0900	# LF_OUT Control test mode
PHASE_DET_CON	= 0x0800	# PHASE_DET Control test mode
TARGET_CON	= 0x0700	# Target Control test mode
SCALER_CON	= 0x0600	# Scaler Control test mode
MLT3_NRZ_ERR_CON	= 0x0500	# MLT3(NRZ)/Error Control test mode
TAP1_CON	= 0x0400	# Tap1 Control test mode
BW_CON		= 0x0300	# BLW Control test mode
AGC_CON		= 0x0200	# AGC Control test mode
AGC_MULT_CON	= 0x0100	# AGC Mult Control test mode
DSP_CTRL1 = 0x117		# DSP control Reg 1
PMD_INIT_TEST	= 0x8000	# PMD Init Test mode (speed up timers)
DIS_PMD_INIT 	= 0x4000	# Disable Auto PMD Init (AEQ and AAGC)
IGNORE_MSEOK 	= 0x2000	# Ignore MSE_OK in AFE/DSP LOCKED state
BLW_8BITS 	= 0x0800	# Restrict BLW to 8 bits
AGC_7BITS 	= 0x0400	# Restrict AGC to 7 bits
MSE_THSEL	= 0x0200	# Slicer MSE Threshold select
INIT_MSE	= 0x0100	# Init Slicer MSE
FORCE_MSE_OK	= 0x0080	# Force Slicer MSE OK
FORCE_MSE_NOTOK	= 0x0040	# Force Slicer MSE Not OK
LOAD_BLW 	= 0x0020	# Load Baseline Wander
FRZ_BLW 	= 0x0010	# Freeze Baseline Wander
LOAD_AGC 	= 0x0008	# Load AGC multiplier
FRZ_AGC 	= 0x0004	# Freeze AGC multiplier
DSP_CTRL2 = 0x118		# DSP control Reg 2 
LOAD_AEQ_THRESH	= 0x4000	# Load AEQ COEF1 Comparison Threshold
DIS_AEQ1	= 0x2000	# Disable AEQ of 1
MAX_AEQ_3	= 0x1800	# Max AEQ to 3
MAX_AEQ_2	= 0x1000	# Max AEQ to 2
MAX_AEQ_1	= 0x0800	# Max AEQ to 1
MAX_AEQ_0	= 0x0000	# Max AEQ to 0
FORCE_AEQ_3	= 0x0700	# Force AEQ to value of 3
FORCE_AEQ_2	= 0x0500	# Force AEQ to value of 2
FORCE_AEQ_1	= 0x0300	# Force AEQ to value of 1
FORCE_AEQ_0	= 0x0100	# Force AEQ to value of 0
FORCE_AEQ	= 0x0100	# Force AEQ
LOAD_AAGC_TMR	= 0x0080	# Load Analog AGC Timer
LOAD_AAGC_ACC	= 0x0040	# Load Analog AGC Accumulator
AAGC_FRZ	= 0x0020	# Freeze Analog AGC Accumulator
AAGC_THR_12	= 0x0012	# AAGC Threshold to default of 12
TRL_CTRL = 0x119		# TRL Control Register
TRL_CTRL1 = TRL_CTRL	# TRL Control Register 1
LOAD_TRL_BETA	= 0x8000	# Load TRL Beta accumulator
LOAD_TRL_LFO	= 0x4000	# Load TRL LFO accumulator
LOAD_TRL_PH	= 0x2000	# Load TRL Phase register
TRL_FRZ_LFO	= 0x1000	# Freeze 8-bit Loopfilter output accumulator
TRL_FRZ_ACC	= 0x0800	# Freeze TRL Beta accumulator
TRL_TRACK	= 0x0400	# Enables tracking mode
TRL_SEL_REG	= 0x0200	# Selects registered Phase Detect value
TRL_KILLREG	= 0x0100	# Clears all TRL registered fields
DEQ_CTRL = 0x11A		# DEQ Control Register
ALLOW_POS_C1	= 0x2000	# Allow positive Coefficient 1
COEF3_6BITS 	= 0x1000	# Restrict Equalizer Coef 3 to 6 bits
COEF2_7BITS 	= 0x0800	# Restrict Equalizer Coef 2 to 7 bits
COEF1_8BITS 	= 0x0400	# Restrict Equalizer Coef 1 to 8 bits
LOAD_COEF3 	= 0x0200	# Load Equalizer Coef 1
LOAD_COEF2 	= 0x0100	# Load Equalizer Coef 1
LOAD_COEF1 	= 0x0080	# Load Equalizer Coef 1
NOSHIFT_N1 	= 0x0040	# Dont shift Coef N1
FREEZE_COEF 	= 0x0020	# Freeze Equalizer Coefs
KILL_COEF3 	= 0x0010	# Kill Equalizer Coef 1
KILL_COEF2 	= 0x0008	# Kill Equalizer Coef 1
KILL_COEF1 	= 0x0004	# Kill Equalizer Coef 1
KILL_EQ_TAP0 	= 0x0002	# Kill Equalizer Tap 0
KILL_COEFF_N1	= 0x0001	# Kill Equalizer Precursor
AN_TEST	= 0x11B		# Autoneg test register
ANEG_TEST = AN_TEST	# Autoneg test register
LOAD_ED_TMR	= 0x4000	# load ED ms timer
LOAD_NLP_RCV	= 0x2000	# load NLP receive LIT timer
LOAD_NLP_MAX	= 0x1000	# load NLP max timer
LOAD_NLP_MIN	= 0x0800	# load NLP min timer
LOAD_FLP_DATA	= 0x0400	# load auto-neg FLP timer
LOAD_TX_ANEG	= 0x0200	# load auto-neg TX timer
LOAD_ARB_ANEG	= 0x0100	# load auto-neg ARB timer
EXT_CFG	= 0x11C		# Extended Config register
EXTCFG	= EXT_CFG	# Extended Config register
HIGH_FLP_THRESH	= 0x1000	# high FLP threshold
NLP_RX_FIX	= 0x0020	# Eliminates lockup condition in 802.3 NLP RX SM
ADC_WATCH_OUT	= 0x0002	# Enable ADC watchdog output to external pin
ADC_WATCH_EN	= 0x0001	# Enables the ADC watchdog function
TST_CTRL = 0x11D	# Test Control register
DSPSEL_EQ1 	= 0x0000	# Equalizer Datapath output, coef1 (default)
DSPSEL_EQ2 	= 1 << 11	# EQ Coef 3, EQ coef 2 [8:1]
DSPSEL_AGCBLW	= 2 << 11	# AGC and BLW adapt
DSPSEL_SLICER	= 3 << 11	# Slicer Outputs
DSPSEL_TRL 	= 4 << 11	# TRL Phase and Beta
DSPSEL_LFO 	= 5 << 11	# TRL Loopfilter Output
DSPSEL_AAGCAEQ	= 6 << 11	# AAGC/AEQ Controls
DSPSEL_ADC 	= 7 << 11	# ADC data
DSPSEL_AN_ARB	= 8 << 11	# auto-neg arbitration timer
DSPSEL_AN_TX	= 9 << 11	# auto-neg TX timer
DSPSEL_AN_FLP	= 0x0a << 11	# auto-neg FLP timer
DSPSEL_AN_NLPN	= 0x0b << 11	# auto-neg NLP min timer
DSPSEL_AN_NLPX	= 0x0c << 11	# auto-neg NLP max timer
DSPSEL_AN_RCV	= 0x0d << 11	# auto-neg NLP receive timer
DSPSEL_ED_TMR	= 0x0e << 11	# ED ms timer
PLLBIST_REF0	= 0x10 << 11	# Read PLL Bist Reference Counter Low
PLLBIST_REF1	= 0x11 << 11	# Read PLL Bist Reference Counter High
PLLBIST_PGM0	= 0x12 << 11	# Read PLL Bist PGM Counter Low
PLLBIST_PGM1	= 0x13 << 11	# Read PLL Bist PGM Counter High
PLLBIST_CGM0	= 0x14 << 11	# Read PLL Bist CGM Counter Low
PLLBIST_CGM1	= 0x15 << 11	# Read PLL Bist CGM Counter High
PLLBIST_FCO0	= 0x16 << 11	# Read PLL Bist FCO Counter Low
PLLBIST_FCO1	= 0x17 << 11	# Read PLL Bist FCO Counter High
PTP_TEST_CLK	= 1 << 6	# PTP Test Mode: Clock
PTP_TEST_TX 	= 2 << 6	# PTP Test Mode: TX Parse
PTP_TEST_TXTSU	= 3 << 6	# PTP Test Mode: TX TSU
PTP_TEST_RX 	= 4 << 6	# PTP Test Mode: RX Parse
PTP_TEST_RXTSU	= 5 << 6	# PTP Test Mode: RX TSU
PTP_TEST_EVENT	= 6 << 6	# PTP Test Mode: EVENT
PTP_TEST_TRIG	= 7 << 6	# PTP Test Mode: TRIG
PTP_TEST_STS_PKT	= 8 << 6	# PTP Test Mode: STS Packet
PTP_TEST_STS_BUF	= 9 << 6	# PTP Test Mode: STS Buffer
PLLBIST_SEL 	= 0x0020	# PLL BIST PGM and FCO 1 or 2 select
PLLBIST_DONE	= 0x0010	# PLL BIST done (read only)
PLLBIST_MODE	= 0x0008	# PLL BIST mode (1	= 0xbench, 0	= 0xATE)
PLLBIST_EN 	= 0x0004	# Enable PLL BIST
PLLBIST_RST 	= 0x0002	# RePLL BIST logic
SAMPLE_DATA 	= 0x0001	# Sample DSP or AN data
SD_CFG	= 0x11E		# Signal Detect Configuration Register
SDCFG	= SD_CFG	# signal detect configuration
SD_P2P  	= 0x8000	# signal detect peak-to-peak algorithm
AN_TEST_EN 	= 0x4000	# auto-neg test enable
PMA_TEST_EN 	= 0x2000	# link monitor timeout reduced to 32 clocks
SD_DELTA 	= 0x1000	# SD on/off thresholds are different
SD_SHORT 	= 0x0800	# SD on/off thresholds inc. by 1 count
SCALE_10BT 	= 0x0400	# ?
FORCE_SIG_DET	= 0x0200	# force signal detect
SIG_DET_TIME	= 0x0100	# reduces signal detect timer
TEST_DATA = 0x11F		# Test Data Register
TESTDATA = TEST_DATA	# Test Data Register
TSTDAT	= TEST_DATA	# Test Data Register

# ---- Page 2 register space offsets ----
LEN100_DET = 0x214	# 100Mb Length Detect Register
FREQ100 = 0x215		# 100Mb Frequency Detect Register
SAMPLE_FREQ	= 0x8000	# Sample TRL Beta accumulator
SELECT_FC	= 0x0100	# Select TRL LFO instead of TRL Beta
TDR_CTRL = 0x216	# TDR Control Register
TDR_EN  	= 0x8000	# TDR Enable
TDR_100MB 	= 0x4000	# Use 100Mb Transmitter for TDR
TDR_TX_CHNL 	= 0x2000	# Send pulse on transmit channel
TDR_RX_CHNL 	= 0x1000	# monitor Receive channel
TDR_SEND_PULSE	= 0x0800	# Send pulse control
TDR_MINMODE 	= 0x0080	# Look for minimum values
TDR_RX_SEL 	= 0x0040	# Receive data source (1=Slicer input)
TDR_WIN = 0x217		# TDR Control Register
TDR_PEAK = 0x218	# TDR Peak Register
TDR_THR  = 0x219	# TDR Threshold Register
VAR_CTRL = 0x21A	# Variance Control Register
LOAD_VAR_HI	= 0x0020	# Load upper variance register
LOAD_VAR_LO	= 0x0010	# Load lower variance register
VAR_FREEZE	= 0x0008	# Freeze Variance Registers
VAR_ENABLE	= 0x0001	# Enable Variance calculation
VAR_DATA = 0x21B	# Variance Data Register
LQMR	= 0x21D		# Link Quality Monitor Register
LQM_EN		= 0x8000	# Enable all 4 monitor functions
LQM_AUTO_FC	= 0x4000	# Enable Auto Reof DSP on FC Warning
LQM_AUTO_FREQ	= 0x2000	# Enable Auto Reof DSP on FREQ Warning
LQM_AUTO_DBLW	= 0x1000	# Enable Auto Reof DSP on DBLW Warning
LQM_AUTO_DAGC	= 0x0800	# Enable Auto Reof DSP on DAGC Warning
LQM_AUTO_C1	= 0x0400	# Enable Auto Reof DSP on C1 Warning
FC_HI_WARN	= 0x0200	# FREQ CONTROL Threshold Warning
FC_LO_WARN	= 0x0100	# FREQ CONTROL Threshold Warning
FREQ_HI_WARN	= 0x0080	# FREQ Threshold Warning
FREQ_LO_WARN	= 0x0040	# FREQ Threshold Warning
DBLW_HI_WARN	= 0x0020	# DBLW Threshold Warning
DBLW_LO_WARN	= 0x0010	# DBLW Threshold Warning
DAGC_HI_WARN	= 0x0008	# DAGC Threshold Warning
DAGC_LO_WARN	= 0x0004	# DAGC Threshold Warning
C1_HI_WARN	= 0x0002	# C1 Threshold Warning
C1_LO_WARN	= 0x0001	# C1 Threshold Warning
LQDR	= 0x21E		# Link Quality Data Register
SAMPLE_PARAM	= 0x2000	# Sample DSP Parameter
WRITE_LQ_THR	= 0x1000	# Write LQM Threshold
LQ_THR_SEL11	= 0x0b00	# Check Threshold 11
LQ_THR_SEL10	= 0x0a00	# Check Threshold 10
LQ_THR_SEL9	= 0x0900	# Check Threshold 9
LQ_THR_SEL8	= 0x0800	# Check Threshold 8
LQ_THR_SEL7	= 0x0700	# Check Threshold 7
LQ_THR_SEL6	= 0x0600	# Check Threshold 6
LQ_THR_SEL5	= 0x0500	# Check Threshold 5
LQ_THR_SEL4	= 0x0400	# Check Threshold 4
LQ_THR_SEL3	= 0x0300	# Check Threshold 3
LQ_THR_SEL2	= 0x0200	# Check Threshold 2
LQ_THR_SEL1	= 0x0100	# Check Threshold 1
LQ_THR_SEL0	= 0x0000	# Check Threshold 0
LQ_VAR2_SEL	= 0x0b00	# Select Variance
LQ_VAR1_SEL	= 0x0a00	# Select Variance
LQ_FC_SEL	= 0x0800	# Select Frequency Control
LQ_FREQ_SEL	= 0x0600	# Select Frequency Offset
LQ_DBLW_SEL	= 0x0400	# Select DBLW
LQ_DAGC_SEL	= 0x0200	# Select DAGC
LQ_C1_SEL	= 0x0000	# Select DEQ C1
LQ_HI_SEL	= 0x0100	# Select High Threshold
LQ_LO_SEL	= 0x0000	# Select Low Threshold
LQMR2	= 0x21F		# Link Quality Monitor Register 2
LQM_AUTO_VAR	= 0x0400	# Enable Auto Reof DSP on Variance warning
VAR_HI_WARN	= 0x0002	# Variance threshold warning


# ---- Page 3 test mode register space offsets ----
CGCR 	= 0x314		# Clock Gating Control Register
DIS_TRIG_UPD_GATE	= 0x8000	# Disable PTP trigger update clock gating
DIS_TX_TS_GATE	= 0x4000	# Disable PTP TX timestamp clock gating
DIS_RX_TS_GATE	= 0x2000	# Disable PTP RX timestamp clock gating
DIS_RX_INFO_GATE	= 0x1000	# Disable PTP RX information clock gating
DIS_EVNT_GATE	= 0x0800	# Disable PTP event read/capture clock gating
DIS_CLK_UPD_GATE	= 0x0400	# Disable PTP clock update clock gating
DIS_REG125_GATE	= 0x0200	# Disable PTP 125MHz register clock gating
DIS_CLKTX_GATE	= 0x0100	# Disable PTP TX Parse static clock gating
DIS_CLKRX_GATE	= 0x0080	# Disable PTP RX Parse static clock gating
DIS_CLK125_GATE	= 0x0040	# Disable PTP 125MHz static clock gating
DIS_CLKDIV_GATE	= 0x0020	# Disable PTP 125MHz clock divider gating
DIS_ADC125_GATE	= 0x0004	# Disable static 125MHz ADC RX clock gating
DIS_ADC80_GATE	= 0x0002	# Disable static 80MHz ADC RX clock gating
DIS_REGCLK_GATE	= 0x0001	# Disable dynamic clock gating for mgnt regs
CDCR1	= 0x317	# CD10/100 Control Register
CD10_PREEMP41	= 0x1000	# Enable CD10 4/1 preemphasis
CDCR2	= 0x318	# CD100 Control Register
CD100_PATTSEL_14T6T= 0x0600	# 14T/6T pattern
CD100_PATTSEL_2T	= 0x0400	# 2T pattern
CD100_PATTSEL_ONES	= 0x0200	# Ones pattern
CD100_PATTSEL_ZEROS= 0x0000	# Zeros pattern
CD100_TEST_PATT_EN	= 0x0100	# Enable test pattern generation
CD100_TEST_EN	= 0x0001	# Enable test mode
FCO1CR	= 0x319	# FCO1 Control Register
FCO2CR	= 0x31A	# FCO2 Control Register
FCO_DISABLE_D2S_FB	= 0x2000	# Disable FCO feedback around inverter
FCO_PPM_RANGE_660	= 0x0000	# 660ppm
FCO_PPM_RANGE_440	= 0x1000	# 440ppm
FCO_PPM_RANGE_220	= 0x1800	# 220ppm
FCO_PPM_INV	= 0x0080	# Invert FA word bits
FCO_JC_RESET	= 0x0040	# ReJohnson counter
FCO_PA_UP_DN	= 0x0020	# Step up or down
FCO_CURR	= 0x0010	# Double FCO mixer current
FCO_TEST_EN	= 0x0008	# Enable test of Johnson counter
FCO_SEL_32	= 0x0004	# Select falling edge of 31.25MHz clock
FCO_FORCE_PGM	= 0x0002	# Force use of PGM 31.25MHz clock in FCO
FCO_PA_STEP_EN	= 0x0001	# Step clock
ADCCR1	= 0x31B	# ADC Control Register 1
ADC_TST_CLK_EN	= 0x0004	# Enable ADC test clock
ADC_FORCE_CMP	= 0x0002	# Force comparators to 01
ADC_LOW_POWER	= 0x0001	# Enable 10Mb low power
ADCCR2	= 0x31C	# ADC/AAGC/ED Control Register
AAGC_ENAUX	= 0x8000	# Enable AAGC bypass
BGREGCR	= 0x31D	# Bandgap/Regulator Control Register
CGMCR	= 0x31E	# CGM Control Register
PGMCR	= 0x31F	# PGM Control Register

# ---- Page 4 register space offsets ----
PTP_CTL = 0x414  # IEEE 1588 Control Register
TRIG7_SEL 	= (7 << 10)  # Select Trigger for enable/read/load
TRIG6_SEL 	= (6 << 10)
TRIG5_SEL 	= (5 << 10)
TRIG4_SEL 	= (4 << 10)
TRIG3_SEL 	= (3 << 10)
TRIG2_SEL 	= (2 << 10)
TRIG1_SEL 	= (1 << 10)
TRIG0_SEL 	= (0 << 10)
TRIG_DIS 	= 0x0200	# Disable Trigger
TRIG_EN 	= 0x0100	# Enable Trigger
TRIG_READ 	= 0x0080	# Read Trigger
TRIG_LOAD 	= 0x0040	# Load Trigger
PTP_READ_CLK 	= 0x0020	# Read PTP Clock
PTP_LOAD_CLK 	= 0x0010	# Load PTP Clock
PTP_STEP_CLK 	= 0x0008	# Step (add/sub) PTP Clock
PTP_ENABLE 	= 0x0004	# Enable PTP Clock
PTP_DISABLE 	= 0x0002	# Disable PTP Clock
PTP_RESET 	= 0x0001	# Reset PTP Clock
PTP_TDR = 0x415  # IEEE 1588 Time Data Register
PTP_STS = 0x416  # IEEE 1588 Status Register
TXTS_RDY 	= 0x0800	# Transmit TimeStamp Ready	
PTP_TXTS_RDY 	= 0x0800	# Transmit TimeStamp Ready	
RXTS_RDY 	= 0x0400	# Receive TimeStamp Ready
PTP_RXTS_RDY 	= 0x0400	# Receive TimeStamp Ready
TRIG_DONE 	= 0x0200	# Trigger done
PTP_TRIG_RDY 	= 0x0200	# Trigger done
EVENT_RDY 	= 0x0100	# Event Ready
PTP_EVNT_RDY 	= 0x0100	# Event Ready
TXTS_IE 	= 0x0008	# Transmit Timestamp Interrupt Enable
RXTS_IE 	= 0x0004	# Receive Timestamp Interrupt Enable
TRIG_IE 	= 0x0002	# Trigger Interrupt Enable
EVENT_IE 	= 0x0001	# Event Interrupt Enable
PTP_TSTS = 0x417  # IEEE 1588 Trigger Status Register
TRIG7_LATE 	= 0x8000	# Trigger 7 Late indication
TRIG7_ACTIVE 	= 0x4000	# Trigger 7 Active
TRIG6_LATE 	= 0x2000
TRIG6_ACTIVE 	= 0x1000
TRIG5_LATE 	= 0x0800
TRIG5_ACTIVE 	= 0x0400
TRIG4_LATE 	= 0x0200
TRIG4_ACTIVE 	= 0x0100
TRIG3_LATE 	= 0x0080
TRIG3_ACTIVE 	= 0x0040
TRIG2_LATE 	= 0x0020
TRIG2_ACTIVE 	= 0x0010
TRIG1_LATE 	= 0x0008
TRIG1_ACTIVE 	= 0x0004
TRIG0_LATE 	= 0x0002
TRIG0_ACTIVE 	= 0x0001
PTP_RATEL = 0x418  # IEEE 1588 Rate Low Register
PTP_RATEH = 0x419  # IEEE 1588 Rate High Register
PTP_RDCKSUM = 0x41A  # Page 4 read checksum register
PTP_WRCKSUM = 0x41B  # Page 4 write checksum register
PTP_TXTS = 0x41C  # IEEE 1588 Transmit Timestamp Register
PTP_RXTS = 0x41D  # IEEE 1588 Receive Timestamp Register
PTP_ESTS = 0x41E  # IEEE 1588 Event Status
EVNTS_MISSED_MASK = 0x0700
EVNTS_MISSED_SHFT = 0x8
EVNT_TS_LEN_MASK = 0x00C0
EVNT_TS_LEN_SHIFT = 0x6
EVNT_RF 	= 0x0020
EVNT_NUM_SHFT 	= 0x2	# Shift value for Event Number
EVNT_NUM_MASK 	= 0x001C	# Mask value for Event Number
MULT_EVNT 	= 0x0002
EVENT_DET 	= 0x0001
PTP_EDATA = 0x41F  # IEEE 1588 Event Data Register
E7_RISE 	= 0x8000	# Event 7 fall
E7_DET 		= 0x4000	# Event 7 rise
E6_RISE 	= 0x2000
E6_DET 		= 0x1000
E5_RISE 	= 0x0800
E5_DET 		= 0x0400
E4_RISE 	= 0x0200
E4_DET 		= 0x0100
E3_RISE 	= 0x0080
E3_DET 		= 0x0040
E2_RISE 	= 0x0020
E2_DET 		= 0x0010
E1_RISE 	= 0x0008
E1_DET 		= 0x0004
E0_RISE 	= 0x0002
E0_DET 		= 0x0001


# ---- Page 5 register space offsets ----
PTP_TRIG = 0x514  # IEEE 1588 Trigger Configuration Register
TRIG_PULSE 	= 0x8000	# Trigger Pulse enable (vs edge)
TRIG_PER 	= 0x4000	# Trigger Periodic enable (vs. single)
TRIG_IF_LATE 	= 0x2000	# Trigger if late enable	
TRIG_NOTIFY 	= 0x1000	# Trigger Notification enable
TRIG_GPIO12 	= 0x0C00	# Trigger GPIO Select encodings
TRIG_GPIO11 	= 0x0B00
TRIG_GPIO10 	= 0x0A00
TRIG_GPIO9 	= 0x0900
TRIG_GPIO8 	= 0x0800
TRIG_GPIO7 	= 0x0700
TRIG_GPIO6 	= 0x0600
TRIG_GPIO5 	= 0x0500
TRIG_GPIO4 	= 0x0400
TRIG_GPIO3 	= 0x0300
TRIG_GPIO2 	= 0x0200
TRIG_GPIO1 	= 0x0100
TRIG_TOGGLE 	= 0x0080	# Trigger Toggle Mode enable
TRIG7_CSEL 	= (7 << 1)	# Trigger config select encodings
TRIG6_CSEL 	= (6 << 1)
TRIG5_CSEL 	= (5 << 1)
TRIG4_CSEL 	= (4 << 1)
TRIG3_CSEL 	= (3 << 1)
TRIG2_CSEL 	= (2 << 1)
TRIG1_CSEL 	= (1 << 1)
TRIG0_CSEL 	= (0 << 1)
TRIG_WR 	= 0x0001	# Trigger configuration write, 0 = read
PTP_EVNT = 0x515  # IEEE 1588 Event Configuration Register
EVNT_RISE 	= 0x4000	# Capture event rise
EVNT_FALL 	= 0x2000	# Capture event fall
EVNT_SINGLE 	= 0x1000	# Enable single event detect
EVNT_GPIO 	= 0x8	# shift 8 bits
EVNT7_SEL 	= (7 << 1)	# Event Select encodings
EVNT6_SEL 	= (6 << 1)
EVNT5_SEL 	= (5 << 1)
EVNT4_SEL 	= (4 << 1)
EVNT3_SEL 	= (3 << 1)
EVNT2_SEL 	= (2 << 1)
EVNT1_SEL 	= (1 << 1)
EVNT0_SEL 	= (0 << 1)
EVNT_WR 	= 0x0001	# Event configuration write, 0 = read
PTP_TXCFG0 = 0x516  # PTP Transmit Config Register 0
SYNC_1STEP	 = 0x8000	# Enable One-Step operation for Sync messages
PTP_DR_INSERT	= 0x2000	# Enable Delay_Req TS insert in Delay_Resp
IP_DIRECT	= 0x1000	# Enable PTP direct in IP
IGNORE_2STEP	= 0x0800	# Allows One-step oper. to ignore 2-step flag
CRC_1STEP	 = 0x0400	# Allows One-step operation to ignore CRC errors
TX_FIX_CHK 	= 0x0200	# Enable IPv4 UDP Checksum fix for 1-Step
IP1588_EN 	= 0x0100	# Enable IANA assigned IP address detect
TX_L2_EN 	= 0x0080	# Enable TS of Layer 2 Ethernet PTP messages
TX_IPV6_EN 	= 0x0040	# Enable TS of IPv6 PTP messages
TX_IPV4_EN 	= 0x0020	# Enable TS of IPv4 PTP messages
TX_PTP_VER2 	= (2 << 1)	# Transmit PTP Version = 2
TX_PTP_VER1 	= (1 << 1)	# Transmit PTP Version = 0
TX_PTP_VER0 	= (0 << 1)	# Accept any PTP Version
TX_TS_EN 	= 0x0001	# Transmit Timestamp Enable
PTP_TXCFG1 = 0x517  # PTP Transmit Config Register 1
PTP_PKTSTS = 0x518  # PTP Packet-based Status Config Register
PSF_CFG0 = 0x518  # PTP Packet-based Status Config Register
MAC_ADD_SEL3	= 0x0C00	# Select Mac Src Addr = 00 00 00 00 00 00
MAC_ADD_SEL2	= 0x0800	# Select Mac Src Addr = Destination Address
MAC_ADD_SEL1	= 0x0400	# Select Mac Src Addr = 08 00 17 00 00 00
MAC_ADD_SEL0	= 0x0000	# Select Mac Src Addr = 08 00 17 0B 6B 0F
MAC_ADD_SEL_SHFT = 0x0B	# Select Mac Src Addr = 08 00 17 0B 6B 0F
MIN_PRE_SHFT	= 0x8	# Shift value for Minimum Preamble
PKT_ENDIAN	= 0x0080	# Packet-based status Endian control
PSF_ENDIAN	= 0x0080	# Packet-based status Endian control
PKT_IPV4	= 0x0040	# Enable IPv4 Packet-based status
PSF_IPV4	= 0x0040	# Enable IPv4 Packet-based status
PKT_PCF_RD	= 0x0020	# Enable Packet-based delivery of PCF Read Data
PSF_PCF_RD	= 0x0020	# Enable Packet-based delivery of PCF Read Data
PKT_STAT	= 0x0010	# Enable Packet-based delivery of Error Status
PKT_DRR_EN	= 0x0010	# Enable Packet-based delivery of Error Status
PKT_TXTS	= 0x0008	# Enable Packet-based delivery of TX Timestamp
PSF_TXTS_EN	= 0x0008	# Enable Packet-based delivery of TX Timestamp
PKT_RXTS	= 0x0004	# Enable Packet-based delivery of RX Timestamp
PSF_RXTS_EN	= 0x0004	# Enable Packet-based delivery of RX Timestamp
PKT_TRIG	= 0x0002	# Enable Packet-based delivery of Trigger Sts
PSF_TRIG_EN	= 0x0002	# Enable Packet-based delivery of Trigger Sts
PKT_EVNT	= 0x0001	# Enable Packet-based delivery of Event TS
PSF_EVNT_EN	= 0x0001	# Enable Packet-based delivery of Event TS
PTP_RXCFG0 = 0x519  # PTP Receive Config Register 0
DOMAIN_EN 	= 0x8000	# Enable Domain field checking
ALT_MAST_DIS 	= 0x4000	# Disable Timestamp if Alternate Master set
USER_IP_SEL 	= 0x2000	# Selects upper IP address for PTP_RXCFG2
USER_IP_EN 	= 0x1000	# Enable User-programmed IP address detect
RX_SLAVE	= 0x0800	# Disable Timestamp of Delay_Req (control = 1)
IP1588_EN2 	= 0x0400	# Enable IANA assigned IP address detect
IP1588_EN1 	= 0x0200	# Enable IANA assigned IP address detect
IP1588_EN0 	= 0x0100	# Enable IANA assigned IP address detect
RX_L2_EN 	= 0x0080	# Enable TS of Layer 2 Ethernet PTP messages
RX_IPV6_EN 	= 0x0040	# Enable TS of IPv6 PTP messages
RX_IPV4_EN 	= 0x0020	# Enable TS of IPv4 PTP messages
RX_PTP_VER2 	= (2 << 1)	# Receive PTP Version = 2
RX_PTP_VER1 	= (1 << 1)	# Receive PTP Version = 0
RX_PTP_VER0 	= (0 << 1)	# Accept any PTP Version
RX_TS_EN 	= 0x0001	# Receive Timestamp Enable
PTP_RXCFG1 = 0x51A  # PTP Receive Config Register 1
PTP_RXCFG2 = 0x51B  # PTP Receive Config Register 2
PTP_RXCFG3 = 0x51C  # PTP Receive Config Register 3
RX_MIN_IFG 	= 12	# shift 12 bits
RX_ACC_UDP 	= 0x0800	# Ignore UDP checksum errors
RX_ACC_CRC 	= 0x0400	# Ignore CRC errors
RXTS_APPEND 	= 0x0200	# Attach Timestamp to PTP message
RXTS_INSERT 	= 0x0100	# Insert Timestamp to PTP message
PTP_RXCFG4 = 0x51D  # PTP Receive Config Register 4
IPV4_UDP_MOD 	= 0x8000	# Modify UDP checksum extra bytes for IPV4
RXTS_SEC_EN 	= 0x4000	# If attaching Timestamp, enable seconds field
RXTS_SEC_LEN 	= 12	# shift 12 bits
RXTS_NS_OFF 	= 6	# shift 6 bits
RXTS_SEC_OFF 	= 0	# shift 0 bits
PTP_TRDL = 0x51E  # IEEE 1588 Temporary Rate Duration Low
PTP_TRDH = 0x51F  # IEEE 1588 Temparary Rate Duration Hi

# ---- Page 6 register space offsets ----
PTP_CLK_CTL = 0x614  # Output Clock Control
PTP_CLKOUT_EN 	= 0x8000	# Enable clock output
PTP_CLKOUT_SEL 	= 0x4000	# Select PGM or FCO for output clock control
PTP_CLKOUT_SPD 	= 0x2000	# Sets turbo mode for CLK2MAC
PTP_PKTSTS1 = 0x615  # PTP Packet-based Status Config Register 1
PTP_PKTSTS2 = 0x616  # PTP Packet-based Status Config Register 2 
PTP_PKTSTS3 = 0x617  # PTP Packet-based Status Config Register 3
PTP_PKTSTS4 = 0x618  # PTP Packet-based Status Config Register 4
PTP_SFDCFG  = 0x619  # PTP SFD Configuration Register
PTP_INTCTL  = 0x61A  # PTP SFD Configuration Register
PTP_CLKSRC  = 0x61B  # PTP Clock Source Configuration Register
PTP_CLKSRC_EXT	= 0x8000	# Use external PTP clock source
PTP_CLKSRC_DIV	= 0x4000	# Use divided-down PGM clock for PTP clock src.
PTP_ETR	= 0x61C  # PTP Ether Type field for Layer 2 packets
PTP_ETYPE = 0x61C  # PTP Ether Type field for Layer 2 packets
PTP_OFF	= 0x61D  # PTP Offset to PTP Header
PTP_GPIOMON = 0x61E	# PTP GPIO Monitor Register
PTP_RXHASH = 0x61F  # PTP Receive Hash Register
RX_HASH_EN	= 0x1000	# Enable source identification hash filter


# ---- FPGA Register Space Offsets ----
#### Global Registers 0x0000-0x001F
FPGA_CTRL_1 = 0x0002        # FPGA Control Register 1
FPGA_RESET      = 0x0040    # Global reset
FPGA_EVENT_CLR  = 0x0020    # Event Clear
PLL_CTRL_1  = 0x0003        # PLL Control Register 1
PLL_RESET       = 0x8000    # Reset PLL
VCO_R3_LF       = 0x0000    # Loopfilter resistor
VCO_C3_C4_LF    = 0x0A00    # Loopfilter capacitor
DIVIDER         = 0x000C    # Divide by 12 (300MHz / 12 = 25MHz)
PLL_CTRL_2  = 0x0004        # PLL Control Register 2
OSC_IN_FREQ     = 0x0C00    # 25MHz
VCO_DIV         = 0x0020    # VCO divider
VCO_R4_LF       = 0x0000    # Loopfilter resistor
PLL_CTRL_3  = 0x0005        # PLL Control Register 3
PLL_R           = 0x001A    # pll_r[11:0]
PLL_CTRL_4  = 0x0006        # PLL Control Register 4
PLL_N           = 0x028A    # pll_n[15:0]
FPGA_CTRL_2 = 0x0007        # FPGA Control Register 2
SLAVE_MUX       = 0x0004    # Default Connector 2
MASTER_MUX      = 0x0003    # Default Connector 4
FPGA_LED_STS = 0x0008       # LED status
FPGA_DIP_STS = 0x0009       # DIP status
FPGA_BTN_STS = 0x000A       # BUTTON status
FPGA_SPLY_STS= 0x000B       # Supply status
LMK_STATUS  = 0x000E        # LMK Status Register
EVENT_LMK_READY = 0x0002    # LMK Event Ready
LMK_READY       = 0x0001    # LMK Ready
#### Slave Registers 0x0020-0x003F
######   Read-only status 0x0020-0x002F
SLAVE_TX_BYTES_L= 0x0020    # MAC Tx Byte Count [15:0]
SLAVE_TX_BYTES_H= 0x0021    # MAC Tx Byte Count [31:16]
SLAVE_TX_PKT_CNT= 0x0022    # MAC Tx Packet Count
SLAVE_RX_BYTES_L= 0x0023    # MAC Rx Byte Count [15:0]
SLAVE_RX_BYTES_H= 0x0024    # MAC Rx Byte Count [31:16]
SLAVE_RX_PKT_CNT= 0x0025    # MAC Rx Packet Count
SLAVE_CRC_ERR   = 0x0026    # MAC Rx CRC Error Count
SLAVE_RX_MSD    = 0x0027    # MAC Rx Missed Packet Count
SLAVE_RUNT_CNT  = 0x0028    # MAC Rx Runt Packet Count
SLAVE_RX_ER_CNT = 0x0029    # MAC Rx Errored Packet Count
SLAVE_MAC_STS_1 = 0x002A    # MAC Status Register 1
MAC_IGNORE_CRC_ERR  = 0x2000# Accept CRC errored packets
MAC_PTP_FILTER_EN   = 0x1000# Discard non-PTP/NTP packets
MAC_RMII_MODE       = 0x0200# RMII Mode
MAC_SCMII_MODE      = 0x0100# SCMII Mode
MAC_CS_IGNORE       = 0x0008# Carrier Sense Ignore
MAC_FULL_DUP        = 0x0004# Full Duplex
MAC_SPEED_10        = 0x0002# 10Mb Mode
PHY_LINK_UP         = 0x0001# Link Up
######   Writeable Control 0x0030-0x003F
SLAVE_MAC_CTRL_1 = 0x0030   # MAC Control Register 1
MAC_CROSS_LOOP      = 0x0200# Loop other MAC Rx to Tx
MAC_MII_LOOP        = 0x0100# Loop local MAC Rx to Tx
SLAVE_MAC_CTRL_2 = 0x0031   # MAC Control Register 2
#### Master Registers 0x0040-0x005F
######   Read-only status 0x0040-0x004F
MASTER_TX_BYTES_L= 0x0040    # MAC Tx Byte Count [15:0]
MASTER_TX_BYTES_H= 0x0041    # MAC Tx Byte Count [31:16]
MASTER_TX_PKT_CNT= 0x0042    # MAC Tx Packet Count
MASTER_RX_BYTES_L= 0x0043    # MAC Rx Byte Count [15:0]
MASTER_RX_BYTES_H= 0x0044    # MAC Rx Byte Count [31:16]
MASTER_RX_PKT_CNT= 0x0045    # MAC Rx Packet Count
MASTER_CRC_ERR   = 0x0046    # MAC Rx CRC Error Count
MASTER_RX_MSD    = 0x0047    # MAC Rx Missed Packet Count
MASTER_RUNT_CNT  = 0x0048    # MAC Rx Runt Packet Count
MASTER_RX_ER_CNT = 0x0049    # MAC Rx Errored Packet Count
MASTER_MAC_STS_1 = 0x004A    # MAC Status Register 1
MAC_IGNORE_CRC_ERR  = 0x2000# Accept CRC errored packets
MAC_PTP_FILTER_EN   = 0x1000# Discard non-PTP/NTP packets
MAC_RMII_MODE       = 0x0200# RMII Mode
MAC_SCMII_MODE      = 0x0100# SCMII Mode
MAC_CS_IGNORE       = 0x0008# Carrier Sense Ignore
MAC_FULL_DUP        = 0x0004# Full Duplex
MAC_SPEED_10        = 0x0002# 10Mb Mode
PHY_LINK_UP         = 0x0001# Link Up
######   Writeable Control 0x0050-0x005F
MASTER_MAC_CTRL_1 = 0x0050   # MAC Control Register 1
MAC_CROSS_LOOP      = 0x0200# Loop other MAC Rx to Tx
MAC_MII_LOOP        = 0x0100# Loop local MAC Rx to Tx
MASTER_MAC_CTRL_2 = 0x0051   # MAC Control Register 2
