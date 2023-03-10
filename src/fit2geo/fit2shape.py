import fitdecode


def decode_fit_frame_data(frame):
    data = {}
    for field in frame.fields:
        if frame.has_field(field.name):
            value = frame.get_field(field.name).value
            data[field.name] = value
    return data


def fit_frame_filter(frame, msg_num, frame_type):
    if frame.frame_type == frame_type:
        if frame.global_mesg_num == msg_num:
            return frame


def get_data_frames(fit_file):
    with fitdecode.FitReader(fit_file) as fit:
        for frame in fit:
            if fit_frame_filter(frame, 19, fitdecode.FIT_FRAME_DATA):
                yield frame


def Convert(file_path):
    frames = get_data_frames(file_path)
    for frame in frames:
        data = decode_fit_frame_data(frame)
        print(data)
