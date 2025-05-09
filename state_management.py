

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
            each_state.update_asset()


class OverlayManage:

    def __init__(self):
        self.overlays = []
        self.block_update = False

    def add_overlay(self, overlay):
        self.overlays.append(overlay)

    def remove_overlay(self, overlay):
        if overlay in self.overlays:
            self.overlays.remove(overlay)

    def check_overlay_type(self):
        if len(self.overlays) != 0:
            for each in self.overlays:
                if each.freeze is True:
                    self.block_update = True
                else :
                    self.block_update = False

    def update(self):
        self.check_overlay_type()

    def draw(self):
        pass