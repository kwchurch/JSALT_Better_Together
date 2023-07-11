#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif /* PY_SSIZE_T_CLEAN */
#include "Python.h"
#ifndef Py_PYTHON_H
    #error Python headers needed to compile C extensions, please install development version of Python.
#elif PY_VERSION_HEX < 0x02060000 || (0x03000000 <= PY_VERSION_HEX && PY_VERSION_HEX < 0x03030000)
    #error Cython requires Python 2.6+ or Python 3.3+.
#else
#define CYTHON_ABI "0_29_32"
#define CYTHON_HEX_VERSION 0x001D20F0
#define CYTHON_FUTURE_DIVISION 0
#include <stddef.h>
#ifndef offsetof
  #define offsetof(type, member) ( (size_t) & ((type*)0) -> member )
#endif
#if !defined(WIN32) && !defined(MS_WINDOWS)
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
  #ifndef __fastcall
    #define __fastcall
  #endif
#endif
#ifndef DL_IMPORT
  #define DL_IMPORT(t) t
#endif
#ifndef DL_EXPORT
  #define DL_EXPORT(t) t
#endif
#define __PYX_COMMA ,
#ifndef HAVE_LONG_LONG
  #if PY_VERSION_HEX >= 0x02070000
    #define HAVE_LONG_LONG
  #endif
#endif
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#ifndef Py_HUGE_VAL
  #define Py_HUGE_VAL HUGE_VAL
#endif
#ifdef PYPY_VERSION
  #define CYTHON_COMPILING_IN_PYPY 1
  #define CYTHON_COMPILING_IN_PYSTON 0
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_NOGIL 0
  #undef CYTHON_USE_TYPE_SLOTS
  #define CYTHON_USE_TYPE_SLOTS 0
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #if PY_VERSION_HEX < 0x03050000
    #undef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 0
  #elif !defined(CYTHON_USE_ASYNC_SLOTS)
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #undef CYTHON_USE_UNICODE_INTERNALS
  #define CYTHON_USE_UNICODE_INTERNALS 0
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #undef CYTHON_AVOID_BORROWED_REFS
  #define CYTHON_AVOID_BORROWED_REFS 1
  #undef CYTHON_ASSUME_SAFE_MACROS
  #define CYTHON_ASSUME_SAFE_MACROS 0
  #undef CYTHON_UNPACK_METHODS
  #define CYTHON_UNPACK_METHODS 0
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #undef CYTHON_PEP489_MULTI_PHASE_INIT
  #define CYTHON_PEP489_MULTI_PHASE_INIT 0
  #undef CYTHON_USE_TP_FINALIZE
  #define CYTHON_USE_TP_FINALIZE 0
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC (PYPY_VERSION_HEX >= 0x07030900)
  #endif
#elif defined(PYSTON_VERSION)
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_PYSTON 1
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_NOGIL 0
  #ifndef CYTHON_USE_TYPE_SLOTS
    #define CYTHON_USE_TYPE_SLOTS 1
  #endif
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #undef CYTHON_USE_ASYNC_SLOTS
  #define CYTHON_USE_ASYNC_SLOTS 0
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #ifndef CYTHON_USE_UNICODE_INTERNALS
    #define CYTHON_USE_UNICODE_INTERNALS 1
  #endif
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #ifndef CYTHON_ASSUME_SAFE_MACROS
    #define CYTHON_ASSUME_SAFE_MACROS 1
  #endif
  #ifndef CYTHON_UNPACK_METHODS
    #define CYTHON_UNPACK_METHODS 1
  #endif
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #undef CYTHON_PEP489_MULTI_PHASE_INIT
  #define CYTHON_PEP489_MULTI_PHASE_INIT 0
  #undef CYTHON_USE_TP_FINALIZE
  #define CYTHON_USE_TP_FINALIZE 0
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 0
  #endif
#elif defined(PY_NOGIL)
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_PYSTON 0
  #define CYTHON_COMPILING_IN_CPYTHON 0
  #define CYTHON_COMPILING_IN_NOGIL 1
  #ifndef CYTHON_USE_TYPE_SLOTS
    #define CYTHON_USE_TYPE_SLOTS 1
  #endif
  #undef CYTHON_USE_PYTYPE_LOOKUP
  #define CYTHON_USE_PYTYPE_LOOKUP 0
  #ifndef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #undef CYTHON_USE_PYLIST_INTERNALS
  #define CYTHON_USE_PYLIST_INTERNALS 0
  #ifndef CYTHON_USE_UNICODE_INTERNALS
    #define CYTHON_USE_UNICODE_INTERNALS 1
  #endif
  #undef CYTHON_USE_UNICODE_WRITER
  #define CYTHON_USE_UNICODE_WRITER 0
  #undef CYTHON_USE_PYLONG_INTERNALS
  #define CYTHON_USE_PYLONG_INTERNALS 0
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #ifndef CYTHON_ASSUME_SAFE_MACROS
    #define CYTHON_ASSUME_SAFE_MACROS 1
  #endif
  #ifndef CYTHON_UNPACK_METHODS
    #define CYTHON_UNPACK_METHODS 1
  #endif
  #undef CYTHON_FAST_THREAD_STATE
  #define CYTHON_FAST_THREAD_STATE 0
  #undef CYTHON_FAST_PYCALL
  #define CYTHON_FAST_PYCALL 0
  #ifndef CYTHON_PEP489_MULTI_PHASE_INIT
    #define CYTHON_PEP489_MULTI_PHASE_INIT 1
  #endif
  #ifndef CYTHON_USE_TP_FINALIZE
    #define CYTHON_USE_TP_FINALIZE 1
  #endif
  #undef CYTHON_USE_DICT_VERSIONS
  #define CYTHON_USE_DICT_VERSIONS 0
  #undef CYTHON_USE_EXC_INFO_STACK
  #define CYTHON_USE_EXC_INFO_STACK 0
#else
  #define CYTHON_COMPILING_IN_PYPY 0
  #define CYTHON_COMPILING_IN_PYSTON 0
  #define CYTHON_COMPILING_IN_CPYTHON 1
  #define CYTHON_COMPILING_IN_NOGIL 0
  #ifndef CYTHON_USE_TYPE_SLOTS
    #define CYTHON_USE_TYPE_SLOTS 1
  #endif
  #if PY_VERSION_HEX < 0x02070000
    #undef CYTHON_USE_PYTYPE_LOOKUP
    #define CYTHON_USE_PYTYPE_LOOKUP 0
  #elif !defined(CYTHON_USE_PYTYPE_LOOKUP)
    #define CYTHON_USE_PYTYPE_LOOKUP 1
  #endif
  #if PY_MAJOR_VERSION < 3
    #undef CYTHON_USE_ASYNC_SLOTS
    #define CYTHON_USE_ASYNC_SLOTS 0
  #elif !defined(CYTHON_USE_ASYNC_SLOTS)
    #define CYTHON_USE_ASYNC_SLOTS 1
  #endif
  #if PY_VERSION_HEX < 0x02070000
    #undef CYTHON_USE_PYLONG_INTERNALS
    #define CYTHON_USE_PYLONG_INTERNALS 0
  #elif !defined(CYTHON_USE_PYLONG_INTERNALS)
    #define CYTHON_USE_PYLONG_INTERNALS 1
  #endif
  #ifndef CYTHON_USE_PYLIST_INTERNALS
    #define CYTHON_USE_PYLIST_INTERNALS 1
  #endif
  #ifndef CYTHON_USE_UNICODE_INTERNALS
    #define CYTHON_USE_UNICODE_INTERNALS 1
  #endif
  #if PY_VERSION_HEX < 0x030300F0 || PY_VERSION_HEX >= 0x030B00A2
    #undef CYTHON_USE_UNICODE_WRITER
    #define CYTHON_USE_UNICODE_WRITER 0
  #elif !defined(CYTHON_USE_UNICODE_WRITER)
    #define CYTHON_USE_UNICODE_WRITER 1
  #endif
  #ifndef CYTHON_AVOID_BORROWED_REFS
    #define CYTHON_AVOID_BORROWED_REFS 0
  #endif
  #ifndef CYTHON_ASSUME_SAFE_MACROS
    #define CYTHON_ASSUME_SAFE_MACROS 1
  #endif
  #ifndef CYTHON_UNPACK_METHODS
    #define CYTHON_UNPACK_METHODS 1
  #endif
  #if PY_VERSION_HEX >= 0x030B00A4
    #undef CYTHON_FAST_THREAD_STATE
    #define CYTHON_FAST_THREAD_STATE 0
  #elif !defined(CYTHON_FAST_THREAD_STATE)
    #define CYTHON_FAST_THREAD_STATE 1
  #endif
  #ifndef CYTHON_FAST_PYCALL
    #define CYTHON_FAST_PYCALL (PY_VERSION_HEX < 0x030A0000)
  #endif
  #ifndef CYTHON_PEP489_MULTI_PHASE_INIT
    #define CYTHON_PEP489_MULTI_PHASE_INIT (PY_VERSION_HEX >= 0x03050000)
  #endif
  #ifndef CYTHON_USE_TP_FINALIZE
    #define CYTHON_USE_TP_FINALIZE (PY_VERSION_HEX >= 0x030400a1)
  #endif
  #ifndef CYTHON_USE_DICT_VERSIONS
    #define CYTHON_USE_DICT_VERSIONS (PY_VERSION_HEX >= 0x030600B1)
  #endif
  #if PY_VERSION_HEX >= 0x030B00A4
    #undef CYTHON_USE_EXC_INFO_STACK
    #define CYTHON_USE_EXC_INFO_STACK 0
  #elif !defined(CYTHON_USE_EXC_INFO_STACK)
    #define CYTHON_USE_EXC_INFO_STACK (PY_VERSION_HEX >= 0x030700A3)
  #endif
  #ifndef CYTHON_UPDATE_DESCRIPTOR_DOC
    #define CYTHON_UPDATE_DESCRIPTOR_DOC 1
  #endif
#endif
#if !defined(CYTHON_FAST_PYCCALL)
#define CYTHON_FAST_PYCCALL  (CYTHON_FAST_PYCALL && PY_VERSION_HEX >= 0x030600B1)
#endif
#if CYTHON_USE_PYLONG_INTERNALS
  #if PY_MAJOR_VERSION < 3
    #include "longintrepr.h"
  #endif
  #undef SHIFT
  #undef BASE
  #undef MASK
  #ifdef SIZEOF_VOID_P
    enum { __pyx_check_sizeof_voidp = 1 / (int)(SIZEOF_VOID_P == sizeof(void*)) };
  #endif
#endif
#ifndef __has_attribute
  #define __has_attribute(x) 0
#endif
#ifndef __has_cpp_attribute
  #define __has_cpp_attribute(x) 0
#endif
#ifndef CYTHON_RESTRICT
  #if defined(__GNUC__)
    #define CYTHON_RESTRICT __restrict__
  #elif defined(_MSC_VER) && _MSC_VER >= 1400
    #define CYTHON_RESTRICT __restrict
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_RESTRICT restrict
  #else
    #define CYTHON_RESTRICT
  #endif
#endif
#ifndef CYTHON_UNUSED
# if defined(__GNUC__)
#   if !(defined(__cplusplus)) || (__GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4))
#     define CYTHON_UNUSED __attribute__ ((__unused__))
#   else
#     define CYTHON_UNUSED
#   endif
# elif defined(__ICC) || (defined(__INTEL_COMPILER) && !defined(_MSC_VER))
#   define CYTHON_UNUSED __attribute__ ((__unused__))
# else
#   define CYTHON_UNUSED
# endif
#endif
#ifndef CYTHON_MAYBE_UNUSED_VAR
#  if defined(__cplusplus)
     template<class T> void CYTHON_MAYBE_UNUSED_VAR( const T& ) { }
#  else
#    define CYTHON_MAYBE_UNUSED_VAR(x) (void)(x)
#  endif
#endif
#ifndef CYTHON_NCP_UNUSED
# if CYTHON_COMPILING_IN_CPYTHON
#  define CYTHON_NCP_UNUSED
# else
#  define CYTHON_NCP_UNUSED CYTHON_UNUSED
# endif
#endif
#define __Pyx_void_to_None(void_result) ((void)(void_result), Py_INCREF(Py_None), Py_None)
#ifdef _MSC_VER
    #ifndef _MSC_STDINT_H_
        #if _MSC_VER < 1300
           typedef unsigned char     uint8_t;
           typedef unsigned int      uint32_t;
        #else
           typedef unsigned __int8   uint8_t;
           typedef unsigned __int32  uint32_t;
        #endif
    #endif
#else
   #include <stdint.h>
#endif
#ifndef CYTHON_FALLTHROUGH
  #if defined(__cplusplus) && __cplusplus >= 201103L
    #if __has_cpp_attribute(fallthrough)
      #define CYTHON_FALLTHROUGH [[fallthrough]]
    #elif __has_cpp_attribute(clang::fallthrough)
      #define CYTHON_FALLTHROUGH [[clang::fallthrough]]
    #elif __has_cpp_attribute(gnu::fallthrough)
      #define CYTHON_FALLTHROUGH [[gnu::fallthrough]]
    #endif
  #endif
  #ifndef CYTHON_FALLTHROUGH
    #if __has_attribute(fallthrough)
      #define CYTHON_FALLTHROUGH __attribute__((fallthrough))
    #else
      #define CYTHON_FALLTHROUGH
    #endif
  #endif
  #if defined(__clang__ ) && defined(__apple_build_version__)
    #if __apple_build_version__ < 7000000
      #undef  CYTHON_FALLTHROUGH
      #define CYTHON_FALLTHROUGH
    #endif
  #endif
#endif

#ifndef CYTHON_INLINE
  #if defined(__clang__)
    #define CYTHON_INLINE __inline__ __attribute__ ((__unused__))
  #elif defined(__GNUC__)
    #define CYTHON_INLINE __inline__
  #elif defined(_MSC_VER)
    #define CYTHON_INLINE __inline
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_INLINE inline
  #else
    #define CYTHON_INLINE
  #endif
#endif

#if CYTHON_COMPILING_IN_PYPY && PY_VERSION_HEX < 0x02070600 && !defined(Py_OptimizeFlag)
  #define Py_OptimizeFlag 0
#endif
#define __PYX_BUILD_PY_SSIZE_T "n"
#define CYTHON_FORMAT_SSIZE_T "z"
#if PY_MAJOR_VERSION < 3
  #define __Pyx_BUILTIN_MODULE_NAME "__builtin__"
  #define __Pyx_PyCode_New(a, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_New(a+k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
  #define __Pyx_DefaultClassType PyClass_Type
#else
  #define __Pyx_BUILTIN_MODULE_NAME "builtins"
  #define __Pyx_DefaultClassType PyType_Type
#if PY_VERSION_HEX >= 0x030B00A1
    static CYTHON_INLINE PyCodeObject* __Pyx_PyCode_New(int a, int k, int l, int s, int f,
                                                    PyObject *code, PyObject *c, PyObject* n, PyObject *v,
                                                    PyObject *fv, PyObject *cell, PyObject* fn,
                                                    PyObject *name, int fline, PyObject *lnos) {
        PyObject *kwds=NULL, *argcount=NULL, *posonlyargcount=NULL, *kwonlyargcount=NULL;
        PyObject *nlocals=NULL, *stacksize=NULL, *flags=NULL, *replace=NULL, *call_result=NULL, *empty=NULL;
        const char *fn_cstr=NULL;
        const char *name_cstr=NULL;
        PyCodeObject* co=NULL;
        PyObject *type, *value, *traceback;
        PyErr_Fetch(&type, &value, &traceback);
        if (!(kwds=PyDict_New())) goto end;
        if (!(argcount=PyLong_FromLong(a))) goto end;
        if (PyDict_SetItemString(kwds, "co_argcount", argcount) != 0) goto end;
        if (!(posonlyargcount=PyLong_FromLong(0))) goto end;
        if (PyDict_SetItemString(kwds, "co_posonlyargcount", posonlyargcount) != 0) goto end;
        if (!(kwonlyargcount=PyLong_FromLong(k))) goto end;
        if (PyDict_SetItemString(kwds, "co_kwonlyargcount", kwonlyargcount) != 0) goto end;
        if (!(nlocals=PyLong_FromLong(l))) goto end;
        if (PyDict_SetItemString(kwds, "co_nlocals", nlocals) != 0) goto end;
        if (!(stacksize=PyLong_FromLong(s))) goto end;
        if (PyDict_SetItemString(kwds, "co_stacksize", stacksize) != 0) goto end;
        if (!(flags=PyLong_FromLong(f))) goto end;
        if (PyDict_SetItemString(kwds, "co_flags", flags) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_code", code) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_consts", c) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_names", n) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_varnames", v) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_freevars", fv) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_cellvars", cell) != 0) goto end;
        if (PyDict_SetItemString(kwds, "co_linetable", lnos) != 0) goto end;
        if (!(fn_cstr=PyUnicode_AsUTF8AndSize(fn, NULL))) goto end;
        if (!(name_cstr=PyUnicode_AsUTF8AndSize(name, NULL))) goto end;
        if (!(co = PyCode_NewEmpty(fn_cstr, name_cstr, fline))) goto end;
        if (!(replace = PyObject_GetAttrString((PyObject*)co, "replace"))) goto cleanup_code_too;
        if (!(empty = PyTuple_New(0))) goto cleanup_code_too; // unfortunately __pyx_empty_tuple isn't available here
        if (!(call_result = PyObject_Call(replace, empty, kwds))) goto cleanup_code_too;
        Py_XDECREF((PyObject*)co);
        co = (PyCodeObject*)call_result;
        call_result = NULL;
        if (0) {
            cleanup_code_too:
            Py_XDECREF((PyObject*)co);
            co = NULL;
        }
        end:
        Py_XDECREF(kwds);
        Py_XDECREF(argcount);
        Py_XDECREF(posonlyargcount);
        Py_XDECREF(kwonlyargcount);
        Py_XDECREF(nlocals);
        Py_XDECREF(stacksize);
        Py_XDECREF(replace);
        Py_XDECREF(call_result);
        Py_XDECREF(empty);
        if (type) {
            PyErr_Restore(type, value, traceback);
        }
        return co;
    }
#else
  #define __Pyx_PyCode_New(a, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_New(a, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#endif
  #define __Pyx_DefaultClassType PyType_Type
#endif
#ifndef Py_TPFLAGS_CHECKTYPES
  #define Py_TPFLAGS_CHECKTYPES 0
#endif
#ifndef Py_TPFLAGS_HAVE_INDEX
  #define Py_TPFLAGS_HAVE_INDEX 0
#endif
#ifndef Py_TPFLAGS_HAVE_NEWBUFFER
  #define Py_TPFLAGS_HAVE_NEWBUFFER 0
#endif
#ifndef Py_TPFLAGS_HAVE_FINALIZE
  #define Py_TPFLAGS_HAVE_FINALIZE 0
#endif
#ifndef METH_STACKLESS
  #define METH_STACKLESS 0
#endif
#if PY_VERSION_HEX <= 0x030700A3 || !defined(METH_FASTCALL)
  #ifndef METH_FASTCALL
     #define METH_FASTCALL 0x80
  #endif
  typedef PyObject *(*__Pyx_PyCFunctionFast) (PyObject *self, PyObject *const *args, Py_ssize_t nargs);
  typedef PyObject *(*__Pyx_PyCFunctionFastWithKeywords) (PyObject *self, PyObject *const *args,
                                                          Py_ssize_t nargs, PyObject *kwnames);
#else
  #define __Pyx_PyCFunctionFast _PyCFunctionFast
  #define __Pyx_PyCFunctionFastWithKeywords _PyCFunctionFastWithKeywords
#endif
#if CYTHON_FAST_PYCCALL
#define __Pyx_PyFastCFunction_Check(func)\
    ((PyCFunction_Check(func) && (METH_FASTCALL == (PyCFunction_GET_FLAGS(func) & ~(METH_CLASS | METH_STATIC | METH_COEXIST | METH_KEYWORDS | METH_STACKLESS)))))
#else
#define __Pyx_PyFastCFunction_Check(func) 0
#endif
#if CYTHON_COMPILING_IN_PYPY && !defined(PyObject_Malloc)
  #define PyObject_Malloc(s)   PyMem_Malloc(s)
  #define PyObject_Free(p)     PyMem_Free(p)
  #define PyObject_Realloc(p)  PyMem_Realloc(p)
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030400A1
  #define PyMem_RawMalloc(n)           PyMem_Malloc(n)
  #define PyMem_RawRealloc(p, n)       PyMem_Realloc(p, n)
  #define PyMem_RawFree(p)             PyMem_Free(p)
#endif
#if CYTHON_COMPILING_IN_PYSTON
  #define __Pyx_PyCode_HasFreeVars(co)  PyCode_HasFreeVars(co)
  #define __Pyx_PyFrame_SetLineNumber(frame, lineno) PyFrame_SetLineNumber(frame, lineno)
#else
  #define __Pyx_PyCode_HasFreeVars(co)  (PyCode_GetNumFree(co) > 0)
  #define __Pyx_PyFrame_SetLineNumber(frame, lineno)  (frame)->f_lineno = (lineno)
#endif
#if !CYTHON_FAST_THREAD_STATE || PY_VERSION_HEX < 0x02070000
  #define __Pyx_PyThreadState_Current PyThreadState_GET()
#elif PY_VERSION_HEX >= 0x03060000
  #define __Pyx_PyThreadState_Current _PyThreadState_UncheckedGet()
#elif PY_VERSION_HEX >= 0x03000000
  #define __Pyx_PyThreadState_Current PyThreadState_GET()
#else
  #define __Pyx_PyThreadState_Current _PyThreadState_Current
#endif
#if PY_VERSION_HEX < 0x030700A2 && !defined(PyThread_tss_create) && !defined(Py_tss_NEEDS_INIT)
#include "pythread.h"
#define Py_tss_NEEDS_INIT 0
typedef int Py_tss_t;
static CYTHON_INLINE int PyThread_tss_create(Py_tss_t *key) {
  *key = PyThread_create_key();
  return 0;
}
static CYTHON_INLINE Py_tss_t * PyThread_tss_alloc(void) {
  Py_tss_t *key = (Py_tss_t *)PyObject_Malloc(sizeof(Py_tss_t));
  *key = Py_tss_NEEDS_INIT;
  return key;
}
static CYTHON_INLINE void PyThread_tss_free(Py_tss_t *key) {
  PyObject_Free(key);
}
static CYTHON_INLINE int PyThread_tss_is_created(Py_tss_t *key) {
  return *key != Py_tss_NEEDS_INIT;
}
static CYTHON_INLINE void PyThread_tss_delete(Py_tss_t *key) {
  PyThread_delete_key(*key);
  *key = Py_tss_NEEDS_INIT;
}
static CYTHON_INLINE int PyThread_tss_set(Py_tss_t *key, void *value) {
  return PyThread_set_key_value(*key, value);
}
static CYTHON_INLINE void * PyThread_tss_get(Py_tss_t *key) {
  return PyThread_get_key_value(*key);
}
#endif
#if CYTHON_COMPILING_IN_CPYTHON || defined(_PyDict_NewPresized)
#define __Pyx_PyDict_NewPresized(n)  ((n <= 8) ? PyDict_New() : _PyDict_NewPresized(n))
#else
#define __Pyx_PyDict_NewPresized(n)  PyDict_New()
#endif
#if PY_MAJOR_VERSION >= 3 || CYTHON_FUTURE_DIVISION
  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_TrueDivide(x,y)
  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceTrueDivide(x,y)
#else
  #define __Pyx_PyNumber_Divide(x,y)         PyNumber_Divide(x,y)
  #define __Pyx_PyNumber_InPlaceDivide(x,y)  PyNumber_InPlaceDivide(x,y)
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030500A1 && CYTHON_USE_UNICODE_INTERNALS
#define __Pyx_PyDict_GetItemStr(dict, name)  _PyDict_GetItem_KnownHash(dict, name, ((PyASCIIObject *) name)->hash)
#else
#define __Pyx_PyDict_GetItemStr(dict, name)  PyDict_GetItem(dict, name)
#endif
#if PY_VERSION_HEX > 0x03030000 && defined(PyUnicode_KIND)
  #define CYTHON_PEP393_ENABLED 1
  #if defined(PyUnicode_IS_READY)
  #define __Pyx_PyUnicode_READY(op)       (likely(PyUnicode_IS_READY(op)) ?\
                                              0 : _PyUnicode_Ready((PyObject *)(op)))
  #else
  #define __Pyx_PyUnicode_READY(op)       (0)
  #endif
  #define __Pyx_PyUnicode_GET_LENGTH(u)   PyUnicode_GET_LENGTH(u)
  #define __Pyx_PyUnicode_READ_CHAR(u, i) PyUnicode_READ_CHAR(u, i)
  #define __Pyx_PyUnicode_MAX_CHAR_VALUE(u)   PyUnicode_MAX_CHAR_VALUE(u)
  #define __Pyx_PyUnicode_KIND(u)         PyUnicode_KIND(u)
  #define __Pyx_PyUnicode_DATA(u)         PyUnicode_DATA(u)
  #define __Pyx_PyUnicode_READ(k, d, i)   PyUnicode_READ(k, d, i)
  #define __Pyx_PyUnicode_WRITE(k, d, i, ch)  PyUnicode_WRITE(k, d, i, ch)
  #if defined(PyUnicode_IS_READY) && defined(PyUnicode_GET_SIZE)
  #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x03090000
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != (likely(PyUnicode_IS_READY(u)) ? PyUnicode_GET_LENGTH(u) : ((PyCompactUnicodeObject *)(u))->wstr_length))
  #else
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != (likely(PyUnicode_IS_READY(u)) ? PyUnicode_GET_LENGTH(u) : PyUnicode_GET_SIZE(u)))
  #endif
  #else
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != PyUnicode_GET_LENGTH(u))
  #endif
#else
  #define CYTHON_PEP393_ENABLED 0
  #define PyUnicode_1BYTE_KIND  1
  #define PyUnicode_2BYTE_KIND  2
  #define PyUnicode_4BYTE_KIND  4
  #define __Pyx_PyUnicode_READY(op)       (0)
  #define __Pyx_PyUnicode_GET_LENGTH(u)   PyUnicode_GET_SIZE(u)
  #define __Pyx_PyUnicode_READ_CHAR(u, i) ((Py_UCS4)(PyUnicode_AS_UNICODE(u)[i]))
  #define __Pyx_PyUnicode_MAX_CHAR_VALUE(u)   ((sizeof(Py_UNICODE) == 2) ? 65535 : 1114111)
  #define __Pyx_PyUnicode_KIND(u)         (sizeof(Py_UNICODE))
  #define __Pyx_PyUnicode_DATA(u)         ((void*)PyUnicode_AS_UNICODE(u))
  #define __Pyx_PyUnicode_READ(k, d, i)   ((void)(k), (Py_UCS4)(((Py_UNICODE*)d)[i]))
  #define __Pyx_PyUnicode_WRITE(k, d, i, ch)  (((void)(k)), ((Py_UNICODE*)d)[i] = ch)
  #define __Pyx_PyUnicode_IS_TRUE(u)      (0 != PyUnicode_GET_SIZE(u))
#endif
#if CYTHON_COMPILING_IN_PYPY
  #define __Pyx_PyUnicode_Concat(a, b)      PyNumber_Add(a, b)
  #define __Pyx_PyUnicode_ConcatSafe(a, b)  PyNumber_Add(a, b)
#else
  #define __Pyx_PyUnicode_Concat(a, b)      PyUnicode_Concat(a, b)
  #define __Pyx_PyUnicode_ConcatSafe(a, b)  ((unlikely((a) == Py_None) || unlikely((b) == Py_None)) ?\
      PyNumber_Add(a, b) : __Pyx_PyUnicode_Concat(a, b))
#endif
#if CYTHON_COMPILING_IN_PYPY && !defined(PyUnicode_Contains)
  #define PyUnicode_Contains(u, s)  PySequence_Contains(u, s)
#endif
#if CYTHON_COMPILING_IN_PYPY && !defined(PyByteArray_Check)
  #define PyByteArray_Check(obj)  PyObject_TypeCheck(obj, &PyByteArray_Type)
#endif
#if CYTHON_COMPILING_IN_PYPY && !defined(PyObject_Format)
  #define PyObject_Format(obj, fmt)  PyObject_CallMethod(obj, "__format__", "O", fmt)
#endif
#define __Pyx_PyString_FormatSafe(a, b)   ((unlikely((a) == Py_None || (PyString_Check(b) && !PyString_CheckExact(b)))) ? PyNumber_Remainder(a, b) : __Pyx_PyString_Format(a, b))
#define __Pyx_PyUnicode_FormatSafe(a, b)  ((unlikely((a) == Py_None || (PyUnicode_Check(b) && !PyUnicode_CheckExact(b)))) ? PyNumber_Remainder(a, b) : PyUnicode_Format(a, b))
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyString_Format(a, b)  PyUnicode_Format(a, b)
#else
  #define __Pyx_PyString_Format(a, b)  PyString_Format(a, b)
#endif
#if PY_MAJOR_VERSION < 3 && !defined(PyObject_ASCII)
  #define PyObject_ASCII(o)            PyObject_Repr(o)
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyBaseString_Type            PyUnicode_Type
  #define PyStringObject               PyUnicodeObject
  #define PyString_Type                PyUnicode_Type
  #define PyString_Check               PyUnicode_Check
  #define PyString_CheckExact          PyUnicode_CheckExact
#ifndef PyObject_Unicode
  #define PyObject_Unicode             PyObject_Str
#endif
#endif
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyBaseString_Check(obj) PyUnicode_Check(obj)
  #define __Pyx_PyBaseString_CheckExact(obj) PyUnicode_CheckExact(obj)
#else
  #define __Pyx_PyBaseString_Check(obj) (PyString_Check(obj) || PyUnicode_Check(obj))
  #define __Pyx_PyBaseString_CheckExact(obj) (PyString_CheckExact(obj) || PyUnicode_CheckExact(obj))
#endif
#ifndef PySet_CheckExact
  #define PySet_CheckExact(obj)        (Py_TYPE(obj) == &PySet_Type)
#endif
#if PY_VERSION_HEX >= 0x030900A4
  #define __Pyx_SET_REFCNT(obj, refcnt) Py_SET_REFCNT(obj, refcnt)
  #define __Pyx_SET_SIZE(obj, size) Py_SET_SIZE(obj, size)
#else
  #define __Pyx_SET_REFCNT(obj, refcnt) Py_REFCNT(obj) = (refcnt)
  #define __Pyx_SET_SIZE(obj, size) Py_SIZE(obj) = (size)
#endif
#if CYTHON_ASSUME_SAFE_MACROS
  #define __Pyx_PySequence_SIZE(seq)  Py_SIZE(seq)
#else
  #define __Pyx_PySequence_SIZE(seq)  PySequence_Size(seq)
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyIntObject                  PyLongObject
  #define PyInt_Type                   PyLong_Type
  #define PyInt_Check(op)              PyLong_Check(op)
  #define PyInt_CheckExact(op)         PyLong_CheckExact(op)
  #define PyInt_FromString             PyLong_FromString
  #define PyInt_FromUnicode            PyLong_FromUnicode
  #define PyInt_FromLong               PyLong_FromLong
  #define PyInt_FromSize_t             PyLong_FromSize_t
  #define PyInt_FromSsize_t            PyLong_FromSsize_t
  #define PyInt_AsLong                 PyLong_AsLong
  #define PyInt_AS_LONG                PyLong_AS_LONG
  #define PyInt_AsSsize_t              PyLong_AsSsize_t
  #define PyInt_AsUnsignedLongMask     PyLong_AsUnsignedLongMask
  #define PyInt_AsUnsignedLongLongMask PyLong_AsUnsignedLongLongMask
  #define PyNumber_Int                 PyNumber_Long
#endif
#if PY_MAJOR_VERSION >= 3
  #define PyBoolObject                 PyLongObject
#endif
#if PY_MAJOR_VERSION >= 3 && CYTHON_COMPILING_IN_PYPY
  #ifndef PyUnicode_InternFromString
    #define PyUnicode_InternFromString(s) PyUnicode_FromString(s)
  #endif
#endif
#if PY_VERSION_HEX < 0x030200A4
  typedef long Py_hash_t;
  #define __Pyx_PyInt_FromHash_t PyInt_FromLong
  #define __Pyx_PyInt_AsHash_t   __Pyx_PyIndex_AsHash_t
#else
  #define __Pyx_PyInt_FromHash_t PyInt_FromSsize_t
  #define __Pyx_PyInt_AsHash_t   __Pyx_PyIndex_AsSsize_t
#endif
#if PY_MAJOR_VERSION >= 3
  #define __Pyx_PyMethod_New(func, self, klass) ((self) ? ((void)(klass), PyMethod_New(func, self)) : __Pyx_NewRef(func))
#else
  #define __Pyx_PyMethod_New(func, self, klass) PyMethod_New(func, self, klass)
#endif
#if CYTHON_USE_ASYNC_SLOTS
  #if PY_VERSION_HEX >= 0x030500B1
    #define __Pyx_PyAsyncMethodsStruct PyAsyncMethods
    #define __Pyx_PyType_AsAsync(obj) (Py_TYPE(obj)->tp_as_async)
  #else
    #define __Pyx_PyType_AsAsync(obj) ((__Pyx_PyAsyncMethodsStruct*) (Py_TYPE(obj)->tp_reserved))
  #endif
#else
  #define __Pyx_PyType_AsAsync(obj) NULL
#endif
#ifndef __Pyx_PyAsyncMethodsStruct
    typedef struct {
        unaryfunc am_await;
        unaryfunc am_aiter;
        unaryfunc am_anext;
    } __Pyx_PyAsyncMethodsStruct;
#endif

#if defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)
  #if !defined(_USE_MATH_DEFINES)
    #define _USE_MATH_DEFINES
  #endif
#endif
#include <math.h>
#ifdef NAN
#define __PYX_NAN() ((float) NAN)
#else
static CYTHON_INLINE float __PYX_NAN() {
  float value;
  memset(&value, 0xFF, sizeof(value));
  return value;
}
#endif
#if defined(__CYGWIN__) && defined(_LDBL_EQ_DBL)
#define __Pyx_truncl trunc
#else
#define __Pyx_truncl truncl
#endif

#define __PYX_MARK_ERR_POS(f_index, lineno) \
    { __pyx_filename = __pyx_f[f_index]; (void)__pyx_filename; __pyx_lineno = lineno; (void)__pyx_lineno; __pyx_clineno = __LINE__; (void)__pyx_clineno; }
#define __PYX_ERR(f_index, lineno, Ln_error) \
    { __PYX_MARK_ERR_POS(f_index, lineno) goto Ln_error; }

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

#define __PYX_HAVE__dict_to_embedding
#define __PYX_HAVE_API__dict_to_embedding
/* Early includes */
#ifdef _OPENMP
#include <omp.h>
#endif /* _OPENMP */

#if defined(PYREX_WITHOUT_ASSERTIONS) && !defined(CYTHON_WITHOUT_ASSERTIONS)
#define CYTHON_WITHOUT_ASSERTIONS
#endif

typedef struct {PyObject **p; const char *s; const Py_ssize_t n; const char* encoding;
                const char is_unicode; const char is_str; const char intern; } __Pyx_StringTabEntry;

#define __PYX_DEFAULT_STRING_ENCODING_IS_ASCII 0
#define __PYX_DEFAULT_STRING_ENCODING_IS_UTF8 0
#define __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT (PY_MAJOR_VERSION >= 3 && __PYX_DEFAULT_STRING_ENCODING_IS_UTF8)
#define __PYX_DEFAULT_STRING_ENCODING ""
#define __Pyx_PyObject_FromString __Pyx_PyBytes_FromString
#define __Pyx_PyObject_FromStringAndSize __Pyx_PyBytes_FromStringAndSize
#define __Pyx_uchar_cast(c) ((unsigned char)c)
#define __Pyx_long_cast(x) ((long)x)
#define __Pyx_fits_Py_ssize_t(v, type, is_signed)  (\
    (sizeof(type) < sizeof(Py_ssize_t))  ||\
    (sizeof(type) > sizeof(Py_ssize_t) &&\
          likely(v < (type)PY_SSIZE_T_MAX ||\
                 v == (type)PY_SSIZE_T_MAX)  &&\
          (!is_signed || likely(v > (type)PY_SSIZE_T_MIN ||\
                                v == (type)PY_SSIZE_T_MIN)))  ||\
    (sizeof(type) == sizeof(Py_ssize_t) &&\
          (is_signed || likely(v < (type)PY_SSIZE_T_MAX ||\
                               v == (type)PY_SSIZE_T_MAX)))  )
static CYTHON_INLINE int __Pyx_is_valid_index(Py_ssize_t i, Py_ssize_t limit) {
    return (size_t) i < (size_t) limit;
}
#if defined (__cplusplus) && __cplusplus >= 201103L
    #include <cstdlib>
    #define __Pyx_sst_abs(value) std::abs(value)
#elif SIZEOF_INT >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) abs(value)
#elif SIZEOF_LONG >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) labs(value)
#elif defined (_MSC_VER)
    #define __Pyx_sst_abs(value) ((Py_ssize_t)_abs64(value))
#elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define __Pyx_sst_abs(value) llabs(value)
#elif defined (__GNUC__)
    #define __Pyx_sst_abs(value) __builtin_llabs(value)
#else
    #define __Pyx_sst_abs(value) ((value<0) ? -value : value)
#endif
static CYTHON_INLINE const char* __Pyx_PyObject_AsString(PyObject*);
static CYTHON_INLINE const char* __Pyx_PyObject_AsStringAndSize(PyObject*, Py_ssize_t* length);
#define __Pyx_PyByteArray_FromString(s) PyByteArray_FromStringAndSize((const char*)s, strlen((const char*)s))
#define __Pyx_PyByteArray_FromStringAndSize(s, l) PyByteArray_FromStringAndSize((const char*)s, l)
#define __Pyx_PyBytes_FromString        PyBytes_FromString
#define __Pyx_PyBytes_FromStringAndSize PyBytes_FromStringAndSize
static CYTHON_INLINE PyObject* __Pyx_PyUnicode_FromString(const char*);
#if PY_MAJOR_VERSION < 3
    #define __Pyx_PyStr_FromString        __Pyx_PyBytes_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyBytes_FromStringAndSize
