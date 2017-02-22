//****************************************************************************
// swig_help.h
// 
// Copyright (c) 2008 National Semiconductor Corporation.
// All Rights Reserved
// 
// This file contains macros that will help define the interfaces 
// more consistently between SWIG and C.
//
//****************************************************************************

#ifndef _SWIG_HELP_INCLUDE
#define _SWIG_HELP_INCLUDE

#ifdef SWIG
// SWIG is defined which means that SWIG is processing the file and we need
// to handle the definitions a bit differently to allow SWIG to the create
// the interface the way we want it to.

// SWIG doesn't know how to handle EXPORT like C does so convert it
// to nothing to remove it.
#define	EXPORT

// SWIG doesn't know how to handle IN and OUT like C does so convert it
// to nothing to remove it.
#define IN	
#define OUT

#else	// SWIG

// SWIG is NOT defined which means that C is processing the file and we need
// to handle the definitions a bit differently to allow C to the create
// the interface the way we want it to.

#endif	// SWIG

#endif // _SWIG_HELP_INCLUDE
