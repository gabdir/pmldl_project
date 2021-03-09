import os
import json
import csv


conversation = []

with open(os.getcwd() + "/max_dialogs.json", "r") as f:
    data = json.load(f)
    dialogs = data["dialogs"]
    admins = data["admins"]


def mark_message(message, message_body=None):
    if message_body is None:
        message_body = {}
    message_body["is_user"] = message["is_user"]
    message_body["dialog_id"] = message["dialog_id"]
    if "createdAt" in message:
        message_body["createdAt"] = getattr(message, 'createdAt')
    message_body["from"] = message['fr']
    message_body["to"] = message['to']
    message_body["text"] = message['text']
    if not message_body["text"]:
        message_body["text"] = "empty_message"

    return message_body


def dialog_frames_daily(dialog_frame):
    full_dialogs = []
    full_admin_dialogs = []
    full_user_dialogs = []
    for i in range(len(dialog_frame)):
        current_dialog_frame = dialog_frame[i]["dialog"]
        full_messages = []
        frame_dialogs = []
        for j in range(len(current_dialog_frame) - 1):
            full_messages.append(current_dialog_frame[j]["text"])
            if current_dialog_frame[j + 1]['from'] != current_dialog_frame[j]['from']:
                full_messages = ", ".join(full_messages)
                if current_dialog_frame[j]['is_user']:
                    frame_dialogs.append({"role": "user", "message": full_messages, "hash": hash(full_messages)})
                    full_user_dialogs.append([{"role": "user", "message": full_messages, "hash": hash(full_messages)}])
                else:
                    frame_dialogs.append({"role": "admin", "message": full_messages, "hash": hash(full_messages)})
                    full_admin_dialogs.append(
                        [{"role": "admin", "message": full_messages, "hash": hash(full_messages)}])
                full_messages = []
        full_dialogs.append(frame_dialogs)
        if current_dialog_frame[len(current_dialog_frame) - 1]['from'] == \
                current_dialog_frame[len(current_dialog_frame) - 2]['from'] and full_messages:
            full_messages = ", ".join(full_messages)
            if current_dialog_frame[len(current_dialog_frame) - 1]['is_user']:
                frame_dialogs.append({"role": "user", "message": full_messages, "hash": hash(full_messages)})
                full_user_dialogs.append([{"role": "user", "message": full_messages, "hash": hash(full_messages)}])
            else:
                frame_dialogs.append({"role": "admin", "message": full_messages, "hash": hash(full_messages)})
                full_admin_dialogs.append(
                    [{"role": "admin", "message": full_messages, "hash": hash(full_messages)}])
        full_dialogs.append(frame_dialogs)

    return full_dialogs, full_admin_dialogs, full_user_dialogs


def strict_contains(obj, admin_list):
    if obj["fr"] not in admin_list:
        obj["is_user"] = True
    else:
        obj["is_user"] = False
    obj["dialog_id"] = obj['fr'] if obj['fr'] not in admin_list else obj['to']

    return obj["dialog_id"]


def dialog_frames_processing(data, admin_list):
    for frame in range(len(data)):
        dialog = data[frame]["dialog"]
        for message in range(len(dialog)):
            # print(dialog[message])
            strict_contains(dialog[message], admin_list)
    for frame in range(len(data)):
        dialog = data[frame]["dialog"]
        for message in range(len(dialog)):
            message_body = mark_message(dialog[message])
            dialog[message] = message_body
    return data


ds = dialog_frames_processing(dialogs, admins)

full_dialogs, full_admin_dialogs, full_user_dialogs = dialog_frames_daily(ds)


with open('dialogs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Question', 'Answer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(0, len(full_dialogs[0]) - 1, 2):
        conv = []
        if full_dialogs[0][i]["role"] == "admin":
            conv.append((full_dialogs[0][i+1]["message"], full_dialogs[0][i]["message"]))
        else:
            conv.append((full_dialogs[0][i]["message"], full_dialogs[0][i+1]["message"]))
        writer.writerow({'Question': conv[0][0], 'Answer': conv[0][1]})
