//****************************************************************************
// PTPTestApp.cpp
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file shows off basic PTP operations.
//
//****************************************************************************


// Prevent inclusion of winsock.h in windows.h will be added as part 
// epl.h by way of ptp stack includes.
#define _WINSOCKAPI_   
#include <windows.h>
#undef  _WINSOCKAPI_    // undo hack above.

#include <iostream>
#include <tchar.h>

#include <setupapi.h>
#include <cfgmgr32.h>
#include <devguid.h>
#include <regstr.h>
#include <math.h>

#include "epl.h"

//****************************************************************************
// Local Definitions and Prototypes
//****************************************************************************

#define MAX_BOARD       2
#define MAX_CONNECTOR   4
#define MAX_MDIO_ADDR   31  // Allow 0-30, 31 is broadcast PCF

void scanForDevices( EPL_ENUM_TYPE iType );
PEPL_PORT_HANDLE initDevice( OAI_DEV_HANDLE oaiDH, EPL_ENUM_TYPE iType );

void configurePTP( PEPL_PORT_HANDLE portHdl );
void startPTP(  PEPL_PORT_HANDLE portHdl );

// Prototypes for helper functions that are not important to the use of EPL
void printMsg( int msgType, char *msgString );
void displayBanner( void );
void displayUsage( char *pName );
NS_BOOL processArgs( int argc, char *argv[] );

//****************************************************************************
// Globals
//****************************************************************************

NS_UINT VerMajor = 1;       // Major Version number
NS_UINT	VerMinor = 90;      // Minor Version number
NS_UINT	VerBuild = 1;       // Build number

// Variables used in command line processing
NS_UINT nAddr  = 1;
NS_UINT nConn  = 3;
NS_UINT nBoard = 1;
NS_BOOL bFind   = FALSE;    // Set to TRUE to simply scan for devices
NS_BOOL bMaster = FALSE;    // Set to TRUE to force PTP master operations
NS_BOOL bVerbose = FALSE;   // Set to TRUE to display all messages;
NS_BOOL bPSF = TRUE;
NS_BOOL bSTSUpdate = TRUE;
NS_BOOL bGraph = FALSE;

NS_BOOL   bTimeUpdate = FALSE;
NS_UINT32 tLast;
NS_UINT32 tUpdateInterval = 1000;

// Variables used in operations EPL 
NS_BOOL bPCF = TRUE;        // PCF Usage default
NS_BOOL bReset = FALSE;     // Set to reset entire device

OAI_DEV_HANDLE_STRUCT   oaiDHStruct;
OAI_DEV_HANDLE          oaiDH = &oaiDHStruct;
PEPL_PORT_HANDLE        devPort = NULL;

struct RunTimeOpts rtOps;       // Structure for setup/control of stack

//****************************************************************************
int _tmain( int argc, _TCHAR* argv[] )
//
//  this is the main procedure called by the startup code.
//
//  Input:
//      argc/argv
//          Standard C arguments for command line parsing.
//
//  Returns:
//      Error code back to the operating system
//****************************************************************************
{

    // Display banner and process the command line, exit if there is an error
    if( !processArgs( argc, argv ) ) {
        return 1;
    }

    // Initialize the library
    if ( EPLInitialize() != NS_STATUS_SUCCESS ) {
        printf( "\nERROR: Call to EPLInitialize() failed\n" );
        return 1;
    }

    if( bFind ) {
        // User just wants to see what is out there
        scanForDevices( EPL_ENUM_DIRECT );
        return 0;
    }

    // Go setup access to device
    devPort = initDevice( oaiDH, EPL_ENUM_DIRECT );
    if( !devPort ) {
        printf( "\nERROR: Device not found\n" );
        return 1;
    }

    do {
        // Initialize PTP
        // Fills out the RunTimeOpts structure to configure the PTP stack
        configurePTP( devPort );

        // Start PTP 
        // NOTE: Normally this would be run in a separate thread to allow for
        //       a GUI to operate while the stack is doing its thing.
        startPTP( devPort );
    } while( bReset );

    // Shutdown
    EPLDeinitialize();

    return 0;
}  // _tmain( ... )