#else
    #define __Pyx_PyStr_FromString        __Pyx_PyUnicode_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyUnicode_FromStringAndSize
#endif
#define __Pyx_PyBytes_AsWritableString(s)     ((char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsWritableSString(s)    ((signed char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsWritableUString(s)    ((unsigned char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsString(s)     ((const char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsSString(s)    ((const signed char*) PyBytes_AS_STRING(s))
#define __Pyx_PyBytes_AsUString(s)    ((const unsigned char*) PyBytes_AS_STRING(s))
#define __Pyx_PyObject_AsWritableString(s)    ((char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsWritableSString(s)    ((signed char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsWritableUString(s)    ((unsigned char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsSString(s)    ((const signed char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsUString(s)    ((const unsigned char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_FromCString(s)  __Pyx_PyObject_FromString((const char*)s)
#define __Pyx_PyBytes_FromCString(s)   __Pyx_PyBytes_FromString((const char*)s)
#define __Pyx_PyByteArray_FromCString(s)   __Pyx_PyByteArray_FromString((const char*)s)
#define __Pyx_PyStr_FromCString(s)     __Pyx_PyStr_FromString((const char*)s)
#define __Pyx_PyUnicode_FromCString(s) __Pyx_PyUnicode_FromString((const char*)s)
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const Py_UNICODE *u) {
    const Py_UNICODE *u_end = u;
    while (*u_end++) ;
    return (size_t)(u_end - u - 1);
}
#define __Pyx_PyUnicode_FromUnicode(u)       PyUnicode_FromUnicode(u, __Pyx_Py_UNICODE_strlen(u))
#define __Pyx_PyUnicode_FromUnicodeAndLength PyUnicode_FromUnicode
#define __Pyx_PyUnicode_AsUnicode            PyUnicode_AsUnicode
#define __Pyx_NewRef(obj) (Py_INCREF(obj), obj)
#define __Pyx_Owned_Py_None(b) __Pyx_NewRef(Py_None)
static CYTHON_INLINE PyObject * __Pyx_PyBool_FromLong(long b);
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject*);
static CYTHON_INLINE int __Pyx_PyObject_IsTrueAndDecref(PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyNumber_IntOrLong(PyObject* x);
#define __Pyx_PySequence_Tuple(obj)\
    (likely(PyTuple_CheckExact(obj)) ? __Pyx_NewRef(obj) : PySequence_Tuple(obj))
static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject*);
static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t);
static CYTHON_INLINE Py_hash_t __Pyx_PyIndex_AsHash_t(PyObject*);
#if CYTHON_ASSUME_SAFE_MACROS
#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))
#else
#define __pyx_PyFloat_AsDouble(x) PyFloat_AsDouble(x)
#endif
#define __pyx_PyFloat_AsFloat(x) ((float) __pyx_PyFloat_AsDouble(x))
#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyNumber_Int(x) (PyLong_CheckExact(x) ? __Pyx_NewRef(x) : PyNumber_Long(x))
#else
#define __Pyx_PyNumber_Int(x) (PyInt_CheckExact(x) ? __Pyx_NewRef(x) : PyNumber_Int(x))
#endif
#define __Pyx_PyNumber_Float(x) (PyFloat_CheckExact(x) ? __Pyx_NewRef(x) : PyNumber_Float(x))
#if PY_MAJOR_VERSION < 3 && __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
static int __Pyx_sys_getdefaultencoding_not_ascii;
static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    PyObject* ascii_chars_u = NULL;
    PyObject* ascii_chars_b = NULL;
    const char* default_encoding_c;
    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    if (strcmp(default_encoding_c, "ascii") == 0) {
        __Pyx_sys_getdefaultencoding_not_ascii = 0;
    } else {
        char ascii_chars[128];
        int c;
        for (c = 0; c < 128; c++) {
            ascii_chars[c] = c;
        }
        __Pyx_sys_getdefaultencoding_not_ascii = 1;
        ascii_chars_u = PyUnicode_DecodeASCII(ascii_chars, 128, NULL);
        if (!ascii_chars_u) goto bad;
        ascii_chars_b = PyUnicode_AsEncodedString(ascii_chars_u, default_encoding_c, NULL);
        if (!ascii_chars_b || !PyBytes_Check(ascii_chars_b) || memcmp(ascii_chars, PyBytes_AS_STRING(ascii_chars_b), 128) != 0) {
            PyErr_Format(
                PyExc_ValueError,
                "This module compiled with c_string_encoding=ascii, but default encoding '%.200s' is not a superset of ascii.",
                default_encoding_c);
            goto bad;
        }
        Py_DECREF(ascii_chars_u);
        Py_DECREF(ascii_chars_b);
    }
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    Py_XDECREF(ascii_chars_u);
    Py_XDECREF(ascii_chars_b);
    return -1;
}
#endif
#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT && PY_MAJOR_VERSION >= 3
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_DecodeUTF8(c_str, size, NULL)
#else
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_Decode(c_str, size, __PYX_DEFAULT_STRING_ENCODING, NULL)
#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT
static char* __PYX_DEFAULT_STRING_ENCODING;
static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    char* default_encoding_c;
    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) (const char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    __PYX_DEFAULT_STRING_ENCODING = (char*) malloc(strlen(default_encoding_c) + 1);
    if (!__PYX_DEFAULT_STRING_ENCODING) goto bad;
    strcpy(__PYX_DEFAULT_STRING_ENCODING, default_encoding_c);
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    return -1;
}
#endif
#endif


/* Test for GCC > 2.95 */
#if defined(__GNUC__)     && (__GNUC__ > 2 || (__GNUC__ == 2 && (__GNUC_MINOR__ > 95)))
  #define likely(x)   __builtin_expect(!!(x), 1)
  #define unlikely(x) __builtin_expect(!!(x), 0)
#else /* !__GNUC__ or GCC < 2.95 */
  #define likely(x)   (x)
  #define unlikely(x) (x)
#endif /* __GNUC__ */
static CYTHON_INLINE void __Pyx_pretend_to_initialize(void* ptr) { (void)ptr; }

static PyObject *__pyx_m = NULL;
static PyObject *__pyx_d;
static PyObject *__pyx_b;
static PyObject *__pyx_cython_runtime = NULL;
static PyObject *__pyx_empty_tuple;
static PyObject *__pyx_empty_bytes;
static PyObject *__pyx_empty_unicode;
static int __pyx_lineno;
static int __pyx_clineno = 0;
static const char * __pyx_cfilenm= __FILE__;
static const char *__pyx_filename;


static const char *__pyx_f[] = {
  "dict_to_embedding.py",
};

/*--- Type declarations ---*/

/* --- Runtime support code (head) --- */
/* Refnanny.proto */
#ifndef CYTHON_REFNANNY
  #define CYTHON_REFNANNY 0
#endif
#if CYTHON_REFNANNY
  typedef struct {
    void (*INCREF)(void*, PyObject*, int);
    void (*DECREF)(void*, PyObject*, int);
    void (*GOTREF)(void*, PyObject*, int);
    void (*GIVEREF)(void*, PyObject*, int);
    void* (*SetupContext)(const char*, int, const char*);
    void (*FinishContext)(void**);
  } __Pyx_RefNannyAPIStruct;
  static __Pyx_RefNannyAPIStruct *__Pyx_RefNanny = NULL;
  static __Pyx_RefNannyAPIStruct *__Pyx_RefNannyImportAPI(const char *modname);
  #define __Pyx_RefNannyDeclarations void *__pyx_refnanny = NULL;
#ifdef WITH_THREAD
  #define __Pyx_RefNannySetupContext(name, acquire_gil)\
          if (acquire_gil) {\
              PyGILState_STATE __pyx_gilstate_save = PyGILState_Ensure();\
              __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), __LINE__, __FILE__);\
              PyGILState_Release(__pyx_gilstate_save);\
          } else {\
              __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), __LINE__, __FILE__);\
          }
#else
  #define __Pyx_RefNannySetupContext(name, acquire_gil)\
          __pyx_refnanny = __Pyx_RefNanny->SetupContext((name), __LINE__, __FILE__)
#endif
  #define __Pyx_RefNannyFinishContext()\
          __Pyx_RefNanny->FinishContext(&__pyx_refnanny)
  #define __Pyx_INCREF(r)  __Pyx_RefNanny->INCREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_DECREF(r)  __Pyx_RefNanny->DECREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_GOTREF(r)  __Pyx_RefNanny->GOTREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_GIVEREF(r) __Pyx_RefNanny->GIVEREF(__pyx_refnanny, (PyObject *)(r), __LINE__)
  #define __Pyx_XINCREF(r)  do { if((r) != NULL) {__Pyx_INCREF(r); }} while(0)
  #define __Pyx_XDECREF(r)  do { if((r) != NULL) {__Pyx_DECREF(r); }} while(0)
  #define __Pyx_XGOTREF(r)  do { if((r) != NULL) {__Pyx_GOTREF(r); }} while(0)
  #define __Pyx_XGIVEREF(r) do { if((r) != NULL) {__Pyx_GIVEREF(r);}} while(0)
#else
  #define __Pyx_RefNannyDeclarations
  #define __Pyx_RefNannySetupContext(name, acquire_gil)
  #define __Pyx_RefNannyFinishContext()
  #define __Pyx_INCREF(r) Py_INCREF(r)
  #define __Pyx_DECREF(r) Py_DECREF(r)
  #define __Pyx_GOTREF(r)
  #define __Pyx_GIVEREF(r)
  #define __Pyx_XINCREF(r) Py_XINCREF(r)
  #define __Pyx_XDECREF(r) Py_XDECREF(r)
  #define __Pyx_XGOTREF(r)
  #define __Pyx_XGIVEREF(r)
#endif
#define __Pyx_XDECREF_SET(r, v) do {\
        PyObject *tmp = (PyObject *) r;\
        r = v; __Pyx_XDECREF(tmp);\
    } while (0)
#define __Pyx_DECREF_SET(r, v) do {\
        PyObject *tmp = (PyObject *) r;\
        r = v; __Pyx_DECREF(tmp);\
    } while (0)
#define __Pyx_CLEAR(r)    do { PyObject* tmp = ((PyObject*)(r)); r = NULL; __Pyx_DECREF(tmp);} while(0)
#define __Pyx_XCLEAR(r)   do { if((r) != NULL) {PyObject* tmp = ((PyObject*)(r)); r = NULL; __Pyx_DECREF(tmp);}} while(0)

/* PyObjectGetAttrStr.proto */
#if CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PyObject* __Pyx_PyObject_GetAttrStr(PyObject* obj, PyObject* attr_name);
#else
#define __Pyx_PyObject_GetAttrStr(o,n) PyObject_GetAttr(o,n)
#endif

/* GetBuiltinName.proto */
static PyObject *__Pyx_GetBuiltinName(PyObject *name);

/* RaiseArgTupleInvalid.proto */
static void __Pyx_RaiseArgtupleInvalid(const char* func_name, int exact,
    Py_ssize_t num_min, Py_ssize_t num_max, Py_ssize_t num_found);

/* RaiseDoubleKeywords.proto */
static void __Pyx_RaiseDoubleKeywordsError(const char* func_name, PyObject* kw_name);

/* ParseKeywords.proto */
static int __Pyx_ParseOptionalKeywords(PyObject *kwds, PyObject **argnames[],\
    PyObject *kwds2, PyObject *values[], Py_ssize_t num_pos_args,\
    const char* function_name);

/* PyCFunctionFastCall.proto */
#if CYTHON_FAST_PYCCALL
static CYTHON_INLINE PyObject *__Pyx_PyCFunction_FastCall(PyObject *func, PyObject **args, Py_ssize_t nargs);
#else
#define __Pyx_PyCFunction_FastCall(func, args, nargs)  (assert(0), NULL)
#endif

/* PyFunctionFastCall.proto */
#if CYTHON_FAST_PYCALL
#define __Pyx_PyFunction_FastCall(func, args, nargs)\
    __Pyx_PyFunction_FastCallDict((func), (args), (nargs), NULL)
#if 1 || PY_VERSION_HEX < 0x030600B1
static PyObject *__Pyx_PyFunction_FastCallDict(PyObject *func, PyObject **args, Py_ssize_t nargs, PyObject *kwargs);
#else
#define __Pyx_PyFunction_FastCallDict(func, args, nargs, kwargs) _PyFunction_FastCallDict(func, args, nargs, kwargs)
#endif
#define __Pyx_BUILD_ASSERT_EXPR(cond)\
    (sizeof(char [1 - 2*!(cond)]) - 1)
#ifndef Py_MEMBER_SIZE
#define Py_MEMBER_SIZE(type, member) sizeof(((type *)0)->member)
#endif
#if CYTHON_FAST_PYCALL
  static size_t __pyx_pyframe_localsplus_offset = 0;
  #include "frameobject.h"
#if PY_VERSION_HEX >= 0x030b00a6
  #ifndef Py_BUILD_CORE
    #define Py_BUILD_CORE 1
  #endif
  #include "internal/pycore_frame.h"
#endif
  #define __Pxy_PyFrame_Initialize_Offsets()\
    ((void)__Pyx_BUILD_ASSERT_EXPR(sizeof(PyFrameObject) == offsetof(PyFrameObject, f_localsplus) + Py_MEMBER_SIZE(PyFrameObject, f_localsplus)),\
     (void)(__pyx_pyframe_localsplus_offset = ((size_t)PyFrame_Type.tp_basicsize) - Py_MEMBER_SIZE(PyFrameObject, f_localsplus)))
  #define __Pyx_PyFrame_GetLocalsplus(frame)\
    (assert(__pyx_pyframe_localsplus_offset), (PyObject **)(((char *)(frame)) + __pyx_pyframe_localsplus_offset))
#endif // CYTHON_FAST_PYCALL
#endif

/* PyObjectCall.proto */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_Call(PyObject *func, PyObject *arg, PyObject *kw);
#else
#define __Pyx_PyObject_Call(func, arg, kw) PyObject_Call(func, arg, kw)
#endif

/* PyObjectCall2Args.proto */
static CYTHON_UNUSED PyObject* __Pyx_PyObject_Call2Args(PyObject* function, PyObject* arg1, PyObject* arg2);

/* PyObjectCallMethO.proto */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallMethO(PyObject *func, PyObject *arg);
#endif

/* PyObjectCallOneArg.proto */
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallOneArg(PyObject *func, PyObject *arg);

/* SliceObject.proto */
static CYTHON_INLINE PyObject* __Pyx_PyObject_GetSlice(
        PyObject* obj, Py_ssize_t cstart, Py_ssize_t cstop,
        PyObject** py_start, PyObject** py_stop, PyObject** py_slice,
        int has_cstart, int has_cstop, int wraparound);

/* PyDictVersioning.proto */
#if CYTHON_USE_DICT_VERSIONS && CYTHON_USE_TYPE_SLOTS
#define __PYX_DICT_VERSION_INIT  ((PY_UINT64_T) -1)
#define __PYX_GET_DICT_VERSION(dict)  (((PyDictObject*)(dict))->ma_version_tag)
#define __PYX_UPDATE_DICT_CACHE(dict, value, cache_var, version_var)\
    (version_var) = __PYX_GET_DICT_VERSION(dict);\
    (cache_var) = (value);
#define __PYX_PY_DICT_LOOKUP_IF_MODIFIED(VAR, DICT, LOOKUP) {\
    static PY_UINT64_T __pyx_dict_version = 0;\
    static PyObject *__pyx_dict_cached_value = NULL;\
    if (likely(__PYX_GET_DICT_VERSION(DICT) == __pyx_dict_version)) {\
        (VAR) = __pyx_dict_cached_value;\
    } else {\
        (VAR) = __pyx_dict_cached_value = (LOOKUP);\
        __pyx_dict_version = __PYX_GET_DICT_VERSION(DICT);\
    }\
}
static CYTHON_INLINE PY_UINT64_T __Pyx_get_tp_dict_version(PyObject *obj);
static CYTHON_INLINE PY_UINT64_T __Pyx_get_object_dict_version(PyObject *obj);
static CYTHON_INLINE int __Pyx_object_dict_version_matches(PyObject* obj, PY_UINT64_T tp_dict_version, PY_UINT64_T obj_dict_version);
#else
#define __PYX_GET_DICT_VERSION(dict)  (0)
#define __PYX_UPDATE_DICT_CACHE(dict, value, cache_var, version_var)
#define __PYX_PY_DICT_LOOKUP_IF_MODIFIED(VAR, DICT, LOOKUP)  (VAR) = (LOOKUP);
#endif

/* GetModuleGlobalName.proto */
#if CYTHON_USE_DICT_VERSIONS
#define __Pyx_GetModuleGlobalName(var, name)  {\
    static PY_UINT64_T __pyx_dict_version = 0;\
    static PyObject *__pyx_dict_cached_value = NULL;\
    (var) = (likely(__pyx_dict_version == __PYX_GET_DICT_VERSION(__pyx_d))) ?\
        (likely(__pyx_dict_cached_value) ? __Pyx_NewRef(__pyx_dict_cached_value) : __Pyx_GetBuiltinName(name)) :\
        __Pyx__GetModuleGlobalName(name, &__pyx_dict_version, &__pyx_dict_cached_value);\
}
#define __Pyx_GetModuleGlobalNameUncached(var, name)  {\
    PY_UINT64_T __pyx_dict_version;\
    PyObject *__pyx_dict_cached_value;\
    (var) = __Pyx__GetModuleGlobalName(name, &__pyx_dict_version, &__pyx_dict_cached_value);\
}
static PyObject *__Pyx__GetModuleGlobalName(PyObject *name, PY_UINT64_T *dict_version, PyObject **dict_cached_value);
#else
#define __Pyx_GetModuleGlobalName(var, name)  (var) = __Pyx__GetModuleGlobalName(name)
#define __Pyx_GetModuleGlobalNameUncached(var, name)  (var) = __Pyx__GetModuleGlobalName(name)
static CYTHON_INLINE PyObject *__Pyx__GetModuleGlobalName(PyObject *name);
#endif

/* IncludeStringH.proto */
#include <string.h>

/* BytesEquals.proto */
static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals);

/* UnicodeEquals.proto */
static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals);

/* StrEquals.proto */
#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyString_Equals __Pyx_PyUnicode_Equals
#else
#define __Pyx_PyString_Equals __Pyx_PyBytes_Equals
#endif

/* PyObjectCallNoArg.proto */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallNoArg(PyObject *func);
#else
#define __Pyx_PyObject_CallNoArg(func) __Pyx_PyObject_Call(func, __pyx_empty_tuple, NULL)
#endif

/* Import.proto */
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list, int level);

/* GetItemInt.proto */
#define __Pyx_GetItemInt(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_Fast(o, (Py_ssize_t)i, is_list, wraparound, boundscheck) :\
    (is_list ? (PyErr_SetString(PyExc_IndexError, "list index out of range"), (PyObject*)NULL) :\
               __Pyx_GetItemInt_Generic(o, to_py_func(i))))
#define __Pyx_GetItemInt_List(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_List_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) :\
    (PyErr_SetString(PyExc_IndexError, "list index out of range"), (PyObject*)NULL))
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck);
#define __Pyx_GetItemInt_Tuple(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck)\
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ?\
    __Pyx_GetItemInt_Tuple_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) :\
    (PyErr_SetString(PyExc_IndexError, "tuple index out of range"), (PyObject*)NULL))
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Tuple_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck);
static PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j);
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i,
                                                     int is_list, int wraparound, int boundscheck);

/* ObjectGetItem.proto */
#if CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PyObject *__Pyx_PyObject_GetItem(PyObject *obj, PyObject* key);
#else
#define __Pyx_PyObject_GetItem(obj, key)  PyObject_GetItem(obj, key)
#endif

/* FetchCommonType.proto */
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/* CythonFunctionShared.proto */
#define __Pyx_CyFunction_USED 1
#define __Pyx_CYFUNCTION_STATICMETHOD  0x01
#define __Pyx_CYFUNCTION_CLASSMETHOD   0x02
#define __Pyx_CYFUNCTION_CCLASS        0x04
#define __Pyx_CyFunction_GetClosure(f)\
    (((__pyx_CyFunctionObject *) (f))->func_closure)
#define __Pyx_CyFunction_GetClassObj(f)\
    (((__pyx_CyFunctionObject *) (f))->func_classobj)
#define __Pyx_CyFunction_Defaults(type, f)\
    ((type *)(((__pyx_CyFunctionObject *) (f))->defaults))
#define __Pyx_CyFunction_SetDefaultsGetter(f, g)\
    ((__pyx_CyFunctionObject *) (f))->defaults_getter = (g)
typedef struct {
    PyCFunctionObject func;
#if PY_VERSION_HEX < 0x030500A0
    PyObject *func_weakreflist;
#endif
    PyObject *func_dict;
    PyObject *func_name;
    PyObject *func_qualname;
    PyObject *func_doc;
    PyObject *func_globals;
    PyObject *func_code;
    PyObject *func_closure;
    PyObject *func_classobj;
    void *defaults;
    int defaults_pyobjects;
    size_t defaults_size;  // used by FusedFunction for copying defaults
    int flags;
    PyObject *defaults_tuple;
    PyObject *defaults_kwdict;
    PyObject *(*defaults_getter)(PyObject *);
    PyObject *func_annotations;
} __pyx_CyFunctionObject;
static PyTypeObject *__pyx_CyFunctionType = 0;
#define __Pyx_CyFunction_Check(obj)  (__Pyx_TypeCheck(obj, __pyx_CyFunctionType))
static PyObject *__Pyx_CyFunction_Init(__pyx_CyFunctionObject* op, PyMethodDef *ml,
                                      int flags, PyObject* qualname,
                                      PyObject *self,
                                      PyObject *module, PyObject *globals,
                                      PyObject* code);
static CYTHON_INLINE void *__Pyx_CyFunction_InitDefaults(PyObject *m,
                                                         size_t size,
                                                         int pyobjects);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsTuple(PyObject *m,
                                                            PyObject *tuple);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsKwDict(PyObject *m,
                                                             PyObject *dict);
static CYTHON_INLINE void __Pyx_CyFunction_SetAnnotationsDict(PyObject *m,
                                                              PyObject *dict);
static int __pyx_CyFunction_init(void);

/* CythonFunction.proto */
static PyObject *__Pyx_CyFunction_New(PyMethodDef *ml,
                                      int flags, PyObject* qualname,
                                      PyObject *closure,
                                      PyObject *module, PyObject *globals,
                                      PyObject* code);

/* PyThreadStateGet.proto */
#if CYTHON_FAST_THREAD_STATE
#define __Pyx_PyThreadState_declare  PyThreadState *__pyx_tstate;
#define __Pyx_PyThreadState_assign  __pyx_tstate = __Pyx_PyThreadState_Current;
#define __Pyx_PyErr_Occurred()  __pyx_tstate->curexc_type
#else
#define __Pyx_PyThreadState_declare
#define __Pyx_PyThreadState_assign
#define __Pyx_PyErr_Occurred()  PyErr_Occurred()
#endif

/* PyErrFetchRestore.proto */
#if CYTHON_FAST_THREAD_STATE
#define __Pyx_PyErr_Clear() __Pyx_ErrRestore(NULL, NULL, NULL)
#define __Pyx_ErrRestoreWithState(type, value, tb)  __Pyx_ErrRestoreInState(PyThreadState_GET(), type, value, tb)
#define __Pyx_ErrFetchWithState(type, value, tb)    __Pyx_ErrFetchInState(PyThreadState_GET(), type, value, tb)
#define __Pyx_ErrRestore(type, value, tb)  __Pyx_ErrRestoreInState(__pyx_tstate, type, value, tb)
#define __Pyx_ErrFetch(type, value, tb)    __Pyx_ErrFetchInState(__pyx_tstate, type, value, tb)
static CYTHON_INLINE void __Pyx_ErrRestoreInState(PyThreadState *tstate, PyObject *type, PyObject *value, PyObject *tb);
static CYTHON_INLINE void __Pyx_ErrFetchInState(PyThreadState *tstate, PyObject **type, PyObject **value, PyObject **tb);
#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_PyErr_SetNone(exc) (Py_INCREF(exc), __Pyx_ErrRestore((exc), NULL, NULL))
#else
#define __Pyx_PyErr_SetNone(exc) PyErr_SetNone(exc)
#endif
#else
#define __Pyx_PyErr_Clear() PyErr_Clear()
#define __Pyx_PyErr_SetNone(exc) PyErr_SetNone(exc)
#define __Pyx_ErrRestoreWithState(type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetchWithState(type, value, tb)  PyErr_Fetch(type, value, tb)
#define __Pyx_ErrRestoreInState(tstate, type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetchInState(tstate, type, value, tb)  PyErr_Fetch(type, value, tb)
#define __Pyx_ErrRestore(type, value, tb)  PyErr_Restore(type, value, tb)
#define __Pyx_ErrFetch(type, value, tb)  PyErr_Fetch(type, value, tb)
#endif

/* CLineInTraceback.proto */
#ifdef CYTHON_CLINE_IN_TRACEBACK
#define __Pyx_CLineForTraceback(tstate, c_line)  (((CYTHON_CLINE_IN_TRACEBACK)) ? c_line : 0)
#else
static int __Pyx_CLineForTraceback(PyThreadState *tstate, int c_line);
#endif

/* CodeObjectCache.proto */
typedef struct {
    PyCodeObject* code_object;
    int code_line;
} __Pyx_CodeObjectCacheEntry;
struct __Pyx_CodeObjectCache {
    int count;
    int max_count;
    __Pyx_CodeObjectCacheEntry* entries;
};
static struct __Pyx_CodeObjectCache __pyx_code_cache = {0,0,NULL};
static int __pyx_bisect_code_objects(__Pyx_CodeObjectCacheEntry* entries, int count, int code_line);
static PyCodeObject *__pyx_find_code_object(int code_line);
static void __pyx_insert_code_object(int code_line, PyCodeObject* code_object);

/* AddTraceback.proto */
static void __Pyx_AddTraceback(const char *funcname, int c_line,
                               int py_line, const char *filename);

/* GCCDiagnostics.proto */
#if defined(__GNUC__) && (__GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 6))
#define __Pyx_HAS_GCC_DIAGNOSTIC
#endif

/* CIntToPy.proto */
static CYTHON_INLINE PyObject* __Pyx_PyInt_From_long(long value);

/* CIntFromPy.proto */
static CYTHON_INLINE long __Pyx_PyInt_As_long(PyObject *);

/* CIntFromPy.proto */
static CYTHON_INLINE int __Pyx_PyInt_As_int(PyObject *);

/* FastTypeChecks.proto */
#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_TypeCheck(obj, type) __Pyx_IsSubtype(Py_TYPE(obj), (PyTypeObject *)type)
static CYTHON_INLINE int __Pyx_IsSubtype(PyTypeObject *a, PyTypeObject *b);
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches(PyObject *err, PyObject *type);
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches2(PyObject *err, PyObject *type1, PyObject *type2);
#else
#define __Pyx_TypeCheck(obj, type) PyObject_TypeCheck(obj, (PyTypeObject *)type)
#define __Pyx_PyErr_GivenExceptionMatches(err, type) PyErr_GivenExceptionMatches(err, type)
#define __Pyx_PyErr_GivenExceptionMatches2(err, type1, type2) (PyErr_GivenExceptionMatches(err, type1) || PyErr_GivenExceptionMatches(err, type2))
#endif
#define __Pyx_PyException_Check(obj) __Pyx_TypeCheck(obj, PyExc_Exception)

/* CheckBinaryVersion.proto */
static int __Pyx_check_binary_version(void);

/* InitStrings.proto */
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t);


/* Module declarations from 'dict_to_embedding' */
#define __Pyx_MODULE_NAME "dict_to_embedding"
extern int __pyx_module_is_main_dict_to_embedding;
int __pyx_module_is_main_dict_to_embedding = 0;

/* Implementation of 'dict_to_embedding' */
static PyObject *__pyx_builtin_range;
static const char __pyx_k_[] = ".";
static const char __pyx_k_E[] = "E";
static const char __pyx_k_F[] = "-F";
static const char __pyx_k_G[] = "G";
static const char __pyx_k_K[] = ".K";
static const char __pyx_k_M[] = "M";
static const char __pyx_k_O[] = ".O";
static const char __pyx_k_T[] = "T";
static const char __pyx_k_X[] = "X";
static const char __pyx_k_d[] = "-d";
static const char __pyx_k_i[] = "-i";
static const char __pyx_k_m[] = "-m";
static const char __pyx_k_o[] = "-o";
static const char __pyx_k_s[] = "s";
static const char __pyx_k_t[] = "-t";
static const char __pyx_k__9[] = "\t";
static const char __pyx_k_cg[] = "cg";
static const char __pyx_k_np[] = "np";
static const char __pyx_k_os[] = "os";
static const char __pyx_k_t0[] = "t0";
static const char __pyx_k_G_2[] = "-G";
static const char __pyx_k_K_2[] = "-K";
static const char __pyx_k_K_3[] = "K";
static const char __pyx_k_O_2[] = "-O";
static const char __pyx_k_O_3[] = "O";
static const char __pyx_k_T_2[] = ".T";
static const char __pyx_k_T_3[] = "-T";
static const char __pyx_k_i_2[] = "i";
static const char __pyx_k_m_2[] = "m";
static const char __pyx_k_mat[] = "mat";
static const char __pyx_k_sep[] = "sep";
static const char __pyx_k_suf[] = "suf";
static const char __pyx_k_sys[] = "sys";
static const char __pyx_k_txt[] = ".txt";
static const char __pyx_k_w2v[] = ".w2v";
static const char __pyx_k_args[] = "args";
static const char __pyx_k_help[] = "help";
static const char __pyx_k_load[] = "load";
static const char __pyx_k_main[] = "__main__";
static const char __pyx_k_name[] = "__name__";
static const char __pyx_k_outf[] = "outf";
static const char __pyx_k_save[] = "save";
static const char __pyx_k_test[] = "__test__";
static const char __pyx_k_time[] = "time";
static const char __pyx_k_txt2[] = ".txt2";
static const char __pyx_k_type[] = "type";
static const char __pyx_k_GGVec[] = "GGVec";
static const char __pyx_k_Glove[] = "Glove";
static const char __pyx_k_ProNE[] = "ProNE";
static const char __pyx_k_array[] = "array";
static const char __pyx_k_edges[] = "edges";
static const char __pyx_k_flush[] = "flush";
static const char __pyx_k_nodes[] = "nodes";
static const char __pyx_k_numpy[] = "numpy";
static const char __pyx_k_order[] = "order";
static const char __pyx_k_range[] = "range";
static const char __pyx_k_savez[] = "savez";
static const char __pyx_k_scipy[] = "scipy";
static const char __pyx_k_GraRep[] = "GraRep";
static const char __pyx_k_action[] = "action";
static const char __pyx_k_import[] = "__import__";
static const char __pyx_k_method[] = "method";
static const char __pyx_k_output[] = "output";
static const char __pyx_k_parser[] = "parser";
static const char __pyx_k_prefix[] = "prefix";
static const char __pyx_k_socket[] = "socket";
static const char __pyx_k_sparse[] = "sparse";
static const char __pyx_k_stderr[] = "stderr";
static const char __pyx_k_suffix[] = "suffix";
static const char __pyx_k_default[] = "default";
static const char __pyx_k_do_file[] = "do_file";
static const char __pyx_k_order_2[] = "--order";
static const char __pyx_k_quoting[] = "quoting";
static const char __pyx_k_threads[] = "threads";
static const char __pyx_k_argparse[] = "argparse";
static const char __pyx_k_csrgraph[] = "csrgraph";
static const char __pyx_k_endswith[] = "endswith";
static const char __pyx_k_exponent[] = "exponent";
static const char __pyx_k_load_npz[] = "load_npz";
static const char __pyx_k_method_2[] = "--method";
static const char __pyx_k_output_2[] = "--output";
static const char __pyx_k_required[] = "required";
static const char __pyx_k_suffixes[] = "suffixes";
static const char __pyx_k_delimiter[] = "delimiter";
static const char __pyx_k_threads_2[] = "--threads";
static const char __pyx_k_transpose[] = "transpose";
static const char __pyx_k_components[] = "components";
static const char __pyx_k_csr_matrix[] = "csr_matrix";
static const char __pyx_k_embeddings[] = "embeddings";
static const char __pyx_k_parse_args[] = "parse_args";
static const char __pyx_k_store_true[] = "store_true";
static const char __pyx_k_delimiter_2[] = "--delimiter";
static const char __pyx_k_input_graph[] = "input_graph";
static const char __pyx_k_nodevectors[] = "nodevectors";
static const char __pyx_k_output_file[] = "output file";
static const char __pyx_k_transpose_2[] = "--transpose";
static const char __pyx_k_add_argument[] = "add_argument";
static const char __pyx_k_components_2[] = "--components";
static const char __pyx_k_method2model[] = "method2model";
static const char __pyx_k_n_components[] = "n_components";
static const char __pyx_k_scipy_sparse[] = "scipy.sparse";
static const char __pyx_k_strip_suffix[] = "strip_suffix";
static const char __pyx_k_fit_transform[] = "fit_transform";
static const char __pyx_k_input_graph_2[] = "--input_graph";
static const char __pyx_k_read_edgelist[] = "read_edgelist";
static const char __pyx_k_ArgumentParser[] = "ArgumentParser";
static const char __pyx_k_defaults_to_tab[] = "defaults to tab";
static const char __pyx_k_features_matrix[] = "features_matrix";
static const char __pyx_k_input_edge_list[] = "input_edge_list";
static const char __pyx_k_output_embedding[] = "output_embedding";
static const char __pyx_k_dict_to_embedding[] = "dict_to_embedding";
static const char __pyx_k_features_matrix_2[] = "--features_matrix";
static const char __pyx_k_input_edge_list_2[] = "--input_edge_list";
static const char __pyx_k_pre_factorization[] = "pre_factorization";
static const char __pyx_k_cline_in_traceback[] = "cline_in_traceback";
static const char __pyx_k_dict_to_embedding_py[] = "dict_to_embedding.py";
static const char __pyx_k_ProNE_prefactorization[] = "ProNE_prefactorization";
static const char __pyx_k_hidden_dimensions_defaults_32[] = "hidden dimensions [defaults = 32]";
static const char __pyx_k_method_s_should_be_one_of_GGVec[] = "method (%s) should be one of: GGVec|GraRep|Glove|ProNE";
static const char __pyx_k_one_of_GGVec_GraRep_Glove_ProNE[] = "one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization";
static const char __pyx_k_for_ProNE_result_of_pre_factoriz[] = "for ProNE, result of pre_factorization";
static const char __pyx_k_input_graph_readable_by_scipy_sp[] = "input graph (readable by scipy.sparse.load_npz)";
static const char __pyx_k_input_text_file_one_line_for_eac[] = "input text file (one line for each edge)";
static const char __pyx_k_number_of_threads_defaults_20_ap[] = "number of threads [defaults = 20] (applies to methods: GGVec and Glove";
static const char __pyx_k_order_defaults_5_applies_to_meth[] = "order [defaults = 5] (applies to methods: GGVec and GraRep";
static const char __pyx_k_please_specify_either_input_edge[] = "please specify either --input_edge_list or --input_graph (but not both)";
static PyObject *__pyx_kp_s_;
static PyObject *__pyx_n_s_ArgumentParser;
static PyObject *__pyx_n_s_E;
static PyObject *__pyx_kp_s_F;
static PyObject *__pyx_n_s_G;
static PyObject *__pyx_n_s_GGVec;
static PyObject *__pyx_kp_s_G_2;
static PyObject *__pyx_n_s_Glove;
static PyObject *__pyx_n_s_GraRep;
static PyObject *__pyx_kp_s_K;
static PyObject *__pyx_kp_s_K_2;
static PyObject *__pyx_n_s_K_3;
static PyObject *__pyx_n_s_M;
static PyObject *__pyx_kp_s_O;
static PyObject *__pyx_kp_s_O_2;
static PyObject *__pyx_n_s_O_3;
static PyObject *__pyx_n_s_ProNE;
static PyObject *__pyx_n_s_ProNE_prefactorization;
static PyObject *__pyx_n_s_T;
static PyObject *__pyx_kp_s_T_2;
static PyObject *__pyx_kp_s_T_3;
static PyObject *__pyx_n_s_X;
static PyObject *__pyx_kp_s__9;
static PyObject *__pyx_n_s_action;
static PyObject *__pyx_n_s_add_argument;
static PyObject *__pyx_n_s_argparse;
static PyObject *__pyx_n_s_args;
static PyObject *__pyx_n_s_array;
static PyObject *__pyx_n_s_cg;
static PyObject *__pyx_n_s_cline_in_traceback;
static PyObject *__pyx_n_s_components;
static PyObject *__pyx_kp_s_components_2;
static PyObject *__pyx_n_s_csr_matrix;
static PyObject *__pyx_n_s_csrgraph;
static PyObject *__pyx_kp_s_d;
static PyObject *__pyx_n_s_default;
static PyObject *__pyx_kp_s_defaults_to_tab;
static PyObject *__pyx_n_s_delimiter;
static PyObject *__pyx_kp_s_delimiter_2;
static PyObject *__pyx_n_s_dict_to_embedding;
static PyObject *__pyx_kp_s_dict_to_embedding_py;
static PyObject *__pyx_n_s_do_file;
static PyObject *__pyx_n_s_edges;
static PyObject *__pyx_n_s_embeddings;
static PyObject *__pyx_n_s_endswith;
static PyObject *__pyx_n_s_exponent;
static PyObject *__pyx_n_s_features_matrix;
static PyObject *__pyx_kp_s_features_matrix_2;
static PyObject *__pyx_n_s_fit_transform;
static PyObject *__pyx_n_s_flush;
static PyObject *__pyx_kp_s_for_ProNE_result_of_pre_factoriz;
static PyObject *__pyx_n_s_help;
static PyObject *__pyx_kp_s_hidden_dimensions_defaults_32;
static PyObject *__pyx_kp_s_i;
static PyObject *__pyx_n_s_i_2;
static PyObject *__pyx_n_s_import;
static PyObject *__pyx_n_s_input_edge_list;
static PyObject *__pyx_kp_s_input_edge_list_2;
static PyObject *__pyx_n_s_input_graph;
static PyObject *__pyx_kp_s_input_graph_2;
static PyObject *__pyx_kp_s_input_graph_readable_by_scipy_sp;
static PyObject *__pyx_kp_s_input_text_file_one_line_for_eac;
static PyObject *__pyx_n_s_load;
static PyObject *__pyx_n_s_load_npz;
static PyObject *__pyx_kp_s_m;
static PyObject *__pyx_n_s_m_2;
static PyObject *__pyx_n_s_main;
static PyObject *__pyx_n_s_mat;
static PyObject *__pyx_n_s_method;
static PyObject *__pyx_n_s_method2model;
static PyObject *__pyx_kp_s_method_2;
static PyObject *__pyx_kp_s_method_s_should_be_one_of_GGVec;
static PyObject *__pyx_n_s_n_components;
static PyObject *__pyx_n_s_name;
static PyObject *__pyx_n_s_nodes;
static PyObject *__pyx_n_s_nodevectors;
static PyObject *__pyx_n_s_np;
static PyObject *__pyx_kp_s_number_of_threads_defaults_20_ap;
static PyObject *__pyx_n_s_numpy;
static PyObject *__pyx_kp_s_o;
static PyObject *__pyx_kp_s_one_of_GGVec_GraRep_Glove_ProNE;
static PyObject *__pyx_n_s_order;
static PyObject *__pyx_kp_s_order_2;
static PyObject *__pyx_kp_s_order_defaults_5_applies_to_meth;
static PyObject *__pyx_n_s_os;
static PyObject *__pyx_n_s_outf;
static PyObject *__pyx_n_s_output;
static PyObject *__pyx_kp_s_output_2;
static PyObject *__pyx_n_s_output_embedding;
static PyObject *__pyx_kp_s_output_file;
static PyObject *__pyx_n_s_parse_args;
static PyObject *__pyx_n_s_parser;
static PyObject *__pyx_kp_s_please_specify_either_input_edge;
static PyObject *__pyx_n_s_pre_factorization;
static PyObject *__pyx_n_s_prefix;
static PyObject *__pyx_n_s_quoting;
static PyObject *__pyx_n_s_range;
static PyObject *__pyx_n_s_read_edgelist;
static PyObject *__pyx_n_s_required;
static PyObject *__pyx_n_s_s;
static PyObject *__pyx_n_s_save;
static PyObject *__pyx_n_s_savez;
static PyObject *__pyx_n_s_scipy;
static PyObject *__pyx_n_s_scipy_sparse;
static PyObject *__pyx_n_s_sep;
static PyObject *__pyx_n_s_socket;
static PyObject *__pyx_n_s_sparse;
static PyObject *__pyx_n_s_stderr;
static PyObject *__pyx_n_s_store_true;
static PyObject *__pyx_n_s_strip_suffix;
static PyObject *__pyx_n_s_suf;
static PyObject *__pyx_n_s_suffix;
static PyObject *__pyx_n_s_suffixes;
static PyObject *__pyx_n_s_sys;
static PyObject *__pyx_kp_s_t;
static PyObject *__pyx_n_s_t0;
static PyObject *__pyx_n_s_test;
static PyObject *__pyx_n_s_threads;
static PyObject *__pyx_kp_s_threads_2;
static PyObject *__pyx_n_s_time;
static PyObject *__pyx_n_s_transpose;
static PyObject *__pyx_kp_s_transpose_2;
static PyObject *__pyx_kp_s_txt;
static PyObject *__pyx_kp_s_txt2;
static PyObject *__pyx_n_s_type;
static PyObject *__pyx_kp_s_w2v;
static PyObject *__pyx_pf_17dict_to_embedding_strip_suffix(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_s, PyObject *__pyx_v_suffixes); /* proto */
static PyObject *__pyx_pf_17dict_to_embedding_2method2model(CYTHON_UNUSED PyObject *__pyx_self); /* proto */
static PyObject *__pyx_pf_17dict_to_embedding_4output_embedding(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_G, PyObject *__pyx_v_E, PyObject *__pyx_v_outf); /* proto */
static PyObject *__pyx_pf_17dict_to_embedding_6do_file(CYTHON_UNUSED PyObject *__pyx_self); /* proto */
static PyObject *__pyx_int_3;
static PyObject *__pyx_int_5;
static PyObject *__pyx_int_20;
static PyObject *__pyx_int_32;
static PyObject *__pyx_tuple__2;
static PyObject *__pyx_tuple__3;
static PyObject *__pyx_tuple__4;
static PyObject *__pyx_tuple__5;
static PyObject *__pyx_tuple__6;
static PyObject *__pyx_tuple__7;
static PyObject *__pyx_tuple__8;
static PyObject *__pyx_tuple__10;
static PyObject *__pyx_tuple__11;
static PyObject *__pyx_tuple__12;
static PyObject *__pyx_tuple__13;
static PyObject *__pyx_tuple__15;
static PyObject *__pyx_tuple__17;
static PyObject *__pyx_tuple__19;
static PyObject *__pyx_codeobj__14;
static PyObject *__pyx_codeobj__16;
static PyObject *__pyx_codeobj__18;
static PyObject *__pyx_codeobj__20;
/* Late includes */

