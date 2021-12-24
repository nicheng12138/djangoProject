local baseid = 10000

function setup(thread)
    thread:set("uid", baseid + math.random(0,1000000))
end

function request()
    headers = {}
    nick = 'nickname_' .. tostring(math.random(100000,999999))
    body = '{"username":"'..tostring(uid) ..'", "token":"tokenTest","picture":"http://r47q6lm7l.hn-bkt.clouddn.com/11639993218235","nickname":"'.. nick ..'"}'
    return wrk.format('POST', '/updateuser', headers, body)
end
