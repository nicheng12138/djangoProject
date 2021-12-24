local baseid = 10000

function request()
    headers = {}
    id = baseid + math.random(0,1000000)
    body = '{"username":"'.. tostring(id) ..'", "token":"tokenTest"}'
    return wrk.format('GET', '/user', headers, body)
end
