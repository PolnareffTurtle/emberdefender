from scripts.utils import Text

def texts(surf,context,level=None):
    if context == 'level_select':
        Text('[ESC]', 10, 'white', surf, (10, 10))
        Text('1   2   3   4   5', 15, '#EF8933', surf, (40, 30))
        Text('6   7   8   9   10', 15, '#EF8933', surf, (40, 70))
        Text('11  12  13  14  15', 15, '#EF8933', surf, (40, 110))
        Text('16  17  18  19  20', 15, '#EF8933', surf, (40, 150))

    elif context == 'main_menu':
        Text('Ember Defender!', 15, '#EF8933', surf, (22, 22)),
        Text('Ember Defender!', 15, (255, 255, 255), surf, (20, 20)),
        Text('Play', 15, '#EF8933', surf, (220, 80)),
        Text('Levels', 15, '#EF8933', surf, (220, 120)),
        Text('Options', 15, '#EF8933', surf, (220, 160))
        Text('Use Arrow Keys + [ENTER] to select',5,'#EF8933',surf,(40,220))


    elif context == 'game_menu':
        Text('[ESC]', 10, 'white', surf, (10, 10))
        Text('Level ' + str(level), 15, 'white', surf, (106, 30))
        Text('Press [SPACE] to continue', 10, 'white', surf, (80, 200))
        if level == 1:
            Text('sample description.',15,'white',surf,(30,70))
            Text('do whatever you want', 15, 'white', surf, (30, 100))
            Text('with this text.', 15, 'white', surf, (30, 130))