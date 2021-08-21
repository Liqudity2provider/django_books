import jwt
import datetime
import config
from app.models.models import AuthorModel, BookModel, UserModel


def get_date(timestamp):
    if timestamp:
        return datetime.datetime.fromtimestamp(float(timestamp))


def get_models_from_id(db_model, _list_id):
    res_list = []
    if _list_id:
        for _id in _list_id:
            obj = db_model.query.get(int(_id))
            if obj:
                """Can be None if query not found Model with this id"""
                res_list.append(db_model.query.get(int(_id)))
    return res_list


def get_status(time_start, time_end):
    now = float(datetime.datetime.now().timestamp())
    if time_start and time_end:
        if now < time_start:
            return 'will'
        elif time_start >= now >= time_end:
            return 'now'
        else:
            return 'was'
    return None


def get_description(_str):
    return _str


def get_data_from_dict(dict_data):
    """dict_data has key and value pairs that we get from put request to update EventModel.
        Method iterates through dict_data and transforms simple data types into objects.
        then, return only objects that need to update in EventModel
    """

    key_value = {
        "name": dict_data.get("name"),
        "date_start": get_date(dict_data.get("date_start")),
        "date_end": get_date(dict_data.get("date_end")),
        "status": get_status(dict_data.get("date_start"), dict_data.get("date_end")),
        "description": get_description(dict_data.get("description")),
        "items": get_models_from_id(BookModel, dict_data.get("items")),
        "guests_users": get_models_from_id(UserModel, dict_data.get("guests_users")),
        "guests_authors": get_models_from_id(AuthorModel, dict_data.get("guests_authors")),
    }

    res_dict = {}

    for key in dict_data.keys():

        res_dict.update({key: key_value[key]})

    return res_dict


def delete_null_fields(_data):
    res_dict = {}
    for key in _data.keys():
        if _data[key]:
            res_dict.update({key: _data[key]})
    return res_dict


def user_from_request(_request):
    """Use Authorization: Bearer {token}"""

    token = None
    if 'Authorization' in _request.headers:
        token = _request.headers['Authorization']
        token = (token.split()[1])

    payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms=["HS256"])
    if payload['exp'] < datetime.datetime.now().timestamp():
        return {"message": "your token has been expired"}
    return UserModel.query.get(int(payload["user_id"]))