/* "dict_to_embedding.py":40
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'
 * 
 * def strip_suffix(s, suffixes):             # <<<<<<<<<<<<<<
 *     for suf in suffixes:
 *         if s.endswith(suf):
 */

/* Python wrapper */
static PyObject *__pyx_pw_17dict_to_embedding_1strip_suffix(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyMethodDef __pyx_mdef_17dict_to_embedding_1strip_suffix = {"strip_suffix", (PyCFunction)(void*)(PyCFunctionWithKeywords)__pyx_pw_17dict_to_embedding_1strip_suffix, METH_VARARGS|METH_KEYWORDS, 0};
static PyObject *__pyx_pw_17dict_to_embedding_1strip_suffix(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_s = 0;
  PyObject *__pyx_v_suffixes = 0;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("strip_suffix (wrapper)", 0);
  {
    static PyObject **__pyx_pyargnames[] = {&__pyx_n_s_s,&__pyx_n_s_suffixes,0};
    PyObject* values[2] = {0,0};
    if (unlikely(__pyx_kwds)) {
      Py_ssize_t kw_args;
      const Py_ssize_t pos_args = PyTuple_GET_SIZE(__pyx_args);
      switch (pos_args) {
        case  2: values[1] = PyTuple_GET_ITEM(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = PyTuple_GET_ITEM(__pyx_args, 0);
        CYTHON_FALLTHROUGH;
        case  0: break;
        default: goto __pyx_L5_argtuple_error;
      }
      kw_args = PyDict_Size(__pyx_kwds);
      switch (pos_args) {
        case  0:
        if (likely((values[0] = __Pyx_PyDict_GetItemStr(__pyx_kwds, __pyx_n_s_s)) != 0)) kw_args--;
        else goto __pyx_L5_argtuple_error;
        CYTHON_FALLTHROUGH;
        case  1:
        if (likely((values[1] = __Pyx_PyDict_GetItemStr(__pyx_kwds, __pyx_n_s_suffixes)) != 0)) kw_args--;
        else {
          __Pyx_RaiseArgtupleInvalid("strip_suffix", 1, 2, 2, 1); __PYX_ERR(0, 40, __pyx_L3_error)
        }
      }
      if (unlikely(kw_args > 0)) {
        if (unlikely(__Pyx_ParseOptionalKeywords(__pyx_kwds, __pyx_pyargnames, 0, values, pos_args, "strip_suffix") < 0)) __PYX_ERR(0, 40, __pyx_L3_error)
      }
    } else if (PyTuple_GET_SIZE(__pyx_args) != 2) {
      goto __pyx_L5_argtuple_error;
    } else {
      values[0] = PyTuple_GET_ITEM(__pyx_args, 0);
      values[1] = PyTuple_GET_ITEM(__pyx_args, 1);
    }
    __pyx_v_s = values[0];
    __pyx_v_suffixes = values[1];
  }
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L5_argtuple_error:;
  __Pyx_RaiseArgtupleInvalid("strip_suffix", 1, 2, 2, PyTuple_GET_SIZE(__pyx_args)); __PYX_ERR(0, 40, __pyx_L3_error)
  __pyx_L3_error:;
  __Pyx_AddTraceback("dict_to_embedding.strip_suffix", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __Pyx_RefNannyFinishContext();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_17dict_to_embedding_strip_suffix(__pyx_self, __pyx_v_s, __pyx_v_suffixes);

  /* function exit code */
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyObject *__pyx_pf_17dict_to_embedding_strip_suffix(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_s, PyObject *__pyx_v_suffixes) {
  PyObject *__pyx_v_suf = NULL;
  PyObject *__pyx_r = NULL;
  __Pyx_RefNannyDeclarations
  PyObject *__pyx_t_1 = NULL;
  Py_ssize_t __pyx_t_2;
  PyObject *(*__pyx_t_3)(PyObject *);
  PyObject *__pyx_t_4 = NULL;
  PyObject *__pyx_t_5 = NULL;
  PyObject *__pyx_t_6 = NULL;
  int __pyx_t_7;
  Py_ssize_t __pyx_t_8;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannySetupContext("strip_suffix", 0);

  /* "dict_to_embedding.py":41
 * 
 * def strip_suffix(s, suffixes):
 *     for suf in suffixes:             # <<<<<<<<<<<<<<
 *         if s.endswith(suf):
 *             return s[0:-len(suf)]
 */
  if (likely(PyList_CheckExact(__pyx_v_suffixes)) || PyTuple_CheckExact(__pyx_v_suffixes)) {
    __pyx_t_1 = __pyx_v_suffixes; __Pyx_INCREF(__pyx_t_1); __pyx_t_2 = 0;
    __pyx_t_3 = NULL;
  } else {
    __pyx_t_2 = -1; __pyx_t_1 = PyObject_GetIter(__pyx_v_suffixes); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 41, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_3 = Py_TYPE(__pyx_t_1)->tp_iternext; if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 41, __pyx_L1_error)
  }
  for (;;) {
    if (likely(!__pyx_t_3)) {
      if (likely(PyList_CheckExact(__pyx_t_1))) {
        if (__pyx_t_2 >= PyList_GET_SIZE(__pyx_t_1)) break;
        #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
        __pyx_t_4 = PyList_GET_ITEM(__pyx_t_1, __pyx_t_2); __Pyx_INCREF(__pyx_t_4); __pyx_t_2++; if (unlikely(0 < 0)) __PYX_ERR(0, 41, __pyx_L1_error)
        #else
        __pyx_t_4 = PySequence_ITEM(__pyx_t_1, __pyx_t_2); __pyx_t_2++; if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 41, __pyx_L1_error)
        __Pyx_GOTREF(__pyx_t_4);
        #endif
      } else {
        if (__pyx_t_2 >= PyTuple_GET_SIZE(__pyx_t_1)) break;
        #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
        __pyx_t_4 = PyTuple_GET_ITEM(__pyx_t_1, __pyx_t_2); __Pyx_INCREF(__pyx_t_4); __pyx_t_2++; if (unlikely(0 < 0)) __PYX_ERR(0, 41, __pyx_L1_error)
        #else
        __pyx_t_4 = PySequence_ITEM(__pyx_t_1, __pyx_t_2); __pyx_t_2++; if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 41, __pyx_L1_error)
        __Pyx_GOTREF(__pyx_t_4);
        #endif
      }
    } else {
      __pyx_t_4 = __pyx_t_3(__pyx_t_1);
      if (unlikely(!__pyx_t_4)) {
        PyObject* exc_type = PyErr_Occurred();
        if (exc_type) {
          if (likely(__Pyx_PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration))) PyErr_Clear();
          else __PYX_ERR(0, 41, __pyx_L1_error)
        }
        break;
      }
      __Pyx_GOTREF(__pyx_t_4);
    }
    __Pyx_XDECREF_SET(__pyx_v_suf, __pyx_t_4);
    __pyx_t_4 = 0;

    /* "dict_to_embedding.py":42
 * def strip_suffix(s, suffixes):
 *     for suf in suffixes:
 *         if s.endswith(suf):             # <<<<<<<<<<<<<<
 *             return s[0:-len(suf)]
 *     return s
 */
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_v_s, __pyx_n_s_endswith); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 42, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_6 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_5))) {
      __pyx_t_6 = PyMethod_GET_SELF(__pyx_t_5);
      if (likely(__pyx_t_6)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_5);
        __Pyx_INCREF(__pyx_t_6);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_5, function);
      }
    }
    __pyx_t_4 = (__pyx_t_6) ? __Pyx_PyObject_Call2Args(__pyx_t_5, __pyx_t_6, __pyx_v_suf) : __Pyx_PyObject_CallOneArg(__pyx_t_5, __pyx_v_suf);
    __Pyx_XDECREF(__pyx_t_6); __pyx_t_6 = 0;
    if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 42, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_t_7 = __Pyx_PyObject_IsTrue(__pyx_t_4); if (unlikely(__pyx_t_7 < 0)) __PYX_ERR(0, 42, __pyx_L1_error)
    __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
    if (__pyx_t_7) {

      /* "dict_to_embedding.py":43
 *     for suf in suffixes:
 *         if s.endswith(suf):
 *             return s[0:-len(suf)]             # <<<<<<<<<<<<<<
 *     return s
 * 
 */
      __Pyx_XDECREF(__pyx_r);
      __pyx_t_8 = PyObject_Length(__pyx_v_suf); if (unlikely(__pyx_t_8 == ((Py_ssize_t)-1))) __PYX_ERR(0, 43, __pyx_L1_error)
      __pyx_t_4 = __Pyx_PyObject_GetSlice(__pyx_v_s, 0, (-__pyx_t_8), NULL, NULL, NULL, 1, 1, 1); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 43, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_4);
      __pyx_r = __pyx_t_4;
      __pyx_t_4 = 0;
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      goto __pyx_L0;

      /* "dict_to_embedding.py":42
 * def strip_suffix(s, suffixes):
 *     for suf in suffixes:
 *         if s.endswith(suf):             # <<<<<<<<<<<<<<
 *             return s[0:-len(suf)]
 *     return s
 */
    }

    /* "dict_to_embedding.py":41
 * 
 * def strip_suffix(s, suffixes):
 *     for suf in suffixes:             # <<<<<<<<<<<<<<
 *         if s.endswith(suf):
 *             return s[0:-len(suf)]
 */
  }
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":44
 *         if s.endswith(suf):
 *             return s[0:-len(suf)]
 *     return s             # <<<<<<<<<<<<<<
 * 
 * def method2model():
 */
  __Pyx_XDECREF(__pyx_r);
  __Pyx_INCREF(__pyx_v_s);
  __pyx_r = __pyx_v_s;
  goto __pyx_L0;

  /* "dict_to_embedding.py":40
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'
 * 
 * def strip_suffix(s, suffixes):             # <<<<<<<<<<<<<<
 *     for suf in suffixes:
 *         if s.endswith(suf):
 */

  /* function exit code */
  __pyx_L1_error:;
  __Pyx_XDECREF(__pyx_t_1);
  __Pyx_XDECREF(__pyx_t_4);
  __Pyx_XDECREF(__pyx_t_5);
  __Pyx_XDECREF(__pyx_t_6);
  __Pyx_AddTraceback("dict_to_embedding.strip_suffix", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  __Pyx_XDECREF(__pyx_v_suf);
  __Pyx_XGIVEREF(__pyx_r);
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

/* "dict_to_embedding.py":46
 *     return s
 * 
 * def method2model():             # <<<<<<<<<<<<<<
 *     m = args.method
 *     K = args.components
 */

/* Python wrapper */
static PyObject *__pyx_pw_17dict_to_embedding_3method2model(PyObject *__pyx_self, CYTHON_UNUSED PyObject *unused); /*proto*/
static PyMethodDef __pyx_mdef_17dict_to_embedding_3method2model = {"method2model", (PyCFunction)__pyx_pw_17dict_to_embedding_3method2model, METH_NOARGS, 0};
static PyObject *__pyx_pw_17dict_to_embedding_3method2model(PyObject *__pyx_self, CYTHON_UNUSED PyObject *unused) {
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("method2model (wrapper)", 0);
  __pyx_r = __pyx_pf_17dict_to_embedding_2method2model(__pyx_self);

  /* function exit code */
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyObject *__pyx_pf_17dict_to_embedding_2method2model(CYTHON_UNUSED PyObject *__pyx_self) {
  PyObject *__pyx_v_m = NULL;
  PyObject *__pyx_v_K = NULL;
  PyObject *__pyx_v_T = NULL;
  PyObject *__pyx_v_O = NULL;
  PyObject *__pyx_r = NULL;
  __Pyx_RefNannyDeclarations
  PyObject *__pyx_t_1 = NULL;
  PyObject *__pyx_t_2 = NULL;
  int __pyx_t_3;
  PyObject *__pyx_t_4 = NULL;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannySetupContext("method2model", 0);

  /* "dict_to_embedding.py":47
 * 
 * def method2model():
 *     m = args.method             # <<<<<<<<<<<<<<
 *     K = args.components
 *     #print('# K = %d, time: %0.2f' % (K, (time.time() - t0)), file=sys.stderr)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 47, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_method); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 47, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_v_m = __pyx_t_2;
  __pyx_t_2 = 0;

  /* "dict_to_embedding.py":48
 * def method2model():
 *     m = args.method
 *     K = args.components             # <<<<<<<<<<<<<<
 *     #print('# K = %d, time: %0.2f' % (K, (time.time() - t0)), file=sys.stderr)
 *     T = args.threads
 */
  __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_args); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 48, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_components); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 48, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_v_K = __pyx_t_1;
  __pyx_t_1 = 0;

  /* "dict_to_embedding.py":50
 *     K = args.components
 *     #print('# K = %d, time: %0.2f' % (K, (time.time() - t0)), file=sys.stderr)
 *     T = args.threads             # <<<<<<<<<<<<<<
 *     O = args.order
 *     # s = args.save_svd
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 50, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_threads); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 50, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_v_T = __pyx_t_2;
  __pyx_t_2 = 0;

  /* "dict_to_embedding.py":51
 *     #print('# K = %d, time: %0.2f' % (K, (time.time() - t0)), file=sys.stderr)
 *     T = args.threads
 *     O = args.order             # <<<<<<<<<<<<<<
 *     # s = args.save_svd
 *     # l = args.load_svd
 */
  __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_args); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 51, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_order); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 51, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_v_O = __pyx_t_1;
  __pyx_t_1 = 0;

  /* "dict_to_embedding.py":55
 *     # l = args.load_svd
 *     # f = args.svd_file
 *     if m == 'GGVec':             # <<<<<<<<<<<<<<
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)
 *     elif m == 'GraRep':
 */
  __pyx_t_3 = (__Pyx_PyString_Equals(__pyx_v_m, __pyx_n_s_GGVec, Py_EQ)); if (unlikely(__pyx_t_3 < 0)) __PYX_ERR(0, 55, __pyx_L1_error)
  if (__pyx_t_3) {

    /* "dict_to_embedding.py":56
 *     # f = args.svd_file
 *     if m == 'GGVec':
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)             # <<<<<<<<<<<<<<
 *     elif m == 'GraRep':
 *         return nodevectors.GraRep(n_components=K, order=O)
 */
    __Pyx_XDECREF(__pyx_r);
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_nodevectors); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 56, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_GGVec); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 56, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = __Pyx_PyDict_NewPresized(3); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 56, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_n_components, __pyx_v_K) < 0) __PYX_ERR(0, 56, __pyx_L1_error)
    if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_threads, __pyx_v_T) < 0) __PYX_ERR(0, 56, __pyx_L1_error)
    if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_order, __pyx_v_O) < 0) __PYX_ERR(0, 56, __pyx_L1_error)
    __pyx_t_4 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_empty_tuple, __pyx_t_1); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 56, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_r = __pyx_t_4;
    __pyx_t_4 = 0;
    goto __pyx_L0;

    /* "dict_to_embedding.py":55
 *     # l = args.load_svd
 *     # f = args.svd_file
 *     if m == 'GGVec':             # <<<<<<<<<<<<<<
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)
 *     elif m == 'GraRep':
 */
  }

  /* "dict_to_embedding.py":57
 *     if m == 'GGVec':
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)
 *     elif m == 'GraRep':             # <<<<<<<<<<<<<<
 *         return nodevectors.GraRep(n_components=K, order=O)
 *     elif m ==  'Glove':
 */
  __pyx_t_3 = (__Pyx_PyString_Equals(__pyx_v_m, __pyx_n_s_GraRep, Py_EQ)); if (unlikely(__pyx_t_3 < 0)) __PYX_ERR(0, 57, __pyx_L1_error)
  if (__pyx_t_3) {

    /* "dict_to_embedding.py":58
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)
 *     elif m == 'GraRep':
 *         return nodevectors.GraRep(n_components=K, order=O)             # <<<<<<<<<<<<<<
 *     elif m ==  'Glove':
 *         return nodevectors.Glove(n_components=K, threads=T)
 */
    __Pyx_XDECREF(__pyx_r);
    __Pyx_GetModuleGlobalName(__pyx_t_4, __pyx_n_s_nodevectors); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 58, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_4, __pyx_n_s_GraRep); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 58, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
    __pyx_t_4 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 58, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    if (PyDict_SetItem(__pyx_t_4, __pyx_n_s_n_components, __pyx_v_K) < 0) __PYX_ERR(0, 58, __pyx_L1_error)
    if (PyDict_SetItem(__pyx_t_4, __pyx_n_s_order, __pyx_v_O) < 0) __PYX_ERR(0, 58, __pyx_L1_error)
    __pyx_t_2 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_empty_tuple, __pyx_t_4); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 58, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
    __pyx_r = __pyx_t_2;
    __pyx_t_2 = 0;
    goto __pyx_L0;

    /* "dict_to_embedding.py":57
 *     if m == 'GGVec':
 *         return nodevectors.GGVec(n_components=K, threads=T, order=O)
 *     elif m == 'GraRep':             # <<<<<<<<<<<<<<
 *         return nodevectors.GraRep(n_components=K, order=O)
 *     elif m ==  'Glove':
 */
  }

  /* "dict_to_embedding.py":59
 *     elif m == 'GraRep':
 *         return nodevectors.GraRep(n_components=K, order=O)
 *     elif m ==  'Glove':             # <<<<<<<<<<<<<<
 *         return nodevectors.Glove(n_components=K, threads=T)
 *     elif m == 'ProNE':
 */
  __pyx_t_3 = (__Pyx_PyString_Equals(__pyx_v_m, __pyx_n_s_Glove, Py_EQ)); if (unlikely(__pyx_t_3 < 0)) __PYX_ERR(0, 59, __pyx_L1_error)
  if (__pyx_t_3) {

    /* "dict_to_embedding.py":60
 *         return nodevectors.GraRep(n_components=K, order=O)
 *     elif m ==  'Glove':
 *         return nodevectors.Glove(n_components=K, threads=T)             # <<<<<<<<<<<<<<
 *     elif m == 'ProNE':
 *         return nodevectors.ProNE(n_components=K)
 */
    __Pyx_XDECREF(__pyx_r);
    __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_nodevectors); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 60, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_4 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_Glove); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 60, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_t_2 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 60, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_n_components, __pyx_v_K) < 0) __PYX_ERR(0, 60, __pyx_L1_error)
    if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_threads, __pyx_v_T) < 0) __PYX_ERR(0, 60, __pyx_L1_error)
    __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_4, __pyx_empty_tuple, __pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 60, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_r = __pyx_t_1;
    __pyx_t_1 = 0;
    goto __pyx_L0;

    /* "dict_to_embedding.py":59
 *     elif m == 'GraRep':
 *         return nodevectors.GraRep(n_components=K, order=O)
 *     elif m ==  'Glove':             # <<<<<<<<<<<<<<
 *         return nodevectors.Glove(n_components=K, threads=T)
 *     elif m == 'ProNE':
 */
  }

  /* "dict_to_embedding.py":61
 *     elif m ==  'Glove':
 *         return nodevectors.Glove(n_components=K, threads=T)
 *     elif m == 'ProNE':             # <<<<<<<<<<<<<<
 *         return nodevectors.ProNE(n_components=K)
 *     # elif m == 'ProNE' or m == 'ProNE_prefactorization':
 */
  __pyx_t_3 = (__Pyx_PyString_Equals(__pyx_v_m, __pyx_n_s_ProNE, Py_EQ)); if (unlikely(__pyx_t_3 < 0)) __PYX_ERR(0, 61, __pyx_L1_error)
  if (__pyx_t_3) {

    /* "dict_to_embedding.py":62
 *         return nodevectors.Glove(n_components=K, threads=T)
 *     elif m == 'ProNE':
 *         return nodevectors.ProNE(n_components=K)             # <<<<<<<<<<<<<<
 *     # elif m == 'ProNE' or m == 'ProNE_prefactorization':
 *     #  return nodevectors.ProNE(n_components=K, save_svd=s, load_svd=l, svd_file=f)
 */
    __Pyx_XDECREF(__pyx_r);
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_nodevectors); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 62, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_ProNE); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 62, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = __Pyx_PyDict_NewPresized(1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 62, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_n_components, __pyx_v_K) < 0) __PYX_ERR(0, 62, __pyx_L1_error)
    __pyx_t_4 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_empty_tuple, __pyx_t_1); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 62, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_4);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_r = __pyx_t_4;
    __pyx_t_4 = 0;
    goto __pyx_L0;

    /* "dict_to_embedding.py":61
 *     elif m ==  'Glove':
 *         return nodevectors.Glove(n_components=K, threads=T)
 *     elif m == 'ProNE':             # <<<<<<<<<<<<<<
 *         return nodevectors.ProNE(n_components=K)
 *     # elif m == 'ProNE' or m == 'ProNE_prefactorization':
 */
  }

  /* "dict_to_embedding.py":65
 *     # elif m == 'ProNE' or m == 'ProNE_prefactorization':
 *     #  return nodevectors.ProNE(n_components=K, save_svd=s, load_svd=l, svd_file=f)
 *     assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m             # <<<<<<<<<<<<<<
 * 
 * def output_embedding(G, E, outf):
 */
  #ifndef CYTHON_WITHOUT_ASSERTIONS
  if (unlikely(!Py_OptimizeFlag)) {
    if (unlikely(!0)) {
      __pyx_t_4 = __Pyx_PyString_FormatSafe(__pyx_kp_s_method_s_should_be_one_of_GGVec, __pyx_v_m); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 65, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_4);
      PyErr_SetObject(PyExc_AssertionError, __pyx_t_4);
      __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
      __PYX_ERR(0, 65, __pyx_L1_error)
    }
  }
  #endif

  /* "dict_to_embedding.py":46
 *     return s
 * 
 * def method2model():             # <<<<<<<<<<<<<<
 *     m = args.method
 *     K = args.components
 */

  /* function exit code */
  __pyx_r = Py_None; __Pyx_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1_error:;
  __Pyx_XDECREF(__pyx_t_1);
  __Pyx_XDECREF(__pyx_t_2);
  __Pyx_XDECREF(__pyx_t_4);
  __Pyx_AddTraceback("dict_to_embedding.method2model", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  __Pyx_XDECREF(__pyx_v_m);
  __Pyx_XDECREF(__pyx_v_K);
  __Pyx_XDECREF(__pyx_v_T);
  __Pyx_XDECREF(__pyx_v_O);
  __Pyx_XGIVEREF(__pyx_r);
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

/* "dict_to_embedding.py":67
 *     assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m
 * 
 * def output_embedding(G, E, outf):             # <<<<<<<<<<<<<<
 *     np.savez(outf, nodes=np.array(G.nodes()), edges=E)
 * 
 */

/* Python wrapper */
static PyObject *__pyx_pw_17dict_to_embedding_5output_embedding(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyMethodDef __pyx_mdef_17dict_to_embedding_5output_embedding = {"output_embedding", (PyCFunction)(void*)(PyCFunctionWithKeywords)__pyx_pw_17dict_to_embedding_5output_embedding, METH_VARARGS|METH_KEYWORDS, 0};
static PyObject *__pyx_pw_17dict_to_embedding_5output_embedding(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_G = 0;
  PyObject *__pyx_v_E = 0;
  PyObject *__pyx_v_outf = 0;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("output_embedding (wrapper)", 0);
  {
    static PyObject **__pyx_pyargnames[] = {&__pyx_n_s_G,&__pyx_n_s_E,&__pyx_n_s_outf,0};
    PyObject* values[3] = {0,0,0};
    if (unlikely(__pyx_kwds)) {
      Py_ssize_t kw_args;
      const Py_ssize_t pos_args = PyTuple_GET_SIZE(__pyx_args);
      switch (pos_args) {
        case  3: values[2] = PyTuple_GET_ITEM(__pyx_args, 2);
        CYTHON_FALLTHROUGH;
        case  2: values[1] = PyTuple_GET_ITEM(__pyx_args, 1);
        CYTHON_FALLTHROUGH;
        case  1: values[0] = PyTuple_GET_ITEM(__pyx_args, 0);
        CYTHON_FALLTHROUGH;
        case  0: break;
        default: goto __pyx_L5_argtuple_error;
      }
      kw_args = PyDict_Size(__pyx_kwds);
      switch (pos_args) {
        case  0:
        if (likely((values[0] = __Pyx_PyDict_GetItemStr(__pyx_kwds, __pyx_n_s_G)) != 0)) kw_args--;
        else goto __pyx_L5_argtuple_error;
        CYTHON_FALLTHROUGH;
        case  1:
        if (likely((values[1] = __Pyx_PyDict_GetItemStr(__pyx_kwds, __pyx_n_s_E)) != 0)) kw_args--;
        else {
          __Pyx_RaiseArgtupleInvalid("output_embedding", 1, 3, 3, 1); __PYX_ERR(0, 67, __pyx_L3_error)
        }
        CYTHON_FALLTHROUGH;
        case  2:
        if (likely((values[2] = __Pyx_PyDict_GetItemStr(__pyx_kwds, __pyx_n_s_outf)) != 0)) kw_args--;
        else {
          __Pyx_RaiseArgtupleInvalid("output_embedding", 1, 3, 3, 2); __PYX_ERR(0, 67, __pyx_L3_error)
        }
      }
      if (unlikely(kw_args > 0)) {
        if (unlikely(__Pyx_ParseOptionalKeywords(__pyx_kwds, __pyx_pyargnames, 0, values, pos_args, "output_embedding") < 0)) __PYX_ERR(0, 67, __pyx_L3_error)
      }
    } else if (PyTuple_GET_SIZE(__pyx_args) != 3) {
      goto __pyx_L5_argtuple_error;
    } else {
      values[0] = PyTuple_GET_ITEM(__pyx_args, 0);
      values[1] = PyTuple_GET_ITEM(__pyx_args, 1);
      values[2] = PyTuple_GET_ITEM(__pyx_args, 2);
    }
    __pyx_v_G = values[0];
    __pyx_v_E = values[1];
    __pyx_v_outf = values[2];
  }
  goto __pyx_L4_argument_unpacking_done;
  __pyx_L5_argtuple_error:;
  __Pyx_RaiseArgtupleInvalid("output_embedding", 1, 3, 3, PyTuple_GET_SIZE(__pyx_args)); __PYX_ERR(0, 67, __pyx_L3_error)
  __pyx_L3_error:;
  __Pyx_AddTraceback("dict_to_embedding.output_embedding", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __Pyx_RefNannyFinishContext();
  return NULL;
  __pyx_L4_argument_unpacking_done:;
  __pyx_r = __pyx_pf_17dict_to_embedding_4output_embedding(__pyx_self, __pyx_v_G, __pyx_v_E, __pyx_v_outf);

  /* function exit code */
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyObject *__pyx_pf_17dict_to_embedding_4output_embedding(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_G, PyObject *__pyx_v_E, PyObject *__pyx_v_outf) {
  PyObject *__pyx_r = NULL;
  __Pyx_RefNannyDeclarations
  PyObject *__pyx_t_1 = NULL;
  PyObject *__pyx_t_2 = NULL;
  PyObject *__pyx_t_3 = NULL;
  PyObject *__pyx_t_4 = NULL;
  PyObject *__pyx_t_5 = NULL;
  PyObject *__pyx_t_6 = NULL;
  PyObject *__pyx_t_7 = NULL;
  PyObject *__pyx_t_8 = NULL;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannySetupContext("output_embedding", 0);

  /* "dict_to_embedding.py":68
 * 
 * def output_embedding(G, E, outf):
 *     np.savez(outf, nodes=np.array(G.nodes()), edges=E)             # <<<<<<<<<<<<<<
 * 
 * #@profile
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_np); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_savez); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = PyTuple_New(1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_INCREF(__pyx_v_outf);
  __Pyx_GIVEREF(__pyx_v_outf);
  PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_v_outf);
  __pyx_t_3 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_np); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __pyx_t_6 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_array); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_6);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_v_G, __pyx_n_s_nodes); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __pyx_t_8 = NULL;
  if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_7))) {
    __pyx_t_8 = PyMethod_GET_SELF(__pyx_t_7);
    if (likely(__pyx_t_8)) {
      PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
      __Pyx_INCREF(__pyx_t_8);
      __Pyx_INCREF(function);
      __Pyx_DECREF_SET(__pyx_t_7, function);
    }
  }
  __pyx_t_5 = (__pyx_t_8) ? __Pyx_PyObject_CallOneArg(__pyx_t_7, __pyx_t_8) : __Pyx_PyObject_CallNoArg(__pyx_t_7);
  __Pyx_XDECREF(__pyx_t_8); __pyx_t_8 = 0;
  if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = NULL;
  if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_6))) {
    __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_6);
    if (likely(__pyx_t_7)) {
      PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_6);
      __Pyx_INCREF(__pyx_t_7);
      __Pyx_INCREF(function);
      __Pyx_DECREF_SET(__pyx_t_6, function);
    }
  }
  __pyx_t_4 = (__pyx_t_7) ? __Pyx_PyObject_Call2Args(__pyx_t_6, __pyx_t_7, __pyx_t_5) : __Pyx_PyObject_CallOneArg(__pyx_t_6, __pyx_t_5);
  __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_4);
  __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_nodes, __pyx_t_4) < 0) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_edges, __pyx_v_E) < 0) __PYX_ERR(0, 68, __pyx_L1_error)
  __pyx_t_4 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_t_1, __pyx_t_3); if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 68, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_4);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;

  /* "dict_to_embedding.py":67
 *     assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m
 * 
 * def output_embedding(G, E, outf):             # <<<<<<<<<<<<<<
 *     np.savez(outf, nodes=np.array(G.nodes()), edges=E)
 * 
 */

  /* function exit code */
  __pyx_r = Py_None; __Pyx_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1_error:;
  __Pyx_XDECREF(__pyx_t_1);
  __Pyx_XDECREF(__pyx_t_2);
  __Pyx_XDECREF(__pyx_t_3);
  __Pyx_XDECREF(__pyx_t_4);
  __Pyx_XDECREF(__pyx_t_5);
  __Pyx_XDECREF(__pyx_t_6);
  __Pyx_XDECREF(__pyx_t_7);
  __Pyx_XDECREF(__pyx_t_8);
  __Pyx_AddTraceback("dict_to_embedding.output_embedding", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  __Pyx_XGIVEREF(__pyx_r);
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

/* "dict_to_embedding.py":71
 * 
 * #@profile
 * def do_file():             # <<<<<<<<<<<<<<
 * 
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 */

/* Python wrapper */
static PyObject *__pyx_pw_17dict_to_embedding_7do_file(PyObject *__pyx_self, CYTHON_UNUSED PyObject *unused); /*proto*/
static PyMethodDef __pyx_mdef_17dict_to_embedding_7do_file = {"do_file", (PyCFunction)__pyx_pw_17dict_to_embedding_7do_file, METH_NOARGS, 0};
static PyObject *__pyx_pw_17dict_to_embedding_7do_file(PyObject *__pyx_self, CYTHON_UNUSED PyObject *unused) {
  PyObject *__pyx_r = 0;
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("do_file (wrapper)", 0);
  __pyx_r = __pyx_pf_17dict_to_embedding_6do_file(__pyx_self);

  /* function exit code */
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyObject *__pyx_pf_17dict_to_embedding_6do_file(CYTHON_UNUSED PyObject *__pyx_self) {
  PyObject *__pyx_v_G = NULL;
  PyObject *__pyx_v_scipy = NULL;
  PyObject *__pyx_v_M = NULL;
  PyObject *__pyx_v_m = NULL;
  PyObject *__pyx_v_features_matrix = NULL;
  PyObject *__pyx_v_embeddings = NULL;
  PyObject *__pyx_v_suffix = NULL;
  PyObject *__pyx_v_prefix = NULL;
  PyObject *__pyx_v_outf = NULL;
  PyObject *__pyx_v_i = NULL;
  PyObject *__pyx_r = NULL;
  __Pyx_RefNannyDeclarations
  PyObject *__pyx_t_1 = NULL;
  PyObject *__pyx_t_2 = NULL;
  int __pyx_t_3;
  int __pyx_t_4;
  PyObject *__pyx_t_5 = NULL;
  PyObject *__pyx_t_6 = NULL;
  PyObject *__pyx_t_7 = NULL;
  PyObject *__pyx_t_8 = NULL;
  int __pyx_t_9;
  PyObject *__pyx_t_10 = NULL;
  Py_ssize_t __pyx_t_11;
  PyObject *(*__pyx_t_12)(PyObject *);
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannySetupContext("do_file", 0);

  /* "dict_to_embedding.py":75
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 * 
 *     if not args.input_edge_list is None:             # <<<<<<<<<<<<<<
 *         # G = cg.read_edgelist(args.input, sep=args.delimiter, directed=False, quoting=3, prefix='X')
 *         G = cg.read_edgelist(args.input_edge_list, sep=args.delimiter, quoting=3, prefix='X')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 75, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_input_edge_list); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 75, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_3 = (__pyx_t_2 != Py_None);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_4 = (__pyx_t_3 != 0);
  if (__pyx_t_4) {

    /* "dict_to_embedding.py":77
 *     if not args.input_edge_list is None:
 *         # G = cg.read_edgelist(args.input, sep=args.delimiter, directed=False, quoting=3, prefix='X')
 *         G = cg.read_edgelist(args.input_edge_list, sep=args.delimiter, quoting=3, prefix='X')             # <<<<<<<<<<<<<<
 *         # model = nodevectors.GGVec()
 *     else:
 */
    __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_cg); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_read_edgelist); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_args); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_input_edge_list); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_t_2 = PyTuple_New(1); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_GIVEREF(__pyx_t_5);
    PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_5);
    __pyx_t_5 = 0;
    __pyx_t_5 = __Pyx_PyDict_NewPresized(3); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_GetModuleGlobalName(__pyx_t_6, __pyx_n_s_args); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_6, __pyx_n_s_delimiter); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    if (PyDict_SetItem(__pyx_t_5, __pyx_n_s_sep, __pyx_t_7) < 0) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (PyDict_SetItem(__pyx_t_5, __pyx_n_s_quoting, __pyx_int_3) < 0) __PYX_ERR(0, 77, __pyx_L1_error)
    if (PyDict_SetItem(__pyx_t_5, __pyx_n_s_prefix, __pyx_n_s_X) < 0) __PYX_ERR(0, 77, __pyx_L1_error)
    __pyx_t_7 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_t_2, __pyx_t_5); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 77, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_v_G = __pyx_t_7;
    __pyx_t_7 = 0;

    /* "dict_to_embedding.py":75
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 * 
 *     if not args.input_edge_list is None:             # <<<<<<<<<<<<<<
 *         # G = cg.read_edgelist(args.input, sep=args.delimiter, directed=False, quoting=3, prefix='X')
 *         G = cg.read_edgelist(args.input_edge_list, sep=args.delimiter, quoting=3, prefix='X')
 */
    goto __pyx_L3;
  }

  /* "dict_to_embedding.py":81
 *     else:
 *         #print('# about to load graph: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *         import scipy.sparse
 */
  /*else*/ {
    __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_sys); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 81, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_stderr); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 81, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_flush); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 81, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_t_2 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_5))) {
      __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_5);
      if (likely(__pyx_t_2)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_5);
        __Pyx_INCREF(__pyx_t_2);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_5, function);
      }
    }
    __pyx_t_7 = (__pyx_t_2) ? __Pyx_PyObject_CallOneArg(__pyx_t_5, __pyx_t_2) : __Pyx_PyObject_CallNoArg(__pyx_t_5);
    __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
    if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 81, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;

    /* "dict_to_embedding.py":83
 *         sys.stderr.flush()
 * 
 *         import scipy.sparse             # <<<<<<<<<<<<<<
 *         # import nextworkx as nx
 *         M = scipy.sparse.load_npz(args.input_graph)
 */
    __pyx_t_7 = __Pyx_Import(__pyx_n_s_scipy_sparse, 0, -1); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 83, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __pyx_v_scipy = __pyx_t_7;
    __pyx_t_7 = 0;

    /* "dict_to_embedding.py":85
 *         import scipy.sparse
 *         # import nextworkx as nx
 *         M = scipy.sparse.load_npz(args.input_graph)             # <<<<<<<<<<<<<<
 * 
 *         #print('# transpose = %s: %0.2f' % (str(args.transpose), time.time() - t0), file=sys.stderr)
 */
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_v_scipy, __pyx_n_s_sparse); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 85, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_load_npz); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 85, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_args); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 85, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_input_graph); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 85, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_t_5 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_2))) {
      __pyx_t_5 = PyMethod_GET_SELF(__pyx_t_2);
      if (likely(__pyx_t_5)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_2);
        __Pyx_INCREF(__pyx_t_5);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_2, function);
      }
    }
    __pyx_t_7 = (__pyx_t_5) ? __Pyx_PyObject_Call2Args(__pyx_t_2, __pyx_t_5, __pyx_t_1) : __Pyx_PyObject_CallOneArg(__pyx_t_2, __pyx_t_1);
    __Pyx_XDECREF(__pyx_t_5); __pyx_t_5 = 0;
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 85, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_v_M = __pyx_t_7;
    __pyx_t_7 = 0;

    /* "dict_to_embedding.py":89
 *         #print('# transpose = %s: %0.2f' % (str(args.transpose), time.time() - t0), file=sys.stderr)
 * 
 *         if args.transpose:             # <<<<<<<<<<<<<<
 *             M = M.T
 * 
 */
    __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_args); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 89, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_transpose); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 89, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_4 = __Pyx_PyObject_IsTrue(__pyx_t_2); if (unlikely(__pyx_t_4 < 0)) __PYX_ERR(0, 89, __pyx_L1_error)
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    if (__pyx_t_4) {

      /* "dict_to_embedding.py":90
 * 
 *         if args.transpose:
 *             M = M.T             # <<<<<<<<<<<<<<
 * 
 *         #print('# about to convert to csr_matrix: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
      __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_v_M, __pyx_n_s_T); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 90, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_2);
      __Pyx_DECREF_SET(__pyx_v_M, __pyx_t_2);
      __pyx_t_2 = 0;

      /* "dict_to_embedding.py":89
 *         #print('# transpose = %s: %0.2f' % (str(args.transpose), time.time() - t0), file=sys.stderr)
 * 
 *         if args.transpose:             # <<<<<<<<<<<<<<
 *             M = M.T
 * 
 */
    }

    /* "dict_to_embedding.py":93
 * 
 *         #print('# about to convert to csr_matrix: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *         M = scipy.sparse.csr_matrix(M)
 */
    __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_sys); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 93, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_stderr); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 93, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_flush); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 93, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_7))) {
      __pyx_t_1 = PyMethod_GET_SELF(__pyx_t_7);
      if (likely(__pyx_t_1)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
        __Pyx_INCREF(__pyx_t_1);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_7, function);
      }
    }
    __pyx_t_2 = (__pyx_t_1) ? __Pyx_PyObject_CallOneArg(__pyx_t_7, __pyx_t_1) : __Pyx_PyObject_CallNoArg(__pyx_t_7);
    __Pyx_XDECREF(__pyx_t_1); __pyx_t_1 = 0;
    if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 93, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;

    /* "dict_to_embedding.py":95
 *         sys.stderr.flush()
 * 
 *         M = scipy.sparse.csr_matrix(M)             # <<<<<<<<<<<<<<
 *         # M2 = nx.from_scipy_sparse_matrix(M)
 * 
 */
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_v_scipy, __pyx_n_s_sparse); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 95, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_csr_matrix); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 95, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_7 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_7)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_7);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_2 = (__pyx_t_7) ? __Pyx_PyObject_Call2Args(__pyx_t_1, __pyx_t_7, __pyx_v_M) : __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_v_M);
    __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 95, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF_SET(__pyx_v_M, __pyx_t_2);
    __pyx_t_2 = 0;

    /* "dict_to_embedding.py":99
 * 
 *         #print('# enforcing symmetry: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *         M += M.T
 */
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_sys); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 99, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_stderr); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 99, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_flush); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 99, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_7 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_7)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_7);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_2 = (__pyx_t_7) ? __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_t_7) : __Pyx_PyObject_CallNoArg(__pyx_t_1);
    __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 99, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;

    /* "dict_to_embedding.py":101
 *         sys.stderr.flush()
 * 
 *         M += M.T             # <<<<<<<<<<<<<<
 * 
 *         #print('# about to convert to csrgraph: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_v_M, __pyx_n_s_T); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 101, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_1 = PyNumber_InPlaceAdd(__pyx_v_M, __pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 101, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_DECREF_SET(__pyx_v_M, __pyx_t_1);
    __pyx_t_1 = 0;

    /* "dict_to_embedding.py":104
 * 
 *         #print('# about to convert to csrgraph: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *         G = cg.csrgraph(M)
 */
    __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_sys); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 104, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_stderr); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 104, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_flush); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 104, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_7 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_2))) {
      __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_2);
      if (likely(__pyx_t_7)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_2);
        __Pyx_INCREF(__pyx_t_7);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_2, function);
      }
    }
    __pyx_t_1 = (__pyx_t_7) ? __Pyx_PyObject_CallOneArg(__pyx_t_2, __pyx_t_7) : __Pyx_PyObject_CallNoArg(__pyx_t_2);
    __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 104, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

    /* "dict_to_embedding.py":106
 *         sys.stderr.flush()
 * 
 *         G = cg.csrgraph(M)             # <<<<<<<<<<<<<<
 * 
 *     #print('# loading graph: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
    __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_cg); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 106, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_csrgraph); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 106, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    __pyx_t_2 = NULL;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_7))) {
      __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_7);
      if (likely(__pyx_t_2)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
        __Pyx_INCREF(__pyx_t_2);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_7, function);
      }
    }
    __pyx_t_1 = (__pyx_t_2) ? __Pyx_PyObject_Call2Args(__pyx_t_7, __pyx_t_2, __pyx_v_M) : __Pyx_PyObject_CallOneArg(__pyx_t_7, __pyx_v_M);
    __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
    if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 106, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_v_G = __pyx_t_1;
    __pyx_t_1 = 0;
  }
  __pyx_L3:;

  /* "dict_to_embedding.py":109
 * 
 *     #print('# loading graph: %0.2f' % (time.time() - t0), file=sys.stderr)
 *     sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *     # I DON'T KNOW WHY, but this doesn't seem to work
 */
  __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_sys); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 109, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_stderr); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 109, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_flush); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 109, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = NULL;
  if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_7))) {
    __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_7);
    if (likely(__pyx_t_2)) {
      PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
      __Pyx_INCREF(__pyx_t_2);
      __Pyx_INCREF(function);
      __Pyx_DECREF_SET(__pyx_t_7, function);
    }
  }
  __pyx_t_1 = (__pyx_t_2) ? __Pyx_PyObject_CallOneArg(__pyx_t_7, __pyx_t_2) : __Pyx_PyObject_CallNoArg(__pyx_t_7);
  __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
  if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 109, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":116
 *     # Thus, we can split the job into two pieces
 *     # This is important because the long queue has a limit on time
 *     if args.method == 'ProNE_prefactorization':             # <<<<<<<<<<<<<<
 *         #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 *         m = method2model()
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 116, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_method); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 116, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_4 = (__Pyx_PyString_Equals(__pyx_t_7, __pyx_n_s_ProNE_prefactorization, Py_EQ)); if (unlikely(__pyx_t_4 < 0)) __PYX_ERR(0, 116, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  if (__pyx_t_4) {

    /* "dict_to_embedding.py":118
 *     if args.method == 'ProNE_prefactorization':
 *         #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 *         m = method2model()             # <<<<<<<<<<<<<<
 *         features_matrix = m.pre_factorization(G.mat, m.n_components, m.exponent)
 *         #print('# pre_factorization time: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_method2model); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 118, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_2 = NULL;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_2)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_2);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_7 = (__pyx_t_2) ? __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_t_2) : __Pyx_PyObject_CallNoArg(__pyx_t_1);
    __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
    if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 118, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_v_m = __pyx_t_7;
    __pyx_t_7 = 0;

    /* "dict_to_embedding.py":119
 *         #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 *         m = method2model()
 *         features_matrix = m.pre_factorization(G.mat, m.n_components, m.exponent)             # <<<<<<<<<<<<<<
 *         #print('# pre_factorization time: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         np.save(args.output + '.K' + str(args.components), features_matrix)
 */
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_v_m, __pyx_n_s_pre_factorization); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 119, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_v_G, __pyx_n_s_mat); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 119, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_v_m, __pyx_n_s_n_components); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 119, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_6 = __Pyx_PyObject_GetAttrStr(__pyx_v_m, __pyx_n_s_exponent); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 119, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __pyx_t_8 = NULL;
    __pyx_t_9 = 0;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_8 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_8)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_8);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
        __pyx_t_9 = 1;
      }
    }
    #if CYTHON_FAST_PYCALL
    if (PyFunction_Check(__pyx_t_1)) {
      PyObject *__pyx_temp[4] = {__pyx_t_8, __pyx_t_2, __pyx_t_5, __pyx_t_6};
      __pyx_t_7 = __Pyx_PyFunction_FastCall(__pyx_t_1, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 119, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_8); __pyx_t_8 = 0;
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
      __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    } else
    #endif
    #if CYTHON_FAST_PYCCALL
    if (__Pyx_PyFastCFunction_Check(__pyx_t_1)) {
      PyObject *__pyx_temp[4] = {__pyx_t_8, __pyx_t_2, __pyx_t_5, __pyx_t_6};
      __pyx_t_7 = __Pyx_PyCFunction_FastCall(__pyx_t_1, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 119, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_8); __pyx_t_8 = 0;
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
      __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    } else
    #endif
    {
      __pyx_t_10 = PyTuple_New(3+__pyx_t_9); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 119, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_10);
      if (__pyx_t_8) {
        __Pyx_GIVEREF(__pyx_t_8); PyTuple_SET_ITEM(__pyx_t_10, 0, __pyx_t_8); __pyx_t_8 = NULL;
      }
      __Pyx_GIVEREF(__pyx_t_2);
      PyTuple_SET_ITEM(__pyx_t_10, 0+__pyx_t_9, __pyx_t_2);
      __Pyx_GIVEREF(__pyx_t_5);
      PyTuple_SET_ITEM(__pyx_t_10, 1+__pyx_t_9, __pyx_t_5);
      __Pyx_GIVEREF(__pyx_t_6);
      PyTuple_SET_ITEM(__pyx_t_10, 2+__pyx_t_9, __pyx_t_6);
      __pyx_t_2 = 0;
      __pyx_t_5 = 0;
      __pyx_t_6 = 0;
      __pyx_t_7 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_t_10, NULL); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 119, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
    }
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_v_features_matrix = __pyx_t_7;
    __pyx_t_7 = 0;

    /* "dict_to_embedding.py":121
 *         features_matrix = m.pre_factorization(G.mat, m.n_components, m.exponent)
 *         #print('# pre_factorization time: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         np.save(args.output + '.K' + str(args.components), features_matrix)             # <<<<<<<<<<<<<<
 *         return
 * 
 */
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_np); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_10 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_save); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_10);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_6 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_output); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = PyNumber_Add(__pyx_t_6, __pyx_kp_s_K); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_6, __pyx_n_s_args); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_t_6, __pyx_n_s_components); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    __pyx_t_6 = __Pyx_PyObject_CallOneArg(((PyObject *)(&PyString_Type)), __pyx_t_5); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_t_5 = PyNumber_Add(__pyx_t_1, __pyx_t_6); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 121, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    __pyx_t_6 = NULL;
    __pyx_t_9 = 0;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_10))) {
      __pyx_t_6 = PyMethod_GET_SELF(__pyx_t_10);
      if (likely(__pyx_t_6)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_10);
        __Pyx_INCREF(__pyx_t_6);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_10, function);
        __pyx_t_9 = 1;
      }
    }
    #if CYTHON_FAST_PYCALL
    if (PyFunction_Check(__pyx_t_10)) {
      PyObject *__pyx_temp[3] = {__pyx_t_6, __pyx_t_5, __pyx_v_features_matrix};
      __pyx_t_7 = __Pyx_PyFunction_FastCall(__pyx_t_10, __pyx_temp+1-__pyx_t_9, 2+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 121, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_6); __pyx_t_6 = 0;
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    } else
    #endif
    #if CYTHON_FAST_PYCCALL
    if (__Pyx_PyFastCFunction_Check(__pyx_t_10)) {
      PyObject *__pyx_temp[3] = {__pyx_t_6, __pyx_t_5, __pyx_v_features_matrix};
      __pyx_t_7 = __Pyx_PyCFunction_FastCall(__pyx_t_10, __pyx_temp+1-__pyx_t_9, 2+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 121, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_6); __pyx_t_6 = 0;
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    } else
    #endif
    {
      __pyx_t_1 = PyTuple_New(2+__pyx_t_9); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 121, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_1);
      if (__pyx_t_6) {
        __Pyx_GIVEREF(__pyx_t_6); PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_6); __pyx_t_6 = NULL;
      }
      __Pyx_GIVEREF(__pyx_t_5);
      PyTuple_SET_ITEM(__pyx_t_1, 0+__pyx_t_9, __pyx_t_5);
      __Pyx_INCREF(__pyx_v_features_matrix);
      __Pyx_GIVEREF(__pyx_v_features_matrix);
      PyTuple_SET_ITEM(__pyx_t_1, 1+__pyx_t_9, __pyx_v_features_matrix);
      __pyx_t_5 = 0;
      __pyx_t_7 = __Pyx_PyObject_Call(__pyx_t_10, __pyx_t_1, NULL); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 121, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    }
    __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;

    /* "dict_to_embedding.py":122
 *         #print('# pre_factorization time: %0.2f' % (time.time() - t0), file=sys.stderr)
 *         np.save(args.output + '.K' + str(args.components), features_matrix)
 *         return             # <<<<<<<<<<<<<<
 * 
 *     if args.features_matrix is None:
 */
    __Pyx_XDECREF(__pyx_r);
    __pyx_r = Py_None; __Pyx_INCREF(Py_None);
    goto __pyx_L0;

    /* "dict_to_embedding.py":116
 *     # Thus, we can split the job into two pieces
 *     # This is important because the long queue has a limit on time
 *     if args.method == 'ProNE_prefactorization':             # <<<<<<<<<<<<<<
 *         #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 *         m = method2model()
 */
  }

  /* "dict_to_embedding.py":124
 *         return
 * 
 *     if args.features_matrix is None:             # <<<<<<<<<<<<<<
 *         embeddings = method2model().fit_transform(G)
 *     else: embeddings = method2model().fit_transform(G, features_matrix=np.load(args.features_matrix))
 */
  __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_args); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 124, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __pyx_t_10 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_features_matrix); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 124, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_4 = (__pyx_t_10 == Py_None);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_3 = (__pyx_t_4 != 0);
  if (__pyx_t_3) {

    /* "dict_to_embedding.py":125
 * 
 *     if args.features_matrix is None:
 *         embeddings = method2model().fit_transform(G)             # <<<<<<<<<<<<<<
 *     else: embeddings = method2model().fit_transform(G, features_matrix=np.load(args.features_matrix))
 * 
 */
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_method2model); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 125, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_5 = NULL;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_5 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_5)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_5);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_7 = (__pyx_t_5) ? __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_t_5) : __Pyx_PyObject_CallNoArg(__pyx_t_1);
    __Pyx_XDECREF(__pyx_t_5); __pyx_t_5 = 0;
    if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 125, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_fit_transform); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 125, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_t_7 = NULL;
    if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_7)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_7);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_10 = (__pyx_t_7) ? __Pyx_PyObject_Call2Args(__pyx_t_1, __pyx_t_7, __pyx_v_G) : __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_v_G);
    __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 125, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_10);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_v_embeddings = __pyx_t_10;
    __pyx_t_10 = 0;

    /* "dict_to_embedding.py":124
 *         return
 * 
 *     if args.features_matrix is None:             # <<<<<<<<<<<<<<
 *         embeddings = method2model().fit_transform(G)
 *     else: embeddings = method2model().fit_transform(G, features_matrix=np.load(args.features_matrix))
 */
    goto __pyx_L6;
  }

  /* "dict_to_embedding.py":126
 *     if args.features_matrix is None:
 *         embeddings = method2model().fit_transform(G)
 *     else: embeddings = method2model().fit_transform(G, features_matrix=np.load(args.features_matrix))             # <<<<<<<<<<<<<<
 * 
 *     #print('dict_to_embedding: # fitting model: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
  /*else*/ {
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_method2model); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_7 = NULL;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_1))) {
      __pyx_t_7 = PyMethod_GET_SELF(__pyx_t_1);
      if (likely(__pyx_t_7)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_1);
        __Pyx_INCREF(__pyx_t_7);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_1, function);
      }
    }
    __pyx_t_10 = (__pyx_t_7) ? __Pyx_PyObject_CallOneArg(__pyx_t_1, __pyx_t_7) : __Pyx_PyObject_CallNoArg(__pyx_t_1);
    __Pyx_XDECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_10);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_10, __pyx_n_s_fit_transform); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
    __pyx_t_10 = PyTuple_New(1); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_10);
    __Pyx_INCREF(__pyx_v_G);
    __Pyx_GIVEREF(__pyx_v_G);
    PyTuple_SET_ITEM(__pyx_t_10, 0, __pyx_v_G);
    __pyx_t_7 = __Pyx_PyDict_NewPresized(1); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __Pyx_GetModuleGlobalName(__pyx_t_6, __pyx_n_s_np); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_6, __pyx_n_s_load); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_2);
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_6, __pyx_n_s_args); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_6);
    __pyx_t_8 = __Pyx_PyObject_GetAttrStr(__pyx_t_6, __pyx_n_s_features_matrix); if (unlikely(!__pyx_t_8)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_8);
    __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
    __pyx_t_6 = NULL;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_2))) {
      __pyx_t_6 = PyMethod_GET_SELF(__pyx_t_2);
      if (likely(__pyx_t_6)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_2);
        __Pyx_INCREF(__pyx_t_6);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_2, function);
      }
    }
    __pyx_t_5 = (__pyx_t_6) ? __Pyx_PyObject_Call2Args(__pyx_t_2, __pyx_t_6, __pyx_t_8) : __Pyx_PyObject_CallOneArg(__pyx_t_2, __pyx_t_8);
    __Pyx_XDECREF(__pyx_t_6); __pyx_t_6 = 0;
    __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
    if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
    if (PyDict_SetItem(__pyx_t_7, __pyx_n_s_features_matrix, __pyx_t_5) < 0) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __pyx_t_5 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_t_10, __pyx_t_7); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 126, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    __pyx_v_embeddings = __pyx_t_5;
    __pyx_t_5 = 0;
  }
  __pyx_L6:;

  /* "dict_to_embedding.py":129
 * 
 *     #print('dict_to_embedding: # fitting model: %0.2f' % (time.time() - t0), file=sys.stderr)
 *     sys.stderr.flush()             # <<<<<<<<<<<<<<
 * 
 *     suffix = args.method + '.K' + str(args.components) + '.T' + str(args.threads) + '.O' + str(args.order) + '.w2v'
 */
  __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_sys); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 129, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __pyx_t_10 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_stderr); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 129, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_10, __pyx_n_s_flush); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 129, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_10 = NULL;
  if (CYTHON_UNPACK_METHODS && likely(PyMethod_Check(__pyx_t_7))) {
    __pyx_t_10 = PyMethod_GET_SELF(__pyx_t_7);
    if (likely(__pyx_t_10)) {
      PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
      __Pyx_INCREF(__pyx_t_10);
      __Pyx_INCREF(function);
      __Pyx_DECREF_SET(__pyx_t_7, function);
    }
  }
  __pyx_t_5 = (__pyx_t_10) ? __Pyx_PyObject_CallOneArg(__pyx_t_7, __pyx_t_10) : __Pyx_PyObject_CallNoArg(__pyx_t_7);
  __Pyx_XDECREF(__pyx_t_10); __pyx_t_10 = 0;
  if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 129, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;

  /* "dict_to_embedding.py":131
 *     sys.stderr.flush()
 * 
 *     suffix = args.method + '.K' + str(args.components) + '.T' + str(args.threads) + '.O' + str(args.order) + '.w2v'             # <<<<<<<<<<<<<<
 *     prefix = strip_suffix(args.output, ['.txt', '.txt2'])
 *     outf = prefix + '.' +  suffix
 */
  __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_args); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_method); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_5 = PyNumber_Add(__pyx_t_7, __pyx_kp_s_K); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_args); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __pyx_t_10 = __Pyx_PyObject_GetAttrStr(__pyx_t_7, __pyx_n_s_components); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = __Pyx_PyObject_CallOneArg(((PyObject *)(&PyString_Type)), __pyx_t_10); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_10 = PyNumber_Add(__pyx_t_5, __pyx_t_7); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = PyNumber_Add(__pyx_t_10, __pyx_kp_s_T_2); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __Pyx_GetModuleGlobalName(__pyx_t_10, __pyx_n_s_args); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_t_10, __pyx_n_s_threads); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_10 = __Pyx_PyObject_CallOneArg(((PyObject *)(&PyString_Type)), __pyx_t_5); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_5 = PyNumber_Add(__pyx_t_7, __pyx_t_10); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_10 = PyNumber_Add(__pyx_t_5, __pyx_kp_s_O); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_args); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __pyx_t_7 = __Pyx_PyObject_GetAttrStr(__pyx_t_5, __pyx_n_s_order); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_5 = __Pyx_PyObject_CallOneArg(((PyObject *)(&PyString_Type)), __pyx_t_7); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_t_7 = PyNumber_Add(__pyx_t_10, __pyx_t_5); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_t_5 = PyNumber_Add(__pyx_t_7, __pyx_kp_s_w2v); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 131, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_v_suffix = __pyx_t_5;
  __pyx_t_5 = 0;

  /* "dict_to_embedding.py":132
 * 
 *     suffix = args.method + '.K' + str(args.components) + '.T' + str(args.threads) + '.O' + str(args.order) + '.w2v'
 *     prefix = strip_suffix(args.output, ['.txt', '.txt2'])             # <<<<<<<<<<<<<<
 *     outf = prefix + '.' +  suffix
 * 
 */
  __Pyx_GetModuleGlobalName(__pyx_t_7, __pyx_n_s_strip_suffix); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 132, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_GetModuleGlobalName(__pyx_t_10, __pyx_n_s_args); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 132, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_10, __pyx_n_s_output); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 132, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  __pyx_t_10 = PyList_New(2); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 132, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_10);
  __Pyx_INCREF(__pyx_kp_s_txt);
  __Pyx_GIVEREF(__pyx_kp_s_txt);
  PyList_SET_ITEM(__pyx_t_10, 0, __pyx_kp_s_txt);
  __Pyx_INCREF(__pyx_kp_s_txt2);
  __Pyx_GIVEREF(__pyx_kp_s_txt2);
  PyList_SET_ITEM(__pyx_t_10, 1, __pyx_kp_s_txt2);
  __pyx_t_2 = NULL;
  __pyx_t_9 = 0;
  if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_7))) {
    __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_7);
    if (likely(__pyx_t_2)) {
      PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_7);
      __Pyx_INCREF(__pyx_t_2);
      __Pyx_INCREF(function);
      __Pyx_DECREF_SET(__pyx_t_7, function);
      __pyx_t_9 = 1;
    }
  }
  #if CYTHON_FAST_PYCALL
  if (PyFunction_Check(__pyx_t_7)) {
    PyObject *__pyx_temp[3] = {__pyx_t_2, __pyx_t_1, __pyx_t_10};
    __pyx_t_5 = __Pyx_PyFunction_FastCall(__pyx_t_7, __pyx_temp+1-__pyx_t_9, 2+__pyx_t_9); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 132, __pyx_L1_error)
    __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  } else
  #endif
  #if CYTHON_FAST_PYCCALL
  if (__Pyx_PyFastCFunction_Check(__pyx_t_7)) {
    PyObject *__pyx_temp[3] = {__pyx_t_2, __pyx_t_1, __pyx_t_10};
    __pyx_t_5 = __Pyx_PyCFunction_FastCall(__pyx_t_7, __pyx_temp+1-__pyx_t_9, 2+__pyx_t_9); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 132, __pyx_L1_error)
    __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
  } else
  #endif
  {
    __pyx_t_8 = PyTuple_New(2+__pyx_t_9); if (unlikely(!__pyx_t_8)) __PYX_ERR(0, 132, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_8);
    if (__pyx_t_2) {
      __Pyx_GIVEREF(__pyx_t_2); PyTuple_SET_ITEM(__pyx_t_8, 0, __pyx_t_2); __pyx_t_2 = NULL;
    }
    __Pyx_GIVEREF(__pyx_t_1);
    PyTuple_SET_ITEM(__pyx_t_8, 0+__pyx_t_9, __pyx_t_1);
    __Pyx_GIVEREF(__pyx_t_10);
    PyTuple_SET_ITEM(__pyx_t_8, 1+__pyx_t_9, __pyx_t_10);
    __pyx_t_1 = 0;
    __pyx_t_10 = 0;
    __pyx_t_5 = __Pyx_PyObject_Call(__pyx_t_7, __pyx_t_8, NULL); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 132, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
  }
  __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  __pyx_v_prefix = __pyx_t_5;
  __pyx_t_5 = 0;

  /* "dict_to_embedding.py":133
 *     suffix = args.method + '.K' + str(args.components) + '.T' + str(args.threads) + '.O' + str(args.order) + '.w2v'
 *     prefix = strip_suffix(args.output, ['.txt', '.txt2'])
 *     outf = prefix + '.' +  suffix             # <<<<<<<<<<<<<<
 * 
 *     if not isinstance(embeddings, list):
 */
  __pyx_t_5 = PyNumber_Add(__pyx_v_prefix, __pyx_kp_s_); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 133, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_5);
  __pyx_t_7 = PyNumber_Add(__pyx_t_5, __pyx_v_suffix); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 133, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_7);
  __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
  __pyx_v_outf = __pyx_t_7;
  __pyx_t_7 = 0;

  /* "dict_to_embedding.py":135
 *     outf = prefix + '.' +  suffix
 * 
 *     if not isinstance(embeddings, list):             # <<<<<<<<<<<<<<
 *         output_embedding(G, embeddings, outf)
 *     else:
 */
  __pyx_t_3 = PyList_Check(__pyx_v_embeddings); 
  __pyx_t_4 = ((!(__pyx_t_3 != 0)) != 0);
  if (__pyx_t_4) {

    /* "dict_to_embedding.py":136
 * 
 *     if not isinstance(embeddings, list):
 *         output_embedding(G, embeddings, outf)             # <<<<<<<<<<<<<<
 *     else:
 *         for i in range(len(embeddings)):
 */
    __Pyx_GetModuleGlobalName(__pyx_t_5, __pyx_n_s_output_embedding); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 136, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __pyx_t_8 = NULL;
    __pyx_t_9 = 0;
    if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_5))) {
      __pyx_t_8 = PyMethod_GET_SELF(__pyx_t_5);
      if (likely(__pyx_t_8)) {
        PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_5);
        __Pyx_INCREF(__pyx_t_8);
        __Pyx_INCREF(function);
        __Pyx_DECREF_SET(__pyx_t_5, function);
        __pyx_t_9 = 1;
      }
    }
    #if CYTHON_FAST_PYCALL
    if (PyFunction_Check(__pyx_t_5)) {
      PyObject *__pyx_temp[4] = {__pyx_t_8, __pyx_v_G, __pyx_v_embeddings, __pyx_v_outf};
      __pyx_t_7 = __Pyx_PyFunction_FastCall(__pyx_t_5, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 136, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_8); __pyx_t_8 = 0;
      __Pyx_GOTREF(__pyx_t_7);
    } else
    #endif
    #if CYTHON_FAST_PYCCALL
    if (__Pyx_PyFastCFunction_Check(__pyx_t_5)) {
      PyObject *__pyx_temp[4] = {__pyx_t_8, __pyx_v_G, __pyx_v_embeddings, __pyx_v_outf};
      __pyx_t_7 = __Pyx_PyCFunction_FastCall(__pyx_t_5, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 136, __pyx_L1_error)
      __Pyx_XDECREF(__pyx_t_8); __pyx_t_8 = 0;
      __Pyx_GOTREF(__pyx_t_7);
    } else
    #endif
    {
      __pyx_t_10 = PyTuple_New(3+__pyx_t_9); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 136, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_10);
      if (__pyx_t_8) {
        __Pyx_GIVEREF(__pyx_t_8); PyTuple_SET_ITEM(__pyx_t_10, 0, __pyx_t_8); __pyx_t_8 = NULL;
      }
      __Pyx_INCREF(__pyx_v_G);
      __Pyx_GIVEREF(__pyx_v_G);
      PyTuple_SET_ITEM(__pyx_t_10, 0+__pyx_t_9, __pyx_v_G);
      __Pyx_INCREF(__pyx_v_embeddings);
      __Pyx_GIVEREF(__pyx_v_embeddings);
      PyTuple_SET_ITEM(__pyx_t_10, 1+__pyx_t_9, __pyx_v_embeddings);
      __Pyx_INCREF(__pyx_v_outf);
      __Pyx_GIVEREF(__pyx_v_outf);
      PyTuple_SET_ITEM(__pyx_t_10, 2+__pyx_t_9, __pyx_v_outf);
      __pyx_t_7 = __Pyx_PyObject_Call(__pyx_t_5, __pyx_t_10, NULL); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 136, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_7);
      __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
    }
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;

    /* "dict_to_embedding.py":135
 *     outf = prefix + '.' +  suffix
 * 
 *     if not isinstance(embeddings, list):             # <<<<<<<<<<<<<<
 *         output_embedding(G, embeddings, outf)
 *     else:
 */
    goto __pyx_L7;
  }

  /* "dict_to_embedding.py":138
 *         output_embedding(G, embeddings, outf)
 *     else:
 *         for i in range(len(embeddings)):             # <<<<<<<<<<<<<<
 *             output_embedding(G, embeddings[i], outf + '.' + str(i))
 * 
 */
  /*else*/ {
    __pyx_t_11 = PyObject_Length(__pyx_v_embeddings); if (unlikely(__pyx_t_11 == ((Py_ssize_t)-1))) __PYX_ERR(0, 138, __pyx_L1_error)
    __pyx_t_7 = PyInt_FromSsize_t(__pyx_t_11); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 138, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_7);
    __pyx_t_5 = __Pyx_PyObject_CallOneArg(__pyx_builtin_range, __pyx_t_7); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 138, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_5);
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
    if (likely(PyList_CheckExact(__pyx_t_5)) || PyTuple_CheckExact(__pyx_t_5)) {
      __pyx_t_7 = __pyx_t_5; __Pyx_INCREF(__pyx_t_7); __pyx_t_11 = 0;
      __pyx_t_12 = NULL;
    } else {
      __pyx_t_11 = -1; __pyx_t_7 = PyObject_GetIter(__pyx_t_5); if (unlikely(!__pyx_t_7)) __PYX_ERR(0, 138, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_7);
      __pyx_t_12 = Py_TYPE(__pyx_t_7)->tp_iternext; if (unlikely(!__pyx_t_12)) __PYX_ERR(0, 138, __pyx_L1_error)
    }
    __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
    for (;;) {
      if (likely(!__pyx_t_12)) {
        if (likely(PyList_CheckExact(__pyx_t_7))) {
          if (__pyx_t_11 >= PyList_GET_SIZE(__pyx_t_7)) break;
          #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
          __pyx_t_5 = PyList_GET_ITEM(__pyx_t_7, __pyx_t_11); __Pyx_INCREF(__pyx_t_5); __pyx_t_11++; if (unlikely(0 < 0)) __PYX_ERR(0, 138, __pyx_L1_error)
          #else
          __pyx_t_5 = PySequence_ITEM(__pyx_t_7, __pyx_t_11); __pyx_t_11++; if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 138, __pyx_L1_error)
          __Pyx_GOTREF(__pyx_t_5);
          #endif
        } else {
          if (__pyx_t_11 >= PyTuple_GET_SIZE(__pyx_t_7)) break;
          #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
          __pyx_t_5 = PyTuple_GET_ITEM(__pyx_t_7, __pyx_t_11); __Pyx_INCREF(__pyx_t_5); __pyx_t_11++; if (unlikely(0 < 0)) __PYX_ERR(0, 138, __pyx_L1_error)
          #else
          __pyx_t_5 = PySequence_ITEM(__pyx_t_7, __pyx_t_11); __pyx_t_11++; if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 138, __pyx_L1_error)
          __Pyx_GOTREF(__pyx_t_5);
          #endif
        }
      } else {
        __pyx_t_5 = __pyx_t_12(__pyx_t_7);
        if (unlikely(!__pyx_t_5)) {
          PyObject* exc_type = PyErr_Occurred();
          if (exc_type) {
            if (likely(__Pyx_PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration))) PyErr_Clear();
            else __PYX_ERR(0, 138, __pyx_L1_error)
          }
          break;
        }
        __Pyx_GOTREF(__pyx_t_5);
      }
      __Pyx_XDECREF_SET(__pyx_v_i, __pyx_t_5);
      __pyx_t_5 = 0;

      /* "dict_to_embedding.py":139
 *     else:
 *         for i in range(len(embeddings)):
 *             output_embedding(G, embeddings[i], outf + '.' + str(i))             # <<<<<<<<<<<<<<
 * 
 * do_file()
 */
      __Pyx_GetModuleGlobalName(__pyx_t_10, __pyx_n_s_output_embedding); if (unlikely(!__pyx_t_10)) __PYX_ERR(0, 139, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_10);
      __pyx_t_8 = __Pyx_PyObject_GetItem(__pyx_v_embeddings, __pyx_v_i); if (unlikely(!__pyx_t_8)) __PYX_ERR(0, 139, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_8);
      __pyx_t_1 = PyNumber_Add(__pyx_v_outf, __pyx_kp_s_); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 139, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_2 = __Pyx_PyObject_CallOneArg(((PyObject *)(&PyString_Type)), __pyx_v_i); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 139, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_2);
      __pyx_t_6 = PyNumber_Add(__pyx_t_1, __pyx_t_2); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 139, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_6);
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = NULL;
      __pyx_t_9 = 0;
      if (CYTHON_UNPACK_METHODS && unlikely(PyMethod_Check(__pyx_t_10))) {
        __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_10);
        if (likely(__pyx_t_2)) {
          PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_10);
          __Pyx_INCREF(__pyx_t_2);
          __Pyx_INCREF(function);
          __Pyx_DECREF_SET(__pyx_t_10, function);
          __pyx_t_9 = 1;
        }
      }
      #if CYTHON_FAST_PYCALL
      if (PyFunction_Check(__pyx_t_10)) {
        PyObject *__pyx_temp[4] = {__pyx_t_2, __pyx_v_G, __pyx_t_8, __pyx_t_6};
        __pyx_t_5 = __Pyx_PyFunction_FastCall(__pyx_t_10, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 139, __pyx_L1_error)
        __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
        __Pyx_GOTREF(__pyx_t_5);
        __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
        __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
      } else
      #endif
      #if CYTHON_FAST_PYCCALL
      if (__Pyx_PyFastCFunction_Check(__pyx_t_10)) {
        PyObject *__pyx_temp[4] = {__pyx_t_2, __pyx_v_G, __pyx_t_8, __pyx_t_6};
        __pyx_t_5 = __Pyx_PyCFunction_FastCall(__pyx_t_10, __pyx_temp+1-__pyx_t_9, 3+__pyx_t_9); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 139, __pyx_L1_error)
        __Pyx_XDECREF(__pyx_t_2); __pyx_t_2 = 0;
        __Pyx_GOTREF(__pyx_t_5);
        __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
        __Pyx_DECREF(__pyx_t_6); __pyx_t_6 = 0;
      } else
      #endif
      {
        __pyx_t_1 = PyTuple_New(3+__pyx_t_9); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 139, __pyx_L1_error)
        __Pyx_GOTREF(__pyx_t_1);
        if (__pyx_t_2) {
          __Pyx_GIVEREF(__pyx_t_2); PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_2); __pyx_t_2 = NULL;
        }
        __Pyx_INCREF(__pyx_v_G);
        __Pyx_GIVEREF(__pyx_v_G);
        PyTuple_SET_ITEM(__pyx_t_1, 0+__pyx_t_9, __pyx_v_G);
        __Pyx_GIVEREF(__pyx_t_8);
        PyTuple_SET_ITEM(__pyx_t_1, 1+__pyx_t_9, __pyx_t_8);
        __Pyx_GIVEREF(__pyx_t_6);
        PyTuple_SET_ITEM(__pyx_t_1, 2+__pyx_t_9, __pyx_t_6);
        __pyx_t_8 = 0;
        __pyx_t_6 = 0;
        __pyx_t_5 = __Pyx_PyObject_Call(__pyx_t_10, __pyx_t_1, NULL); if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 139, __pyx_L1_error)
        __Pyx_GOTREF(__pyx_t_5);
        __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      }
      __Pyx_DECREF(__pyx_t_10); __pyx_t_10 = 0;
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;

      /* "dict_to_embedding.py":138
 *         output_embedding(G, embeddings, outf)
 *     else:
 *         for i in range(len(embeddings)):             # <<<<<<<<<<<<<<
 *             output_embedding(G, embeddings[i], outf + '.' + str(i))
 * 
 */
    }
    __Pyx_DECREF(__pyx_t_7); __pyx_t_7 = 0;
  }
  __pyx_L7:;

  /* "dict_to_embedding.py":71
 * 
 * #@profile
 * def do_file():             # <<<<<<<<<<<<<<
 * 
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 */

  /* function exit code */
  __pyx_r = Py_None; __Pyx_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1_error:;
  __Pyx_XDECREF(__pyx_t_1);
  __Pyx_XDECREF(__pyx_t_2);
  __Pyx_XDECREF(__pyx_t_5);
  __Pyx_XDECREF(__pyx_t_6);
  __Pyx_XDECREF(__pyx_t_7);
  __Pyx_XDECREF(__pyx_t_8);
  __Pyx_XDECREF(__pyx_t_10);
  __Pyx_AddTraceback("dict_to_embedding.do_file", __pyx_clineno, __pyx_lineno, __pyx_filename);
  __pyx_r = NULL;
  __pyx_L0:;
  __Pyx_XDECREF(__pyx_v_G);
  __Pyx_XDECREF(__pyx_v_scipy);
  __Pyx_XDECREF(__pyx_v_M);
  __Pyx_XDECREF(__pyx_v_m);
  __Pyx_XDECREF(__pyx_v_features_matrix);
  __Pyx_XDECREF(__pyx_v_embeddings);
  __Pyx_XDECREF(__pyx_v_suffix);
  __Pyx_XDECREF(__pyx_v_prefix);
  __Pyx_XDECREF(__pyx_v_outf);
  __Pyx_XDECREF(__pyx_v_i);
  __Pyx_XGIVEREF(__pyx_r);
  __Pyx_RefNannyFinishContext();
  return __pyx_r;
}

