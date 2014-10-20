from api import vkapi
from pathlib import Path
import re

sizeRegex = re.compile(r"photo_(?P<num>\d+)")

dateFormat = "%d/%m/%Y %H:%M:%S"

def maxPhoto(item): 
    sizeMax = max(int(size.group("num")) for size in map(sizeRegex.match,item.keys()) if size)
    return item["photo_%d" % sizeMax]

def writePhotos(
        owner: int                 = "2320550",
        album: [int,str,list,tuple]= "wall",
        file : Path                = Path("my_images.csv")
    ) -> None :
    """
    Dumps photos to csv file
    owner : owner id, negative for group
    album : album_id, specials are "wall", "saved" and "profile"
    file  : pathlib's Path file object
    """
    if isinstance(album,str): albums = [album]
    else: albums = album
    photos = [p for alb in albums for p in vkapi.photos.get(owner_id=owner, album_id = alb, extended = 1)]
    with file.open("wt") as fp:
        writer = csv.DictWriter(fp,("timestamp", "likes","photo"),dialect="unix")
        writer.writeheader()
        writer.writerows({
            "timestamp" : dt.fromtimestamp(item["date"]).strftime(dateFormat),
            "likes"     : item["likes"]["count"],
            "photo"     : maxPhoto(item)
            } for item in photos["items"])
