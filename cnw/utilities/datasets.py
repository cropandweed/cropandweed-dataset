class Dataset:
    def __init__(self, labels):
        self.labels = {}
        self.mapping = {}
        for label_id, label in labels.items():
            if type(label) is tuple:
                self.labels[label_id] = (label[0], label[1], label_id) if len(label) > 1 else (label[0], (0, 0, 0))
            else:
                self.labels[label_id] = (label, (0, 0, 0))
            if len(label) > 2:
                for source_id in label[2]:
                    self.mapping[source_id] = label_id
        if len(self.mapping) == 0:
            self.mapping = {label: label for label in labels}

    def get_label_color(self, label_id, bgr=False):
        if bgr:
            return self.labels[label_id][1][::-1] if label_id in self.labels else None
        else:
            return self.labels[label_id][1] if label_id in self.labels else None

    def get_label_ids(self):
        return self.labels.keys()

    def get_label_name(self, label_id):
        return self.labels[label_id][0] if label_id in self.labels else None

    def get_mapped_id(self, source_id):
        return self.mapping[source_id] if source_id in self.mapping else None


DATASETS = dict()

DATASETS['CropAndWeed'] = Dataset({
    0: ('Soil', (0, 0, 0)),
    1: ('Maize', (255, 0, 0)),
    2: ('Maize two-leaf stage', (234, 0, 0)),
    3: ('Maize four-leaf stage', (212, 0, 0)),
    4: ('Maize six-leaf stage', (191, 0, 0)),
    5: ('Maize eight-leaf stage', (170, 0, 0)),
    6: ('Maize max', (149, 0, 0)),
    7: ('Sugar beet', (255, 85, 0)),
    8: ('Sugar beet two-leaf stage', (234, 78, 0)),
    9: ('Sugar beet four-leaf stage', (212, 71, 0)),
    10: ('Sugar beet six-leaf stage', (191, 64, 0)),
    11: ('Sugar beet eight-leaf stage', (170, 57, 0)),
    12: ('Sugar beet Max', (149, 50, 0)),
    13: ('Pea', (255, 170, 0)),
    14: ('Courgette', (255, 255, 0)),
    15: ('Pumpkins', (170, 255, 0)),
    16: ('Radish', (85, 255, 0)),
    17: ('Asparagus', (0, 255, 0)),
    18: ('Potato', (0, 255, 85)),
    19: ('Flat leaf parsley', (0, 255, 170)),
    20: ('Curly leaf parsley', (0, 255, 255)),
    21: ('Cowslip', (0, 170, 255)),
    22: ('Poppy', (0, 85, 255)),
    23: ('Hemp', (0, 0, 255)),
    24: ('Sunflower', (85, 0, 255)),
    25: ('Sage', (170, 0, 255)),
    26: ('Common bean', (255, 0, 255)),
    27: ('Faba bean', (255, 0, 170)),
    28: ('Clover', (255, 0, 85)),
    29: ('Hybrid goosefoot', (255, 188, 178)),
    30: ('Black-bindweed', (255, 207, 178)),
    31: ('Cockspur grass', (255, 226, 178)),
    32: ('Red-root amaranth', (255, 245, 178)),
    33: ('White goosefoot', (245, 255, 178)),
    34: ('Thorn apple', (226, 255, 178)),
    35: ('Potato weed', (207, 255, 178)),
    36: ('German chamomile', (188, 255, 178)),
    37: ('Saltbush', (178, 255, 188)),
    38: ('Creeping thistle', (178, 255, 207)),
    39: ('Field milk thistle', (178, 255, 226)),
    40: ('Purslane', (178, 255, 245)),
    41: ('Black nightshade', (178, 245, 255)),
    42: ('Mercuries', (178, 226, 255)),
    43: ('Spurge', (178, 207, 255)),
    44: ('Pale persicaria', (178, 188, 255)),
    45: ('Geraniums', (188, 178, 255)),
    46: ('Cleavers', (207, 178, 255)),
    47: ('Whitetop', (226, 178, 255)),
    48: ('Meadow-grass', (245, 178, 255)),
    49: ('Frosted orach', (255, 178, 245)),
    50: ('Black horehound', (255, 178, 226)),
    51: ('Shepherds purse', (255, 178, 207)),
    52: ('Field bindweed', (255, 178, 188)),
    53: ('Common mugwort', (255, 194, 178)),
    54: ('Hedge mustard', (255, 213, 178)),
    55: ('Groundsel', (255, 219, 178)),
    56: ('Speedwell', (255, 232, 178)),
    57: ('Broadleaf plantain', (255, 238, 178)),
    58: ('White ball-mustard', (255, 251, 178)),
    59: ('Peppermint', (255, 212, 0)),
    60: ('Field pennycress', (239, 255, 178)),
    61: ('Corn spurry', (233, 255, 178)),
    62: ('Purple crabgrass', (220, 255, 178)),
    63: ('Common fumitory', (214, 255, 178)),
    64: ('Ivy-leaved speedwell', (201, 255, 178)),
    65: ('Annual meadow grass', (195, 255, 178)),
    66: ('Redshank', (182, 255, 178)),
    67: ('Common hemp-nettle', (178, 255, 194)),
    68: ('Rough meadow-grass', (178, 255, 200)),
    69: ('Green bristlegrass', (178, 255, 213)),
    70: ('Small geranium', (178, 255, 220)),
    71: ('Cornflower', (178, 255, 232)),
    72: ('Common corn-cockle', (178, 255, 238)),
    73: ('Creeping crowfoot', (178, 255, 251)),
    74: ('Wall barley', (178, 239, 255)),
    75: ('Annual fescue', (178, 233, 255)),
    76: ('Purple dead-nettle', (178, 220, 255)),
    77: ('Ribwort plantain', (178, 214, 255)),
    78: ('Pineappleweed', (178, 201, 255)),
    79: ('Common chickweed', (178, 195, 255)),
    80: ('Hedge mustard', (178, 182, 255)),
    81: ('Soft brome', (194, 178, 255)),
    82: ('Wild pansy', (200, 178, 255)),
    83: ('Yellow rocket', (213, 178, 255)),
    84: ('Common wild oat', (219, 178, 255)),
    85: ('Red poppy', (232, 178, 255)),
    86: ('Rye brome', (238, 178, 255)),
    87: ('Knotgrass', (251, 178, 255)),
    88: ('Prickly lettuce', (255, 178, 239)),
    89: ('Copse-bindweed', (255, 178, 233)),
    90: ('Manyseeds', (255, 178, 220)),
    91: ('Common buckwheat', (255, 178, 214)),
    92: ('Chives', (212, 255, 0)),
    93: ('Garlic', (127, 255, 0)),
    94: ('Soybean', (42, 255, 0)),
    95: ('Wild carrot', (244, 255, 0)),
    96: ('Field mustard', (159, 255, 0)),
    97: ('Giant fennel', (74, 255, 0)),
    98: ('Common horsetail', (10, 255, 0)),
    99: ('Common dandelion', (202, 255, 0)),
    255: ('Vegetation', (128, 128, 128))})

