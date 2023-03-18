# calendar api: https://developers.google.com/calendar/api/v3/reference?hl=ko


def insert_event(calendar, schedules: list[dict]):

    old_calendars: list = calendar.calendarList().list().execute()['items']
    # if old_calendars:
    old_gookseon = [
        item for item in old_calendars if item['summary'] == '국선']
    for item in old_gookseon:
        calendar.calendars().delete(calendarId=item['id']).execute()

    new_calendar = calendar.calendars().insert(body={
        'summary': '국선',
        'timeZone': 'Asia/Seoul',
    }).execute()

    for i in range(len(schedules)):

        courtroom = schedules[i]['courtroom'] if 'courtroom' in schedules[i] else ''
        if '기일' in schedules[i]['content']:
            summary = courtroom + schedules[i]['content']
        else:
            summary = schedules[i]['content'] + courtroom
        # 'date': '2023-03-23',
        # 'time': '15:30',
        if schedules[i]['time'] == '종일':
            event_date_time = {'date': schedules[i]['date']}
        else:
            event_date_time = {'dateTime':
                               schedules[i]['date'] + 'T' +
                               schedules[i]['time'] + ':00'
                               }

        event_date_time['timeZone'] = 'Asia/Seoul'
        event = {
            'summary': summary,
            'start': event_date_time,
            'end': event_date_time,
        }
        event = calendar.events().insert(
            calendarId=new_calendar['id'], body=event,
        ).execute()
