from BaseClasses import Location

CIV_VI_AP_LOCATION_ID_BASE = 5041000


class CivVILocation(Location):
    game: str = "Civilization VI"


ancient_era = {
    "AP_1": 1 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_2": 2 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_3": 3 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_4": 4 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_5": 5 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_6": 6 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_7": 7 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_8": 8 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_9": 9 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_10": 10 + CIV_VI_AP_LOCATION_ID_BASE,
    "AP_11": 11 + CIV_VI_AP_LOCATION_ID_BASE,
}

location_table = {**ancient_era}
