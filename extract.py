import sys
import csv

from django.contrib.auth.models import User

from doorgame.models import Trial, Choice, MemoryGame, Result

from doorgame.utils import number_of_dots_correct_calculator, number_of_dots_selected_calculator


def results(username):
    user = User.objects.get(username=username)
    trials = Trial.objects.filter(user=user)
    result_table = []

    for trial in trials:
        result_row = []

        number_of_trial = trial.number_of_trial
        if number_of_trial == 0:
            continue

        choices = Choice.objects.filter(trial=trial)
        first_choice_object = choices.get(first_or_second_choice=1)
        first_choice = first_choice_object.door_number
        second_choice_object = choices.get(first_or_second_choice=2)
        second_choice = second_choice_object.door_number
        result_object = Result.objects.get(trial=trial)
        result = result_object.door_number
        if first_choice == second_choice:
            switch_or_stick = 'stick'
        else:
            switch_or_stick = 'switch'
        if second_choice == result:
            win_or_lose = 'win'
        else:
            win_or_lose = 'lose'

        # memory game
        memory_games = MemoryGame.objects.filter(trial=trial)

        memory_game_initial = memory_games.get(initial_or_final='initial')
        memory_game_final_list = memory_games.filter(initial_or_final='final')
        if len(memory_game_final_list) != 0:
            memory_game_final = memory_games.get(initial_or_final='final')
            number_of_dots_correct = number_of_dots_correct_calculator(
                memory_game_initial, memory_game_final
            )
            number_of_dots_selected = number_of_dots_selected_calculator(
                memory_game_final
            )
        else:
            number_of_dots_selected = ""

        hard_or_easy = user.profile.hard_or_easy_dots

        result_row.append(number_of_trial)
        result_row.append(switch_or_stick)
        result_row.append(win_or_lose)
        result_row.append(hard_or_easy)
        result_row.append(number_of_dots_correct)
        result_row.append(number_of_dots_selected)
        result_table.append(result_row)

    return result_table


def write_to_csv(username):
    result_table = results(username)

    with open('csv_results/' + username + '_result.csv', mode='w') as result_file:
        result_writer = csv.writer(
            result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in result_table:
            result_writer.writerow(row)

def write_all_to_csv():
    user_list = User.objects.all()
    for user in user_list:
        username = user.username
        write_to_csv(username)


if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print(results(username))
    else:
        print("you haven't supplied a username")
    results()
