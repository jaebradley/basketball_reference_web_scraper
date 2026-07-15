from enum import Enum, unique

from basketball_reference_web_scraper.html import BasicTeamStatisticsTable, AdvancedTeamStatisticsTable


class Location(Enum):
    HOME = "HOME"
    AWAY = "AWAY"


class Outcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"


@unique
class Team(Enum):
    ATLANTA_HAWKS = "ATLANTA HAWKS"
    BOSTON_CELTICS = "BOSTON CELTICS"
    BROOKLYN_NETS = "BROOKLYN NETS"
    CHARLOTTE_HORNETS = "CHARLOTTE HORNETS"
    CHICAGO_BULLS = "CHICAGO BULLS"
    CLEVELAND_CAVALIERS = "CLEVELAND CAVALIERS"
    DALLAS_MAVERICKS = "DALLAS MAVERICKS"
    DENVER_NUGGETS = "DENVER NUGGETS"
    DETROIT_PISTONS = "DETROIT PISTONS"
    GOLDEN_STATE_WARRIORS = "GOLDEN STATE WARRIORS"
    HOUSTON_ROCKETS = "HOUSTON ROCKETS"
    INDIANA_PACERS = "INDIANA PACERS"
    LOS_ANGELES_CLIPPERS = "LOS ANGELES CLIPPERS"
    LOS_ANGELES_LAKERS = "LOS ANGELES LAKERS"
    MEMPHIS_GRIZZLIES = "MEMPHIS GRIZZLIES"
    MIAMI_HEAT = "MIAMI HEAT"
    MILWAUKEE_BUCKS = "MILWAUKEE BUCKS"
    MINNESOTA_TIMBERWOLVES = "MINNESOTA TIMBERWOLVES"
    NEW_ORLEANS_PELICANS = "NEW ORLEANS PELICANS"
    NEW_YORK_KNICKS = "NEW YORK KNICKS"
    OKLAHOMA_CITY_THUNDER = "OKLAHOMA CITY THUNDER"
    ORLANDO_MAGIC = "ORLANDO MAGIC"
    PHILADELPHIA_76ERS = "PHILADELPHIA 76ERS"
    PHOENIX_SUNS = "PHOENIX SUNS"
    PORTLAND_TRAIL_BLAZERS = "PORTLAND TRAIL BLAZERS"
    SACRAMENTO_KINGS = "SACRAMENTO KINGS"
    SAN_ANTONIO_SPURS = "SAN ANTONIO SPURS"
    TORONTO_RAPTORS = "TORONTO RAPTORS"
    UTAH_JAZZ = "UTAH JAZZ"
    WASHINGTON_WIZARDS = "WASHINGTON WIZARDS"

    # INACTIVE NBA TEAMS (see https://www.basketball-reference.com/teams/)
    ANDERSON_PACKERS = "ANDERSON PACKERS"
    BALTIMORE_BULLETS = "BALTIMORE BULLETS"
    BUFFALO_BRAVES = "BUFFALO BRAVES"
    CAPITAL_BULLETS = "CAPITAL BULLETS"
    CHICAGO_PACKERS = "CHICAGO PACKERS"
    CHICAGO_STAGS = "CHICAGO STAGS"
    CHICAGO_ZEPHYRS = "CHICAGO ZEPHYRS"
    CINCINNATI_ROYALS = "CINCINNATI ROYALS"
    FORT_WAYNE_PISTONS = "FORT WAYNE PISTONS"
    INDIANAPOLIS_OLYMPIANS = "INDIANAPOLIS OLYMPIANS"
    KANSAS_CITY_KINGS = "KANSAS CITY KINGS"
    KANSAS_CITY_OMAHA_KINGS = "KANSAS CITY-OMAHA KINGS"
    CHARLOTTE_BOBCATS = "CHARLOTTE BOBCATS"
    MINNEAPOLIS_LAKERS = "MINNEAPOLIS LAKERS"
    MILWAUKEE_HAWKS = "MILWAUKEE HAWKS"
    NEW_JERSEY_NETS = "NEW JERSEY NETS"
    NEW_ORLEANS_HORNETS = "NEW ORLEANS HORNETS"
    NEW_ORLEANS_JAZZ = "NEW ORLEANS JAZZ"
    NEW_ORLEANS_OKLAHOMA_CITY_HORNETS = "NEW ORLEANS/OKLAHOMA CITY HORNETS"
    NEW_YORK_NETS = "NEW YORK NETS"
    PHILADELPHIA_WARRIORS = "PHILADELPHIA WARRIORS"
    ROCHESTER_ROYALS = "ROCHESTER ROYALS"
    SAN_DIEGO_CLIPPERS = "SAN DIEGO CLIPPERS"
    SAN_DIEGO_ROCKETS = "SAN DIEGO ROCKETS"
    SAN_FRANCISCO_WARRIORS = "SAN FRANCISCO WARRIORS"
    SHEBOYGAN_RED_SKINS = "SHEBOYGAN RED SKINS"
    SEATTLE_SUPERSONICS = "SEATTLE SUPERSONICS"
    ST_LOUIS_BOMBERS = "ST. LOUIS BOMBERS"
    ST_LOUIS_HAWKS = "ST. LOUIS HAWKS"
    SYRACUSE_NATIONALS = "SYRACUSE NATIONALS"
    TRI_CITIES_BLACKHAWKS = "TRI-CITIES BLACKHAWKS"
    VANCOUVER_GRIZZLIES = "VANCOUVER GRIZZLIES"
    WASHINGTON_BULLETS = "WASHINGTON BULLETS"
    WASHINGTON_CAPITOLS = "WASHINGTON CAPITOLS"
    WATERLOO_HAWKS = "WATERLOO HAWKS"