static PyMethodDef __pyx_methods[] = {
  {0, 0, 0, 0}
};

#if PY_MAJOR_VERSION >= 3
#if CYTHON_PEP489_MULTI_PHASE_INIT
static PyObject* __pyx_pymod_create(PyObject *spec, PyModuleDef *def); /*proto*/
static int __pyx_pymod_exec_dict_to_embedding(PyObject* module); /*proto*/
static PyModuleDef_Slot __pyx_moduledef_slots[] = {
  {Py_mod_create, (void*)__pyx_pymod_create},
  {Py_mod_exec, (void*)__pyx_pymod_exec_dict_to_embedding},
  {0, NULL}
};
#endif

static struct PyModuleDef __pyx_moduledef = {
    PyModuleDef_HEAD_INIT,
    "dict_to_embedding",
    0, /* m_doc */
  #if CYTHON_PEP489_MULTI_PHASE_INIT
    0, /* m_size */
  #else
    -1, /* m_size */
  #endif
    __pyx_methods /* m_methods */,
  #if CYTHON_PEP489_MULTI_PHASE_INIT
    __pyx_moduledef_slots, /* m_slots */
  #else
    NULL, /* m_reload */
  #endif
    NULL, /* m_traverse */
    NULL, /* m_clear */
    NULL /* m_free */
};
#endif
#ifndef CYTHON_SMALL_CODE
#if defined(__clang__)
    #define CYTHON_SMALL_CODE
