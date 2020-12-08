# -*- coding: utf-8 -*-

import numpy as np

from mirdata.datasets import queen
from mirdata import utils
from tests.test_utils import run_track_tests


def test_track():
    default_trackid = "0"
    data_home = "tests/resources/mir_datasets/Queen"
    track = queen.Track(default_trackid, data_home=data_home)

    expected_attributes = {
        "audio_path": "tests/resources/mir_datasets/Queen/audio/Greatest Hits I/01 Bohemian Rhapsody.flac",
        "chords_path": "tests/resources/mir_datasets/Queen/"
                       "annotations/chordlab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab",
        "keys_path": "tests/resources/mir_datasets/Queen/"
                     + "annotations/keylab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab",
        "sections_path": "tests/resources/mir_datasets/Queen/"
                         + "annotations/seglab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab",
        "title": "01 Bohemian Rhapsody",
        "track_id": "0",
    }

    expected_property_types = {
        "chords": utils.ChordData,
        "key": utils.KeyData,
        "sections": utils.SectionData,
    }

    run_track_tests(track, expected_attributes, expected_property_types)

    audio, sr = track.audio
    assert sr == 44100, "sample rate {} is not 44100".format(sr)
    assert audio.shape == (15792504,), "audio shape {} was not (15792504,)".format(
        audio.shape
    )


