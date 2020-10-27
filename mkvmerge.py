import os
import subprocess

RAW_PATH = '/mnt/e/Torrent Downloads/Raw/[VCB-Studio] Imouto sae Ireba Ii. [Ma10p_1080p]'
SUBS_PATH = '/mnt/e/Torrent Downloads/Raw/[9volt] Imouto sae Ireba Ii. (01-12) [720p] (Batch)_attachments'
DEST_PATH = '/mnt/c/Users/noel/Desktop/Imouto sae Ireba Ii'

MKVMERGE_PATH = 'mkvmerge'


def mux(video_source, sub_source, output):
    fonts = None
    subs = None
    chapters = None

    if os.path.isdir(sub_source):
        font_source = os.path.join(sub_source, 'attachments')
        fonts = [os.path.join(font_source, font) for font in os.listdir(font_source) if font.endswith(('ttf', 'ttc', 'otf', 'otc'))]
        print(len(fonts), 'fonts to mux')
        subs = [os.path.join(sub_source, sub) for sub in os.listdir(sub_source) if sub.endswith(('utf', 'utf8', 'utf-8', 'idx', 'sub', 'srt', 'rt', 'ssa', 'ass', 'mks', 'vtt'))]
        print(len(subs), "subtitle tracks to mux")
        chapters = os.path.join(sub_source, 'chapters.xml')
        if not os.path.exists(chapters):
            chapters = None

    args = [MKVMERGE_PATH]

    if chapters is not None:
        args.append('--chapters')
        args.append(chapters)

    for font in fonts:
        args.append('--attach-file')
        args.append(font)

    args.append('-o')
    args.append(output)

    if chapters is not None:
        args.append('--no-chapters')
    args.append('--no-subtitles')
    args.append(video_source)

    for sub in subs:
        args.append('--language')
        args.append('0:eng')
        args.append(sub)

    # print(*args)
    subprocess.run(args)


raws = [os.path.join(RAW_PATH, raw) for raw in os.listdir(RAW_PATH) if raw.endswith('.mkv')]
print('Raws:', raws)

sub_folders = [os.path.join(SUBS_PATH, folder) for folder in os.listdir(SUBS_PATH)]

if len(raws) != len(sub_folders):
    print('Different number of raw and subs')
    print(len(raws), 'raw files')
    print(raws)
    print(len(sub_folders), 'sub files')
    print(sub_folders)
    # exit(1)

for (raw, sub) in zip(raws, sub_folders):
    output = DEST_PATH
    output = os.path.join(output, sub.split('/')[-1].strip('_Attachments'))
    if not output.endswith('.mkv'):
        output += '.mkv'
    mux(raw, sub, output)