//****************************************************************************
PEPL_PORT_HANDLE
    initDevice( 
        OAI_DEV_HANDLE  oaiDH,
        EPL_ENUM_TYPE iType )
//
//  find and initialize a device
//
//  Input:
//      oaiDH
//          OAI_DEV_HANDLE to fill in if we find a device
//      iType
//          The interface enumeration type to look on
//
//  Returns:
//      OAI_DEV_HANDLE
//          The handle to the device that was found
//****************************************************************************
{
PEPL_DEV_HANDLE  devHandle = NULL;
PEPL_DEV_INFO    devInfo   = NULL;
PEPL_PORT_HANDLE portHandle = NULL;

    // Setup the basic parameters based on the type of interface
    // Zero out the oaiDevHandle structure for sanity
    memset( oaiDH, 0x00, sizeof( OAI_DEV_HANDLE_STRUCT ) );

    // Initialize structure for search
    oaiDH->board = nBoard;
    oaiDH->connector = nConn;
    oaiDH->address = nAddr;
    oaiDH->pcfDefault = bPCF;
    
    // Find device and initialize de
    printf( "\nInitializing device on board %d connector %d at address %d\n", 
        oaiDH->board+1,
        oaiDH->connector+1, 
        oaiDH->address );

    devHandle = EPLEnumDevice( oaiDH, oaiDH->address, iType );
    if ( devHandle ){   // Did we get something back?

        // Got a device, find out more
        devInfo = EPLGetDeviceInfo( devHandle );

        if( devInfo ){  // Did we get valid info back?
            // Got info parse it out and run the tests
            if( devInfo->numOfPorts == 0 ) {
                printf( "ERROR: No ports on device\n" );
                return NULL;
            }  // if( devInfo->numOfPorts == NULL )

            // Obtain handle to 1st port
            // If device actually had mulitple ports we could walk through
            // each of them
            portHandle = EPLEnumPort( devHandle, 0 );
            if ( portHandle == NULL ) {
                printf( "ERROR: EPLEnumPort() returned NULL port handle\n" );
            }
            return portHandle;

        }  // if( devInfo )
    }  // if( defHandle )

    // If we got here we didn't find anything so portHandle should still be NULL
    return portHandle;
} // initDevice(...)

//****************************************************************************
void
    scanForDevices( 
        EPL_ENUM_TYPE iType )
//
//  Walk through boards, connectors, and addresses to see what boards are there
//
//  Input:
//      Nothing
//
//  Returns:
//      Nothing
//****************************************************************************
{
OAI_DEV_HANDLE_STRUCT   oDHS;
OAI_DEV_HANDLE          oaiDH = &oDHS;
PEPL_PORT_HANDLE        portHandle;
PEPL_DEV_HANDLE  devHandle = NULL;
PEPL_DEV_INFO    devInfo   = NULL;
NS_UINT          nBrd;
NS_UINT          nConn;
NS_UINT          nMDIO;
NS_BOOL          devFound;


    printf( "\n\nScanning for devices (ESC to abort)...\n\n" );
    for( nBrd=0; nBrd < MAX_BOARD; nBrd++ ) {
        devFound = FALSE;
        for( nConn=0; nConn < MAX_CONNECTOR; nConn++ ) {
            for( nMDIO=0; nMDIO < MAX_MDIO_ADDR; nMDIO++ ) {

                printf( "\r%02d/%02d/%02d   \r", nBrd+1, nConn+1, nMDIO );

                // zero out the oaiDevHandle structure for sanity
                memset( oaiDH, 0x00, sizeof( OAI_DEV_HANDLE_STRUCT ) );

                // Initialize structure for search
                oaiDH->pcfDefault = bPCF;
                oaiDH->board = nBrd;
                oaiDH->connector = nConn;

                // Go out and look for devices using the current enumeration type
                devHandle = EPLEnumDevice( oaiDH, nMDIO, iType );
                if ( devHandle ){   // Did we get something back?

                    // Got a device, find out more
                    devInfo = EPLGetDeviceInfo( devHandle );

                    if( devInfo ){  // Did we get valid info back?
                        // Got info parse it out and run the tests
                        if( devInfo->numOfPorts == 0 ) {
                            printf( "ERROR: No ports on device b:%d c:%d a:%d\n", nBrd+1, nConn+1, nMDIO );
                            continue;
                        }  // if( devInfo->numOfPorts == NULL )

                        // Obtain handle to 1st port
                        // If device actually had mulitple ports we could walk through
                        // each of them
                        portHandle = EPLEnumPort( devHandle, 0);
                        if ( portHandle == NULL) {
                            printf( "ERROR: EPLEnumPort() returned NULL port handle b:%d c:%d a:%d\n", nBrd+1, nConn+1, nMDIO );
                        }
                        else {
                            printf( "Device found on board %d connector %d at address %d\n", nBrd+1, nConn+1, nMDIO );
                            devFound = TRUE;
                        }
                    }  // if( devInfo )
                }  // if( defHandle )
                if( _kbhit() ) {
                    if( _getch() == 0x1B ) {
                        printf( "              \nScan Aborted!\n\n" );
                        return;
                    }
                }
            } // for( nMDIO... )
        } // for( nConn... )

        if( !devFound ) {
            // Didn't find anything on that board so assume there are no more boards
            // May not be true if there are other OK boards attached that aren't ALP boards
            break;
        }
    } // for( nBrd )

    printf( "              \nScan Complete!\n\n" );
    return;
} // scanForDevices(...)



