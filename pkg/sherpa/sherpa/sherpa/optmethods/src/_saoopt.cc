// 
//  Copyright (C) 2007  Smithsonian Astrophysical Observatory
//
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License along
//  with this program; if not, write to the Free Software Foundation, Inc.,
//  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//


//#include <stdexcept>

#include <sherpa/extension.hh>
#include <sherpa/functor.hh>

#include "DifEvo.hh"
#include "NelderMead.hh"

//#define haveClmdif 1

#ifdef haveClmdif
#include "minpack/levmar.hh"
static void lmdif_callback_func( int mfct, int npar, double* xpars,
				 double* fvec, int& ierr,
				 PyObject* py_fcn ) {


  DoubleArray pars_array;
  npy_intp dims[1];

  dims[0] = npar;
  if ( EXIT_SUCCESS != pars_array.create( 1, dims, xpars ) ) {
    ierr = EXIT_FAILURE;
    return;
  }

  PyObject* rv = PyObject_CallFunction( py_fcn, "N", pars_array.new_ref() );
  if ( NULL == rv ) {
    ierr = EXIT_FAILURE;
    return;
  }

  DoubleArray vals_array;
  int stat = vals_array.from_obj( rv );
  Py_DECREF( rv );
  if ( EXIT_SUCCESS != stat ) {
    ierr = EXIT_FAILURE;
    return;
  }

  if ( vals_array.get_size() != mfct ) {
    PyErr_SetString( PyExc_TypeError,
		     "callback function returned wrong number of values" );
    ierr = EXIT_FAILURE;
    return;
  }

  std::copy( &vals_array[0], &vals_array[0] + mfct, fvec );

  return;

}

//*****************************************************************************
//
// py_cpp_lmdif:  Python wrapper function for C++ function lmdif
//
//*****************************************************************************
template< typename Func >
static PyObject* py_cpp_lmdif( PyObject* self, PyObject* args, Func func ) {

  PyObject* py_function=NULL;
  DoubleArray par, lb, ub;
  int mfct, maxnfev, nfev, info, verbose;
  double fval, ftol, xtol, gtol, epsfcn, factor;

  if ( !PyArg_ParseTuple( args, (char*) "OiO&dddiddiO&O&",
			  &py_function,
			  &mfct,
			  CONVERTME(DoubleArray), &par,
			  &ftol, &xtol, &gtol, &maxnfev,
			  &epsfcn, &factor, &verbose,
			  CONVERTME(DoubleArray), &lb,
			  CONVERTME(DoubleArray), &ub ) ) {
    return NULL;
  }

  const int npar = par.get_size( );

  std::vector<double> covarerr( npar );

  if ( npar != lb.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(lb)=%d != len(par)=%d",
		  static_cast<int>( lb.get_size( ) ), npar);
    return NULL;
  }
    
  if ( npar != ub.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(ub)=%d != len(par)=%d",
		  static_cast<int>( ub.get_size( ) ), npar );
    return NULL;
  }

  try {

    minpack::LevMar< Func, PyObject* > levmar( npar, &par[0], &lb[0], &ub[0],
					       func, py_function, mfct );

    info = levmar( &par[0], ftol, xtol, gtol, maxnfev, epsfcn, factor,
		   verbose, nfev, fval, &covarerr[0] );

  } catch( sherpa::OptErr& oe ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError,
		       (char*) "The parameters are out of bounds\n" );
    return NULL;

  } catch( std::runtime_error& re ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*) re.what() );
    return NULL;
  } catch ( ... ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"Unknown exception caught" );
    return NULL;
  }

  if ( info < 0 ) {
    // Make sure an exception is set
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"function call failed" );
    return NULL;
  }

  std::copy( &covarerr[0], &covarerr[0] + npar, &lb[0] );

  return Py_BuildValue( (char*)"(NdiiN)", par.return_new_ref(), fval, nfev,
			info, lb.return_new_ref() );
}
static PyObject* py_lmdif( PyObject* self, PyObject* args ) {

  //
  // it looks like an extra indirection but fct_ptr does the nasty
  // work so I do not have to worry about the function prototype.
  //
  return py_cpp_lmdif( self, args, sherpa::fct_ptr( lmdif_callback_func ) );

}
//*****************************************************************************
//
// py_lmdif:  Python wrapper function for C++ function lmdif
//
//*****************************************************************************

