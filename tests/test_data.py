import os

def test_data_splitting():

    BASE_PATH = os.getcwd()
    assert os.path.exists(os.path.join(BASE_PATH, "Data", "split", "train")), "Train folder missing!"
    assert os.path.exists(os.path.join(BASE_PATH, "Data", "split", "test")), "Test folder missing!"