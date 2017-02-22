%module epl
%include typemaps.i

%{
#include "epl.h"

#include "ptpControl.h"
%}

#===================================================================================
# Typemaps to create lists instead of a raw buffer for output
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# typemap(arginit) used to initialize variables for the wrapper
# Here we use it to create a local variable to determine how many list elements to
# create/process.  The default here are for a single structure/value to be returned
# which is not really useful so these are usually overridden below by defining a 
# new typemap(arginit) for the specific needs.  That is the number of items in the 
# list and/or type of value returned.  For VALUE_OUT we also specify a type string
# that is passed into Py_BuildValue to tell it how to convert the data.
#-----------------------------------------------------------------------------------
%typemap(arginit) STRUCT_OUT    "int n_$1 = 1;";
%typemap(arginit) VALUE_OUT     "int n_$1 = 1; \n char *Py_BV_Type_$1 = \"l\"; ";

#-----------------------------------------------------------------------------------
# typemap(in ...) is used to process the input parameter.  
# Here we set numinputs=0 to tell SWIG not to expect any inputs for these parameters.  
# We also use this to allocate the buffers that will be passed into the C function.
#-----------------------------------------------------------------------------------
%typemap(in, numinputs=0) STRUCT_OUT "$1 = ($1_type) malloc( sizeof($*1_type)*n_$1);";
%typemap(in, numinputs=0) VALUE_OUT  "$1 = ($1_type) malloc( sizeof($*1_type)*n_$1);";

#-----------------------------------------------------------------------------------
# typemap(argout) is the main processing agent
# Processing is as follows:
# - define some variables that we need to work
# - Create a list of n_$1 (variable created in arginit) elements
# - For each of the n_$1 elements:
#   - allocate a new buffer
#   - copy data from the buffer filled in by the C function into the new buffer
#   - Create a new object based on that new buffer.  Here we only use SWIG_POINTER_OWN
#     for flags.  This causes a SWIGTYPE_p_xxxxxxxxxx object to be created that
#     Python will take control of.  Another key aspect here is to NOT use SWIG_POINTER_NEW
#     which others to.  SWIG_POINTER_NEW includes SWIG_POINTER_NOSHADOW which prevents
#     the new object from being turned into a shadow class of proxy class.  This is a SWIG
#     created class for a structure that allows you to manipulate the members naturally
#     from Python.
#   - Set the list entry to point to the new object
# - Finally append the newly created list to the result object
#-----------------------------------------------------------------------------------
%typemap(argout) STRUCT_OUT {
  PyObject *list = 0, *obj = 0;
  $1_type nresult = $1;
  int n;
  list = PyList_New(n_$1);
  if( n_$1 > 1 ) { 
        if( list ) {
            for( n=0; n < n_$1 ; n++ ) {
                obj = SWIG_NewPointerObj( ($1_type)memcpy( ($1_type)malloc( sizeof( $*1_type)), nresult, sizeof( $*1_type)), 
                                         $1_descriptor, SWIG_POINTER_OWN );
                PyList_SetItem(list, n, obj);
                nresult++;
            }
            %append_output(list);      
        }
        else {
            %append_output(SWIG_Py_None());
        }
    }
    else {
        obj = SWIG_NewPointerObj( ($1_type)memcpy( ($1_type)malloc( sizeof( $*1_type)), nresult, sizeof( $*1_type)), 
                                 $1_descriptor, SWIG_POINTER_OWN );
        %append_output(obj);          
    }
}

#-----------------------------------------------------------------------------------
# VALUE_OUT
# This is similar to the above except it returns a list of values instead of 
# structures.  Long is used by default since Python is pretty flexible with types.
# To change the type create/modify a arginit typemap to specify a different string
# value that is passed into Py_BuildValue using the Py_BV_Type.  
# If a type other than what Py_BuildValue creates is needed you can copy this and 
# insert whatever code is needed to create a PyObject of the type you need.
#-----------------------------------------------------------------------------------
%typemap(argout) VALUE_OUT {
    PyObject *list = 0, *obj = 0;
    $1_type nresult = $1;
    int n;
    if( n_$1 > 1 ) {
        list = PyList_New(n_$1);
        if( list ) {
            for( n=0; n < n_$1 ; n++ ) {
                obj = Py_BuildValue( Py_BV_Type_$1, *nresult );
                PyList_SetItem(list, n, obj);
                nresult++;
            }
            %append_output(list);      
        }
        else {
            %append_output(SWIG_Py_None());
        }
    }
    else {
        obj = Py_BuildValue( Py_BV_Type_$1, *nresult );
        %append_output(obj);      
    }
}

