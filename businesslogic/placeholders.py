"""placeholders module"""__version__ = '0.0.1'__author__ = '3Peso'import functoolsimport jsonimport loggingimport refrom os import pathfrom collections import UserDictclass Placeholder:    """    The Placeholder class is been used to store 'variables' in a lookup table which later can be used to replace    actual placeholders in the instrcutions with values from the lookup table.    Those placeholders are provided by a placeholder file upon start. Instructions can also be used to fill in    placeholders, using the "placeholder" attribute, which afterwards can be used by following instructions to    run their logic.    """    PLACEHOLDER_RE = r'.*!@(?P<Mosk_Placeholder>\w+)@!.*'    PLACEHOLDER_START = '!@'    PLACEHOLDER_END = '@!'    PLACEHOLDER_GROUP_NAME = 'Mosk_Placeholder'    GLOBAL_PLACEHOLDER_FILE_PATH = './global_placeholders.json'    _logger = logging.getLogger(__name__)    _globalplaceholderfile = GLOBAL_PLACEHOLDER_FILE_PATH    # Variables which are declared inside the class definition, are static.    # Our list of placeholders should be static, so we declare it here and    # not in __init__.    _instruction_placeholders: UserDict = None    def __init__(self, function):        Placeholder._initialize_global_placeholders()        self._logger.info("Could not initialize global placeholders.")        functools.update_wrapper(self, function)        self._function = function    def __call__(self, *args, **kwargs):        """Decotrator which will feed in functions which return strings with possible        variable placeholders. It will replace those placeholders with a value, if there is        one already provided."""        returnvalue = self._function(*args, **kwargs)        return Placeholder.replace_placeholders(returnvalue)    def __get__(self, instance, instancetype):        return functools.partial(self.__call__, instance)    @staticmethod    def get_globalplaceholderfile():        return Placeholder._globalplaceholderfile    # TODO Validate file type. Should be json.    @staticmethod    def set_globalplaceholderfile(value):        if path.exists(value):            Placeholder._globalplaceholderfile = value            Placeholder._initialize_global_placeholders()    @classmethod    def update_placeholder(cls, placeholdername: str, placeholdervalue):        """Adds or updates a variable in the global variable dictionary for later use        to fill in placeholders in strings with the replace_variable decotrator."""        if placeholdername in cls._instruction_placeholders.keys():            Placeholder._logger.info("Overwriting parameter '{}'...".format(placeholdername))        cls._instruction_placeholders[placeholdername] = placeholdervalue    @classmethod    def get_placeholder(cls, placeholdername: str):        return cls._instruction_placeholders[placeholdername]    @classmethod    def _initialize_global_placeholders(cls):        cls._instruction_placeholders = None        cls._instruction_placeholders = UserDict()        with open(Placeholder.get_globalplaceholderfile()) as gpf:            placeholders = json.load(gpf)        for placeholdername in placeholders:            cls.update_placeholder(placeholdername, placeholders[placeholdername])    @classmethod    def replace_placeholders(cls, returnvalue: str):        matches = re.match(cls.PLACEHOLDER_RE, returnvalue.strip())        if matches is not None:            placeholder = matches.group(cls.PLACEHOLDER_GROUP_NAME)            Placeholder._logger.info("Variable '{}' in string found.".format(placeholder))            if placeholder in cls._instruction_placeholders:                returnvalue = returnvalue.replace("{}{}{}".format(cls.PLACEHOLDER_START, placeholder,                                                                  cls.PLACEHOLDER_END),                                                  cls._instruction_placeholders[placeholder])        else:            Placeholder._logger.debug("String '{}' does not contain a placeholder.".format(returnvalue))        return returnvalue