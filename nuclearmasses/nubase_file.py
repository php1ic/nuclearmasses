from nuclearmasses.element_converter import ElementConverter


class NUBASEFile(ElementConverter):
    """Easy access to where variables are in the NUBASE file.

    The NUBASE data file is formatted by location in the line, values exist
    between 2 specific columns in the line. Store the start and end locations
    in this class to allow simple access and stop the NUBASE parser having
    magic numbers.
    """

    def __init__(self, year: int):
        """Setup the values that locate the variable."""
        super().__init__()
        match year:
            case 1995:
                self.HEADER = 0
                self.FOOTER = 0
                self.START_A = 0
                self.END_A = 3
                self.START_Z = 4
                self.END_Z = 7
                self.START_STATE = 7
                self.END_STATE = 8
                self.START_ME = 18
                self.END_ME = 29
                self.START_DME = 29
                self.END_DME = 38
                self.START_ISOMER = 39
                self.END_ISOMER = 46
                self.START_DISOMER = 48
                self.END_DISOMER = 56
                self.START_HALFLIFEVALUE = 60
                self.END_HALFLIFEVALUE = 68
                self.START_HALFLIFEUNIT = 69
                self.END_HALFLIFEUNIT = 71
                self.START_HALFLIFEERROR = 72
                self.END_HALFLIFEERROR = 77
                self.START_SPIN = 79
                self.END_SPIN = 93
                self.START_DECAYSTRING = 106
                self.END_DECAYSTRING = None
            case 2003:
                self.HEADER = 0
                self.FOOTER = 0
                self.START_A = 0
                self.END_A = 3
                self.START_Z = 4
                self.END_Z = 7
                self.START_STATE = 7
                self.END_STATE = 8
                self.START_ME = 18
                self.END_ME = 29
                self.START_DME = 29
                self.END_DME = 38
                self.START_ISOMER = 39
                self.END_ISOMER = 46
                self.START_DISOMER = 48
                self.END_DISOMER = 56
                self.START_HALFLIFEVALUE = 60
                self.END_HALFLIFEVALUE = 68
                self.START_HALFLIFEUNIT = 69
                self.END_HALFLIFEUNIT = 71
                self.START_HALFLIFEERROR = 72
                self.END_HALFLIFEERROR = 77
                self.START_SPIN = 79
                self.END_SPIN = 93
                self.START_DECAYSTRING = 106
                self.END_DECAYSTRING = None
            case 2020:
                self.HEADER = 25
                self.FOOTER = 0
                self.START_A = 0
                self.END_A = 3
                self.START_Z = 4
                self.END_Z = 7
                self.START_STATE = 7
                self.END_STATE = 8
                self.START_ME = 18
                self.END_ME = 31
                self.START_DME = 31
                self.END_DME = 42
                self.START_ISOMER = 43
                self.END_ISOMER = 53
                self.START_DISOMER = 54
                self.END_DISOMER = 64
                self.START_HALFLIFEVALUE = 69
                self.END_HALFLIFEVALUE = 77
                self.START_HALFLIFEUNIT = 78
                self.END_HALFLIFEUNIT = 80
                self.START_HALFLIFEERROR = 81
                self.END_HALFLIFEERROR = 87
                self.START_SPIN = 88
                self.END_SPIN = 101
                self.START_ENSDF = 102
                self.END_ENSDF = 103
                self.START_YEAR = 114
                self.END_YEAR = 118
                self.START_DECAYSTRING = 119
                self.END_DECAYSTRING = None
            case _:
                self.HEADER = 0
                self.FOOTER = 0
                self.START_A = 0
                self.END_A = 3
                self.START_Z = 4
                self.END_Z = 7
                self.START_STATE = 7
                self.END_STATE = 8
                self.START_ME = 18
                self.END_ME = 29
                self.START_DME = 29
                self.END_DME = 38
                self.START_ISOMER = 39
                self.END_ISOMER = 46
                self.START_DISOMER = 48
                self.END_DISOMER = 56
                self.START_HALFLIFEVALUE = 60
                self.END_HALFLIFEVALUE = 68
                self.START_HALFLIFEUNIT = 69
                self.END_HALFLIFEUNIT = 71
                self.START_HALFLIFEERROR = 72
                self.END_HALFLIFEERROR = 77
                self.START_SPIN = 79
                self.END_SPIN = 93
                self.START_YEAR = 105
                self.END_YEAR = 109
                self.START_DECAYSTRING = 110
                self.END_DECAYSTRING = None

        self.column_limits = [
                (self.START_A, self.END_A),
                (self.START_Z, self.END_Z),
                (self.START_STATE, self.END_STATE),
                (self.START_ME, self.END_ME),
                (self.START_DME, self.END_DME),
                (self.START_ISOMER, self.END_ISOMER),
                (self.START_DISOMER, self.END_DISOMER),
                (self.START_HALFLIFEVALUE, self.END_HALFLIFEVALUE),
                (self.START_HALFLIFEUNIT, self.END_HALFLIFEUNIT),
                (self.START_HALFLIFEERROR, self.END_HALFLIFEERROR),
                (self.START_SPIN, self.END_SPIN),
                (self.START_DECAYSTRING, self.END_DECAYSTRING),
                ]

        if year > 2003:
            print("In here")
            self.column_limits.insert(-1, (self.START_YEAR, self.END_YEAR))
