from bosses.Stage_1_Boss import Stage1Boss
from bosses.Stage_2_Boss import Stage2Boss

def initialize_boss(level):
    bosses = {
        1: Stage1Boss,
        2: Stage2Boss,
        # 3: Stage3Boss,
    }
    return bosses.get(level, lambda: None)()