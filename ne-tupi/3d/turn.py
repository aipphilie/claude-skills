import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; font=ImageFont.truetype(F,30)
views=[("Анфас",0),("3/4",-40),("Профиль",-90),("Сзади 3/4",-140),("Спина",180)]
for style in ["flat","toon"]:
    poses={}
    for i,(n,y) in enumerate(views): poses[f"{style}_v{i}"]={"yaw":y,"style":style}
    for k in range(36): poses[f"{style}_t{k:02d}"]={"yaw":k*10,"style":style,"mouth":"rest"}
    poses[f"{style}_wave"]={"yaw":-35,"style":style,"ra":[110,50],"mouth":"smile","raF":0.3}
    subprocess.run(["node","3d/shot.js",json.dumps(poses),"540","960"],check=True)
    w,h=400,711
    sh=Image.new('RGB',(w*len(views),h+70),'white'); d=ImageDraw.Draw(sh)
    for i,(n,y) in enumerate(views):
        sh.paste(Image.open(f"3d/out/{style}_v{i}.png").convert('RGB').crop((40,80,500,898)).resize((w,h),Image.LANCZOS),(i*w,0))
        d.text((i*w+w//2,h+30),n,fill='#111',font=font,anchor='mm')
    sh.save(f"3d/povoroty-{style}.png")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","12","-i",f"3d/out/{style}_t%02d.png","-vf","crop=460:818:40:80,scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=32[p];[b][p]paletteuse","-loop","0",f"3d/povorot-{style}.gif"],check=True)