#-----------------------------------------------------------------------------------
# typemap(freearg) is used to cleanup the memory that we allocated
# It can be used simply as a cleanup section.
#-----------------------------------------------------------------------------------
%typemap(freearg) STRUCT_OUT  "if( $1 ) free($1);";
%typemap(freearg) VALUE_OUT   "if( $1 ) free($1);";

#-----------------------------------------------------------------------------------
# Now derive "new" typemaps from those above for specific needs
# Notice that most of the "new" typemaps only differ in the number of elements
# that they request (as defined in the arginit n_$1 value).
#-----------------------------------------------------------------------------------

# STRUCT_OUT_LIST_10 is used to return a list of 10 structures
%typemap(arginit)         STRUCT_OUT_LIST_10 "int n_$1 = 10;";
%typemap(in, numinputs=0) STRUCT_OUT_LIST_10 = STRUCT_OUT;
%typemap(argout)          STRUCT_OUT_LIST_10 = STRUCT_OUT;
%typemap(freearg)         STRUCT_OUT_LIST_10 = STRUCT_OUT;

# STRUCT_OUT_LIST_8 is used to return a list of 8 structures
%typemap(arginit)         STRUCT_OUT_LIST_8 "int n_$1 = 8;";
%typemap(in, numinputs=0) STRUCT_OUT_LIST_8 = STRUCT_OUT;
%typemap(argout)          STRUCT_OUT_LIST_8 = STRUCT_OUT;
%typemap(freearg)         STRUCT_OUT_LIST_8 = STRUCT_OUT;

# STRUCT_OUT_LIST_2 is used to return a list of 2 structures
%typemap(arginit)         STRUCT_OUT_LIST_2 "int n_$1 = 2;";
%typemap(in, numinputs=0) STRUCT_OUT_LIST_2 = STRUCT_OUT;
%typemap(argout)          STRUCT_OUT_LIST_2 = STRUCT_OUT;
%typemap(freearg)         STRUCT_OUT_LIST_2 = STRUCT_OUT;

# STRUCT_OUT_ONLY_1 is used to simply return a single structure
%typemap(arginit)         STRUCT_OUT_ONLY_1 "int n_$1 = 1;";
%typemap(in, numinputs=0) STRUCT_OUT_ONLY_1 = STRUCT_OUT;
%typemap(argout)          STRUCT_OUT_ONLY_1 = STRUCT_OUT;
%typemap(freearg)         STRUCT_OUT_ONLY_1 = STRUCT_OUT;

# VALUE_OUT_L_LIST_256 is used to return a list of 256 long values
%typemap(arginit)         VALUE_OUT_L_LIST_256 "int n_$1 = 256; \n char *Py_BV_Type_$1 = \"l\"; ";
%typemap(in, numinputs=0) VALUE_OUT_L_LIST_256 = VALUE_OUT;
%typemap(argout)          VALUE_OUT_L_LIST_256 = VALUE_OUT;
%typemap(freearg)         VALUE_OUT_L_LIST_256 = VALUE_OUT;

#===================================================================================
# End of basic typemap definitions
#===================================================================================

%include "epl_types.h"		#// EPL Basic type definitions

%include "platform.h"		#// Platform specific stuff (defines OAI_DEV_HANDLE)

%include "epl_regs.h"		#// Device register definitions

%include "oai.h"			#// Needed to "qualify" defs for the specific O/S

#// Include all of the sub-module headers
%include "swig_help.h"		#// Macros for SWIG processing

%include "epl_core.h"		#// Core/General API definitions/prototypes

#-----------------------------------------------------------------------------------
# Do some typemap adjustments to make things work better for Python
#-----------------------------------------------------------------------------------
%apply NS_BOOL *OUTPUT { NS_BOOL *bistActiveFlag }; 
%apply NS_UINT *OUTPUT { NS_UINT *errDataNibbleCount };
#-----------------------------------------------------------------------------------

%include "epl_bist.h"		#// BIST API definitions/prototypes

%apply STRUCT_OUT_ONLY_1  { PEPL_LINK_STS linkStatusStruct };

%include "epl_link.h"		#// Link API definitions/prototypes

%include "epl_miiconfig.h"	#// MII config API definitions/prototypes

#-----------------------------------------------------------------------------------
# Do some typemap adjustments to make things work better for Python
#-----------------------------------------------------------------------------------
%apply NS_UINT *OUTPUT   { NS_UINT *cableLength };
%apply NS_SINT *OUTPUT   { NS_SINT *freqOffsetValue };
%apply NS_SINT *OUTPUT   { NS_SINT *freqControlValue };
%apply NS_UINT *OUTPUT   { NS_UINT *varianceValue };
%apply STRUCT_OUT_ONLY_1 { PDSP_LINK_QUALITY_GET linkQualityStruct };

