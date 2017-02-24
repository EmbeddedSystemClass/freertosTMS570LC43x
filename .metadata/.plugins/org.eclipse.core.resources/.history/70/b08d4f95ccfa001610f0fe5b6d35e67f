//****************************************************************************
// ifCyUSB.cpp
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// ifCyUSB - Access routines for Cypress USB access to PHY
//****************************************************************************

// Prevent inclusion of winsock.h in windows.h will be added as part 
// epl.h by way of ptp stack includes.
#define _WINSOCKAPI_   
#include <windows.h>
#undef  _WINSOCKAPI_    // undo hack above.

#include "epl.h"

// Cypress structures require default packing (8)
#pragma pack( push, 8 )     // Save current packing and set to 8
#include "cyapi.h"
#pragma pack( pop )         // Restore packing 

// USB Operations aka the request code in a control pipe
#define SERIAL_RD	0xb0
#define SERIAL_WR	0xb1
#define MDIO_RD		0xb2
#define MDIO_WR     0xb3

GUID guid;

CCyUSBDevice *USBDevice;

// Local prototypes
HRESULT ConvertStringtoCLSID(
    LPSTR pszString,
    LPGUID pguid);

//****************************************************************************
EXPORT NS_STATUS
    ifCyUSB_Init( 
	    IN OAI_DEV_HANDLE oaiDevHandle)
//
//  Parameters
//      oaiDevHandle
//          Handle that represents the MDIO bus that the write operation 
//          should occur on. The definition of this is completely up to 
//          higher layer software.
//  Return Value
//      NS_STATUS_SUCCESS - Function was successfully executed.
//      NS_STATUS_FAILURE - Function was not able to initialize the interface.  
//                          This usually means that a device was not found.
//
//  Comments
//      This call is not usually called directly.  It is typically called from 
//      the EPLEnumDevice() function if it hasn’t already been initialized.
//****************************************************************************
{
NS_STATUS   retVal = NS_STATUS_SUCCESS;

    if( !oaiDevHandle->ifHandle ) {

        // Interface is not initialized do it now.
	    ConvertStringtoCLSID("{AE18AA60-7F6A-11d4-97DD-00010229B959}", &guid);
	    USBDevice = new CCyUSBDevice(NULL, guid);
	    if(USBDevice->ControlEndPt == NULL)
	    {
		    delete (USBDevice);
		    ConvertStringtoCLSID("{F8629463-9545-46d8-AB75-A6176D84526C}", &guid);
		    USBDevice = new CCyUSBDevice(NULL, guid);
	    }

        if( USBDevice->ControlEndPt ) {
            oaiDevHandle->ifHandle = USBDevice;
            // Success
        }
        else {
            oaiDevHandle->ifHandle = NULL;
            retVal = NS_STATUS_FAILURE;
        }
    } // if( !oaiDevHandle->ifHandle )

	return retVal;
}


//****************************************************************************
EXPORT void
    ifCyUSB_DeInit( 
	    IN OAI_DEV_HANDLE oaiDevHandle)
//
//  Parameters
//      oaiDevHandle
//          Handle that represents the MDIO bus that the write operation 
//          should occur on. The definition of this is completely up to 
//          higher layer software.
//  Return Value
//      Nothing
//  Comments
//      This call is not usually called directly.  It is typically called 
//      from the EPLDeInitialize() function as part of the overall EPL 
//      shutdown process.
//****************************************************************************
{

	if( USBDevice ) {
		delete (USBDevice);
	}
	return;
}

#define MDIO_BUF_SIZE	6

//****************************************************************************
NS_UINT
    ifCyUSB_ReadMDIO (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex)

