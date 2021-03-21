"""動作確認用のmain関数
"""

import logging

import package.module as md

logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s\t%(levelname)-8s\t%(name)-12s\t%(message)s'
                    )

logging.info("start")
md.testfunc(3,4)
tc = md.TestClass()
tc.sub(bb=5,aa=3)
logging.info("end")