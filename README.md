
# MWK logger

---
[![PyPI](https://img.shields.io/pypi/v/mwk-logger)](https://pypi.org/project/mwk-logger/)  
**Custom logger with colors on terminal.**  

![mwk_logger_example](https://user-images.githubusercontent.com/105928466/172430763-e3407715-3b97-40e4-8cdb-9e2e64adc6e6.jpg)

**And some useful decorators.**  

---

## Using logger 

```
pip install mwk-logger
```
### 1. Get instance of mwk-logger
```python
from mwk_logger import MwkLogger

log = MwkLogger(name='mwk',
                file='logger.log',
                stream_level='DEBUG',
                file_level='DEBUG',
                time=True)
```
>*! No need to add* ***.logger*** *at the end !*   

*keyword parameters:*  
- *name* - name of the logger, by default = 'mwk',
- *file* - path to file to log into, by default = 'mwk.log',
- *stream_level* - logging level for terminal, by default = 'WARNING',
- *file_level* - logging level for file, by default = None,
- *time* - if timestamp should be added to terminal log, by default = False,

LEVELS:
 **None** - no logging or:  
 '**DEBUG**', '**INFO**', '**WARNING**', '**ERROR**', '**CRITICAL**'.  
If both levels are set to **None** stream_level is changed to **WARNING**.  
Timestamp is always added to file logs. One can set if timestamp will be added to terminal logs.  

### 2. Logging  
```python
log.debug('This is a debug message.')
log.info('This is an info message.')
log.warning('This is a warning message.')
log.error('This is an error message!')
log.critical('This is a critical message!!!')
log.exception('This is an exception message!')
```

### 3. Decorators
1. timer - 