thread=200
client=200
duration=300
url=http://127.0.0.1:8080


update_fix:# 更改用户数据 固定用户id
	wrk -t ${thread} -c ${client} -d ${duration}s --latency -s update_fix.lua ${url}/updateuser

update_rand:# 更改用户数据 随机用户id
	wrk -t ${thread} -c ${client} -d ${duration}s --latency -s update_rand.lua ${url}/updateuser

get_fix:# 获取用户数据 固定用户id
	wrk -t ${thread} -c ${client} -d ${duration}s --latency -s getuser_fix.lua ${url}/user

get_rand:# 获取用户数据 随机用户id
	wrk -t ${thread} -c ${client} -d ${duration}s --latency -s getuser_rand.lua ${url}/user
