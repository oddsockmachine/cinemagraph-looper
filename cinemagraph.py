from PIL import Image
import glob, os
from pprint import pprint
from itertools import islice


sourcedir = r"C:\B_Py\Cinemagraph\source"
outdir = sourcedir + r"\output"
if not os.path.exists(outdir):
    os.mkdir( outdir )

name_image_dict = {}

is_gif = False
# if gif, extract images
gif_path = glob.glob(sourcedir+r"\*.gif")
if len(gif_path)>0:
    print "Found a gif - extracting frames, then continuing as normal..."
    is_gif = True
    #load and chop the gif
    infile = gif_path[0] #only take the first gif, if there are many
    print infile
    try:
        im = Image.open(infile)
    except IOError:
            print ( "Cannot load gif '"+str( infile ) )+"'"
    i = 0   #counter for gif frames
    my_palette = im.getpalette()
    new_path = "\\".join(infile.split("\\")[:-1])+"\\"
    name = ((new_path + infile.split("\\")[-1]).split(".")[0])+".png"
    print name
    try:
        while 1:
            im.putpalette(my_palette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            new_im.save(infile.split(".")[0] +str(i)+ '.png')   #save the new img in g/...

            i += 1
            im.seek( im.tell()+1 )

    except( EOFError ):
        pass

# load in sequence of images
if is_gif:
    filelist = glob.iglob(sourcedir+r"\*.png")
else:
    filelist = glob.iglob(sourcedir+r"\*.jpg")

#put all images in a sorted list
for infile in filelist:
    try:
        im = Image.open(infile)
        name = str(infile).split("\\")[-1]
        #name = str(infile)
        name_image_dict[name] = im
    except IOError:
        print ( "Cannot load image '"+str( infile ) )+"'"


# get info on overlap period
# eg: 10 frames / 5%
overlap_amt = 5

# take first and last x frames
# [0][1][x], [-x][-2][-1]
ordered_img_names = sorted(name_image_dict)
#pprint(ordered_img_names)
first = ordered_img_names[:overlap_amt]
last  = ordered_img_names[-overlap_amt:]

# zip them into a sorted list of tuples
# [0][-x], [1][-2], [x][-1]
overlapping_imgs = zip(first, last)
pprint (overlapping_imgs)

output = []

alpha = 1
step = 1.0/overlap_amt


for img in ordered_img_names[overlap_amt:-overlap_amt]:
    output.append(name_image_dict[img])

# while overlap > 0 or
# for pair in list:
for pair in overlapping_imgs:
    a = name_image_dict[pair[0]]
    b = name_image_dict[pair[1]]
    output.append( Image.blend(a, b, alpha) )
    alpha -= step

pprint (output)

def save(img, outdir, count):
    try:
        img.save( outdir +"\\"+ str(count) +".jpg" )
        count += 1
    except:
        print "Oops, couldn't save"
    return count

count = 0
for out in output:
    count = save (out, outdir, count)
    print count
# append output to frames remaining in middle of gif

# convert list of frames to gif, save next to input