#-----------------------------------------------------------------------------------

%include "epl_quality.h"	#// Link Quality API definitions/prototypes

#-----------------------------------------------------------------------------------
# Now that we have the typemaps created we need to tell SWIG where to use it.
# This is kind of like a C macro were every instance of the parameter inside
# the { ... } will be translated to the type listed after %apply.  That type is
# abitrary and is simply used to match the specific parameters to a particular
# typemap.
#-----------------------------------------------------------------------------------
%apply STRUCT_OUT_LIST_10 { PTDR_RUN_RESULTS  posResultsArrayNoInvert };
%apply STRUCT_OUT_LIST_8  { PTDR_RUN_RESULTS  negResultsArrayNoInvert };
%apply STRUCT_OUT_LIST_8  { PTDR_RUN_RESULTS  posResultsArrayInvert };
%apply STRUCT_OUT_LIST_8  { PTDR_RUN_RESULTS  negResultsArrayInvert };
%apply STRUCT_OUT_LIST_8  { PTDR_RUN_RESULTS  posResultsArray };
%apply STRUCT_OUT_LIST_8  { PTDR_RUN_RESULTS  negResultsArray };
%apply STRUCT_OUT_LIST_2  { PTDR_RUN_RESULTS  resultsArray };
%apply STRUCT_OUT_ONLY_1  { PTDR_RUN_RESULTS  tdrResults };

%apply VALUE_OUT_L_LIST_256 { NS_SINT8 *positivePulseResults };
%apply VALUE_OUT_L_LIST_256 { NS_SINT8 *negativePulseResults };

#-----------------------------------------------------------------------------------
# Other apply statements for the simple parameters.
# These simply tell SWIG to treat these specific parameters as OUTPUT of and
# use one of the standard typemaps.  OUTPUT variables are not passed in but are
# returned in the returnObj "list".
#-----------------------------------------------------------------------------------
%apply NS_UINT  *OUTPUT { NS_UINT *baseline };
%apply NS_UINT8 *OUTPUT { EPL_CABLE_STS_ENUM *cableStatus };
%apply NS_UINT  *OUTPUT { NS_UINT *rawCableLength };
#===================================================================================

%include "epl_tdr.h"		#// TDR API definitions/prototypes

%apply NS_UINT32 *OUTPUT { NS_UINT32 *retNumberOfSeconds };
%apply NS_UINT32 *OUTPUT { NS_UINT32 *retNumberOfNanoSeconds };
%apply NS_UINT   *OUTPUT { NS_UINT   *overflowCount };
%apply NS_UINT   *OUTPUT { NS_UINT   *sequenceId };
%apply NS_UINT8  *OUTPUT { NS_UINT8  *messageType };
%apply NS_UINT   *OUTPUT { NS_UINT   *hashValue };
%apply NS_UINT   *OUTPUT { NS_UINT   *eventBits };
%apply NS_UINT   *OUTPUT { NS_UINT   *riseFlags };
%apply NS_UINT32 *OUTPUT { NS_UINT32 *eventTimeSeconds };
%apply NS_UINT32 *OUTPUT { NS_UINT32 *eventTimeNanoSeconds };
%apply NS_UINT   *OUTPUT { NS_UINT   *eventsMissed };

%apply NS_UINT8  *OUTPUT { PHYMSG_MESSAGE_TYPE_ENUM *messageType };
%apply STRUCT_OUT_ONLY_1 { PHYMSG_MESSAGE *message };

        
%include "epl_1588.h"		#// PTP protocol related API definitions/prototypes

#// Other modules for the DLL
%include "ifGenMAC.h"		#// Interface for generic MAC - Not filled in/used
%include "ifLPT.h"			#// Interface for MDIO LPT definitions/prototypes

#-----------------------------------------------------------------------------------
# Do some typemap adjustments to make things work better for Python
#-----------------------------------------------------------------------------------
%apply NS_UINT *OUTPUT { NS_UINT *length };
#-----------------------------------------------------------------------------------

%include "okMAC.h"			#// Interface/MAC related definitions/prototypes

%include "PTPStack\\datatypes.h"
%include "PTPStack\\dep\\datatypes_dep.h"
%include "PTPStack\\constants.h"
%include "ptpControl.h" 

%include "carrays.i"
%array_class(unsigned char, charArray);