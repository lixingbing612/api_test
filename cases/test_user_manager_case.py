
# 主要实现的是用户管理中的测试用例

import unittest
from api.user_manager import UserManager
from loguru import logger

class TestUserManager(unittest.TestCase):

    user_id = 0

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = UserManager()
        # cls.user.login()  # 在runcase进行登录一次
        cls.username = 'testj06'
        cls.new_username = 'testj16'



    # case1->添加管理员 ： 只输入用户名和密码的情况
    def test01_add_user(self):
        #1. 初始化添加管理员的测试数据

        self.password = '123456'
        # self.user_id = None
        # 2.调用添加管理员接口
        actual_result = self.user.add_user(self.username,self.password)
        data = actual_result.get('data')
        if data:
            self.user_id = data.get('id')
            TestUserManager.user_id = self.user_id
            logger.info("获取添加管理员的用户id:{}".format(self.user_id))
        # 3. 进行断言
        self.assertEqual(0,actual_result['errno'])
        self.assertEqual(self.username,actual_result.get('data').get('username'))


    # case2 ->编辑用户 ：修改的是用户名称
    def test02_edit_username(self):
        # 1. 定义编辑的测试数据

        # 2. 请求编辑管理员的接口
        actual_result = self.user.edit_user(TestUserManager.user_id,self.new_username,password=123456)
        # 3. 进行断言
        self.assertEqual(0, actual_result['errno'])
        self.assertEqual(self.new_username, actual_result.get('data').get('username'))

    # case3 -> 查询用户列表 ：
    def test03_search_user(self):
        actual_result = self.user.search_user()

        self.assertEqual(0, actual_result['errno'])
        self.assertEqual(self.new_username, actual_result.get('data').get('list')[0].get('username'))

    # case4 -> 删除用户 ：删除指定id的用户名
    def test04_delete_user(self):
        # 1. 定义删除数据
        # 2. 请求删除接口
        logger.info("这里获取到的user_id:{}".format(self.user_id))
        actual_result = self.user.delete_user(TestUserManager.user_id,self.new_username)
        # 3. 断言返回结果
        self.assertEqual(0,actual_result['errno'])



if __name__ == '__main__':
    unittest.main()