from myutils.EngLiteBase import Operator

if __name__ == '__main__':
    worker = Operator('civi2.db')
    worker.addwords_BySearch('civi.txt')
    # worker.reset()