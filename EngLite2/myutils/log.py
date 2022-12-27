import logging

__handlerF = logging.FileHandler('log.log')
__handlerF.setLevel(logging.DEBUG)
__handlerC = logging.StreamHandler()
__handlerC.setLevel(logging.INFO)
__formatter = logging.Formatter('%(asctime)s <%(levelname)s>: %(message)s')
__handlerF.setFormatter(__formatter)
__handlerC.setFormatter(__formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(__handlerF)
logger.addHandler(__handlerC)