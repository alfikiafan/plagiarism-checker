# /utils/logger.py

import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Mengatur logger dengan nama tertentu dan file log.

    Args:
        name (str): Nama logger.
        log_file (str): Path ke file log.
        level (int, optional): Level logging. Default adalah logging.INFO.

    Returns:
        logging.Logger: Logger yang sudah dikonfigurasi.
    """
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Contoh penggunaan:
# logger = setup_logger('plagiarism_logger', os.path.join('logs', 'app.log'))
# logger.info('Aplikasi mulai berjalan.')
