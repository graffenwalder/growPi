import os
from datetime import datetime
from ftplib import FTP
import subprocess
import secrets

mp4File = 'timelapse.mp4'
localImagePath = "/root/growpi/images/"

def getAllImages():
    start = datetime.now()
    ftp = FTP(secrets.FTP_URL)
    ftp.login(user=secrets.USERNAME, passwd=secrets.PASSWORD)
    ftp.cwd('/images/')
    # Get All Files
    files = ftp.nlst()
    files.remove('..')
    #print(files)

    # Print out the files
    for file in files:
        if not os.path.isfile(file):
            print('Downloading...' + file)
            ftp.retrbinary('RETR ' + file, open(localImagePath + file, 'wb').write)
        else:
            print(file + ' Already exists')

    ftp.close()
    end = datetime.now()
    diff = end - start
    print('All files downloaded for ' + str(diff.seconds) + 's')


def uploadMP4():
    ftp = FTP(secrets.FTP_URL)
    ftp.login(user=secrets.USERNAME, passwd=secrets.PASSWORD)
    ftp.storbinary('STOR ' + mp4File, open(mp4File, 'rb'))
    print("Succesfully uploaded: " + mp4File)
    ftp.quit()


def makeTimelapse(frames=5):
    p = subprocess.Popen(['ffmpeg', '-r', '{}'.format(frames), '-pattern_type', 'glob' ,'-i', '*.jpg', '-c:v', 'libx264', mp4File, '-y'])
    p.wait()
    print("Created: " + mp4File)

def main():
    os.chdir(localImagePath)
    getAllImages()
    makeTimelapse(24)
    uploadMP4()

if __name__ == '__main__':
    main()
