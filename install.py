import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask==1.1.2'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-math'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask-Cors==3.0.10'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'werkzeug==0.16.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'jinja2==3.0.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'itsdangerous==2.0.1'])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)