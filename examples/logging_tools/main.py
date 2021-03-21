"""動作確認用のmain関数
"""

import logging, logging.config

import logconfig
import package.module as md

# logging.basicConfig(level=logging.DEBUG
#                     , format='%(asctime)s\t%(levelname)-8s\t%(name)-12s\t%(message)s'
#                     )

logger = logging.getLogger(__name__)

conf_dic = logconfig.load_logconfig_dic("examples/logging_tools/logconfig.yaml",filtering=True)
logging.config.dictConfig(conf_dic)

logger.info("start")
md.testfunc(3,4)
tc = md.TestClass()
tc.sub(bb=5,aa=3)
logger.info("end")