DATASETS['Fine24'] = Dataset({
    0: ('Maize', (255, 0, 0), [1, 2, 3, 4, 5, 6]),
    1: ('Sugar beet', (255, 85, 0), [7, 8, 9, 10, 11, 12]),
    2: ('Soy', (42, 255, 0), [94]),
    3: ('Sunflower', (85, 0, 255), [24]),
    4: ('Potato', (0, 255, 85), [18]),
    5: ('Pea', (255, 170, 0), [13]),
    6: ('Bean', (255, 0, 170), [26, 27]),
    7: ('Pumpkin', (170, 255, 0), [15]),
    8: ('Grasses', (255, 226, 178), [31, 48, 62, 65, 68, 69, 74, 75, 81, 84, 86]),
    9: ('Amaranth', (255, 245, 178), [32]),
    10: ('Goosefoot', (226, 255, 178), [29, 33, 37, 49]),
    11: ('Knotweed', (255, 207, 178), [30, 44, 66, 87, 89, 91]),
    12: ('Corn spurry', (233, 255, 178), [61]),
    13: ('Chickweed', (178, 195, 255), [79]),
    14: ('Solanales', (226, 255, 178), [34, 41, 52]),
    15: ('Potato weed', (207, 255, 178), [35]),
    16: ('Chamomile', (188, 255, 178), [36, 78]),
    17: ('Thistle', (178, 255, 207), [38, 39, 71, 72, 88]),
    18: ('Mercuries', (178, 226, 255), [42]),
    19: ('Geranium', (188, 178, 255), [45, 70]),
    20: ('Crucifer', (239, 255, 178), [47, 51, 54, 58, 60, 80, 83, 96]),
    21: ('Poppy', (214, 255, 178), [22, 63, 85]),
    22: ('Plantago', (255, 232, 178), [56, 57, 64, 77]),
    23: ('Labiate', (255, 212, 0), [50, 59, 67, 76])})

