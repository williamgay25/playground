import subprocess

def download_video(filename: str, url: str) -> dict:
    command = ['udown', '-f', filename, url]
    try:
        result = subprocess.run(
            command,
            shell=False,
            capture_output=True,
            text=True,
            check=True
        )
        return {
            'success': True,
            'output': result.stdout,
            'error': result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'output': e.stdout,
            'error': e.stderr
        }

if __name__ == '__main__':
    filenames = ['ajff.mp4', 'drum.mp4', 'hypernorm.mp4', 'bobbyken.mp4', 'markfisher.mp4', 'jbearly.mp4']
    urls = ['https://www.youtube.com/watch?v=AOCQp6lAfEE', 'https://www.youtube.com/watch?v=GiPe1OiKQuk', 'https://www.youtube.com/watch?v=AUiqaFIONPQ&t=80s', 'https://www.youtube.com/watch?v=DOiDUbaBL9E', 'https://www.youtube.com/watch?v=aCgkLICTskQ&t=602s', 'https://www.youtube.com/watch?v=rWRbTnE1PEM']
    
    for filename, url  in zip(filenames, urls):
        download_video(filename, url)