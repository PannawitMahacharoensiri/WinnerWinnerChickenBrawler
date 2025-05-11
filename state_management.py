

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

    def update(self, frame, ms_per_loop, event_object):
        self.current_state.update_state(frame, ms_per_loop, event_object)

    def draw(self, screen, event_object):
        self.current_state.draw_state(screen, event_object)

    def resize(self):
        for each_state in self.states.values():
            each_state.asset_update()


class OverlayManage:

    def __init__(self):
        self.overlays = []
        self.block_update = False

    def add_overlay(self, overlay):
        self.overlays.append(overlay)

    def remove_overlay(self, overlay):
        # print(overlay)
        if overlay in self.overlays:
            self.overlays.remove(overlay)

    def check_overlay_type(self):
        if len(self.overlays) != 0:
            for each in self.overlays:
                if each.blocker is True:
                    self.block_update = True
                else :
                    self.block_update = False
        else:
            self.block_update = False

    def update(self, ms_per_loop):
        self.check_overlay_type()
        if self.block_update is True:
            for each_overlay in self.overlays:
                if each_overlay.blocker is True:
                    each_overlay.update_overlay(ms_per_loop)
        else :
            for each_overlay in self.overlays:
                each_overlay.update_overlay(ms_per_loop)

    def draw(self, screen):
        for each_overlay in self.overlays:
            each_overlay.draw_overlay(screen)