from nuclearmasses.parse import ElementConverter


class AMEReactionFileTwo(ElementConverter):
    """Easy access to where the variables are in the second AME reaction file."""

    def __init__(self, year: int):
        super().__init__()
        match year:
            case 1983:
                self.HEADER = 30
                self.FOOTER = 0
                self.START_R2_A = 1
                self.END_R2_A = 4
                self.START_R2_Z = 8
                self.END_R2_Z = 11
                self.START_SN = 14
                self.END_SN = 22
                self.START_DSN = 24
                self.END_DSN = 28
                self.START_SP = 30
                self.END_SP = 40
                self.START_DSP = 42
                self.END_DSP = 48
                self.START_Q4B = 49
                self.END_Q4B = 57
                self.START_DQ4B = 60
                self.END_DQ4B = 65
                self.START_QDA = 68
                self.END_QDA = 76
                self.START_DQDA = 78
                self.END_DQDA = 84
                self.START_QPA = 86
                self.END_QPA = 94
                self.START_DQPA = 96
                self.END_DQPA = 102
                self.START_QNA = 103
                self.END_QNA = 112
                self.START_DQNA = 114
                self.END_DQNA = 120
            case 2020:
                self.HEADER = 37
                self.FOOTER = 15
                self.START_R2_A = 1
                self.END_R2_A = 4
                self.START_R2_Z = 8
                self.END_R2_Z = 11
                self.START_SN = 14
                self.END_SN = 24
                self.START_DSN = 25
                self.END_DSN = 34
                self.START_SP = 36
                self.END_SP = 46
                self.START_DSP = 47
                self.END_DSP = 56
                self.START_Q4B = 57
                self.END_Q4B = 68
                self.START_DQ4B = 69
                self.END_DQ4B = 78
                self.START_QDA = 79
                self.END_QDA = 90
                self.START_DQDA = 91
                self.END_DQDA = 100
                self.START_QPA = 101
                self.END_QPA = 112
                self.START_DQPA = 113
                self.END_DQPA = 122
                self.START_QNA = 123
                self.END_QNA = 134
                self.START_DQNA = 135
                self.END_DQNA = 144
            case _:
                match year:
                    case 1995 | 2003 | 2012 | 2016:
                        self.HEADER = 39
                    case 1993:
                        self.HEADER = 40
                self.FOOTER = 0
                self.START_R2_A = 1
                self.END_R2_A = 4
                self.START_R2_Z = 8
                self.END_R2_Z = 11
                self.START_SN = 14
                self.END_SN = 22
                self.START_DSN = 23
                self.END_DSN = 30
                self.START_SP = 32
                self.END_SP = 40
                self.START_DSP = 41
                self.END_DSP = 48
                self.START_Q4B = 49
                self.END_Q4B = 58
                self.START_DQ4B = 59
                self.END_DQ4B = 66
                self.START_QDA = 67
                self.END_QDA = 76
                self.START_DQDA = 77
                self.END_DQDA = 84
                self.START_QPA = 85
                self.END_QPA = 94
                self.START_DQPA = 95
                self.END_DQPA = 102
                self.START_QNA = 103
                self.END_QNA = 112
                self.START_DQNA = 113
                self.END_DQNA = 125

        self.column_limits = [
                (self.START_R2_A, self.END_R2_A),
                (self.START_R2_Z, self.END_R2_Z),
                (self.START_SN, self.END_SN),
                (self.START_DSN, self.END_DSN),
                (self.START_SP, self.END_SP),
                (self.START_DSP, self.END_DSP),
                (self.START_Q4B, self.END_Q4B),
                (self.START_DQ4B, self.END_DQ4B),
                (self.START_QDA, self.END_QDA),
                (self.START_DQDA, self.END_DQDA),
                (self.START_QPA, self.END_QPA),
                (self.START_DQPA, self.END_DQPA),
                (self.START_QNA, self.END_QNA),
                (self.START_DQNA, self.END_DQNA),
                ]
