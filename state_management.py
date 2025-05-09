

class GameStateManage:

    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None

    def register_state(self, state_name, state_object):
        self.states[state_name] = state_object

    def set_state(self, name, level=0):
        if self.current_state is not None:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter(level)

    def update(self, frame, event_object):
        self.current_state.update_state(frame, event_object)

    def draw(self, screen, frame, event_object):
        self.current_state.draw_state(screen, frame, event_object)

    def resize(self):
        for each_state in self.states.values():
            each_state.load_assert()
            if len(each_state.button_list) != 0:
                for each_button in each_state.button_list:
                    each_button.widget_setting()