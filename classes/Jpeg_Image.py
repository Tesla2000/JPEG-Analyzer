from chunk_info.chunk_dict import chunks


class JpegImage:

    def __init__(self, filename):
        file = open(filename, "rb")
        self.binary_img = list(file.read())
        self.chunks = []

    def read_chunks(self):
        index = -1
        for i in range(len(self.binary_img)):
            if self.binary_img[i] == 0xff:
                if self.binary_img[i+1] in chunks:
                    self.chunks.append([])
                    index += 1
                else:
                    self.chunks[index].append(self.binary_img[i])
            else:
                self.chunks[index].append(self.binary_img[i])
