#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为提示对话框的封装
 
Authors: turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import static_text
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import view

import time


class Alert(base_frame_view.BaseFrameView):
    """
        Summary:
            普通弹出框，比如退出登录时候的弹出框\删除故事集弹出框
    """

    def __init__(self, parent, **kwargs):
        super(Alert, self).__init__(parent)

    # @property
    # def title(self):
    #     """
    #         Summary:
    #             对话框的标题
    #     """
    #     id_ = 'android:id/alertTitle'
    #     return static_text.TextView(self._linear_layout, id=id_)
    #
    # @property
    # def message(self):
    #     """
    #         Summary:
    #             对话框文本内容
    #     """
    #     id_ = 'android:id/message'
    #     return static_text.TextView(self._linear_layout, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                返回对话框上的取消按钮
        """
        name_ = '取消'
        return button.UIAButton(self.parent, name=name_)

    @property
    def confirm_button(self):
        """
            Summary:
                返回对话框上的确定按钮
        """
        name_ = '确认'
        return button.UIAButton(self.parent, name=name_)


class SelectCityAlert(Alert):
    """
        Summary:
            选择城市/地区的弹出框
    """
    title_value = u'选择城市'

    def __init__(self, parent, **kwargs):
        super(SelectCityAlert, self).__init__(parent, **kwargs)

    @property
    def province_view(self):
        """
            Summary:
                省级区域view
        """
        id_ = 'com.jiuyan.infashion:id/uc_province'
        return view.View(self._linear_layout, id=id_)

    @property
    def city_view(self):
        """
            Summary:
                市级区域view
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/uc_city'
        return view.View(self._linear_layout, id=id_)

    def _init_city(self):
        """
            Summary:
                滑动区域滑动到顶部，将城市初始化到北京东城区
        """
        curr_view = self.province_view
        location = curr_view.location
        size = curr_view.size

        x = location['x'] + size['width']/2
        end_y = location['y'] + size['height'] - 1
        start_y = location['y'] + 1

        for _ in range(9):
            self.swipe_down(x, start_y, end_y)
            time.sleep(1)
        time.sleep(3)
        log.logger.info("已经滑动到顶部")
        log.logger.info("城市初始化完毕")

    def _swipe_one_region_item(self, direction, swipe_view):
        """
            Summary:
                上下滑动一个区域item的高度
            Args:
                direction: up：向上；down:向下
                swipe_view: province_view 或者 city_view
        """
        curr_view = swipe_view
        location = curr_view.location
        size = curr_view.size

        item_height = size['height']/5
        x = location['x'] + size['width']/2

        if direction == 'up':
            end_y = location['y'] + item_height*2 + 5
            start_y = location['y'] + item_height*3
            self.swipe_up(x, start_y, end_y)
            time.sleep(1)
        elif direction == 'down':
            end_y = location['y'] + item_height * 3 + 2
            start_y = location['y'] + item_height * 2
            self.swipe_down(x, start_y, end_y)
            time.sleep(1)
        else:
            log.logger.error("滑动方向指定错误")

    def select_hangzhou(self):
        """
            Summary:
                选择浙江杭州
        """
        log.logger.info("初始化选择城市")
        self._init_city()

        for _ in range(20):
            self._swipe_one_region_item('up', self.province_view)
        time.sleep(2)
        log.logger.info("已定位到浙江省")
        time.sleep(2)
        log.logger.info("已定位到杭州市")

    def select_ningbo(self):
        """
            Summary:
                选择浙江宁波
        """
        log.logger.info("初始化选择城市")
        self._init_city()

        for _ in range(20):
            self._swipe_one_region_item('up', self.province_view)
        time.sleep(2)
        log.logger.info("已定位到浙江省")

        for _ in range(3):
            self._swipe_one_region_item('up', self.city_view)
        time.sleep(2)
        log.logger.info("已定位到宁波市")
