//****************************************************************************
// EPLTestApp.cpp
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file shows off basic EPL operations.
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
// Local Prototypes
//****************************************************************************

#define MAX_BOARD       2
#define MAX_CONNECTOR   4
#define MAX_MDIO_ADDR   31  // Allow 0-30, 31 is broadcast PCF

void RunTests( PEPL_DEV_HANDLE devHandle);
void DecodeMiiCfg(EPL_MIICFG_ENUM miiCfg);
void DisplayLinkStatus( EPL_LINK_STS *linkSts);
void DisplayLinkQualityGetInfo( PEPL_PORT_HANDLE portHandle);

// Prototypes for helper functions that are not important to the use of EPL
void displayBanner( void );
void displayUsage( char *pName );
NS_BOOL processArgs( int argc, char *argv[] );

//****************************************************************************
// Globals
//****************************************************************************

NS_UINT VerMajor=1;     // Major Version number
NS_UINT	VerMinor=90;     // Minor Version number
NS_UINT	VerBuild=1;     // Build number

// Variables used in command line processing
NS_UINT nMDIOAddr   = 0;
NS_UINT nConnector  = 0;
NS_UINT nBoard      = 0;

NS_BOOL bScanOnly = FALSE;  // Set to TRUE to just scan for devices
NS_BOOL bFind    = TRUE;    // Set to TRUE to simply scan for devices
NS_BOOL bVerbose = FALSE;   // Set to TRUE to display all messages;

// bPCF - Set to TRUE if you want to use PCF/PSFs
// NOTE: If you set this to true, a limited number of tests will be run
//       Tests that disable communications through MII interface can
//       not be run because we lose connection and can't continue.
//       See SDG for additional details of those tests.
//NS_BOOL bPCF = TRUE;
NS_BOOL bPCF = FALSE;


