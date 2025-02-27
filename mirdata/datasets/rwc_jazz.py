# -*- coding: utf-8 -*-
"""RWC Jazz Dataset Loader.

.. admonition:: Dataset Info
    :class: dropdown

    The Jazz Music Database consists of 50 pieces:

    - **Instrumentation variations:** 35 pieces (5 pieces × 7 instrumentations).

        The instrumentation-variation pieces were recorded to obtain different versions
        of the same piece; i.e., different arrangements performed by different player
        instrumentations. Five standard-style jazz pieces were originally composed
        and then performed in modern-jazz style using the following seven instrumentations:

        1. Piano solo
        2. Guitar solo
        3. Duo: Vibraphone + Piano, Flute + Piano, and Piano + Bass
        4. Piano trio: Piano + Bass + Drums
        5. Piano trio + Trumpet or Tenor saxophone
        6. Octet: Piano trio + Guitar + Alto saxophone + Baritone saxophone + Tenor saxophone × 2
        7. Piano trio + Vibraphone or Flute

    - **Style variations:** 9 pieces

        The style-variation pieces were recorded to represent various styles of jazz.
        They include four well-known public-domain pieces and consist of
        
        1. Vocal jazz: 2 pieces (including "Aura Lee")
        2. Big band jazz: 2 pieces (including "The Entertainer")
        3. Modal jazz: 2 pieces
        4. Funky jazz: 2 pieces (including "Silent Night")
        5. Free jazz: 1 piece (including "Joyful, Joyful, We Adore Thee")

    - **Fusion (crossover):** 6 pieces

        The fusion pieces were recorded to obtain music that combines elements of jazz
        with other styles such as popular, rock, and latin. They include music with an
        eighth-note feel, music with a sixteenth-note feel, and Latin jazz music.

    For more details, please visit: https://staff.aist.go.jp/m.goto/RWC-MDB/rwc-mdb-j.html

"""
import csv
import logging
import os

import librosa

from mirdata import download_utils
from mirdata import jams_utils
from mirdata import core

# these functions are identical for all rwc datasets
from mirdata.datasets.rwc_classical import (
    load_beats,
    load_sections,
    load_audio,
    _duration_to_sec,
    LICENSE_INFO,
)

BIBTEX = """@inproceedings{goto2002rwc,
  title={RWC Music Database: Popular, Classical and Jazz Music Databases.},
  author={Goto, Masataka and Hashiguchi, Hiroki and Nishimura, Takuichi and Oka, Ryuichi},
  booktitle={3rd International Society for Music Information Retrieval Conference},
  year={2002},
  series={ISMIR},
}"""
REMOTES = {
    "metadata": download_utils.RemoteFileMetadata(
        filename="master.zip",
        url="https://github.com/magdalenafuentes/metadata/archive/master.zip",
        checksum="7dbe87fedbaaa1f348625a2af1d78030",
        destination_dir="",
    ),
    "annotations_beat": download_utils.RemoteFileMetadata(
        filename="AIST.RWC-MDB-J-2001.BEAT.zip",
        url="https://staff.aist.go.jp/m.goto/RWC-MDB/AIST-Annotation/AIST.RWC-MDB-J-2001.BEAT.zip",
        checksum="b483853da05d0fff3992879f7729bcb4",
        destination_dir="annotations",
    ),
    "annotations_sections": download_utils.RemoteFileMetadata(
        filename="AIST.RWC-MDB-J-2001.CHORUS.zip",
        url="https://staff.aist.go.jp/m.goto/RWC-MDB/AIST-Annotation/AIST.RWC-MDB-J-2001.CHORUS.zip",
        checksum="44afcf7f193d7e48a7d99e7a6f3ed39d",
        destination_dir="annotations",
    ),
}
DOWNLOAD_INFO = """
    Unfortunately the audio files of the RWC-Jazz dataset are not available
    for download. If you have the RWC-Jazz dataset, place the contents into a
    folder called RWC-Jazz with the following structure:
        > RWC-Jazz/
            > annotations/
            > audio/rwc-j-m0i with i in [1 .. 4]
            > metadata-master/
    and copy the RWC-Jazz folder to {}
"""