//*****************************************************************************
//
// py_difevo_lm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************
template< typename Func >
static PyObject* py_difevo_levmar( PyObject* self, PyObject* args,
				   Func callback_func ) {

  PyObject* py_function=NULL;
  DoubleArray par, step, lb, ub;
  int verbose, maxnfev, seed, population_size, strategy, mfcts, nfev, err;
  double fval, tol, xprob, weighting_factor;

  if ( !PyArg_ParseTuple( args, (char*) "iiiiidddO&O&O&Oi",
			  &verbose,
			  &maxnfev,
			  &seed,
			  &population_size,
			  &strategy,
			  &tol,
			  &xprob,
			  &weighting_factor,
			  CONVERTME(DoubleArray), &lb,
			  CONVERTME(DoubleArray), &ub,
			  CONVERTME(DoubleArray), &par,
			  &py_function, &mfcts ) ) {
    return NULL;
  }

  const int npar = par.get_size( );

  if ( npar != lb.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(lb)=%d != len(par)=%d",
		  static_cast<int>( lb.get_size( ) ), npar);
    return NULL;
  }
    
  if ( npar != ub.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(ub)=%d != len(par)=%d",
		  static_cast<int>( ub.get_size( ) ), npar );
    return NULL;
  }

  if ( strategy < 0 || strategy > 9 ) {
    PyErr_Format( PyExc_ValueError, (char*) "strategy(%d) must be within [0,9]",
		  strategy );
    return NULL;
  }

  try {

    sherpa::DifEvo< Func, PyObject*, minpack::LevMar< Func, PyObject* > >
      difevo( npar, &par[0], &lb[0], &ub[0], callback_func, py_function,
	      xprob, weighting_factor, strategy, seed, mfcts );

    err =
      difevo( &par[0], verbose, maxnfev, tol, population_size, nfev, fval );

  } catch( sherpa::OptErr& oe ) {

    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError,
		       (char*) "The parameters are out of bounds\n" );
    return NULL;

  } catch( std::runtime_error& re ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*) re.what() );
    return NULL;
  } catch ( ... ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"Unknown exception caught" );
    return NULL;
  }


  if ( err < 0 ) {
    // Make sure an exception is set
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"function call failed" );
    return NULL;
  }

  return Py_BuildValue( (char*)"(Ndii)", par.return_new_ref(), fval, nfev,
			err );
}
static PyObject* py_difevo_lm( PyObject* self, PyObject* args ) {

  //
  // it looks like an extra indirection but fct_ptr does the nasty
  // work so I do not have to worry about the function prototype.
  //
  return py_difevo_levmar( self, args, 
			   sherpa::fct_ptr( lmdif_callback_func ) );

}
//*****************************************************************************
//
// py_difevo_lm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************


#else
static PyObject* py_lmdif( PyObject* self, PyObject* args ) {
  return NULL;
}
static PyObject* py_difevo_lm( PyObject* self, PyObject* args ) {
  return NULL;
}
#endif



static void sao_callback_func( int npar, double* xpars, double& fval,
			       int& ierr, PyObject* py_function ) {

  DoubleArray py_xpars;
  npy_intp dim[1];

  dim[0] = npar;
  if ( EXIT_SUCCESS != py_xpars.create( 1, dim, xpars ) ) {
    ierr = EXIT_FAILURE;
    return;
  }

  PyObject* return_val = PyObject_CallFunction( py_function, (char*)"O",
						py_xpars.borrowed_ref() );

  if ( NULL == return_val || Py_None == return_val ) {
    ierr = EXIT_FAILURE;
    return;
  }
  if ( !PyFloat_Check( return_val ) ) {
      PyErr_SetString( PyExc_TypeError,
		       (char*)"callback did not return a float" );
      Py_DECREF( return_val );
      ierr = -1;
      return;
  }

  fval = PyFloat_AsDouble( return_val );

  Py_DECREF( return_val );

}

