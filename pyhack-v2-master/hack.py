import pymem, time, c_process, offsets, c_features, config


def main():
    try:
        print("started")
        process = c_process.c_process()
        print(f"client_panorama address {process.client_panorama.lpBaseOfDll}")
        offsets.client_panorama = process.client_panorama.lpBaseOfDll
        print(f"engine address {process.engine.lpBaseOfDll}")
        offsets.engine = process.engine.lpBaseOfDll

        # Замените ввод данных на фиксированные значения
        cooldown = "1000"
        config.force_radar = "1"
        config.no_flash = "1"
        config.glow = "1"
        config.auto_bunnyhop = "1"
        config.glow_color[0] = "0.5"
        config.glow_color[1] = "0.5"
        config.glow_color[2] = "0.5"
        config.glow_color[3] = "0.7"

        features = c_features.c_features(process.process)

        while True:
            if features.local_player:
                features.run()
                print("features.run")

            time.sleep(int(cooldown) / 1000)
    except:
        print("mamsmams")


main()