//****************************************************************************
int _tmain( int argc, _TCHAR* argv[])
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
    NS_STATUS               nsResult;

    PEPL_DEV_HANDLE         devHandle = NULL;
    PEPL_DEV_INFO           devInfo   = NULL;
    PEPL_PORT_HANDLE        devPort   = NULL;

    OAI_DEV_HANDLE_STRUCT   oaiDevHandleStruct[MAX_CONNECTOR];  // 1 for each connector 
    OAI_DEV_HANDLE          oaiDH = &oaiDevHandleStruct[0];

    NS_UINT                 nBrd;
    NS_UINT                 nMDIO;
    NS_UINT                 nConn;
    NS_BOOL                 devFound;

    EPL_ENUM_TYPE           iType = EPL_ENUM_DIRECT;          // force DIRECT

    // Display banner and process the command line, exit if there is an error
    if( !processArgs( argc, argv ) ) {
        return 1;
    }

    // Initialize the library
    nsResult = EPLInitialize();
    if ( nsResult != NS_STATUS_SUCCESS) {
        printf( "ERROR: Call to EPLInitialize() failed\n");
        return 0;
    }

    if( bScanOnly || bFind ) {
        printf( "\n\nScanning for devices (ESC to abort)...\n\n" );
    }
    else {
        printf( "\n\n" );
    }

    for( nBrd=nBoard; nBrd < MAX_BOARD; nBrd++ ) {
        devFound = FALSE;
        for( nConn=nConnector; nConn < MAX_CONNECTOR; nConn++ ) {
            for( nMDIO=nMDIOAddr; nMDIO < MAX_MDIO_ADDR; nMDIO++ ) {

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
                        devPort = EPLEnumPort( devHandle, 0);
                        if ( devPort == NULL) {
                            printf( "ERROR: EPLEnumPort() returned NULL port handle b:%d c:%d a:%d\n", nBrd+1, nConn+1, nMDIO );
                        }
                        else {
                            devFound = TRUE;
                            printf(   "===============================================================================");
                            printf( "\nPHY Device found on board %d connector %d at address %d", nBrd+1, nConn+1, nMDIO );
                            printf( "\n===============================================================================");

                            if( !bScanOnly ) {
                                printf( "\nRunning Tests...\n" );
                                RunTests( devHandle );
                            }
                            printf( "\n\n" );

                            if( !bFind ) {
                                // Only testing a single device, bail out now.
                                EPLDeinitialize();
                                return 0;
                            }

                            // Move onto next device
                            nMDIO += devInfo->numOfPorts;
                        }
                    }  // if( devInfo )
                }  // if( defHandle )
                if( _kbhit() ) {
                    if( _getch() == 0x1B ) {
                        printf( "              \nScan Aborted!\n\n" );
                        EPLDeinitialize();
                        return 0;
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

    EPLDeinitialize();
    return 0;
}  // _tmain( ... )

//****************************************************************************
void RunTests( PEPL_DEV_HANDLE devHandle)
//
//  Get, parse, and display information for the device
//
//  Input:
//      devHandle - Handle for the device we want to look at
//
//  Returns:
//      Nothing
//****************************************************************************
{
    PEPL_DEV_INFO devInfo;
    PEPL_PORT_HANDLE portHandle;
    EPL_LINK_STS linkSts;
    EPL_LINK_CFG linkCfg;
    NS_BOOL bistActiveFlag;
    NS_UINT x, errNibbles;
    NS_STATUS ccode;
    NS_UINT cableLength, varianceValue;
    NS_SINT freqOffsetValue, freqControlValue;

    NS_UINT nEndTime;

    printf( "\nDevice Information:\n");
    devInfo = EPLGetDeviceInfo( devHandle);

    printf( "  Device has %d individual port(s)\n", devInfo->numOfPorts);
    printf( "  Model: %d\n", devInfo->deviceModelNum);
    printf( "  Revision: %d\n", devInfo->deviceRevision);
    printf( "  Device has %d extended register pages\n", devInfo->numExtRegisterPages);

    printf( "\nDevice Capabilities:\n");
    printf( "  Device %s capable of TDR functionality.\n",
                (EPLIsDeviceCapable( devHandle, EPL_CAPA_TDR) ? "IS" : "is NOT" ));

    printf( "  Device %s capable of Link Quality functionality.\n",
                (EPLIsDeviceCapable( devHandle, EPL_CAPA_LINK_QUALITY) ? "IS" : "is NOT" ));

    printf( "  Device %s capable of MII Port Configuration functionality.\n",
                (EPLIsDeviceCapable( devHandle, EPL_CAPA_MII_PORT_CFG) ? "IS" : "is NOT" ));

    // MII configuration tests.
    if ( EPLIsDeviceCapable( devHandle, EPL_CAPA_MII_PORT_CFG))
    {
        printf( "\nInitial MII Device Confieguration:\n");
        EPL_MIICFG_ENUM miiCfg = EPLGetMiiConfig( devHandle);
        DecodeMiiCfg( miiCfg);

        printf( "\nConfiguring MII device port configuration to MIIPCFG_PORT_SWAP\n");
        EPLSetMiiConfig( devHandle, MIIPCFG_PORT_SWAP);
        miiCfg = EPLGetMiiConfig( devHandle);
        DecodeMiiCfg( miiCfg);

        printf( "\nConfiguring MII device port configuration to MIIPCFG_NORMAL\n");
        EPLSetMiiConfig( devHandle, MIIPCFG_NORMAL);
        miiCfg = EPLGetMiiConfig( devHandle);
        DecodeMiiCfg( miiCfg);
    }

    // Walk through each of the ports and run additional tests
    for ( x = 0; x < devInfo->numOfPorts; x++)
    {
        printf( "\n-------------------------------------------------------------------------------");
        printf( "\nRUNNING ALL TESTS ON PORT %d", x);
        printf( "\n-------------------------------------------------------------------------------\n");

        portHandle = EPLEnumPort( devHandle, x);
        if ( portHandle == NULL) {
            printf( "ERROR: EPLEnumPort() returned NULL port hanndle\n");
            exit(1);
        }

        printf( "\nPort MDIO address = %d\n", EPLGetPortMdioAddress( portHandle));        
        printf( "Device Handle at address %08p\n", EPLGetDeviceHandle( portHandle));

        if( !bPCF ) {
            // Reset to start fresh.   See note about bPCF above
            printf( "\nDevice Reset Tests\n");
            printf( "  Resetting device...\n");        
            EPLResetDevice( devHandle );
            printf( "  Reset finished\n");
            Sleep( 3000 );
        }

        printf( "\nEPLIsLinkUp:\n");
        if ( EPLIsLinkUp( portHandle)) 
            printf( "  Link is UP\n");
        else
            printf( "  Link is DOWN\n");

        printf( "\nEPLGetLinkStatus:\n");
        EPLGetLinkStatus( portHandle, &linkSts);
        DisplayLinkStatus( &linkSts );

        linkCfg.autoNegEnable = FALSE;
        linkCfg.speed = 10;
        linkCfg.duplex = FALSE;
        linkCfg.pause = TRUE;
        linkCfg.autoMdix = MDIX_AUTO;
        linkCfg.energyDetect = FALSE;
        printf( "\nSetting link to 10Mbps, half duplex ....\n");
        EPLSetLinkConfig( portHandle, &linkCfg);
        Sleep( 3000);

        EPLGetLinkStatus( portHandle, &linkSts);
        DisplayLinkStatus( &linkSts );

        printf( "\nRestarting auto-negotiation:\n");
        EPLRestartAutoNeg( portHandle);
        EPLGetLinkStatus( portHandle, &linkSts);
        if ( linkSts.autoNegCompleted) 
        printf( "  Auto-neg has COMPLETED\n");
        else 
        printf( "  Auto-neg has NOT completed\n");

        if( bPCF ) {
            printf( "\nBIST Tests:\n");
            EPLBistGetStatus( portHandle, &bistActiveFlag, &errNibbles);
            if ( bistActiveFlag) printf( "    BIST is ACTIVE, Error Nibbles Count %d\n", errNibbles);
            else printf( "    BIST is NOT ACTIVE, Error Nibbles Count %d\n", errNibbles);
        }
        else {
            // Running these tests effectively result in disabling 
            // communications with the parts MII interface so if you 
            // are using PHY Control and Status Frames you shouldn't
            // call these.  See the SDG for additional information
            // about the calls.
            printf( "\nBIST Tests:\n");
            printf( "  Enabling loopback mode\n");
            EPLSetLoopbackMode( portHandle, TRUE);

            EPLBistGetStatus( portHandle, &bistActiveFlag, &errNibbles);
            if ( bistActiveFlag) printf( "    BIST is ACTIVE, Error Nibbles Count %d\n", errNibbles);
            else printf( "    BIST is NOT ACTIVE, Error Nibbles Count %d\n", errNibbles);

            printf( "  Starting Transmit BIST\n");
            EPLBistStartTxTest( portHandle, TRUE);

            EPLBistGetStatus( portHandle, &bistActiveFlag, &errNibbles);
            if ( bistActiveFlag) printf( "    BIST is ACTIVE, Error Nibbles Count %d\n", errNibbles);
            else printf( "    BIST is NOT ACTIVE, Error Nibbles Count %d\n", errNibbles);

            printf( "  Stopping Transmit BIST\n");
            EPLBistStopTxTest( portHandle);

            printf( "  Disabling loopback mode\n");
            EPLSetLoopbackMode( portHandle, FALSE);

            printf( "\nPort Power Tests\n");
            printf( "  Powering DOWN port\n");
            EPLSetPortPowerMode( portHandle, FALSE);
            Sleep( 2000);
            printf( "  Powering UP port\n");
            EPLSetPortPowerMode( portHandle, TRUE);
            Sleep( 2000);
        }

        // DSP link quality stuff
        if ( EPLIsDeviceCapable( devHandle, EPL_CAPA_LINK_QUALITY))
        {
            linkCfg.autoNegEnable = TRUE;
            linkCfg.speed = 100;
            linkCfg.duplex = TRUE;
            linkCfg.pause = TRUE;
            linkCfg.autoMdix = MDIX_AUTO;
            linkCfg.energyDetect = FALSE;
            printf( "\nRestoring link to 100Mbps, full duplex ....\n");
            EPLSetLinkConfig( portHandle, &linkCfg);
            Sleep( 3000);

            printf( "\nLink Quality Tests\n");
            for ( NS_UINT x = 2; x < 10; x += 2)
            {
                printf( "\n  Attempting to obtain DSP cable quality info, sample time %d ms\n", x);
                ccode = EPLGetCableStatus( portHandle, x, &cableLength,
                &freqOffsetValue, &freqControlValue,
                &varianceValue);
                if ( ccode != NS_STATUS_SUCCESS) {
                    printf( "  Could not get DSP cable status info because link is NOT established or NOT at 100Mbps\n");
                    break;
                }
                else {
                    printf( "    Jitter in PPM = %d\n", abs((int)((freqControlValue * 5.1562) - (freqOffsetValue * 5.1562))));
                    printf( "    Cable length  = %dm\n", cableLength);
                                    double varData = (288.0 * ((1024*1024*x) / 8.0)) / varianceValue;
                                    double rxSNR = 10.0 * log10( varData);
                    printf( "    SNR %.2f db\n", rxSNR);
                }
            }

            DisplayLinkQualityGetInfo( portHandle);

            // Enable link quality monitoring.
            printf( "\nLink Quality Monitoring:\n");
            printf( "  Enabling Link Quality Monitoring and Setting New Thresholds\n");
            DSP_LINK_QUALITY_SET lqs = { TRUE, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
            EPLDspSetLinkQualityConfig( portHandle, &lqs);
            DisplayLinkQualityGetInfo( portHandle);

            // TDR functions
            printf( "\nTDR Tests:\n");

            printf( "  Disconnect cable from opposite end of link (leave cable attached to PHY under test)\n" );
            nEndTime = GetTickCount()+10000;
            while( (GetTickCount() < nEndTime) && !_kbhit() ) {
                if( !(GetTickCount() % 1000) ) {
                    printf( "\r  Press any key to continue or wait for timeout in %d seconds...", (nEndTime-GetTickCount())/1000 );
                }
            }
            printf( "\r                                                                                \r" );

            EPL_CABLE_STS_ENUM cableStatus;
            NS_UINT rawCableLength;
            char *cableStatusStrings[5] = {
                "Terminated",
                "Open",
                "Short",
                "Cross Shorted",
                "Unknown"
            };

            printf( "  Calling EPLGetTDRCableInfo() for Tx Channel\n");
            ccode = EPLGetTDRCableInfo( portHandle, TRUE, &cableStatus, &rawCableLength);
            if ( ccode != NS_STATUS_SUCCESS) {
                printf( "    ERROR: Call to EPLGetTDRCableInfo() FAILED\n");
            }
            else {
                printf( "    Tx Cable pair status is %s\n", cableStatusStrings[cableStatus] );
                if( cableStatus == CABLE_STS_TERMINATED ) {
                    printf( "    Tx Raw cable length = N/A, cable length = N/A\n" );
                }
                else {
                    printf( "    Tx Raw cable length = %d, cable length = %.2fm\n", 
                    rawCableLength, ((float)rawCableLength / TDR_CABLE_VELOCITY / 2) );
                }
            }

            printf( "\n  Calling EPLGetTDRCableInfo() for Rx Channel\n");
            ccode = EPLGetTDRCableInfo( portHandle, FALSE, &cableStatus, &rawCableLength);
            if ( ccode != NS_STATUS_SUCCESS)
                printf( "    ERROR: Call to EPLGetTDRCableInfo() FAILED\n");
            else
            {
                printf( "    Rx Cable pair status is %s\n", cableStatusStrings[cableStatus]);
                if( cableStatus == CABLE_STS_TERMINATED ) {
                    printf( "    Tx Raw cable length = N/A, cable length = N/A\n" );
                }
                else {
                    printf( "    Tx Raw cable length = %d, cable length = %.2fm\n", 
                    rawCableLength, ((float)rawCableLength / TDR_CABLE_VELOCITY / 2) );
                }
            }

            if( bVerbose ) {
                // Obtain a trace of the reflected pulse on the tx and rx channels.
                printf( "\nTDR Reflection Oscilloscope Tests:\n");

                NS_SINT8 *posPulseResults = (NS_SINT8*)malloc( 256);
                NS_SINT8 *negPulseResults = (NS_SINT8*)malloc( 256);
                if ( posPulseResults == NULL || negPulseResults == NULL)        {
                    printf( "  ERROR: Could NOT alloc memory for pulse oscilloscope data\n");
                    exit( 1);
                }

                printf( "  Obtaining TDR reflection oscilloscope traces...\n");

                printf( "\n  Tx Pulse Data Points (8ns):\n");
                EPLGetTDRPulseShape( portHandle, TRUE, FALSE, posPulseResults, negPulseResults);    // 100Mbps 8ns pulse
                for ( NS_UINT x = 0; x < 256; x++) {
                    if( posPulseResults[x] || negPulseResults[x] ) {
                        printf( "    Time %4d ns   pos = %4d  neg = %4d\n", x*8, posPulseResults[x], negPulseResults[x]);
                    }  // if( data != 0 )
                }  // for( ... )

                printf( "\n  Tx Pulse Data Points (50ns):\n");
                EPLGetTDRPulseShape( portHandle, TRUE, TRUE, posPulseResults, negPulseResults);     // 100Mbps 50ns pulse
                for ( NS_UINT x = 0; x < 256; x++) {
                    if( posPulseResults[x] ) {
                        printf( "    Time %4d ns   pos = %4d  neg =  N/A\n", x*8, posPulseResults[x] );
                    }  // if( data != 0 )
                }  // for( ... )

                printf( "\n  Rx Pulse Data Points (8ns):\n");
                EPLGetTDRPulseShape( portHandle, FALSE, FALSE, posPulseResults, negPulseResults);    // 100Mbps 8ns pulse
                for ( NS_UINT x = 0; x < 256; x++) {
                    if( posPulseResults[x] || negPulseResults[x] ) {
                        printf( "    Time %4d ns   pos = %4d  neg = %4d\n", x*8, posPulseResults[x], negPulseResults[x]);
                    }  // if( data != 0 )
                }  // for( ... )

                printf( "\n  Rx Pulse Data Points (50ns):\n");
                EPLGetTDRPulseShape( portHandle, FALSE, TRUE, posPulseResults, negPulseResults);     // 100Mbps 50ns pulse
                for ( NS_UINT x = 0; x < 256; x++) {
                    if( posPulseResults[x] ) {
                        printf( "    Time %4d ns   pos = %4d  neg =  N/A\n", x*8, posPulseResults[x] );
                    }  // if( data != 0 )
                }  // for( ... )

                free( posPulseResults);
                free( negPulseResults);
            }  // if( bVerbose )
            else {
                printf( "\nTDR Reflection Oscilloscope Tests NOT run (use -v)\n");
            }  // if( bVerbose )

        }  // if ( EPLIsDeviceCapable( devHandle, EPL_CAPA_LINK_QUALITY))

    }  // for ( x = 0; x < devInfo->numOfPorts; x++)

    return;
}	// RunTests(...)

//****************************************************************************
void DecodeMiiCfg( EPL_MIICFG_ENUM miiCfg)
//
//  Parse and display the MII configuration information
//
//  Input:
//      miiCfg - pointer to the MII Config info structure
//
//  Returns:
//      Nothing
//****************************************************************************
{
    switch ( miiCfg) {
    case MIIPCFG_UNKNOWN:
        printf( "  Unknown MII port configuration\n");
        break;
    case MIIPCFG_NORMAL:
        printf( "  Normal MII port configuration\n");
        break;
    case MIIPCFG_PORT_SWAP:
        printf( "  MII ports swapped configuration\n");
        break;
    case MIIPCFG_EXT_MEDIA_CONVERTER:
        printf( "  MII ports - extender media converter configuration\n");
        break;
    case MIIPCFG_BROADCAST_TX_PORT_A:
        printf( "  MII ports - broadcast Tx port A configuration\n");
        break;
    case MIIPCFG_BROADCAST_TX_PORT_B:
        printf( "  MII ports - broadcast Tx port B configuration\n");
        break;
    case MIIPCFG_MIRROR_RX_CHANNEL_A:
        printf( "  MII ports - mirror Rx channnel to port A configuration\n");
        break;
    case MIIPCFG_MIRROR_RX_CHANNEL_B:
        printf( "  MII ports - mirror Rx channnel to port B configuration\n");
        break;
    case MIIPCFG_DISABLE_PORT_A:
        printf( "  MII ports - port A disabled\n");
        break;
    case MIIPCFG_DISABLE_PORT_B:
        printf( "  MII ports - port B disabled\n");
        break;
    default:
        printf( "  ERROR: Unknown MII device configuration\n");
        break;
    }  // switch ( miiCfg) {

    return;
}  // DecodeMiiCfg(...)

//****************************************************************************
void DisplayLinkStatus( EPL_LINK_STS *linkSts)
//
//  Parse and display the link status information
//
//  Input:
//      linkSts - pointer to the link status info structure
//
//  Returns:
//      Nothing
//****************************************************************************
{
    if ( linkSts->linkup)
        printf( "  Link is UP\n");
    else
        printf( "  Link is DOWN\n");

    if ( linkSts->autoNegEnabled)
        printf( "  Auto-neg is ENABLED\n");
    else
        printf( "  Auto-neg is DISABLED\n");

    if ( linkSts->autoNegCompleted)
        printf( "  Auto-neg has COMPLETED\n");
    else
        printf( "  Auto-neg has NOT completed\n");

    if ( linkSts->speed==100)
        printf( "  Link speed is 100Mbps\n");
    else if ( linkSts->speed==10)
        printf( "  Link speed is 10Mbps\n");
    else
        printf( "  Link speed is INVALID\n");

    if ( linkSts->duplex) 
        printf( "  Link duplex is FULL\n");
    else 
        printf( "  Link duplex is HALF\n");

    if ( linkSts->mdixStatus) 
        printf( "  Wire pairs are swapped (crossed)\n");
    else 
        printf( "  Wire pairs are NOT swapped (crossed)\n");

    if ( linkSts->autoMdixEnabled) 
        printf( "  Auto-MDIX is ENABLED\n");
    else 
        printf( "  Auto-MDIX is NOT enabled\n");

    if ( linkSts->polarity) 
        printf( "  Inverted pair polarity WAS DETECTED\n");
    else 
        printf( "  Inverted pair polarity NOT detected\n");

    if ( linkSts->energyDetectPower) 
        printf( "  Energy detect power is ON\n");
    else 
        printf( "  Energy detect power is OFF\n");

    return;
}  // DisplayLinkStatus( ... )

//****************************************************************************
void DisplayLinkQualityGetInfo( PEPL_PORT_HANDLE portHandle)
//
//  Get, parse, and display the link quality information
//
//  Input:
//      portHandle - Handle for the port that we want to look at
//
//  Returns:
//      Nothing
//****************************************************************************
{
    DSP_LINK_QUALITY_GET lq;

    EPLDspGetLinkQualityInfo( portHandle, &lq);
    printf( "\n  Link Quality Details:\n");
    printf( "    Link Quality       %s\n",  lq.linkQualityEnabled ? "ENABLED":"DISABLED");

    printf( "\n");
    printf( "            Current   Thresholds   Alarms / Triggers\n");
    printf( "            Samples   Low   High   Low          High\n");
    printf( "    DEQ C1     %4d  %4d   %4d   %s   %s\n",
                    lq.c1CtrlSample, lq.c1LowThresh, lq.c1HighThresh, 
                    (lq.c1LowWarn ?  "TRIGGERED " : "no trigger"),
                    (lq.c1HighWarn ? "TRIGGERED " : "no trigger"));

    printf( "    DAGC       %4d  %4d   %4d   %s   %s\n",
                    lq.dagcCtrlSample, lq.dagcLowThresh, lq.dagcHighThresh,
                    (lq.dagcLowWarn ?  "TRIGGERED " : "no trigger"),
                    (lq.dagcHighWarn ? "TRIGGERED " : "no trigger"));

    printf( "    DBLW       %4d  %4d   %4d   %s   %s\n",
                    lq.dblwCtrlSample, lq.dblwLowThresh, lq.dblwHighThresh,
                    (lq.dblwLowWarn ?  "TRIGGERED " : "no trigger"),
                    (lq.dblwHighWarn ? "TRIGGERED " : "no trigger"));

    printf( "    FREQ       %4d  %4d   %4d   %s   %s\n",
                    lq.freqOffSample, lq.freqOffLowThresh, lq.freqOffHighThresh,
                    (lq.freqOffLowWarn ?  "TRIGGERED " : "no trigger"),
                    (lq.freqOffHighWarn ? "TRIGGERED " : "no trigger"));

    printf( "    FC         %4d  %4d   %4d   %s   %s\n",
                    lq.freqCtrlSample, lq.freqCtrlLowThresh, lq.freqCtrlHighThresh,
                    (lq.freqCtrlLowWarn ?  "TRIGGERED " : "no trigger"),
                    (lq.freqCtrlHighWarn ? "TRIGGERED " : "no trigger"));

    return;
}	// DisplayLinkStatus(...)


//****************************************************************************
//****************************************************************************
// Helper Functions - Not important to EPL usage
//****************************************************************************
//****************************************************************************

//****************************************************************************
void 
    displayBanner( 
        void)
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
    printf(   "*** EPL Test Application v%d.%d  Build: %d\n", VerMajor, VerMinor, VerBuild);
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
            "| -S "
            "| -D bb cc aa "
			"]\nCommands:\n"
			"  -H or -h or -?   Display this help\n"
            "  -V or -v         Verbose Mode where\n"
            "  -S or -s         Scan only (don't run tests)\n"
            "  -D bb cc aa      Device where:\n"
            "                      bb is the board number\n"
            "                      cc is the connector number\n"
            "                      aa is the address number\n"
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

			case 'S':
			case 's':
				bScanOnly = TRUE;
				break;

			case 'F':
			case 'f':
				bFind = TRUE;
				break;

            case 'D':
			case 'd':
                bFind = FALSE;
                nBoard      = ((NS_UINT)strtoul( (argv[ CurArg+1 ]), NULL, 0 ) - 1);
                nConnector  = ((NS_UINT)strtoul( (argv[ CurArg+2 ]), NULL, 0 ) - 1);
                nMDIOAddr   = ((NS_UINT)strtoul( (argv[ CurArg+3 ]), NULL, 0 ));
                break;

            case 'V':
            case 'v':
                bVerbose = TRUE;
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
