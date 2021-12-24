local baseid = 10000

function setup(thread)
    thread:set("uid", baseid + math.random(0,1000000))
end

function request()
    headers = {}
    body = '{"username":"'.. tostring(uid) ..'", "token":"tokenTest"}'
    return wrk.format('GET', '/user', headers, body)
end