//****************************************************************************
//****************************************************************************
// PTP Functions
//****************************************************************************
//****************************************************************************

//****************************************************************************
void
    updateTime()
// Get and display the current time from the PHY
//****************************************************************************
{
NS_UINT32 timeSec;
NS_UINT32 timeNanoSec;

    PTPClockReadCurrent( devPort, &timeSec, &timeNanoSec );
    printf( "Local Time: %ds %dns \n", timeSec, timeNanoSec );

} // updateTime()

//****************************************************************************
void
    handleCommands()
// Handle commands from the user.  These is a cheesy way to process input
// from the user without having a real thread.  It relies on a constant
// stream of messages/events from the PTP stack to operate.  Shouldn't take
// too long here, just enough to do the job.
// 
//****************************************************************************
{
int ch;

    // See if user pressed ESC, if so kill the "thread"
    if( !_kbhit() ) {
        return;
    }

    ch = _getch();
    switch( ch ) {
    case 0x1B:  // ESC
        bReset = FALSE;
        PTPKillThread( devPort );
        break;

    case 'r':   // reset time to 0,0
        PTPClockSet( devPort, 0, 0 );
        break;

    case 'R':   // Reset entire clock and restart it
        bReset = TRUE;
        PTPKillThread( devPort );
        break;

    case 'v':
    case 'V':
        bVerbose = !bVerbose;
        break;

    case 't':
    case 'T':
        bTimeUpdate = !bTimeUpdate;
        break;

    case 'p':
    case 'P':
        bPSF = !bPSF;
        break;

    case 's':
    case 'S':
        bSTSUpdate = !bSTSUpdate;
        break;

    case 'g':
    case 'G':
        bGraph = !bGraph;
        break;



    default:
        // do nothing
        break;
    }

    return;
}  // handleCommands()

//****************************************************************************
void 
    ptpStatusUpdate( 
        NS_UINT8 stsType, 
        void *stsData )
