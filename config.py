import yaml
from enum import Enum


class CommonConfig(dict):

    class Any(object):
        pass

    def __init__(self, dictInst={}):
        super(CommonConfig, self).__init__(dictInst)
        self.structurize()

    def structurize(self):
        ''' Walks through the dict recursevly
            and replaces interior dicts with
            CommonConfig objects '''
        for key, value in self.iteritems():
            if type(value) == dict and len(value):
                self[key] = CommonConfig(self[key])

    def read(self, fname):
        with open(fname, 'r') as f:
            self.update(yaml.load(f.read()))
            self.structurize()

    def write(self, fname):
        with open(fname, 'w') as f:
            f.write(yaml.dump(self, default_flow_style=False))

    def get(self, key, default=None):
        ''' Returns an instance of CommonConfig class or,
            if there no interior dicts, an object stored in the dict.
        '''
        __retval = dict.get(self, key, default)
        if type(__retval) == CommonConfig and len(__retval):
            return __retval
        else:
            return CommonConfig() if default == {} else __retval

    def __getitem__(self, key):
        ''' Operator [].
            Returns an instance of CommonConfig class or,
            if there no interior dicts, an object stored in the dict.
        '''
        return dict.__getitem__(self, key)

    def validate(self, ref_conf):
        ''' Makes validation of current held configuration
            agains referenced one, passed as ref_conf.
            Reference configuration must have following structure:
            {'dgt_param' : {'def': default_int_value1, \
                            'range': 'range_string'},  # for int, float, long
             'str_param' : {'def': 'string'},          # for strings
             'dict_param': {'def': {...}},             # for dicts
             'enum_param': {'def': Enum(...)[...]},    # for enums
             'list_param': {'def': [...]},             # for lists
             'other':      {'def': value}}             # for other types
            Range string is optional. Content of dicts and list is verified
            as well.
            In case of any collisions found between configuration,
            default values from reference configuration are applied.
            Returns array of messages for all collisions found.
        '''
        if type(ref_conf) != dict:
            return []

        ABSENT_SRT = 'Parameter \'{}\' is absent in configuration. '
        APPLAY_STR = 'Applying default value: {}.\n'
        WRONG_TYPE_STR = 'Unexpected type for \'{}\' ' \
                         'in configuration: {}; expected: {}. '
        WRONG_BOUND_STR = 'Parameter \'{}\'={} is out of ' \
                          'expected boundaries {}{}...{}{}. '
        WRONG_ENUM_STR = 'Unexpected value for \'{}\'={}; ' \
                         'possible values: {}. '
        WRONG_LIST_LEN = 'Unexpected list lenght for \'{}\' ' \
                         'in configuration: {}; expected: {}. '
        WRONG_LIST_ELEM = 'Unexpected list element for \'{}\': '
        ret = []

        for param in ref_conf:
            if type(ref_conf[param]) != dict:
                continue

            error_str = ''
            self[param] = self.get(param)
            def_val = ref_conf[param].get('def')
            rng_str = ref_conf[param].get('range')
            exp_type = type(def_val)

            if self[param] is None:
                error_str += ABSENT_SRT.format(param)
                if issubclass(exp_type, Enum):
                    def_val = def_val.name  # take only value name
                elif issubclass(exp_type, dict):
                    tmp_val = CommonConfig({})
                    retv = tmp_val.validate(def_val)
                    map(lambda x: ret.append(x), retv)
                    def_val = tmp_val
                elif issubclass(exp_type, list):
                    def_val = filter(lambda x: x != self.Any, def_val)

            # Dict
            elif issubclass(exp_type, dict):
                retv = self[param].validate(def_val)
                map(lambda x: ret.append(x), retv)

            # List
            elif issubclass(exp_type, list):
                def validate_list(_it, _list, _def):
                    ''' Aux function to check content of the list'''
                    res, err = [], []
                    for ix, item in enumerate(_it):
                        access_srt = 'list elem by index ' + str(ix)
                        tmp_val = CommonConfig({access_srt: item}) \
                            if _it == _list else CommonConfig({})
                        if (isinstance(_def[ix], dict) and
                           _def[ix].get('def') is not None):
                                retv = tmp_val.validate(
                                    {access_srt: _def[ix]})
                        else:
                            retv = tmp_val.validate(
                                {access_srt: {'def': _def[ix]}})
                        map(lambda x: err.append(x), retv)
                        res.append(tmp_val[access_srt])
                    return res, err

                if not isinstance(self[param], list):
                    def_val = filter(lambda x: x != self.Any, def_val)
                    error_str += WRONG_TYPE_STR.format(
                        param, type(self[param]), exp_type)
                    def_val, err = validate_list(def_val, {}, def_val)
                    self[param] = None

                else:
                    first = (self.Any
                             if (def_val and
                                 def_val[0] is self.Any)
                             else None)
                    last = (self.Any
                            if ((len(def_val) > 1 and
                                 def_val[len(def_val) - 1] is self.Any) or
                                (len(def_val) == 1 and
                                 first is self.Any))
                            else None)
                    def_val = filter(lambda x: x != self.Any, def_val)

                    if ((len(self[param]) < len(def_val)
                         if first is None else False) or
                        (len(self[param]) > len(def_val)
                         if last is None else False) or
                        (len(self[param]) != len(def_val)
                         if (first is None and last is None) else False)):
                        error_str += WRONG_LIST_LEN.format(
                            param, len(self[param]), len(def_val))
                        def_val, err = validate_list(def_val, {}, def_val)
                        self[param] = None
                    else:
                        size_to_check = min(len(self[param]), len(def_val))
                        res, err = validate_list(
                            self[param][:size_to_check],
                            self[param][:size_to_check], def_val)
                        tail = self[param][size_to_check:]
                        self[param] = res
                        map(lambda x:  self[param].append(x), tail)
                        map(lambda x: ret.append(
                            WRONG_LIST_ELEM.format(param) + x), err)

            # Enum
            elif issubclass(exp_type, Enum):
                if exp_type.__members__.get(
                   str(self[param]), None) is None:
                    error_str += WRONG_ENUM_STR.format(
                        param, self[param],
                        [x for x, _ in exp_type.__members__.items()])
                    def_val = def_val.name  # take only value name
                    self[param] = None

            # Integral common
            elif (exp_type is not None and
                  not isinstance(self[param], exp_type)):
                    error_str += WRONG_TYPE_STR.format(
                        param, type(self[param]), exp_type)
                    self[param] = None

            # Ordered
            elif ((exp_type == int or
                   exp_type == float or
                   exp_type == long) and
                  rng_str is not None):

                rng_str = rng_str.replace(' ', '')
                left_bnd, body, right_bnd = \
                    rng_str[0], rng_str[1:-1], rng_str[-1]
                values = body.split(',')

                if len(values) == 2:
                    left_val, right_val = values[0], values[1]
                else:  # ignore silently
                    continue

                predicates = {'[': lambda a, b: float(a).__ge__(float(b)),
                              '(': lambda a, b: float(a).__gt__(float(b)),
                              ']': lambda a, b: float(a).__le__(float(b)),
                              ')': lambda a, b: float(a).__lt__(float(b))}

                if ((not predicates[left_bnd](self[param], left_val)
                        if left_val is not '' else False) or
                    (not predicates[right_bnd](self[param], right_val)
                        if right_val is not '' else False)):

                        error_str += WRONG_BOUND_STR.format(
                            param, self[param], left_bnd,
                            left_val if left_val is not '' else 'Inf',
                            right_val if right_val is not '' else 'Inf',
                            right_bnd)
                        self[param] = None

            if self[param] is None:
                error_str += APPLAY_STR.format(def_val)
                self[param] = def_val
                ret.append(error_str[:-1])

        return ret

# singleton
config = CommonConfig()