def test_to_jams():
    data_home = "tests/resources/mir_datasets/Queen"
    track = queen.Track("0", data_home=data_home)
    jam = track.to_jams()
    segments = jam.search(namespace="segment")[0]["data"]

    assert [segment.time for segment in segments] == [
        0.0, 0.4, 49.072, 108.392, 156.32, 183.414, 248.621, 296.13, 354.92
    ], "segment time does not match expected"

    assert [segment.duration for segment in segments] == [
        0.4, 48.672000000000004, 59.31999999999999, 47.928, 27.093999999999994, 65.20700000000002, 47.508999999999986,
        58.79000000000002, 3.3729999999999905
    ], "segment duration does not match expected"
    assert [segment.value for segment in segments] == [
        'silence', 'intro', 'verse', 'verse', 'instrumental_solo', 'section_y', 'section_z', 'outro', 'silence'
    ], "segment value does not match expected"
    assert [segment.confidence for segment in segments] == [
        None, None, None, None, None, None, None, None, None
    ], "segment confidence does not match expected"

    chords = jam.search(namespace="chord")[0]["data"]
    assert [chord.time for chord in chords] == [
        0.0, 0.459, 4.122, 4.911, 5.304, 7.576, 8.847, 9.694, 11.378, 12.237, 12.608, 15.07, 18.582, 22.241, 25.489,
        28.932, 32.276, 33.097, 33.897, 34.742, 35.585, 36.409, 37.175, 38.041, 38.839, 40.671, 42.375, 44.048, 45.697,
        49.16, 55.96, 59.327, 62.76, 67.802, 69.521, 72.921, 76.324, 78.073, 78.809, 79.748, 81.444, 82.28, 83.141,
        85.702, 86.586, 89.999, 91.243, 91.723, 92.531, 93.383, 96.712, 98.408, 100.112, 101.816, 103.492, 105.21,
        106.026, 106.823, 107.674, 108.519, 115.436, 118.852, 122.284, 127.343, 128.998, 132.447, 135.814, 137.546,
        138.398, 139.254, 140.99, 141.808, 142.662, 145.277, 146.093, 149.485, 150.779, 151.193, 151.993, 152.893,
        156.268, 157.976, 159.637, 163.076, 164.356, 164.778, 165.604, 166.459, 169.86, 171.588, 173.308, 176.669,
        177.933, 178.382, 179.238, 180.02, 181.706, 182.597, 183.397, 186.782, 187.174, 187.615, 188.056, 188.451,
        188.846, 189.263, 189.658, 190.053, 190.424, 190.866, 191.284, 191.678, 192.073, 192.468, 192.863, 193.276,
        194.065, 194.855, 195.667, 196.48, 196.896, 203.453, 203.851, 204.246, 204.664, 205.059, 205.477, 205.895,
        206.313, 206.728, 207.123, 207.541, 207.913, 208.307, 208.679, 209.074, 209.468, 209.863, 210.722, 211.488,
        212.324, 213.174, 213.546, 213.917, 214.335, 214.707, 215.078, 215.496, 215.891, 216.332, 216.727, 217.098,
        217.493, 217.911, 219.336, 220.532, 222.528, 223.713, 225.756, 230.876, 232.281, 232.689, 233.014, 233.386,
        233.781, 234.175, 234.617, 236.636, 237.731, 238.608, 239.421, 240.233, 241.0, 241.812, 248.662, 253.91,
        255.633, 256.539, 257.398, 258.257, 259.184, 260.903, 261.785, 262.644, 263.503, 264.417, 265.245, 267.02,
        268.738, 270.48, 272.221, 273.986, 274.868, 275.714, 276.61, 277.469, 282.724, 284.419, 285.315, 286.23,
        287.955, 289.75, 296.008, 297.68, 299.398, 301.093, 301.859, 302.718, 303.531, 304.344, 305.157, 306.016,
        307.664, 309.383, 311.124, 312.842, 314.607, 316.325, 317.997, 319.785, 321.573, 323.804, 327.502, 329.096,
        330.629, 332.161, 333.647, 335.041, 336.434, 338.013, 339.87, 342.024, 344.082, 344.924, 345.815, 346.767,
        348.578, 353.011
    ], "chord time does not match expected"
    assert [chord.duration for chord in chords] == [
        0.459, 3.663, 0.7889999999999997, 0.3930000000000007, 2.2719999999999994, 1.271, 0.8470000000000013,
        1.6839999999999993, 0.859, 0.37100000000000044, 2.4619999999999997, 3.5120000000000005, 3.658999999999999,
        3.248000000000001, 3.442999999999998, 3.3440000000000047, 0.820999999999998, 0.7999999999999972,
        0.8449999999999989, 0.8430000000000035, 0.8239999999999981, 0.7659999999999982, 0.8659999999999997,
        0.7980000000000018, 1.8320000000000007, 1.7040000000000006, 1.6730000000000018, 1.649000000000001,
        3.462999999999994, 6.800000000000004, 3.3669999999999973, 3.433, 5.042000000000009, 1.718999999999994,
        3.4000000000000057, 3.4029999999999916, 1.7489999999999952, 0.7360000000000042, 0.9390000000000072,
        1.695999999999998, 0.8359999999999985, 0.8610000000000042, 2.560999999999993, 0.8840000000000003,
        3.4129999999999967, 1.2439999999999998, 0.480000000000004, 0.8080000000000069, 0.8519999999999897,
        3.3290000000000077, 1.695999999999998, 1.7039999999999935, 1.7040000000000077, 1.676000000000002,
        1.7179999999999893, 0.8160000000000025, 0.796999999999997, 0.8510000000000133, 0.8449999999999989,
        6.917000000000002, 3.415999999999997, 3.432000000000002, 5.0589999999999975, 1.654999999999987,
        3.4490000000000123, 3.3669999999999902, 1.7319999999999993, 0.8520000000000039, 0.8559999999999945,
        1.7360000000000184, 0.8179999999999836, 0.8540000000000134, 2.6149999999999807, 0.8160000000000025,
        3.3920000000000243, 1.2939999999999827, 0.4140000000000157, 0.799999999999983, 0.9000000000000057, 3.375,
        1.7079999999999984, 1.6610000000000014, 3.438999999999993, 1.2800000000000011, 0.42199999999999704,
        0.8260000000000218, 0.8549999999999898, 3.4010000000000105, 1.7279999999999802, 1.7199999999999989,
        3.3610000000000184, 1.2639999999999816, 0.4490000000000123, 0.8559999999999945, 0.7820000000000107,
        1.6859999999999786, 0.8910000000000196, 0.799999999999983, 3.3850000000000193, 0.3919999999999959,
        0.4410000000000025, 0.4410000000000025, 0.3949999999999818, 0.39500000000001023, 0.4170000000000016,
        0.3949999999999818, 0.39500000000001023, 0.3710000000000093, 0.4420000000000073, 0.41799999999997794,
        0.39400000000000546, 0.39500000000001023, 0.3949999999999818, 0.39500000000001023, 0.4130000000000109,
        0.7889999999999873, 0.789999999999992, 0.8120000000000118, 0.8129999999999882, 0.4159999999999968,
        6.557000000000016, 0.39799999999999613, 0.39500000000001023, 0.41799999999997794, 0.39500000000001023,
        0.41800000000000637, 0.41800000000000637, 0.41799999999997794, 0.41500000000002046, 0.3949999999999818,
        0.41800000000000637, 0.3720000000000141, 0.39399999999997704, 0.3720000000000141, 0.39500000000001023,
        0.39399999999997704, 0.39500000000001023, 0.8590000000000089, 0.7659999999999911, 0.8360000000000127,
        0.8499999999999943, 0.3719999999999857, 0.3710000000000093, 0.41800000000000637, 0.3719999999999857,
        0.3710000000000093, 0.41800000000000637, 0.3949999999999818, 0.4410000000000025, 0.39500000000001023,
        0.3710000000000093, 0.3949999999999818, 0.41800000000000637, 1.4250000000000114, 1.195999999999998,
        1.995999999999981, 1.1850000000000023, 2.0430000000000064, 5.1200000000000045, 1.4050000000000011,
        0.40799999999998704, 0.32500000000001705, 0.3719999999999857, 0.39500000000001023, 0.39400000000000546,
        0.44199999999997885, 2.0190000000000055, 1.0949999999999989, 0.8770000000000095, 0.8129999999999882,
        0.8120000000000118, 0.7669999999999959, 0.8120000000000118, 6.849999999999994, 5.2479999999999905,
        1.7230000000000132, 0.9059999999999775, 0.8590000000000373, 0.8589999999999804, 0.9270000000000209,
        1.718999999999994, 0.882000000000005, 0.8589999999999804, 0.8589999999999804, 0.9139999999999873,
        0.8280000000000314, 1.7749999999999773, 1.7180000000000177, 1.7420000000000186, 1.7409999999999854,
        1.7649999999999864, 0.882000000000005, 0.8460000000000036, 0.896000000000015, 0.8589999999999804,
        5.2549999999999955, 1.6949999999999932, 0.896000000000015, 0.9150000000000205, 1.724999999999966,
        1.795000000000016, 6.257999999999981, 1.6720000000000255, 1.7180000000000177, 1.6949999999999932,
        0.7659999999999627, 0.8590000000000373, 0.8129999999999882, 0.8129999999999882, 0.8129999999999882,
        0.8590000000000373, 1.6479999999999677, 1.718999999999994, 1.7410000000000423, 1.717999999999961,
        1.7650000000000432, 1.717999999999961, 1.6720000000000255, 1.788000000000011, 1.787999999999954,
        2.2309999999999945, 3.698000000000036, 1.593999999999994, 1.5330000000000155, 1.5319999999999823,
        1.48599999999999, 1.3940000000000055, 1.393000000000029, 1.5789999999999509, 1.8570000000000277,
        2.1539999999999964, 2.0579999999999927, 0.8419999999999845, 0.8910000000000196, 0.9519999999999982,
        1.8109999999999786, 4.43300000000005, 5.281999999999982
    ], "chord duration does not match expected"
    assert [chord.value for chord in chords] == [
        'N', 'Bb:maj6', 'C:7', 'Bb:maj6', 'C:7', 'F:7', 'C:min7', 'F:7', 'Bb:maj', 'C:min7', 'Bb:maj', 'G:min', 'Bb:7',
        'Eb:maj', 'C:min', 'F:7', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'Eb:maj', 'Bb/3',
        'C#:dim', 'F/5', 'F:maj', 'Bb:maj', 'Bb:maj', 'G:min', 'C:min', 'F:maj', 'Bb:maj', 'G:min', 'C:min7', 'B:aug',
        'Eb/5', 'F/3', 'F:min/b3', 'G:(1)', 'Eb:maj', 'Bb/3', 'C:min', 'F:min', 'F:min/7', 'F:min/b7', 'F:min/6',
        'Bb:maj', 'Eb:maj', 'Bb/3', 'C:min', 'Ab:min', 'Eb:maj', 'Ab:maj', 'Eb:maj', 'Eb:dim', 'F:min7', 'Bb:maj',
        'Bb:maj', 'G:min', 'C:min', 'F:maj', 'Bb:maj', 'G:min', 'C:min7', 'B:aug', 'Eb/5', 'F/3', 'F:min/3', 'G:(1)',
        'Eb:maj', 'Bb/3', 'C:min', 'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Bb:maj', 'Eb:maj', 'Bb/3', 'C:min',
        'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Bb:7', 'Eb:maj', 'G:min/5', 'C:min', 'F:min', 'F:min/7', 'F:min/b7',
        'F:min/6', 'Db:maj', 'Db/7', 'Bb:min', 'A:maj', 'D/5', 'A:maj', 'A:dim', 'A:maj', 'D/5', 'A:maj', 'A:dim',
        'A:maj', 'D/5', 'A:maj', 'D/5', 'A:maj', 'A:dim', 'A:maj', 'D/5', 'A:maj', 'Db/5', 'Ab:maj', 'C/5', 'E:maj',
        'A:maj', 'N', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'Ab/5', 'Eb:maj', 'Eb:dim', 'Eb:maj',
        'Ab/5', 'Eb:maj', 'Eb:dim', 'Eb:maj', 'Ab:maj', 'Eb/3', 'F:maj', 'Bb:maj', 'Ab:maj', 'Eb/3', 'F#:dim', 'F:min7',
        'B:maj', 'Bb:maj', 'A:maj', 'Bb:maj', 'B:maj', 'Bb:maj', 'A:maj', 'Bb:maj', 'Eb:maj', 'Bb:maj', 'Eb:maj',
        'Bb:maj', 'Eb:maj', 'Bb:maj', 'Gb:7', 'B:(5)', 'A', 'D:maj', 'Db:maj', 'Gb:maj', 'Bb:maj', 'Eb:maj', 'Eb:maj',
        'Bb:maj', 'Eb:maj', 'Ab:maj', 'D:maj', 'G:min', 'Bb:maj', 'Eb:maj', 'F:7', 'Bb:7', 'Eb/5', 'Bb:maj', 'Eb:maj',
        'Bb:maj', 'Db:maj', 'Bb:7', 'Eb/5', 'Bb:maj', 'Eb:maj', 'Ab:maj', 'F:min', 'Bb:maj', 'F:min', 'Bb:maj',
        'F:min7', 'Bb:maj', 'F:min7', 'Bb:maj', 'Eb:maj', 'F:7', 'F#', 'Ab', 'B', 'Ab', 'Bb', 'Eb:maj', 'Bb/3', 'C:min',
        'G/3', 'C:min', 'G:7/3', 'C:min', 'Bb:7', 'Eb:maj', 'D:maj', 'G:min', 'Ab:maj', 'Eb:maj', 'C:min', 'G:min',
        'C:min', 'G:min', 'C:min', 'Ab:min', 'Bb:9(11)', 'Eb:maj', 'Ab/5', 'Eb:maj', 'Eb:dim', 'Bb/3', 'Bb:min/b3',
        'C:7', 'C:7(b9)', 'C:7', 'F:maj', 'Bb:maj', 'F/3', 'Ab:dim', 'G:min7', 'F:maj', 'N'
    ], "chord value does not match expected"
    assert [chord.confidence for chord in chords] == [
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None
    ], "chord confidence does not match expected"

    keys = jam.search(namespace="key")[0]["data"]
    assert [key.time for key in keys] == [0.456, 83.139, 108.519, 142.649, 183.411, 206.713,
                                          339.87], "key time does not match expected"
    assert [key.duration for key in keys] == [
        82.68299999999999, 25.38000000000001, 34.129999999999995, 40.762, 23.301999999999992, 133.157,
        13.206000000000017
    ], "key duration does not match expected"
    assert [key.value for key in keys] == [
        'Bb', 'Eb', 'Bb', 'Eb', 'A', 'Eb', 'F'
    ], "key value does not match expected"
    assert [key.confidence for key in keys] == [
        None, None, None, None, None, None, None
    ], "key confidence does not match expected"

    assert (
            jam["file_metadata"]["title"] == '01 Bohemian Rhapsody'
    ), "title does not match expected"
    assert (
            jam["file_metadata"]["artist"] == "The Queen"
    ), "artist does not match expected"


