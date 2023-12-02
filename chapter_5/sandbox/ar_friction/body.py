import numpy as np
from numba import njit
import config


class Body:
    def __init__(self, init_dict):
        self.name = init_dict["id"]
        self.x = init_dict["x"]
        self.y = init_dict["y"]
        self.angle = 0
        self.x_atoms = init_dict["x_atoms"]
        self.y_atoms = init_dict["y_atoms"]
        self.n_atoms = self.x_atoms.size

        # If initial velocities aren't provided, initialize them to zero.
        try:
            self.v_x = init_dict["v_x"]
        except KeyError:
            self.v_x = 0
        try:
            self.v_y = init_dict["v_y"]
        except KeyError:
            self.v_y = 0
        try:
            self.v_rot = init_dict["v_rot"]
        except KeyError:
            self.v_rot = 0

        # Default to a mass of 1, if no mass is provided.
        try:
            self.m_atoms = init_dict["m_atoms"]
        except KeyError:
            self.m_atoms = np.ones(self.n_atoms)

        # Find center of gravity.
        # Adjust x's and y's to put (0, 0) at the center of gravity.
        self.m = np.sum(self.m_atoms)
        x_c = np.sum(self.x_atoms * self.m_atoms) / self.m
        y_c = np.sum(self.y_atoms * self.m_atoms) / self.m
        self.x_atoms_local = self.x_atoms - x_c
        self.y_atoms_local = self.y_atoms - y_c
        self.x_atoms = self.x_atoms_local + self.x
        self.y_atoms = self.y_atoms_local + self.y

        self.v_x_atoms = self.v_x - self.v_rot * self.y_atoms_local
        self.v_y_atoms = self.v_y + self.v_rot * self.x_atoms_local

        # Find the moment of inertia
        self.rot_inertia = np.sum(
            self.m_atoms * (self.x_atoms_local**2 + self.y_atoms_local**2)
        )

        self.r_atoms = init_dict["r_atoms"]
        self.stiffness_atoms = init_dict["stiffness_atoms"]

        # Default to a sliding friction coefficient if none is provided.
        try:
            self.sliding_friction = init_dict["sliding_friction"]
        except KeyError:
            self.sliding_friction = 0.3

        # Default to an inelasticity coefficient if none is provided.
        try:
            self.inelasticity = init_dict["inelasticity"]
        except KeyError:
            self.inelasticity = 0.2

        self.bounding_box = {}
        self.update_bounding_box()

        # If a body is free to move, it's 'free' value will be True.
        # Otherwise it will be False.
        # If the value isn't specified, assume free.
        try:
            self.free = init_dict["free"]
        except KeyError:
            self.free = True

        self.f_x_atoms = np.zeros(self.n_atoms)
        self.f_y_atoms = np.zeros(self.n_atoms)
        self.row_tile = np.ones((self.n_atoms, 1))
        self.col_tile = np.ones((1, self.n_atoms))

    def start_step(self):
        self.f_x_atoms = np.zeros(self.n_atoms)
        self.f_y_atoms = np.zeros(self.n_atoms)
        self.update_bounding_box()

    def calculate_interactions(self, body):
        # Check whether these two bodys have any chance of interaction
        # by comparing their bounding boxes.
        if self.is_close(body):
            sliding_friction = (
                self.sliding_friction + body.sliding_friction
            ) / 2
            inelasticity = (self.inelasticity + body.inelasticity) / 2

            body_interactions_numba(
                body.row_tile,
                self.col_tile,
                self.f_x_atoms,
                body.f_x_atoms,
                self.f_y_atoms,
                body.f_y_atoms,
                self.stiffness_atoms[np.newaxis, :],
                body.stiffness_atoms[:, np.newaxis],
                self.r_atoms[np.newaxis, :],
                body.r_atoms[:, np.newaxis],
                self.x_atoms[np.newaxis, :],
                body.x_atoms[:, np.newaxis],
                self.y_atoms[np.newaxis, :],
                body.y_atoms[:, np.newaxis],
                self.v_x_atoms[np.newaxis, :],
                body.v_x_atoms[:, np.newaxis],
                self.v_y_atoms[np.newaxis, :],
                body.v_y_atoms[:, np.newaxis],
                sliding_friction,
                inelasticity,
            )

    def is_close(self, body):
        bb_a = self.bounding_box
        bb_b = body.bounding_box
        overlaps = True
        if (
            bb_a["x_min"] > bb_b["x_max"]
            or bb_b["x_min"] > bb_a["x_max"]
            or bb_a["y_min"] > bb_b["y_max"]
            or bb_b["y_min"] > bb_a["y_max"]
        ):
            overlaps = False
        return overlaps

    def update_bounding_box(self):
        self.bounding_box["x_min"] = np.min(self.x_atoms - self.r_atoms)
        self.bounding_box["x_max"] = np.max(self.x_atoms + self.r_atoms)
        self.bounding_box["y_min"] = np.min(self.y_atoms - self.r_atoms)
        self.bounding_box["y_max"] = np.max(self.y_atoms + self.r_atoms)

    def calculate_wall_forces(self, walls):
        row_tile = np.ones((walls.count, 1))
        sliding_friction = (
            self.sliding_friction + walls.sliding_friction
        ) / 2
        inelasticity = (self.inelasticity + walls.inelasticity) / 2
        wall_forces_numba(
            self.col_tile,
            row_tile,
            self.f_x_atoms,
            self.f_y_atoms,
            self.stiffness_atoms[np.newaxis, :],
            self.r_atoms,
            walls.x[:, np.newaxis],
            walls.x_n,
            self.x_atoms[np.newaxis, :],
            walls.y[:, np.newaxis],
            walls.y_n,
            self.y_atoms[np.newaxis, :],
            self.v_x_atoms[np.newaxis, :],
            self.v_y_atoms[np.newaxis, :],
            sliding_friction,
            inelasticity,
        )

    def update_positions(self):
        if self.free:
            (
                self.x,
                self.y,
                self.angle,
                self.v_x,
                self.v_y,
                self.v_rot,
                self.x_atoms,
                self.y_atoms,
                self.v_x_atoms,
                self.v_y_atoms,
            ) = update_positions_numba(
                self.x_atoms_local,
                self.y_atoms_local,
                self.x_atoms,
                self.y_atoms,
                self.x,
                self.y,
                self.angle,
                self.v_x,
                self.v_y,
                self.v_rot,
                self.m,
                self.rot_inertia,
                self.f_x_atoms,
                self.f_y_atoms,
                config.CLOCK_PERIOD_SIM,
                config.SPEED_LIMIT,
            )

    def get_state(self):
        state = {
            "x": list(self.x_atoms),
            "y": list(self.y_atoms),
            "r": list(self.r_atoms),
        }
        return state


