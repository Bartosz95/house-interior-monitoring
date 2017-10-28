import picamera  # obsluga kamery
import user_conf_file  # plik z informacjami od uzytkownika
import os  # sciezka do pliku
import datetime
import paramiko


def recording_video():
    video_data = datetime.datetime.now()
    path_to_video = os.path.abspath('.') + '/VIDEO/' + video_data.strftime("%y.%m.%d") + '/' + user_conf_file.cam_name + \
                     '/' + video_data.strftime(user_conf_file.data_format) + '.' + user_conf_file.video_format

    if os.path.isdir(os.path.dirname(path_to_video)) == False: os.makedirs(os.path.dirname(path_to_video))

    camera = picamera.PiCamera()
    camera.resolution = (user_conf_file.video_resolution_x, user_conf_file.video_resolution_y)
    camera.start_recording(path_to_video)
    camera.wait_recording(user_conf_file.video_time)
    camera.stop_recording()

    print("recording succesfully!")
    return video_data


def server_connect(video_data, remotepath):
    end_of_path = '/VIDEO/' + video_data.strftime("%y.%m.%d") + '/' + user_conf_file.cam_name + \
                     '/' + video_data.strftime(user_conf_file.data_format) + '.' + user_conf_file.video_format
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(user_conf_file.server_hostname,
                port=user_conf_file.server_port,
                username=user_conf_file.server_username,
                password=user_conf_file.server_password)
    sftp = ssh.open_sftp()

    if sftp.chdir(os.path.dirname(remotepath + end_of_path +'/')) == False:
        print("Nie istnieje")
    else: print("istnieje")


    #sftp.mkdir(os.path.dirname(remotepath + end_of_path))

    #sftp.put(os.path.abspath('.') + end_of_path, remotepath + end_of_path)
    sftp.close()
    ssh.close()
    print("connect succesfully!")


#try:
video_data = recording_video()
server_connect(video_data, user_conf_file.video_path)
#except Exception as ex:
#    print(ex)