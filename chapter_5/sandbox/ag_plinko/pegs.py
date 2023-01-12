import numpy as np
import config


def create_pegs():

    pegs = []
    for i_row in range(config.N_PEG_ROWS):
        peg_y = (
            config.PEG_BOTTOM_SPACING
            + (2 * i_row + 1) * config.PEG_RADIUS
            + i_row * config.PEG_ROW_SPACING
        )
        # Half-column shift every other row
        shift = (
            (i_row % 2) * (config.PEG_COL_SPACING + 2 * config.PEG_RADIUS) / 2
        )
        for i_col in range(config.N_PEG_COLS):

            peg_x = (
                shift
                + config.PEG_EDGE_SPACING
                + (2 * i_col + 1) * config.PEG_RADIUS
                + i_col * config.PEG_COL_SPACING
            )
            pegs.append(Peg(peg_x, peg_y, config.PEG_RADIUS))

    return pegs


def get_state(pegs):
    pegs_state = {}
    for i_peg, peg in enumerate(pegs):
        pegs_state[f"peg_{i_peg}"] = peg.get_state()
    return pegs_state


class Peg:
    def __init__(
        self,
        x=0,
        y=0,
        radius=1,
    ):
        self.x = x
        self.y = y
        self.radius = radius

        self.fx = 0
        self.fy = 0

    def get_state(self):
        return {"x": self.x, "y": self.y, "fx": self.fx, "fy": self.fy}

    def calculate_collision_forces(self, puck):
        self.fx = 0
        self.fy = 0

        distance = ((self.x - puck.x) ** 2 + (self.y - puck.y) ** 2) ** 0.5
        compression = puck.radius + self.radius - distance
        if compression > 0:
            f_mag = puck.stiffness * compression
            angle_of_action = np.arctan2(self.y - puck.y, self.x - puck.x)
            self.fx = f_mag * np.cos(angle_of_action)
            self.fy = f_mag * np.sin(angle_of_action)
            # print(angle_of_action * 180 / 3.1415922)

        # Return the forces that the peg exerts on the puck
        return (-self.fx, -self.fy)