# @njit
def body_interactions_numba(
    row_tile_a,
    col_tile_b,
    f_x_a,
    f_x_b,
    f_y_a,
    f_y_b,
    k_a,
    k_b,
    r_a,
    r_b,
    x_a,
    x_b,
    y_a,
    y_b,
    v_x_a,
    v_x_b,
    v_y_a,
    v_y_b,
    sliding_friction,
    inelasticity,
):
    epsilon = 1e-12
    d_x = (row_tile_a @ x_a) - (x_b @ col_tile_b)
    d_y = (row_tile_a @ y_a) - (y_b @ col_tile_b)
    d_v_x = (row_tile_a @ v_x_a) - (v_x_b @ col_tile_b)
    d_v_y = (row_tile_a @ v_y_a) - (v_y_b @ col_tile_b)

    r_ab = (row_tile_a @ r_a) - (r_b @ col_tile_b)
    k_ab = 1 / (
        row_tile_a @ (1 / (k_a + epsilon))
        + (1 / (k_b + epsilon)) @ col_tile_b
        + epsilon
    )
    distance = (d_x**2 + d_y**2) ** 0.5 + epsilon
    compression = r_ab - distance
    compression = np.maximum(compression, 0)

    f_mag = k_ab * compression

    f_norm = f_mag / distance

    # The normal forces due to contact
    f_x_ab_contact = f_norm * d_x
    f_y_ab_contact = f_norm * d_y
    f_x_a_contact = np.sum(f_x_ab_contact, axis=0)
    f_x_b_contact = -np.sum(f_x_ab_contact, axis=1)
    f_y_a_contact = np.sum(f_y_ab_contact, axis=0)
    f_y_b_contact = -np.sum(f_y_ab_contact, axis=1)

    # Friction
    # Forces from energy dissipation due to lateral velocity
    f_x_ab_sliding = (
        -sliding_friction * np.abs(f_y_ab_contact) * np.sign(d_v_x)
    )
    f_y_ab_sliding = (
        -sliding_friction * np.abs(f_x_ab_contact) * np.sign(d_v_y)
    )
    f_x_a_sliding = np.sum(f_x_ab_sliding, axis=0)
    f_x_b_sliding = -np.sum(f_x_ab_sliding, axis=1)
    f_y_a_sliding = np.sum(f_y_ab_sliding, axis=0)
    f_y_b_sliding = -np.sum(f_y_ab_sliding, axis=1)

    # Inelasticity
    # Forces from energy dissipation due to normal velocity
    f_x_ab_inelastic = -inelasticity * f_x_ab_contact * np.sign(d_v_x)
    f_y_ab_inelastic = -inelasticity * f_y_ab_contact * np.sign(d_v_y)
    f_x_a_inelastic = np.sum(f_x_ab_inelastic, axis=0)
    f_x_b_inelastic = -np.sum(f_x_ab_inelastic, axis=1)
    f_y_a_inelastic = np.sum(f_y_ab_inelastic, axis=0)
    f_y_b_inelastic = -np.sum(f_y_ab_inelastic, axis=1)

    f_x_a += f_x_a_contact + f_x_a_sliding + f_x_a_inelastic
    f_x_b += f_x_b_contact + f_x_b_sliding + f_x_b_inelastic
    f_y_a += f_y_a_contact + f_y_a_sliding + f_y_a_inelastic
    f_y_b += f_y_b_contact + f_y_b_sliding + f_y_b_inelastic


