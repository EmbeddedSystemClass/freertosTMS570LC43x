%insert(runtime) %{
/* Python.h has to appear first */
//#include <Python.h>
#ifdef _DEBUG
    #undef _DEBUG
    #include <python.h>
    #define _DEBUG
#else
    #include <python.h>
#endif
%}

%insert(runtime) "swigrun.swg";         /* SWIG API */
%insert(runtime) "swigerrors.swg";      /* SWIG errors */   
%insert(runtime) "pyhead.swg";          /* Python includes and fixes */
%insert(runtime) "pyerrors.swg";        /* Python errors */
%insert(runtime) "pythreads.swg";       /* Python thread code */
%insert(runtime) "pyapi.swg";           /* Pyton API */
%insert(runtime) "pyrun.swg";           /* Python run-time code */

