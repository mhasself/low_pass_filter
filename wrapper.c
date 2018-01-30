/* -*- mode: C; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-
 *      vim: sw=4 ts=4 et tw=80
 */

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#include <assert.h>

/* Custom includes... */
#include "lo_pass.h"

PyDoc_STRVAR(contract__doc,
             "contract(v, M, w)\n"
             "\n"
             "Compute dot(v, dot(m, w))\n"
             "\n"
             "v and w are 1-d C-ordered numpy arrays.\n"
             "M is a 2-d C-ordered numpy array, with dimensions matching v and w.\n"
             "\n"
             "All arrays must have dtype='float64'\n"
    );




static PyObject *apply_filter(PyObject *self, PyObject *args) {
    PyArrayObject *i_array;
    PyArrayObject *o_array;
    int mode;
    if (!PyArg_ParseTuple(args, "O!O!i",
                          &PyArray_Type, &i_array,
                          &PyArray_Type, &o_array,
                          &mode)) {
        printf("contract: bad input arguments.\n");
        Py_RETURN_NONE;
    }

    // Check ordering
    assert(PyArray_FLAGS(i_array) & NPY_ARRAY_CARRAY);
    assert(PyArray_FLAGS(o_array) & NPY_ARRAY_CARRAY);
    
    // Check dimensionality
    assert(PyArray_NDIM(i_array)==2);
    assert(PyArray_NDIM(o_array)==2);

    // Check size
    int n_chan = PyArray_DIMS(i_array)[0];
    int n_samp = PyArray_DIMS(i_array)[1];
    assert(PyArray_DIMS(o_array)[0] == n_chan);
    assert(PyArray_DIMS(o_array)[1] == n_samp);

    // And types.
    assert(PyArray_TYPE(i_array) == NPY_INT32);
    assert(PyArray_TYPE(o_array) == NPY_INT32);

    // Ok I'm convinced.
    int32_t *buf0 = PyArray_DATA(i_array);
    int32_t *buf1 = PyArray_DATA(o_array);
    
    static int32_t *temp = NULL;
    static filtpar *pars = NULL;
    static filtbank banks[2];
    if (pars == NULL) {
        pars = mce_filter();
        filtbank *bank;
        bank = create_filtbank(n_chan, pars+0);
        memcpy(&banks[0], bank, sizeof(*bank));
        bank = create_filtbank(n_chan, pars+0);
        memcpy(&banks[1], bank, sizeof(*bank));
        temp = malloc(n_chan*n_samp * sizeof(int32_t));
    }

    if (mode == 0) {
        //int32_t *temp = malloc(n_chan*n_samp * sizeof(int32_t));
        filter_data(banks+0, buf0, temp, n_samp);
        filter_data(banks+1, temp, buf1, n_samp);
        //free(buf1);
    } else {
        multi_filter_data(banks, 2, buf0, buf1, n_samp);
    }
        
    return Py_None;
}


static PyMethodDef helpersMethods[] = {
    {"apply_filter", apply_filter, METH_VARARGS,
     contract__doc},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initnpfilt(void)
{
    Py_InitModule("npfilt", helpersMethods);
    import_array();
}
