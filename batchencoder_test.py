import unittest
import os
import batchencoder

#Don't encode any videos for testing
batchencoder.ReadOnly = True

class MediaFileTests(unittest.TestCase):
    basedir = os.path.expandUser('~/Media/Encoded')
    knownValues = (('/media/So.You.Think.You.Can.Dance.S07E22.HDTV.XviD-2HD.avi',
                                basedir + 'So You Think You Can Dance - 7x22.m4v'),
                   ('/media/Two and a Half Men/Two.and.a.Half.Men.S07E21.Gumby.with.a.Pokey.HDTV.XviD-FQM.mkv',
                                basedir + 'Two and a Half Men - 7x21 - Gumby With A Pokey.m4v'),
                   ('/media/Two and a Half Men/Two.and.a.Half.Men.S07E21.Gumby.with.a.Pokey.HDTV.XviD-FQM.avi',
                                basedir + 'Two and a Half Men - 7x21 - Gumby With A Pokey.m4v'),
                   ('/media/The Mentalist/The.Mentalist.S02E17.HDTV.XviD-NoTV.[VTV].avi',
                                basedir + 'The Mentalist - 2x17.m4v'),
                   ('NCIS/NCIS.S08E01.HDTV.XviD-LOL.[VTV].avi',
                                basedir + 'NCIS - 8x01.m4v'),
                   ('Psych.S05E01.Romeo.and.Juliet.and.Juliet.HDTV.XviD-FQM.avi',
                                basedir + 'Psych - 5x01 - Romeo and Juliet and Juliet.m4v'),
                   ('Psych.S05E05.HDTV.XviD-XII.avi',
                                basedir + 'Psych - 5x05 - XII.m4v'),
                   ('Arrested Development/1-01 Pilot.avi',
                                basedir + 'Arrested Development - 1x01 - Pilot.m4v'),
                   ('Arrested Development/1-01 Pilot [Extended].avi',
                                basedir + 'Arrested Development - 1x01 - Pilot [Extended].m4v'))

    def testConvertingKnownValues(self):
        """Test that the first value in knownValues is converted to the second value"""
        for path,correct in self.knownValues:
           mediafile = batchencoder.MediaFile(path)
           self.assertTrue(mediafile.isValidVideo())
           self.assertEqual(correct, mediafile.getOutputFile())

