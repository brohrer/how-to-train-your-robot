import math
import numpy as np
from numba import njit
import config


class Body:
    def __init__(self, init_dict):
        self.type = init_dict["type"]
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
        stiffness = init_dict["stiffness_atoms"]
        if isinstance(stiffness, float) or isinstance(stiffness, int):
            self.stiffness_atoms = stiffness * np.ones(self.x_atoms.size)
        else:
            self.stiffness_atoms = stiffness

        # Find the object radius, the greatest distance from the
        # center of gravity to that end of an atom.
        atom_distance = np.sqrt(
            self.x_atoms_local**2 + self.y_atoms_local**2
        )
        atom_edge = atom_distance + self.r_atoms
        self.radius = np.max(atom_edge)

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

        # If a body is free to move, it's 'free' value will be True.
        # Otherwise it will be False.
        # If the value isn't specified, assume free.
        try:
            self.free = init_dict["free"]
        except KeyError:
            self.free = True

        self.f_x_atoms = np.zeros(self.n_atoms)
        self.f_y_atoms = np.zeros(self.n_atoms)

        # Create one second buffers for forces on the body.
        # self.f_x_ext_buffer = RingBuffer(config.CLOCK_FREQ_SIM)
        # self.f_y_ext_buffer = RingBuffer(config.CLOCK_FREQ_SIM)
        # self.torque_ext_buffer = RingBuffer(config.CLOCK_FREQ_SIM)

    def start_step(self):
        self.f_x_atoms = np.zeros(self.n_atoms)
        self.f_y_atoms = np.zeros(self.n_atoms)

        # Create one second buffers for forces on the body.
        self.f_x_ext = 0
        self.f_y_ext = 0
        self.torque_ext = 0

    def calculate_interactions(self, body):
        sliding_friction = (self.sliding_friction + body.sliding_friction) / 2
        inelasticity = (self.inelasticity + body.inelasticity) / 2

        body_interactions_numba(
            self.f_x_atoms,
            body.f_x_atoms,
            self.f_y_atoms,
            body.f_y_atoms,
            self.stiffness_atoms,
            body.stiffness_atoms,
            self.r_atoms,
            body.r_atoms,
            self.x_atoms,
            body.x_atoms,
            self.y_atoms,
            body.y_atoms,
            self.v_x_atoms,
            body.v_x_atoms,
            self.v_y_atoms,
            body.v_y_atoms,
            sliding_friction,
            inelasticity,
        )

    def calculate_wall_forces(self, walls):
        sliding_friction = (self.sliding_friction + walls.sliding_friction) / 2
        inelasticity = (self.inelasticity + walls.inelasticity) / 2
        wall_forces_numba(
            self.f_x_atoms,
            self.f_y_atoms,
            self.stiffness_atoms,
            self.r_atoms,
            walls.x,
            walls.x_n,
            self.x_atoms,
            walls.y,
            walls.y_n,
            self.y_atoms,
            self.v_x_atoms,
            self.v_y_atoms,
            sliding_friction,
            inelasticity,
        )

    def update_positions(self):
        # f_x_ext = self.f_x_ext_buffer.pop()
        # f_y_ext = self.f_y_ext_buffer.pop() + config.GRAVITY * self.m
        # torque_ext = self.torque_ext_buffer.pop()

        if self.free:
            (
                self.x,
                self.y,
                self.angle,
                self.v_x,
                self.v_y,
                self.v_rot,
            ) = update_positions_numba(
                self.x_atoms_local,
                self.y_atoms_local,
                self.x_atoms,
                self.y_atoms,
                self.v_x_atoms,
                self.v_y_atoms,
                self.f_x_atoms,
                self.f_y_atoms,
                self.x,
                self.y,
                self.angle,
                self.v_x,
                self.v_y,
                self.v_rot,
                self.m,
                self.rot_inertia,
                self.f_x_ext,
                self.f_y_ext,
                self.torque_ext,
                config.CLOCK_PERIOD_SIM,
            )

    def get_state(self):
        viz_info = {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "type": self.type,
        }
        return viz_info


