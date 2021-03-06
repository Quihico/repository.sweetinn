""" downloaded from http://xbmc-addons.googlecode.com/svn/addons/ """
""" This is a modded version of the original addons.xml generator """

""" Put this version in the root folder of your repo and it will """
""" zip up all add-on folders, create a new zip in your zips folder """
""" and then update the md5 and addons.xml file """

""" Recoded by whufclee (info@totalrevolution.tv) """

import re
import os
import shutil
import md5
import zipfile

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__(self):
# Create the zips folder if it doesn't already exist
        zips_path = ('zips')
        if not os.path.exists(zips_path):
            os.makedirs(zips_path)
        self._generate_addons_file()
        self._generate_md5_file()
        print "Finished updating addons xml and md5 files"

    def Create_Zips(self,addon_id,version):
        xml_path     = os.path.join(addon_id,'addon.xml')
        addon_folder = os.path.join('zips',addon_id)
        if not os.path.exists(addon_folder):
            os.makedirs(addon_folder)
        final_zip = os.path.join('zips',addon_id,'%s-%s.zip' % (addon_id,version))
        if not os.path.exists(final_zip):
            print "NEW ADD-ON - Creating zip for: %s v.%s" % (addon_id,version)
            zip = zipfile.ZipFile(final_zip, 'w', compression=zipfile.ZIP_DEFLATED )
            root_len = len(os.path.dirname(os.path.abspath(addon_id)))
            for root, dirs, files in os.walk(addon_id):
                archive_root = os.path.abspath(root)[root_len:]
                for f in files:
                        fullpath = os.path.join( root, f )
                        archive_name = os.path.join( archive_root, f )
                        zip.write( fullpath, archive_name, zipfile.ZIP_DEFLATED )
            zip.close()
# Copy over the icon, fanart and addon.xml to the zip directory
            copyfiles = ['icon.png', 'fanart.jpg', 'addon.xml']
            files = os.listdir(addon_id)
            for file in files:
                if file in copyfiles:
                    shutil.copy(os.path.join(addon_id, file), addon_folder)
            shutil.copytree(os.path.join(addon_id, 'resources'), os.path.join(addon_folder, 'resources'), symlinks=False, ignore=None)

    def _generate_addons_file(self):
# Addon list
        addons = os.listdir('.')
# Final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
# Loop through and add each addons addon.xml file
        for addon in addons:
            try:
                if (not os.path.isdir(addon) or addon == "zips" or addon.startswith('.')): continue
                _path = os.path.join( addon, "addon.xml" )
                xml_lines = open( _path, "r" ).read().splitlines()
                addon_xml = ""
# Loop through cleaning each line
                ver_found = False
                for line in xml_lines:
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    if 'version="' in line and not ver_found:
                        version = re.compile('version="(.+?)"').findall(line)[0]
                        ver_found = True
                    addon_xml += unicode( line.rstrip() + "\n", "utf-8")
                addons_xml += addon_xml.rstrip() + "\n\n"
# Create the zip files
                self.Create_Zips(addon,version)
            except Exception, e:
                print "Excluding %s for %s" % ( _path, e, )
# Clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        self._save_file(addons_xml.encode( "utf-8" ), file='addons.xml')

    def _generate_md5_file(self):
        try:
            m = md5.new(open('addons.xml').read()).hexdigest()
            self._save_file(m, file='addons.xml.md5')
        except Exception, e:
            print "An error occurred creating addons.xml.md5 file!\n%s" % (e)

    def _save_file(self,data,file):
        try:
            open(file, 'w').write(data)
        except Exception, e:
            print "An error occurred saving %s file!\n%s" % (file,e)

if ( __name__ == "__main__" ):
    Generator()
