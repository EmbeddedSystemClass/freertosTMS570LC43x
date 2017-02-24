@set PYTHON_INCLUDE="c:\program files\python24\include"
@set PYTHON_LIB="c:\program files\python24\libs\python24.lib"

@set SWIG_FEATURES=-v
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\core
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\interface
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\interface\ALP_OK
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\interface\LPT
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\interface\GenMAC
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\OS\Windows
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\protocol\PTP
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\protocol\PTPStack
@set SWIG_FEATURES=%SWIG_FEATURES% -I..\..\..\protocol\PTPStack\dep
@set SWIG_FEATURES=%SWIG_FEATURES% -D_WIN32
@set SWIG_FEATURES=%SWIG_FEATURES% -o epl_wrap.c

@..\..\..\tools\swig\swig -python epl.i