"""Storage for variable line positions."""
from nuclearmasses.parse import Parse


class AMEMassFile(Parse):
    """Easy access to where the variables are in the AME mass file."""

    def __init__(self, year: int):
        super().__init__()
        match year:
            case 2020:
                self.HEADER = 36
                self.FOOTER = 0
                self.START_Z = 11
                self.END_Z = 14
                self.START_A = 16
                self.END_A = 19
                self.START_ME = 29
                self.END_ME = 42
                self.START_DME = 43
                self.END_DME = 53
                self.START_BE_PER_A = 56
                self.END_BE_PER_A = 66
                self.START_DBE_PER_A = 69
                self.END_DBE_PER_A = 77
                self.START_BETA_DECAY_ENERGY = 82
                self.END_BETA_DECAY_ENERGY = 93
                self.START_DBETA_DECAY_ENERGY = 95
                self.END_DBETA_DECAY_ENERGY = 104
                self.START_AM = 106
                self.END_AM = 109
                self.START_MICRO_U = 110
                self.END_MICRO_U = 120
                self.START_MICRO_DU = 124
                self.END_MICRO_DU = 135
            case _:
                self.HEADER = 39
                self.FOOTER = 0
                self.START_Z = 11
                self.END_Z = 14
                self.START_A = 16
                self.END_A = 19
                self.START_ME = 29
                self.END_ME = 41
                self.START_DME = 42
                self.END_DME = 53
                self.START_BE_PER_A = 54
                self.END_BE_PER_A = 64
                self.START_DBE_PER_A = 65
                self.END_DBE_PER_A = 72
                self.START_BETA_DECAY_ENERGY = 76
                self.END_BETA_DECAY_ENERGY = 86
                self.START_DBETA_DECAY_ENERGY = 87
                self.END_DBETA_DECAY_ENERGY = 95
                self.START_AM = 0
                self.END_AM = 0
                self.START_MICRO_U = 100
                self.END_MICRO_U = 112
                self.START_MICRO_DU = 113
                self.END_MICRO_DU = 125

        self.column_limits = [
                (self.START_Z, self.END_Z),
                (self.START_A, self.END_A),
                (self.START_ME, self.END_ME),
                (self.START_DME, self.END_DME),
                (self.START_BE_PER_A, self.END_BE_PER_A),
                (self.START_DBE_PER_A, self.END_DBE_PER_A),
                (self.START_BETA_DECAY_ENERGY, self.END_BETA_DECAY_ENERGY),
                (self.START_DBETA_DECAY_ENERGY, self.END_DBETA_DECAY_ENERGY),
                (self.START_AM, self.END_AM),
                (self.START_MICRO_U, self.END_MICRO_U),
                (self.START_MICRO_DU, self.END_MICRO_DU),
                ]
