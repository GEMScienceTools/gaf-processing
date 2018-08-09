import logging
import numpy as np
import pandas as pd

import geopandas as gpd

""" value checkers and changers """


##########
# triples
##########

def triple_to_vals(tup):
    tup = tup.replace('(','').replace(')','')
    vals = tup.split(',')
    return vals


def check_triple_to_float(val):
    trip_vals = triple_to_vals(val)

    if len(trip_vals) > 3:
        return False

    try:
        float(trip_vals[0])
        first = True
    except:
        first = False

    try:
        if trip_vals[1] != '':
            try:
                float(trip_vals[1])
                second = True
            except:
                second = False
            try:
                float(trip_vals[2])
                third = True
            except:
                third = False
        else:
            second = True
            third = True

        return (first and second and third)
    except:
        return False


def check_triple_sort(val):
    # should be done after check_triple_to_float
    trip_vals = triple_to_vals(val)
    if trip_vals[1] == '':
        return True
    else:
        floats = [float(tv) for tv in trip_vals]
        return (floats[1] <= floats[0] <= floats[2])


def sort_triple(val):
    trip_vals = triple_to_vals(val)
    sort_vals = sorted(trip_vals)

    return (sort_vals[1], sort_vals[0], sort_vals[2])


def check_triple(val, accept_none=False):
    if pd.isnull(val) or val == '':
        return accept_none

    try:
        vals = triple_to_vals(val)
    except:
        return False

    if not check_triple_to_float(val):
        return False
    if not check_triple_sort(val):
        return False

    return True


def change_triple_sort(bad_trip):
    if isinstance(bad_trip, str):
        trip_vals = triple_to_vals(bad_trip)
        sv = sorted(v for v in trip_vals if v is not '')
    else:
        sv = sorted(bad_trip)

    if len(sv) == 1:
        return '({},,)'.format(sv[0])
    elif len(sv) == 2:
        sv = [float(v) for v in sv]
        sv.append(np.mean(sv))
        sv_str = '({},{}.,{}'.format(*sv)
        return sort_triple(sv_str)


def check_int_value(val, accept_none=True):
    # allowable: 0, 1, 2 ?
    if pd.isnull(val) or val == '':
        return accept_none
        
    try:
        val_ = int(val)
        return (val_ in (1, 2, 3))
    except:
        return False

  
def change_int_value(val, replace_bad=True, bad_value=None):
    return change_value(val, check_int_value, replace_bad, bad_value)


