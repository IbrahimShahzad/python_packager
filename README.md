# python_packager
pip package handler for downloading/zipping packages to export and install them on a separate machine

:bulb: **IMP!** USE PYTHON VERSION 3.8
## How to run:

command:

$ python packager.py [option]

            options:
                -p list, download and zip packages, and creates "package_list.txt"
                -z zip only -- "./downloads" directory must exist
                -d list and download packages only
                -r list packages only in requirements.txt
                -u unzip "python_packages.zip"
                -i unzip and install from "python_tar_packages.zip" and "python_whl_packages.zip"
                [IMPORTANT: MAKE SURE YOUR ARE USING PYTHON3.8]

### Packaging current libs
python3.8 packager.py -p
-    lists pip packages in requirements.txt
-    creates a download directory and downloads all the packages listed in requiremetns.txt
-    Finally zips the tar and whl packages separately and creates package_whl_list.txt and package_gz_list.txt for installation use

### Installing from package
required files in folder 
- package_whl_list.txt
- package_gz_list.txt
- python_tar_packages.zip
- python_tar_packages.zip
- packager.py script

 run "python3.8 packager.py -i" to install the packages on the machine.
 -    creates a directory 'extracted_files'
 -    unzips and installs from "python_tar_packages.zip" using package_gz_list.txt
 -    unzips and installs from "python_whl_packages.zip" using package_whl_list.txt
