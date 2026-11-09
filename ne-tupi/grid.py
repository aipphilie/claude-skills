import sys, os, glob, subprocess; sys.path.insert(0,'.')
import anim
from PIL import Image, ImageDraw, ImageFont
out=sys.argv[1]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; font=ImageFont.truetype(F,18)
names=list(anim.ANIMS); cols=5; rows=3
cw,ch=216,384; lh=34
frames={n:[Image.open(f).convert('RGB').resize((cw,ch),Image.LANCZOS) for f in sorted(glob.glob(f"{out}/kadry/{n}/*.png"))] for n in names}
os.makedirs('gridtmp',exist_ok=True)
for i in range(144):
    g=Image.new('RGB',(cw*cols,(ch+lh)*rows),'white'); d=ImageDraw.Draw(g)
    for k,n in enumerate(names):
        c,r=k%cols,k//cols
        fr=frames[n]; g.paste(fr[i%len(fr)],(c*cw,r*(ch+lh)))
        d.text((c*cw+cw//2,r*(ch+lh)+ch+lh//2-4),anim.ANIMS[n][0],fill='#111',font=font,anchor='mm')
    g.save(f'gridtmp/{i:03d}.png')
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","24","-i","gridtmp/%03d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","20",f"{out}/vse-animacii.mp4"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","24","-i","gridtmp/%03d.png","-vf","scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse","-loop","0",f"{out}/vse-animacii.gif"],check=True)
