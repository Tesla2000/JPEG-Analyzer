from classes.Jpeg_Image import JpegImage
from chunk_info.chunk_dict import chunks


jpeg = JpegImage("lizard.jpg")
jpeg.read_chunks()
for chunk in jpeg.chunks:
    print(chunks[chunk[0]])
    