from datetime import datetime


def readeable_hour(hours: str, fecha) -> bool:
    valid, gst = hours.split(" ")
    middle = 12
    year, month, day = fecha.year, fecha.month, fecha.day

    if gst == "PM":
        hour, minute = valid.split(":")
        middle += int(hour)

        return (
            datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=middle,
                minute=int(minute),
            )
            < datetime.now()
        )

    elif gst == "AM":
        hour, minute = valid.split(":")

        return (
            datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute),
            )
            < datetime.now()
        )

    return False
