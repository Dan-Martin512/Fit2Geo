import fitdecode
from shapely import Point
import geopandas


def decode_fit_frame_data(frame: fitdecode.records.FitDataMessage):
    data = {}
    for field in frame.fields:
        if frame.has_field(field.name):
            value = frame.get_field(field.name).value
            data[field.name] = value
    return data


def fit_frame_filter(
        frame: fitdecode.records.FitDataMessage,
        msg_num: int,
        frame_type: int):
    if frame.frame_type == frame_type:
        if frame.global_mesg_num == msg_num:
            return frame


def get_data_frames(fit_file: str):
    with fitdecode.FitReader(fit_file) as fit:
        for frame in fit:
            if fit_frame_filter(frame, 20, fitdecode.FIT_FRAME_DATA):
                yield frame


def fit_frame_to_point(fit_frame):
    assert "position_lat" in fit_frame.keys()
    assert "position_long" in fit_frame.keys()
    assert "enhanced_altitude" in fit_frame.keys()
    lat = fit_frame["position_lat"] / (2**32 / 360)
    lon = fit_frame["position_long"] / (2**32 / 360)
    height = fit_frame["enhanced_altitude"]
    return Point(lat, lon, height)


def convert_to_geopandas(file_path: str):
    frames = get_data_frames(file_path)
    geopoints = []
    data = []

    for frame in frames:
        frame_data = decode_fit_frame_data(frame)
        timestamp = frame_data["timestamp"]
        geopoint = fit_frame_to_point(frame_data)
        geopoints.append(geopoint)
        data.append(timestamp)

    gpdf = geopandas.GeoDataFrame(data, geopoints)
    return gpdf


if __name__ == "__main__":
    print(convert_to_geopandas(r"test\data\9270632244.fit"))
