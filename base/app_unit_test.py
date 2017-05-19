#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 商家版单测模块

Authors: turinblueice
Date:    16/3/23 16:18
"""

import traceback
import unittest

from base import base_frame_view
from util import log


class AppTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AppTestCase, self).__init__(*args, **kwargs)

    def assert_and_save_screen_shot(self, obj, screen_shot_name, expected, actual, msg=None):
        """
        Args:
            obj: BaseFrameView对象
        Return:
        """

        try:
            super(AppTestCase, self).assertEqual(expected, actual, msg)
        except:
            if isinstance(obj, base_frame_view.BaseFrameView):
                obj.save_screen_shot(screen_shot_name)
            else:
                log.logger.error('截图失败,截图对象不是BaseFrameView类型。')
            tmp_msg = '期待结果:{},实际结果:{}。失败信息:'.format(expected, actual)
            tmp_msg += msg

            #  抛出已捕获的异常, 供上层捕获判断用例失败
            raise self.failureException(tmp_msg)

    @staticmethod
    def raise_exp_and_save_screen_shot(obj, case_name, exp):
        """
        Summary:
            截图并抛出截获的异常
        Args:
            obj: 测试framework对象，如activity、控件对象等
            case_name: 测试用例名称
            exp: 引发的异常对象
        Return:
        """
        log.logger.error(str(exp))
        log.logger.error(traceback.format_exc())
        if isinstance(obj, base_frame_view.BaseFrameView):
            obj.save_screen_shot(case_name)
        else:
            log.logger.error('截图失败,截图对象不是BaseFrameView类型。')
        raise exp