@njit
def body_interactions_numba(
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

    for i_row in range(x_a.size):
        for j_col in range(x_b.size):
            d_x = x_a[i_row] - x_b[j_col]
            d_y = y_a[i_row] - y_b[j_col]

            d_v_x = v_x_a[i_row] - v_x_b[j_col]
            d_v_y = v_y_a[i_row] - v_y_b[j_col]

            r_ab = r_a[i_row] + r_b[j_col]
            k_ab = 1 / (
                (1 / (k_a[i_row] + epsilon)) + (1 / (k_b[j_col] + epsilon))
            )
            distance = (d_x**2 + d_y**2) ** 0.5 + epsilon
            compression = r_ab - distance
            # Negative distance indicates that the center of the disc
            # is inside the wall.
            compression = max(0, compression)

            f_ab_contact = k_ab * compression

            # Breaking the contact forces into their x- and y-components
            # requires multiplying them by the sin and cos of the angle
            # of the line of connecting the centers of the two:
            # sin(angle) = d_y / distance
            # cos(angle) = d_x / distance
            #
            # All together it looks like this
            # f_x_ab_contact = f_ab_contact * d_x / distance
            # f_y_ab_contact = f_ab_contact * d_y / distance
            #
            # To save an extra element-wise division operation, this is broken
            # out here into two steps.
            # First, f_ab_contact is divided by distance,
            # then it is multiplied by d_x and d_y separately.
            f_norm = f_ab_contact / distance

            # The normal forces due to contact
            f_x_ab_contact = f_norm * d_x
            f_y_ab_contact = f_norm * d_y

            # Aggregate to sum the forces of all other atoms
            # on each one individualy.
            f_x_a[i_row] += f_x_ab_contact
            f_x_b[j_col] -= f_x_ab_contact
            f_y_a[i_row] += f_y_ab_contact
            f_y_b[j_col] -= f_y_ab_contact

            # Friction
            # Forces from energy dissipation due to lateral velocity
            f_x_ab_sliding = (
                -sliding_friction * np.abs(f_y_ab_contact) * np.sign(d_v_x)
            )
            f_y_ab_sliding = (
                -sliding_friction * np.abs(f_x_ab_contact) * np.sign(d_v_y)
            )
            f_x_a[i_row] += f_x_ab_sliding
            f_x_b[j_col] -= f_x_ab_sliding
            f_y_a[i_row] += f_y_ab_sliding
            f_y_b[j_col] -= f_y_ab_sliding

            # Inelasticity
            # Forces from energy dissipation due to normal velocity
            f_x_ab_inelastic = -inelasticity * f_x_ab_contact * np.sign(d_v_x)
            f_y_ab_inelastic = -inelasticity * f_y_ab_contact * np.sign(d_v_y)
            f_x_a[i_row] += f_x_ab_inelastic
            f_x_b[j_col] -= f_x_ab_inelastic
            f_y_a[i_row] += f_y_ab_inelastic
            f_y_b[j_col] -= f_y_ab_inelastic


@njit
def wall_forces_numba(
    f_x,
    f_y,
    stiffness_atoms,
    r_atoms,
    x_wall,
    x_n_wall,
    x_atoms,
    y_wall,
    y_n_wall,
    y_atoms,
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
    # i_wall is also i_row
    for i_wall in range(x_wall.size):
        # j_atom is also j_col
        for j_atom in range(x_atoms.size):
            d_x = x_atoms[j_atom] - x_wall[i_wall]
            d_y = y_atoms[j_atom] - y_wall[i_wall]

            dx_n = d_x * x_n_wall[i_wall]
            dy_n = d_y * y_n_wall[i_wall]
            # Negative distance indicates that the center of the disc
            # is inside the wall.
            distance = dx_n + dy_n
            compression = r_atoms[j_atom] - distance
            compression = max(compression, 0.0)

            f_total = stiffness_atoms[j_atom] * compression

            # Find the x- and y-components of the total force
            # with calculated sin (y_n / 1)
            # and cos (x_n / 1) terms.
            f_x_wall_contact = f_total * x_n_wall[i_wall]
            f_y_wall_contact = f_total * y_n_wall[i_wall]
            f_x[j_atom] += f_x_wall_contact
            f_y[j_atom] += f_y_wall_contact

            # Friction
            # Forces from energy dissipation due to lateral velocity
            f_x_wall_sliding = (
                -sliding_friction
                * np.abs(f_y_wall_contact)
                * np.sign(v_x_atoms[j_atom])
            )
            f_y_wall_sliding = (
                -sliding_friction
                * np.abs(f_x_wall_contact)
                * np.sign(v_y_atoms[j_atom])
            )
            f_x[j_atom] += f_x_wall_sliding
            f_y[j_atom] += f_y_wall_sliding

            # Inelasticity
            # Forces from energy dissipation due to normal velocity
            f_x_wall_inelastic = (
                -inelasticity
                * f_x_wall_contact
                * np.sign(v_x_atoms[j_atom])
                * np.sign(x_n_wall[i_wall])
            )
            f_y_wall_inelastic = (
                -inelasticity
                * f_y_wall_contact
                * np.sign(v_y_atoms[j_atom])
                * np.sign(y_n_wall[i_wall])
            )
            f_x[j_atom] += f_x_wall_inelastic
            f_y[j_atom] += f_y_wall_inelastic


@njit
def update_positions_numba(
    x_atoms_local,
    y_atoms_local,
    x_atoms,
    y_atoms,
    v_x_atoms,
    v_y_atoms,
    f_x_atoms,
    f_y_atoms,
    x,
    y,
    angle,
    v_x,
    v_y,
    v_rot,
    m,
    rot_inertia,
    f_x_ext,
    f_y_ext,
    torque_ext,
    CLOCK_PERIOD_SIM,
):
    epsilon = 1e-10
    n_atoms = x_atoms.size
    f_x = 0
    f_y = 0
    torque = 0
    for i_atom in range(n_atoms):
        f_x += f_x_atoms[i_atom]
        f_y += f_y_atoms[i_atom]
        torque += f_y_atoms[i_atom] * (x_atoms[i_atom] - x) - f_x_atoms[
            i_atom
        ] * (y_atoms[i_atom] - y)

    a_x = (f_x + f_x_ext) / m
    a_y = (f_y + f_y_ext) / m
    a_rot = (torque + torque_ext) / (rot_inertia + epsilon)

    v_x += CLOCK_PERIOD_SIM * a_x
    v_y += CLOCK_PERIOD_SIM * a_y
    v_rot += CLOCK_PERIOD_SIM * a_rot

    x += CLOCK_PERIOD_SIM * v_x
    y += CLOCK_PERIOD_SIM * v_y
    angle += CLOCK_PERIOD_SIM * v_rot

    for i_atom in range(n_atoms):
        x_atom_rel = x_atoms_local[i_atom] * math.cos(angle) - y_atoms_local[
            i_atom
        ] * math.sin(angle)
        y_atom_rel = y_atoms_local[i_atom] * math.cos(angle) + x_atoms_local[
            i_atom
        ] * math.sin(angle)
        v_x_atom_rel = -v_rot * y_atom_rel
        v_y_atom_rel = v_rot * x_atom_rel
        x_atoms[i_atom] = x + x_atom_rel
        y_atoms[i_atom] = y + y_atom_rel
        v_x_atoms[i_atom] = v_x + v_x_atom_rel
        v_y_atoms[i_atom] = v_y + v_y_atom_rel

    return x, y, angle, v_x, v_y, v_rot
