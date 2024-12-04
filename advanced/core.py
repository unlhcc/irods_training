import exifread

import python_storage_balancing
import session_vars

from genquery import *

#def pep_resource_resolve_hierarchy_pre(rule_args, callback, rei):
#    return python_storage_balancing.pep_resource_resolve_hierarchy_pre(rule_args, callback, rei)

def pep_api_data_obj_put_post(rule_args, callback, rei):
    import os

    data_obj_inp = rule_args[2]
    obj_path = str(data_obj_inp.objPath)
    resc_hier = str(data_obj_inp.condInput['resc_hier'])
    query_condition_string = f'COLL_NAME = \'{os.path.dirname(obj_path)}\' and '  \
                             f'DATA_NAME = \'{os.path.basename(obj_path)}\' and ' \
                             f'DATA_RESC_HIER = \'{resc_hier}\''

    # Note: The physical path fetched by the query may not exist on the host executing this
    # bit of policy. In a real deployment, the policy implementer should consider the hostname
    # of the resource on which the data resides and consider using the remote() microservice.
    phypath = list(Query(callback, 'DATA_PATH', query_condition_string))[0]

    exiflist = []
    with open(phypath, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        for (k, v) in tags.items():
            if k not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                exifpair = '{0}={1}'.format(k, v)
                exiflist.append(exifpair)
    exifstring = '%'.join(exiflist)
    callback.add_metadata_to_objpath(exifstring, obj_path, '-d')
    callback.writeLine('serverLog', 'PYTHON - pep_api_data_obj_put_post() complete')