#elif defined(__GNUC__) && (__GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 3))
    #define CYTHON_SMALL_CODE __attribute__((cold))
#else
    #define CYTHON_SMALL_CODE
#endif
#endif

static __Pyx_StringTabEntry __pyx_string_tab[] = {
  {&__pyx_kp_s_, __pyx_k_, sizeof(__pyx_k_), 0, 0, 1, 0},
  {&__pyx_n_s_ArgumentParser, __pyx_k_ArgumentParser, sizeof(__pyx_k_ArgumentParser), 0, 0, 1, 1},
  {&__pyx_n_s_E, __pyx_k_E, sizeof(__pyx_k_E), 0, 0, 1, 1},
  {&__pyx_kp_s_F, __pyx_k_F, sizeof(__pyx_k_F), 0, 0, 1, 0},
  {&__pyx_n_s_G, __pyx_k_G, sizeof(__pyx_k_G), 0, 0, 1, 1},
  {&__pyx_n_s_GGVec, __pyx_k_GGVec, sizeof(__pyx_k_GGVec), 0, 0, 1, 1},
  {&__pyx_kp_s_G_2, __pyx_k_G_2, sizeof(__pyx_k_G_2), 0, 0, 1, 0},
  {&__pyx_n_s_Glove, __pyx_k_Glove, sizeof(__pyx_k_Glove), 0, 0, 1, 1},
  {&__pyx_n_s_GraRep, __pyx_k_GraRep, sizeof(__pyx_k_GraRep), 0, 0, 1, 1},
  {&__pyx_kp_s_K, __pyx_k_K, sizeof(__pyx_k_K), 0, 0, 1, 0},
  {&__pyx_kp_s_K_2, __pyx_k_K_2, sizeof(__pyx_k_K_2), 0, 0, 1, 0},
  {&__pyx_n_s_K_3, __pyx_k_K_3, sizeof(__pyx_k_K_3), 0, 0, 1, 1},
  {&__pyx_n_s_M, __pyx_k_M, sizeof(__pyx_k_M), 0, 0, 1, 1},
  {&__pyx_kp_s_O, __pyx_k_O, sizeof(__pyx_k_O), 0, 0, 1, 0},
  {&__pyx_kp_s_O_2, __pyx_k_O_2, sizeof(__pyx_k_O_2), 0, 0, 1, 0},
  {&__pyx_n_s_O_3, __pyx_k_O_3, sizeof(__pyx_k_O_3), 0, 0, 1, 1},
  {&__pyx_n_s_ProNE, __pyx_k_ProNE, sizeof(__pyx_k_ProNE), 0, 0, 1, 1},
  {&__pyx_n_s_ProNE_prefactorization, __pyx_k_ProNE_prefactorization, sizeof(__pyx_k_ProNE_prefactorization), 0, 0, 1, 1},
  {&__pyx_n_s_T, __pyx_k_T, sizeof(__pyx_k_T), 0, 0, 1, 1},
  {&__pyx_kp_s_T_2, __pyx_k_T_2, sizeof(__pyx_k_T_2), 0, 0, 1, 0},
  {&__pyx_kp_s_T_3, __pyx_k_T_3, sizeof(__pyx_k_T_3), 0, 0, 1, 0},
  {&__pyx_n_s_X, __pyx_k_X, sizeof(__pyx_k_X), 0, 0, 1, 1},
  {&__pyx_kp_s__9, __pyx_k__9, sizeof(__pyx_k__9), 0, 0, 1, 0},
  {&__pyx_n_s_action, __pyx_k_action, sizeof(__pyx_k_action), 0, 0, 1, 1},
  {&__pyx_n_s_add_argument, __pyx_k_add_argument, sizeof(__pyx_k_add_argument), 0, 0, 1, 1},
  {&__pyx_n_s_argparse, __pyx_k_argparse, sizeof(__pyx_k_argparse), 0, 0, 1, 1},
  {&__pyx_n_s_args, __pyx_k_args, sizeof(__pyx_k_args), 0, 0, 1, 1},
  {&__pyx_n_s_array, __pyx_k_array, sizeof(__pyx_k_array), 0, 0, 1, 1},
  {&__pyx_n_s_cg, __pyx_k_cg, sizeof(__pyx_k_cg), 0, 0, 1, 1},
  {&__pyx_n_s_cline_in_traceback, __pyx_k_cline_in_traceback, sizeof(__pyx_k_cline_in_traceback), 0, 0, 1, 1},
  {&__pyx_n_s_components, __pyx_k_components, sizeof(__pyx_k_components), 0, 0, 1, 1},
  {&__pyx_kp_s_components_2, __pyx_k_components_2, sizeof(__pyx_k_components_2), 0, 0, 1, 0},
  {&__pyx_n_s_csr_matrix, __pyx_k_csr_matrix, sizeof(__pyx_k_csr_matrix), 0, 0, 1, 1},
  {&__pyx_n_s_csrgraph, __pyx_k_csrgraph, sizeof(__pyx_k_csrgraph), 0, 0, 1, 1},
  {&__pyx_kp_s_d, __pyx_k_d, sizeof(__pyx_k_d), 0, 0, 1, 0},
  {&__pyx_n_s_default, __pyx_k_default, sizeof(__pyx_k_default), 0, 0, 1, 1},
  {&__pyx_kp_s_defaults_to_tab, __pyx_k_defaults_to_tab, sizeof(__pyx_k_defaults_to_tab), 0, 0, 1, 0},
  {&__pyx_n_s_delimiter, __pyx_k_delimiter, sizeof(__pyx_k_delimiter), 0, 0, 1, 1},
  {&__pyx_kp_s_delimiter_2, __pyx_k_delimiter_2, sizeof(__pyx_k_delimiter_2), 0, 0, 1, 0},
  {&__pyx_n_s_dict_to_embedding, __pyx_k_dict_to_embedding, sizeof(__pyx_k_dict_to_embedding), 0, 0, 1, 1},
  {&__pyx_kp_s_dict_to_embedding_py, __pyx_k_dict_to_embedding_py, sizeof(__pyx_k_dict_to_embedding_py), 0, 0, 1, 0},
  {&__pyx_n_s_do_file, __pyx_k_do_file, sizeof(__pyx_k_do_file), 0, 0, 1, 1},
  {&__pyx_n_s_edges, __pyx_k_edges, sizeof(__pyx_k_edges), 0, 0, 1, 1},
  {&__pyx_n_s_embeddings, __pyx_k_embeddings, sizeof(__pyx_k_embeddings), 0, 0, 1, 1},
  {&__pyx_n_s_endswith, __pyx_k_endswith, sizeof(__pyx_k_endswith), 0, 0, 1, 1},
  {&__pyx_n_s_exponent, __pyx_k_exponent, sizeof(__pyx_k_exponent), 0, 0, 1, 1},
  {&__pyx_n_s_features_matrix, __pyx_k_features_matrix, sizeof(__pyx_k_features_matrix), 0, 0, 1, 1},
  {&__pyx_kp_s_features_matrix_2, __pyx_k_features_matrix_2, sizeof(__pyx_k_features_matrix_2), 0, 0, 1, 0},
  {&__pyx_n_s_fit_transform, __pyx_k_fit_transform, sizeof(__pyx_k_fit_transform), 0, 0, 1, 1},
  {&__pyx_n_s_flush, __pyx_k_flush, sizeof(__pyx_k_flush), 0, 0, 1, 1},
  {&__pyx_kp_s_for_ProNE_result_of_pre_factoriz, __pyx_k_for_ProNE_result_of_pre_factoriz, sizeof(__pyx_k_for_ProNE_result_of_pre_factoriz), 0, 0, 1, 0},
  {&__pyx_n_s_help, __pyx_k_help, sizeof(__pyx_k_help), 0, 0, 1, 1},
  {&__pyx_kp_s_hidden_dimensions_defaults_32, __pyx_k_hidden_dimensions_defaults_32, sizeof(__pyx_k_hidden_dimensions_defaults_32), 0, 0, 1, 0},
  {&__pyx_kp_s_i, __pyx_k_i, sizeof(__pyx_k_i), 0, 0, 1, 0},
  {&__pyx_n_s_i_2, __pyx_k_i_2, sizeof(__pyx_k_i_2), 0, 0, 1, 1},
  {&__pyx_n_s_import, __pyx_k_import, sizeof(__pyx_k_import), 0, 0, 1, 1},
  {&__pyx_n_s_input_edge_list, __pyx_k_input_edge_list, sizeof(__pyx_k_input_edge_list), 0, 0, 1, 1},
  {&__pyx_kp_s_input_edge_list_2, __pyx_k_input_edge_list_2, sizeof(__pyx_k_input_edge_list_2), 0, 0, 1, 0},
  {&__pyx_n_s_input_graph, __pyx_k_input_graph, sizeof(__pyx_k_input_graph), 0, 0, 1, 1},
  {&__pyx_kp_s_input_graph_2, __pyx_k_input_graph_2, sizeof(__pyx_k_input_graph_2), 0, 0, 1, 0},
  {&__pyx_kp_s_input_graph_readable_by_scipy_sp, __pyx_k_input_graph_readable_by_scipy_sp, sizeof(__pyx_k_input_graph_readable_by_scipy_sp), 0, 0, 1, 0},
  {&__pyx_kp_s_input_text_file_one_line_for_eac, __pyx_k_input_text_file_one_line_for_eac, sizeof(__pyx_k_input_text_file_one_line_for_eac), 0, 0, 1, 0},
  {&__pyx_n_s_load, __pyx_k_load, sizeof(__pyx_k_load), 0, 0, 1, 1},
  {&__pyx_n_s_load_npz, __pyx_k_load_npz, sizeof(__pyx_k_load_npz), 0, 0, 1, 1},
  {&__pyx_kp_s_m, __pyx_k_m, sizeof(__pyx_k_m), 0, 0, 1, 0},
  {&__pyx_n_s_m_2, __pyx_k_m_2, sizeof(__pyx_k_m_2), 0, 0, 1, 1},
  {&__pyx_n_s_main, __pyx_k_main, sizeof(__pyx_k_main), 0, 0, 1, 1},
  {&__pyx_n_s_mat, __pyx_k_mat, sizeof(__pyx_k_mat), 0, 0, 1, 1},
  {&__pyx_n_s_method, __pyx_k_method, sizeof(__pyx_k_method), 0, 0, 1, 1},
  {&__pyx_n_s_method2model, __pyx_k_method2model, sizeof(__pyx_k_method2model), 0, 0, 1, 1},
  {&__pyx_kp_s_method_2, __pyx_k_method_2, sizeof(__pyx_k_method_2), 0, 0, 1, 0},
  {&__pyx_kp_s_method_s_should_be_one_of_GGVec, __pyx_k_method_s_should_be_one_of_GGVec, sizeof(__pyx_k_method_s_should_be_one_of_GGVec), 0, 0, 1, 0},
  {&__pyx_n_s_n_components, __pyx_k_n_components, sizeof(__pyx_k_n_components), 0, 0, 1, 1},
  {&__pyx_n_s_name, __pyx_k_name, sizeof(__pyx_k_name), 0, 0, 1, 1},
  {&__pyx_n_s_nodes, __pyx_k_nodes, sizeof(__pyx_k_nodes), 0, 0, 1, 1},
  {&__pyx_n_s_nodevectors, __pyx_k_nodevectors, sizeof(__pyx_k_nodevectors), 0, 0, 1, 1},
  {&__pyx_n_s_np, __pyx_k_np, sizeof(__pyx_k_np), 0, 0, 1, 1},
  {&__pyx_kp_s_number_of_threads_defaults_20_ap, __pyx_k_number_of_threads_defaults_20_ap, sizeof(__pyx_k_number_of_threads_defaults_20_ap), 0, 0, 1, 0},
  {&__pyx_n_s_numpy, __pyx_k_numpy, sizeof(__pyx_k_numpy), 0, 0, 1, 1},
  {&__pyx_kp_s_o, __pyx_k_o, sizeof(__pyx_k_o), 0, 0, 1, 0},
  {&__pyx_kp_s_one_of_GGVec_GraRep_Glove_ProNE, __pyx_k_one_of_GGVec_GraRep_Glove_ProNE, sizeof(__pyx_k_one_of_GGVec_GraRep_Glove_ProNE), 0, 0, 1, 0},
  {&__pyx_n_s_order, __pyx_k_order, sizeof(__pyx_k_order), 0, 0, 1, 1},
  {&__pyx_kp_s_order_2, __pyx_k_order_2, sizeof(__pyx_k_order_2), 0, 0, 1, 0},
  {&__pyx_kp_s_order_defaults_5_applies_to_meth, __pyx_k_order_defaults_5_applies_to_meth, sizeof(__pyx_k_order_defaults_5_applies_to_meth), 0, 0, 1, 0},
  {&__pyx_n_s_os, __pyx_k_os, sizeof(__pyx_k_os), 0, 0, 1, 1},
  {&__pyx_n_s_outf, __pyx_k_outf, sizeof(__pyx_k_outf), 0, 0, 1, 1},
  {&__pyx_n_s_output, __pyx_k_output, sizeof(__pyx_k_output), 0, 0, 1, 1},
  {&__pyx_kp_s_output_2, __pyx_k_output_2, sizeof(__pyx_k_output_2), 0, 0, 1, 0},
  {&__pyx_n_s_output_embedding, __pyx_k_output_embedding, sizeof(__pyx_k_output_embedding), 0, 0, 1, 1},
  {&__pyx_kp_s_output_file, __pyx_k_output_file, sizeof(__pyx_k_output_file), 0, 0, 1, 0},
  {&__pyx_n_s_parse_args, __pyx_k_parse_args, sizeof(__pyx_k_parse_args), 0, 0, 1, 1},
  {&__pyx_n_s_parser, __pyx_k_parser, sizeof(__pyx_k_parser), 0, 0, 1, 1},
  {&__pyx_kp_s_please_specify_either_input_edge, __pyx_k_please_specify_either_input_edge, sizeof(__pyx_k_please_specify_either_input_edge), 0, 0, 1, 0},
  {&__pyx_n_s_pre_factorization, __pyx_k_pre_factorization, sizeof(__pyx_k_pre_factorization), 0, 0, 1, 1},
  {&__pyx_n_s_prefix, __pyx_k_prefix, sizeof(__pyx_k_prefix), 0, 0, 1, 1},
  {&__pyx_n_s_quoting, __pyx_k_quoting, sizeof(__pyx_k_quoting), 0, 0, 1, 1},
  {&__pyx_n_s_range, __pyx_k_range, sizeof(__pyx_k_range), 0, 0, 1, 1},
  {&__pyx_n_s_read_edgelist, __pyx_k_read_edgelist, sizeof(__pyx_k_read_edgelist), 0, 0, 1, 1},
  {&__pyx_n_s_required, __pyx_k_required, sizeof(__pyx_k_required), 0, 0, 1, 1},
  {&__pyx_n_s_s, __pyx_k_s, sizeof(__pyx_k_s), 0, 0, 1, 1},
  {&__pyx_n_s_save, __pyx_k_save, sizeof(__pyx_k_save), 0, 0, 1, 1},
  {&__pyx_n_s_savez, __pyx_k_savez, sizeof(__pyx_k_savez), 0, 0, 1, 1},
  {&__pyx_n_s_scipy, __pyx_k_scipy, sizeof(__pyx_k_scipy), 0, 0, 1, 1},
  {&__pyx_n_s_scipy_sparse, __pyx_k_scipy_sparse, sizeof(__pyx_k_scipy_sparse), 0, 0, 1, 1},
  {&__pyx_n_s_sep, __pyx_k_sep, sizeof(__pyx_k_sep), 0, 0, 1, 1},
  {&__pyx_n_s_socket, __pyx_k_socket, sizeof(__pyx_k_socket), 0, 0, 1, 1},
  {&__pyx_n_s_sparse, __pyx_k_sparse, sizeof(__pyx_k_sparse), 0, 0, 1, 1},
  {&__pyx_n_s_stderr, __pyx_k_stderr, sizeof(__pyx_k_stderr), 0, 0, 1, 1},
  {&__pyx_n_s_store_true, __pyx_k_store_true, sizeof(__pyx_k_store_true), 0, 0, 1, 1},
  {&__pyx_n_s_strip_suffix, __pyx_k_strip_suffix, sizeof(__pyx_k_strip_suffix), 0, 0, 1, 1},
  {&__pyx_n_s_suf, __pyx_k_suf, sizeof(__pyx_k_suf), 0, 0, 1, 1},
  {&__pyx_n_s_suffix, __pyx_k_suffix, sizeof(__pyx_k_suffix), 0, 0, 1, 1},
  {&__pyx_n_s_suffixes, __pyx_k_suffixes, sizeof(__pyx_k_suffixes), 0, 0, 1, 1},
  {&__pyx_n_s_sys, __pyx_k_sys, sizeof(__pyx_k_sys), 0, 0, 1, 1},
  {&__pyx_kp_s_t, __pyx_k_t, sizeof(__pyx_k_t), 0, 0, 1, 0},
  {&__pyx_n_s_t0, __pyx_k_t0, sizeof(__pyx_k_t0), 0, 0, 1, 1},
  {&__pyx_n_s_test, __pyx_k_test, sizeof(__pyx_k_test), 0, 0, 1, 1},
  {&__pyx_n_s_threads, __pyx_k_threads, sizeof(__pyx_k_threads), 0, 0, 1, 1},
  {&__pyx_kp_s_threads_2, __pyx_k_threads_2, sizeof(__pyx_k_threads_2), 0, 0, 1, 0},
  {&__pyx_n_s_time, __pyx_k_time, sizeof(__pyx_k_time), 0, 0, 1, 1},
  {&__pyx_n_s_transpose, __pyx_k_transpose, sizeof(__pyx_k_transpose), 0, 0, 1, 1},
  {&__pyx_kp_s_transpose_2, __pyx_k_transpose_2, sizeof(__pyx_k_transpose_2), 0, 0, 1, 0},
  {&__pyx_kp_s_txt, __pyx_k_txt, sizeof(__pyx_k_txt), 0, 0, 1, 0},
  {&__pyx_kp_s_txt2, __pyx_k_txt2, sizeof(__pyx_k_txt2), 0, 0, 1, 0},
  {&__pyx_n_s_type, __pyx_k_type, sizeof(__pyx_k_type), 0, 0, 1, 1},
  {&__pyx_kp_s_w2v, __pyx_k_w2v, sizeof(__pyx_k_w2v), 0, 0, 1, 0},
  {0, 0, 0, 0, 0, 0, 0}
};
static CYTHON_SMALL_CODE int __Pyx_InitCachedBuiltins(void) {
  __pyx_builtin_range = __Pyx_GetBuiltinName(__pyx_n_s_range); if (!__pyx_builtin_range) __PYX_ERR(0, 138, __pyx_L1_error)
  return 0;
  __pyx_L1_error:;
  return -1;
}

static CYTHON_SMALL_CODE int __Pyx_InitCachedConstants(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_InitCachedConstants", 0);

  /* "dict_to_embedding.py":23
 * 
 * parser = argparse.ArgumentParser()
 * parser.add_argument("-o", "--output", help="output file", required=True)             # <<<<<<<<<<<<<<
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 */
  __pyx_tuple__2 = PyTuple_Pack(2, __pyx_kp_s_o, __pyx_kp_s_output_2); if (unlikely(!__pyx_tuple__2)) __PYX_ERR(0, 23, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__2);
  __Pyx_GIVEREF(__pyx_tuple__2);

  /* "dict_to_embedding.py":24
 * parser = argparse.ArgumentParser()
 * parser.add_argument("-o", "--output", help="output file", required=True)
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)             # <<<<<<<<<<<<<<
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 */
  __pyx_tuple__3 = PyTuple_Pack(2, __pyx_kp_s_i, __pyx_kp_s_input_edge_list_2); if (unlikely(!__pyx_tuple__3)) __PYX_ERR(0, 24, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__3);
  __Pyx_GIVEREF(__pyx_tuple__3);

  /* "dict_to_embedding.py":25
 * parser.add_argument("-o", "--output", help="output file", required=True)
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)             # <<<<<<<<<<<<<<
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 */
  __pyx_tuple__4 = PyTuple_Pack(2, __pyx_kp_s_G_2, __pyx_kp_s_input_graph_2); if (unlikely(!__pyx_tuple__4)) __PYX_ERR(0, 25, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__4);
  __Pyx_GIVEREF(__pyx_tuple__4);

  /* "dict_to_embedding.py":26
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)             # <<<<<<<<<<<<<<
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 */
  __pyx_tuple__5 = PyTuple_Pack(2, __pyx_kp_s_K_2, __pyx_kp_s_components_2); if (unlikely(!__pyx_tuple__5)) __PYX_ERR(0, 26, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__5);
  __Pyx_GIVEREF(__pyx_tuple__5);

  /* "dict_to_embedding.py":27
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)             # <<<<<<<<<<<<<<
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 */
  __pyx_tuple__6 = PyTuple_Pack(2, __pyx_kp_s_T_3, __pyx_kp_s_threads_2); if (unlikely(!__pyx_tuple__6)) __PYX_ERR(0, 27, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__6);
  __Pyx_GIVEREF(__pyx_tuple__6);

  /* "dict_to_embedding.py":28
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)             # <<<<<<<<<<<<<<
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 */
  __pyx_tuple__7 = PyTuple_Pack(2, __pyx_kp_s_O_2, __pyx_kp_s_order_2); if (unlikely(!__pyx_tuple__7)) __PYX_ERR(0, 28, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__7);
  __Pyx_GIVEREF(__pyx_tuple__7);

  /* "dict_to_embedding.py":29
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')             # <<<<<<<<<<<<<<
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')
 */
  __pyx_tuple__8 = PyTuple_Pack(2, __pyx_kp_s_d, __pyx_kp_s_delimiter_2); if (unlikely(!__pyx_tuple__8)) __PYX_ERR(0, 29, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__8);
  __Pyx_GIVEREF(__pyx_tuple__8);

  /* "dict_to_embedding.py":30
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')             # <<<<<<<<<<<<<<
 * parser.add_argument("-t", '--transpose', action='store_true')
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)
 */
  __pyx_tuple__10 = PyTuple_Pack(2, __pyx_kp_s_m, __pyx_kp_s_method_2); if (unlikely(!__pyx_tuple__10)) __PYX_ERR(0, 30, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__10);
  __Pyx_GIVEREF(__pyx_tuple__10);

  /* "dict_to_embedding.py":31
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')             # <<<<<<<<<<<<<<
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)
 * # parser.add_argument("-s", "--save_svd", help="save a svd model", action='store_true')
 */
  __pyx_tuple__11 = PyTuple_Pack(2, __pyx_kp_s_t, __pyx_kp_s_transpose_2); if (unlikely(!__pyx_tuple__11)) __PYX_ERR(0, 31, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__11);
  __Pyx_GIVEREF(__pyx_tuple__11);

  /* "dict_to_embedding.py":32
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)             # <<<<<<<<<<<<<<
 * # parser.add_argument("-s", "--save_svd", help="save a svd model", action='store_true')
 * # parser.add_argument("-l", "--load_svd", help="load an svd model", action='store_true')
 */
  __pyx_tuple__12 = PyTuple_Pack(2, __pyx_kp_s_F, __pyx_kp_s_features_matrix_2); if (unlikely(!__pyx_tuple__12)) __PYX_ERR(0, 32, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__12);
  __Pyx_GIVEREF(__pyx_tuple__12);

  /* "dict_to_embedding.py":40
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'
 * 
 * def strip_suffix(s, suffixes):             # <<<<<<<<<<<<<<
 *     for suf in suffixes:
 *         if s.endswith(suf):
 */
  __pyx_tuple__13 = PyTuple_Pack(3, __pyx_n_s_s, __pyx_n_s_suffixes, __pyx_n_s_suf); if (unlikely(!__pyx_tuple__13)) __PYX_ERR(0, 40, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__13);
  __Pyx_GIVEREF(__pyx_tuple__13);
  __pyx_codeobj__14 = (PyObject*)__Pyx_PyCode_New(2, 0, 3, 0, CO_OPTIMIZED|CO_NEWLOCALS, __pyx_empty_bytes, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_tuple__13, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_kp_s_dict_to_embedding_py, __pyx_n_s_strip_suffix, 40, __pyx_empty_bytes); if (unlikely(!__pyx_codeobj__14)) __PYX_ERR(0, 40, __pyx_L1_error)

  /* "dict_to_embedding.py":46
 *     return s
 * 
 * def method2model():             # <<<<<<<<<<<<<<
 *     m = args.method
 *     K = args.components
 */
  __pyx_tuple__15 = PyTuple_Pack(4, __pyx_n_s_m_2, __pyx_n_s_K_3, __pyx_n_s_T, __pyx_n_s_O_3); if (unlikely(!__pyx_tuple__15)) __PYX_ERR(0, 46, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__15);
  __Pyx_GIVEREF(__pyx_tuple__15);
  __pyx_codeobj__16 = (PyObject*)__Pyx_PyCode_New(0, 0, 4, 0, CO_OPTIMIZED|CO_NEWLOCALS, __pyx_empty_bytes, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_tuple__15, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_kp_s_dict_to_embedding_py, __pyx_n_s_method2model, 46, __pyx_empty_bytes); if (unlikely(!__pyx_codeobj__16)) __PYX_ERR(0, 46, __pyx_L1_error)

  /* "dict_to_embedding.py":67
 *     assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m
 * 
 * def output_embedding(G, E, outf):             # <<<<<<<<<<<<<<
 *     np.savez(outf, nodes=np.array(G.nodes()), edges=E)
 * 
 */
  __pyx_tuple__17 = PyTuple_Pack(3, __pyx_n_s_G, __pyx_n_s_E, __pyx_n_s_outf); if (unlikely(!__pyx_tuple__17)) __PYX_ERR(0, 67, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__17);
  __Pyx_GIVEREF(__pyx_tuple__17);
  __pyx_codeobj__18 = (PyObject*)__Pyx_PyCode_New(3, 0, 3, 0, CO_OPTIMIZED|CO_NEWLOCALS, __pyx_empty_bytes, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_tuple__17, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_kp_s_dict_to_embedding_py, __pyx_n_s_output_embedding, 67, __pyx_empty_bytes); if (unlikely(!__pyx_codeobj__18)) __PYX_ERR(0, 67, __pyx_L1_error)

  /* "dict_to_embedding.py":71
 * 
 * #@profile
 * def do_file():             # <<<<<<<<<<<<<<
 * 
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 */
  __pyx_tuple__19 = PyTuple_Pack(10, __pyx_n_s_G, __pyx_n_s_scipy, __pyx_n_s_M, __pyx_n_s_m_2, __pyx_n_s_features_matrix, __pyx_n_s_embeddings, __pyx_n_s_suffix, __pyx_n_s_prefix, __pyx_n_s_outf, __pyx_n_s_i_2); if (unlikely(!__pyx_tuple__19)) __PYX_ERR(0, 71, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_tuple__19);
  __Pyx_GIVEREF(__pyx_tuple__19);
  __pyx_codeobj__20 = (PyObject*)__Pyx_PyCode_New(0, 0, 10, 0, CO_OPTIMIZED|CO_NEWLOCALS, __pyx_empty_bytes, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_tuple__19, __pyx_empty_tuple, __pyx_empty_tuple, __pyx_kp_s_dict_to_embedding_py, __pyx_n_s_do_file, 71, __pyx_empty_bytes); if (unlikely(!__pyx_codeobj__20)) __PYX_ERR(0, 71, __pyx_L1_error)
  __Pyx_RefNannyFinishContext();
  return 0;
  __pyx_L1_error:;
  __Pyx_RefNannyFinishContext();
  return -1;
}

static CYTHON_SMALL_CODE int __Pyx_InitGlobals(void) {
  if (__Pyx_InitStrings(__pyx_string_tab) < 0) __PYX_ERR(0, 1, __pyx_L1_error);
  __pyx_int_3 = PyInt_FromLong(3); if (unlikely(!__pyx_int_3)) __PYX_ERR(0, 1, __pyx_L1_error)
  __pyx_int_5 = PyInt_FromLong(5); if (unlikely(!__pyx_int_5)) __PYX_ERR(0, 1, __pyx_L1_error)
  __pyx_int_20 = PyInt_FromLong(20); if (unlikely(!__pyx_int_20)) __PYX_ERR(0, 1, __pyx_L1_error)
  __pyx_int_32 = PyInt_FromLong(32); if (unlikely(!__pyx_int_32)) __PYX_ERR(0, 1, __pyx_L1_error)
  return 0;
  __pyx_L1_error:;
  return -1;
}

static CYTHON_SMALL_CODE int __Pyx_modinit_global_init_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_variable_export_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_function_export_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_type_init_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_type_import_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_variable_import_code(void); /*proto*/
static CYTHON_SMALL_CODE int __Pyx_modinit_function_import_code(void); /*proto*/

static int __Pyx_modinit_global_init_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_global_init_code", 0);
  /*--- Global init code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_variable_export_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_variable_export_code", 0);
  /*--- Variable export code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_function_export_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_function_export_code", 0);
  /*--- Function export code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_type_init_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_type_init_code", 0);
  /*--- Type init code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_type_import_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_type_import_code", 0);
  /*--- Type import code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_variable_import_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_variable_import_code", 0);
  /*--- Variable import code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}

static int __Pyx_modinit_function_import_code(void) {
  __Pyx_RefNannyDeclarations
  __Pyx_RefNannySetupContext("__Pyx_modinit_function_import_code", 0);
  /*--- Function import code ---*/
  __Pyx_RefNannyFinishContext();
  return 0;
}


#ifndef CYTHON_NO_PYINIT_EXPORT
#define __Pyx_PyMODINIT_FUNC PyMODINIT_FUNC
#elif PY_MAJOR_VERSION < 3
#ifdef __cplusplus
#define __Pyx_PyMODINIT_FUNC extern "C" void
#else
#define __Pyx_PyMODINIT_FUNC void
#endif
#else
#ifdef __cplusplus
#define __Pyx_PyMODINIT_FUNC extern "C" PyObject *
#else
#define __Pyx_PyMODINIT_FUNC PyObject *
#endif
#endif


