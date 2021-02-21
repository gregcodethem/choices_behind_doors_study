import csv
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.core import serializers

from django.contrib.auth.models import User

from doorgame.models import SurveyAnswers

from extract import write_to_csv, results


def dots_remembered(number_of_trials=30):
    easy_grid = []
    hard_grid = []
    very_hard_grid = []
    user_list = User.objects.all()

    column_headings = ['']
    for i in range(number_of_trials):
        column_headings.append(i + 1)

    easy_grid.append(column_headings)
    hard_grid.append(column_headings)
    very_hard_grid.append(column_headings)

    for user in user_list:
        username = user.username

        try:
            user_result_list_of_dics = results(username, row_format='dic')
            
            hard_or_easy_setting = user_result_list_of_dics[0]['hard_or_easy']
            user_result = []
            user_result.append(username)

            for user_trial_result_dic in user_result_list_of_dics:
                number_of_dots_correct = user_trial_result_dic['number_of_dots_correct']
                user_result.append(number_of_dots_correct)
            if hard_or_easy_setting == 'hard':
                hard_grid.append(user_result)
            elif hard_or_easy_setting == 'easy':
                easy_grid.append(user_result)
            elif hard_or_easy_setting == 'very_hard':
                very_hard_gid.append(user_result)
            else:
                print(f'hard_or_easy_setting not defined correctly in extract_all.py')

        except Exception as e:
            print(f'not worked for user: {username}')
            print(e)
    grid_dic = {
        'hard_grid': hard_grid,
        'easy_grid': easy_grid,
        'very_hard_grid': very_hard_grid
    }
    return grid_dic

def door_result(number_of_trials=30):
    easy_grid = []
    hard_grid = []
    very_hard_grid = []
    user_list = User.objects.all()

    column_headings = ['']
    for i in range(number_of_trials):
        column_headings.append(i + 1)

    easy_grid.append(column_headings)
    hard_grid.append(column_headings)
    very_hard_grid.append(column_headings)

    for user in user_list:
        username = user.username

        try:
            user_result_list_of_dics = results(username, row_format='dic')
            
            hard_or_easy_setting = user_result_list_of_dics[0]['hard_or_easy']
            user_result = []
            user_result.append(username)

            for user_trial_result_dic in user_result_list_of_dics:
                switch_or_stick = user_trial_result_dic['switch_or_stick']
                win_or_lose = user_trial_result_dic['win_or_lose']
                trial_result = switch_or_stick + '-' + win_or_lose
                user_result.append(trial_result)
            if hard_or_easy_setting == 'hard':
                hard_grid.append(user_result)
            elif hard_or_easy_setting == 'easy':
                easy_grid.append(user_result)
            elif hard_or_easy_setting == 'very_hard':
                very_hard_grid.append(user_result)
            else:
                print(f'hard_or_easy_setting not defined correctly in extract_all.py door_result method')

        except Exception as e:
            print(f'not worked for user: {username}')
            print(e)


    grid_dic = {
        'hard_grid': hard_grid,
        'easy_grid': easy_grid,
        'very_hard_grid': very_hard_grid
    }
    return grid_dic

def other_data():
    grid = []
    user_list = User.objects.all()
    for user in user_list:
        username = user.username

        SurveyAnswersForUser = SurveyAnswers.objects.filter(user=user)

        #user_data = 





def write_to_csv_summary(grid_input, easy_or_hard, type_of_grid):
    result_table = grid_input

    with open('csv_results/' + easy_or_hard + '_' + type_of_grid + '.csv', mode='w') as result_file:
        result_writer = csv.writer(
            result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in result_table:
            result_writer.writerow(row)

def write_all_to_csv():
    user_list = User.objects.all()
    for user in user_list:
        username = user.username
        try:
            write_to_csv(username)
        except:
            print(f'not worked for user: {username}')


if __name__ == "__main__":
    # execute only if run as a script

    # write_all_to_csv()
    dots_remembered_result = dots_remembered()
    easy_grid_dots = dots_remembered_result['easy_grid']
    hard_grid_dots = dots_remembered_result['hard_grid']
    very_hard_grid_dots = dots_remembered_result['very_hard_grid']
    write_to_csv_summary(easy_grid_dots, 'easy', 'dots_remembered')
    write_to_csv_summary(hard_grid_dots, 'hard', 'dots_remembered')
    write_to_csv_summary(very_hard_grid_dots, 'very_hard', 'dots_remembered')

    door_result = door_result()
    easy_grid_door = door_result['easy_grid']
    hard_grid_door = door_result['hard_grid']
    very_hard_grid_door = door_result['very_hard_grid']
    write_to_csv_summary(easy_grid_door, 'easy', 'door_strategy')
    write_to_csv_summary(hard_grid_door, 'hard', 'door_strategy')
    write_to_csv_summary(very_hard_grid_door, 'very_hard', 'door_strategy')

