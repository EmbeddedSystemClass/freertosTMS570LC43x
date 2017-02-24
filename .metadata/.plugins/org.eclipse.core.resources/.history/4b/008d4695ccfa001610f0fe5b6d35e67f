//****************************************************************************
// epl_miiconfig.c
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// Contains sources for multi-port MII configuration.
//
// It implements the following functions:
//      EPLGetMiiConfig
//      EPLSetMiiConfig
//****************************************************************************

#include "epl.h"

static NS_UINT miiPortCfgMap[7][3] = \
                    { {P849_RBR_NORMAL, P849_RBR_NORMAL, MIIPCFG_NORMAL},
                      {P849_RBR_SWAP, P849_RBR_SWAP, MIIPCFG_PORT_SWAP},
                      {P849_RBR_EXT, P849_RBR_EXT, MIIPCFG_EXT_MEDIA_CONVERTER},
                      {P849_RBR_TX_NORMAL, P849_RBR_TX_OPPOSITE, MIIPCFG_BROADCAST_TX_PORT_A},
                      {P849_RBR_TX_OPPOSITE, P849_RBR_TX_NORMAL, MIIPCFG_BROADCAST_TX_PORT_B},
                      {P849_RBR_RX_BOTH_PORTS, P849_RBR_RX_DISABLED, MIIPCFG_MIRROR_RX_CHANNEL_A},
                      {P849_RBR_RX_DISABLED, P849_RBR_RX_BOTH_PORTS, MIIPCFG_MIRROR_RX_CHANNEL_B} };

//****************************************************************************
EXPORT EPL_MIICFG_ENUM
    EPLGetMiiConfig(
        IN PEPL_DEV_HANDLE deviceHandle)

//  Returns the current MII configuration. On devices supporting the 
//  EPL_CAPA_MII_PORT_CFG feature this method returns the device's current 
//  MII port mapping configuration. If the device configuration is 
//  undefined, MIIPCFG_UNKNOWN will be returned.
//
//  deviceHandle
//      Handle that represents the device. This is obtained using the 
//      EPLEnumDevice function.
//
//  Returns:
//      A value from EPLMII_CFG_ENUM.
//****************************************************************************
{
PDEVICE_OBJ devObj = (PDEVICE_OBJ)deviceHandle;
NS_UINT x, chArbr, chBrbr, keya, keyb;
 
    if( !(devObj->capa & EPL_CAPA_MII_PORT_CFG) ) 
        return MIIPCFG_UNKNOWN;

    chArbr = EPLReadReg( (PEPL_PORT_HANDLE)devObj->portObjs, PHY_RBR) & \
                         (P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK);
    chBrbr = EPLReadReg( (PEPL_PORT_HANDLE)devObj->portObjs->link, PHY_RBR) & \
                         (P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK);

    for ( x = 0; x < (sizeof( miiPortCfgMap) / (sizeof( NS_UINT) * 3)); x++)
    {
        if ( chArbr == miiPortCfgMap[x][0] && chBrbr == miiPortCfgMap[x][1])
            return miiPortCfgMap[x][2];
    }

    // Could be one of the don't care values.
    keya = chArbr & ~P849_RBR_RX_PORT_MASK;
    keyb = chBrbr & ~P849_RBR_RX_PORT_MASK;
    for ( x = 0; x < (sizeof( miiPortCfgMap) / (sizeof( NS_UINT) * 3)); x++)
    {
        if ( keya == miiPortCfgMap[x][0] && keyb == miiPortCfgMap[x][1])
            return miiPortCfgMap[x][2];
    }
    
    keya = chArbr & ~P849_RBR_TX_SOURCE_MASK;
    keyb = chBrbr & ~P849_RBR_TX_SOURCE_MASK;
    for ( x = 0; x < (sizeof( miiPortCfgMap) / (sizeof( NS_UINT) * 3)); x++)
    {
        if ( keya == miiPortCfgMap[x][0] && keyb == miiPortCfgMap[x][1])
            return miiPortCfgMap[x][2];
    }

    if ( (chArbr & (P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK)) == \
         (P849_RBR_RX_DISABLED | P849_RBR_TX_DISABLED))
        return MIIPCFG_DISABLE_PORT_A;

    if ( (chBrbr & (P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK)) == \
         (P849_RBR_RX_DISABLED | P849_RBR_TX_DISABLED))
        return MIIPCFG_DISABLE_PORT_B;
    
    return MIIPCFG_UNKNOWN;
}


//****************************************************************************
EXPORT void
    EPLSetMiiConfig(
        IN PEPL_DEV_HANDLE deviceHandle,
        IN EPL_MIICFG_ENUM miiPortConfig)
        
//  Configures the device's MII configuration. On devices supporting the 
//  EPL_CAPA_MII_PORT_CFG feature this method sets the device's MII port 
//  mapping configuration. 
//
//  deviceHandle
//      Handle that represents the device. This is obtained using the 
//      EPLEnumDevice function.
//  miiPortConfig
//      One of the values defined in EPL_MIICFG_ENUM (see 
//      EPLGetMiiPortConfig). This parameter should NOT be set to 
//      MIIPCFG_UNKNOWN.
//
//  Returns:
//      Nothing
//****************************************************************************
{
PDEVICE_OBJ devObj = (PDEVICE_OBJ)deviceHandle;
NS_UINT x, chArbr, chBrbr;

    if( !(devObj->capa & EPL_CAPA_MII_PORT_CFG) ) 
        return;

    chArbr = EPLReadReg( (PEPL_PORT_HANDLE)devObj->portObjs, PHY_RBR) & \
                         ~(P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK);
    chBrbr = EPLReadReg( (PEPL_PORT_HANDLE)devObj->portObjs->link, PHY_RBR) & \
                         ~(P849_RBR_RX_PORT_MASK | P849_RBR_TX_SOURCE_MASK);
    
    for ( x = 0; x < (sizeof( miiPortCfgMap) / (sizeof( NS_UINT) * 3)); x++)
    {
        if ( miiPortCfgMap[x][2] == miiPortConfig)
        {
            chArbr |= miiPortCfgMap[x][0];
            chBrbr |= miiPortCfgMap[x][1];
            break;
        }
    }

    if (x > (sizeof( miiPortCfgMap) / (sizeof( NS_UINT) * 3)))
    {
        if ( miiPortConfig == MIIPCFG_DISABLE_PORT_A)
            chArbr |= (P849_RBR_RX_DISABLED | P849_RBR_TX_DISABLED);
        else if ( miiPortConfig == MIIPCFG_DISABLE_PORT_B)
            chBrbr |= (P849_RBR_RX_DISABLED | P849_RBR_TX_DISABLED);
    }
            
    EPLWriteReg( (PEPL_PORT_HANDLE)devObj->portObjs, PHY_RBR, chArbr);
    EPLWriteReg( (PEPL_PORT_HANDLE)devObj->portObjs->link, PHY_RBR, chBrbr);
    return;
}