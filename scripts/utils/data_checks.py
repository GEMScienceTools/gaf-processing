import numpy as np

col_dict = {'accuracy' : ,
            'activity_confidence' : ,
            'average_dip' : ,
            'average_rake' : ,
            'catalog_name' : ,
            'dip_dir' : ,
            'downthrown_side_dir' : ,
            'downthrown_side_id' : ,
            'epistemic_quality' : ,
            'exposure_quality' : ,
            'fz_name' : ,
            'geometry' : ,
            'is_active' : ,
            'last_movement' : ,
            'name' : ,
            'net_slip_rate' : ,
            'notes' : ,
            'ogc_fid' : ,
            'reference' : ,
            'shortening_rate' : ,
            'slip_type' : ,
            'strike_slip_rate' : ,
            'vert_slip_rate' : ,
            }


def accuracy(val, idx=None, accept_none=False, change_val=False):
    
    if not _check_accuracy(val):
        pass
    pass
        


def _check_accuracy(val):
    return isinstance(val, int)
  


