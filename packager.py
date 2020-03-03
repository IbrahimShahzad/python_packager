import glob, os
import sys
from zipfile import ZipFile

def create_install_list_gz(dir):
    """ Installs insall list for tar.gz files """
    print("----tar.gz files------")
    os.chdir(f'{dir}/downloads/')
    for file_name in glob.glob('*.gz'):
        with open(f'{dir}/package_gz_list.txt','a') as f:
            working_dir = os.getcwd()
            f.write(f"extracted_packages/gz/{file_name}\n")
            print(f"extracted_packages/gz/{file_name}")

def create_install_list_whl(dir):
    """ Installs insall list for whl files """
    print("----whl files------")
    os.chdir(f'{dir}/downloads/')
    for file_name in glob.glob('*.whl'):
        if "py3" in file_name:
            with open(f'{dir}/package_whl_list.txt','a') as f:
                working_dir = os.getcwd()
                f.write(f"extracted_packages/whl/{file_name}\n")
                print(f"extracted_packages/whl/{file_name}")


def package(dir):
    """ Packages tar.gz and whl files + create install list """
    # printing the list of all files to be zipped
    print('files in downoads directory  will be zipped: ')
    create_install_list_gz(dir)
    os.chdir(f'{dir}/downloads/')
    print('ZIPPING .gz files as python_gz_packages.zip')
    with ZipFile(f'{dir}/python_gz_packages.zip','w') as zip:
        # writing each file one by one
        for file_name in glob.glob("*.gz"):
            zip.write(file_name)
    create_install_list_whl(dir)
    os.chdir(f'{dir}/downloads/')
    print('ZIPPING .whl files as python_whl_packages.zip')
    with ZipFile(f'{dir}/python_whl_packages.zip','w') as zip:
        # writing each file one by one
        for file_name in glob.glob("*.whl"):
            if "py3" in file_name:
                zip.write(file_name)
    print("All files zipped successfully!")


def install_packages_whl(dir):
    """ install whl packages """
    os.chdir(f'{dir}/extracted_packages/whl/')
    os.system(f'python3.8 -m pip3 install *.whl')

def install_packages_tar(dir):
    """ install tar.gz packages """
    file_name = []
    os.chdir(f'{dir}/extracted_packages/gz/')
    print("im here")
    with open(f'{dir}/package_gz_list.txt','r') as f:
        line = f.readline()
        cnt = 1
        while line:
            line = f.readline()
            if line == '':
                break
            print(f"Extracting {line}!")
            os.system(f'tar -xvzf {dir}/{line}')
            new_dir = line.replace('.tar.gz\n','')
            if new_dir == '':
                return 1 
            print(f"Installing {new_dir}")
            os.chdir(f'{dir}/{new_dir}')
            os.system(f'python3.8 -m pip3 install .')
            os.chdir(f'{dir}/extracted_packages/gz/')
            cnt += 1
    print("DONE!!") 


def write_requirements(dir):
    """ write pip packages to requirements.txt """
    os.system('python3.8 -m pip3 freeze > requirements.txt')

def download_packages(dir):
    """ download pip packages reading requirements.txt """
    print("creating downloads directory")
    os.system('mkdir downloads >/dev/null 2>&1')
    print("downloading packages")
    os.system('python3.8 -m pip3 download -r requirements.txt -d ./downloads >/dev/null 2>&1')
    print("DONE. Please see requirements.txt for package details")

def print_help():
    """ prints command line help """
    print('''
            command:
                python packager.py [option]
            options:
                -p list, download and zip packages, and creates "package_list.txt"
                -z zip only -- "./downloads" directory must exist
                -d list and download packages only
                -r list packages only
                -u unzip "python_packages.zip"
                -i unzip and install from "python_packages.zip" using package_list.txt
                [IMPORTANT: MAKE SURE YOUR ARE USING PYTHON3.8]
            ''')

    pass

def unzip_gz_packages(dir):
    """ Unzip tar.gz packages """
    print("creating directory")
    os.system(f'mkdir {dir}/extracted_packages/gz >/dev/null 2>&1')
    with ZipFile(f'{dir}/python_gz_packages.zip','r') as zipObj:
        zipObj.extractall(f'{dir}/extracted_packages/gz')
    print(f"Extracted in -TARGET_DIR={dir}/extracted_packages/gz")

def unzip_whl_packages(dir):
    """ Unzip whl packages """
    print("creating directory")
    os.system(f'mkdir {dir}/extracted_packages/whl >/dev/null 2>&1')
    with ZipFile(f'{dir}/python_whl_packages.zip','r') as zipObj:
        zipObj.extractall(f'{dir}/extracted_packages/whl')
    print(f"Extracted in -TARGET_DIR={dir}/extracted_packages/whl")

def unzip_main(dir):
    """ Unzip main tar.gz file """
    print("creating directory")
    os.system(f'mkdir {dir}/extracted_packages >/dev/null 2>&1')
    with ZipFile(f'{dir}/python_packages.zip','r') as zipObj:
        zipObj.extractall(f'{dir}/extracted_packages')
    print(f"Extracted in -TARGET_DIR={dir}/extracted_packages")

def invalid():
    """ print out in case of invalid arguments """
    print('Invalid number of Arguments... Exiting!')
    print_help()
    sys.exit()

def main():
    """ main method """
    arguments = len(sys.argv) -1
    #output argument-wise
    position = 1
    main_dir = os.getcwd()

    if (arguments > 1 or arguments == 0):
        invalid()

    if sys.argv[position] == '-p':
        print("---list, download and zip packages---")

        print("wrting requirements.txt")
        write_requirements(main_dir)

        print("downloading packages -- TARGET_DIR=./downloads ")
        download_packages(main_dir)

        print("Packaging")
        package(main_dir)

    elif sys.argv[position] == '-z':
        print("---zip packages only---")

        print("Packaging -TARGET_DIR=./downloads ")
        package(main_dir)


    elif sys.argv[position] == '-d':
        print("---list and download packages only---")

        print("wrting requirements.txt")
        write_requirements(main_dir)

        print("downloading packages -- TARGET_DIR=./downloads/ ")
        download_packages(main_dir)

    elif sys.argv[position] == '-r':
        print("---list packages only---")
        print("wrting requirements.txt")
        write_requirements(main_dir)

    elif sys.argv[position] == '-u':
        print("---unzip 'python_gz_packages.zip'---")
        unzip_gz_packages(main_dir)
        print("---unzip 'python_gz_packages.zip'---")
        unzip_whl_packages(main_dir)
        
    elif sys.argv[position] == '-i':
        print("---unzip and install from 'python_packages.zip'")
        unzip_gz_packages(main_dir)
          
        print("---unzip and install from 'python_packages.zip'")
        #unzip_packages(main_dir)
        unzip_whl_packages(main_dir)
        
        print("Installing packages")
        install_packages_tar(main_dir)
       
        print("Installing packages")
        install_packages_whl(main_dir)
    
    elif sys.argv[position] == '-t':
        print("---TEST ")
        create_install_list_gz(main_dir)
        create_install_list_whl(main_dir)

    else:
        invalid()

    


if __name__ == '__main__':
    main()