@unique
class TeamAbbreviation(Enum):
    ATL = "ATL"
    BOS = "BOS"
    BRK = "BRK"
    CHI = "CHI"
    CHO = "CHO"
    CLE = "CLE"
    DAL = "DAL"
    DEN = "DEN"
    DET = "DET"
    GSW = "GSW"
    HOU = "HOU"
    IND = "IND"
    LAC = "LAC"
    LAL = "LAL"
    MEM = "MEM"
    MIA = "MIA"
    MIL = "MIL"
    MIN = "MIN"
    NOP = "NOP"
    NYK = "NYK"
    OKC = "OKC"
    ORL = "ORL"
    PHI = "PHI"
    PHO = "PHO"
    POR = "POR"
    SAC = "SAC"
    SAS = "SAS"
    TOR = "TOR"
    UTA = "UTA"
    WAS = "WAS"

    # INACTIVE NBA TEAMS (see https://www.basketball-reference.com/teams/)
    AND = "AND"
    BAL = "BAL"
    BLB = "BLB"
    BUF = "BUF"
    CAP = "CAP"
    CHA = "CHA"
    CHH = "CHH"
    CHP = "CHP"
    CHS = "CHS"
    CHZ = "CHZ"
    CIN = "CIN"
    DNN = "DNN"
    FTW = "FTW"
    INO = "INO"
    KCK = "KCK"
    KCO = "KCO"
    MLH = "MLH"
    NJN = "NJN"
    NOH = "NOH"
    NOJ = "NOJ"
    NOK = "NOK"
    NYN = "NYN"
    MNL = "MNL"
    PHW = "PHW"
    ROC = "ROC"
    SDC = "SDC"
    SDR = "SDR"
    SEA = "SEA"
    SHE = "SHE"
    SFW = "SFW"
    STB = "STB"
    STL = "STL"
    SYR = "SYR"
    TRI = "TRI"
    VAN = "VAN"
    WAT = "WAT"
    WSB = "WSB"
    WSC = "WSC"


class OutputType(Enum):
    JSON = "JSON"
    CSV = "CSV"


class OutputWriteOption(Enum):
    WRITE = "w"
    CREATE_AND_WRITE = "w+"
    APPEND = "a"
    APPEND_AND_WRITE = "a+"


class Position(Enum):
    POINT_GUARD = "POINT GUARD"
    SHOOTING_GUARD = "SHOOTING GUARD"
    SMALL_FORWARD = "SMALL FORWARD"
    POWER_FORWARD = "POWER FORWARD"
    CENTER = "CENTER"
    FORWARD = "FORWARD"
    GUARD = "GUARD"


class PeriodType(Enum):
    QUARTER = "QUARTER"
    OVERTIME = "OVERTIME"


