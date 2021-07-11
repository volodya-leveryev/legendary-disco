from datetime import datetime
import json

from mongoengine import connect

from jimmy.models import Department, Person, StudentGroup


def convert(f1, f2):
    with open(f1) as f:
        obj = json.load(f)
    with open(f2, mode='w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=True)


def remove_persons_without_id():
    to_remove = []
    for p in Person.objects.all():
        if not p.person_id:
            to_remove.append(p)
    for p in to_remove:
        p.delete()


def load_data(filename):
    data = {}
    with open(f'./{filename}') as f:
        obj_list = json.load(f)
        for obj in obj_list:
            model = obj['model']
            data.setdefault(model, {})
            data[model][obj['pk']] = obj['fields']
    return data


def load_teachers(auth_data, umo_data):
    teachers = umo_data['umo.teacher']
    persons = umo_data['umo.person']
    users = auth_data['auth.user']

    new_positions = {
        1: 'ст.пр.',
        2: 'зав.каф.',
        3: 'нач.',
        4: 'доц.',
        5: 'проф.',
        6: 'асс.',
        7: 'доц.-исс.',
        8: 'зав.лаб.',
        9: 'зам.дир.',
    }

    new_departments = {}
    for d in Department.objects.all():
        new_departments[d.depart_id] = d

    new_persons = {}
    for p in Person.objects.all():
        new_persons[p.person_id] = p

    for key, t in teachers.items():
        if key in new_persons:
            new_person = new_persons[key]
        else:
            new_person = Person()

        p = persons[key]

        if p['last_name'] and p['first_name']:
            new_person.last_name = p['last_name']
            new_person.first_name = p['first_name']
            new_person.second_name = p['second_name']
            new_person.maiden_name = p['maiden_name']
        else:
            fio = p['FIO'].strip()
            new_person.last_name, fio = fio.split(maxsplit=1)
            if ' ' in fio:
                new_person.first_name, fio = fio.split(maxsplit=1)
                new_person.second_name = fio
            else:
                new_person.first_name = fio

        new_person.person_id = key
        new_person.is_user = False
        new_person.is_admin = False
        if p['user'] and p['user'] in users:
            u = users[p['user']]
            if u['email'] and u['email'] not in new_person.emails:
                new_person.emails.append(u['email'])
            new_person.user_id = p['user']
            new_person.is_user = u['is_active']
            new_person.is_admin = u['is_superuser'] or u['is_staff']

        if t['title'] > 0:
            if not new_person.title_history:
                title = Person.Title()
                title.date = datetime(2020, 1, 1)
                title.title = 'доц.' if t['title'] == 1 else 'проф.'
                new_person.title_history.append(title)

        if t['position'] > 0:
            if t['cathedra'] not in new_departments:
                continue
            if t['position'] not in new_positions:
                continue
            if not new_person.job_history:
                job = Person.Job()
                job.date = datetime(2020, 1, 1)
                job.department = new_departments[t['cathedra']].id
                job.position = new_positions[t['position']]
                job.wage_rate = 1.0
                job.is_active = True
                new_person.job_history.append(job)

        new_person.save()


def load_students(auth_data, umo_data):
    students = umo_data['umo.student']
    persons = umo_data['umo.person']
    users = auth_data['auth.user']

    new_persons = {}
    for p in Person.objects.all():
        new_persons[p.person_id] = p

    for key, s in students.items():
        if key in new_persons:
            new_person = new_persons[key]
        else:
            new_person = Person()

        p = persons[key]

        if p['last_name'] and p['first_name']:
            new_person.last_name = p['last_name']
            new_person.first_name = p['first_name']
            new_person.second_name = p['second_name']
            new_person.maiden_name = p['maiden_name']
        else:
            fio = p['FIO'].strip()
            new_person.last_name, fio = fio.split(maxsplit=1)
            if ' ' in fio:
                new_person.first_name, fio = fio.split(maxsplit=1)
                new_person.second_name = fio
            else:
                new_person.first_name = fio

        new_person.person_id = key
        new_person.is_user = False
        new_person.is_admin = False
        if p['user'] and p['user'] in users:
            u = users[p['user']]
            if u['email'] and u['email'] not in new_person.emails:
                new_person.emails.append(u['email'])
            new_person.user_id = p['user']
            new_person.is_user = u['is_active']
            new_person.is_admin = u['is_superuser'] or u['is_staff']

        new_person.save()


def load_groups(umo_data):
    year = {
        1: 2014,
        4: 2015,
        5: 2016,
        6: 2017,
        2: 2018,
        3: 2019,
        7: 2020,
        8: 2021,
    }

    programs = umo_data['umo.eduprogram']
    specials = umo_data['umo.specialization']
    profiles = umo_data['umo.profile']
    groups = umo_data['umo.group']

    new_groups = {}
    for sg in StudentGroup.objects.all():
        new_groups[sg.group_id] = sg

    for key, g in groups.items():
        if not g['program']:
            continue

        p = programs[g['program']]
        s = specials[p['specialization']]
        p2 = profiles[p['profile']]

        if key in new_groups:
            new_group = new_groups[key]
        else:
            new_group = StudentGroup()

        new_group.name = g['Name']
        new_group.year = year[g['begin_year']]
        new_group.program_code = s['code']
        new_group.program_name = s['name']
        new_group.program_specialty = p2['name']
        new_group.level = 'Бак' if s['level'] else 'Маг'
        new_group.group_id = key

        new_group.save()


def main():
    _client = connect('jimmy')
    auth_data = load_data('2021-07-02-auth.json')
    umo_data = load_data('2021-07-02-umo.json')
    # load_teachers(auth_data, umo_data)
    # load_students(auth_data, umo_data)
    load_groups(umo_data)


if __name__ == '__main__':
    main()
