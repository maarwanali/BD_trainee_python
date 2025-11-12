
LOGGING_CONFIG={
    'version':1,
    'disable_existing_loggers':False,
    
    "formatters":{
        "standard":{
            "format":'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers':{
        'console':{
            'class':'logging.StreamHandler', 
            'formatter':'standard',
            'level':'INFO'
        },
        'file':{
            'class':'logging.FileHandler',
            'filename':'debug/elt.log',
            'formatter':'standard',
            'level':'DEBUG'
        }
    },

    'root':{
        'handlers':['console','file'],
        'level':'DEBUG'
    }


}