class League(Enum):
    NATIONAL_BASKETBALL_ASSOCIATION = "NATIONAL_BASKETBALL_ASSOCIATION"
    AMERICAN_BASKETBALL_ASSOCIATION = "AMERICAN_BASKETBALL_ASSOCIATION"
    BASKETBALL_ASSOCIATION_OF_AMERICA = "BASKETBALL_ASSOCIATION_OF_AMERICA"


class Conference(Enum):
    EASTERN = "EASTERN"
    WESTERN = "WESTERN"


class Division(Enum):
    ATLANTIC = "ATLANTIC"
    CENTRAL = "CENTRAL"
    MIDWEST = "MIDWEST"
    NORTHWEST = "NORTHWEST"
    PACIFIC = "PACIFIC"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"


DIVISIONS_TO_CONFERENCES = {
    Division.ATLANTIC: Conference.EASTERN,
    Division.CENTRAL: Conference.EASTERN,
    Division.SOUTHEAST: Conference.EASTERN,
    Division.MIDWEST: Conference.WESTERN,
    Division.PACIFIC: Conference.WESTERN,
    Division.SOUTHWEST: Conference.WESTERN,
    Division.NORTHWEST: Conference.WESTERN
}

TEAMS_BY_ABBREVIATION: dict[TeamAbbreviation, Team] = {
    TeamAbbreviation.ATL: Team.ATLANTA_HAWKS,
    TeamAbbreviation.BOS: Team.BOSTON_CELTICS,
    TeamAbbreviation.BRK: Team.BROOKLYN_NETS,
    TeamAbbreviation.CHI: Team.CHICAGO_BULLS,
    TeamAbbreviation.CHO: Team.CHARLOTTE_HORNETS,
    TeamAbbreviation.CLE: Team.CLEVELAND_CAVALIERS,
    TeamAbbreviation.DAL: Team.DALLAS_MAVERICKS,
    TeamAbbreviation.DEN: Team.DENVER_NUGGETS,
    TeamAbbreviation.DET: Team.DETROIT_PISTONS,
    TeamAbbreviation.DNN: Team.DENVER_NUGGETS,
    TeamAbbreviation.GSW: Team.GOLDEN_STATE_WARRIORS,
    TeamAbbreviation.HOU: Team.HOUSTON_ROCKETS,
    TeamAbbreviation.IND: Team.INDIANA_PACERS,
    TeamAbbreviation.LAC: Team.LOS_ANGELES_CLIPPERS,
    TeamAbbreviation.LAL: Team.LOS_ANGELES_LAKERS,
    TeamAbbreviation.MEM: Team.MEMPHIS_GRIZZLIES,
    TeamAbbreviation.MIA: Team.MIAMI_HEAT,
    TeamAbbreviation.MIL: Team.MILWAUKEE_BUCKS,
    TeamAbbreviation.MIN: Team.MINNESOTA_TIMBERWOLVES,
    TeamAbbreviation.NOP: Team.NEW_ORLEANS_PELICANS,
    TeamAbbreviation.NYK: Team.NEW_YORK_KNICKS,
    TeamAbbreviation.OKC: Team.OKLAHOMA_CITY_THUNDER,
    TeamAbbreviation.ORL: Team.ORLANDO_MAGIC,
    TeamAbbreviation.PHI: Team.PHILADELPHIA_76ERS,
    TeamAbbreviation.PHO: Team.PHOENIX_SUNS,
    TeamAbbreviation.POR: Team.PORTLAND_TRAIL_BLAZERS,
    TeamAbbreviation.SAC: Team.SACRAMENTO_KINGS,
    TeamAbbreviation.SAS: Team.SAN_ANTONIO_SPURS,
    TeamAbbreviation.TOR: Team.TORONTO_RAPTORS,
    TeamAbbreviation.UTA: Team.UTAH_JAZZ,
    TeamAbbreviation.WAS: Team.WASHINGTON_WIZARDS,

    # INACTIVE NBA TEAMS (see https://www.basketball-reference.com/teams/)
    TeamAbbreviation.AND: Team.ANDERSON_PACKERS,
    TeamAbbreviation.BAL: Team.BALTIMORE_BULLETS,
    TeamAbbreviation.BLB: Team.BALTIMORE_BULLETS,
    TeamAbbreviation.BUF: Team.BUFFALO_BRAVES,
    TeamAbbreviation.CAP: Team.CAPITAL_BULLETS,
    TeamAbbreviation.CHP: Team.CHICAGO_PACKERS,
    TeamAbbreviation.CHS: Team.CHICAGO_STAGS,
    TeamAbbreviation.CHZ: Team.CHICAGO_ZEPHYRS,
    TeamAbbreviation.CIN: Team.CINCINNATI_ROYALS,
    TeamAbbreviation.FTW: Team.FORT_WAYNE_PISTONS,
    TeamAbbreviation.INO: Team.INDIANAPOLIS_OLYMPIANS,
    TeamAbbreviation.KCK: Team.KANSAS_CITY_KINGS,
    TeamAbbreviation.KCO: Team.KANSAS_CITY_OMAHA_KINGS,
    TeamAbbreviation.MLH: Team.MILWAUKEE_HAWKS,
    TeamAbbreviation.MNL: Team.MINNEAPOLIS_LAKERS,
    TeamAbbreviation.NJN: Team.NEW_JERSEY_NETS,
    TeamAbbreviation.NOH: Team.NEW_ORLEANS_HORNETS,
    TeamAbbreviation.NOJ: Team.NEW_ORLEANS_JAZZ,
    TeamAbbreviation.NOK: Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS,
    TeamAbbreviation.NYN: Team.NEW_YORK_NETS,
    TeamAbbreviation.CHA: Team.CHARLOTTE_BOBCATS,
    TeamAbbreviation.CHH: Team.CHARLOTTE_HORNETS,
    TeamAbbreviation.PHW: Team.PHILADELPHIA_WARRIORS,
    TeamAbbreviation.ROC: Team.ROCHESTER_ROYALS,
    TeamAbbreviation.SDC: Team.SAN_DIEGO_CLIPPERS,
    TeamAbbreviation.SDR: Team.SAN_DIEGO_ROCKETS,
    TeamAbbreviation.SEA: Team.SEATTLE_SUPERSONICS,
    TeamAbbreviation.SHE: Team.SHEBOYGAN_RED_SKINS,
    TeamAbbreviation.SFW: Team.SAN_FRANCISCO_WARRIORS,
    TeamAbbreviation.STB: Team.ST_LOUIS_BOMBERS,
    TeamAbbreviation.STL: Team.ST_LOUIS_HAWKS,
    TeamAbbreviation.SYR: Team.SYRACUSE_NATIONALS,
    TeamAbbreviation.TRI: Team.TRI_CITIES_BLACKHAWKS,
    TeamAbbreviation.VAN: Team.VANCOUVER_GRIZZLIES,
    TeamAbbreviation.WAT: Team.WATERLOO_HAWKS,
    TeamAbbreviation.WSB: Team.WASHINGTON_BULLETS,
    TeamAbbreviation.WSC: Team.WASHINGTON_CAPITOLS,
}

