import izi
import happy_birthday
from falcon import HTTP_400, HTTP_404, HTTP_200

def tests_happy_birthday():
    response = izi.test.get(happy_birthday, 'happy_birthday', {'name': 'ViTuocGia', 'age': 25})
    assert response.status == HTTP_200
    assert response.data is not None

def tests_season_greetings():
    response = izi.test.get(happy_birthday, 'greet/Christmas')
    assert response.status == HTTP_200
    assert response.data is not None
    assert str(response.data) == "Merry Christmas!"
    response = izi.test.get(happy_birthday, 'greet/holidays')
    assert str(response.data) == "Happy holidays!"
