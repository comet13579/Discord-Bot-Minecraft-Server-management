def playercount_string(log_string, enableChinese):
    outputstringlist = []
    if log_string == "0":
        outputstringlist.append("No players online")
        if enableChinese:
            outputstringlist.append("目前沒有玩家在線上")
        return outputstringlist
    start_index = log_string.find("There are")
    if start_index != -1:
    # Find the position of "players online:"
        start_index = start_index + len("There are")
        end_index = log_string.find("players online:", start_index)
    if end_index != -1:
        # Extract player count
        count_str = log_string[start_index:end_index].strip()
        player_count = int(count_str.split()[0])

        # Find the position of ": " after "players online:"
        start_index = end_index + len("players online: ")
        # Find the position of "\n" after player names
        end_index = log_string.find("\n", start_index)
        if end_index != -1:
            # Extract player names
            player_names_str = log_string[start_index:end_index].strip()
            player_names = player_names_str.split(", ")
            
            # Print player count and player names
            outputstringlist.append(f"There are {player_count} players online: ")
            if enableChinese:
                outputstringlist.append(f"目前有{player_count}名玩家在線上: ")
                outputstringlist.append(player_names_str)
    return outputstringlist

if __name__ == "__main__":
    log_string = '2024-06-30 00:57:19 - Command: list\nResponse: J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00There are 2 of a max of 20 players online: Hashed_Ice, moyinQAQ\n\x00\x00'
    outputstringlist = playercount_string(log_string, True)
    print(outputstringlist)