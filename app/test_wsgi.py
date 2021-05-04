1
2
3
4
5
6
7
8
9
def application(environ, start_response):
    status = '200 OK'
    output = b'Hooray, mod_wsgi is working'
 
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
 
    return [output]
