def test_health_check(client):
    assert client.get('/is-alive').json['alive'] == True