//*****************************************************************************
//
// py_difevo_nm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************
template< typename Func >
static PyObject* py_difevo_neldermead( PyObject* self, PyObject* args, 
				       Func func ) {

  PyObject* py_function=NULL;
  DoubleArray par, step, lb, ub;
  int verbose, maxnfev, seed, population_size, strategy, nfev, err;
  double fval, tol, xprob, weighting_factor;

  if ( !PyArg_ParseTuple( args, (char*) "iiiiidddO&O&O&O",
			  &verbose,
			  &maxnfev,
			  &seed,
			  &population_size,
			  &strategy,
			  &tol,
			  &xprob,
			  &weighting_factor,
			  CONVERTME(DoubleArray), &lb,
			  CONVERTME(DoubleArray), &ub,
			  CONVERTME(DoubleArray), &par,
			  &py_function ) ) {
    return NULL;
  }

  const int npar = par.get_size( );

  if ( npar != lb.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(lb)=%d != len(par)=%d",
		  static_cast<int>( lb.get_size( ) ), npar);
    return NULL;
  }
    
  if ( npar != ub.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(ub)=%d != len(par)=%d",
		  static_cast<int>( ub.get_size( ) ), npar );
    return NULL;
  }

  if ( strategy < 0 || strategy > 9 ) {
    PyErr_Format( PyExc_ValueError, (char*) "strategy(%d) must be within [0,9]",
		  strategy );
    return NULL;
  }

  try {

    sherpa::DifEvo< Func, PyObject*, sherpa::NelderMead< Func, PyObject* > >
      difevo( npar, &par[0], &lb[0], &ub[0], func, py_function,
	      xprob, weighting_factor, strategy, seed );

    err =
      difevo( &par[0], verbose, maxnfev, tol, population_size, nfev, fval );

  } catch( sherpa::OptErr& oe ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError,
		       (char*) "The parameters are out of bounds\n" );
    return NULL;

  } catch( std::runtime_error& re ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*) re.what() );
    return NULL;
  } catch ( ... ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"Unknown exception caught" );
    return NULL;
  }


  if ( err < 0 ) {
    // Make sure an exception is set
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"function call failed" );
    return NULL;
  }

  return Py_BuildValue( (char*)"(Ndii)", par.return_new_ref(), fval, nfev,
			err );
}
static PyObject* py_difevo_nm( PyObject* self, PyObject* args ) {

  //
  // it looks like an extra indirection but fct_ptr does the nasty
  // work so I do not have to worry about the function prototype.
  //
  return py_difevo_neldermead( self, args, 
			       sherpa::fct_ptr( sao_callback_func ) );

}
//*****************************************************************************
//
// py_difevo_nm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************

//*****************************************************************************
//
// py_difevo_nm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************
template< typename Func >
static PyObject* py_difevo( PyObject* self, PyObject* args, Func func ) {

  PyObject* py_function=NULL;
  DoubleArray par, step, lb, ub;
  int verbose, maxnfev, seed, population_size, strategy, nfev, err;
  double fval, tol, xprob, weighting_factor;

  if ( !PyArg_ParseTuple( args, (char*) "iiiiidddO&O&O&O",
			  &verbose,
			  &maxnfev,
			  &seed,
			  &population_size,
			  &strategy,
			  &tol,
			  &xprob,
			  &weighting_factor,
			  CONVERTME(DoubleArray), &lb,
			  CONVERTME(DoubleArray), &ub,
			  CONVERTME(DoubleArray), &par,
			  &py_function ) ) {
    return NULL;
  }

  const int npar = par.get_size( );

  if ( npar != lb.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(lb)=%d != len(par)=%d",
		  static_cast<int>( lb.get_size( ) ), npar);
    return NULL;
  }
    
  if ( npar != ub.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*) "len(ub)=%d != len(par)=%d",
		  static_cast<int>( ub.get_size( ) ), npar );
    return NULL;
  }

  if ( strategy < 0 || strategy > 9 ) {
    PyErr_Format( PyExc_ValueError, (char*) "strategy(%d) must be within [0,9]",
		  strategy );
    return NULL;
  }

  try {

    sherpa::DifEvo< Func, PyObject*, sherpa::OptFunc< Func, PyObject* > >
      difevo( npar, &par[0], &lb[0], &ub[0], func, py_function,
	      xprob, weighting_factor, strategy, seed );

    err =
      difevo( &par[0], verbose, maxnfev, tol, population_size, nfev, fval );

  } catch( sherpa::OptErr& oe ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError,
		       (char*) "The parameters are out of bounds\n" );
    return NULL;

  } catch( std::runtime_error& re ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*) re.what() );
    return NULL;
  } catch ( ... ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"Unknown exception caught" );
    return NULL;
  }


  if ( err < 0 ) {
    // Make sure an exception is set
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"function call failed" );
    return NULL;
  }

  return Py_BuildValue( (char*)"(Ndii)", par.return_new_ref(), fval, nfev,
			err );
}
static PyObject* py_difevo( PyObject* self, PyObject* args ) {

  //
  // it looks like an extra indirection but fct_ptr does the nasty
  // work so I do not have to worry about the function prototype.
  //
  return py_difevo( self, args, sherpa::fct_ptr( sao_callback_func ) );

}
//*****************************************************************************
//
// py_difevo_nm:  Python wrapper function for C++ function difevo
//
//*****************************************************************************