TEAM_ABBREVIATIONS_BY_TEAM: dict[Team, TeamAbbreviation] = {v: k for k, v in TEAMS_BY_ABBREVIATION.items()}
# Both CHH and CHO are abbreviations for the Charlotte Hornets. Use the current active team abbreviation when identifying the abbreviation for the Charlotte Hornets.
TEAM_ABBREVIATIONS_BY_TEAM[Team.CHARLOTTE_HORNETS] = TeamAbbreviation.CHO
# The Baltimore Bullets existed from 1949-1955 in the NBA: https://www.basketball-reference.com/teams/BLB/
# A different Baltimore Bullets team existed in the NBA (associated with the Washington Wizards franchise: https://www.basketball-reference.com/teams/BAL/1964.html)
TEAM_ABBREVIATIONS_BY_TEAM[Team.BALTIMORE_BULLETS] = TeamAbbreviation.BAL
# A Denver Nuggets team existed from 1949-1950 in the NBA: https://www.basketball-reference.com/teams/DNN/
# The currently active Denver Nuggets franchise only became an NBA team starting in the 1976-1977 NBA season: https://www.basketball-reference.com/teams/DEN/
TEAM_ABBREVIATIONS_BY_TEAM[Team.DENVER_NUGGETS] = TeamAbbreviation.DEN

