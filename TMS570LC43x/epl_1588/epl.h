//****************************************************************************
// epl.h
// 
// Copyright (c) 2006-2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This is the main EPL include (header) file. Include this to pull in 
// all EPL definitions and prototypes.
//****************************************************************************

#ifndef _EPL_INCLUDE
#define _EPL_INCLUDE

#include "epl_types.h"		// EPL Basic type definitions
#include "epl_oai.h"

#include "epl_regs.h"		// Device register definitions
#include "HL_mdio.h"
#include "HL_emac.h"

//#include "oai.h"			// Needed to "qualify" defs for the specific O/S

// Include all of the sub-module headers
//#include "swig_help.h"		// Macros for SWIG processing

//#include "epl_core.h"		// Core/General API definitions/prototypes
//#include "epl_bist.h"		// BIST API definitions/prototypes
//#include "epl_link.h"		// Link API definitions/prototypes
//#include "epl_miiconfig.h"	// MII config API definitions/prototypes
//#include "epl_quality.h"	// Link Quality API definitions/prototypes
//#include "epl_tdr.h"		// TDR API definitions/prototypes

#include "epl_platform.h"

#include "epl_1588.h"		// PTP protocol related API definitions/prototypes

#define PAGESEL_REG		(0x13)
#define PAGESEL_MASK	(0xE0)
#define PAGESEL_SHIFT	(5u)
#define GET_PAGE(x)		((x & PAGESEL_MASK)>> PAGESEL_SHIFT)
void dp83630_set_page(hdkif_t *hdkif, uint16_t reg);

// Other modules for the DLL
//#include "ifGenMAC.h"		// Interface for generic MAC - Not filled in/used
//#include "ifCyUSB.h"		// Interface for Cypress USB definitions/prototypes
//#include "ifLPT.h"			// Interface for MDIO LPT definitions/prototypes
//#include "okMAC.h"			// Interface/MAC related definitions/prototypes

// PTP definitions
//#include "PTPStack\\ptpd.h"

#endif // _EPL_INCLUDE
