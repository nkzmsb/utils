
# loggingのconfigファイルを辞書型に変換するモジュール
# filterの定義・付加が可能
# filterの定義や付加のさせ方はユーザーが変更する必要がある
# クライアントからはload_logconfig_dic()のみが参照される


import logging
import re
import yaml

# Filterの定義
class TagFilter(logging.Filter):
    """traceモードをフィルタリング

    logのメッセージに
        "filterTag" : "detail"
    の記述があるものをフィルタする
    
    一言でデバッグといっても、多くの情報をトレースしたい場合と、
    ピンポイント部分だけログしたい場合とがあるが、ログレベルはDEBUGしか用意されていない。
    そこで、ログメッセージに辞書型で{"filterTag" : ...}と記入しておき、フィルタでカットする。
    """
    
    def filter(self, record):
        # TrueをreturnすればLogする
        log_message = record.getMessage()
        
        # traceの判定
        pattern = r"'filterTag' ?: ?'detail'"
        mach = re.search(pattern, log_message, re.IGNORECASE)
        
        if mach:
            ret = False
        else:
            ret = True

        return ret
 
def addfilter(logconfig_dic, filtering=False):
    """configにfilter情報を付加する
    
    Parameters
    ----------
    logconfig_dic : dict
        付加対象の辞書
    filtering : bool, optional
        filterを付加するかどうか
        付加の仕方は、このクラス内を自分で編集する必要がある
        , by default False

    Returns
    -------
    dict
        filter情報が付加された辞書
        
    
    example of the config dictionary added filter
    LOGGING = {
        'version': 1,
        'filters': {
            'myfilter': {
                '()': MyFilter,
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'filters': ['myfilter']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
    """
    
    added_dic = logconfig_dic.copy()
    
    #####################################################
    # この部分をyamlファイルと付加させる対象にあわせて編集する
    if filtering:
        filterinfo_dic = {"tag_filter" : {'()': TagFilter}}
    else:
        # filterを付加しない場合は、デフォルトのフィルタ（logging.Filter）を設定する
        filterinfo_dic = {"tag_filter" : {'()': logging.Filter}}
    #####################################################
    
    added_dic["filters"] = filterinfo_dic
    
    # 以下のように、ハンドラへのフィルター付加をここで行うことも可能だが、
    # 記述が複雑になるので、yamlファイル側でやる方がわかりやすい。
    # ただし、同じyamlファイルの内容へのフィルタの付け外しを頻繁に行う場合には、
    # この部分でハンドラへ付加して、load_logconfig_dicのfiltering引数を切り替えるほうが良い。
    # added_dic['handlers']['console']["filters"] = ['tag_filter']
    
    return added_dic



def load_logconfig_dic(yaml_filepath, filtering=False):
    """logging.config.dictConfigの引数をyamlファイルから生成

    Parameters
    ----------
    yaml_filepath : str
        元となるyamlファイルのパス
    filtering : bool, optional
        filterを付加するかどうか
        付加の仕方は、addfilter()を自分で編集する必要がある
        , by default False

    Returns
    -------
    dict
        logging.config.dictConfigの引数となる辞書
    """
    # yamlファイルを辞書に変換
    try:
        with open(yaml_filepath, 'r') as yml:
            yaml_dic = yaml.safe_load(yml)
    except FileNotFoundError as fnfe:
        print(fnfe)
        raise
    
    yaml_dic = addfilter(yaml_dic, filtering)
              
    return yaml_dic


if __name__ == "__main__":
    print(load_logconfig_dic("log2/logconfig.yaml",filtering=True))