#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:好友添加模块

Authors: turinblueice
Date: 2016/7/26
"""


from UIAWindows.friend_activities import add_friend_activity
from UIAWindows.in_main_windows import focus_tab_activity
from UIAWindows.in_main_windows import user_center_tab_window
from UIAWindows.user_center_sub_windows import user_friends_activity
from UIAWindows.personal_detail_windows import personal_main_window

from gui_widgets.custom_widgets import bottom_tab_widget

from base import base_frame_view
from base import app_unit_test
from util import log

from multi_clients_manager import multi_clients_base_test
from common_actions import access_to_window


class FriendsTestCase(app_unit_test.AppTestCase, multi_clients_base_test.MultiClientsBaseTest):

    driver = None

    def __init__(self, *args, **kwargs):
        super(FriendsTestCase, self).__init__(*args, **kwargs)
        multi_clients_base_test.MultiClientsBaseTest.__init__(self, **kwargs)

    def setUp(self):
        driver = self.create_driver(self.debug_mode)
        action = access_to_window.ActionsAccess2Window(driver)

        action.wait_for_app_launch()
        action.go_to_focus_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()

    def test_follow_and_unfollow_talent_operation(self):
        """
            test_cases/test_friends_operations.py:FriendsTestCase.test_follow_talent_operation
        Summary:
            关注达人和取消关注达人case

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:

            curr_focus_activity = focus_tab_activity.FocusTabActivity(base_app)

            log.logger.info("点击添加好友按钮")
            status = curr_focus_activity.tap_add_friend_button()
            self.assertTrue(status, "进入好友添加页面失败")

            curr_friend_add_activity = add_friend_activity.AddFriendActivity(base_app)
            log.logger.info("开始向左边滑动好友类型栏")
            curr_friend_add_activity.swipe_left_friend_category()

            log.logger.info("开始点击明星达人按钮")
            status = curr_friend_add_activity.tap_start_talent_item()
            self.assertTrue(status, "明星达人列表未加载成功")

            log.logger.info("获取第一个推荐明星的名称")
            follow_talent_name = curr_friend_add_activity.start_talent_follow_friends_list[0].user_name

            log.logger.info("点击关注\"{}\"".format(follow_talent_name))
            curr_friend_add_activity.start_talent_follow_friends_list[0].tap_follow_button()

            log.logger.info("点击返回按钮，准备去好友中心验证关注结果")
            status = curr_friend_add_activity.tap_back_button()
            self.assertTrue(status, "返回主页失败")

            tab_widget = bottom_tab_widget.BottomTabWidget(base_app)
            log.logger.info("点击中心tab")
            tab_widget.tap_center_tab()

            curr_center_activity = user_center_tab_window.UserCenterTabWindow(base_app)
            curr_center_activity.swipe_up_entire_scroll_view()

            curr_center_activity.tap_friends_bar()

            curr_my_friends_activity = user_friends_activity.UserFriendsActivity(base_app)

            log.logger.info("搜索刚刚关注的达人")
            status = curr_my_friends_activity.display_search_list()
            self.assertTrue(status, "搜索结果列表没有出现")

            log.logger.info("验证搜索结果内是否存在刚刚关注的达人")
            index = curr_my_friends_activity.check_friend_in_search_list(follow_talent_name)

            self.assertTrue(index, "没有搜索出刚刚关注的达人")
            log.logger.info("搜索结果已成功搜出")

            log.logger.info("点击该达人搜索结果")
            status = curr_my_friends_activity.friend_item_list[index].tap()
            self.assertTrue(status, "进入达人日记主页失败")

            curr_personal_activity = personal_main_window.PersonalMainActivity(base_app)
            curr_personal_activity.tap_unfollow_button()
            curr_personal_activity.tap_confirm_unfollow_button()

            self.assertEqual('+ 关注', curr_personal_activity.follow_button.text,
                             "取消关注未成功")

        except Exception as exp:
            log.logger.error("发现异常, case:test_follow_unfollow_talent_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'follow_talent', exp)
