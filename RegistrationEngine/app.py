import PySimpleGUI as sg

from googleapiclient.errors import HttpError

import google_sheet
import registration_email
from google_sheet import get_new_id


def main_window():
    sg.theme('DarkPurple1')
    sg.set_options(font=("Arial", 24))

    window = sg.Window('Prom Registration', [
        [sg.Text('New Registration')],
        [sg.Text('Name'), sg.In(key='-NAME-')],
        [sg.Text('Email'), sg.In(key='-EMAIL-')],
        [sg.Text('Grade'), sg.In(key='-GRADE-')],
        [sg.Checkbox('Out of District', key='-EXTERNAL-', enable_events=True),
         sg.In(tooltip='School', key='-SCHOOL-', visible=False)],
        [sg.Button('OK'), sg.Button('Clear')],
    ])

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            return

        # School option becomes visible depending on whether the "external" checkbox is selected
        window['-SCHOOL-'].update(visible=values['-EXTERNAL-'])

        if event == 'OK':
            name = values['-NAME-']
            email = values['-EMAIL-']
            grade = values['-GRADE-']
            external = values['-EXTERNAL-']
            school = values['-SCHOOL-']

            if not name:
                error('Name was not entered')
                continue

            if not email:
                error('Email was not entered')
                continue

            try:
                grade = int(grade)
            except ValueError:
                if not grade == "N/A":
                    grade = None

            if not grade:
                error('Invalid grade. Please enter a number, or "N/A" if not in school.')
                continue

            if external and not school:
                error('School was not entered')
                continue

            ticket_id = get_new_id(name)

            name = name.split()[0].capitalize() + ' ' + name.split()[1].capitalize()

            new = [ticket_id, name, email, grade, 'Yes', 'N/A', 'No']

            if external:
                new[5] = 'No'  # Sets "approved" to No instead of N/A
                new.append(school)  # Adds the school name in the end column

            print(F'Registrant generated with id: {ticket_id}, name: {name}, email: {email}')

            if registration_email.send_email(new) is None:
                error('Something went wrong when sending the email')
                continue

            if google_sheet.append_values([new]) is HttpError:
                error('Something went wrong while writing to the Google Sheet.'
                      '\nInformation may need to be entered manually')
                continue

            successful_register(new)
            event = 'Clear'

        if event == 'Clear':
            window['-NAME-'].update('')
            window['-EMAIL-'].update('')
            window['-GRADE-'].update('')
            window['-EXTERNAL-'].update(False)
            window['-SCHOOL-'].update('')
            window['-SCHOOL-'].update(visible=False)


def error(description: str = 'Something went wrong'):
    sg.Window('Error',
              [
                  [sg.Text(description)],
                  [sg.Text('Please try again')],
                  [sg.Button('OK')]
              ]
              ).read(close=True)


def successful_register(new: list[str]):
    print(F'New success: {new}')

    bold_font = 'arial 24 bold'

    event, _ = sg.Window('Success!',
                         [
                             [sg.Text('Successfully registered new attendee')],
                             [sg.Text('ID: ', font=bold_font), sg.Text(new[0])],
                             [sg.Text('Name: ', font=bold_font), sg.Text(new[1])],
                             [sg.Text('Email: ', font=bold_font), sg.Text(new[2])],
                             [sg.Text('Grade: ', font=bold_font), sg.Text(new[3])],
                             [sg.Text('Paid: ', font=bold_font), sg.Text(new[4])],
                             [sg.Text('Approved: ', font=bold_font), sg.Text(new[5])],
                             [sg.Button('OK'), sg.Button('Undo')]
                         ]).read(close=True)

    if event == 'Undo':
        _, _ = sg.Window('Unsupported',
                         [
                             [sg.Text("Sorry, but right now you can't do that here."
                                      "\nYou may need to edit the entry manually in the Google Sheet")]
                         ]
                         ).read(close=True)


if __name__ == "__main__":
    main_window()
