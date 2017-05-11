# Check values in : https://blinktrade.com/docs/

user_agent = 'private_foxbit/0.1'

BLINKTRADE_API_URL = 'https://api.blinktrade.com'
BLINKTRADE_API_VERSION = 'v1'
TIMEOUT_IN_SECONDS = 10

CURRENCY = 'BRL'
BROKER_ID = '4'
SYMBOL = 'BTCBRL'


key = '_YOURS_INFO_'
secret = '_YOURS_INFO_'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(lineno)d %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'private_foxbit.log',
            'formatter': 'verbose',
            'when': 'midnight',
            'backupCount': 30,
            'delay': False
        },
    },
    'loggers': {
        # Might as well log any errors anywhere else in Django
        'public': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '__main__' : {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

from logging import config as logConf
logConf.dictConfig(LOGGING)

try:
    from local_config import *
except ImportError:
    pass