//  Issues a read request Phy control operation through the environment's 
//  MAC interface. Host software must implement this function as a synchronous 
//  operation.
//
//  portHandle
//      Handle that represents the device that the read operation should 
//      occur on.
//  regIndex
//      Index to read - Bits 7:5 select the  register page 
//      (000-pg0, 001-pg1, 010-pg3, 011-pg4, etc.).
//
//  Returns:
//      The value read from the register.
//****************************************************************************
{
	CCyControlEndPoint  *ept = USBDevice->ControlEndPt;    
	
    ept->Target    = TGT_DEVICE;  
    ept->ReqType   = REQ_VENDOR;  
    ept->Direction = DIR_FROM_DEVICE;   
    ept->ReqCode   = MDIO_RD;
    ept->Value     = (NS_UINT)(portHandle->portMdioAddress | (regIndex << 8));
    ept->Index     = 0x00;

	long buflen = MDIO_BUF_SIZE;  
	unsigned char buf[MDIO_BUF_SIZE];
	for(int i=0; i<MDIO_BUF_SIZE; ++i ){
		buf[i]=0;
	}

	ept->XferData(buf, buflen);      
	
    return ( (NS_UINT)(buf[0] | (buf[1]<<8)) );
}

 
//****************************************************************************
void
    ifCyUSB_WriteMDIO (
        IN PEPL_PORT_HANDLE portHandle,
        IN NS_UINT regIndex,
		IN NS_UINT value)

//  Issues a write operation Phy control operation through the environment's 
//  MAC interface.
//
//  portHandle
//      Handle that represents the device that the write operation should 
//      occur on.
//  regIndex
//      Index to write - Bits 7:5 select the  register page 
//      (000-pg0, 001-pg1, 010-pg3, 011-pg4, etc.).
//  value
//      value to write
//
//  Returns:
//      Nothing
//****************************************************************************
{
	CCyControlEndPoint  *ept = USBDevice->ControlEndPt;    
	
	ept->Target    = TGT_DEVICE;  
	ept->ReqType   = REQ_VENDOR;  
	ept->Direction = DIR_FROM_DEVICE;   
	ept->ReqCode   = MDIO_WR;    
    ept->Value     = (NS_UINT)(portHandle->portMdioAddress | (regIndex << 8));
	ept->Index     = value;
		
	long buflen = MDIO_BUF_SIZE;  
	unsigned char buf[MDIO_BUF_SIZE];
	for(int i=0; i<MDIO_BUF_SIZE; ++i ){
		buf[i]=0;
	}
	 
	ept->XferData(buf,  buflen);      
		
	return;
}


//****************************************************************************
//
// Function: ConvertStringtoCLSID
//
// Synopsis: Utility function to convert a string to a GUID. Uses CLSIDFromString.
//
// Arguments:
//           [in]
//           LPSTR pszString,
//
//           [out]
//           LPGUID pguid)
//
// Returns:
//          S_OK if the function succeeded
//
//****************************************************************************
HRESULT ConvertStringtoCLSID(
    LPSTR pszString,
    LPGUID pguid)
{
    #define GUID_STRING_SIZE 39

    HRESULT hr= S_OK;
    WCHAR szWGuid[GUID_STRING_SIZE];
    LPSTR pszSrc;
    LPWSTR pszWDest;
   
    if(pszString == NULL) {
        hr = E_INVALIDARG;
        goto CLEANUP;
    }

    pszSrc = pszString;

    if(*pszSrc != '{') {
        hr = E_INVALIDARG;
        goto CLEANUP;
    }

    // Convert to Unicode while you are copying to your temporary buffer.
    // Do not worry about non-ANSI characters; this is a GUID string.

    pszWDest = szWGuid;

    while((*pszSrc) && (*pszSrc != '}') &&
          (pszWDest < &szWGuid[GUID_STRING_SIZE - 2])) {

        *pszWDest++ = *pszSrc++;
    }

    // On success, pszSrc will point to '}' (the last character of the GUID string).

    if(*pszSrc != '}') {
        hr = E_INVALIDARG;
        goto CLEANUP;
    }


    // pszDest will still be in range and have two chars left because
    // of the condition in the preceding while loop.

    *pszWDest++ = '}';
    *pszWDest = '\0';

    // Borrow the functionality of CLSIDFromString to get the 16-byte
    // GUID from the GUID string.

     hr = CLSIDFromString(
        szWGuid,
        pguid);

 CLEANUP:

    return hr;
}

 
