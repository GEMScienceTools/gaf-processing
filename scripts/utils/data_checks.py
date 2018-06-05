import logging
import numpy as np
import pandas as pd

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
        sv = [float(sv) for v in sv]
        sv.append(np.mean(sv))

        return sort_triple(sv)


def check_int_value(val, accept_none=True):
    # allowable: 0, 1, 2 ?
    if pd.isnull(val) or val == '':
        return accept_none
        
    try:
        val_ = int(val)
        return (val_ in (1, 2))
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
            if not (0 <= float(val) <= 90):
                return False
    else:
        return True


def change_average_dip(val, replace_bad=False, bad_return_val=None):
    # return change_value(val, check_average_dip, replace_bad, bad_return_val)
    # need to think about defauts for this
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
            return (False, 'val0')
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
    pass


def check_dip_dir(val, accept_none=False):
    return check_dir_str(val, accept_none)

    
def change_dip_dir(val, **args):
    pass


def check_downthrown_side_id(val, accept_none=True):
    return check_dir_str(val, accept_none)


def change_downthrown_side_id(val, **args):
    pass


def check_downthrown_side_dir(val, accept_none=True):
    return check_downthrown_side_id(val, accept_none)


def change_downthrown_side_dir(val, accept_none=True):
    return change_downthrown_side_id(val, accept_none)


def check_epistemic_quality(val, accept_none=True):
    return check_int_value(val, accept_none)


def change_epistemic_quality(val, **args):
    pass


def check_exposure_quality(val, accept_none=True):
    return check_int_value(val, accept_none)


def check_fz_name(val, accept_none=True):
    return check_str(val, accept_none)


def check_geometry(val, accept_none=False):
    if pd.isnull(val) or val == '':
        return accept_none
    else:
        # at some point do some good geometry checking?
        return True


def check_is_active(val, accept_none=True):
    return check_int_value(val, accept_none)


def check_last_movement(val, accept_none=True):
    if pd.isnull(val) or val == '':
        return accept_none
    else:
        return True


def check_name(val, accept_none=True):
    return check_str(val, accept_none)


def check_net_slip_rate(val, accept_none=True):
    return check_triple(val, accept_none)


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

    if val in ['Reverse', 'Reverse-Dextral', 'Dextral-Reverse', 
               'Dextral', 'Dextral-Normal', 'Normal-Dextral', 
               'Normal', 'Normal-Sinistral', 'Sinistral-Normal',
               'Sinistral', 'Sinistral-Reverse', 'Reverse-Sinistral',
               'Subduction Thrust', 'Spreading Ridge', 'Anticline',
               'Syncline']:
        return True
    else:
        return False


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
    'downthrown_side_id' : check_downthrown_side_id,
    'epistemic_quality' : check_epistemic_quality,
    'exposure_quality' : check_exposure_quality,
    'fz_name' : check_fz_name,
    'geometry' : check_geometry,
    'is_active' : check_is_active,
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
    'catalog_name' : None,
    'dip_dir' : None,
    'downthrown_side_dir' : None,
    'downthrown_side_id' : None,
    'epistemic_quality' : None,
    'exposure_quality' : None,
    'fz_name' : None,
    'geometry' : None,
    'is_active' : None,
    'last_movement' : None,
    'name' : None,
    'net_slip_rate' : None,
    'notes' : None,
    'ogc_fid' : None,
    'reference' : None,
    'shortening_rate' : None,
    'slip_type' : None,
    'strike_slip_rate' : None,
    'vert_slip_rate' : None,
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


def change_value(val, check_func, replace_bad, bad_value):
    if not replace_bad:
        bad_return_val = val

    try:
        new_val = int(val)
        if check_func(new_val):
            return new_val, True
        else:
            return bad_return_val, False
    except:
        return bad_return_val, False


