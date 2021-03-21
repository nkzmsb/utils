import logging
import sys

sys.path.append('../utils/')

from logging_tools import LoggingTools,getfuncname

log = LoggingTools(__name__) # 引数は__name__

# LoggingToolsの使い方
@log.log_deco # 関数にデコレートすることで前後にログを発生
def testfunc(a,b):
    log.logger.info({"arg":[a,b], "func":getfuncname()}) # loggerを使って任意のログを発生
    
class TestClass(object):
    @log.log_deco
    def __init__(self, a=2, b=5):
        self.a = a
        self.b = b
    
    # クラス内のメンバ関数にも同様にデコレータを使用可能
    @log.log_deco
    def sub(self,aa,bb):
        log.logger.info({"arg":[aa,bb],"func":getfuncname()})