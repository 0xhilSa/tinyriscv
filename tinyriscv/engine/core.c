#include <python3.10/Python.h>
#include <python3.10/methodobject.h>
#include <python3.10/pycapsule.h>
#include <python3.10/pyerrors.h>

size_t getsize(const char *fmt){
  if(fmt == NULL) return 0;
  switch(*fmt){
    case 'b': case 'B': return sizeof(char);
    case 'h': case 'H': return sizeof(short);
    case 'i': case 'I': return sizeof(int);
    default: return 0;
  }
}

void cpu_free(PyObject *pycapsule){
  void *ptr = PyCapsule_GetPointer(pycapsule, "array");
  if(ptr) free(ptr);
}

static inline void *fail_exit(void *buf){
  free(buf);
  return NULL;
}

void *__typecasting__(PyObject *pylist, Py_ssize_t length, const char *fmt){
  size_t size = getsize(fmt);
  if(size == 0){
    PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
    return NULL;
  }
  void *buf = malloc(size * length);
  for(Py_ssize_t i = 0; i < length; i++){
    PyObject *item = PyList_GetItem(pylist, i);
    void *dest = (char *)buf + i * size;
    switch(*fmt){
      case 'b': {
        char val = (char)PyLong_AsLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      case 'B': {
        unsigned char val = (unsigned char)PyLong_AsUnsignedLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      case 'h': {
        short val = (short)PyLong_AsLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      case 'H': {
        unsigned short val = (unsigned short)PyLong_AsUnsignedLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      case 'i': {
        int val = (int)PyLong_AsLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      case 'I': {
        unsigned int val = (unsigned int)PyLong_AsUnsignedLong(item);
        if(PyErr_Occurred()) return fail_exit(buf);
        memcpy(dest, &val, size);
        break;
      }
      default: {
        free(buf);
        PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
        return NULL;
      }
    }
  }
  return buf;
}

static PyObject *__list__(void *buf, Py_ssize_t length, const char *fmt){
  PyObject *pylist = PyList_New(length);
  for(Py_ssize_t i = 0; i < length; i++){
    PyObject *item = NULL;
    switch(*fmt){
      case 'b': item = PyLong_FromLong(((char*)buf)[i]); break;
      case 'B': item = PyLong_FromUnsignedLong(((unsigned char*)buf)[i]); break;
      case 'h': item = PyLong_FromUnsignedLong(((short*)buf)[i]); break;
      case 'H': item = PyLong_FromUnsignedLong(((unsigned short*)buf)[i]); break;
      case 'i': item = PyLong_FromLong(((int*)buf)[i]); break;
      case 'I': item = PyLong_FromUnsignedLong(((unsigned int*)buf)[i]); break;
    }
    if(!item){
      Py_DECREF(pylist);
      return NULL;
    }
    PyList_SET_ITEM(pylist, i, item);
  }
  return pylist;
}

static PyObject *tolist(PyObject *self, PyObject *args){
  PyObject *pycapsule;
  Py_ssize_t length;
  const char *fmt;
  if(!PyArg_ParseTuple(args, "Ons", &pycapsule, &length, &fmt)) return NULL;
  void *buf = PyCapsule_GetPointer(pycapsule, "array");
  if(!buf) return NULL;
  size_t size = getsize(fmt);
  if(size == 0){
    PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
    return NULL;
  }
  PyObject *list = __list__(buf, length, fmt);
  if(!list){
    PyErr_SetString(PyExc_RuntimeError, "Failed converting C array to list");
    return NULL;
  }
  return list;
}

static PyObject *array(PyObject *self, PyObject *args){
  PyObject *pylist;
  const char *fmt;
  if(!PyArg_ParseTuple(args, "Os", &pylist, &fmt)) return NULL;
  void *buf;
  Py_ssize_t length;
  if(PyList_Check(pylist)){
    length = PyList_Size(pylist);
    buf = __typecasting__(pylist, length, fmt);
  }else{
    PyErr_SetString(PyExc_TypeError, "1D array were expected");
  }
  return PyCapsule_New(buf, "array", cpu_free);
}

static PyObject *__sizeof__(PyObject *self, PyObject *args){
  Py_ssize_t length;
  const char *fmt;
  if(!PyArg_ParseTuple(args, "ns", &length, &fmt)) return NULL;
  size_t size = getsize(fmt);
  long tsize = size * length;
  return PyLong_FromLong(tsize);
}

static PyObject *__getitem__(PyObject *self, PyObject *args){
  PyObject *pycapsule;
  Py_ssize_t index, length;
  const char *fmt;
  if(!PyArg_ParseTuple(args, "Onns", &pycapsule, &index, &length, &fmt)) return NULL;
  if(!PyCapsule_CheckExact(pycapsule)){
    PyErr_SetString(PyExc_TypeError, "expected a capsule");
    return NULL;
  }
  void *buf = PyCapsule_GetPointer(pycapsule, "array");
  if(!buf) return NULL;
  size_t size = getsize(fmt);
  if(size == 0){
    PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
    return NULL;
  }
  if(index <= 0 || index >= length){
    PyErr_SetString(PyExc_IndexError, "Index out of range");
    return NULL;
  }
  void *src = (char *)buf + index * size;
  switch(*fmt){
    case 'b': return PyLong_FromLong(*(char*)src);
    case 'B': return PyLong_FromUnsignedLong(*(unsigned char*)src);
    case 'h': return PyLong_FromLong(*(short*)src);
    case 'H': return PyLong_FromUnsignedLong(*(unsigned short*)src);
    case 'i': return PyLong_FromLong(*(int*)src);
    case 'I': return PyLong_FromUnsignedLong(*(unsigned int*)src);
    default:
      PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
      return NULL;
  }
}

static PyObject *__setitem__(PyObject *self, PyObject *args){
  PyObject *pycapsule;
  PyObject *value;
  Py_ssize_t index, length;
  const char *fmt;
  if(!PyArg_ParseTuple(args, "OOnns", &pycapsule, &value, &index, &length, &fmt)) return NULL;
  if(!PyCapsule_CheckExact(pycapsule)){
    PyErr_SetString(PyExc_TypeError, "expected a pycapsule");
    return NULL;
  }
  void *buf = PyCapsule_GetPointer(pycapsule, "array");
  if(!buf) return NULL;
  size_t size = getsize(fmt);
  if(size == 0){
    PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
    return NULL;
  }
  if(index < 0 || index >= length){
    PyErr_Format(PyExc_IndexError, "Invalid index %zd", index);
    return NULL;
  }
  long val = PyLong_AsLong(value);
  if(PyErr_Occurred()) return NULL;
  void *dest = (char *)buf + index * size;
  switch(*fmt){
    case 'b': {
      char v = (char)val;
      memcpy(dest, &v, size);
      break;
    }
    case 'B': {
      unsigned char v = (unsigned char)val;
      memcpy(dest, &v, size);
      break;
    }
    case 'h': {
      short v = (short)val;
      memcpy(dest, &v, size);
      break;
    }
    case 'H': {
      unsigned short v = (unsigned short)val;
      memcpy(dest, &v, size);
      break;
    }
    case 'i': {
      int v = (int)val;
      memcpy(dest, &v, size);
      break;
    }
    case 'I': {
      unsigned int v = (unsigned int)val;
      memcpy(dest, &v, size);
      break;
    }
    default:
      PyErr_Format(PyExc_ValueError, "Invalid DType: %s", fmt);
      return NULL;
  }
  Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
  {"array", array, METH_VARARGS, "Create a C-allocated array from a Python list"},
  {"tolist", tolist, METH_VARARGS, "Convert a C array capsule back into a Python list"},
  {"sizeof", __sizeof__, METH_VARARGS, "Get the array size"},
  {"getitem", __getitem__, METH_VARARGS, "GetItem via index"},
  {"setitem", __setitem__, METH_VARARGS, "SetItem via index"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "core",
  NULL,
  -1,
  methods
};

PyMODINIT_FUNC PyInit_core(void){
  return PyModule_Create(&module);
}
