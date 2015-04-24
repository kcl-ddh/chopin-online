#!/usr/bin/python
"""Module for batch converting images to JPEG 2000 format.

Takes an input directory and recreates the directory structure, with
converted images, in the specified output directory.

WARNING: If the same directory contains two or more images with the
same name (excepting the extension), only one of these images will
end up converted.

WARNING: kdu_compress does not handle filenames containing a comma,
even if the entire string is quoted or the comma quoted with a \.

Refactored by EH for use as a specialsed upload converter/archiver only for tiffs in OCVE upload dir

"""

import copy_reg
import logging
import multiprocessing
import os
import shlex
import subprocess
import types
import re
from shutil import move

import progressbar as pb

import fcntl
import sys

logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger('Main logger')
logger.setLevel(logging.INFO)

# Guard against multiple instances with a fcntl lock

def lockFile(lockfile):
    fd = os.open(lockfile, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False
    return True

if not lockFile("/vol/ocve3/webroot/stg/logs/.imageconvert.lock"):
    logger.error('Another instance detected as lock exists, exiting.')
    sys.exit(0)

# End lock guard

class ArchiveJP2Converter (object):
    def __init__ (self, in_dir, out_dir, archive_dir,fail_dir, force=False, show_progress=False):
        """Initialise this object.
        :param in_dir: path to directory containing images to be converted
        :type in_dir: `str`
        :param out_dir: path to directory to output converted images
        :type out_dir: `str`
        :param out_dir: archive directory for successfully converted images
        :type out_dir: `str`
        :param force: whether to overwrite existing converted images
        :type force: `bool`
        :param show_progress: whether to show a progress bar during conversion
        :type show_progress: `bool`

        """

        self._in_dir = os.path.abspath(in_dir)
        self._out_dir = os.path.abspath(out_dir)
        if len(archive_dir) > 0:
            self._archive_dir = os.path.abspath(archive_dir)
        else:
            self._archive_dir = None
        if len(fail_dir) > 0:
            self._failed_dir = os.path.abspath(fail_dir)
        else:
            self._fail_dir = None
        self._force = force
        self._progress = show_progress
        self._bar = None
        self._has_errors = False

    def convert (self, lossless=False):
        """Converts images.
        Returns True if there were no errors.
        :param compress: whether to use a lossless conversion
        :type compress: `bool`
        :rtype: `bool`
        """

        self._has_errors = False
        if self._progress:
            max_val = 0
            for root, dirs, files in os.walk(self._in_dir):
                max_val += len(files)
            self._bar = pb.ProgressBar(widgets=[pb.Percentage(), pb.Bar()],
                                       maxval=max_val).start()
        pool = multiprocessing.Pool()

        for root, dirs, files in os.walk(self._in_dir):
            out_rel_path = os.path.relpath(root, self._in_dir)
            out_full_path = os.path.abspath( os.path.join(self._out_dir, out_rel_path) )
            if not os.path.isdir(out_full_path):
                logger.info('Creating directory [%s]' % (out_full_path) )
                try:
                     os.makedirs(out_full_path)
                except OSError as e:
                    logger.fatal('Unable to create directory [%s], Reason: %s' % (out_full_path,e.strerror) )
                    sys.exit(1)
            for name in files:
                # Changed to only look at Tifs, the OCVE image format
                if re.match('.*\.tif',name,re.IGNORECASE):
                    basename = os.path.splitext(name)[0]
                    in_file = os.path.join(root, name)
                    base_out_file = os.path.join(out_full_path, basename)
                    tiff_file = '%s.tif' % base_out_file
                    jp2_file = '%s.jp2' % base_out_file
                    if self._force or not(os.path.isfile(jp2_file)):
                        params = (in_file, tiff_file, jp2_file, lossless)
                        pool.apply_async(self._convert, params,
                                         callback=self._result_callback)

                    elif self._progress:
                        self._bar.update(self._bar.currval + 1)
        pool.close()
        pool.join()
        if self._progress:
            self._bar.finish()
        #Added by EH for archiving originals outside input dir (for OCVE)
        if self._archive_dir is not None:
            for root, dirs, files in os.walk(self._in_dir):
                out_rel_path = os.path.relpath(root, self._in_dir)
                out_full_path = os.path.abspath(
                    os.path.join(self._out_dir, out_rel_path))
                for name in files:
                     if re.match('.*\.[tif|TIF]',name,re.IGNORECASE):
                        basename = os.path.splitext(name)[0]
                        in_file = os.path.join(root, name)
                        jp2_file=basename+'.jp2'
                        jp2= os.path.join(out_full_path, jp2_file)
                        archive_full_path = ''
                        if os.path.isfile(jp2) and  os.path.getsize(jp2) > 0:
                            #JP2 is successfully converted, archive original
                            archive_full_path = os.path.abspath(os.path.join(self._archive_dir, out_rel_path))
                        else:
                            #Move to failed dir
                            archive_full_path = os.path.abspath(os.path.join(self._failed_dir, out_rel_path))
                        if len(archive_full_path) > 0:
                            if not os.path.isdir(archive_full_path):
                               logger.info('Creating directory [%s]' % archive_full_path)
                               try:
                                   os.makedirs(archive_full_path)
                               except OSError as e:
                                   logger.fatal('Unable to create directory [%s], Reason: %s' % (archive_full_path, e.strerror))
                                   sys.exit(1)
                            src = in_file
                            dst=os.path.join(archive_full_path,name)
                            move(src,dst)
                            logger.info('Image archived at [%s]' % dst)
                #If folder is now empty, remove it.
                if len(os.listdir(root)) == 0:
                    if os.path.isdir(root):
                        os.rmdir(root)
        else:
            logger.info('Archive folder not found')
        return not(self._has_errors)

    def _convert (self, in_file, tiff_file, jp2_file, lossless):
        logger.info('convert [%s]->[%s]' % (in_file, tiff_file) )
        cmd = [ 'convert', 
                '-compress', 
                'None', 
                '-alpha', 
                'off', 
                in_file, 
                tiff_file
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = proc.communicate()[1]
        if err:
            logger.error('Error converting to TIFF [%s]->[%s], Reason: %s' % (in_file,tiff_file,err))
            # In some cases, at least, an error may be reported
            # (typically "unknown field") but the TIFF is in fact
            # converted in a visually satisfactory way. In such cases,
            # where the converted TIFF file is created, continue on
            # with the JPEG 2000 conversion.
            if not os.path.exists(tiff_file):
                return False
        logger.info('convert [%s]->[%s] completed' % (in_file,tiff_file))
        if lossless:
            logger.info('(lossless) kdu_compress [%s]->[%s]' % ( tiff_file, jp2_file ) )
            cmd = [
                    'kdu_compress', 
                    '-i', 
                    tiff_file, 
                    '-o',
                    jp2_file, 
                    '-rate', 
                    '-', 
                    'Creversible=yes', 
                    'Clevels=5', 
                    'Stiles={1024,1024}', 
                    'Cblk={64,64}', 
                    'Corder=RPCL'
            ]
        else:
            logger.info('(lossy) kdu_compress [%s]->[%s]' % ( tiff_file, jp2_file ) )
            cmd = [
                    'kdu_compress', 
                    '-i', 
                    tiff_file, 
                    '-o', 
                    jp2_file, 
                    '-rate', 
                    '-,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185', 
                    'Stiles={1024,1024}', 
                    'Cblk={64,64}', 
                    'Creversible=no', 
                    'Clevels=5', 
                    'Corder=RPCL', 
                    'Cmodes=BYPASS'
            ]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = proc.communicate()[1]
        if err:
            logger.error('Error converting to JPEG2000 [%s]->[%s], Reason: %s' % (tiff_file,jp2_file,err))
            return False
        else:
            logger.info('kdu_compress completed [%s]->%s[]' % (tiff_file,jp2_file))
            logger.info('Deleting TIFF file [%s]' % tiff_file)
            try:
                os.remove(tiff_file)
            except (IOError, OSError), e:
                logger.warn('Error removing TIFF [%s], Reason: %s' % (tiff_file, e))
        logger.info('Conversion complete: [%s]' % in_file)
        return True

    def _result_callback (self, result):
        if not result:
            self._has_errors = True
        if self._progress:
            self._bar.update(self._bar.currval + 1)


# Support pickling methods, as required by the multiprocessing
# code. Code taken from
# http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods#edit2155350
def _pickle_method (method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method (func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

if __name__ == "__main__":

    logger.info('Starting image conversion run')
# FIXME change the paths here
    ArchiveJP2Converter('/vol/ocve2/images/upload','/vol/ocve2/images/temp/','/vol/ocve2/images/convert/','/vol/ocve2/images/convertfail/',True,False).convert(True)
    logger.info('Completed image conversion run')
