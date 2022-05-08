from classes.Jpeg_Image import JpegImage


jpeg = JpegImage("test.jpg")
jpeg.read_markers()
jpeg.display_image()
jpeg.DFT()
jpeg.parse_app0()
jpeg.parse_exif()
jpeg.save_anon()
for marker in jpeg.markers:
    print(marker)

    