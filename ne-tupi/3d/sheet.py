import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
P = {
 "Спокойно": {},
 "Объясняет": {"la":[75,35],"ra":[75,35],"mouth":"A","head":-4,"laF":0.3,"raF":0.3},
 "Указывает вверх": {"ra":[155,10],"mouth":"O","head":-5},
 "Пожимает плечами": {"la":[45,95],"ra":[45,95],"mouth":"sad","head":10,"laF":0.4,"raF":0.4},
 "Машет": {"ra":[110,50],"mouth":"smile","head":-6},
}
poses = {}
for i,(n,p) in enumerate(P.items()):
    poses[f"p{i}"] = dict(p, yaw=-18)
for k in range(36):
    poses[f"t{k:02d}"] = {"yaw": k*10, "mouth": "smile"}
poses["hero"] = {"yaw": -18}
subprocess.run(["node","3d/shot.js",json.dumps(poses),"540","960"],check=True)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; font=ImageFont.truetype(F,30)
w,h=440,782
sh=Image.new('RGB',(w*len(P),h+70),'white'); d=ImageDraw.Draw(sh)
for i,n in enumerate(P):
    im=Image.open(f"3d/out/p{i}.png").convert('RGB').resize((w,h),Image.LANCZOS)
    sh.paste(im,(i*w,0)); d.text((i*w+w//2,h+30),n,fill='#111',font=font,anchor='mm')
sh.save("3d/pozy-3d.png")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","12","-i","3d/out/t%02d.png","-vf","scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse","-loop","0","3d/povorot-3d.gif"],check=True)