#if PY_MAJOR_VERSION < 3
__Pyx_PyMODINIT_FUNC initdict_to_embedding(void) CYTHON_SMALL_CODE; /*proto*/
__Pyx_PyMODINIT_FUNC initdict_to_embedding(void)
#else
__Pyx_PyMODINIT_FUNC PyInit_dict_to_embedding(void) CYTHON_SMALL_CODE; /*proto*/
__Pyx_PyMODINIT_FUNC PyInit_dict_to_embedding(void)
#if CYTHON_PEP489_MULTI_PHASE_INIT
{
  return PyModuleDef_Init(&__pyx_moduledef);
}
static CYTHON_SMALL_CODE int __Pyx_check_single_interpreter(void) {
    #if PY_VERSION_HEX >= 0x030700A1
    static PY_INT64_T main_interpreter_id = -1;
    PY_INT64_T current_id = PyInterpreterState_GetID(PyThreadState_Get()->interp);
    if (main_interpreter_id == -1) {
        main_interpreter_id = current_id;
        return (unlikely(current_id == -1)) ? -1 : 0;
    } else if (unlikely(main_interpreter_id != current_id))
    #else
    static PyInterpreterState *main_interpreter = NULL;
    PyInterpreterState *current_interpreter = PyThreadState_Get()->interp;
    if (!main_interpreter) {
        main_interpreter = current_interpreter;
    } else if (unlikely(main_interpreter != current_interpreter))
    #endif
    {
        PyErr_SetString(
            PyExc_ImportError,
            "Interpreter change detected - this module can only be loaded into one interpreter per process.");
        return -1;
    }
    return 0;
}
static CYTHON_SMALL_CODE int __Pyx_copy_spec_to_module(PyObject *spec, PyObject *moddict, const char* from_name, const char* to_name, int allow_none) {
    PyObject *value = PyObject_GetAttrString(spec, from_name);
    int result = 0;
    if (likely(value)) {
        if (allow_none || value != Py_None) {
            result = PyDict_SetItemString(moddict, to_name, value);
        }
        Py_DECREF(value);
    } else if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
        PyErr_Clear();
    } else {
        result = -1;
    }
    return result;
}
static CYTHON_SMALL_CODE PyObject* __pyx_pymod_create(PyObject *spec, CYTHON_UNUSED PyModuleDef *def) {
    PyObject *module = NULL, *moddict, *modname;
    if (__Pyx_check_single_interpreter())
        return NULL;
    if (__pyx_m)
        return __Pyx_NewRef(__pyx_m);
    modname = PyObject_GetAttrString(spec, "name");
    if (unlikely(!modname)) goto bad;
    module = PyModule_NewObject(modname);
    Py_DECREF(modname);
    if (unlikely(!module)) goto bad;
    moddict = PyModule_GetDict(module);
    if (unlikely(!moddict)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "loader", "__loader__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "origin", "__file__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "parent", "__package__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "submodule_search_locations", "__path__", 0) < 0)) goto bad;
    return module;
bad:
    Py_XDECREF(module);
    return NULL;
}


static CYTHON_SMALL_CODE int __pyx_pymod_exec_dict_to_embedding(PyObject *__pyx_pyinit_module)
#endif
#endif
{
  PyObject *__pyx_t_1 = NULL;
  PyObject *__pyx_t_2 = NULL;
  PyObject *__pyx_t_3 = NULL;
  int __pyx_t_4;
  int __pyx_t_5;
  int __pyx_lineno = 0;
  const char *__pyx_filename = NULL;
  int __pyx_clineno = 0;
  __Pyx_RefNannyDeclarations
  #if CYTHON_PEP489_MULTI_PHASE_INIT
  if (__pyx_m) {
    if (__pyx_m == __pyx_pyinit_module) return 0;
    PyErr_SetString(PyExc_RuntimeError, "Module 'dict_to_embedding' has already been imported. Re-initialisation is not supported.");
    return -1;
  }
  #elif PY_MAJOR_VERSION >= 3
  if (__pyx_m) return __Pyx_NewRef(__pyx_m);
  #endif
  #if CYTHON_REFNANNY
__Pyx_RefNanny = __Pyx_RefNannyImportAPI("refnanny");
if (!__Pyx_RefNanny) {
  PyErr_Clear();
  __Pyx_RefNanny = __Pyx_RefNannyImportAPI("Cython.Runtime.refnanny");
  if (!__Pyx_RefNanny)
      Py_FatalError("failed to import 'refnanny' module");
}
#endif
  __Pyx_RefNannySetupContext("__Pyx_PyMODINIT_FUNC PyInit_dict_to_embedding(void)", 0);
  if (__Pyx_check_binary_version() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #ifdef __Pxy_PyFrame_Initialize_Offsets
  __Pxy_PyFrame_Initialize_Offsets();
  #endif
  __pyx_empty_tuple = PyTuple_New(0); if (unlikely(!__pyx_empty_tuple)) __PYX_ERR(0, 1, __pyx_L1_error)
  __pyx_empty_bytes = PyBytes_FromStringAndSize("", 0); if (unlikely(!__pyx_empty_bytes)) __PYX_ERR(0, 1, __pyx_L1_error)
  __pyx_empty_unicode = PyUnicode_FromStringAndSize("", 0); if (unlikely(!__pyx_empty_unicode)) __PYX_ERR(0, 1, __pyx_L1_error)
  #ifdef __Pyx_CyFunction_USED
  if (__pyx_CyFunction_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  #ifdef __Pyx_FusedFunction_USED
  if (__pyx_FusedFunction_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  #ifdef __Pyx_Coroutine_USED
  if (__pyx_Coroutine_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  #ifdef __Pyx_Generator_USED
  if (__pyx_Generator_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  #ifdef __Pyx_AsyncGen_USED
  if (__pyx_AsyncGen_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  #ifdef __Pyx_StopAsyncIteration_USED
  if (__pyx_StopAsyncIteration_init() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  /*--- Library function declarations ---*/
  /*--- Threads initialization code ---*/
  #if defined(WITH_THREAD) && PY_VERSION_HEX < 0x030700F0 && defined(__PYX_FORCE_INIT_THREADS) && __PYX_FORCE_INIT_THREADS
  PyEval_InitThreads();
  #endif
  /*--- Module creation code ---*/
  #if CYTHON_PEP489_MULTI_PHASE_INIT
  __pyx_m = __pyx_pyinit_module;
  Py_INCREF(__pyx_m);
  #else
  #if PY_MAJOR_VERSION < 3
  __pyx_m = Py_InitModule4("dict_to_embedding", __pyx_methods, 0, 0, PYTHON_API_VERSION); Py_XINCREF(__pyx_m);
  #else
  __pyx_m = PyModule_Create(&__pyx_moduledef);
  #endif
  if (unlikely(!__pyx_m)) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  __pyx_d = PyModule_GetDict(__pyx_m); if (unlikely(!__pyx_d)) __PYX_ERR(0, 1, __pyx_L1_error)
  Py_INCREF(__pyx_d);
  __pyx_b = PyImport_AddModule(__Pyx_BUILTIN_MODULE_NAME); if (unlikely(!__pyx_b)) __PYX_ERR(0, 1, __pyx_L1_error)
  Py_INCREF(__pyx_b);
  __pyx_cython_runtime = PyImport_AddModule((char *) "cython_runtime"); if (unlikely(!__pyx_cython_runtime)) __PYX_ERR(0, 1, __pyx_L1_error)
  Py_INCREF(__pyx_cython_runtime);
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) __PYX_ERR(0, 1, __pyx_L1_error);
  /*--- Initialize various global constants etc. ---*/
  if (__Pyx_InitGlobals() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #if PY_MAJOR_VERSION < 3 && (__PYX_DEFAULT_STRING_ENCODING_IS_ASCII || __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT)
  if (__Pyx_init_sys_getdefaultencoding_params() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif
  if (__pyx_module_is_main_dict_to_embedding) {
    if (PyObject_SetAttr(__pyx_m, __pyx_n_s_name, __pyx_n_s_main) < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  }
  #if PY_MAJOR_VERSION >= 3
  {
    PyObject *modules = PyImport_GetModuleDict(); if (unlikely(!modules)) __PYX_ERR(0, 1, __pyx_L1_error)
    if (!PyDict_GetItemString(modules, "dict_to_embedding")) {
      if (unlikely(PyDict_SetItemString(modules, "dict_to_embedding", __pyx_m) < 0)) __PYX_ERR(0, 1, __pyx_L1_error)
    }
  }
  #endif
  /*--- Builtin init code ---*/
  if (__Pyx_InitCachedBuiltins() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  /*--- Constants init code ---*/
  if (__Pyx_InitCachedConstants() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  /*--- Global type/function init code ---*/
  (void)__Pyx_modinit_global_init_code();
  (void)__Pyx_modinit_variable_export_code();
  (void)__Pyx_modinit_function_export_code();
  (void)__Pyx_modinit_type_init_code();
  (void)__Pyx_modinit_type_import_code();
  (void)__Pyx_modinit_variable_import_code();
  (void)__Pyx_modinit_function_import_code();
  /*--- Execution code ---*/
  #if defined(__Pyx_Generator_USED) || defined(__Pyx_Coroutine_USED)
  if (__Pyx_patch_abc() < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  #endif

  /* "dict_to_embedding.py":3
 * #!/usr/bin/env python
 * 
 * import numpy as np             # <<<<<<<<<<<<<<
 * import csrgraph as cg
 * import sys,os,socket,argparse,time
 */
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_numpy, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 3, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_np, __pyx_t_1) < 0) __PYX_ERR(0, 3, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":4
 * 
 * import numpy as np
 * import csrgraph as cg             # <<<<<<<<<<<<<<
 * import sys,os,socket,argparse,time
 * import nodevectors
 */
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_csrgraph, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 4, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_cg, __pyx_t_1) < 0) __PYX_ERR(0, 4, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":5
 * import numpy as np
 * import csrgraph as cg
 * import sys,os,socket,argparse,time             # <<<<<<<<<<<<<<
 * import nodevectors
 * 
 */
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_sys, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_sys, __pyx_t_1) < 0) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_os, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_os, __pyx_t_1) < 0) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_socket, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_socket, __pyx_t_1) < 0) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_argparse, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_argparse, __pyx_t_1) < 0) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_time, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_time, __pyx_t_1) < 0) __PYX_ERR(0, 5, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":6
 * import csrgraph as cg
 * import sys,os,socket,argparse,time
 * import nodevectors             # <<<<<<<<<<<<<<
 * 
 * #from memory_profiler import profile
 */
  __pyx_t_1 = __Pyx_Import(__pyx_n_s_nodevectors, 0, -1); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 6, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_nodevectors, __pyx_t_1) < 0) __PYX_ERR(0, 6, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":12
 * #print('dict_to_embedding.py: ' + str(sys.argv), file=sys.stderr)
 * 
 * t0 = time.time()             # <<<<<<<<<<<<<<
 * 
 * # echo hostname = `hostname` 1>&2
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_time); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 12, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_time); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 12, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyObject_CallNoArg(__pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 12, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_t0, __pyx_t_1) < 0) __PYX_ERR(0, 12, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":22
 * #print('dict_to_embedding: SLURM_ARRAY_TASK_ID = ' + str(os.getenv('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
 * 
 * parser = argparse.ArgumentParser()             # <<<<<<<<<<<<<<
 * parser.add_argument("-o", "--output", help="output file", required=True)
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_argparse); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 22, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_ArgumentParser); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 22, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyObject_CallNoArg(__pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 22, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_parser, __pyx_t_1) < 0) __PYX_ERR(0, 22, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":23
 * 
 * parser = argparse.ArgumentParser()
 * parser.add_argument("-o", "--output", help="output file", required=True)             # <<<<<<<<<<<<<<
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_parser); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 23, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 23, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 23, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_help, __pyx_kp_s_output_file) < 0) __PYX_ERR(0, 23, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_required, Py_True) < 0) __PYX_ERR(0, 23, __pyx_L1_error)
  __pyx_t_3 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_tuple__2, __pyx_t_1); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 23, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":24
 * parser = argparse.ArgumentParser()
 * parser.add_argument("-o", "--output", help="output file", required=True)
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)             # <<<<<<<<<<<<<<
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_parser); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 24, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_3, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 24, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __pyx_t_3 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 24, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_help, __pyx_kp_s_input_text_file_one_line_for_eac) < 0) __PYX_ERR(0, 24, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_default, Py_None) < 0) __PYX_ERR(0, 24, __pyx_L1_error)
  __pyx_t_2 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_tuple__3, __pyx_t_3); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 24, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;

  /* "dict_to_embedding.py":25
 * parser.add_argument("-o", "--output", help="output file", required=True)
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)             # <<<<<<<<<<<<<<
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_parser); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 25, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __pyx_t_3 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 25, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 25, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_help, __pyx_kp_s_input_graph_readable_by_scipy_sp) < 0) __PYX_ERR(0, 25, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_default, Py_None) < 0) __PYX_ERR(0, 25, __pyx_L1_error)
  __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_3, __pyx_tuple__4, __pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 25, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":26
 * parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)             # <<<<<<<<<<<<<<
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_parser); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 26, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 26, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyDict_NewPresized(3); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 26, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_type, ((PyObject *)(&PyInt_Type))) < 0) __PYX_ERR(0, 26, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_help, __pyx_kp_s_hidden_dimensions_defaults_32) < 0) __PYX_ERR(0, 26, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_default, __pyx_int_32) < 0) __PYX_ERR(0, 26, __pyx_L1_error)
  __pyx_t_3 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_tuple__5, __pyx_t_1); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 26, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":27
 * parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)             # <<<<<<<<<<<<<<
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_parser); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 27, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_3, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 27, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __pyx_t_3 = __Pyx_PyDict_NewPresized(3); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 27, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_type, ((PyObject *)(&PyInt_Type))) < 0) __PYX_ERR(0, 27, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_help, __pyx_kp_s_number_of_threads_defaults_20_ap) < 0) __PYX_ERR(0, 27, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_default, __pyx_int_20) < 0) __PYX_ERR(0, 27, __pyx_L1_error)
  __pyx_t_2 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_tuple__6, __pyx_t_3); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 27, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;

  /* "dict_to_embedding.py":28
 * parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)             # <<<<<<<<<<<<<<
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_parser); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 28, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __pyx_t_3 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 28, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = __Pyx_PyDict_NewPresized(3); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 28, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_type, ((PyObject *)(&PyInt_Type))) < 0) __PYX_ERR(0, 28, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_help, __pyx_kp_s_order_defaults_5_applies_to_meth) < 0) __PYX_ERR(0, 28, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_default, __pyx_int_5) < 0) __PYX_ERR(0, 28, __pyx_L1_error)
  __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_3, __pyx_tuple__7, __pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 28, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":29
 * parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')             # <<<<<<<<<<<<<<
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_parser); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 29, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 29, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 29, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_help, __pyx_kp_s_defaults_to_tab) < 0) __PYX_ERR(0, 29, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_default, __pyx_kp_s__9) < 0) __PYX_ERR(0, 29, __pyx_L1_error)
  __pyx_t_3 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_tuple__8, __pyx_t_1); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 29, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":30
 * parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')             # <<<<<<<<<<<<<<
 * parser.add_argument("-t", '--transpose', action='store_true')
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_parser); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 30, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_3, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 30, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __pyx_t_3 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 30, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_help, __pyx_kp_s_one_of_GGVec_GraRep_Glove_ProNE) < 0) __PYX_ERR(0, 30, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_3, __pyx_n_s_default, __pyx_n_s_ProNE) < 0) __PYX_ERR(0, 30, __pyx_L1_error)
  __pyx_t_2 = __Pyx_PyObject_Call(__pyx_t_1, __pyx_tuple__10, __pyx_t_3); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 30, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;

  /* "dict_to_embedding.py":31
 * parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')             # <<<<<<<<<<<<<<
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)
 * # parser.add_argument("-s", "--save_svd", help="save a svd model", action='store_true')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_2, __pyx_n_s_parser); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 31, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __pyx_t_3 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 31, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __pyx_t_2 = __Pyx_PyDict_NewPresized(1); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 31, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  if (PyDict_SetItem(__pyx_t_2, __pyx_n_s_action, __pyx_n_s_store_true) < 0) __PYX_ERR(0, 31, __pyx_L1_error)
  __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_3, __pyx_tuple__11, __pyx_t_2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 31, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":32
 * parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
 * parser.add_argument("-t", '--transpose', action='store_true')
 * parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)             # <<<<<<<<<<<<<<
 * # parser.add_argument("-s", "--save_svd", help="save a svd model", action='store_true')
 * # parser.add_argument("-l", "--load_svd", help="load an svd model", action='store_true')
 */
  __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_parser); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 32, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_add_argument); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 32, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_2);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __pyx_t_1 = __Pyx_PyDict_NewPresized(2); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 32, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_help, __pyx_kp_s_for_ProNE_result_of_pre_factoriz) < 0) __PYX_ERR(0, 32, __pyx_L1_error)
  if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_default, Py_None) < 0) __PYX_ERR(0, 32, __pyx_L1_error)
  __pyx_t_3 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_tuple__12, __pyx_t_1); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 32, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":36
 * # parser.add_argument("-l", "--load_svd", help="load an svd model", action='store_true')
 * # parser.add_argument("-f", "--svd_file", help="filename/dirname to load or save", default=".")
 * args = parser.parse_args()             # <<<<<<<<<<<<<<
 * 
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'
 */
  __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_parser); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 36, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_3, __pyx_n_s_parse_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 36, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __pyx_t_3 = __Pyx_PyObject_CallNoArg(__pyx_t_1); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 36, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_args, __pyx_t_3) < 0) __PYX_ERR(0, 36, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":38
 * args = parser.parse_args()
 * 
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'             # <<<<<<<<<<<<<<
 * 
 * def strip_suffix(s, suffixes):
 */
  #ifndef CYTHON_WITHOUT_ASSERTIONS
  if (unlikely(!Py_OptimizeFlag)) {
    __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_args); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 38, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_3);
    __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_t_3, __pyx_n_s_input_graph); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 38, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
    __pyx_t_4 = (__pyx_t_1 == Py_None);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __Pyx_GetModuleGlobalName(__pyx_t_1, __pyx_n_s_args); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 38, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_1);
    __pyx_t_3 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_input_edge_list); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 38, __pyx_L1_error)
    __Pyx_GOTREF(__pyx_t_3);
    __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    __pyx_t_5 = (__pyx_t_3 == Py_None);
    __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
    if (unlikely(!((__pyx_t_4 != __pyx_t_5) != 0))) {
      PyErr_SetObject(PyExc_AssertionError, __pyx_kp_s_please_specify_either_input_edge);
      __PYX_ERR(0, 38, __pyx_L1_error)
    }
  }
  #endif

  /* "dict_to_embedding.py":40
 * assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'
 * 
 * def strip_suffix(s, suffixes):             # <<<<<<<<<<<<<<
 *     for suf in suffixes:
 *         if s.endswith(suf):
 */
  __pyx_t_3 = __Pyx_CyFunction_New(&__pyx_mdef_17dict_to_embedding_1strip_suffix, 0, __pyx_n_s_strip_suffix, NULL, __pyx_n_s_dict_to_embedding, __pyx_d, ((PyObject *)__pyx_codeobj__14)); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 40, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_strip_suffix, __pyx_t_3) < 0) __PYX_ERR(0, 40, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":46
 *     return s
 * 
 * def method2model():             # <<<<<<<<<<<<<<
 *     m = args.method
 *     K = args.components
 */
  __pyx_t_3 = __Pyx_CyFunction_New(&__pyx_mdef_17dict_to_embedding_3method2model, 0, __pyx_n_s_method2model, NULL, __pyx_n_s_dict_to_embedding, __pyx_d, ((PyObject *)__pyx_codeobj__16)); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 46, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_method2model, __pyx_t_3) < 0) __PYX_ERR(0, 46, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":67
 *     assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m
 * 
 * def output_embedding(G, E, outf):             # <<<<<<<<<<<<<<
 *     np.savez(outf, nodes=np.array(G.nodes()), edges=E)
 * 
 */
  __pyx_t_3 = __Pyx_CyFunction_New(&__pyx_mdef_17dict_to_embedding_5output_embedding, 0, __pyx_n_s_output_embedding, NULL, __pyx_n_s_dict_to_embedding, __pyx_d, ((PyObject *)__pyx_codeobj__18)); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 67, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_output_embedding, __pyx_t_3) < 0) __PYX_ERR(0, 67, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":71
 * 
 * #@profile
 * def do_file():             # <<<<<<<<<<<<<<
 * 
 *     #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
 */
  __pyx_t_3 = __Pyx_CyFunction_New(&__pyx_mdef_17dict_to_embedding_7do_file, 0, __pyx_n_s_do_file, NULL, __pyx_n_s_dict_to_embedding, __pyx_d, ((PyObject *)__pyx_codeobj__20)); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 71, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_do_file, __pyx_t_3) < 0) __PYX_ERR(0, 71, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;

  /* "dict_to_embedding.py":141
 *             output_embedding(G, embeddings[i], outf + '.' + str(i))
 * 
 * do_file()             # <<<<<<<<<<<<<<
 * 
 * #print('dict_to_embedding: # total time: %0.2f' % (time.time() - t0), file=sys.stderr)
 */
  __Pyx_GetModuleGlobalName(__pyx_t_3, __pyx_n_s_do_file); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 141, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_3);
  __pyx_t_1 = __Pyx_PyObject_CallNoArg(__pyx_t_3); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 141, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /* "dict_to_embedding.py":1
 * #!/usr/bin/env python             # <<<<<<<<<<<<<<
 * 
 * import numpy as np
 */
  __pyx_t_1 = __Pyx_PyDict_NewPresized(0); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 1, __pyx_L1_error)
  __Pyx_GOTREF(__pyx_t_1);
  if (PyDict_SetItem(__pyx_d, __pyx_n_s_test, __pyx_t_1) < 0) __PYX_ERR(0, 1, __pyx_L1_error)
  __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

  /*--- Wrapped vars code ---*/

  goto __pyx_L0;
  __pyx_L1_error:;
  __Pyx_XDECREF(__pyx_t_1);
  __Pyx_XDECREF(__pyx_t_2);
  __Pyx_XDECREF(__pyx_t_3);
  if (__pyx_m) {
    if (__pyx_d) {
      __Pyx_AddTraceback("init dict_to_embedding", __pyx_clineno, __pyx_lineno, __pyx_filename);
    }
    Py_CLEAR(__pyx_m);
  } else if (!PyErr_Occurred()) {
    PyErr_SetString(PyExc_ImportError, "init dict_to_embedding");
  }
  __pyx_L0:;
  __Pyx_RefNannyFinishContext();
  #if CYTHON_PEP489_MULTI_PHASE_INIT
  return (__pyx_m != NULL) ? 0 : -1;
  #elif PY_MAJOR_VERSION >= 3
  return __pyx_m;
  #else
  return;
  #endif
}

/* --- Runtime support code --- */
/* Refnanny */
#if CYTHON_REFNANNY
static __Pyx_RefNannyAPIStruct *__Pyx_RefNannyImportAPI(const char *modname) {
    PyObject *m = NULL, *p = NULL;
    void *r = NULL;
    m = PyImport_ImportModule(modname);
    if (!m) goto end;
    p = PyObject_GetAttrString(m, "RefNannyAPI");
    if (!p) goto end;
    r = PyLong_AsVoidPtr(p);
end:
    Py_XDECREF(p);
    Py_XDECREF(m);
    return (__Pyx_RefNannyAPIStruct *)r;
}
#endif

/* PyObjectGetAttrStr */
#if CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PyObject* __Pyx_PyObject_GetAttrStr(PyObject* obj, PyObject* attr_name) {
    PyTypeObject* tp = Py_TYPE(obj);
    if (likely(tp->tp_getattro))
        return tp->tp_getattro(obj, attr_name);
#if PY_MAJOR_VERSION < 3
    if (likely(tp->tp_getattr))
        return tp->tp_getattr(obj, PyString_AS_STRING(attr_name));
#endif
    return PyObject_GetAttr(obj, attr_name);
}
#endif

/* GetBuiltinName */
static PyObject *__Pyx_GetBuiltinName(PyObject *name) {
    PyObject* result = __Pyx_PyObject_GetAttrStr(__pyx_b, name);
    if (unlikely(!result)) {
        PyErr_Format(PyExc_NameError,
#if PY_MAJOR_VERSION >= 3
            "name '%U' is not defined", name);
#else
            "name '%.200s' is not defined", PyString_AS_STRING(name));
#endif
    }
    return result;
}

/* RaiseArgTupleInvalid */
static void __Pyx_RaiseArgtupleInvalid(
    const char* func_name,
    int exact,
    Py_ssize_t num_min,
    Py_ssize_t num_max,
    Py_ssize_t num_found)
{
    Py_ssize_t num_expected;
    const char *more_or_less;
    if (num_found < num_min) {
        num_expected = num_min;
        more_or_less = "at least";
    } else {
        num_expected = num_max;
        more_or_less = "at most";
    }
    if (exact) {
        more_or_less = "exactly";
    }
    PyErr_Format(PyExc_TypeError,
                 "%.200s() takes %.8s %" CYTHON_FORMAT_SSIZE_T "d positional argument%.1s (%" CYTHON_FORMAT_SSIZE_T "d given)",
                 func_name, more_or_less, num_expected,
                 (num_expected == 1) ? "" : "s", num_found);
}

/* RaiseDoubleKeywords */
static void __Pyx_RaiseDoubleKeywordsError(
    const char* func_name,
    PyObject* kw_name)
{
    PyErr_Format(PyExc_TypeError,
        #if PY_MAJOR_VERSION >= 3
        "%s() got multiple values for keyword argument '%U'", func_name, kw_name);
        #else
        "%s() got multiple values for keyword argument '%s'", func_name,
        PyString_AsString(kw_name));
        #endif
}

/* ParseKeywords */
static int __Pyx_ParseOptionalKeywords(
    PyObject *kwds,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name)
{
    PyObject *key = 0, *value = 0;
    Py_ssize_t pos = 0;
    PyObject*** name;
    PyObject*** first_kw_arg = argnames + num_pos_args;
    while (PyDict_Next(kwds, &pos, &key, &value)) {
        name = first_kw_arg;
        while (*name && (**name != key)) name++;
        if (*name) {
            values[name-argnames] = value;
            continue;
        }
        name = first_kw_arg;
        #if PY_MAJOR_VERSION < 3
        if (likely(PyString_Check(key))) {
            while (*name) {
                if ((CYTHON_COMPILING_IN_PYPY || PyString_GET_SIZE(**name) == PyString_GET_SIZE(key))
                        && _PyString_Eq(**name, key)) {
                    values[name-argnames] = value;
                    break;
                }
                name++;
            }
            if (*name) continue;
            else {
                PyObject*** argname = argnames;
                while (argname != first_kw_arg) {
                    if ((**argname == key) || (
                            (CYTHON_COMPILING_IN_PYPY || PyString_GET_SIZE(**argname) == PyString_GET_SIZE(key))
                             && _PyString_Eq(**argname, key))) {
                        goto arg_passed_twice;
                    }
                    argname++;
                }
            }
        } else
        #endif
        if (likely(PyUnicode_Check(key))) {
            while (*name) {
                int cmp = (**name == key) ? 0 :
                #if !CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
                    (__Pyx_PyUnicode_GET_LENGTH(**name) != __Pyx_PyUnicode_GET_LENGTH(key)) ? 1 :
                #endif
                    PyUnicode_Compare(**name, key);
                if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                if (cmp == 0) {
                    values[name-argnames] = value;
                    break;
                }
                name++;
            }
            if (*name) continue;
            else {
                PyObject*** argname = argnames;
                while (argname != first_kw_arg) {
                    int cmp = (**argname == key) ? 0 :
                    #if !CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
                        (__Pyx_PyUnicode_GET_LENGTH(**argname) != __Pyx_PyUnicode_GET_LENGTH(key)) ? 1 :
                    #endif
                        PyUnicode_Compare(**argname, key);
                    if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                    if (cmp == 0) goto arg_passed_twice;
                    argname++;
                }
            }
        } else
            goto invalid_keyword_type;
        if (kwds2) {
            if (unlikely(PyDict_SetItem(kwds2, key, value))) goto bad;
        } else {
            goto invalid_keyword;
        }
    }
    return 0;
arg_passed_twice:
    __Pyx_RaiseDoubleKeywordsError(function_name, key);
    goto bad;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%.200s() keywords must be strings", function_name);
    goto bad;
invalid_keyword:
    PyErr_Format(PyExc_TypeError,
    #if PY_MAJOR_VERSION < 3
        "%.200s() got an unexpected keyword argument '%.200s'",
        function_name, PyString_AsString(key));
    #else
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
bad:
    return -1;
}

/* PyCFunctionFastCall */
#if CYTHON_FAST_PYCCALL
static CYTHON_INLINE PyObject * __Pyx_PyCFunction_FastCall(PyObject *func_obj, PyObject **args, Py_ssize_t nargs) {
    PyCFunctionObject *func = (PyCFunctionObject*)func_obj;
    PyCFunction meth = PyCFunction_GET_FUNCTION(func);
    PyObject *self = PyCFunction_GET_SELF(func);
    int flags = PyCFunction_GET_FLAGS(func);
    assert(PyCFunction_Check(func));
    assert(METH_FASTCALL == (flags & ~(METH_CLASS | METH_STATIC | METH_COEXIST | METH_KEYWORDS | METH_STACKLESS)));
    assert(nargs >= 0);
    assert(nargs == 0 || args != NULL);
    /* _PyCFunction_FastCallDict() must not be called with an exception set,
       because it may clear it (directly or indirectly) and so the
       caller loses its exception */
    assert(!PyErr_Occurred());
    if ((PY_VERSION_HEX < 0x030700A0) || unlikely(flags & METH_KEYWORDS)) {
        return (*((__Pyx_PyCFunctionFastWithKeywords)(void*)meth)) (self, args, nargs, NULL);
    } else {
        return (*((__Pyx_PyCFunctionFast)(void*)meth)) (self, args, nargs);
    }
}
#endif

/* PyFunctionFastCall */
#if CYTHON_FAST_PYCALL
static PyObject* __Pyx_PyFunction_FastCallNoKw(PyCodeObject *co, PyObject **args, Py_ssize_t na,
                                               PyObject *globals) {
    PyFrameObject *f;
    PyThreadState *tstate = __Pyx_PyThreadState_Current;
    PyObject **fastlocals;
    Py_ssize_t i;
    PyObject *result;
    assert(globals != NULL);
    /* XXX Perhaps we should create a specialized
       PyFrame_New() that doesn't take locals, but does
       take builtins without sanity checking them.
       */
    assert(tstate != NULL);
    f = PyFrame_New(tstate, co, globals, NULL);
    if (f == NULL) {
        return NULL;
    }
    fastlocals = __Pyx_PyFrame_GetLocalsplus(f);
    for (i = 0; i < na; i++) {
        Py_INCREF(*args);
        fastlocals[i] = *args++;
    }
    result = PyEval_EvalFrameEx(f,0);
    ++tstate->recursion_depth;
    Py_DECREF(f);
    --tstate->recursion_depth;
    return result;
}
#if 1 || PY_VERSION_HEX < 0x030600B1
static PyObject *__Pyx_PyFunction_FastCallDict(PyObject *func, PyObject **args, Py_ssize_t nargs, PyObject *kwargs) {
    PyCodeObject *co = (PyCodeObject *)PyFunction_GET_CODE(func);
    PyObject *globals = PyFunction_GET_GLOBALS(func);
    PyObject *argdefs = PyFunction_GET_DEFAULTS(func);
    PyObject *closure;
#if PY_MAJOR_VERSION >= 3
    PyObject *kwdefs;
#endif
    PyObject *kwtuple, **k;
    PyObject **d;
    Py_ssize_t nd;
    Py_ssize_t nk;
    PyObject *result;
    assert(kwargs == NULL || PyDict_Check(kwargs));
    nk = kwargs ? PyDict_Size(kwargs) : 0;
    if (Py_EnterRecursiveCall((char*)" while calling a Python object")) {
        return NULL;
    }
    if (
#if PY_MAJOR_VERSION >= 3
            co->co_kwonlyargcount == 0 &&
#endif
            likely(kwargs == NULL || nk == 0) &&
            co->co_flags == (CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE)) {
        if (argdefs == NULL && co->co_argcount == nargs) {
            result = __Pyx_PyFunction_FastCallNoKw(co, args, nargs, globals);
            goto done;
        }
        else if (nargs == 0 && argdefs != NULL
                 && co->co_argcount == Py_SIZE(argdefs)) {
            /* function called with no arguments, but all parameters have
               a default value: use default values as arguments .*/
            args = &PyTuple_GET_ITEM(argdefs, 0);
            result =__Pyx_PyFunction_FastCallNoKw(co, args, Py_SIZE(argdefs), globals);
            goto done;
        }
    }
    if (kwargs != NULL) {
        Py_ssize_t pos, i;
        kwtuple = PyTuple_New(2 * nk);
        if (kwtuple == NULL) {
            result = NULL;
            goto done;
        }
        k = &PyTuple_GET_ITEM(kwtuple, 0);
        pos = i = 0;
        while (PyDict_Next(kwargs, &pos, &k[i], &k[i+1])) {
            Py_INCREF(k[i]);
            Py_INCREF(k[i+1]);
            i += 2;
        }
        nk = i / 2;
    }
    else {
        kwtuple = NULL;
        k = NULL;
    }
    closure = PyFunction_GET_CLOSURE(func);
#if PY_MAJOR_VERSION >= 3
    kwdefs = PyFunction_GET_KW_DEFAULTS(func);
#endif
    if (argdefs != NULL) {
        d = &PyTuple_GET_ITEM(argdefs, 0);
        nd = Py_SIZE(argdefs);
    }
    else {
        d = NULL;
        nd = 0;
    }
#if PY_MAJOR_VERSION >= 3
    result = PyEval_EvalCodeEx((PyObject*)co, globals, (PyObject *)NULL,
                               args, (int)nargs,
                               k, (int)nk,
                               d, (int)nd, kwdefs, closure);
#else
    result = PyEval_EvalCodeEx(co, globals, (PyObject *)NULL,
                               args, (int)nargs,
                               k, (int)nk,
                               d, (int)nd, closure);
#endif
    Py_XDECREF(kwtuple);
done:
    Py_LeaveRecursiveCall();
    return result;
}
#endif
#endif

/* PyObjectCall */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_Call(PyObject *func, PyObject *arg, PyObject *kw) {
    PyObject *result;
    ternaryfunc call = Py_TYPE(func)->tp_call;
    if (unlikely(!call))
        return PyObject_Call(func, arg, kw);
    if (unlikely(Py_EnterRecursiveCall((char*)" while calling a Python object")))
        return NULL;
    result = (*call)(func, arg, kw);
    Py_LeaveRecursiveCall();
    if (unlikely(!result) && unlikely(!PyErr_Occurred())) {
        PyErr_SetString(
            PyExc_SystemError,
            "NULL result without error in PyObject_Call");
    }
    return result;
}
#endif

/* PyObjectCall2Args */
static CYTHON_UNUSED PyObject* __Pyx_PyObject_Call2Args(PyObject* function, PyObject* arg1, PyObject* arg2) {
    PyObject *args, *result = NULL;
    #if CYTHON_FAST_PYCALL
    if (PyFunction_Check(function)) {
        PyObject *args[2] = {arg1, arg2};
        return __Pyx_PyFunction_FastCall(function, args, 2);
    }
    #endif
    #if CYTHON_FAST_PYCCALL
    if (__Pyx_PyFastCFunction_Check(function)) {
        PyObject *args[2] = {arg1, arg2};
        return __Pyx_PyCFunction_FastCall(function, args, 2);
    }
    #endif
    args = PyTuple_New(2);
    if (unlikely(!args)) goto done;
    Py_INCREF(arg1);
    PyTuple_SET_ITEM(args, 0, arg1);
    Py_INCREF(arg2);
    PyTuple_SET_ITEM(args, 1, arg2);
    Py_INCREF(function);
    result = __Pyx_PyObject_Call(function, args, NULL);
    Py_DECREF(args);
    Py_DECREF(function);
done:
    return result;
}

/* PyObjectCallMethO */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallMethO(PyObject *func, PyObject *arg) {
    PyObject *self, *result;
    PyCFunction cfunc;
    cfunc = PyCFunction_GET_FUNCTION(func);
    self = PyCFunction_GET_SELF(func);
    if (unlikely(Py_EnterRecursiveCall((char*)" while calling a Python object")))
        return NULL;
    result = cfunc(self, arg);
    Py_LeaveRecursiveCall();
    if (unlikely(!result) && unlikely(!PyErr_Occurred())) {
        PyErr_SetString(
            PyExc_SystemError,
            "NULL result without error in PyObject_Call");
    }
    return result;
}
#endif

/* PyObjectCallOneArg */
#if CYTHON_COMPILING_IN_CPYTHON
static PyObject* __Pyx__PyObject_CallOneArg(PyObject *func, PyObject *arg) {
    PyObject *result;
    PyObject *args = PyTuple_New(1);
    if (unlikely(!args)) return NULL;
    Py_INCREF(arg);
    PyTuple_SET_ITEM(args, 0, arg);
    result = __Pyx_PyObject_Call(func, args, NULL);
    Py_DECREF(args);
    return result;
}
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallOneArg(PyObject *func, PyObject *arg) {
#if CYTHON_FAST_PYCALL
    if (PyFunction_Check(func)) {
        return __Pyx_PyFunction_FastCall(func, &arg, 1);
    }
#endif
    if (likely(PyCFunction_Check(func))) {
        if (likely(PyCFunction_GET_FLAGS(func) & METH_O)) {
            return __Pyx_PyObject_CallMethO(func, arg);
#if CYTHON_FAST_PYCCALL
        } else if (__Pyx_PyFastCFunction_Check(func)) {
            return __Pyx_PyCFunction_FastCall(func, &arg, 1);
#endif
        }
    }
    return __Pyx__PyObject_CallOneArg(func, arg);
}
#else
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallOneArg(PyObject *func, PyObject *arg) {
    PyObject *result;
    PyObject *args = PyTuple_Pack(1, arg);
    if (unlikely(!args)) return NULL;
    result = __Pyx_PyObject_Call(func, args, NULL);
    Py_DECREF(args);
    return result;
}
#endif

/* SliceObject */
static CYTHON_INLINE PyObject* __Pyx_PyObject_GetSlice(PyObject* obj,
        Py_ssize_t cstart, Py_ssize_t cstop,
        PyObject** _py_start, PyObject** _py_stop, PyObject** _py_slice,
        int has_cstart, int has_cstop, CYTHON_UNUSED int wraparound) {
#if CYTHON_USE_TYPE_SLOTS
    PyMappingMethods* mp;
#if PY_MAJOR_VERSION < 3
    PySequenceMethods* ms = Py_TYPE(obj)->tp_as_sequence;
    if (likely(ms && ms->sq_slice)) {
        if (!has_cstart) {
            if (_py_start && (*_py_start != Py_None)) {
                cstart = __Pyx_PyIndex_AsSsize_t(*_py_start);
                if ((cstart == (Py_ssize_t)-1) && PyErr_Occurred()) goto bad;
            } else
                cstart = 0;
        }
        if (!has_cstop) {
            if (_py_stop && (*_py_stop != Py_None)) {
                cstop = __Pyx_PyIndex_AsSsize_t(*_py_stop);
                if ((cstop == (Py_ssize_t)-1) && PyErr_Occurred()) goto bad;
            } else
                cstop = PY_SSIZE_T_MAX;
        }
        if (wraparound && unlikely((cstart < 0) | (cstop < 0)) && likely(ms->sq_length)) {
            Py_ssize_t l = ms->sq_length(obj);
            if (likely(l >= 0)) {
                if (cstop < 0) {
                    cstop += l;
                    if (cstop < 0) cstop = 0;
                }
                if (cstart < 0) {
                    cstart += l;
                    if (cstart < 0) cstart = 0;
                }
            } else {
                if (!PyErr_ExceptionMatches(PyExc_OverflowError))
                    goto bad;
                PyErr_Clear();
            }
        }
        return ms->sq_slice(obj, cstart, cstop);
    }
#endif
    mp = Py_TYPE(obj)->tp_as_mapping;
    if (likely(mp && mp->mp_subscript))
#endif
    {
        PyObject* result;
        PyObject *py_slice, *py_start, *py_stop;
        if (_py_slice) {
            py_slice = *_py_slice;
        } else {
            PyObject* owned_start = NULL;
            PyObject* owned_stop = NULL;
            if (_py_start) {
                py_start = *_py_start;
            } else {
                if (has_cstart) {
                    owned_start = py_start = PyInt_FromSsize_t(cstart);
                    if (unlikely(!py_start)) goto bad;
                } else
                    py_start = Py_None;
            }
            if (_py_stop) {
                py_stop = *_py_stop;
            } else {
                if (has_cstop) {
                    owned_stop = py_stop = PyInt_FromSsize_t(cstop);
                    if (unlikely(!py_stop)) {
                        Py_XDECREF(owned_start);
                        goto bad;
                    }
                } else
                    py_stop = Py_None;
            }
            py_slice = PySlice_New(py_start, py_stop, Py_None);
            Py_XDECREF(owned_start);
            Py_XDECREF(owned_stop);
            if (unlikely(!py_slice)) goto bad;
        }
#if CYTHON_USE_TYPE_SLOTS
        result = mp->mp_subscript(obj, py_slice);
#else
        result = PyObject_GetItem(obj, py_slice);
#endif
        if (!_py_slice) {
            Py_DECREF(py_slice);
        }
        return result;
    }
    PyErr_Format(PyExc_TypeError,
        "'%.200s' object is unsliceable", Py_TYPE(obj)->tp_name);
bad:
    return NULL;
}

