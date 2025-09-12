import plotter.colors as colors
style = {
    "L": {
        "name": "Local",
        "color": "black",
        "alpha": 1,
        "marker": "o",
        "linestyle": "-",
        "hatch": "",

    },
    "R_[1.0, 0.0, 0.0]": {
        "name": "S - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "",

    },
    "R_[0.0, 1.0, 0.0]": {
        "name": "S - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "",

    },
    "R_[0.0, 0.0, 1.0]": {
        "name": "S - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "",

    },
    "R_[0.333, 0.333, 0.334]": {
        "name": "S - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "",

    },
    "RP_[1.0, 0.0, 0.0]": {
        "name": "SP - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 1,

        "marker": "s",
        "linestyle": "-",
        "hatch": "\\",

    },
    "RP_[0.0, 1.0, 0.0]": {
        "name": "SP - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "\\",

    },
    "RP_[0.0, 0.0, 1.0]": {
        "name": "SP - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "\\",

    },
    "RP_[0.333, 0.333, 0.334]": {
        "name": "SP - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "\\",

    },

    "TP_[1.0, 0.0, 0.0]_dt4": {
        "name": "T (dt4) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 1.0, 0.0]_dt4": {
        "name": "T (dt4) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 0.0, 1.0]_dt4": {
        "name": "T (dt4) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.333, 0.333, 0.334]_dt4": {
        "name": "T (dt4) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[1.0, 0.0, 0.0]_dt12": {
        "name": "T (dt12) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 1.0, 0.0]_dt12": {
        "name": "T (dt12) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 0.0, 1.0]_dt12": {
        "name": "T (dt12) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.333, 0.333, 0.334]_dt12": {
        "name": "T (dt12) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[1.0, 0.0, 0.0]_dt24": {
        "name": "T (dt24) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 1.0, 0.0]_dt24": {
        "name": "T (dt24) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 0.0, 1.0]_dt24": {
        "name": "T (dt24) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.333, 0.333, 0.334]_dt24": {
        "name": "T (dt24) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[1.0, 0.0, 0.0]_dt48": {
        "name": "T (dt48) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 1.0, 0.0]_dt48": {
        "name": "T (dt48) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.0, 0.0, 1.0]_dt48": {
        "name": "T (dt48) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TP_[0.333, 0.333, 0.334]_dt48": {
        "name": "T (dt48) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "/",

    },
    "TRP_[1.0, 0.0, 0.0]_dt4": {
        "name": "STP (dt4) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 1.0, 0.0]_dt4": {
        "name": "STP (dt4) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 0.0, 1.0]_dt4": {
        "name": "STP (dt4) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.333, 0.333, 0.334]_dt4": {
        "name": "STP (dt4) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 1,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[1.0, 0.0, 0.0]_dt12": {
        "name": "STP (dt12) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 1.0, 0.0]_dt12": {
        "name": "STP (dt12) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 0.0, 1.0]_dt12": {
        "name": "STP (dt12) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.333, 0.333, 0.334]_dt12": {
        "name": "STP (dt12) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.8,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[1.0, 0.0, 0.0]_dt24": {
        "name": "STP (dt24) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 1.0, 0.0]_dt24": {
        "name": "STP (dt24) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 0.0, 1.0]_dt24": {
        "name": "STP (dt24) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.333, 0.333, 0.334]_dt24": {
        "name": "STP (dt24) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.6,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[1.0, 0.0, 0.0]_dt48": {
        "name": "STP (dt48) - carbon-only",
        "color": colors.color_blind_palette[6],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 1.0, 0.0]_dt48": {
        "name": "STP (dt48) - water-only",
        "color": colors.color_blind_palette[4],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.0, 0.0, 1.0]_dt48": {
        "name": "STP (dt48) - land-only",
        "color": colors.color_blind_palette[3],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },
    "TRP_[0.333, 0.333, 0.334]_dt48": {
        "name": "STP (dt48) - mix",
        "color": colors.color_blind_palette[2],
        "alpha": 0.4,
        "marker": "s",
        "linestyle": "-",
        "hatch": "x",

    },



}