// Status Message from stack
// Input:
//      Various Time values from stack - Would like to change this to 
//      a simple structure.
// Returns:
//      Nothing
//****************************************************************************
{
    // NOTE/WARNING:
    // This procedure shouldn't do too much work unless it is in a separate
    // If the environment allows, it should only store the event and get out
    // If it takes too long it can cause the PTP stack to miss events and
    // will prevent it from achieving optimal synchronization.
    switch( stsType ) {
    case STS_PSF_DATA:
        {
        PHYMSG_MESSAGE_TYPE_ENUM msgType;
        PHYMSG_MESSAGE phyMsg;
        NS_UINT8 *nxtMsg;
            // Normally we'd call IsPhyStatusFrame() using a raw packet but 
            // since we got here we already know that the data is the 1st
            // of potentially several PSFs so we just process it.
            nxtMsg = (NS_UINT8 *)stsData;
            while( nxtMsg ) {
                nxtMsg = GetNextPhyMessage( devPort, nxtMsg, &msgType, &phyMsg );
                if( !nxtMsg || !bPSF ) {
                    continue;
                }
                switch( msgType ) {
                case PHYMSG_STATUS_TX:
                    printf( "PHYMSG_STATUS_TX:    %ds %dns  %d\n",
                                phyMsg.TxStatus.txTimestampSecs, 
                                phyMsg.TxStatus.txTimestampNanoSecs,
                                phyMsg.TxStatus.txOverflowCount );
                    break;
                case PHYMSG_STATUS_RX:
                    printf( "PHYMSG_STATUS_RX:    %ds %dns  %d   #%d   %d  %d\n", 
                                phyMsg.RxStatus.rxTimestampSecs, 
                                phyMsg.RxStatus.rxTimestampNanoSecs,
                                phyMsg.RxStatus.rxOverflowCount,
                                phyMsg.RxStatus.sequenceId,
                                phyMsg.RxStatus.messageType, 
                                phyMsg.RxStatus.sourceHash );
                    break;
                case PHYMSG_STATUS_TRIGGER:
                    printf( "PHYMSG_STATUS_TRIGGER: %d\n", phyMsg.TriggerStatus.triggerStatus );
                    break;
                case PHYMSG_STATUS_EVENT:
                    printf( "PHYMSG_STATUS_EVENT: \n" );
                    break;
                case PHYMSG_STATUS_ERROR:
                    printf( "PHYMSG_STATUS_ERROR: \n" );
                    break;
                case PHYMSG_STATUS_REG_READ:
                    // Should never get this, but just in case!
                    printf( "PHYMSG_STATUS_REG_READ: \n" );
                    break;
                default:
                    printf( "Unknown type of PSF %04X\n", msgType );
                    break;
                }
            }  // while( nxtMsg )
        }
        break;

    case STS_OFFSET_DATA: 
        {
        STS_OFFSET_DATA_STRUCT *stsODS = (STS_OFFSET_DATA_STRUCT *)stsData;
            if( bSTSUpdate ) {
                printf( "ptpStatusUpdate %d.%d  %d.%d  %d.%d  %d.%d\n", 
                        stsODS->offset_from_master.seconds,
                        stsODS->offset_from_master.nanoseconds,
                        stsODS->master_to_slave_delay.seconds,
                        stsODS->master_to_slave_delay.nanoseconds,
                        stsODS->slave_to_master_delay.seconds,
                        stsODS->slave_to_master_delay.nanoseconds,
                        stsODS->oneWayAvg.seconds,
                        stsODS->oneWayAvg.nanoseconds );
            }
        }
        break;
    default:
        break;
    } // switch( stsType )

    // Break out to another handler to see what the user wants to do
    handleCommands();

    return;
}

//****************************************************************************
void 
    printMsg( 
        int  msgType, 
        char *msgString )
// Display message from stack
// Input:
//      msgType - Type of message provided
//          0 - Debug Message (verbose)
//          1 - Debug Message (normal)
//          2 - Nofication Message
//          3 - Error Message
// Returns:
//      Nothing
//****************************************************************************
{
    // NOTE/WARNING:
    // This procedure shouldn't do too much work unless it is in a separate
    // If the environment allows, it should only store the event and get out
    // If it takes too long it can cause the PTP stack to miss events and
    // will prevent it from achieving optimal synchronization.
    if( bVerbose ) {
        switch( msgType ) {
        case 0:
        case 1:
        case 2:
        case 3:
        default:
            printf( "[%d] %s", msgType, msgString );
            break;
        }
    } // if( bVerbose )

    // Break out to another handler to see what the user wants to do
    handleCommands();

    // NOTE/WARNING: 
    // This is just on the edge of sanity for a non-threaded environment
    // if the update time option is used it should be used with a fairly
    // high interval to allow the stack time to operate.  This is 
    // especially true for the slave side.
    if( bTimeUpdate && (GetTickCount()-tLast) > tUpdateInterval ) {
        bTimeUpdate = FALSE;    // Avoid recursive calling
        updateTime();
        tLast = GetTickCount();
        bTimeUpdate = TRUE;    // Avoid recursive calling
    }

    return;
} // printMsg(...)