def _load_metadata(data_home):

    metadata_path = os.path.join(data_home, "metadata-master", "rwc-j.csv")

    if not os.path.exists(metadata_path):
        logging.info(
            "Metadata file {} not found.".format(metadata_path)
            + "You can download the metadata file by running download()"
        )
        return None

    with open(metadata_path, "r") as fhandle:
        dialect = csv.Sniffer().sniff(fhandle.read(1024))
        fhandle.seek(0)
        reader = csv.reader(fhandle, dialect)
        raw_data = []
        for line in reader:
            if line[0] != "Piece No.":
                raw_data.append(line)

    metadata_index = {}
    for line in raw_data:
        if line[0] == "Piece No.":
            continue
        p = "00" + line[0].split(".")[1][1:]
        track_id = "RM-J{}".format(p[len(p) - 3 :])

        metadata_index[track_id] = {
            "piece_number": line[0],
            "suffix": line[1],
            "track_number": line[2],
            "title": line[3],
            "artist": line[4],
            "duration": _duration_to_sec(line[5]),
            "variation": line[6],
            "instruments": line[7],
        }

    metadata_index["data_home"] = data_home

    return metadata_index


DATA = core.LargeData("rwc_jazz_index.json", _load_metadata)


class Track(core.Track):
    """rwc_jazz Track class

    Args:
        track_id (str): track id of the track

    Attributes:
        artist (str): Artist name
        audio_path (str): path of the audio file
        beats_path (str): path of the beat annotation file
        duration (float): Duration of the track in seconds
        instruments (str): list of used instruments.
        piece_number (str): Piece number of this Track, [1-50]
        sections_path (str): path of the section annotation file
        suffix (str): M01-M04
        title (str): Title of The track.
        track_id (str): track id
        track_number (str): CD track number of this Track
        variation (str):  style variations

    Cached Properties:
        sections (SectionData): human-labeled section data
        beats (BeatData): human-labeled beat data

    """

    def __init__(self, track_id, data_home):
        if track_id not in DATA.index["tracks"]:
            raise ValueError("{} is not a valid track ID in RWC-Jazz".format(track_id))

        self.track_id = track_id
        self._data_home = data_home

        self._track_paths = DATA.index["tracks"][track_id]
        self.sections_path = os.path.join(
            self._data_home, self._track_paths["sections"][0]
        )
        self.beats_path = os.path.join(self._data_home, self._track_paths["beats"][0])

        metadata = DATA.metadata(data_home)
        if metadata is not None and track_id in metadata:
            self._track_metadata = metadata[track_id]
        else:
            self._track_metadata = {
                "piece_number": None,
                "suffix": None,
                "track_number": None,
                "title": None,
                "artist": None,
                "duration": None,
                "variation": None,
                "instruments": None,
            }

        self.audio_path = os.path.join(self._data_home, self._track_paths["audio"][0])

        self.piece_number = self._track_metadata["piece_number"]
        self.suffix = self._track_metadata["suffix"]
        self.track_number = self._track_metadata["track_number"]
        self.title = self._track_metadata["title"]
        self.artist = self._track_metadata["artist"]
        self.duration = self._track_metadata["duration"]
        self.variation = self._track_metadata["variation"]
        self.instruments = self._track_metadata["instruments"]

    @core.cached_property
    def sections(self):
        return load_sections(self.sections_path)

    @core.cached_property
    def beats(self):
        return load_beats(self.beats_path)

    @property
    def audio(self):
        """The track's audio

        Returns:
           * np.ndarray - audio signal
           * float - sample rate

        """
        return load_audio(self.audio_path)

    def to_jams(self):
        """Get the track's data in jams format

        Returns:
            jams.JAMS: the track's data in jams format

        """
        return jams_utils.jams_converter(
            audio_path=self.audio_path,
            beat_data=[(self.beats, None)],
            section_data=[(self.sections, None)],
            metadata=self._track_metadata,
        )


@core.docstring_inherit(core.Dataset)
class Dataset(core.Dataset):
    """
    The rwc_jazz dataset
    """

    def __init__(self, data_home=None):
        super().__init__(
            data_home,
            index=DATA.index,
            name="rwc_jazz",
            track_object=Track,
            bibtex=BIBTEX,
            remotes=REMOTES,
            download_info=DOWNLOAD_INFO,
            license_info=LICENSE_INFO,
        )

    @core.copy_docs(load_audio)
    def load_audio(self, *args, **kwargs):
        return load_audio(*args, **kwargs)

    @core.copy_docs(load_sections)
    def load_sections(self, *args, **kwargs):
        return load_sections(*args, **kwargs)

    @core.copy_docs(load_beats)
    def load_beats(self, *args, **kwargs):
        return load_beats(*args, **kwargs)
