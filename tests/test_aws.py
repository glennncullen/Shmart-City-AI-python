from app.communication import aws


# test connection to aws
def test_connect():
    assert aws.connect() is True