def test_load_chords():
    chords_path = "tests/resources/mir_datasets/Queen/annotations/chordlab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab"
    chord_data = queen.load_chords(chords_path)

    assert type(chord_data) == utils.ChordData
    assert type(chord_data.intervals) == np.ndarray
    assert type(chord_data.labels) == list

    assert np.array_equal(
        chord_data.intervals[:, 0],
        np.array([0., 0.459, 4.122, 4.911, 5.304, 7.576, 8.847,
                  9.694, 11.378, 12.237, 12.608, 15.07, 18.582, 22.241,
                  25.489, 28.932, 32.276, 33.097, 33.897, 34.742, 35.585,
                  36.409, 37.175, 38.041, 38.839, 40.671, 42.375, 44.048,
                  45.697, 49.16, 55.96, 59.327, 62.76, 67.802, 69.521,
                  72.921, 76.324, 78.073, 78.809, 79.748, 81.444, 82.28,
                  83.141, 85.702, 86.586, 89.999, 91.243, 91.723, 92.531,
                  93.383, 96.712, 98.408, 100.112, 101.816, 103.492, 105.21,
                  106.026, 106.823, 107.674, 108.519, 115.436, 118.852, 122.284,
                  127.343, 128.998, 132.447, 135.814, 137.546, 138.398, 139.254,
                  140.99, 141.808, 142.662, 145.277, 146.093, 149.485, 150.779,
                  151.193, 151.993, 152.893, 156.268, 157.976, 159.637, 163.076,
                  164.356, 164.778, 165.604, 166.459, 169.86, 171.588, 173.308,
                  176.669, 177.933, 178.382, 179.238, 180.02, 181.706, 182.597,
                  183.397, 186.782, 187.174, 187.615, 188.056, 188.451, 188.846,
                  189.263, 189.658, 190.053, 190.424, 190.866, 191.284, 191.678,
                  192.073, 192.468, 192.863, 193.276, 194.065, 194.855, 195.667,
                  196.48, 196.896, 203.453, 203.851, 204.246, 204.664, 205.059,
                  205.477, 205.895, 206.313, 206.728, 207.123, 207.541, 207.913,
                  208.307, 208.679, 209.074, 209.468, 209.863, 210.722, 211.488,
                  212.324, 213.174, 213.546, 213.917, 214.335, 214.707, 215.078,
                  215.496, 215.891, 216.332, 216.727, 217.098, 217.493, 217.911,
                  219.336, 220.532, 222.528, 223.713, 225.756, 230.876, 232.281,
                  232.689, 233.014, 233.386, 233.781, 234.175, 234.617, 236.636,
                  237.731, 238.608, 239.421, 240.233, 241., 241.812, 248.662,
                  253.91, 255.633, 256.539, 257.398, 258.257, 259.184, 260.903,
                  261.785, 262.644, 263.503, 264.417, 265.245, 267.02, 268.738,
                  270.48, 272.221, 273.986, 274.868, 275.714, 276.61, 277.469,
                  282.724, 284.419, 285.315, 286.23, 287.955, 289.75, 296.008,
                  297.68, 299.398, 301.093, 301.859, 302.718, 303.531, 304.344,
                  305.157, 306.016, 307.664, 309.383, 311.124, 312.842, 314.607,
                  316.325, 317.997, 319.785, 321.573, 323.804, 327.502, 329.096,
                  330.629, 332.161, 333.647, 335.041, 336.434, 338.013, 339.87,
                  342.024, 344.082, 344.924, 345.815, 346.767, 348.578, 353.011])
    )
    assert np.array_equal(
        chord_data.intervals[:, 1],
        np.array([0.459, 4.122, 4.911, 5.304, 7.576, 8.847, 9.694,
                  11.378, 12.237, 12.608, 15.07, 18.582, 22.241, 25.489,
                  28.932, 32.276, 33.097, 33.897, 34.742, 35.585, 36.409,
                  37.175, 38.041, 38.839, 40.671, 42.375, 44.048, 45.697,
                  49.16, 55.96, 59.327, 62.76, 67.802, 69.521, 72.921,
                  76.324, 78.073, 78.809, 79.748, 81.444, 82.28, 83.141,
                  85.702, 86.586, 89.999, 91.243, 91.723, 92.531, 93.383,
                  96.712, 98.408, 100.112, 101.816, 103.492, 105.21, 106.026,
                  106.823, 107.674, 108.519, 115.436, 118.852, 122.284, 127.343,
                  128.998, 132.447, 135.814, 137.546, 138.398, 139.254, 140.99,
                  141.808, 142.662, 145.277, 146.093, 149.485, 150.779, 151.193,
                  151.993, 152.893, 156.268, 157.976, 159.637, 163.076, 164.356,
                  164.778, 165.604, 166.459, 169.86, 171.588, 173.308, 176.669,
                  177.933, 178.382, 179.238, 180.02, 181.706, 182.597, 183.397,
                  186.782, 187.174, 187.615, 188.056, 188.451, 188.846, 189.263,
                  189.658, 190.053, 190.424, 190.866, 191.284, 191.678, 192.073,
                  192.468, 192.863, 193.276, 194.065, 194.855, 195.667, 196.48,
                  196.896, 203.453, 203.851, 204.246, 204.664, 205.059, 205.477,
                  205.895, 206.313, 206.728, 207.123, 207.541, 207.913, 208.307,
                  208.679, 209.074, 209.468, 209.863, 210.722, 211.488, 212.324,
                  213.174, 213.546, 213.917, 214.335, 214.707, 215.078, 215.496,
                  215.891, 216.332, 216.727, 217.098, 217.493, 217.911, 219.336,
                  220.532, 222.528, 223.713, 225.756, 230.876, 232.281, 232.689,
                  233.014, 233.386, 233.781, 234.175, 234.617, 236.636, 237.731,
                  238.608, 239.421, 240.233, 241., 241.812, 248.662, 253.91,
                  255.633, 256.539, 257.398, 258.257, 259.184, 260.903, 261.785,
                  262.644, 263.503, 264.417, 265.245, 267.02, 268.738, 270.48,
                  272.221, 273.986, 274.868, 275.714, 276.61, 277.469, 282.724,
                  284.419, 285.315, 286.23, 287.955, 289.75, 296.008, 297.68,
                  299.398, 301.093, 301.859, 302.718, 303.531, 304.344, 305.157,
                  306.016, 307.664, 309.383, 311.124, 312.842, 314.607, 316.325,
                  317.997, 319.785, 321.573, 323.804, 327.502, 329.096, 330.629,
                  332.161, 333.647, 335.041, 336.434, 338.013, 339.87, 342.024,
                  344.082, 344.924, 345.815, 346.767, 348.578, 353.011, 358.293])
    )
    assert np.array_equal(
        chord_data.labels,
        [
            'N', 'Bb:maj6', 'C:7', 'Bb:maj6', 'C:7', 'F:7', 'C:min7',
            'F:7', 'Bb:maj', 'C:min7', 'Bb:maj', 'G:min', 'Bb:7', 'Eb:maj',
            'C:min', 'F:7', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'B/3', 'Bb/3',
            'A/3', 'Bb/3', 'Eb:maj', 'Bb/3', 'C#:dim', 'F/5', 'F:maj', 'Bb:maj',
            'Bb:maj', 'G:min', 'C:min', 'F:maj', 'Bb:maj', 'G:min', 'C:min7',
            'B:aug', 'Eb/5', 'F/3', 'F:min/b3', 'G:(1)', 'Eb:maj', 'Bb/3', 'C:min',
            'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Bb:maj', 'Eb:maj', 'Bb/3',
            'C:min', 'Ab:min', 'Eb:maj', 'Ab:maj', 'Eb:maj', 'Eb:dim', 'F:min7',
            'Bb:maj', 'Bb:maj', 'G:min', 'C:min', 'F:maj', 'Bb:maj', 'G:min', 'C:min7',
            'B:aug', 'Eb/5', 'F/3', 'F:min/3', 'G:(1)', 'Eb:maj', 'Bb/3', 'C:min',
            'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Bb:maj', 'Eb:maj', 'Bb/3',
            'C:min', 'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Bb:7', 'Eb:maj',
            'G:min/5', 'C:min', 'F:min', 'F:min/7', 'F:min/b7', 'F:min/6', 'Db:maj',
            'Db/7', 'Bb:min', 'A:maj', 'D/5', 'A:maj', 'A:dim', 'A:maj', 'D/5',
            'A:maj', 'A:dim', 'A:maj', 'D/5', 'A:maj', 'D/5', 'A:maj', 'A:dim',
            'A:maj', 'D/5', 'A:maj', 'Db/5', 'Ab:maj', 'C/5', 'E:maj', 'A:maj',
            'N', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'B/3', 'Bb/3', 'A/3', 'Bb/3', 'Ab/5',
            'Eb:maj', 'Eb:dim', 'Eb:maj', 'Ab/5', 'Eb:maj', 'Eb:dim', 'Eb:maj', 'Ab:maj',
            'Eb/3', 'F:maj', 'Bb:maj', 'Ab:maj', 'Eb/3', 'F#:dim', 'F:min7', 'B:maj',
            'Bb:maj', 'A:maj', 'Bb:maj', 'B:maj', 'Bb:maj', 'A:maj', 'Bb:maj', 'Eb:maj',
            'Bb:maj', 'Eb:maj', 'Bb:maj', 'Eb:maj', 'Bb:maj', 'Gb:7', 'B:(5)', 'A', 'D:maj',
            'Db:maj', 'Gb:maj', 'Bb:maj', 'Eb:maj', 'Eb:maj', 'Bb:maj', 'Eb:maj', 'Ab:maj',
            'D:maj', 'G:min', 'Bb:maj', 'Eb:maj', 'F:7', 'Bb:7', 'Eb/5', 'Bb:maj', 'Eb:maj',
            'Bb:maj', 'Db:maj', 'Bb:7', 'Eb/5', 'Bb:maj', 'Eb:maj', 'Ab:maj', 'F:min',
            'Bb:maj', 'F:min', 'Bb:maj', 'F:min7', 'Bb:maj', 'F:min7', 'Bb:maj', 'Eb:maj',
            'F:7', 'F#', 'Ab', 'B', 'Ab', 'Bb', 'Eb:maj', 'Bb/3', 'C:min', 'G/3', 'C:min',
            'G:7/3', 'C:min', 'Bb:7', 'Eb:maj', 'D:maj', 'G:min', 'Ab:maj', 'Eb:maj', 'C:min',
            'G:min', 'C:min', 'G:min', 'C:min', 'Ab:min', 'Bb:9(11)', 'Eb:maj', 'Ab/5', 'Eb:maj',
            'Eb:dim', 'Bb/3', 'Bb:min/b3', 'C:7', 'C:7(b9)', 'C:7', 'F:maj', 'Bb:maj', 'F/3',
            'Ab:dim', 'G:min7', 'F:maj', 'N'
        ])

    assert queen.load_chords(None) is None