def check_dir_str(val, accept_none=False):
    if pd.isnull or val == '':
        return accept_none
    else:
        return (val in ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'))


def check_str(val, accept_none=False):
    if pd.isnull or val == '':
        return accept_none
    else:
        if isinstance(val, str):
            return True


def check_accuracy_value(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none
    try:
        val_ = int(val)
        return (val_ > 0)
    except:
       return False

  
def change_accuracy_value(val, replace_bad=True, bad_value=None):
    return change_value(val, check_accuracy_value, replace_bad, bad_value)


def check_activity_confidence(val, accept_none=True):
    return check_int_value(val, accept_none=accept_none)


def change_activity_confidence(val, replace_bad=False, bad_return_val=None):
    return change_int_value(val, replace_bad=replace_bad,
                            bad_return_val=bad_return_val)


def check_average_dip(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none

    elif not check_triple(val, accept_none):
        return False

    vals = triple_to_vals(val)
    return check_dip_magnitudes(vals)


def check_dip_magnitudes(vals):
    for val in vals:
        if val != '':
            try:
                if not (0 <= float(val) <= 90):
                    return False
            except ValueError:
                return False
    else:
        return True


def change_average_dip(val, replace_bad=False, bad_return_val=None):
    # should remove replace_bad and bad_return_val from function call chain
    if not check_dip_magnitudes(triple_to_vals(val)):
        success = False
        return val, success

    try:
        good_val = change_triple_sort(val)
        success = True
        return good_val, success
    except:
        success = False
        return val, success


def check_average_rake(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none
    
    elif not check_triple(val, accept_none):
        return False

    vals = triple_to_vals(val)
    
    try:
        if not (-180 <= float(vals[0]) <= 180):
            return (False, 'val0') # what is this shit??
    except:
        return (False, 'val0_comp')
    
    if vals[1] != '':
        if not (-180 <= float(vals[1]) <= 180):
            return (False, 'val1')
        if not (-180 <= float(vals[2]) <= 180):
            return (False, 'val2')

    return True


def rake_to_aki_richards(rake):
    while rake >= 180:
        rake -= 360

    while rake <= -180:
        rake += 360

    return rake


def change_average_rake(val, replace_bad=False, bad_return_val=None):
    # return change_value(val, check_average_rake, replace_bad, bad_return_val)
    # need to think about defauts for this
    try:
        vals = triple_to_vals(val)
        for val in vals:
            if val is not '':
                val = str(rake_to_aki_richards(float(val)))
        good_val = change_triple_sort(vals)
        success = True
        return good_val, success

    except Exception as e:
        logging.info(e)
        return val, False


def check_catalog_name(val, accept_none=True):
    return check_str(val, accept_none)

def change_catalog_name(val, **args):
    return val, False


def check_dip_dir(val, accept_none=False):
    # could check w/ strike, kinematics?
    return check_dir_str(val, accept_none)

    
def change_dip_dir(val, **args):
    return val, False


def check_downthrown_side_dir(val, accept_none=True):
    return check_dir_str(val, accept_none)


def change_downthrown_side_dir(val, **args):
    return val, False


def check_epistemic_quality(val, accept_none=True):
    return check_int_value(val, accept_none)


def change_epistemic_quality(val, **args):
    return val, False


def check_exposure_quality(val, accept_none=True):
    return check_int_value(val, accept_none)


def change_exposure_quality(val, **args):
    return val, False


def check_fz_name(val, accept_none=True):
    return check_str(val, accept_none)


def change_fz_name(val):
    return val, False


def check_geometry(val, accept_none=False):
    if pd.isnull(val) or val == '':
        return accept_none
    else:
        # at some point do some good geometry checking?
        return True


def check_activity_confidence(val, accept_none=True):
    return check_int_value(val, accept_none)


def change_activity_confidence(val):
    return val, False


def check_last_movement(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none
    else:
        return True


def check_name(val, accept_none=True):
    return check_str(val, accept_none)


def check_net_slip_rate(val, accept_none=True):
    return check_triple(val, accept_none)


def change_slip_rate(val, accept_none=True):
    """
    only one function for all slip rates
    """
    # add value sanity checks?  What is appropriate?
    try:
        good_val = str(change_triple_sort(val))
        success = True
        return good_val, success
    except:
        success = False
        return val, success

def check_notes(val, accept_none=True):
    return check_str(val, accept_none)


def check_ogc_fid(val, accept_none=True):
    # is this the catalog ID or final ID?
    if pd.isnull(val) or val == '':
        return accept_none

    else:
        try:
            val_ = int(val)
            if val_ < 0:
                return False
        except:
            return False

        return True


def check_reference(val, accept_none=True):
    return check_str(val, accept_none)


def check_shortening_rate(val, accept_none=True):
    return check_triple(val, accept_none)


def check_slip_type(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none

    if val in slip_types:
        return True
    else:
        return False


slip_types = ['Reverse', 'Reverse-Dextral', 'Dextral-Reverse', 'Dextral',
              'Dextral-Normal', 'Normal-Dextral', 'Normal', 'Normal-Sinistral',
              'Sinistral-Normal', 'Sinistral', 'Sinistral-Reverse',
              'Reverse-Sinistral', 'Subduction Thrust', 'Spreading Ridge',
              'Strike-Slip', 'Reverse-Strike-Slip', 'Normal-Strike-Slip',
              'Anticline', 'Syncline']


def change_slip_type(val, min_distance=3):

    if val in ['thrust', 'Thrust']:
        success = True
        return 'Reverse', success

    else:
        edit_dists = {st: edit_distance(val, st) for st in slip_types}
        keepers = {k:v for k, v in edit_dists.items() if v <= min_distance}

        if keepers == {}:
            success = False
            return val, success
        else:
            good_val = min(keepers, key=keepers.get)
            success = True
            return good_val, success


def edit_distance(s, t):
# A fast and memory efficient implementation
# by Hjelmqvist, Sten

    # degenerate cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)
  
    # create two work vectors of integer distances
    #int[] v0 = new int[t.Length + 1];
    #int[] v1 = new int[t.Length + 1];
    v0 = []
    v1 = []
  
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    # for (int i = 0; i < v0.Length; i++)
    # v0[i] = i;
    for i in range(len(t)+1):
        v0.append(i)
        v1.append(0)
 
    for i in range(len(s)): 
        # calculate v1 (current row distances) from the previous row v0
        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1
  
        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1;
            v1[j + 1] = min(v1[j]+1, v0[j+1]+1, v0[j]+cost)
  
        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(t)+1):
            v0[j] = v1[j]
  
    return v1[len(t)]


def check_strike_slip_rate(val, accept_none=True):
    return check_triple(val, accept_none)


def check_vert_slip_rate(val, accept_none=True):
    return check_triple(val, accept_none)


check_val_funcs = {
    'accuracy' : check_accuracy_value,
    'activity_confidence' : check_activity_confidence,
    'average_dip' : check_average_dip,
    'average_rake' : check_average_rake,
    'catalog_name' : check_catalog_name,
    'dip_dir' : check_dip_dir,
    'downthrown_side_dir' : check_downthrown_side_dir,
#    'downthrown_side_id' : check_downthrown_side_id,
    'epistemic_quality' : check_epistemic_quality,
    'exposure_quality' : check_exposure_quality,
    'fz_name' : check_fz_name,
    'geometry' : check_geometry,
    'activity_confidence' : check_activity_confidence,
    'last_movement' : check_last_movement,
    'name' : check_name,
    'net_slip_rate' : check_net_slip_rate,
    'notes' : check_notes,
#    'ogc_fid' : check_ogc_fid,
    'reference' : check_reference,
    'shortening_rate' : check_shortening_rate,
    'slip_type' : check_slip_type,
    'strike_slip_rate' : check_strike_slip_rate,
    'vert_slip_rate' : check_vert_slip_rate,
    }

change_val_funcs = {
    'accuracy' : change_accuracy_value,
    'activity_confidence' : change_activity_confidence,
    'average_dip' : change_average_dip,
    'average_rake' : change_average_rake,
    'catalog_name' : change_catalog_name,
    'dip_dir' : change_dip_dir,
    'downthrown_side_dir' : change_downthrown_side_dir,
    'epistemic_quality' : change_epistemic_quality,
    'exposure_quality' : change_exposure_quality,
    'fz_name' : change_fz_name,
    'geometry' : None,
    'activity_confidence' : change_activity_confidence,
    'last_movement' : None,
    'name' : None,
    'net_slip_rate' : change_slip_rate,
    'notes' : None,
    'ogc_fid' : None,
    'reference' : None,
    'shortening_rate' : change_slip_rate,
    'slip_type' : change_slip_type,
    'strike_slip_rate' : change_slip_rate,
    'vert_slip_rate' : change_slip_rate,
    }


def check_value(row, idx, column, accept_none=True, change_val=False,
                report=True, _cat=False):
    """
    docs
    """

    val = row[column]
    catalog_name = row['catalog_name']

    if check_val_funcs[column](val, accept_none):
        pass  # value checked out

    else:
        if change_val:
            new_val, success = change_val_funcs[column](val)
            action = 'fixed' if success else "couldn't fix"
        else:
            action = 'skipping'

        if report:
            log = 'Bad value: `{val}` in {col} at index {ind} ({cat})...{act}'.format(
                **{'val': val, 'col': column, 'ind': idx, 'act': action,
                   'cat': catalog_name})
            if action == 'fixed':
                #logging.info(log)
                pass
            elif action in ["skipping", "couldn't fix"]:
                logging.info(log)

        if action == 'fixed':
            return (idx, new_val) # do I want to do this here?


def change_value(val, check_func, replace_bad, bad_return_val):
    if replace_bad is False:
        bad_return_val = val

    try:
        new_val = int(val)
        if check_func(new_val):
            return new_val, True
        else:
            return bad_return_val, False
    except:

        return bad_return_val, False


    
def check_data(mdf):
   

    for column in check_val_funcs.keys():
        print('checking {}'.format(column))
        logging.info('checking {}'.format(column))
        check_results = [check_value(row, idx, column, change_val=True)
                         for idx, row in mdf.iterrows()]
        changes = []
        change_idxs = []
        for cr in check_results:
            if cr is not None:
                if cr[1] is not None:
                    change_idxs.append(cr[0])
                    changes.append(cr[1])
    
        mdf.at[change_idxs, column] = changes

    return mdf