/* PyDictVersioning */
#if CYTHON_USE_DICT_VERSIONS && CYTHON_USE_TYPE_SLOTS
static CYTHON_INLINE PY_UINT64_T __Pyx_get_tp_dict_version(PyObject *obj) {
    PyObject *dict = Py_TYPE(obj)->tp_dict;
    return likely(dict) ? __PYX_GET_DICT_VERSION(dict) : 0;
}
static CYTHON_INLINE PY_UINT64_T __Pyx_get_object_dict_version(PyObject *obj) {
    PyObject **dictptr = NULL;
    Py_ssize_t offset = Py_TYPE(obj)->tp_dictoffset;
    if (offset) {
#if CYTHON_COMPILING_IN_CPYTHON
        dictptr = (likely(offset > 0)) ? (PyObject **) ((char *)obj + offset) : _PyObject_GetDictPtr(obj);
#else
        dictptr = _PyObject_GetDictPtr(obj);
#endif
    }
    return (dictptr && *dictptr) ? __PYX_GET_DICT_VERSION(*dictptr) : 0;
}
static CYTHON_INLINE int __Pyx_object_dict_version_matches(PyObject* obj, PY_UINT64_T tp_dict_version, PY_UINT64_T obj_dict_version) {
    PyObject *dict = Py_TYPE(obj)->tp_dict;
    if (unlikely(!dict) || unlikely(tp_dict_version != __PYX_GET_DICT_VERSION(dict)))
        return 0;
    return obj_dict_version == __Pyx_get_object_dict_version(obj);
}
#endif

/* GetModuleGlobalName */
#if CYTHON_USE_DICT_VERSIONS
static PyObject *__Pyx__GetModuleGlobalName(PyObject *name, PY_UINT64_T *dict_version, PyObject **dict_cached_value)
#else
static CYTHON_INLINE PyObject *__Pyx__GetModuleGlobalName(PyObject *name)
#endif
{
    PyObject *result;
#if !CYTHON_AVOID_BORROWED_REFS
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030500A1
    result = _PyDict_GetItem_KnownHash(__pyx_d, name, ((PyASCIIObject *) name)->hash);
    __PYX_UPDATE_DICT_CACHE(__pyx_d, result, *dict_cached_value, *dict_version)
    if (likely(result)) {
        return __Pyx_NewRef(result);
    } else if (unlikely(PyErr_Occurred())) {
        return NULL;
    }
#else
    result = PyDict_GetItem(__pyx_d, name);
    __PYX_UPDATE_DICT_CACHE(__pyx_d, result, *dict_cached_value, *dict_version)
    if (likely(result)) {
        return __Pyx_NewRef(result);
    }
#endif
#else
    result = PyObject_GetItem(__pyx_d, name);
    __PYX_UPDATE_DICT_CACHE(__pyx_d, result, *dict_cached_value, *dict_version)
    if (likely(result)) {
        return __Pyx_NewRef(result);
    }
    PyErr_Clear();
#endif
    return __Pyx_GetBuiltinName(name);
}

/* BytesEquals */
static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY
    return PyObject_RichCompareBool(s1, s2, equals);
#else
    if (s1 == s2) {
        return (equals == Py_EQ);
    } else if (PyBytes_CheckExact(s1) & PyBytes_CheckExact(s2)) {
        const char *ps1, *ps2;
        Py_ssize_t length = PyBytes_GET_SIZE(s1);
        if (length != PyBytes_GET_SIZE(s2))
            return (equals == Py_NE);
        ps1 = PyBytes_AS_STRING(s1);
        ps2 = PyBytes_AS_STRING(s2);
        if (ps1[0] != ps2[0]) {
            return (equals == Py_NE);
        } else if (length == 1) {
            return (equals == Py_EQ);
        } else {
            int result;
#if CYTHON_USE_UNICODE_INTERNALS && (PY_VERSION_HEX < 0x030B0000)
            Py_hash_t hash1, hash2;
            hash1 = ((PyBytesObject*)s1)->ob_shash;
            hash2 = ((PyBytesObject*)s2)->ob_shash;
            if (hash1 != hash2 && hash1 != -1 && hash2 != -1) {
                return (equals == Py_NE);
            }
#endif
            result = memcmp(ps1, ps2, (size_t)length);
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & PyBytes_CheckExact(s2)) {
        return (equals == Py_NE);
    } else if ((s2 == Py_None) & PyBytes_CheckExact(s1)) {
        return (equals == Py_NE);
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
#endif
}

/* UnicodeEquals */
static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY
    return PyObject_RichCompareBool(s1, s2, equals);
#else
#if PY_MAJOR_VERSION < 3
    PyObject* owned_ref = NULL;
#endif
    int s1_is_unicode, s2_is_unicode;
    if (s1 == s2) {
        goto return_eq;
    }
    s1_is_unicode = PyUnicode_CheckExact(s1);
    s2_is_unicode = PyUnicode_CheckExact(s2);
#if PY_MAJOR_VERSION < 3
    if ((s1_is_unicode & (!s2_is_unicode)) && PyString_CheckExact(s2)) {
        owned_ref = PyUnicode_FromObject(s2);
        if (unlikely(!owned_ref))
            return -1;
        s2 = owned_ref;
        s2_is_unicode = 1;
    } else if ((s2_is_unicode & (!s1_is_unicode)) && PyString_CheckExact(s1)) {
        owned_ref = PyUnicode_FromObject(s1);
        if (unlikely(!owned_ref))
            return -1;
        s1 = owned_ref;
        s1_is_unicode = 1;
    } else if (((!s2_is_unicode) & (!s1_is_unicode))) {
        return __Pyx_PyBytes_Equals(s1, s2, equals);
    }
#endif
    if (s1_is_unicode & s2_is_unicode) {
        Py_ssize_t length;
        int kind;
        void *data1, *data2;
        if (unlikely(__Pyx_PyUnicode_READY(s1) < 0) || unlikely(__Pyx_PyUnicode_READY(s2) < 0))
            return -1;
        length = __Pyx_PyUnicode_GET_LENGTH(s1);
        if (length != __Pyx_PyUnicode_GET_LENGTH(s2)) {
            goto return_ne;
        }
#if CYTHON_USE_UNICODE_INTERNALS
        {
            Py_hash_t hash1, hash2;
        #if CYTHON_PEP393_ENABLED
            hash1 = ((PyASCIIObject*)s1)->hash;
            hash2 = ((PyASCIIObject*)s2)->hash;
        #else
            hash1 = ((PyUnicodeObject*)s1)->hash;
            hash2 = ((PyUnicodeObject*)s2)->hash;
        #endif
            if (hash1 != hash2 && hash1 != -1 && hash2 != -1) {
                goto return_ne;
            }
        }
#endif
        kind = __Pyx_PyUnicode_KIND(s1);
        if (kind != __Pyx_PyUnicode_KIND(s2)) {
            goto return_ne;
        }
        data1 = __Pyx_PyUnicode_DATA(s1);
        data2 = __Pyx_PyUnicode_DATA(s2);
        if (__Pyx_PyUnicode_READ(kind, data1, 0) != __Pyx_PyUnicode_READ(kind, data2, 0)) {
            goto return_ne;
        } else if (length == 1) {
            goto return_eq;
        } else {
            int result = memcmp(data1, data2, (size_t)(length * kind));
            #if PY_MAJOR_VERSION < 3
            Py_XDECREF(owned_ref);
            #endif
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & s2_is_unicode) {
        goto return_ne;
    } else if ((s2 == Py_None) & s1_is_unicode) {
        goto return_ne;
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        #if PY_MAJOR_VERSION < 3
        Py_XDECREF(owned_ref);
        #endif
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
return_eq:
    #if PY_MAJOR_VERSION < 3
    Py_XDECREF(owned_ref);
    #endif
    return (equals == Py_EQ);
return_ne:
    #if PY_MAJOR_VERSION < 3
    Py_XDECREF(owned_ref);
    #endif
    return (equals == Py_NE);
#endif
}

/* PyObjectCallNoArg */
#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_PyObject_CallNoArg(PyObject *func) {
#if CYTHON_FAST_PYCALL
    if (PyFunction_Check(func)) {
        return __Pyx_PyFunction_FastCall(func, NULL, 0);
    }
#endif
#ifdef __Pyx_CyFunction_USED
    if (likely(PyCFunction_Check(func) || __Pyx_CyFunction_Check(func)))
#else
    if (likely(PyCFunction_Check(func)))
#endif
    {
        if (likely(PyCFunction_GET_FLAGS(func) & METH_NOARGS)) {
            return __Pyx_PyObject_CallMethO(func, NULL);
        }
    }
    return __Pyx_PyObject_Call(func, __pyx_empty_tuple, NULL);
}
#endif

/* Import */
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list, int level) {
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    #if PY_MAJOR_VERSION < 3
    PyObject *py_import;
    py_import = __Pyx_PyObject_GetAttrStr(__pyx_b, __pyx_n_s_import);
    if (!py_import)
        goto bad;
    #endif
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(__pyx_m);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    {
        #if PY_MAJOR_VERSION >= 3
        if (level == -1) {
            if ((1) && (strchr(__Pyx_MODULE_NAME, '.'))) {
                module = PyImport_ImportModuleLevelObject(
                    name, global_dict, empty_dict, list, 1);
                if (!module) {
                    if (!PyErr_ExceptionMatches(PyExc_ImportError))
                        goto bad;
                    PyErr_Clear();
                }
            }
            level = 0;
        }
        #endif
        if (!module) {
            #if PY_MAJOR_VERSION < 3
            PyObject *py_level = PyInt_FromLong(level);
            if (!py_level)
                goto bad;
            module = PyObject_CallFunctionObjArgs(py_import,
                name, global_dict, empty_dict, list, py_level, (PyObject *)NULL);
            Py_DECREF(py_level);
            #else
            module = PyImport_ImportModuleLevelObject(
                name, global_dict, empty_dict, list, level);
            #endif
        }
    }
bad:
    #if PY_MAJOR_VERSION < 3
    Py_XDECREF(py_import);
    #endif
    Py_XDECREF(empty_list);
    Py_XDECREF(empty_dict);
    return module;
}

/* GetItemInt */
static PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j) {
    PyObject *r;
    if (!j) return NULL;
    r = PyObject_GetItem(o, j);
    Py_DECREF(j);
    return r;
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                              CYTHON_NCP_UNUSED int wraparound,
                                                              CYTHON_NCP_UNUSED int boundscheck) {
#if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += PyList_GET_SIZE(o);
    }
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, PyList_GET_SIZE(o)))) {
        PyObject *r = PyList_GET_ITEM(o, wrapped_i);
        Py_INCREF(r);
        return r;
    }
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
#else
    return PySequence_GetItem(o, i);
#endif
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Tuple_Fast(PyObject *o, Py_ssize_t i,
                                                              CYTHON_NCP_UNUSED int wraparound,
                                                              CYTHON_NCP_UNUSED int boundscheck) {
#if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += PyTuple_GET_SIZE(o);
    }
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, PyTuple_GET_SIZE(o)))) {
        PyObject *r = PyTuple_GET_ITEM(o, wrapped_i);
        Py_INCREF(r);
        return r;
    }
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
#else
    return PySequence_GetItem(o, i);
#endif
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i, int is_list,
                                                     CYTHON_NCP_UNUSED int wraparound,
                                                     CYTHON_NCP_UNUSED int boundscheck) {
#if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS && CYTHON_USE_TYPE_SLOTS
    if (is_list || PyList_CheckExact(o)) {
        Py_ssize_t n = ((!wraparound) | likely(i >= 0)) ? i : i + PyList_GET_SIZE(o);
        if ((!boundscheck) || (likely(__Pyx_is_valid_index(n, PyList_GET_SIZE(o))))) {
            PyObject *r = PyList_GET_ITEM(o, n);
            Py_INCREF(r);
            return r;
        }
    }
    else if (PyTuple_CheckExact(o)) {
        Py_ssize_t n = ((!wraparound) | likely(i >= 0)) ? i : i + PyTuple_GET_SIZE(o);
        if ((!boundscheck) || likely(__Pyx_is_valid_index(n, PyTuple_GET_SIZE(o)))) {
            PyObject *r = PyTuple_GET_ITEM(o, n);
            Py_INCREF(r);
            return r;
        }
    } else {
        PySequenceMethods *m = Py_TYPE(o)->tp_as_sequence;
        if (likely(m && m->sq_item)) {
            if (wraparound && unlikely(i < 0) && likely(m->sq_length)) {
                Py_ssize_t l = m->sq_length(o);
                if (likely(l >= 0)) {
                    i += l;
                } else {
                    if (!PyErr_ExceptionMatches(PyExc_OverflowError))
                        return NULL;
                    PyErr_Clear();
                }
            }
            return m->sq_item(o, i);
        }
    }
#else
    if (is_list || PySequence_Check(o)) {
        return PySequence_GetItem(o, i);
    }
#endif
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
}

/* ObjectGetItem */
#if CYTHON_USE_TYPE_SLOTS
static PyObject *__Pyx_PyObject_GetIndex(PyObject *obj, PyObject* index) {
    PyObject *runerr;
    Py_ssize_t key_value;
    PySequenceMethods *m = Py_TYPE(obj)->tp_as_sequence;
    if (unlikely(!(m && m->sq_item))) {
        PyErr_Format(PyExc_TypeError, "'%.200s' object is not subscriptable", Py_TYPE(obj)->tp_name);
        return NULL;
    }
    key_value = __Pyx_PyIndex_AsSsize_t(index);
    if (likely(key_value != -1 || !(runerr = PyErr_Occurred()))) {
        return __Pyx_GetItemInt_Fast(obj, key_value, 0, 1, 1);
    }
    if (PyErr_GivenExceptionMatches(runerr, PyExc_OverflowError)) {
        PyErr_Clear();
        PyErr_Format(PyExc_IndexError, "cannot fit '%.200s' into an index-sized integer", Py_TYPE(index)->tp_name);
    }
    return NULL;
}
static PyObject *__Pyx_PyObject_GetItem(PyObject *obj, PyObject* key) {
    PyMappingMethods *m = Py_TYPE(obj)->tp_as_mapping;
    if (likely(m && m->mp_subscript)) {
        return m->mp_subscript(obj, key);
    }
    return __Pyx_PyObject_GetIndex(obj, key);
}
#endif

/* FetchCommonType */
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* fake_module;
    PyTypeObject* cached_type = NULL;
    fake_module = PyImport_AddModule((char*) "_cython_" CYTHON_ABI);
    if (!fake_module) return NULL;
    Py_INCREF(fake_module);
    cached_type = (PyTypeObject*) PyObject_GetAttrString(fake_module, type->tp_name);
    if (cached_type) {
        if (!PyType_Check((PyObject*)cached_type)) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s is not a type object",
                type->tp_name);
            goto bad;
        }
        if (cached_type->tp_basicsize != type->tp_basicsize) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s has the wrong size, try recompiling",
                type->tp_name);
            goto bad;
        }
    } else {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        if (PyType_Ready(type) < 0) goto bad;
        if (PyObject_SetAttrString(fake_module, type->tp_name, (PyObject*) type) < 0)
            goto bad;
        Py_INCREF(type);
        cached_type = type;
    }
done:
    Py_DECREF(fake_module);
    return cached_type;
bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}