DATASETS['CropsOrWeed9'] = Dataset({
    0: ('Maize', (255, 0, 0), [1, 2, 3, 4, 5, 6]),
    1: ('Sugar beet', (255, 85, 0), [7, 8, 9, 10, 11, 12]),
    2: ('Soy', (42, 255, 0), [94]),
    3: ('Sunflower', (85, 0, 255), [24]),
    4: ('Potato', (0, 255, 85), [18]),
    5: ('Pea', (255, 170, 0), [13]),
    6: ('Bean', (255, 0, 170), [26, 27]),
    7: ('Pumpkin', (170, 255, 0), [15]),
    8: ('Weed', (128, 255, 192),
        [31, 48, 62, 65, 68, 69, 74, 75, 81, 84, 86, 32, 29, 33, 37, 49, 30, 44, 66, 87, 89, 91, 61, 79, 34, 41, 52, 35,
         36, 78, 38, 39, 71, 72, 88, 42, 45, 70, 47, 51, 54, 58, 60, 80, 83, 96, 22, 63, 85, 56, 57, 64, 77, 50, 59, 67,
         76])})

DATASETS['Maize2'] = Dataset({
    0: ('Maize', (255, 0, 0), [1, 2, 3, 4, 5, 6]),
    1: ('Other', (128, 255, 192), [*range(7, 100)])})

DATASETS['Maize1'] = Dataset({
    0: ('Maize', (255, 0, 0), [1, 2, 3, 4, 5, 6])})

DATASETS['SugarBeet2'] = Dataset({
    0: ('Sugar beet', (255, 85, 0), [7, 8, 9, 10, 11, 12]),
    1: ('Other', (128, 255, 192), [*range(1, 7)] + [*range(13, 100)])})

DATASETS['SugarBeet1'] = Dataset({
    0: ('Sugar beet', (255, 85, 0), [7, 8, 9, 10, 11, 12])})

DATASETS['Soy2'] = Dataset({
    0: ('Soy', (42, 255, 0), [94]),
    1: ('Other', (128, 255, 192), [*range(1, 94)] + [*range(95, 100)])})

DATASETS['Soy1'] = Dataset({
    0: ('Soy', (42, 255, 0), [94])})

DATASETS['Sunflower2'] = Dataset({
    0: ('Sunflower', (85, 0, 255), [24]),
    1: ('Other', (128, 255, 192), [*range(1, 24)] + [*range(25, 100)])})

DATASETS['Sunflower1'] = Dataset({
    0: ('Sunflower', (85, 0, 255), [24])})

DATASETS['Potato2'] = Dataset({
    0: ('Potato', (0, 255, 85), [18]),
    1: ('Other', (128, 255, 192), [*range(1, 18)] + [*range(19, 100)])})

DATASETS['Potato1'] = Dataset({
    0: ('Potato', (0, 255, 85), [18])})

DATASETS['Pea2'] = Dataset({
    0: ('Pea', (255, 170, 0), [13]),
    1: ('Other', (128, 255, 192), [*range(1, 13)] + [*range(14, 100)])})

DATASETS['Pea1'] = Dataset({
    0: ('Pea', (255, 170, 0), [13])})

DATASETS['Bean2'] = Dataset({
    0: ('Bean', (255, 0, 170), [26, 27]),
    1: ('Other', (128, 255, 192), [*range(1, 26)] + [*range(28, 100)])})

DATASETS['Bean1'] = Dataset({
    0: ('Bean', (255, 0, 170), [26, 27])})

DATASETS['Pumpkin2'] = Dataset({
    0: ('Pumpkin', (170, 255, 0), [15]),
    1: ('Other', (128, 255, 192), [*range(1, 15)] + [*range(16, 100)])})

DATASETS['Pumpkin1'] = Dataset({
    0: ('Pumpkin', (170, 255, 0), [15])})

DATASETS['CropOrWeed2'] = Dataset({
    0: ('Crop', (0, 255, 0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 94, 24, 18, 13, 26, 27, 15]),
    1: ('Weed', (128, 255, 192),
        [31, 48, 62, 65, 68, 69, 74, 75, 81, 84, 86, 32, 29, 33, 37, 49, 30, 44, 66, 87, 89, 91, 61, 79, 34, 41, 52, 35,
         36, 78, 38, 39, 71, 72, 88, 42, 45, 70, 47, 51, 54, 58, 60, 80, 83, 96, 22, 63, 85, 56, 57, 64, 77, 50, 59, 67,
         76])})

DATASETS['Coarse1'] = Dataset({
    0: ('Vegetation', (255, 0, 0),
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
         59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
         87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 255])})
