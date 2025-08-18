from dubu_client.client import DubuClient

def test_dubu_client_login():
    client = DubuClient("roboa@odense.dk")
    assert client._client.cookies, "Login failed - no cookies set after login"

    activities = client.get("odata/Aktivitet/Default.GetBySag(Id=606094)")
    assert activities, "Failed to retrieve activities"