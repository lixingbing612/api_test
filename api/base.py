

"""
base文件作用：主要用于所有接口的公共功能使用一个基类（父类）
1.处理url
2.重新封装get、post方法
3.处理头信息
4.登录功能
"""
from setting import BASE_URL, LOGIN_INFO  	# 导入setting
import requests						# 导入requests
from loguru import logger			# 导入日志
from cacheout import Cache					# 导入缓存包  主要用作缓存	1.设置缓存：cache.set(key,value) 2.获取缓存：cache.get(key)

cache = Cache()		# 创建了cache对象

class Base():

	# 实现url的拼接
	def get_url(self,path,params=None):
		"""
		返回一个完整的url
		:param path:接口路径，如/admin/admin/update
		:param params:查询参数，如?page=1&limit=20&sort=add_time&order=desc
		retrun：full_url:http://121.196.13.152:8080/admin/auth/login
		"""
		if params:	# params 有参数
			full_url = BASE_URL + path + params
			return full_url
		return BASE_URL + path	# params 没有参数

	# 重写get方法
	def get(self,url,headers=None):
		result = None
		response = requests.get(url,headers=self.get_headers())		# headers调用get_headers
		try:
			result = response.json()
			logger.success("请求URL:{},返回结果:{}".format(url,result))
			return result
		except Exception as e:
			logger.error("请求get方法异常，返回数据为:{}".format(result))

	# 重写post方法
	def post(self,url,data,headers=None):
		"""
		在原来post方法的基础上，新增日志以及直接返回json格式
		:return
		"""
		result = None
		response = requests.post(url,json=data,headers=self.get_headers())		# headers调用get_headers
		try:
			result = response.json()
			logger.success("请求URL:{},请求参数:{},返回结果:{}".format(url,data,result))
			return result
		except Exception as e:
			logger.error("请求post方法异常，返回数据:{}".format(result))

	# 实现所有头信息的处理
	def get_headers(self):
		"""
		处理请求头
		:return:返回的时字段格式的请求头，多是包括了Content-Type，X-Litemall-Admin-Token
		"""
		headers = {"Content-Type":"application/json"}
		token = cache.get("token")			# 从缓存中获取token值
		if token:
			headers.update({"X-Litemall-Admin-Token":token})
			return headers
		return headers

	#实现登录功能
	def login(self):
		"""
		通过调用登录接口获取token值，将其缓存，其他接口使用时直接从缓存中取数
		若没有取到，再调用登录，再将token值放在缓存中
		:return:
		"""
		login_path = "/admin/auth/login"
		login_url = self.get_url(login_path)			# 拼接登录接口地址
		result = self.post(login_url,LOGIN_INFO)		# 请求登录接口
		try:
			if 0 == result.get("errno"):
				logger.info("请求登录接口成功")
				token = result.get("data").get("token")
				cache.set("token",token)				# 设置缓存token
			else:
				logger.error("登录失败:{}".format(result))
				return None
		except Exception as e:
			logger.error("请求登录接口异常，异常数据:{}".format(result))
			logger.error("报错信息:{}".format(e))


if __name__ == '__main__':
	base = Base()
	# print(base.get_url("/admin/auth/login"))
	# print(base.get_url("/admin/admin/update"))
	# print(base.get_url("/admin/admin/list", "?page=1&limit=20&sort=add_time&order=desc"))
	login_url = base.get_url("/admin/auth/login")
	login_data = {"username":"admin123","password":"admin123"}
	print(base.post(login_url, login_data))