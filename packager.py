import glob, os
import sys
from zipfile import ZipFile

def create_install_list(dir):
    os.chdir(f'{dir}/downloads/')
    for file_name in glob.glob('*.gz'):
        with open(f'{dir}/package_list.txt','a') as f:
            working_dir = os.getcwd()
            f.write(f"{dir}/extracted_packages/{file_name}\n")
            print(f"{dir}/extracted_packages/{file_name}")

def package(dir):

    # printing the list of all files to be zipped
    print('files in downoads directory  will be zipped: ')

    create_install_list(dir)

    #os.chdir('./downloads/')
        # writing files to a zipfile
    os.chdir(f'{dir}/downloads/')
    print('ZIPPING .whl files as python_packages.zip')
    with ZipFile(f'{dir}/python_packages.zip','w') as zip:
        
        # writing each file one by one
        for file in glob.glob("*.gz"):
            zip.write(file)

    print("All files zipped successfully!")

def write_requirements(dir):
    os.system('python3 -m pip freeze > requirements.txt')

def download_packages(dir):
    print("creating downloads directory")
    os.system('mkdir downloads >/dev/null 2>&1')
    print("downloading packages")
    os.system('python3 -m pip download -r requirements.txt -d ./downloads >/dev/null 2>&1')
    print("DONE. Please see requirements.txt for package details")

def print_help():
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

def unzip_packages(dir):
    print("creating directory")
    os.system(f'mkdir {dir}/extracted_packages >/dev/null 2>&1')
    with ZipFile(f'{dir}/python_packages.zip','r') as zipObj:
        zipObj.extractall(f'{dir}/extracted_packages')
    print(f"Extracted in -TARGET_DIR={dir}/extracted_packages")

def install_packages_whl(dir):
    os.chdir(f'{dir}/extracted_packages/')
    os.system(f'python3 -m pip install -r {dir}/package_list.txt')

def install_packages_tar(dir):
    file_name = []
    os.chdir(f'{dir}/extracted_packages/')
    with open(f'{dir}/package_list.txt','r') as f:
        line = f.readline()
        cnt = 1
        while line:
            line = f.readline()
            print(f"Extracting {line}!")
            os.system(f'tar -xvzf {line}')
            new_dir = line.replace('.tar.gz\n','')
            if new_dir == '':
                return 1 
            print(f"Installing {new_dir}")
            os.chdir(f'{new_dir}')
            os.system(f'python3 -m pip install .')
            os.chdir(f'{dir}/extracted_packages/')
            cnt += 1
    print("DONE!!") 


def invalid():
    print('Invalid number of Arguments... Exiting!')
    print_help()
    sys.exit()

def main():
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
        print("---unzip 'python_packages.zip'---")
        unzip_packages(main_dir)
        
    elif sys.argv[position] == '-i':
        print("---unzip and install from 'python_packages.zip'")
        unzip_packages(main_dir)
        
        print("Installing packages")
        #install_packages(main_dir)
        install_packages_tar(main_dir)
    
    elif sys.argv[position] == '-t':
        print("---TEST ")
        create_install_list(main_dir)

    else:
        invalid()

    


if __name__ == '__main__':
    main()