/* CythonFunctionShared */
#include <structmember.h>
static PyObject *
__Pyx_CyFunction_get_doc(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *closure)
{
    if (unlikely(op->func_doc == NULL)) {
        if (op->func.m_ml->ml_doc) {
#if PY_MAJOR_VERSION >= 3
            op->func_doc = PyUnicode_FromString(op->func.m_ml->ml_doc);
#else
            op->func_doc = PyString_FromString(op->func.m_ml->ml_doc);
#endif
            if (unlikely(op->func_doc == NULL))
                return NULL;
        } else {
            Py_INCREF(Py_None);
            return Py_None;
        }
    }
    Py_INCREF(op->func_doc);
    return op->func_doc;
}
static int
__Pyx_CyFunction_set_doc(__pyx_CyFunctionObject *op, PyObject *value, CYTHON_UNUSED void *context)
{
    PyObject *tmp = op->func_doc;
    if (value == NULL) {
        value = Py_None;
    }
    Py_INCREF(value);
    op->func_doc = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_name(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    if (unlikely(op->func_name == NULL)) {
#if PY_MAJOR_VERSION >= 3
        op->func_name = PyUnicode_InternFromString(op->func.m_ml->ml_name);
#else
        op->func_name = PyString_InternFromString(op->func.m_ml->ml_name);
#endif
        if (unlikely(op->func_name == NULL))
            return NULL;
    }
    Py_INCREF(op->func_name);
    return op->func_name;
}
static int
__Pyx_CyFunction_set_name(__pyx_CyFunctionObject *op, PyObject *value, CYTHON_UNUSED void *context)
{
    PyObject *tmp;
#if PY_MAJOR_VERSION >= 3
    if (unlikely(value == NULL || !PyUnicode_Check(value)))
#else
    if (unlikely(value == NULL || !PyString_Check(value)))
#endif
    {
        PyErr_SetString(PyExc_TypeError,
                        "__name__ must be set to a string object");
        return -1;
    }
    tmp = op->func_name;
    Py_INCREF(value);
    op->func_name = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_qualname(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    Py_INCREF(op->func_qualname);
    return op->func_qualname;
}
static int
__Pyx_CyFunction_set_qualname(__pyx_CyFunctionObject *op, PyObject *value, CYTHON_UNUSED void *context)
{
    PyObject *tmp;
#if PY_MAJOR_VERSION >= 3
    if (unlikely(value == NULL || !PyUnicode_Check(value)))
#else
    if (unlikely(value == NULL || !PyString_Check(value)))
#endif
    {
        PyErr_SetString(PyExc_TypeError,
                        "__qualname__ must be set to a string object");
        return -1;
    }
    tmp = op->func_qualname;
    Py_INCREF(value);
    op->func_qualname = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_self(__pyx_CyFunctionObject *m, CYTHON_UNUSED void *closure)
{
    PyObject *self;
    self = m->func_closure;
    if (self == NULL)
        self = Py_None;
    Py_INCREF(self);
    return self;
}
static PyObject *
__Pyx_CyFunction_get_dict(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    if (unlikely(op->func_dict == NULL)) {
        op->func_dict = PyDict_New();
        if (unlikely(op->func_dict == NULL))
            return NULL;
    }
    Py_INCREF(op->func_dict);
    return op->func_dict;
}
static int
__Pyx_CyFunction_set_dict(__pyx_CyFunctionObject *op, PyObject *value, CYTHON_UNUSED void *context)
{
    PyObject *tmp;
    if (unlikely(value == NULL)) {
        PyErr_SetString(PyExc_TypeError,
               "function's dictionary may not be deleted");
        return -1;
    }
    if (unlikely(!PyDict_Check(value))) {
        PyErr_SetString(PyExc_TypeError,
               "setting function's dictionary to a non-dict");
        return -1;
    }
    tmp = op->func_dict;
    Py_INCREF(value);
    op->func_dict = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_globals(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    Py_INCREF(op->func_globals);
    return op->func_globals;
}
static PyObject *
__Pyx_CyFunction_get_closure(CYTHON_UNUSED __pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    Py_INCREF(Py_None);
    return Py_None;
}
static PyObject *
__Pyx_CyFunction_get_code(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context)
{
    PyObject* result = (op->func_code) ? op->func_code : Py_None;
    Py_INCREF(result);
    return result;
}
static int
__Pyx_CyFunction_init_defaults(__pyx_CyFunctionObject *op) {
    int result = 0;
    PyObject *res = op->defaults_getter((PyObject *) op);
    if (unlikely(!res))
        return -1;
    #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    op->defaults_tuple = PyTuple_GET_ITEM(res, 0);
    Py_INCREF(op->defaults_tuple);
    op->defaults_kwdict = PyTuple_GET_ITEM(res, 1);
    Py_INCREF(op->defaults_kwdict);
    #else
    op->defaults_tuple = PySequence_ITEM(res, 0);
    if (unlikely(!op->defaults_tuple)) result = -1;
    else {
        op->defaults_kwdict = PySequence_ITEM(res, 1);
        if (unlikely(!op->defaults_kwdict)) result = -1;
    }
    #endif
    Py_DECREF(res);
    return result;
}
static int
__Pyx_CyFunction_set_defaults(__pyx_CyFunctionObject *op, PyObject* value, CYTHON_UNUSED void *context) {
    PyObject* tmp;
    if (!value) {
        value = Py_None;
    } else if (value != Py_None && !PyTuple_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "__defaults__ must be set to a tuple object");
        return -1;
    }
    Py_INCREF(value);
    tmp = op->defaults_tuple;
    op->defaults_tuple = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_defaults(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context) {
    PyObject* result = op->defaults_tuple;
    if (unlikely(!result)) {
        if (op->defaults_getter) {
            if (__Pyx_CyFunction_init_defaults(op) < 0) return NULL;
            result = op->defaults_tuple;
        } else {
            result = Py_None;
        }
    }
    Py_INCREF(result);
    return result;
}
static int
__Pyx_CyFunction_set_kwdefaults(__pyx_CyFunctionObject *op, PyObject* value, CYTHON_UNUSED void *context) {
    PyObject* tmp;
    if (!value) {
        value = Py_None;
    } else if (value != Py_None && !PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "__kwdefaults__ must be set to a dict object");
        return -1;
    }
    Py_INCREF(value);
    tmp = op->defaults_kwdict;
    op->defaults_kwdict = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_kwdefaults(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context) {
    PyObject* result = op->defaults_kwdict;
    if (unlikely(!result)) {
        if (op->defaults_getter) {
            if (__Pyx_CyFunction_init_defaults(op) < 0) return NULL;
            result = op->defaults_kwdict;
        } else {
            result = Py_None;
        }
    }
    Py_INCREF(result);
    return result;
}
static int
__Pyx_CyFunction_set_annotations(__pyx_CyFunctionObject *op, PyObject* value, CYTHON_UNUSED void *context) {
    PyObject* tmp;
    if (!value || value == Py_None) {
        value = NULL;
    } else if (!PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "__annotations__ must be set to a dict object");
        return -1;
    }
    Py_XINCREF(value);
    tmp = op->func_annotations;
    op->func_annotations = value;
    Py_XDECREF(tmp);
    return 0;
}
static PyObject *
__Pyx_CyFunction_get_annotations(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *context) {
    PyObject* result = op->func_annotations;
    if (unlikely(!result)) {
        result = PyDict_New();
        if (unlikely(!result)) return NULL;
        op->func_annotations = result;
    }
    Py_INCREF(result);
    return result;
}
static PyGetSetDef __pyx_CyFunction_getsets[] = {
    {(char *) "func_doc", (getter)__Pyx_CyFunction_get_doc, (setter)__Pyx_CyFunction_set_doc, 0, 0},
    {(char *) "__doc__",  (getter)__Pyx_CyFunction_get_doc, (setter)__Pyx_CyFunction_set_doc, 0, 0},
    {(char *) "func_name", (getter)__Pyx_CyFunction_get_name, (setter)__Pyx_CyFunction_set_name, 0, 0},
    {(char *) "__name__", (getter)__Pyx_CyFunction_get_name, (setter)__Pyx_CyFunction_set_name, 0, 0},
    {(char *) "__qualname__", (getter)__Pyx_CyFunction_get_qualname, (setter)__Pyx_CyFunction_set_qualname, 0, 0},
    {(char *) "__self__", (getter)__Pyx_CyFunction_get_self, 0, 0, 0},
    {(char *) "func_dict", (getter)__Pyx_CyFunction_get_dict, (setter)__Pyx_CyFunction_set_dict, 0, 0},
    {(char *) "__dict__", (getter)__Pyx_CyFunction_get_dict, (setter)__Pyx_CyFunction_set_dict, 0, 0},
    {(char *) "func_globals", (getter)__Pyx_CyFunction_get_globals, 0, 0, 0},
    {(char *) "__globals__", (getter)__Pyx_CyFunction_get_globals, 0, 0, 0},
    {(char *) "func_closure", (getter)__Pyx_CyFunction_get_closure, 0, 0, 0},
    {(char *) "__closure__", (getter)__Pyx_CyFunction_get_closure, 0, 0, 0},
    {(char *) "func_code", (getter)__Pyx_CyFunction_get_code, 0, 0, 0},
    {(char *) "__code__", (getter)__Pyx_CyFunction_get_code, 0, 0, 0},
    {(char *) "func_defaults", (getter)__Pyx_CyFunction_get_defaults, (setter)__Pyx_CyFunction_set_defaults, 0, 0},
    {(char *) "__defaults__", (getter)__Pyx_CyFunction_get_defaults, (setter)__Pyx_CyFunction_set_defaults, 0, 0},
    {(char *) "__kwdefaults__", (getter)__Pyx_CyFunction_get_kwdefaults, (setter)__Pyx_CyFunction_set_kwdefaults, 0, 0},
    {(char *) "__annotations__", (getter)__Pyx_CyFunction_get_annotations, (setter)__Pyx_CyFunction_set_annotations, 0, 0},
    {0, 0, 0, 0, 0}
};
static PyMemberDef __pyx_CyFunction_members[] = {
    {(char *) "__module__", T_OBJECT, offsetof(PyCFunctionObject, m_module), PY_WRITE_RESTRICTED, 0},
    {0, 0, 0,  0, 0}
};
static PyObject *
__Pyx_CyFunction_reduce(__pyx_CyFunctionObject *m, CYTHON_UNUSED PyObject *args)
{
#if PY_MAJOR_VERSION >= 3
    Py_INCREF(m->func_qualname);
    return m->func_qualname;
#else
    return PyString_FromString(m->func.m_ml->ml_name);
#endif
}
static PyMethodDef __pyx_CyFunction_methods[] = {
    {"__reduce__", (PyCFunction)__Pyx_CyFunction_reduce, METH_VARARGS, 0},
    {0, 0, 0, 0}
};
#if PY_VERSION_HEX < 0x030500A0
#define __Pyx_CyFunction_weakreflist(cyfunc) ((cyfunc)->func_weakreflist)
#else
#define __Pyx_CyFunction_weakreflist(cyfunc) ((cyfunc)->func.m_weakreflist)
#endif
static PyObject *__Pyx_CyFunction_Init(__pyx_CyFunctionObject *op, PyMethodDef *ml, int flags, PyObject* qualname,
                                       PyObject *closure, PyObject *module, PyObject* globals, PyObject* code) {
    if (unlikely(op == NULL))
        return NULL;
    op->flags = flags;
    __Pyx_CyFunction_weakreflist(op) = NULL;
    op->func.m_ml = ml;
    op->func.m_self = (PyObject *) op;
    Py_XINCREF(closure);
    op->func_closure = closure;
    Py_XINCREF(module);
    op->func.m_module = module;
    op->func_dict = NULL;
    op->func_name = NULL;
    Py_INCREF(qualname);
    op->func_qualname = qualname;
    op->func_doc = NULL;
    op->func_classobj = NULL;
    op->func_globals = globals;
    Py_INCREF(op->func_globals);
    Py_XINCREF(code);
    op->func_code = code;
    op->defaults_pyobjects = 0;
    op->defaults_size = 0;
    op->defaults = NULL;
    op->defaults_tuple = NULL;
    op->defaults_kwdict = NULL;
    op->defaults_getter = NULL;
    op->func_annotations = NULL;
    return (PyObject *) op;
}
static int
__Pyx_CyFunction_clear(__pyx_CyFunctionObject *m)
{
    Py_CLEAR(m->func_closure);
    Py_CLEAR(m->func.m_module);
    Py_CLEAR(m->func_dict);
    Py_CLEAR(m->func_name);
    Py_CLEAR(m->func_qualname);
    Py_CLEAR(m->func_doc);
    Py_CLEAR(m->func_globals);
    Py_CLEAR(m->func_code);
    Py_CLEAR(m->func_classobj);
    Py_CLEAR(m->defaults_tuple);
    Py_CLEAR(m->defaults_kwdict);
    Py_CLEAR(m->func_annotations);
    if (m->defaults) {
        PyObject **pydefaults = __Pyx_CyFunction_Defaults(PyObject *, m);
        int i;
        for (i = 0; i < m->defaults_pyobjects; i++)
            Py_XDECREF(pydefaults[i]);
        PyObject_Free(m->defaults);
        m->defaults = NULL;
    }
    return 0;
}
static void __Pyx__CyFunction_dealloc(__pyx_CyFunctionObject *m)
{
    if (__Pyx_CyFunction_weakreflist(m) != NULL)
        PyObject_ClearWeakRefs((PyObject *) m);
    __Pyx_CyFunction_clear(m);
    PyObject_GC_Del(m);
}
static void __Pyx_CyFunction_dealloc(__pyx_CyFunctionObject *m)
{
    PyObject_GC_UnTrack(m);
    __Pyx__CyFunction_dealloc(m);
}
static int __Pyx_CyFunction_traverse(__pyx_CyFunctionObject *m, visitproc visit, void *arg)
{
    Py_VISIT(m->func_closure);
    Py_VISIT(m->func.m_module);
    Py_VISIT(m->func_dict);
    Py_VISIT(m->func_name);
    Py_VISIT(m->func_qualname);
    Py_VISIT(m->func_doc);
    Py_VISIT(m->func_globals);
    Py_VISIT(m->func_code);
    Py_VISIT(m->func_classobj);
    Py_VISIT(m->defaults_tuple);
    Py_VISIT(m->defaults_kwdict);
    if (m->defaults) {
        PyObject **pydefaults = __Pyx_CyFunction_Defaults(PyObject *, m);
        int i;
        for (i = 0; i < m->defaults_pyobjects; i++)
            Py_VISIT(pydefaults[i]);
    }
    return 0;
}
static PyObject *__Pyx_CyFunction_descr_get(PyObject *func, PyObject *obj, PyObject *type)
{
#if PY_MAJOR_VERSION < 3
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;
    if (m->flags & __Pyx_CYFUNCTION_STATICMETHOD) {
        Py_INCREF(func);
        return func;
    }
    if (m->flags & __Pyx_CYFUNCTION_CLASSMETHOD) {
        if (type == NULL)
            type = (PyObject *)(Py_TYPE(obj));
        return __Pyx_PyMethod_New(func, type, (PyObject *)(Py_TYPE(type)));
    }
    if (obj == Py_None)
        obj = NULL;
#endif
    return __Pyx_PyMethod_New(func, obj, type);
}
static PyObject*
__Pyx_CyFunction_repr(__pyx_CyFunctionObject *op)
{
#if PY_MAJOR_VERSION >= 3
    return PyUnicode_FromFormat("<cyfunction %U at %p>",
                                op->func_qualname, (void *)op);
#else
    return PyString_FromFormat("<cyfunction %s at %p>",
                               PyString_AsString(op->func_qualname), (void *)op);
#endif
}
static PyObject * __Pyx_CyFunction_CallMethod(PyObject *func, PyObject *self, PyObject *arg, PyObject *kw) {
    PyCFunctionObject* f = (PyCFunctionObject*)func;
    PyCFunction meth = f->m_ml->ml_meth;
    Py_ssize_t size;
    switch (f->m_ml->ml_flags & (METH_VARARGS | METH_KEYWORDS | METH_NOARGS | METH_O)) {
    case METH_VARARGS:
        if (likely(kw == NULL || PyDict_Size(kw) == 0))
            return (*meth)(self, arg);
        break;
    case METH_VARARGS | METH_KEYWORDS:
        return (*(PyCFunctionWithKeywords)(void*)meth)(self, arg, kw);
    case METH_NOARGS:
        if (likely(kw == NULL || PyDict_Size(kw) == 0)) {
            size = PyTuple_GET_SIZE(arg);
            if (likely(size == 0))
                return (*meth)(self, NULL);
            PyErr_Format(PyExc_TypeError,
                "%.200s() takes no arguments (%" CYTHON_FORMAT_SSIZE_T "d given)",
                f->m_ml->ml_name, size);
            return NULL;
        }
        break;
    case METH_O:
        if (likely(kw == NULL || PyDict_Size(kw) == 0)) {
            size = PyTuple_GET_SIZE(arg);
            if (likely(size == 1)) {
                PyObject *result, *arg0;
                #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
                arg0 = PyTuple_GET_ITEM(arg, 0);
                #else
                arg0 = PySequence_ITEM(arg, 0); if (unlikely(!arg0)) return NULL;
                #endif
                result = (*meth)(self, arg0);
                #if !(CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS)
                Py_DECREF(arg0);
                #endif
                return result;
            }
            PyErr_Format(PyExc_TypeError,
                "%.200s() takes exactly one argument (%" CYTHON_FORMAT_SSIZE_T "d given)",
                f->m_ml->ml_name, size);
            return NULL;
        }
        break;
    default:
        PyErr_SetString(PyExc_SystemError, "Bad call flags in "
                        "__Pyx_CyFunction_Call. METH_OLDARGS is no "
                        "longer supported!");
        return NULL;
    }
    PyErr_Format(PyExc_TypeError, "%.200s() takes no keyword arguments",
                 f->m_ml->ml_name);
    return NULL;
}
static CYTHON_INLINE PyObject *__Pyx_CyFunction_Call(PyObject *func, PyObject *arg, PyObject *kw) {
    return __Pyx_CyFunction_CallMethod(func, ((PyCFunctionObject*)func)->m_self, arg, kw);
}
static PyObject *__Pyx_CyFunction_CallAsMethod(PyObject *func, PyObject *args, PyObject *kw) {
    PyObject *result;
    __pyx_CyFunctionObject *cyfunc = (__pyx_CyFunctionObject *) func;
    if ((cyfunc->flags & __Pyx_CYFUNCTION_CCLASS) && !(cyfunc->flags & __Pyx_CYFUNCTION_STATICMETHOD)) {
        Py_ssize_t argc;
        PyObject *new_args;
        PyObject *self;
        argc = PyTuple_GET_SIZE(args);
        new_args = PyTuple_GetSlice(args, 1, argc);
        if (unlikely(!new_args))
            return NULL;
        self = PyTuple_GetItem(args, 0);
        if (unlikely(!self)) {
            Py_DECREF(new_args);
            PyErr_Format(PyExc_TypeError,
                         "unbound method %.200S() needs an argument",
                         cyfunc->func_qualname);
            return NULL;
        }
        result = __Pyx_CyFunction_CallMethod(func, self, new_args, kw);
        Py_DECREF(new_args);
    } else {
        result = __Pyx_CyFunction_Call(func, args, kw);
    }
    return result;
}
static PyTypeObject __pyx_CyFunctionType_type = {
    PyVarObject_HEAD_INIT(0, 0)
    "cython_function_or_method",
    sizeof(__pyx_CyFunctionObject),
    0,
    (destructor) __Pyx_CyFunction_dealloc,
    0,
    0,
    0,
#if PY_MAJOR_VERSION < 3
    0,
#else
    0,
#endif
    (reprfunc) __Pyx_CyFunction_repr,
    0,
    0,
    0,
    0,
    __Pyx_CyFunction_CallAsMethod,
    0,
    0,
    0,
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    0,
    (traverseproc) __Pyx_CyFunction_traverse,
    (inquiry) __Pyx_CyFunction_clear,
    0,
#if PY_VERSION_HEX < 0x030500A0
    offsetof(__pyx_CyFunctionObject, func_weakreflist),
#else
    offsetof(PyCFunctionObject, m_weakreflist),
#endif
    0,
    0,
    __pyx_CyFunction_methods,
    __pyx_CyFunction_members,
    __pyx_CyFunction_getsets,
    0,
    0,
    __Pyx_CyFunction_descr_get,
    0,
    offsetof(__pyx_CyFunctionObject, func_dict),
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
#if PY_VERSION_HEX >= 0x030400a1
    0,
#endif
#if PY_VERSION_HEX >= 0x030800b1 && (!CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07030800)
    0,
#endif
#if PY_VERSION_HEX >= 0x030800b4 && PY_VERSION_HEX < 0x03090000
    0,
#endif
#if CYTHON_COMPILING_IN_PYPY && PY_VERSION_HEX >= 0x03090000
    0,
#endif
};
static int __pyx_CyFunction_init(void) {
    __pyx_CyFunctionType = __Pyx_FetchCommonType(&__pyx_CyFunctionType_type);
    if (unlikely(__pyx_CyFunctionType == NULL)) {
        return -1;
    }
    return 0;
}
static CYTHON_INLINE void *__Pyx_CyFunction_InitDefaults(PyObject *func, size_t size, int pyobjects) {
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;
    m->defaults = PyObject_Malloc(size);
    if (unlikely(!m->defaults))
        return PyErr_NoMemory();
    memset(m->defaults, 0, size);
    m->defaults_pyobjects = pyobjects;
    m->defaults_size = size;
    return m->defaults;
}
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsTuple(PyObject *func, PyObject *tuple) {
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;
    m->defaults_tuple = tuple;
    Py_INCREF(tuple);
}
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsKwDict(PyObject *func, PyObject *dict) {
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;
    m->defaults_kwdict = dict;
    Py_INCREF(dict);
}
static CYTHON_INLINE void __Pyx_CyFunction_SetAnnotationsDict(PyObject *func, PyObject *dict) {
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;
    m->func_annotations = dict;
    Py_INCREF(dict);
}

/* CythonFunction */
static PyObject *__Pyx_CyFunction_New(PyMethodDef *ml, int flags, PyObject* qualname,
                                      PyObject *closure, PyObject *module, PyObject* globals, PyObject* code) {
    PyObject *op = __Pyx_CyFunction_Init(
        PyObject_GC_New(__pyx_CyFunctionObject, __pyx_CyFunctionType),
        ml, flags, qualname, closure, module, globals, code
    );
    if (likely(op)) {
        PyObject_GC_Track(op);
    }
    return op;
}

/* PyErrFetchRestore */
#if CYTHON_FAST_THREAD_STATE
static CYTHON_INLINE void __Pyx_ErrRestoreInState(PyThreadState *tstate, PyObject *type, PyObject *value, PyObject *tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    tmp_type = tstate->curexc_type;
    tmp_value = tstate->curexc_value;
    tmp_tb = tstate->curexc_traceback;
    tstate->curexc_type = type;
    tstate->curexc_value = value;
    tstate->curexc_traceback = tb;
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
}
static CYTHON_INLINE void __Pyx_ErrFetchInState(PyThreadState *tstate, PyObject **type, PyObject **value, PyObject **tb) {
    *type = tstate->curexc_type;
    *value = tstate->curexc_value;
    *tb = tstate->curexc_traceback;
    tstate->curexc_type = 0;
    tstate->curexc_value = 0;
    tstate->curexc_traceback = 0;
}
#endif

/* CLineInTraceback */
#ifndef CYTHON_CLINE_IN_TRACEBACK
static int __Pyx_CLineForTraceback(CYTHON_NCP_UNUSED PyThreadState *tstate, int c_line) {
    PyObject *use_cline;
    PyObject *ptype, *pvalue, *ptraceback;
#if CYTHON_COMPILING_IN_CPYTHON
    PyObject **cython_runtime_dict;
#endif
    if (unlikely(!__pyx_cython_runtime)) {
        return c_line;
    }
    __Pyx_ErrFetchInState(tstate, &ptype, &pvalue, &ptraceback);
#if CYTHON_COMPILING_IN_CPYTHON
    cython_runtime_dict = _PyObject_GetDictPtr(__pyx_cython_runtime);
    if (likely(cython_runtime_dict)) {
        __PYX_PY_DICT_LOOKUP_IF_MODIFIED(
            use_cline, *cython_runtime_dict,
            __Pyx_PyDict_GetItemStr(*cython_runtime_dict, __pyx_n_s_cline_in_traceback))
    } else
#endif
    {
      PyObject *use_cline_obj = __Pyx_PyObject_GetAttrStr(__pyx_cython_runtime, __pyx_n_s_cline_in_traceback);
      if (use_cline_obj) {
        use_cline = PyObject_Not(use_cline_obj) ? Py_False : Py_True;
        Py_DECREF(use_cline_obj);
      } else {
        PyErr_Clear();
        use_cline = NULL;
      }
    }
    if (!use_cline) {
        c_line = 0;
        (void) PyObject_SetAttr(__pyx_cython_runtime, __pyx_n_s_cline_in_traceback, Py_False);
    }
    else if (use_cline == Py_False || (use_cline != Py_True && PyObject_Not(use_cline) != 0)) {
        c_line = 0;
    }
    __Pyx_ErrRestoreInState(tstate, ptype, pvalue, ptraceback);
    return c_line;
}
#endif

/* CodeObjectCache */
static int __pyx_bisect_code_objects(__Pyx_CodeObjectCacheEntry* entries, int count, int code_line) {
    int start = 0, mid = 0, end = count - 1;
    if (end >= 0 && code_line > entries[end].code_line) {
        return count;
    }
    while (start < end) {
        mid = start + (end - start) / 2;
        if (code_line < entries[mid].code_line) {
            end = mid;
        } else if (code_line > entries[mid].code_line) {
             start = mid + 1;
        } else {
            return mid;
        }
    }
    if (code_line <= entries[mid].code_line) {
        return mid;
    } else {
        return mid + 1;
    }
}
static PyCodeObject *__pyx_find_code_object(int code_line) {
    PyCodeObject* code_object;
    int pos;
    if (unlikely(!code_line) || unlikely(!__pyx_code_cache.entries)) {
        return NULL;
    }
    pos = __pyx_bisect_code_objects(__pyx_code_cache.entries, __pyx_code_cache.count, code_line);
    if (unlikely(pos >= __pyx_code_cache.count) || unlikely(__pyx_code_cache.entries[pos].code_line != code_line)) {
        return NULL;
    }
    code_object = __pyx_code_cache.entries[pos].code_object;
    Py_INCREF(code_object);
    return code_object;
}
static void __pyx_insert_code_object(int code_line, PyCodeObject* code_object) {
    int pos, i;
    __Pyx_CodeObjectCacheEntry* entries = __pyx_code_cache.entries;
    if (unlikely(!code_line)) {
        return;
    }
    if (unlikely(!entries)) {
        entries = (__Pyx_CodeObjectCacheEntry*)PyMem_Malloc(64*sizeof(__Pyx_CodeObjectCacheEntry));
        if (likely(entries)) {
            __pyx_code_cache.entries = entries;
            __pyx_code_cache.max_count = 64;
            __pyx_code_cache.count = 1;
            entries[0].code_line = code_line;
            entries[0].code_object = code_object;
            Py_INCREF(code_object);
        }
        return;
    }
    pos = __pyx_bisect_code_objects(__pyx_code_cache.entries, __pyx_code_cache.count, code_line);
    if ((pos < __pyx_code_cache.count) && unlikely(__pyx_code_cache.entries[pos].code_line == code_line)) {
        PyCodeObject* tmp = entries[pos].code_object;
        entries[pos].code_object = code_object;
        Py_DECREF(tmp);
        return;
    }
    if (__pyx_code_cache.count == __pyx_code_cache.max_count) {
        int new_max = __pyx_code_cache.max_count + 64;
        entries = (__Pyx_CodeObjectCacheEntry*)PyMem_Realloc(
            __pyx_code_cache.entries, ((size_t)new_max) * sizeof(__Pyx_CodeObjectCacheEntry));
        if (unlikely(!entries)) {
            return;
        }
        __pyx_code_cache.entries = entries;
        __pyx_code_cache.max_count = new_max;
    }
    for (i=__pyx_code_cache.count; i>pos; i--) {
        entries[i] = entries[i-1];
    }
    entries[pos].code_line = code_line;
    entries[pos].code_object = code_object;
    __pyx_code_cache.count++;
    Py_INCREF(code_object);
}

/* AddTraceback */
#include "compile.h"
#include "frameobject.h"
#include "traceback.h"
#if PY_VERSION_HEX >= 0x030b00a6
  #ifndef Py_BUILD_CORE
    #define Py_BUILD_CORE 1
  #endif
  #include "internal/pycore_frame.h"
#endif
static PyCodeObject* __Pyx_CreateCodeObjectForTraceback(
            const char *funcname, int c_line,
            int py_line, const char *filename) {
    PyCodeObject *py_code = NULL;
    PyObject *py_funcname = NULL;
    #if PY_MAJOR_VERSION < 3
    PyObject *py_srcfile = NULL;
    py_srcfile = PyString_FromString(filename);
    if (!py_srcfile) goto bad;
    #endif
    if (c_line) {
        #if PY_MAJOR_VERSION < 3
        py_funcname = PyString_FromFormat( "%s (%s:%d)", funcname, __pyx_cfilenm, c_line);
        if (!py_funcname) goto bad;
        #else
        py_funcname = PyUnicode_FromFormat( "%s (%s:%d)", funcname, __pyx_cfilenm, c_line);
        if (!py_funcname) goto bad;
        funcname = PyUnicode_AsUTF8(py_funcname);
        if (!funcname) goto bad;
        #endif
    }
    else {
        #if PY_MAJOR_VERSION < 3
        py_funcname = PyString_FromString(funcname);
        if (!py_funcname) goto bad;
        #endif
    }
    #if PY_MAJOR_VERSION < 3
    py_code = __Pyx_PyCode_New(
        0,
        0,
        0,
        0,
        0,
        __pyx_empty_bytes, /*PyObject *code,*/
        __pyx_empty_tuple, /*PyObject *consts,*/
        __pyx_empty_tuple, /*PyObject *names,*/
        __pyx_empty_tuple, /*PyObject *varnames,*/
        __pyx_empty_tuple, /*PyObject *freevars,*/
        __pyx_empty_tuple, /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        py_line,
        __pyx_empty_bytes  /*PyObject *lnotab*/
    );
    Py_DECREF(py_srcfile);
    #else
    py_code = PyCode_NewEmpty(filename, funcname, py_line);
    #endif
    Py_XDECREF(py_funcname);  // XDECREF since it's only set on Py3 if cline
    return py_code;
bad:
    Py_XDECREF(py_funcname);
    #if PY_MAJOR_VERSION < 3
    Py_XDECREF(py_srcfile);
    #endif
    return NULL;
}
static void __Pyx_AddTraceback(const char *funcname, int c_line,
                               int py_line, const char *filename) {
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    PyThreadState *tstate = __Pyx_PyThreadState_Current;
    PyObject *ptype, *pvalue, *ptraceback;
    if (c_line) {
        c_line = __Pyx_CLineForTraceback(tstate, c_line);
    }
    py_code = __pyx_find_code_object(c_line ? -c_line : py_line);
    if (!py_code) {
        __Pyx_ErrFetchInState(tstate, &ptype, &pvalue, &ptraceback);
        py_code = __Pyx_CreateCodeObjectForTraceback(
            funcname, c_line, py_line, filename);
        if (!py_code) {
            /* If the code object creation fails, then we should clear the
               fetched exception references and propagate the new exception */
            Py_XDECREF(ptype);
            Py_XDECREF(pvalue);
            Py_XDECREF(ptraceback);
            goto bad;
        }
        __Pyx_ErrRestoreInState(tstate, ptype, pvalue, ptraceback);
        __pyx_insert_code_object(c_line ? -c_line : py_line, py_code);
    }
    py_frame = PyFrame_New(
        tstate,            /*PyThreadState *tstate,*/
        py_code,           /*PyCodeObject *code,*/
        __pyx_d,    /*PyObject *globals,*/
        0                  /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    __Pyx_PyFrame_SetLineNumber(py_frame, py_line);
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}

/* CIntToPy */
static CYTHON_INLINE PyObject* __Pyx_PyInt_From_long(long value) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const long neg_one = (long) -1, const_zero = (long) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    if (is_unsigned) {
        if (sizeof(long) < sizeof(long)) {
            return PyInt_FromLong((long) value);
        } else if (sizeof(long) <= sizeof(unsigned long)) {
            return PyLong_FromUnsignedLong((unsigned long) value);
#ifdef HAVE_LONG_LONG
        } else if (sizeof(long) <= sizeof(unsigned PY_LONG_LONG)) {
            return PyLong_FromUnsignedLongLong((unsigned PY_LONG_LONG) value);
#endif
        }
    } else {
        if (sizeof(long) <= sizeof(long)) {
            return PyInt_FromLong((long) value);
#ifdef HAVE_LONG_LONG
        } else if (sizeof(long) <= sizeof(PY_LONG_LONG)) {
            return PyLong_FromLongLong((PY_LONG_LONG) value);
#endif
        }
    }
    {
        int one = 1; int little = (int)*(unsigned char *)&one;
        unsigned char *bytes = (unsigned char *)&value;
        return _PyLong_FromByteArray(bytes, sizeof(long),
                                     little, !is_unsigned);
    }
}

/* CIntFromPyVerify */
#define __PYX_VERIFY_RETURN_INT(target_type, func_type, func_value)\
    __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, 0)
#define __PYX_VERIFY_RETURN_INT_EXC(target_type, func_type, func_value)\
    __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, 1)
#define __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, exc)\
    {\
        func_type value = func_value;\
        if (sizeof(target_type) < sizeof(func_type)) {\
            if (unlikely(value != (func_type) (target_type) value)) {\
                func_type zero = 0;\
                if (exc && unlikely(value == (func_type)-1 && PyErr_Occurred()))\
                    return (target_type) -1;\
                if (is_unsigned && unlikely(value < zero))\
                    goto raise_neg_overflow;\
                else\
                    goto raise_overflow;\
            }\
        }\
        return (target_type) value;\
    }

/* CIntFromPy */
static CYTHON_INLINE long __Pyx_PyInt_As_long(PyObject *x) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const long neg_one = (long) -1, const_zero = (long) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
#if PY_MAJOR_VERSION < 3
    if (likely(PyInt_Check(x))) {
        if (sizeof(long) < sizeof(long)) {
            __PYX_VERIFY_RETURN_INT(long, long, PyInt_AS_LONG(x))
        } else {
            long val = PyInt_AS_LONG(x);
            if (is_unsigned && unlikely(val < 0)) {
                goto raise_neg_overflow;
            }
            return (long) val;
        }
    } else
#endif
    if (likely(PyLong_Check(x))) {
        if (is_unsigned) {
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return (long) 0;
                case  1: __PYX_VERIFY_RETURN_INT(long, digit, digits[0])
                case 2:
                    if (8 * sizeof(long) > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) >= 2 * PyLong_SHIFT) {
                            return (long) (((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
                case 3:
                    if (8 * sizeof(long) > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) >= 3 * PyLong_SHIFT) {
                            return (long) (((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
                case 4:
                    if (8 * sizeof(long) > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) >= 4 * PyLong_SHIFT) {
                            return (long) (((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
            }
#endif
#if CYTHON_COMPILING_IN_CPYTHON
            if (unlikely(Py_SIZE(x) < 0)) {
                goto raise_neg_overflow;
            }
#else
            {
                int result = PyObject_RichCompareBool(x, Py_False, Py_LT);
                if (unlikely(result < 0))
                    return (long) -1;
                if (unlikely(result == 1))
                    goto raise_neg_overflow;
            }
#endif
            if (sizeof(long) <= sizeof(unsigned long)) {
                __PYX_VERIFY_RETURN_INT_EXC(long, unsigned long, PyLong_AsUnsignedLong(x))
#ifdef HAVE_LONG_LONG
            } else if (sizeof(long) <= sizeof(unsigned PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC(long, unsigned PY_LONG_LONG, PyLong_AsUnsignedLongLong(x))
#endif
            }
        } else {
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return (long) 0;
                case -1: __PYX_VERIFY_RETURN_INT(long, sdigit, (sdigit) (-(sdigit)digits[0]))
                case  1: __PYX_VERIFY_RETURN_INT(long,  digit, +digits[0])
                case -2:
                    if (8 * sizeof(long) - 1 > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 2 * PyLong_SHIFT) {
                            return (long) (((long)-1)*(((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 2:
                    if (8 * sizeof(long) > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 2 * PyLong_SHIFT) {
                            return (long) ((((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case -3:
                    if (8 * sizeof(long) - 1 > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 3 * PyLong_SHIFT) {
                            return (long) (((long)-1)*(((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 3:
                    if (8 * sizeof(long) > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 3 * PyLong_SHIFT) {
                            return (long) ((((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case -4:
                    if (8 * sizeof(long) - 1 > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 4 * PyLong_SHIFT) {
                            return (long) (((long)-1)*(((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 4:
                    if (8 * sizeof(long) > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(long) - 1 > 4 * PyLong_SHIFT) {
                            return (long) ((((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
            }
#endif
            if (sizeof(long) <= sizeof(long)) {
                __PYX_VERIFY_RETURN_INT_EXC(long, long, PyLong_AsLong(x))
#ifdef HAVE_LONG_LONG
            } else if (sizeof(long) <= sizeof(PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC(long, PY_LONG_LONG, PyLong_AsLongLong(x))
#endif
            }
        }
        {
#if CYTHON_COMPILING_IN_PYPY && !defined(_PyLong_AsByteArray)
            PyErr_SetString(PyExc_RuntimeError,
                            "_PyLong_AsByteArray() not available in PyPy, cannot convert large numbers");
#else
            long val;
            PyObject *v = __Pyx_PyNumber_IntOrLong(x);
 #if PY_MAJOR_VERSION < 3
            if (likely(v) && !PyLong_Check(v)) {
                PyObject *tmp = v;
                v = PyNumber_Long(tmp);
                Py_DECREF(tmp);
            }
 #endif
            if (likely(v)) {
                int one = 1; int is_little = (int)*(unsigned char *)&one;
                unsigned char *bytes = (unsigned char *)&val;
                int ret = _PyLong_AsByteArray((PyLongObject *)v,
                                              bytes, sizeof(val),
                                              is_little, !is_unsigned);
                Py_DECREF(v);
                if (likely(!ret))
                    return val;
            }
#endif
            return (long) -1;
        }
    } else {
        long val;
        PyObject *tmp = __Pyx_PyNumber_IntOrLong(x);
        if (!tmp) return (long) -1;
        val = __Pyx_PyInt_As_long(tmp);
        Py_DECREF(tmp);
        return val;
    }
raise_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "value too large to convert to long");
    return (long) -1;
raise_neg_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "can't convert negative value to long");
    return (long) -1;
}

/* CIntFromPy */
static CYTHON_INLINE int __Pyx_PyInt_As_int(PyObject *x) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const int neg_one = (int) -1, const_zero = (int) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
#if PY_MAJOR_VERSION < 3
    if (likely(PyInt_Check(x))) {
        if (sizeof(int) < sizeof(long)) {
            __PYX_VERIFY_RETURN_INT(int, long, PyInt_AS_LONG(x))
        } else {
            long val = PyInt_AS_LONG(x);
            if (is_unsigned && unlikely(val < 0)) {
                goto raise_neg_overflow;
            }
            return (int) val;
        }
    } else
#endif
    if (likely(PyLong_Check(x))) {
        if (is_unsigned) {
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return (int) 0;
                case  1: __PYX_VERIFY_RETURN_INT(int, digit, digits[0])
                case 2:
                    if (8 * sizeof(int) > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) >= 2 * PyLong_SHIFT) {
                            return (int) (((((int)digits[1]) << PyLong_SHIFT) | (int)digits[0]));
                        }
                    }
                    break;
                case 3:
                    if (8 * sizeof(int) > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) >= 3 * PyLong_SHIFT) {
                            return (int) (((((((int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0]));
                        }
                    }
                    break;
                case 4:
                    if (8 * sizeof(int) > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) >= 4 * PyLong_SHIFT) {
                            return (int) (((((((((int)digits[3]) << PyLong_SHIFT) | (int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0]));
                        }
                    }
                    break;
            }
#endif
#if CYTHON_COMPILING_IN_CPYTHON
            if (unlikely(Py_SIZE(x) < 0)) {
                goto raise_neg_overflow;
            }
#else
            {
                int result = PyObject_RichCompareBool(x, Py_False, Py_LT);
                if (unlikely(result < 0))
                    return (int) -1;
                if (unlikely(result == 1))
                    goto raise_neg_overflow;
            }
#endif
            if (sizeof(int) <= sizeof(unsigned long)) {
                __PYX_VERIFY_RETURN_INT_EXC(int, unsigned long, PyLong_AsUnsignedLong(x))
#ifdef HAVE_LONG_LONG
            } else if (sizeof(int) <= sizeof(unsigned PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC(int, unsigned PY_LONG_LONG, PyLong_AsUnsignedLongLong(x))
#endif
            }
        } else {
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return (int) 0;
                case -1: __PYX_VERIFY_RETURN_INT(int, sdigit, (sdigit) (-(sdigit)digits[0]))
                case  1: __PYX_VERIFY_RETURN_INT(int,  digit, +digits[0])
                case -2:
                    if (8 * sizeof(int) - 1 > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, long, -(long) (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 2 * PyLong_SHIFT) {
                            return (int) (((int)-1)*(((((int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
                case 2:
                    if (8 * sizeof(int) > 1 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 2 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 2 * PyLong_SHIFT) {
                            return (int) ((((((int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
                case -3:
                    if (8 * sizeof(int) - 1 > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, long, -(long) (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 3 * PyLong_SHIFT) {
                            return (int) (((int)-1)*(((((((int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
                case 3:
                    if (8 * sizeof(int) > 2 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 3 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 3 * PyLong_SHIFT) {
                            return (int) ((((((((int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
                case -4:
                    if (8 * sizeof(int) - 1 > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, long, -(long) (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 4 * PyLong_SHIFT) {
                            return (int) (((int)-1)*(((((((((int)digits[3]) << PyLong_SHIFT) | (int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
                case 4:
                    if (8 * sizeof(int) > 3 * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > 4 * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT(int, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if (8 * sizeof(int) - 1 > 4 * PyLong_SHIFT) {
                            return (int) ((((((((((int)digits[3]) << PyLong_SHIFT) | (int)digits[2]) << PyLong_SHIFT) | (int)digits[1]) << PyLong_SHIFT) | (int)digits[0])));
                        }
                    }
                    break;
            }
#endif
            if (sizeof(int) <= sizeof(long)) {
                __PYX_VERIFY_RETURN_INT_EXC(int, long, PyLong_AsLong(x))
#ifdef HAVE_LONG_LONG
            } else if (sizeof(int) <= sizeof(PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC(int, PY_LONG_LONG, PyLong_AsLongLong(x))
#endif
            }
        }
        {
#if CYTHON_COMPILING_IN_PYPY && !defined(_PyLong_AsByteArray)
            PyErr_SetString(PyExc_RuntimeError,
                            "_PyLong_AsByteArray() not available in PyPy, cannot convert large numbers");
#else
            int val;
            PyObject *v = __Pyx_PyNumber_IntOrLong(x);
 #if PY_MAJOR_VERSION < 3
            if (likely(v) && !PyLong_Check(v)) {
                PyObject *tmp = v;
                v = PyNumber_Long(tmp);
                Py_DECREF(tmp);
            }
 #endif
            if (likely(v)) {
                int one = 1; int is_little = (int)*(unsigned char *)&one;
                unsigned char *bytes = (unsigned char *)&val;
                int ret = _PyLong_AsByteArray((PyLongObject *)v,
                                              bytes, sizeof(val),
                                              is_little, !is_unsigned);
                Py_DECREF(v);
                if (likely(!ret))
                    return val;
            }
#endif
            return (int) -1;
        }
    } else {
        int val;
        PyObject *tmp = __Pyx_PyNumber_IntOrLong(x);
        if (!tmp) return (int) -1;
        val = __Pyx_PyInt_As_int(tmp);
        Py_DECREF(tmp);
        return val;
    }
raise_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "value too large to convert to int");
    return (int) -1;
raise_neg_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "can't convert negative value to int");
    return (int) -1;
}

/* FastTypeChecks */
#if CYTHON_COMPILING_IN_CPYTHON
static int __Pyx_InBases(PyTypeObject *a, PyTypeObject *b) {
    while (a) {
        a = a->tp_base;
        if (a == b)
            return 1;
    }
    return b == &PyBaseObject_Type;
}
static CYTHON_INLINE int __Pyx_IsSubtype(PyTypeObject *a, PyTypeObject *b) {
    PyObject *mro;
    if (a == b) return 1;
    mro = a->tp_mro;
    if (likely(mro)) {
        Py_ssize_t i, n;
        n = PyTuple_GET_SIZE(mro);
        for (i = 0; i < n; i++) {
            if (PyTuple_GET_ITEM(mro, i) == (PyObject *)b)
                return 1;
        }
        return 0;
    }
    return __Pyx_InBases(a, b);
}
#if PY_MAJOR_VERSION == 2
static int __Pyx_inner_PyErr_GivenExceptionMatches2(PyObject *err, PyObject* exc_type1, PyObject* exc_type2) {
    PyObject *exception, *value, *tb;
    int res;
    __Pyx_PyThreadState_declare
    __Pyx_PyThreadState_assign
    __Pyx_ErrFetch(&exception, &value, &tb);
    res = exc_type1 ? PyObject_IsSubclass(err, exc_type1) : 0;
    if (unlikely(res == -1)) {
        PyErr_WriteUnraisable(err);
        res = 0;
    }
    if (!res) {
        res = PyObject_IsSubclass(err, exc_type2);
        if (unlikely(res == -1)) {
            PyErr_WriteUnraisable(err);
            res = 0;
        }
    }
    __Pyx_ErrRestore(exception, value, tb);
    return res;
}
#else
static CYTHON_INLINE int __Pyx_inner_PyErr_GivenExceptionMatches2(PyObject *err, PyObject* exc_type1, PyObject *exc_type2) {
    int res = exc_type1 ? __Pyx_IsSubtype((PyTypeObject*)err, (PyTypeObject*)exc_type1) : 0;
    if (!res) {
        res = __Pyx_IsSubtype((PyTypeObject*)err, (PyTypeObject*)exc_type2);
    }
    return res;
}
#endif
static int __Pyx_PyErr_GivenExceptionMatchesTuple(PyObject *exc_type, PyObject *tuple) {
    Py_ssize_t i, n;
    assert(PyExceptionClass_Check(exc_type));
    n = PyTuple_GET_SIZE(tuple);
#if PY_MAJOR_VERSION >= 3
    for (i=0; i<n; i++) {
        if (exc_type == PyTuple_GET_ITEM(tuple, i)) return 1;
    }
#endif
    for (i=0; i<n; i++) {
        PyObject *t = PyTuple_GET_ITEM(tuple, i);
        #if PY_MAJOR_VERSION < 3
        if (likely(exc_type == t)) return 1;
        #endif
        if (likely(PyExceptionClass_Check(t))) {
            if (__Pyx_inner_PyErr_GivenExceptionMatches2(exc_type, NULL, t)) return 1;
        } else {
        }
    }
    return 0;
}
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches(PyObject *err, PyObject* exc_type) {
    if (likely(err == exc_type)) return 1;
    if (likely(PyExceptionClass_Check(err))) {
        if (likely(PyExceptionClass_Check(exc_type))) {
            return __Pyx_inner_PyErr_GivenExceptionMatches2(err, NULL, exc_type);
        } else if (likely(PyTuple_Check(exc_type))) {
            return __Pyx_PyErr_GivenExceptionMatchesTuple(err, exc_type);
        } else {
        }
    }
    return PyErr_GivenExceptionMatches(err, exc_type);
}
static CYTHON_INLINE int __Pyx_PyErr_GivenExceptionMatches2(PyObject *err, PyObject *exc_type1, PyObject *exc_type2) {
    assert(PyExceptionClass_Check(exc_type1));
    assert(PyExceptionClass_Check(exc_type2));
    if (likely(err == exc_type1 || err == exc_type2)) return 1;
    if (likely(PyExceptionClass_Check(err))) {
        return __Pyx_inner_PyErr_GivenExceptionMatches2(err, exc_type1, exc_type2);
    }
    return (PyErr_GivenExceptionMatches(err, exc_type1) || PyErr_GivenExceptionMatches(err, exc_type2));
}
#endif

/* CheckBinaryVersion */
static int __Pyx_check_binary_version(void) {
    char ctversion[5];
    int same=1, i, found_dot;
    const char* rt_from_call = Py_GetVersion();
    PyOS_snprintf(ctversion, 5, "%d.%d", PY_MAJOR_VERSION, PY_MINOR_VERSION);
    found_dot = 0;
    for (i = 0; i < 4; i++) {
        if (!ctversion[i]) {
            same = (rt_from_call[i] < '0' || rt_from_call[i] > '9');
            break;
        }
        if (rt_from_call[i] != ctversion[i]) {
            same = 0;
            break;
        }
    }
    if (!same) {
        char rtversion[5] = {'\0'};
        char message[200];
        for (i=0; i<4; ++i) {
            if (rt_from_call[i] == '.') {
                if (found_dot) break;
                found_dot = 1;
            } else if (rt_from_call[i] < '0' || rt_from_call[i] > '9') {
                break;
            }
            rtversion[i] = rt_from_call[i];
        }
        PyOS_snprintf(message, sizeof(message),
                      "compiletime version %s of module '%.100s' "
                      "does not match runtime version %s",
                      ctversion, __Pyx_MODULE_NAME, rtversion);
        return PyErr_WarnEx(NULL, message, 1);
    }
    return 0;
}

/* InitStrings */
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        #if PY_MAJOR_VERSION < 3
        if (t->is_unicode) {
            *t->p = PyUnicode_DecodeUTF8(t->s, t->n - 1, NULL);
        } else if (t->intern) {
            *t->p = PyString_InternFromString(t->s);
        } else {
            *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        }
        #else
        if (t->is_unicode | t->is_str) {
            if (t->intern) {
                *t->p = PyUnicode_InternFromString(t->s);
            } else if (t->encoding) {
                *t->p = PyUnicode_Decode(t->s, t->n - 1, t->encoding, NULL);
            } else {
                *t->p = PyUnicode_FromStringAndSize(t->s, t->n - 1);
            }
        } else {
            *t->p = PyBytes_FromStringAndSize(t->s, t->n - 1);
        }
        #endif
        if (!*t->p)
            return -1;
        if (PyObject_Hash(*t->p) == -1)
            return -1;
        ++t;
    }
    return 0;
}

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_FromString(const char* c_str) {
    return __Pyx_PyUnicode_FromStringAndSize(c_str, (Py_ssize_t)strlen(c_str));
}
static CYTHON_INLINE const char* __Pyx_PyObject_AsString(PyObject* o) {
    Py_ssize_t ignore;
    return __Pyx_PyObject_AsStringAndSize(o, &ignore);
}
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII || __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT
#if !CYTHON_PEP393_ENABLED
static const char* __Pyx_PyUnicode_AsStringAndSize(PyObject* o, Py_ssize_t *length) {
    char* defenc_c;
    PyObject* defenc = _PyUnicode_AsDefaultEncodedString(o, NULL);
    if (!defenc) return NULL;
    defenc_c = PyBytes_AS_STRING(defenc);
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
    {
        char* end = defenc_c + PyBytes_GET_SIZE(defenc);
        char* c;
        for (c = defenc_c; c < end; c++) {
            if ((unsigned char) (*c) >= 128) {
                PyUnicode_AsASCIIString(o);
                return NULL;
            }
        }
    }
#endif
    *length = PyBytes_GET_SIZE(defenc);
    return defenc_c;
}
#else
static CYTHON_INLINE const char* __Pyx_PyUnicode_AsStringAndSize(PyObject* o, Py_ssize_t *length) {
    if (unlikely(__Pyx_PyUnicode_READY(o) == -1)) return NULL;
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
    if (likely(PyUnicode_IS_ASCII(o))) {
        *length = PyUnicode_GET_LENGTH(o);
        return PyUnicode_AsUTF8(o);
    } else {
        PyUnicode_AsASCIIString(o);
        return NULL;
    }
#else
    return PyUnicode_AsUTF8AndSize(o, length);
#endif
}
#endif
#endif
static CYTHON_INLINE const char* __Pyx_PyObject_AsStringAndSize(PyObject* o, Py_ssize_t *length) {
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII || __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT
    if (
#if PY_MAJOR_VERSION < 3 && __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
            __Pyx_sys_getdefaultencoding_not_ascii &&
#endif
            PyUnicode_Check(o)) {
        return __Pyx_PyUnicode_AsStringAndSize(o, length);
    } else
#endif
#if (!CYTHON_COMPILING_IN_PYPY) || (defined(PyByteArray_AS_STRING) && defined(PyByteArray_GET_SIZE))
    if (PyByteArray_Check(o)) {
        *length = PyByteArray_GET_SIZE(o);
        return PyByteArray_AS_STRING(o);
    } else
#endif
    {
        char* result;
        int r = PyBytes_AsStringAndSize(o, &result, length);
        if (unlikely(r < 0)) {
            return NULL;
        } else {
            return result;
        }
    }
}
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject* x) {
   int is_true = x == Py_True;
   if (is_true | (x == Py_False) | (x == Py_None)) return is_true;
   else return PyObject_IsTrue(x);
}
static CYTHON_INLINE int __Pyx_PyObject_IsTrueAndDecref(PyObject* x) {
    int retval;
    if (unlikely(!x)) return -1;
    retval = __Pyx_PyObject_IsTrue(x);
    Py_DECREF(x);
    return retval;
}
static PyObject* __Pyx_PyNumber_IntOrLongWrongResultType(PyObject* result, const char* type_name) {
#if PY_MAJOR_VERSION >= 3
    if (PyLong_Check(result)) {
        if (PyErr_WarnFormat(PyExc_DeprecationWarning, 1,
                "__int__ returned non-int (type %.200s).  "
                "The ability to return an instance of a strict subclass of int "
                "is deprecated, and may be removed in a future version of Python.",
                Py_TYPE(result)->tp_name)) {
            Py_DECREF(result);
            return NULL;
        }
        return result;
    }
#endif
    PyErr_Format(PyExc_TypeError,
                 "__%.4s__ returned non-%.4s (type %.200s)",
                 type_name, type_name, Py_TYPE(result)->tp_name);
    Py_DECREF(result);
    return NULL;
}
static CYTHON_INLINE PyObject* __Pyx_PyNumber_IntOrLong(PyObject* x) {
#if CYTHON_USE_TYPE_SLOTS
  PyNumberMethods *m;
#endif
  const char *name = NULL;
  PyObject *res = NULL;
#if PY_MAJOR_VERSION < 3
  if (likely(PyInt_Check(x) || PyLong_Check(x)))
#else
  if (likely(PyLong_Check(x)))
#endif
    return __Pyx_NewRef(x);
#if CYTHON_USE_TYPE_SLOTS
  m = Py_TYPE(x)->tp_as_number;
  #if PY_MAJOR_VERSION < 3
  if (m && m->nb_int) {
    name = "int";
    res = m->nb_int(x);
  }
  else if (m && m->nb_long) {
    name = "long";
    res = m->nb_long(x);
  }
  #else
  if (likely(m && m->nb_int)) {
    name = "int";
    res = m->nb_int(x);
  }
  #endif
#else
  if (!PyBytes_CheckExact(x) && !PyUnicode_CheckExact(x)) {
    res = PyNumber_Int(x);
  }
#endif
  if (likely(res)) {
#if PY_MAJOR_VERSION < 3
    if (unlikely(!PyInt_Check(res) && !PyLong_Check(res))) {
#else
    if (unlikely(!PyLong_CheckExact(res))) {
#endif
        return __Pyx_PyNumber_IntOrLongWrongResultType(res, name);
    }
  }
  else if (!PyErr_Occurred()) {
    PyErr_SetString(PyExc_TypeError,
                    "an integer is required");
  }
  return res;
}
static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject* b) {
  Py_ssize_t ival;
  PyObject *x;
#if PY_MAJOR_VERSION < 3
  if (likely(PyInt_CheckExact(b))) {
    if (sizeof(Py_ssize_t) >= sizeof(long))
        return PyInt_AS_LONG(b);
    else
        return PyInt_AsSsize_t(b);
  }
#endif
  if (likely(PyLong_CheckExact(b))) {
    #if CYTHON_USE_PYLONG_INTERNALS
    const digit* digits = ((PyLongObject*)b)->ob_digit;
    const Py_ssize_t size = Py_SIZE(b);
    if (likely(__Pyx_sst_abs(size) <= 1)) {
        ival = likely(size) ? digits[0] : 0;
        if (size == -1) ival = -ival;
        return ival;
    } else {
      switch (size) {
         case 2:
           if (8 * sizeof(Py_ssize_t) > 2 * PyLong_SHIFT) {
             return (Py_ssize_t) (((((size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
         case -2:
           if (8 * sizeof(Py_ssize_t) > 2 * PyLong_SHIFT) {
             return -(Py_ssize_t) (((((size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
         case 3:
           if (8 * sizeof(Py_ssize_t) > 3 * PyLong_SHIFT) {
             return (Py_ssize_t) (((((((size_t)digits[2]) << PyLong_SHIFT) | (size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
         case -3:
           if (8 * sizeof(Py_ssize_t) > 3 * PyLong_SHIFT) {
             return -(Py_ssize_t) (((((((size_t)digits[2]) << PyLong_SHIFT) | (size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
         case 4:
           if (8 * sizeof(Py_ssize_t) > 4 * PyLong_SHIFT) {
             return (Py_ssize_t) (((((((((size_t)digits[3]) << PyLong_SHIFT) | (size_t)digits[2]) << PyLong_SHIFT) | (size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
         case -4:
           if (8 * sizeof(Py_ssize_t) > 4 * PyLong_SHIFT) {
             return -(Py_ssize_t) (((((((((size_t)digits[3]) << PyLong_SHIFT) | (size_t)digits[2]) << PyLong_SHIFT) | (size_t)digits[1]) << PyLong_SHIFT) | (size_t)digits[0]));
           }
           break;
      }
    }
    #endif
    return PyLong_AsSsize_t(b);
  }
  x = PyNumber_Index(b);
  if (!x) return -1;
  ival = PyInt_AsSsize_t(x);
  Py_DECREF(x);
  return ival;
}
static CYTHON_INLINE Py_hash_t __Pyx_PyIndex_AsHash_t(PyObject* o) {
  if (sizeof(Py_hash_t) == sizeof(Py_ssize_t)) {
    return (Py_hash_t) __Pyx_PyIndex_AsSsize_t(o);
#if PY_MAJOR_VERSION < 3
  } else if (likely(PyInt_CheckExact(o))) {
    return PyInt_AS_LONG(o);
#endif
  } else {
    Py_ssize_t ival;
    PyObject *x;
    x = PyNumber_Index(o);
    if (!x) return -1;
    ival = PyInt_AsLong(x);
    Py_DECREF(x);
    return ival;
  }
}
static CYTHON_INLINE PyObject * __Pyx_PyBool_FromLong(long b) {
  return b ? __Pyx_NewRef(Py_True) : __Pyx_NewRef(Py_False);
}
static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t ival) {
    return PyInt_FromSize_t(ival);
}


#endif /* Py_PYTHON_H */
