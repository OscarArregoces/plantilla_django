from rest_framework.utils.serializer_helpers import ReturnDict
import json
import re


def create_response(code, message, data, path="", method=""):
    """
    Function to create a response to be sent back via the API
    :param request_id:Id fo the request
    :param code:Error Code to be used
    :param message:Message to be sent via the APi
    :return:Dict with the above given params
    """

    data_parse = {
        "ok": False,
        "message": "",
        "errors": "",
        "path": "",
        "method": "",
        "next": None,
        "previous": None,
        "count": None,
    }
    render = False

    try:
        match = re.search("html", data)
        if match:
            return data, code, True

        match_object = re.search("{|]", data)

        if code in [400, 401, 404, 301]:
            proccess_data = data
            if type(data) is list and len(data) > 0:
                proccess_data = ["".join(x) for x in data]
            elif type(data) is dict:
                proccess_data = [{x: data[x]} for x in data]
            elif type(data) is ReturnDict:
                proccess_data = [
                    {
                        x: data[x]["non_field_errors"][0]
                        if "non_field_errors" in data[x]
                        else data[x][0]
                    }
                    for x in data
                ]
            elif type(data) is str:
                proccess_data = data

            if type(proccess_data) is dict or type(proccess_data) is list:
                data_parse["errors"] = proccess_data
                data_parse["message"] = message
                data_parse["path"] = path
                data_parse["method"] = method
            else:
                data_parse["errors"] = (
                    proccess_data if not match_object else json.loads(proccess_data)
                )  # type:ignore
                data_parse["message"] = message
                data_parse["path"] = path
                data_parse["method"] = method

            return data_parse, code, False

        data = data if not match_object else json.loads(data)

        data_parse["data"] = data if "count" not in data else data["results"]
        data_parse["next"] = None if "next" not in data else data["next"]
        data_parse["previous"] = None if "previous" not in data else data["previous"]
        data_parse["count"] = None if "count" not in data else data["count"]

        data_parse["message"] = message
        data_parse["ok"] = True
        data_parse["path"] = path
        data_parse["method"] = method

        return data_parse, code, render
    except (Exception, BaseException) as creation_error:
        return creation_error, code, render
