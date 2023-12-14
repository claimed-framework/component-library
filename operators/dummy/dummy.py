"""
This operator sleeps for a specified time.
The idle pod can be used for testing code and accessing the terminal.
"""

import os
import logging
import time

# number of seconds to sleep (default: 600)
seconds= int(os.getenv('seconds', 600))

# Optional shell script to be executed before sleep.
shcode = os.getenv('shcode', None)

# Optional python code to be executed before sleep.
pycode = os.getenv('pycode', None)


if __name__ == '__main__':
    if shcode is not None:
        logging.info('Execute shell script:\n' + shcode)
        os.system(shcode)

    if pycode is not None:
        logging.info('Execute python code:\n' + pycode)
        exec(pycode)

    logging.info(f'Sleeps for {seconds / 60:.1f} minutes.')
    time.sleep(seconds)
