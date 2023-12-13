players_list = {}

# Пополнение на +1
player_id = len(players_list) + 5
new_player_data = {'name': 'Новый игрок', 'score': 0}

players_list[player_id] = new_player_data

print(players_list)
