

def receive(conn, n):
    rs = []
    while n > 0:
        r = conn.recv(n)
        if not r:  # EOF
            return r
        rs.append(r)
        n -= len(r)
    return ''.join(rs)
