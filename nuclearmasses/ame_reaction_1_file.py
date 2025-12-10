from nuclearmasses.element_converter import ElementConverter


class AMEReactionFileOne(ElementConverter):
    """Easy access to where the variables are in the first AME reaction file."""

    def __init__(self, year: int):
        """Setup the values that locate the variable."""
        super().__init__()
        match year:
            case 1983:
                self.HEADER = 30
                self.FOOTER = 0
                self.START_R1_A = 1
                self.END_R1_A = 4
                self.START_R1_Z = 8
                self.END_R1_Z = 11
                self.START_S2N = 14
                self.END_S2N = 22
                self.START_DS2N = 24
                self.END_DS2N = 30
                self.START_S2P = 32
                self.END_S2P = 39
                self.START_DS2P = 43
                self.END_DS2P = 47
                self.START_QA = 50
                self.END_QA = 57
                self.START_DQA = 60
                self.END_DQA = 65
                self.START_Q2B = 68
                self.END_Q2B = 75
                self.START_DQ2B = 78
                self.END_DQ2B = 83
                self.START_QEP = 86
                self.END_QEP = 93
                self.START_DQEP = 96
                self.END_DQEP = 101
                self.START_QBN = 103
                self.END_QBN = 111
                self.START_DQBN = 114
                self.END_DQBN = 119
            case 2020:
                self.HEADER = 35
                self.FOOTER = 0
                self.START_R1_A = 1
                self.END_R1_A = 4
                self.START_R1_Z = 8
                self.END_R1_Z = 11
                self.START_S2N = 14
                self.END_S2N = 24
                self.START_DS2N = 25
                self.END_DS2N = 34
                self.START_S2P = 36
                self.END_S2P = 46
                self.START_DS2P = 47
                self.END_DS2P = 56
                self.START_QA = 58
                self.END_QA = 68
                self.START_DQA = 69
                self.END_DQA = 78
                self.START_Q2B = 79
                self.END_Q2B = 90
                self.START_DQ2B = 91
                self.END_DQ2B = 100
                self.START_QEP = 101
                self.END_QEP = 112
                self.START_DQEP = 113
                self.END_DQEP = 122
                self.START_QBN = 123
                self.END_QBN = 134
                self.START_DQBN = 135
                self.END_DQBN = 144
            case _:
                match year:
                    case 1995 | 2003 | 2012 | 2016:
                        self.HEADER = 39
                    case 1993:
                        self.HEADER = 40
                self.FOOTER = 0
                self.START_R1_A = 1
                self.END_R1_A = 4
                self.START_R1_Z = 8
                self.END_R1_Z = 11
                self.START_S2N = 14
                self.END_S2N = 22
                self.START_DS2N = 23
                self.END_DS2N = 30
                self.START_S2P = 32
                self.END_S2P = 40
                self.START_DS2P = 41
                self.END_DS2P = 48
                self.START_QA = 50
                self.END_QA = 58
                self.START_DQA = 59
                self.END_DQA = 66
                self.START_Q2B = 67
                self.END_Q2B = 76
                self.START_DQ2B = 77
                self.END_DQ2B = 84
                self.START_QEP = 85
                self.END_QEP = 94
                self.START_DQEP = 95
                self.END_DQEP = 102
                self.START_QBN = 103
                self.END_QBN = 112
                self.START_DQBN = 113
                self.END_DQBN = 125

        self.column_limits = [
            (self.START_R1_A, self.END_R1_A),
            (self.START_R1_Z, self.END_R1_Z),
            (self.START_S2N, self.END_S2N),
            (self.START_DS2N, self.END_DS2N),
            (self.START_S2P, self.END_S2P),
            (self.START_DS2P, self.END_DS2P),
            (self.START_QA, self.END_QA),
            (self.START_DQA, self.END_DQA),
            (self.START_Q2B, self.END_Q2B),
            (self.START_DQ2B, self.END_DQ2B),
            (self.START_QEP, self.END_QEP),
            (self.START_DQEP, self.END_DQEP),
            (self.START_QBN, self.END_QBN),
            (self.START_DQBN, self.END_DQBN),
        ]