//****************************************************************************
//****************************************************************************
// PTP Functions
//****************************************************************************
//****************************************************************************

//****************************************************************************
void
    configurePTP(
        PEPL_PORT_HANDLE portHdl )
// Configure the stack for operation
//
// Input:
//      portHdl
//          pointer to port object to setup and used
//
// Returns:
//      Nothing
//
//****************************************************************************
{
EPL_LINK_STS linkSTS;
NS_UINT tmp;
NS_UINT8 dstMACAddr[6] = { 0x10, 0x00, 0x5E, 0x00, 0x01, 0x81 }; 
NS_UINT8 lclMACAddr[6] = { 0x08, 0x00, 0x17, 0x00, 0x00, 0x01 };
NS_UINT8 srcIP[4] = { 100, 100, 100, 8 };


    printf( "\nInitializing PTP %s...\n\n", ( bMaster ? "MASTER" : "SLAVE" ) );

    EPLGetLinkStatus( portHdl, &linkSTS );

    // Initialize RunTimeOpts structure to meaningful values
    // TODO: Should pull this from a config file...
    if( bMaster ) {
        // Master Specific items
        rtOps.forceBMCFlag = TRUE;
        rtOps.useOneStepFlag = TRUE;
        //rtOps.useOneStepFlag = FALSE;
    }
    else {
        //rtOps.useOneStepFlag = TRUE;
        rtOps.useOneStepFlag = FALSE;

        // Slave Specific items
        rtOps.useTempRateFlag = TRUE;
        rtOps.tempRateLength = 10000;
        rtOps.syncEthMode = FALSE;

        rtOps.limiterEnable = TRUE;
        rtOps.limiterThresh = 150;
        rtOps.limiterThreshMax = 250;
        rtOps.limiterGoodThresh = 100;
        rtOps.limiterLimitMultiplier = 25;

        rtOps.syncAdjustValue.seconds = 0;
        rtOps.syncAdjustValue.nanoseconds = 0;
        rtOps.delayReqAdjustValue.seconds = 0;
        rtOps.delayReqAdjustValue.nanoseconds = 0;

        rtOps.numRateSamples = 4;
        if( rtOps.numRateSamples > 64 ) rtOps.numRateSamples = 64;  
        if( rtOps.numRateSamples <  2 ) rtOps.numRateSamples = 2;

        rtOps.numRateAvgs = 2;
        if( rtOps.numRateAvgs > 64 ) rtOps.numRateAvgs = 64;
        if( rtOps.numRateAvgs <  2 ) rtOps.numRateAvgs = 2;

        rtOps.numOneWayAvgSamples = 8;
        if( rtOps.numOneWayAvgSamples > 64 ) rtOps.numOneWayAvgSamples = 64;
        if( rtOps.numOneWayAvgSamples <  2 ) rtOps.numOneWayAvgSamples = 2;

        // Setup synchronous ethernet mode
        // write port to turn on/off based on link status
        // Only works at 100Mb
        if( linkSTS.speed != 100 ) {
            rtOps.syncEthMode = FALSE;
        }
        tmp = EPLReadReg( portHdl, PHY_PG0_PHYCR2 );
        if( rtOps.syncEthMode )
            tmp |= PHYCR2_SYNC_ENET_EN;
        else
            tmp &= ~PHYCR2_SYNC_ENET_EN;
        EPLWriteReg( portHdl, PHY_PG0_PHYCR2, tmp );
    }

    SetDuplex( portHdl, FALSE );

    // Bug fix for A1 where PTP clock gets reset to 0 on link loss
    tmp = EPLReadReg( portHdl, PHY_IDR2 );
    if( tmp == 0x5CE0 && linkSTS.speed == 100 ) {
        EPLWriteReg( portHdl, 0x1E, 0x803F );
        EPLWriteReg( portHdl, 0x1E, 0x803F );
    }

    // Always disable loopbak for 10Mb - doesn't affect other modes
    tmp = EPLReadReg( portHdl, PHY_10BTSCR );
    tmp |= P848_10BTSCR_LP_10_DIS;
    EPLWriteReg( portHdl, PHY_10BTSCR, tmp );

    rtOps.syncInterval = 250;

    if( !bMaster ) {
        // Slave needs different MAC and IP addresses
        lclMACAddr[5] = 0x02;
        srcIP[3] = 0x7;
    } // if( !bMaster )

    memcpy( rtOps.localMACAddress, lclMACAddr, sizeof( lclMACAddr ) );
    memcpy( rtOps.srcIPAddress, srcIP, sizeof( srcIP ) );

    rtOps.udpChksumEnable = TRUE;

    rtOps.phaseAlignClkoutFlag = TRUE;

    rtOps.clkOutEnableFlag = TRUE;
    rtOps.clkOutDivide = 25;
    rtOps.clkOutSpeed = FALSE;
    rtOps.clkOutSource = 0;

    rtOps.ppsEnableFlag = TRUE;
    rtOps.ppsStartTime = 5;
    rtOps.ppsRiseOrFallFlag = 0;
    rtOps.ppsGpio = 1;

    memcpy(rtOps.subdomainName, DEFAULT_PTP_DOMAIN_NAME, PTP_SUBDOMAIN_NAME_LENGTH);
    memcpy(rtOps.clockIdentifier, IDENTIFIER_DFLT, PTP_CODE_STRING_LENGTH);
    rtOps.clockVariance = DEFAULT_CLOCK_VARIANCE;
    rtOps.clockStratum = DEFAULT_CLOCK_STRATUM;

    memset( rtOps.directAddress, 0x00, sizeof(rtOps.directAddress) ); 

    rtOps.inboundLatency.seconds = 0;
    rtOps.inboundLatency.nanoseconds = DEFAULT_INBOUND_LATENCY;
    rtOps.outboundLatency.seconds = 0;
    rtOps.outboundLatency.nanoseconds = DEFAULT_OUTBOUND_LATENCY;

    rtOps.max_foreign_records = DEFUALT_MAX_FOREIGN_RECORDS;
    rtOps.currentUtcOffset = DEFAULT_UTC_OFFSET;
    rtOps.displayStats = FALSE;

    rtOps.slaveOnly = !bMaster;

    rtOps.eplPortHandle = portHdl;
    rtOps.oaiHandle = portHdl->oaiDevHandle;

    return;
}  // configurePTP(...)


