import logging

# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')

error_logger = logging.getLogger(__name__)

error_logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('logs/errorlogfile.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
file_handler.setFormatter(formatter)
error_logger.addHandler(file_handler)