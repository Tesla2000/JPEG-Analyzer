# markers taken from: https://github.com/corkami/formats/blob/master/image/jpeg.md
marker_dict = {
    0x01: "TEM",
    0x51: "SIZ",
    0x53: "COD",
    0x55: "TLM",
    0x57: "PLM",
    0x58: "PLT",
    0x5c: "QCD",
    0x5d: "QCC",
    0x5e: "RGN",
    0x5f: "POC",
    0x60: "PPM",
    0x61: "PPT",
    0x63: "CRG",
    0x64: "COM",
    0x65: "SEC",
    0x66: "EPB",
    0x67: "ESD",
    0x68: "EPC",
    0x69: "RED",
    0x90: "SOT",
    0x91: "SOP",
    0x92: "EPH",
    0x93: "SOD",
    0x94: "INSEC",
    0xc0: "SOF0",
    0xc1: "SOF1",
    0xc2: "SOF2",
    0xc3: "SOF3",
    0xc4: "DHT",
    0xc5: "SOF5",
    0xc6: "SOF6",
    0xc7: "SOF7",
    0xc8: "JPG",
    0xc9: "SOF9",
    0xca: "SOF10",
    0xcb: "SOF11",
    0xcc: "DAC",
    0xcd: "SOF13",
    0xce: "SOF14",
    0xcf: "SOF15",
    0xd0: "RST0",
    0xd1: "RST1",
    0xd2: "RST2",
    0xd3: "RST3",
    0xd4: "RST4",
    0xd5: "RST5",
    0xd6: "RST6",
    0xd7: "RST7",
    0xd8: "SOI",
    0xd9: "EOI",
    0xda: "SOS",
    0xdb: "DQT",
    0xdc: "DNL",
    0xdd: "DRI",
    0xde: "DHP",
    0xdf: "EXP",
    0xe0: "APP0",
    0xe1: "APP1",
    0xe2: "APP2",
    0xe3: "APP3",
    0xe4: "APP4",
    0xe5: "APP5",
    0xe6: "APP6",
    0xe7: "APP7",
    0xe8: "APP8",
    0xe9: "APP9",
    0xea: "APP10",
    0xeb: "APP11",
    0xec: "APP12",
    0xed: "APP13",
    0xee: "APP14",
    0xef: "APP15",
    0xf0: "JPG0",
    0xf1: "JPG1",
    0xf2: "JPG2",
    0xf3: "JPG3",
    0xf4: "JPG4",
    0xf5: "JPG5",
    0xf6: "JPG6",
    0xf7: "SOF48",
    0xf8: "LSE",
    0xf9: "JPG9",
    0xfa: "JPG10",
    0xfb: "JPG11",
    0xfc: "JPG12",
    0xfd: "JPG13",
    0xfe: "COM"
}

necessary_chunks = {0xc0: "SOF0",
                    0xc1: "SOF1",
                    0xc2: "SOF2",
                    0xc3: "SOF3",
                    0xc4: "DHT",
                    0xc5: "SOF5",
                    0xc6: "SOF6",
                    0xc7: "SOF7",
                    0xc9: "SOF9",
                    0xca: "SOF10",
                    0xcb: "SOF11",
                    0xcd: "SOF13",
                    0xce: "SOF14",
                    0xcf: "SOF15",
                    0xd0: "RST0",
                    0xd1: "RST1",
                    0xd2: "RST2",
                    0xd3: "RST3",
                    0xd4: "RST4",
                    0xd5: "RST5",
                    0xd6: "RST6",
                    0xd7: "RST7",
                    0xd8: "SOI",
                    0xd9: "EOI",
                    0xda: "SOS",
                    0xdb: "DQT",
                    0xdd: "DRI"
                    }

