import os
import random
import django
import argparse


PHRASES = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


from datacenter.models import Schoolkid, Subject, Lesson, Mark, Chastisement, Commendation


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    all_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    return all_chastisements.delete()        


def create_commendation(schoolkid, subject):
    lesson_in_schedule = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study, 
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject
    ).order_by('-date').first()
    add_new_commendation = Commendation.objects.create(
        schoolkid=schoolkid,
        subject=lesson_in_schedule.subject,
        teacher=lesson_in_schedule.teacher,
        created=lesson_in_schedule.date,
        text=random.choice(PHRASES)
    )
    return add_new_commendation


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Исправление оценок, удаление замечаний и добавление похвалы от учителя по ученику')
    parser.add_argument('name', type=str, help="Необходимо ввести фамилию и имя ученика (например, 'Фролов Иван')")
    parser.add_argument('subject', type=str, help="Необходимо ввести название предмета (например, 'Математика')")
    args = parser.parse_args()

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=args.name)
    except Schoolkid.DoesNotExist:
        print("Ученик не найден!")
        exit()
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с таким именем!")
        exit()

    try:
        subject = Subject.objects.get(
            title=args.subject, 
            year_of_study=schoolkid.year_of_study
        )
    except Subject.DoesNotExist:
        print(f"Предмет не найден!")
        exit()


    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject.title)