import sys
import os
import subprocess
import click
import logging
from pymediainfo import MediaInfo
logger = logging.getLogger(__name__)


@click.command()
@click.argument("directory", type=click.Path(exists=True), required=False)
@click.option("--language", "-l", default="ja", help="set language track to keep")
# @click.option("--video", "-V", help="set video source to use")
@click.option("--verbose", "-v", help="increase output verbosity", count=True)
@click.option("--overwrite/--no-overwrite", "-w/", help="allow overwriting of existing files", default=False)
@click.option("--dry-run", "-n", is_flag=True, help="do not write files", default=False)
@click.option("--ffmpeg", "-f", type=click.Path(exists=True, file_okay=True, readable=True),
              help="the ffmpeg binary path you wish to use")
def main(directory, language, verbose, overwrite, dry_run):
    # configure logger
    levels = [logger.WARNING, logger.INFO, logger.DEBUG]
    level = levels[min(len(levels) - 1, verbose)]
    logger.basicConfig(
        level=level, format='%(asctime)s %(levelname)s %(message)s')

    if directory is None:
        directory = os.getcwd()
        logger.debug(directory)

    files = get_files(directory)
    for file in files:
        tracks = get_tracks(file, language)
        mux(file, tracks, overwrite=overwrite, dry_run=dry_run)


def get_files(path):
    files = []
    for file in (os.listdir(path)):
        if file.endswith('.mkv'):
            files.append(file)
            logger.debug("Read file: %s", file)
    return files


def get_tracks(file, sub_language='en'):
    to_mux = []
    info = MediaInfo.parse(file)
    for track in info.tracks:
        if (track.track_type == 'Audio') and (track.language == 'ja'):
            to_mux.append('a:' + str(track.stream_identifier))
        if (track.track_type == 'Text') and (track.language == sub_language):
            to_mux.append('s:' + str(track.stream_identifier))
    return to_mux


def mux(in_file, tracks_to_mux, out_dir=None, overwrite=False, ffmpeg=None, dry_run=False):
    if ffmpeg is None:
        ffmpeg = 'ffmpeg'
        # TODO: check if ffmpeg exists in PATH

    if out_dir is None:
        new_dir = os.path.join(os.getcwd(), 'remuxed')
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        out_dir = new_dir

    params = [ffmpeg]

    if overwrite:
        params.append('-y')
    else:
        params.append('-n')

    params += ['-i', in_file, '-map', '0:v:0', ]

    for track in tracks_to_mux:
        params.append('-map')
        params.append('0:' + track)

    params += ['-map', '0:t?', '-c', 'copy']
    params.append(os.path.join(out_dir, in_file))

    try:
        logger.debug("running ffmpeg with parameters: %s", params)
        if not dry_run:
            subprocess.run(params)

    except FileNotFoundError as e:
        logger.exception("ffmpeg not found")
        exit(1)
