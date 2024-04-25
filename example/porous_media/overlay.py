import subprocess


input_movie ='/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/script_output/ink_output.mp4'
input_img = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/script_output/tw_tk_1024x1024.png'
destination_directory = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/script_output/' 


ffmpeg_command = [
    'ffmpeg',
    '-i', f'{input_movie}.mp4',
    '-i', f'{input_img}.png',
    '-filter_complex', "[1:v]scale=512:512,format=argb,geq=r='r(X,Y)':a='0.5*alpha(X,Y)'[zork]; [0:v][zork]overlay",
    '-vcodec', 'libx264',
    f'{destination_directory}tk_overlay.mp4'
]

subprocess.run(ffmpeg_command, text=True, input='y\n')
# result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)