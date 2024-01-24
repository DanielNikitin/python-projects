def analyze_player_health(player_data):
    hp_data = {'hp_data': str(player_data.hp)}  # player hp data for HUD

    # Player HP check
    if player_data.hp <= 0:
        hp_data = {'hp_data': 'YOU DIED'}
        player_data.status = 'died'
        player_data.vel = 0
        # остальные действия

    return hp_data