def test_load_key():
    key_path = (
        "tests/resources/mir_datasets/Queen/annotations/keylab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab"
    )
    key_data = queen.load_key(key_path)

    assert type(key_data) == utils.KeyData
    assert type(key_data.start_times) == np.ndarray

    assert np.array_equal(key_data.start_times, np.array([0.456, 83.139, 108.519, 142.649, 183.411, 206.713, 339.87]))
    assert np.array_equal(key_data.end_times, np.array([83.139, 108.519, 142.649, 183.411, 206.713, 339.87, 353.076]))
    assert np.array_equal(key_data.keys, np.array(['Bb', 'Eb', 'Bb', 'Eb', 'A', 'Eb', 'F']))

    assert queen.load_key(None) is None


def test_load_sections():
    sections_path = (
        "tests/resources/mir_datasets/Queen/annotations/seglab/Queen/Greatest Hits I/01 Bohemian Rhapsody.lab"
    )
    section_data = queen.load_sections(sections_path)

    assert type(section_data) == utils.SectionData
    assert type(section_data.intervals) == np.ndarray
    assert type(section_data.labels) == list

    assert np.array_equal(section_data.intervals[:, 0], np.array([0., 0.4, 49.072, 108.392, 156.32, 183.414, 248.621,
                                                                  296.13, 354.92]))
    assert np.array_equal(section_data.intervals[:, 1],
                          np.array([0.4, 49.072, 108.392, 156.32, 183.414, 248.621, 296.13,
                                    354.92, 358.293]))
    assert np.array_equal(section_data.labels, np.array(['silence', 'intro', 'verse', 'verse', 'instrumental_solo', 'section_y', 'section_z', 'outro', 'silence']))

    assert queen.load_sections(None) is None