@njit
def wall_forces_numba(
    col_tile,
    row_tile,
    f_x,
    f_y,
    stiffness_atoms,
    r_atoms,
    x_wall_col,
    x_n_wall,
    x_atoms_row,
    y_wall_col,
    y_n_wall,
    y_atoms_row,
    v_x_atoms,
    v_y_atoms,
    sliding_friction,
    inelasticity,
):
    """
    Taken from
    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    and modfied to the form
    d = (x - x1) * x_normal + (y - y1) * y_normal
    where (x1, y1) is any point on the line.

    This is a signed distance.
    A positive value indicates distance away from the wall.
    A negative value indicates distance *into* the wall.
    """
    dx = (row_tile @ x_atoms_row) - (x_wall_col @ col_tile)
    dy = (row_tile @ y_atoms_row) - (y_wall_col @ col_tile)

    dx_n = dx * x_n_wall
    dy_n = dy * y_n_wall
    # Negative distance indicates that the center of the disc
    # is inside the wall.
    distance = dx_n + dy_n
    compression = r_atoms - distance
    compression = np.maximum(compression, 0)

    f_total = stiffness_atoms * compression

    # Find the x- and y-components of the total force
    # with calculated sin (y_n / |dist|)
    # and cos (x_n / |dist|) terms.
    # Add a small nonzero term for numerical stability.
    epsilon = 1e-6
    f_x_walls_contact = f_total * x_n_wall / (np.abs(distance) + epsilon)
    f_y_walls_contact = f_total * y_n_wall / (np.abs(distance) + epsilon)
    f_x_contact = np.sum(f_x_walls_contact, axis=0)
    f_y_contact = np.sum(f_y_walls_contact, axis=0)

    # Friction
    # Forces from energy dissipation due to lateral velocity
    f_x_walls_sliding = (
        -sliding_friction * np.abs(f_y_walls_contact) * np.sign(v_x_atoms)
    )
    f_y_walls_sliding = (
        -sliding_friction * np.abs(f_x_walls_contact) * np.sign(v_y_atoms)
    )
    f_x_sliding = np.sum(f_x_walls_sliding, axis=0)
    f_y_sliding = np.sum(f_y_walls_sliding, axis=0)

    # Inelasticity
    # Forces from energy dissipation due to normal velocity
    f_x_walls_inelastic = (
        -inelasticity * f_x_walls_contact * np.sign(v_x_atoms)
        * np.sign(x_n_wall)
    )
    f_y_walls_inelastic = (
        -inelasticity * f_y_walls_contact * np.sign(v_y_atoms)
        * np.sign(y_n_wall)
    )
    f_x_inelastic = np.sum(f_x_walls_inelastic, axis=0)
    f_y_inelastic = np.sum(f_y_walls_inelastic, axis=0)

    f_x += f_x_contact + f_x_sliding + f_x_inelastic
    f_y += f_y_contact + f_y_sliding + f_y_inelastic


@njit
def update_positions_numba(
    x_atoms_local,
    y_atoms_local,
    x_atoms,
    y_atoms,
    x,
    y,
    angle,
    v_x,
    v_y,
    v_rot,
    m,
    rot_inertia,
    f_x_atoms,
    f_y_atoms,
    CLOCK_PERIOD_SIM,
    SPEED_LIMIT,
):
    f_x = np.sum(f_x_atoms)
    f_y = np.sum(f_y_atoms)
    torque = np.sum(f_y_atoms * (x_atoms - x)) - np.sum(
        f_x_atoms * (y_atoms - y)
    )

    a_x = f_x / m
    a_y = f_y / m
    a_rot = torque / rot_inertia

    v_x += CLOCK_PERIOD_SIM * a_x
    v_y += CLOCK_PERIOD_SIM * a_y
    v_rot += CLOCK_PERIOD_SIM * a_rot
    # For numerical stability, put a speed limit on movement.
    # v_x = np.sign(v_x) * (1 - np.exp( -np.abs(v_x) / SPEED_LIMIT))
    # v_y = np.sign(v_y) * (1 - np.exp( -np.abs(v_y) / SPEED_LIMIT))

    x += CLOCK_PERIOD_SIM * v_x
    y += CLOCK_PERIOD_SIM * v_y
    angle += CLOCK_PERIOD_SIM * v_rot

    x_atoms_rel = x_atoms_local * np.cos(angle) - y_atoms_local * np.sin(angle)
    y_atoms_rel = y_atoms_local * np.cos(angle) + x_atoms_local * np.sin(angle)
    v_x_atoms_rel = -v_rot * y_atoms_rel
    v_y_atoms_rel = v_rot * x_atoms_rel
    x_atoms = x + x_atoms_rel
    y_atoms = y + y_atoms_rel
    v_x_atoms = v_x + v_x_atoms_rel
    v_y_atoms = v_y + v_y_atoms_rel

    return x, y, angle, v_x, v_y, v_rot, x_atoms, y_atoms, v_x_atoms, v_y_atoms