//*****************************************************************************
//
// py_nm: Python wrapper function for C++ function neldermead
//
//*****************************************************************************
template< typename Func >
static PyObject* py_neldermead( PyObject* self, PyObject* args,
				Func callback_func ) {

  PyObject* py_function=NULL;
  DoubleArray par, step, lb, ub;
  IntArray finalsimplex;
  int verbose, maxnfev, nfev, initsimplex, err_status;
  double fval, tol;

  if ( !PyArg_ParseTuple( args, (char*) "iiiO&dO&O&O&O&O",
			  &verbose,
			  &maxnfev,
			  &initsimplex,
			  CONVERTME(IntArray), &finalsimplex,
			  &tol,
			  CONVERTME(DoubleArray), &step,
			  CONVERTME(DoubleArray), &lb,
			  CONVERTME(DoubleArray), &ub,
			  CONVERTME(DoubleArray), &par,
			  &py_function ) ) {
    return NULL;
  }

  const int npar = par.get_size( );

  if ( npar != step.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*)"len(step)=%d != len(par)=%d",
		  static_cast<int>( step.get_size( ) ), npar );
    return NULL;
  }

  if ( npar != lb.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*)"len(lb)=%d != len(par)=%d",
		  static_cast<int>( lb.get_size( ) ), npar);
    return NULL;
  }
    
  if ( npar != ub.get_size( ) ) {
    PyErr_Format( PyExc_ValueError, (char*)"len(ub)=%d != len(par)=%d",
		  static_cast<int>( ub.get_size( ) ), npar );
    return NULL;
  }

  try {

    sherpa::NelderMead< Func, PyObject* >
      nm( npar, &par[0], &lb[0], &ub[0], callback_func, py_function );

    std::vector< int > myfinalsimplex( &finalsimplex[0],
				       &finalsimplex[0] + 
				       finalsimplex.get_size( ) );

    err_status = nm( &par[0], verbose, initsimplex, myfinalsimplex, tol,
		     &step[0], maxnfev, nfev, fval );

  } catch( sherpa::OptErr& oe ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError,
		       (char*) "The parameters are out of bounds\n" );
    return NULL;

  } catch( std::runtime_error& re ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*) re.what() );
    return NULL;
  } catch ( ... ) {
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"Unknown exception caught" );
    return NULL;
  }


  if ( err_status < 0 ) {
    // Make sure an exception is set
    if ( NULL == PyErr_Occurred() )
      PyErr_SetString( PyExc_RuntimeError, (char*)"function call failed" );
    return NULL;
  }

  return Py_BuildValue( (char*)"(Ndii)", par.return_new_ref(), fval, nfev,
			err_status );

}
static PyObject* py_nm( PyObject* self, PyObject* args ) {

  //
  // it looks like an extra indirection but fct_ptr does the nasty
  // work so I do not have to worry about the function prototype.
  //
  return py_neldermead( self, args, sherpa::fct_ptr( sao_callback_func ) );

}
//*****************************************************************************
//
// py_nm: Python wrapper function for C++ function neldermead
//
//*****************************************************************************



//*****************************************************************************
//
// Module initialization
//
//*****************************************************************************
static PyMethodDef WrapperFcts[] = {


  FCTSPEC(difevo, py_difevo),
  FCTSPEC(nm_difevo, py_difevo_nm),
  FCTSPEC(lm_difevo, py_difevo_lm),               // not for public consumption
  FCTSPEC(clmdif, py_lmdif),                      // not for public consumption
  FCTSPEC(neldermead, py_nm),
  { NULL, NULL, 0, NULL }

};
SHERPAMOD(_saoopt, WrapperFcts)
//*****************************************************************************
//
// Module initialization
//
//*****************************************************************************
