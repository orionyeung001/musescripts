from functools import reduce
from itertools import tee
def ilen(iterable):
    return reduce(lambda sum, element: sum + 1, iterable, 0)

def get_data(f, process_data, obj_filt=None, data_filt=None):
    """
    for each object `obj` in file `f` passing `obj_filt`
        map(process_data, filter(filt, f.keys()))

    assumes that obj_filt function accepts the file object and the object key
    [from f.keys()] as args, ex:
        >>> obj_filt(f, f.keys()[0]) # test if first item is to be processed
    """
    if obj_filt is not None:
        obj_keys = filter(lambda x: obj_filt(f, x), f.keys())
    else:
        obj_keys = f.keys()

    obj_keys, obj_keys_ = tee(obj_keys)
    if ilen(obj_keys_) == 0: return None

    obj_list = (f[obj_key] for obj_key in obj_keys)
    data_pair_list = list(map(lambda obj: (obj, process_data(obj)), obj_list))
    if data_filt is not None:
        return filter(lambda p: data_filt(p[1]), data_pair_list)
    else:
        return data_pair_list

# class ROOT_Reader:
#     def __init__(self, fname_getter, ps_routine, obj_filt, data_filt):
#         self.get_fnames = fname_getter
#         self.process_routine = ps_routine
#         self.object_filter = object_filt
#         self.data_filter = data_filt

#     # defd for for loops to ps files
#     def __init__():
#         self.filenames_iter = iter(self.get_fnames())
#         return self
#     def __next__():
#         return next(filenames_iter)