//****************************************************************************
void
    startPTP(
        PEPL_PORT_HANDLE portHdl )
// Start up the stack
//
// Input:
//      portHdl
//          pointer to port object to setup and used
//
// Returns:
//      Nothing
//
//****************************************************************************
{

    // Everything is initialized, start it up...
    PTPThreadC( portHdl, (void *)NULL, printMsg, ptpStatusUpdate, &rtOps );

    return;
}  // startPTP(...)


//****************************************************************************
//****************************************************************************
// Helper Functions - Not important to EPL usage
//****************************************************************************
//****************************************************************************

//****************************************************************************
void 
    displayBanner( 
        void)
//
//  Displays the banner for the program
//
//  Input:
//      Nothing
//
//  Returns:
//      Nothing
//****************************************************************************
{
    printf( "\n-------------------------------------------------------------------------------\n");
    printf(   "*** PTP Test Application v%d.%d  Build: %d\n", VerMajor, VerMinor, VerBuild);
    printf(   "-------------------------------------------------------------------------------\n");
    return;
}  // DisplayBanner( ... )


//****************************************************************************
void 
    displayUsage( 
        char * pName )
//
//  Displays the program usage
//
//  Input:
//      pName - Pointer to the name out of argv
//
//  Returns:
//      Nothing
//****************************************************************************
{
	char  *pOff;

	// Determine the current name of the program being run
	// Strip leading path and trailing extension from name
	for( pOff = pName; *pOff; pOff++ ) {
		switch( *pOff ) {
		case '\\':
			// We got a \ in the name, start from here so we will always
			// start from the last slash in the string.
			pName = pOff+1;
			break;
		case '.':
			// We got a . turn it into a NULL so string will end there
			// if it is the last . in the string.
			*pOff = '\0';
			break;
		default:
			break;
		}  // switch( ... )
	}  // for( ... )

    printf( "\n%s [ "
            " -H | -? "
            "| -V "
            "| -F "
            "| -MM "
            "| -MS "
            "| -D bb cc aa "
            "| -T[nnnnn] "

			"]\nCommands:\n"
			"  -H or -h or -?   Display this help\n"
            "  -V or -v         Verbose Mode where\n"
            "  -F or -f         Find all devices\n"         
            "  -MM or -mm       Mode Master (Default)\n"
            "  -MS or -ms       Mode Slave \n"
            "  -D bb cc aa      Device where:\n"
            "                      bb is the board number\n"
            "                      cc is the connector number\n"
            "                      aa is the address number\n"
            "  -T[nnnnn]        Update Time where nnnnn is the interval in ms. 1000 is default\n"
			, pName
	);

	return;
}  // DisplayUsage( ... )


