import functoolsimport jsonimport refrom collections import UserDictfrom businesslogic.log import mosk_loggerclass PlaceholderReplacer:    PLACEHOLDER_RE = r'.*!@(?P<Mosk_Placeholder>\w+)@!.*'    PLACEHOLDER_START = '!@'    PLACEHOLDER_END = '@!'    PLACEHOLDER_GROUP_NAME = 'Mosk_Placeholder'    GLOBAL_PLACEHOLDER_FILE_PATH = './global_placeholders.json'    # Variables which are declared inside the class definition, are static.    # Our list of placeholders should be static, so we declare it here and    # not in __init__.    _instruction_placeholders: UserDict = None    # TODO A solution but not a good solution to set wether we are in init phase or    # collect phase and thus wether a placeholder have to be replaced (collect phase)    # or if a placeholder can remain unresolved (init phase).    _collectPhase = False    def __init__(self, function):        PlaceholderReplacer._initialize_global_placeholders()        functools.update_wrapper(self, function)        self._function = function    def __call__(self, *args, **kwargs):        """Decotrator which will feed in functions which return strings with possible        variable placeholders. It will replace those placeholders with a value, if there is        one already provided."""        returnvalue = self._function(*args, **kwargs)        return PlaceholderReplacer.replace_placeholders(returnvalue)    def __get__(self, instance, instancetype):        return functools.partial(self.__call__, instance)    @staticmethod    def update_placeholder(placeholdername: str, placeholdervalue):        """Adds or updates a variable in the global variable dictionary for later use        to fill in placeholders in strings with the replace_variable decotrator."""        if placeholdername in PlaceholderReplacer._instruction_placeholders.keys():            mosk_logger.info("Overwriting parameter '{}'...".format(placeholdername))        PlaceholderReplacer._instruction_placeholders[placeholdername] = placeholdervalue    @staticmethod    def get_placeholder(placeholdername: str):        return PlaceholderReplacer._instruction_placeholders[placeholdername]    @staticmethod    def _initialize_global_placeholders():        if PlaceholderReplacer._instruction_placeholders is None:            PlaceholderReplacer._instruction_placeholders = UserDict()            with open(PlaceholderReplacer.GLOBAL_PLACEHOLDER_FILE_PATH) as gpf:                placeholders = json.load(gpf)            for placeholdername in placeholders:                PlaceholderReplacer.update_placeholder(placeholdername, placeholders[placeholdername])    @staticmethod    def set_collect_phase():        mosk_logger.debug("Collect phase has been started.")        PlaceholderReplacer._collectPhase = True    @staticmethod    def replace_placeholders(returnvalue: str):        matches = re.match(PlaceholderReplacer.PLACEHOLDER_RE, returnvalue.strip())        if matches is not None:            placeholder = matches.group(PlaceholderReplacer.PLACEHOLDER_GROUP_NAME)            mosk_logger.info("Variable '{}' in string found.".format(placeholder))            if placeholder in PlaceholderReplacer._instruction_placeholders:                returnvalue = returnvalue.replace("{}{}{}".format(PlaceholderReplacer.PLACEHOLDER_START, placeholder,                                                                  PlaceholderReplacer.PLACEHOLDER_END),                                                  PlaceholderReplacer._instruction_placeholders[placeholder])            else:                mosk_logger.info("Could not replace placeholder '{}'.".format(placeholder))                # If a placeholder is not resolved during collect phase raise an exception.                if PlaceholderReplacer._collectPhase:                    raise RuntimeError("Placeholder '{}' has not been replaced during collect phase."                                       .format(placeholder))        else:            mosk_logger.debug("String '{}' does not contain a placeholder.".format(returnvalue))        if returnvalue is None:            raise AssertionError('replace_placeholders cannot return nothing but it actually did.')        return returnvalue