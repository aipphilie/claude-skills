# python3 tools/sheet.py prev/ — склеить кадры t*.png в лист 6×N
import sys,glob
from PIL import Image
d=sys.argv[1];fs=sorted(glob.glob(d+'/t*.png'),key=lambda s:float(s.split('/t')[-1][:-4]));ims=[Image.open(f).convert('RGB') for f in fs];w,h=ims[0].size
c=6;r=(len(ims)+c-1)//c;sheet=Image.new('RGB',(w*c,h*r),'white')
for i,im in enumerate(ims):sheet.paste(im,((i%c)*w,(i//c)*h))
sheet.save(d+'/sheet.jpg',quality=85);print(sheet.size)