//****************************************************************************
NS_BOOL 
    processArgs( 
        int argc, 
        char *argv[] )
//	processArgs
//	This procedure processes the command line for the program
//****************************************************************************
{
	NS_UINT8	CurArg;
    NS_BOOL     bHelp=FALSE;

	displayBanner();

	// Check all of the parameters that they specified
	for ( CurArg=1; (CurArg < argc) && !bHelp; CurArg++ ) {

		switch( *(argv[ CurArg ]) ) {
		case '-':
		case '/':

			// We have a proper switch, which one?
			switch( *(argv[ CurArg ]+1) ) {
			case 'H':
			case 'h':
			case '?':
				bHelp = TRUE;
				break;

			case 'F':
			case 'f':
				bFind = TRUE;
				break;

            case 'M':
			case 'm':
		        switch( *(argv[ CurArg ]+2) ) {
    			case 'S':
    			case 's':
                    bMaster = FALSE;
				    break;
    			case 'M':
    			case 'm':
				    bMaster = TRUE;
				    break;
                default:
                    break;
                }
                break;

            case 'D':
			case 'd':
                nBoard = ((NS_UINT)strtoul( (argv[ CurArg+1 ]), NULL, 0 ) - 1);
                nConn  = ((NS_UINT)strtoul( (argv[ CurArg+2 ]), NULL, 0 ) - 1);
                nAddr  = ((NS_UINT)strtoul( (argv[ CurArg+3 ]), NULL, 0 ));
                break;

            case 'B':
			case 'b':
				nBoard = ((NS_UINT)strtoul( (argv[ CurArg ]+2), NULL, 0 ) - 1);
				break;

			case 'C':
			case 'c':
				nConn = ((NS_UINT)strtoul( (argv[ CurArg ]+2), NULL, 0 ) - 1);
				break;

			case 'A':
			case 'a':
				nAddr = ((NS_UINT)strtoul( (argv[ CurArg ]+2), NULL, 0 ));
				break;

            case 'V':
            case 'v':
                bVerbose = TRUE;
                break;

            case 'T':
			case 't':
                bTimeUpdate = TRUE;
                if( (argv[ CurArg ]+2) ) {
				    tUpdateInterval = ((NS_UINT)strtoul( (argv[ CurArg ]+2), NULL, 0 ) );
                    if( tUpdateInterval > 500 ) {
                        tUpdateInterval -= 500;
                    }
                }
				break;

            default:
				break;
			}  // switch()
			break;
		case '?':
			bHelp = TRUE;
            break;
		default:
			break;
		}  // switch()
	}  // for ( each argument )

	if ( bHelp ) {
		displayUsage( argv[0] );
		return FALSE;
	}  // if( bHelp )

	return TRUE;
}  // processArgs(...)

//****************************************************************************
// End of program
//****************************************************************************
