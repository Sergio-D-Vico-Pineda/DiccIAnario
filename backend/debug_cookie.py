import httpx

def main():
    s = httpx.Client()
    resp = s.post('http://127.0.0.1:8000/api/session')
    print('status', resp.status_code)
    print('set-cookie header:', resp.headers.get('set-cookie'))
    print('client cookies after response:', s.cookies)

    resp2 = s.post('http://127.0.0.1:8000/api/validate', json={'term':'gato'})
    print('validate status (with cookie):', resp2.status_code)
    print('validate body:', resp2.text)

    # manual cookie header attempt
    c = httpx.Client()
    if 'set-cookie' in resp.headers:
        c.headers['cookie'] = resp.headers['set-cookie']
    resp3 = c.post('http://127.0.0.1:8000/api/validate', json={'term':'gato'})
    print('validate status (manual header):', resp3.status_code)
    print('validate body (manual):', resp3.text)

if __name__ == '__main__':
    main()
