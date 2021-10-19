from main import modifyFilePath


def test_file():
    assert modifyFilePath("/mnt/data/srv/data/newsarchive/2020-01-01/test") == "C:/srv/data/newsarchive/2020-01-01/test"