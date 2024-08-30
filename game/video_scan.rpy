# Esse script escaneia a pasta images procurando por vídeos .webm e já cria a declaração deles. 

default persistent.video_resolution = 0
init -1800 python:
    
    video_resolutions = [720, 1080, 1440, 2160]
    active_video_resolution = ''
    loaded_video_sizes = {}

    no_loop_anims = [
        "ep6 anim_15fps",
        "ep3 anim_sat_chloesex_037",
        "ep4 anim_emilyvisit_192",
        "ep4 anim_emilyvisit_192_var1",
        "ep4 anim_emilyvisit_144_1",
        "ep4 anim_suesex_137",
        "ep4 anim_suesex_137_var1",
        "ep5 anim_gabbysex_049",
        "ep5 anim_gabbysex_046",
        "ep5 anim_gabbysex_052",
        "ep5 anim_lilysex_038",
        "ep5 anim_lilysex_074"
        "ep7 anim_hellsangels_001",
        "ep6 anim_nursesex_052",
        "ep6 anim_nursesex_038",
        "ep6 anim_nursesex_033",
        "ep6 anim_nursesex_055_var1",
        "ep6 anim_chloesex_024",
        "ep7 anim_gabbysex_038",
        "ep7 anim_gettingcaught_999",
    ]


    def _scan_images_directory_for_videos():
        global active_video_resolution

        if not persistent.video_resolution or persistent.video_resolution not in video_resolutions:
            if len(video_resolutions) > 1:
                active_video_resolution = default_resolution_per_system()
                if active_video_resolution not in video_resolutions:
                    active_video_resolution = video_resolutions[0]
            else:
                persistent.video_resolution = video_resolutions[0]
                active_video_resolution = video_resolutions[0]

        elif persistent.video_resolution:
            active_video_resolution = persistent.video_resolution

        if active_video_resolution == 2160:
            _scan_images_directory_for_videos_2('images_2160', 'uhd:', 1800)
            _scan_images_directory_for_videos_2('images', '', 1080)
        elif active_video_resolution == 1440:
            _scan_images_directory_for_videos_2('images_1440', 'qhd:', 1440)
            _scan_images_directory_for_videos_2('images', '', 1080)
        elif active_video_resolution == 1080:
            _scan_images_directory_for_videos_2('images', '', 1080)
        elif active_video_resolution == 720:
            _scan_images_directory_for_videos_2('images_720', 'hd:', 720)
            _scan_images_directory_for_videos_2('images', '', 1080)
            
        

    def _scan_images_directory_for_videos_2(directory, load_prefix, resolution):
        import os
        prefix = directory.rstrip('/') + '/'

        video_size = (1920,1080)
        # if renpy.emscripten:
        #     video_size = None

        for fn in renpy.list_files():
            if not fn.startswith(prefix):
                continue

            basename = os.path.basename(fn)
            base, ext = os.path.splitext(basename)

            if not ext.lower() in [".webm", ".mp4" ]:
                continue

            base = base.lower()
            base = base.partition("@")[0]
            if renpy.has_image(base, exact=True):
                continue

            if base in no_loop_anims or '_pan' in base or 'pan_' in base:
                end_frame = base + '_end'
                start_frame = base + '_beg'
                # print('loaded no_loop_anim: ' + start_frame)
                renpy.image(base, Movie(play=fn, image=end_frame, start_image=start_frame, loop=False, size=video_size))
            elif 'titlecard' in base:
                renpy.image(base, Movie(play=fn, image='black', start_image='black', loop=False, size=video_size))
            else:
                start_frame = base + '_beg'
                #print('Loaded video: {}'.format(fn))
                renpy.image(base, Movie(play=fn, image=start_frame, start_image=start_frame, size=video_size))

            loaded_video_sizes[base] = resolution


    
    def default_resolution_per_system():
        if not renpy.variant('small'):
            return 1080
        elif renpy.variant('small'):
            return 720
        
        return 720
    
init python:
    _scan_images_directory_for_videos()

    