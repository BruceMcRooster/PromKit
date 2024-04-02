from playsound import playsound

import google_sheet
import csv
import PySimpleGUI as sg
import cv2


def main():
    sg.theme('Black')

    layout = [
        [sg.Button('🔄', key='refresh')],
        [
            sg.Frame('New Sign In', [
                [sg.Text('', key='name', font=('default', 32))],
                [sg.Text('Paid '), sg.Text('', key='has_payed')],
                [sg.Text('Approved '), sg.Text('', key='is_approved')],
                [sg.Text('Already Checked In '), sg.Text('', key='already_checked_in')],
                [sg.Frame('Uh-Oh', [
                    [sg.Text('', key='warning_msg')],
                    [sg.Button('Check In Anyway', key='override_button', visible=False)]
                ],
                          key='warning',
                          background_color='red',
                          visible=False)]
            ]),
            sg.Frame('Feed', [
                [sg.Image(filename='', key='camera_feed', size=(400, 300))],
                [sg.Frame('Raw Collected', [
                    [sg.Text('ID: '), sg.Text('', key='raw_id')],
                    [sg.Text('Name: '), sg.Text('', key='raw_name')]
                ])]
            ])
        ]]

    window = sg.Window('Prom Check-In', layout=layout, relative_location=(-200, -100))

    cap = cv2.VideoCapture(0)
    qcd = cv2.QRCodeDetector()

    cache = {
        'raw_id': '',
        'raw_name': '',
        'name': '',
        'grade': '',
        'has_payed': '',
        'is_approved': '',
        'already_checked_in': ''
    }

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        if event == 'refresh':
            refresh()

        if event == 'override_button':
            mark_as_checked_in(cache['raw_id'])

            window['warning'].update(visible=False)
            window['override_button'].update(visible=False)

        img_byte, raw_id, raw_name = read_qr(cap, qcd)

        window['camera_feed'].update(data=img_byte)

        if not raw_id:
            continue

        if raw_id == cache['raw_id'] and raw_name == cache['raw_name']:
            continue

        cache['raw_id'] = raw_id

        cache['raw_name'] = raw_name

        window['raw_id'].update(cache['raw_id'])
        window['raw_name'].update(cache['raw_name'])

        id_and_name_agree: bool | None
        id_and_name_agree, data = lookup(raw_id, raw_name)

        if id_and_name_agree is not None:
            cache['name'] = data[0]
            cache['age'] = data[1]
            cache['has_payed'] = '✔' if data[2] == 'Yes' else '❌'
            cache['is_approved'] = '✔' if data[3] == 'Yes' else '❌' if data == 'No' else 'N/A'
            cache['already_checked_in'] = data[4]

            if id_and_name_agree:
                if cache['already_checked_in'] == 'Yes':

                    playsound('deny.mp3')

                    window['warning'].update(visible=True)
                    window['warning_msg'].update('User has already checked in')
                    window['override_button'].update(visible=True)

                elif cache['has_payed'] == '✔' and (cache['is_approved'] == '✔' or cache['is_approved'] == 'N/A'):
                    window['warning'].update(visible=False)
                    mark_as_checked_in(raw_id)

                else:
                    playsound('deny.mp3')
                    window['warning'].update(visible=True)
                    window['warning_msg'].update('User has not payed or is not approved.')
                    window['override_button'].update(visible=True)

            else:
                playsound('deny.mp3')
                window['warning'].update(visible=True)
                window['warning_msg'].update('Found name that is different than that on the QR Code.')
                window['override_button'].update(visible=True)

        else:

            cache['name'] = ''
            cache['grade'] = ''
            cache['has_payed'] = ''
            cache['is_approved'] = ''
            cache['already_checked_in'] = ''

            playsound('deny.mp3')
            window['warning'].update(visible=True)
            window['warning_msg'].update('Could not find ID.')
            window['override_button'].update(visible=False)

        window['name'].update(cache['name'])
        window['has_payed'].update(cache['has_payed'])
        window['is_approved'].update(cache['is_approved'])
        window['already_checked_in'].update(cache['already_checked_in'])


def read_qr(cap: cv2.VideoCapture, qcd: cv2.QRCodeDetector) -> [bytes, str | None, str | None]:
    """Reads the QR Code using the given QRCodeDetector from the video capture.
    If nothing is can be captured, None is returned
    :returns A frame, with any QR Codes highlighted, as well as the ID and Name gathered from the code"""
    ret, frame = cap.read()

    if not ret:
        return None

    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

    if retval:
        img = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)
        data = decoded_info[0].split('&')
    else:
        img = frame
        data = None

    h = 450
    w = 800
    x = int(len(img[0]) / 2 - w / 2)
    y = int(len(img) / 2 - h / 2)

    img = img[y:y + h, x:x + w]

    img_bytes = cv2.imencode('.png', img)[1].tobytes()

    if data and len(data) > 1:
        return img_bytes, data[0], data[1]
    else:
        return img_bytes, None, None


def mark_as_checked_in(lookup_id: str):
    row_num, row = get_row_by_id(lookup_id)

    if row_num is None:
        return

    google_sheet.set_value(F'G{row_num + 1}:G', [['Yes']])

    data = []
    with open('local_registration.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    data[row_num - 1][6] = 'Yes'
    with open('local_registration.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)

    playsound('confirmation.mp3')


def get_row_by_id(raw_id: str) -> (int | None, list[str] | None):
    with open('local_registration.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row_num, row in enumerate(reader, start=1):
            if row[0].upper() == raw_id.upper():
                return row_num, row
    return None, None


def lookup(raw_id: str, raw_name: str) -> [bool | None, [str, str, str, str]]:
    row = get_row_by_id(raw_id)[1]

    if row:
        found = row[1], row[3], row[4], row[5], row[6]
        if row[1].upper() == raw_name.upper():
            return True, found
        else:
            return False, found

    else:
        return None, None


def refresh():
    f = open('local_registration.csv', 'w')
    data = google_sheet.read_data()

    csv_string = ''

    for row in data:
        csv_string += ','.join(row) + '\n'

    f.write(csv_string)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
