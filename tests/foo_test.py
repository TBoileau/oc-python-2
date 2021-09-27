from src.example import Example


def test_foo():
    example: Example = Example('name')
    assert example.name == 'name'
    assert example.test() == 'name'
    assert example.test2() == 'name'