# Tags used by the exif format
TAGS = {  # Tags used by IFD0:
    0x010e: 'ImageDescription',
    0x010f: 'Make',
    0x0110: 'Model',
    0x0112: 'Orientation',
    0x011a: 'XResolution',
    0x011b: 'YResolution',
    0x0128: 'ResolutionUnit',
    0x0131: 'Software',
    0x0132: 'DateTime',
    0x013e: 'WhitePoint',
    0x013f: 'PrimaryChromaticities',
    0x0211: 'YCbCrCoefficients',
    0x0213: 'YCbCrPositioning',
    0x0214: 'ReferenceBlackWhite',
    0x8298: 'Copyright',
    0x8769: 'ExifOffset',

    # Tags used by Exif SubIFD:
    0x829a: 'ExposureTime',
    0x829d: 'FNumber',
    0x8822: 'ExposureProgram',
    0x8827: 'ISOSpeedRatings',
    0x9000: 'ExifVersion',
    0x9003: 'DateTimeOriginal',
    0x9004: 'DateTimeDigitized',
    0x9101: 'ComponentConfiguration',
    0x9102: 'CompressedBitsPerPixel',
    0x9201: 'ShutterSpeedValue',
    0x9202: 'ApertureValue',
    0x9203: 'BrightnessValue',
    0x9204: 'ExposureBiasValue',
    0x9205: 'MaxApertureValue',
    0x9206: 'SubjectDistance',
    0x9207: 'MeteringMode',
    0x9208: 'LightSource',
    0x9209: 'Flash',
    0x920a: 'FocalLength',
    0x927c: 'MakerNote',
    0x9286: 'UserComment',
    0xa000: 'FlashPixVersion',
    0xa001: 'ColorSpace',
    0xa002: 'ExifImageWidth',
    0xa003: 'ExifImageHeight',
    0xa004: 'RelatedSoundFile',
    0xa005: 'ExifInteroperabilityOffset',
    0xa20e: 'FocalPlaneXResolution',
    0xa20f: 'FocalPlaneYResolution',
    0xa210: 'FocalPlaneResolutionUnit',
    0xa217: 'SensingMethod',
    0xa300: 'FileSource',
    0xa301: 'SceneType',

    # Tags used by IFD1 (thumbnail image):
    0x0100: 'ImageWidth',
    0x0101: 'ImageLength',
    0x0102: 'BitsPerSample',
    0x0103: 'Compression',
    0x0106: 'PhotometricInterpretation',
    0x0111: 'StripOffsets',
    0x0115: 'SamplesPerPixel',
    0x0116: 'RowsPerStrip',
    0x0117: 'StripByteConunts',
    0x011a: 'XResolution',
    0x011b: 'YResolution',
    0x011c: 'PlanarConfiguration',
    0x0128: 'ResolutionUnit',
    0x0201: 'JpegIFOffset',
    0x0202: 'JpegIFByteCount',
    0x0211: 'YCbCrCoefficients',
    0x0212: 'YCbCrSubSampling',
    0x0213: 'YCbCrPositioning',
    0x0214: 'ReferenceBlackWhite',

    # Misc tags:
    0x00fe: 'NewSubfileType',
    0x00ff: 'SubfileType',
    0x012d: 'TransferFunction',
    0x013b: 'Artist',
    0x013d: 'Predictor',
    0x0142: 'TileWidth',
    0x0143: 'TileLength',
    0x0144: 'TileOffsets',
    0x0145: 'TileByteCounts',
    0x014a: 'SubIFDs',
    0x015b: 'JPEGTables',
    0x828d: 'CFARepeatPatternDim',
    0x828e: 'CFAPattern',
    0x828f: 'BatteryLevel',
    0x83bb: 'IPTC/NAA',
    0x8773: 'InterColorProfile',
    0x8824: 'SpectralSensitivity',
    0x8825: 'GPSInfo',
    0x8828: 'OECF',
    0x8829: 'Interlace',
    0x882a: 'TimeZoneOffset',
    0x882b: 'SelfTimerMode',
    0x920b: 'FlashEnergy',
    0x920c: 'SpatialFrequencyResponse',
    0x920d: 'Noise',
    0x9211: 'ImageNumber',
    0x9212: 'SecurityClassification',
    0x9213: 'ImageHistory',
    0x9214: 'SubjectLocation',
    0x9215: 'ExposureIndex',
    0x9216: 'TIFF/EPStandardID',
    0x9290: 'SubSecTime',
    0x9291: 'SubSecTimeOriginal',
    0x9292: 'SubSecTimeDigitized',
    0xa20b: 'FlashEnergy',
    0xa20c: 'SpatialFrequencyResponse',
    0xa214: 'SubjectLocation',
    0xa215: 'ExposureIndex',
    0xa302: 'CFAPattern'}

# Metadata format used in APP1 segment
# key is a format symbol
# first element in list in values determines number of bytes
# needed to write the given format
# rational means that there are two values: numerator and denominator
DATA_FORMAT = {1: [1, 'int'],
               2: [1, 'str'],
               3: [2, 'int'],
               4: [4, 'int'],
               5: [8, 'rational'],
               6: [1, 'int'],
               7: [1, 'int'],
               8: [2, 'int'],
               9: [4, 'int'],
               10: [8, 'rational'],
               11: [4, 'float'],
               12: [8, 'float']}
