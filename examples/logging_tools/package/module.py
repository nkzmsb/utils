import logging
import sys

sys.path.append('../utils/')

from logging_tools import LoggingTools,getfuncname

log = LoggingTools(__name__) # 引数は__name__

# LoggingToolsの使い方
@log.log_deco # 関数にデコレートすることで前後にログを発生
def testfunc(a,b):
    ret = a+b
    log.logger.debug({"filterTag":"detail"
                      , "func":getfuncname()
                      , "values":{"args":[a,b], "return":ret}}) # loggerを使って任意のログを発生
    log.logger.info({"func":getfuncname(), "values":{"return":ret}})
    return ret
    
class TestClass(object):
    @log.log_deco
    def __init__(self, a=2, b=5):
        self.a = a
        self.b = b
    
    # クラス内のメンバ関数にも同様にデコレータを使用可能
    @log.log_deco
    def sub(self,aa,bb):
        ret = aa-bb
        log.logger.debug({"filterTag":"detail"
                        , "func":getfuncname()
                        , "values":{"args":[aa,bb], "return":ret}}) # loggerを使って任意のログを発生
        log.logger.info({"func":getfuncname(), "values":{"return":ret}})
        return ret