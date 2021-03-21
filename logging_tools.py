
import inspect
import logging

class LoggingTools():
    """モジュールのロギング実装を補助するユーティリティークラス
    """
    def __init__(self,name):
        """
        Parameters
        ----------
        name : str
            "__name__"が渡されることを推奨する
        """
        self.__logger = logging.getLogger(name)
        self.__logger.addHandler(logging.NullHandler())

    @property
    def logger(self):
        return self.__logger

    def log_deco(self,func):
        """関数呼び出し前後のデバッグログ実装用デコレータ
        
        ログメッセージの内容は必要に応じて編集して使用する
        """
        def wrap(*args,**kwargs):
            self.logger.debug({"action":"run"
                               , "function":func.__qualname__})
            func(*args, **kwargs)
            self.logger.debug({"action":"finished"
                               , "function":func.__qualname__})
        return wrap
    
def getfuncname()->str:
    """呼び出し元の関数名を返す
    
    呼び出し元がクラスメソッドの場合、
    "[クラス名].[メソッド名]"
    を返す。
    クラス名の取得が少し強引。もっといい方法があるかも。
    """
    
    frame = inspect.stack()[1]
    function_name = frame.function
    locals_dic = inspect.getargvalues(frame[0]).locals
    if ("self" in locals_dic.keys()):
        # 名前空間内にselfがある場合、呼び出し元はメソッド関数であると判断してクラス名を取りに行く
        try:
            class_name = locals_dic["self"].__class__.__name__
            return class_name + "." + function_name
        except Exception as ex:
            # 現時点では例外発生を想定していないけれども、念のため
            print(ex)
            return function_name
    else:
        return function_name