POSITION_ABBREVIATIONS_TO_POSITION = {
    "PG": Position.POINT_GUARD,
    "SG": Position.SHOOTING_GUARD,
    "SF": Position.SMALL_FORWARD,
    "PF": Position.POWER_FORWARD,
    "C": Position.CENTER,
    "F": Position.FORWARD,
    "G": Position.GUARD,
}

LOCATION_ABBREVIATIONS_TO_POSITION = {
    "": Location.HOME,
    "@": Location.AWAY,
}

OUTCOME_ABBREVIATIONS_TO_OUTCOME = {
    "W": Outcome.WIN,
    "L": Outcome.LOSS,
}

LEAGUE_ABBREVIATIONS_TO_LEAGUE = {
    "NBA": League.NATIONAL_BASKETBALL_ASSOCIATION,
    "ABA": League.AMERICAN_BASKETBALL_ASSOCIATION,
    "BAA": League.BASKETBALL_ASSOCIATION_OF_AMERICA,
}


class TeamTotal:
    def __init__(self, basic_statistics_table: BasicTeamStatisticsTable,
                 advanced_statistics_table: AdvancedTeamStatisticsTable):
        if basic_statistics_table.team_abbreviation != advanced_statistics_table.team_abbreviation:
            raise ValueError(
                f"mismatched team abbreviations between the basic totals team: {basic_statistics_table.team_abbreviation} and the advanced totals team: {advanced_statistics_table.team_abbreviation}")

        self.team_abbreviation = basic_statistics_table.team_abbreviation
        self.basic_totals = basic_statistics_table.team_totals
        self.advanced_totals = advanced_statistics_table.team_totals

    @property
    def minutes_played(self):
        return self.basic_totals.minutes_played

    @property
    def made_field_goals(self):
        return self.basic_totals.made_field_goals

    @property
    def attempted_field_goals(self):
        return self.basic_totals.attempted_field_goals

    @property
    def made_three_point_field_goals(self):
        return self.basic_totals.made_three_point_field_goals

    @property
    def attempted_three_point_field_goals(self):
        return self.basic_totals.attempted_three_point_field_goals

    @property
    def made_free_throws(self):
        return self.basic_totals.made_free_throws

    @property
    def attempted_free_throws(self):
        return self.basic_totals.attempted_free_throws

    @property
    def offensive_rebounds(self):
        return self.basic_totals.offensive_rebounds

    @property
    def defensive_rebounds(self):
        return self.basic_totals.defensive_rebounds

    @property
    def assists(self):
        return self.basic_totals.assists

    @property
    def steals(self):
        return self.basic_totals.steals

    @property
    def blocks(self):
        return self.basic_totals.blocks

    @property
    def turnovers(self):
        return self.basic_totals.turnovers

    @property
    def personal_fouls(self):
        return self.basic_totals.personal_fouls

    @property
    def points(self):
        return self.basic_totals.points

    @property
    def true_shooting_percentage(self):
        return self.advanced_totals.true_shooting_percentage

    @property
    def effective_field_goal_percentage(self):
        return self.advanced_totals.effective_field_goal_percentage

    @property
    def three_point_attempt_rate(self):
        return self.advanced_totals.three_point_attempt_rate

    @property
    def free_throw_attempt_rate(self):
        return self.advanced_totals.free_throw_attempt_rate

    @property
    def offensive_rebound_percentage(self):
        return self.advanced_totals.offensive_rebound_percentage

    @property
    def defensive_rebound_percentage(self):
        return self.advanced_totals.defensive_rebound_percentage

    @property
    def total_rebound_percentage(self):
        return self.advanced_totals.total_rebound_percentage

    @property
    def assist_percentage(self):
        return self.advanced_totals.assist_percentage

    @property
    def steal_percentage(self):
        return self.advanced_totals.steal_percentage

    @property
    def block_percentage(self):
        return self.advanced_totals.block_percentage

    @property
    def turnover_rate(self):
        return self.advanced_totals.turnover_rate

    @property
    def offensive_rating(self):
        return self.advanced_totals.offensive_rating

    @property
    def defensive_rating(self):
        return self.advanced_totals.defensive_rating


class PlayerData:
    def __init__(self, name, resource_location, league_abbreviations):
        self.name = name
        self.resource_location = resource_location
        self.league_abbreviations = set(league_abbreviations)
