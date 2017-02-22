//****************************************************************************
// nscphyter1588.cpp
//
// Defines the entry point for the DLL application.
// This is O/S specific since it defines the enry point for a Windows DLL.
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
//****************************************************************************

// Prevent inclusion of winsock.h in windows.h will be added as part 
// epl.h by way of ptp stack includes.
#define _WINSOCKAPI_   
//#include <windows.h>
#include <Shlwapi.h>	// Needed for PathRemoveFileSpec
#include <strsafe.h>	// Needed for StringCbCat
#undef  _WINSOCKAPI_    // undo hack above.

// Suppress warnings for deprecated functions - We aren't using them so it should matter
#pragma warning(disable : 4995) 

#include "epl.h"		// The rest of the definitions for the project

#pragma warning(default : 4995) // Restore warning level

#ifdef __cplusplus
extern "C" {
#endif

extern DWORD  ptpTLSSlot;

#define SHMEMSIZE 4096 

LPVOID lpvMem = NULL;            // pointer to shared memory
static HANDLE hMapObject = NULL; // handle to file mapping

#ifdef __cplusplus
}
#endif



BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
BOOL bResult = TRUE;

BOOL fInit, fIgnore;

	switch (ul_reason_for_call)
	{
	    case DLL_PROCESS_ATTACH:
            TCHAR pth[MAX_PATH];
            DWORD pthLen;
            
            pthLen = GetModuleFileName( (HMODULE)hModule, pth, sizeof( pth) / sizeof( TCHAR));
            if ( pthLen == 0 || pthLen == (sizeof( pth) / sizeof( TCHAR)))
            {
                bResult = FALSE;
                break;
            }
            
            PathRemoveFileSpec( pth);
            StringCbCat( pth, sizeof( pth), "\\okFrontPanel.dll");
            
            bResult = okFrontPanelDLL_LoadLib( pth);
            
            // Allocate our PTP thread local storage slot
            if ( (ptpTLSSlot = TlsAlloc()) == TLS_OUT_OF_INDEXES) 
            {
                bResult = FALSE;
                break;
            }

            // Create a named file mapping object
            hMapObject = CreateFileMapping( 
                INVALID_HANDLE_VALUE,   // use paging file
                NULL,                   // default security attributes
                PAGE_READWRITE,         // read/write access
                0,                      // size: high 32-bits
                SHMEMSIZE,              // size: low 32-bits
                TEXT("EPLifmemfile")); // name of map object
            if (hMapObject == NULL) 
                return FALSE; 
 
            // The first process to attach initializes memory
            fInit = (GetLastError() != ERROR_ALREADY_EXISTS); 
 
            // Get a pointer to the file-mapped shared memory
            lpvMem = MapViewOfFile( 
                hMapObject,     // object to map view of
                FILE_MAP_WRITE, // read/write access
                0,              // high offset:  map from
                0,              // low offset:   beginning
                0);             // default: map entire file
            if (lpvMem == NULL) 
                return FALSE; 
 
            // Initialize memory if this is the first process
            if( fInit ) 
                memset(lpvMem, '\0', SHMEMSIZE); 
            break;
        
	    case DLL_THREAD_ATTACH:
            break;
            
	    case DLL_THREAD_DETACH:
            break;
            
	    case DLL_PROCESS_DETACH:
            okFrontPanelDLL_FreeLib();
            TlsFree( ptpTLSSlot );

            // Unmap shared memory from the process's address space
            fIgnore = UnmapViewOfFile(lpvMem); 
 
            // Close the process's handle to the file-mapping object
            fIgnore = CloseHandle(hMapObject); 

    		break;
	}
    
    return bResult;
}

