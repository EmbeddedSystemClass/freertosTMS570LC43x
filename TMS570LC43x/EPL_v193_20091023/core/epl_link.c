//****************************************************************************
// epl_link.c
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// Contains sources for link related functions.
//
// It implements the following functions:
//      EPLIsLinkUp
//      EPLGetLinkStatus
//      EPLSetLinkConfig
//      EPLSetLoopbackMode
//****************************************************************************

#include "epl.h"


//****************************************************************************
EXPORT NS_BOOL
    EPLIsLinkUp(
        IN PEPL_PORT_HANDLE portHandle)
        
//  Returns whether or not a valid link exists on the specified port.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//
//  Returns:
//      TRUE if a valid link exists on the specified port, FALSE otherwise.
//****************************************************************************
{
    return EPLReadReg( portHandle, PHY_PHYSTS) & P848_STS_LINK;
}

 
//****************************************************************************
EXPORT void
    EPLGetLinkStatus(
        IN PEPL_PORT_HANDLE portHandle,
        IN OUT PEPL_LINK_STS linkStatusStruct)
        
//  Returns detailed information regarding the port's link status.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  linkStatusStruct
//      Pointer to a caller supplied EPL_LINK_STS (see below) structure 
//      that is filled out on return.
//
//  Returns:
//      The fields in the passed in linkStatusStruct will be set accordingly 
//      on return.
//****************************************************************************
{
NS_UINT reg;

    OAIBeginMultiCriticalSection( portHandle->oaiDevHandle);
    linkStatusStruct->linkup = EPLIsLinkUp( portHandle);
    linkStatusStruct->autoNegEnabled = FALSE;
    linkStatusStruct->autoNegCompleted = FALSE;
    linkStatusStruct->duplex = FALSE;
    linkStatusStruct->mdixStatus = FALSE;
    linkStatusStruct->autoMdixEnabled = FALSE;
    linkStatusStruct->polarity = FALSE;
    linkStatusStruct->energyDetectPower = FALSE;
    linkStatusStruct->speed = 10;

    reg = EPLReadReg( portHandle, PHY_BMCR);
    if ( reg & BMCR_AUTO_NEG_ENABLE)
        linkStatusStruct->autoNegEnabled = TRUE;
        
    reg = EPLReadReg( portHandle, PHY_BMSR);
    if ( reg & BMSR_AUTO_NEG_COMPLETE)
        linkStatusStruct->autoNegCompleted = TRUE;
        
    reg = EPLReadReg( portHandle, PHY_PHYSTS);
    if ( reg & P848_STS_DUPLEX)
        linkStatusStruct->duplex = TRUE;
    if ( reg & P848_STS_POLARITY)
        linkStatusStruct->polarity = TRUE;
    if ( !(reg & P848_STS_SPEED))
        linkStatusStruct->speed = 100;
    if ( reg & P848_STS_MDIX_MODE)
        linkStatusStruct->mdixStatus = TRUE;
        
    reg = EPLReadReg( portHandle, PHY_PHYCTRL);
    if ( reg & P848_PHYCTRL_MDIX_EN)
        linkStatusStruct->autoMdixEnabled = TRUE;
        
    reg = EPLReadReg( portHandle, PHY_EDCR);
    if ( reg & P848_EDCR_PWR_STATE)
        linkStatusStruct->energyDetectPower = TRUE;
    OAIEndMultiCriticalSection( portHandle->oaiDevHandle);
    return;
}

 
//****************************************************************************
EXPORT void
    EPLSetLinkConfig(
        IN PEPL_PORT_HANDLE portHandle,
        IN PEPL_LINK_CFG linkConfigStruct)
        
