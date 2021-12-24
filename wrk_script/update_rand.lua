local baseid = 10000

function request()
    headers = {}
    id = baseid + math.random(0,1000000)
    nick = 'nickname_' .. tostring(math.random(100000,999999))
    body = '{"username":"'.. id .. '", "token":"tokenTest","picture":"http://r47q6lm7l.hn-bkt.clouddn.com/11639993218235","nickname":"'.. nick ..'"}'
    return wrk.format('POST', '/updateuser', headers, body)
end
