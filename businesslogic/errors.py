__author__ = '3Peso'
__all__ = ['MaxDirectoriesReachedError', 'UnknownVersionStringError', 'ApiKeyNotSetError', 'ApiKeyFormatError',
           'PathNotSetError', 'NoCollectorError', 'MD5SupportError', 'NoCountryCodeError', 'NoStringResourcesError',
           'LogFileMaximumReachedError', 'CollectorParameterError', 'GlobalPlaceholderFileError']


class MaxDirectoriesReachedError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnknownVersionStringError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ApiKeyNotSetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ApiKeyFormatError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PathNotSetError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoCollectorError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MD5SupportError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoStringResourcesError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoCountryCodeError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LogFileMaximumReachedError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CollectorParameterError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GlobalPlaceholderFileError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)