//  Configures the port's link settings. This function does NOT wait for link 
//  establishment to complete (e.g. auto-negotiation).
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  linkConfigStruct
//      Pointer to a caller supplied EPL_LINK_CFG (see below) structure that 
//      specifies link configuration parameters.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT edcr, bmcr, anar, phycr;

    OAIBeginMultiCriticalSection( portHandle->oaiDevHandle);
    bmcr = EPLReadReg( portHandle, PHY_BMCR);
    bmcr &= BMCR_LOOPBACK | BMCR_ISOLATE | BMCR_POWER_DOWN;
    anar = EPLReadReg( portHandle, PHY_ANAR);
    anar &= ~(ANAR_PAUSE_SUPPORT | ANAR_ASY_PAUSE_SUPPORT |
              ANAR_100T_FULL_DUP | ANAR_100T_HALF_DUP |
              ANAR_10T_FULL_DUP  | ANAR_10T_HALF_DUP);

    // Setup PAUSE support
    if ( linkConfigStruct->duplex && linkConfigStruct->pause)
        anar |= ANAR_PAUSE_SUPPORT;
                
    // Set the link speed according to which modes are backward compatible
    // In autoneg mode, the modes are backwards compatible. For example,
    // with a 1 Gbps max link speed, 100 and 10 Mbps modes are also
    // support. Same type of thing with the duplex.
    if ( linkConfigStruct->speed >= 100)
    {
        anar |= ANAR_100T_HALF_DUP;
        if ( linkConfigStruct->duplex)
            anar |= ANAR_100T_FULL_DUP;
    }

    if ( linkConfigStruct->speed >= 10)
    {
        anar |= ANAR_10T_HALF_DUP;
        if ( linkConfigStruct->duplex) 
            anar |= ANAR_10T_FULL_DUP;
    }
                
    if ( !linkConfigStruct->autoNegEnable)
    {
        if ( linkConfigStruct->duplex) 
            bmcr |= BMCR_FORCE_FULL_DUP;
        if ( linkConfigStruct->speed == 100)
            bmcr |= BMCR_FORCE_SPEED_100;
        else if ( linkConfigStruct->speed == 10)
            bmcr |= BMCR_FORCE_SPEED_10;
    }
    else
    {
        // Enable auto-neg
        bmcr |= BMCR_AUTO_NEG_ENABLE | BMCR_RESTART_AUTONEG;
    }

    // Setup MDIX
    phycr = EPLReadReg( portHandle, PHY_PHYCTRL);
    phycr &= ~(P848_PHYCTRL_MDIX_EN | P848_PHYCTRL_FORCE_MDIX);
    if ( linkConfigStruct->autoMdix == MDIX_FORCE_SWAP)
        phycr |= P848_PHYCTRL_FORCE_MDIX;
    else if ( linkConfigStruct->autoMdix == MDIX_AUTO)
        phycr |= P848_PHYCTRL_MDIX_EN;
    EPLWriteReg( portHandle, PHY_PHYCTRL, phycr);
    
    edcr = EPLReadReg( portHandle, PHY_EDCR) & ~(P848_EDCR_ENABLE|P848_EDCR_DATA_CNT_MASK);
    edcr |= P848_EDCR_BURST_DIS;
    edcr &= ~(P848_EDCR_DATA_CNT_MASK | P848_EDCR_ERR_CNT_MASK);
    if ( linkConfigStruct->energyDetect)
    {
        edcr |= P848_EDCR_ENABLE;
        edcr |= (linkConfigStruct->energyDetectDataCountThresh & 0x0F) | \
                ((linkConfigStruct->energyDetectErrCountThresh & 0x0F) << 4);
    }
    EPLWriteReg( portHandle, PHY_EDCR, edcr);
    
    // Activate the new speed & autoneg settings
    EPLWriteReg( portHandle, PHY_ANAR, anar);
    EPLWriteReg( portHandle, PHY_BMCR, bmcr);
    OAIEndMultiCriticalSection( portHandle->oaiDevHandle);
    return;
}

 
//****************************************************************************
EXPORT void
    EPLSetLoopbackMode(
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_BOOL enableLoopback)
       
//  Enables or disables port loopback mode.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//  enableLoopback
//      Set to TRUE to enable port loopback, FALSE otherwise.
//
//  Returns:
//      Nothing
//****************************************************************************
{
NS_UINT bmcr;

    OAIBeginMultiCriticalSection( portHandle->oaiDevHandle);
    bmcr = EPLReadReg( portHandle, PHY_BMCR) & ~BMCR_LOOPBACK;
    
    if ( enableLoopback)
    {
        // Must disable auto-neg when entering loopback
        bmcr &= ~BMCR_AUTO_NEG_ENABLE;
        bmcr |= BMCR_LOOPBACK;
    }
    else
    {
        // Disable all loopback
        bmcr &= ~BMCR_LOOPBACK;
        bmcr |= BMCR_AUTO_NEG_ENABLE;
    }
    
    EPLWriteReg( portHandle, PHY_BMCR, bmcr);
    OAIEndMultiCriticalSection( portHandle->oaiDevHandle);
    return;
}

  
//****************************************************************************
EXPORT void
    EPLRestartAutoNeg(
        IN PEPL_PORT_HANDLE portHandle)
        
//  Restarts auto-negotiation. This function does NOT wait for 
//  auto-negotiation to finish.
//
//  portHandle
//      Handle that represents a port. This is obtained using the 
//      EPLEnumPort function.
//
//  Returns:
//      Nothing
//****************************************************************************
{
    EPLWriteReg( portHandle, PHY_BMCR, BMCR_RESTART_AUTONEG);
    return;
}
