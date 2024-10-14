MOTHERSHIP = { # NAVE MÃE
    "image_path": "imgs/ships/mothership-1-256px.png",
    "life": 90,
    "speed": 150,
    "speed_shot": 1000,
    "rate_shot": 2.5,
    "damage_shot": 5,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_3 = { # NAVE TIPO FLOR
    "image_path": "imgs/ships/enemy-3-48px.png",
    "life": 3,
    "speed": 250,
    "speed_shot": 600,
    "rate_shot": 1e-12,
    "damage_shot": 1,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_4 = { # ESTRELA CINZA DE 4 LADOS
    "image_path": "imgs/ships/enemy-4-64px.png",
    "life": 5,
    "speed": 170,
    "speed_shot": 600,
    "rate_shot": 1,
    "damage_shot": 1,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_5 = { # DISCO PRATA
    "image_path": "imgs/ships/enemy-5-48px.png",
    "life": 3,
    "speed": 250,
    "speed_shot": 600,
    "rate_shot": 1e-12,
    "damage_shot": 1,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_6 = { # DISCO MARRON
    "image_path": "imgs/ships/enemy-6-60px.png",
    "life": 3,
    "speed": 270,
    "speed_shot": 600,
    "rate_shot": 1,
    "damage_shot": 2,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_7 = { # INIMIGO COM LUZ VERMLEHA NO CENTRO
    "image_path": "imgs/ships/enemy-7-48px.png",
    "life": 3,
    "speed": 200,
    "speed_shot": 650,
    "rate_shot": 1.333,
    "damage_shot": 1,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_8 = { # DISCO OCTÁGONO
    "image_path": "imgs/ships/enemy-8-48px.png",
    "life": 2,
    "speed": 350,
    "speed_shot": 600,
    "rate_shot": 1e-12,
    "damage_shot": 1,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_9 = { # ESTRELA AZUL DE 8 LADOS
    "image_path": "imgs/ships/enemy-9-96px.png",
    "life": 4,
    "speed": 310,
    "speed_shot": 700,
    "rate_shot": 2,
    "damage_shot": 2.5,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_10 = { # ESTRELA CINZA DE 8 LADOS
    "image_path": "imgs/ships/enemy-10-96px.png",
    "life": 7,
    "speed": 210,
    "speed_shot": 650,
    "rate_shot": 1,
    "damage_shot": 3,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_11 = { # ESTRELA AZUL DE 16 LADOS
    "image_path": "imgs/ships/enemy-11-80px.png",
    "life": 4,
    "speed": 310,
    "speed_shot": 600,
    "rate_shot": 3,
    "damage_shot": 2,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ENEMY_12 = { # ESTRELA COM 8 CHAMAS
    "image_path": "imgs/ships/enemy-12-64px.png",
    "life": 3,
    "speed": 310,
    "speed_shot": 600,
    "rate_shot": 2,
    "damage_shot": 3,
    "path_shot": "imgs/shots/shot-ball-1-sm.png",
    "state": "seeking"
}

ORB_1_3 = {
    "image_path": "imgs/ships/orb-1-24px.png",
    "image_path_locked": "imgs/ships/orb-3-24px.png",
    "speed": 750,
    "life": 3,
    "state": "resting"
}

phases = [
    {
        "level": 1,
        "background": "imgs/backgrounds/montain-1-4096px.jpg",
        "player": {
            "life": 5
        },
        "orbs": [],
        "waves": [
            {
                "enemies": [
                    {
                        "n_enemies": 3,
                        "min_dist": 1000,
                        "max_dist": 4000,
                        "config": ENEMY_3
                    },
                    {
                        "n_enemies": 2,
                        "min_dist": 2000,
                        "max_dist": 6000,
                        "config": ENEMY_4
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 5,
                        "min_dist": 1000,
                        "max_dist": 4000,
                        "config": ENEMY_3
                    },
                    {
                        "n_enemies": 3,
                        "min_dist": 2000,
                        "max_dist": 6000,
                        "config": ENEMY_4
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 5,
                        "min_dist": 1000,
                        "max_dist": 6000,
                        "config": ENEMY_3
                    },
                    {
                        "n_enemies": 3,
                        "min_dist": 2000,
                        "max_dist": 8000,
                        "config": ENEMY_4
                    },
                    {
                        "n_enemies": 5,
                        "min_dist": 2000,
                        "max_dist": 8000,
                        "config": ENEMY_9
                    }
                ]
            }
        ]
    },
    {
        "level": 2,
        "background": "imgs/backgrounds/ocean-7-4096px-iloveimg.jpeg",
        "player": {
            "life": 10
        },
        "orbs": [
            {
                "n": 3,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
            {
                "n": 3,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
            {
                "n": 3,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
        ],
        "waves": [
            {
                "enemies": [
                    {
                        "n_enemies": 5,
                        "min_dist": 1000,
                        "max_dist": 5000,
                        "config": ENEMY_5
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 2000,
                        "max_dist": 10000,
                        "config": ENEMY_7
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 4,
                        "min_dist": 1000,
                        "max_dist": 5000,
                        "config": ENEMY_5
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 2000,
                        "max_dist": 10000,
                        "config": ENEMY_7
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_12
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 4,
                        "min_dist": 1000,
                        "max_dist": 5000,
                        "config": ENEMY_5
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 2000,
                        "max_dist": 10000,
                        "config": ENEMY_7
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_12
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_11
                    }
                ]
            },
            # {
            #     "enemies": [
            #         {
            #             "n_enemies": 6,
            #             "min_dist": 2000,
            #             "max_dist": 5000,
            #             "config": ENEMY_5
            #         },
            #         {
            #             "n_enemies": 4,
            #             "min_dist": 3000,
            #             "max_dist": 8000,
            #             "config": ENEMY_7
            #         },
            #         {
            #             "n_enemies": 6,
            #             "min_dist": 5000,
            #             "max_dist": 10000,
            #             "config": ENEMY_12
            #         },
            #         {
            #             "n_enemies": 4,
            #             "min_dist": 5000,
            #             "max_dist": 10000,
            #             "config": ENEMY_11
            #         }
            #     ]
            # },
            # {
            #     "enemies": [
            #         {
            #             "n_enemies": 6,
            #             "min_dist": 2000,
            #             "max_dist": 5000,
            #             "config": ENEMY_5
            #         },
            #         {
            #             "n_enemies": 4,
            #             "min_dist": 3000,
            #             "max_dist": 8000,
            #             "config": ENEMY_7
            #         },
            #         {
            #             "n_enemies": 7,
            #             "min_dist": 5000,
            #             "max_dist": 10000,
            #             "config": ENEMY_12
            #         },
            #         {
            #             "n_enemies": 6,
            #             "min_dist": 5000,
            #             "max_dist": 10000,
            #             "config": ENEMY_11
            #         }
            #     ]
            # }
        ]
    },
    {
        "level": 3,
        "background": "imgs/backgrounds/deep_space_gray-4096x2048.png",
        "player": {
            "life": 15
        },
        "orbs": [
            {
                "n": 5,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
            {
                "n": 5,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
            {
                "n": 5,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },            
            {
                "n": 5,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },
            {
                "n": 5,
                "wait": 0,
                "wait_between": 2,
                "config": ORB_1_3
            },            
        ],
        "waves": [
            {
                "enemies": [
                    {
                        "n_enemies": 1,
                        "min_dist": 2000,
                        "max_dist": 6000,
                        "config": MOTHERSHIP
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 2000,
                        "max_dist": 5000,
                        "config": ENEMY_4
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 3000,
                        "max_dist": 8000,
                        "config": ENEMY_6
                    },
                    {
                        "n_enemies": 3,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_10
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 6,
                        "min_dist": 2000,
                        "max_dist": 5000,
                        "config": ENEMY_4
                    },
                    {
                        "n_enemies": 6,
                        "min_dist": 3000,
                        "max_dist": 8000,
                        "config": ENEMY_6
                    },
                    {
                        "n_enemies": 5,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_10
                    }
                ]
            },
            {
                "enemies": [
                    {
                        "n_enemies": 6,
                        "min_dist": 2000,
                        "max_dist": 5000,
                        "config": ENEMY_4
                    },
                    {
                        "n_enemies": 6,
                        "min_dist": 3000,
                        "max_dist": 8000,
                        "config": ENEMY_6
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_10
                    },
                    {
                        "n_enemies": 4,
                        "min_dist": 5000,
                        "max_dist": 10000,
                        "config": ENEMY_11
                    }
                ]
            },
        ]
    }
]